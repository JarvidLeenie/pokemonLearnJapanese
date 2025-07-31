#!/usr/bin/env python3
"""
Extract TCG types and Pokémon TCG type information from Bulbapedia
Scrapes the TCG type page for type information and individual Pokémon TCG pages for their types
"""

import json
import requests
import re
import time
import pathlib
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Constants
BASE_URL = "https://bulbapedia.bulbagarden.net"
HEADERS = {
    "User-Agent": "PokemonTCGTypeExtractor/1.0 (contact@example.com)"
}

def get_page_content(url, cache_name=None):
    """Get page content with caching"""
    cache_dir = pathlib.Path("cache")
    cache_dir.mkdir(exist_ok=True)
    
    if cache_name:
        cache_file = cache_dir / f"{cache_name}.html"
        if cache_file.exists():
            print(f"Using cached {cache_name}")
            return cache_file.read_text(encoding='utf-8')
    
    print(f"Downloading {url}")
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    
    if cache_name:
        cache_file.write_text(response.text, encoding='utf-8')
    
    return response.text

def extract_tcg_types_from_page(html_content):
    """Extract TCG types and their colors from the TCG type page"""
    soup = BeautifulSoup(html_content, 'html.parser')
    tcg_types = {}
    
    # Look for the table that contains TCG types
    # The table should have "TCG" as the first column header
    tables = soup.find_all('table')
    
    for table in tables:
        # Look for a table with "TCG" in the header
        headers = table.find_all('th')
        if headers and any('TCG' in header.get_text() for header in headers):
            # Found the TCG types table
            rows = table.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    # First cell should contain the type name
                    type_cell = cells[0]
                    type_name = type_cell.get_text(strip=True)
                    
                    if type_name and type_name not in ['TCG', 'Type']:
                        # Get the background color from the cell
                        style = type_cell.get('style', '')
                        color_match = re.search(r'background:\s*(#[0-9A-Fa-f]{6})', style)
                        color = color_match.group(1) if color_match else None
                        
                        # Look for an icon in the cell
                        icon_img = type_cell.find('img')
                        icon_url = None
                        if icon_img:
                            icon_url = icon_img.get('src')
                            if icon_url and not icon_url.startswith('http'):
                                icon_url = urljoin(BASE_URL, icon_url)
                        
                        tcg_types[type_name] = {
                            'name': type_name,
                            'color': color,
                            'icon_url': icon_url
                        }
            
            break
    
    return tcg_types

def extract_pokemon_tcg_type_from_page(html_content, pokemon_name):
    """Extract TCG type from a Pokémon's TCG page"""
    soup = BeautifulSoup(html_content, 'html.parser')
    tcg_type = None
    
    # Look for the table that contains card information
    # The type is usually in a table with card details
    tables = soup.find_all('table')
    
    for table in tables:
        # Look for a table that contains type information
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            
            # Look for a cell that contains type information
            for cell in cells:
                # Check if this cell contains a type icon
                type_img = cell.find('img', alt=re.compile(r'(Grass|Fire|Water|Electric|Psychic|Fighting|Darkness|Metal|Colorless|Fairy)', re.IGNORECASE))
                if type_img:
                    # Extract the type from the alt text or surrounding text
                    alt_text = type_img.get('alt', '')
                    if alt_text:
                        tcg_type = alt_text.strip()
                        break
            
            if tcg_type:
                break
        
        if tcg_type:
            break
    
    return tcg_type

def main():
    """Main function to extract TCG types and Pokémon TCG types"""
    
    print("Extracting TCG types and colors...")
    
    # Get TCG types page
    tcg_types_url = f"{BASE_URL}/wiki/Type_(TCG)"
    tcg_types_html = get_page_content(tcg_types_url, "tcg_types_page")
    
    # Extract TCG types
    tcg_types = extract_tcg_types_from_page(tcg_types_html)
    
    if tcg_types:
        # Save TCG types info
        with open('tcg_types_info.json', 'w', encoding='utf-8') as f:
            json.dump(tcg_types, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(tcg_types)} TCG types to tcg_types_info.json")
        print("TCG types found:", list(tcg_types.keys()))
    else:
        print("No TCG types found!")
        return
    
    # Now extract TCG types for each Pokémon
    print("\nExtracting TCG types for Pokémon...")
    
    # Load Pokémon data
    with open('pokemon_base_0001_1025_with_types.json', 'r', encoding='utf-8') as f:
        pokemon_data = json.load(f)
    
    # Process each Pokémon
    pokemon_with_tcg_types = []
    
    # Process all Pokémon
    for pokemon in pokemon_data:
        pokemon_name = pokemon['english'].lower()
        
        # Construct TCG page URL
        tcg_page_url = f"{BASE_URL}/wiki/{pokemon['english']}_(TCG)"
        
        # Get TCG page
        cache_name = f"tcg_{pokemon_name}"
        try:
            tcg_html = get_page_content(tcg_page_url, cache_name)
            tcg_type = extract_pokemon_tcg_type_from_page(tcg_html, pokemon['english'])
            
            # Add TCG type to Pokémon data
            pokemon_with_tcg_types.append({
                **pokemon,
                'tcg_type': tcg_type
            })
            
            if tcg_type:
                print(f"{pokemon['english']}: {tcg_type}")
            else:
                print(f"{pokemon['english']}: No TCG type found")
            
            # Small delay to be respectful
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error processing {pokemon['english']}: {e}")
            # Add Pokémon without TCG type
            pokemon_with_tcg_types.append({
                **pokemon,
                'tcg_type': None
            })
    
    # Save Pokémon data with TCG types
    with open('pokemon_base_0001_1025_with_tcg_types.json', 'w', encoding='utf-8') as f:
        json.dump(pokemon_with_tcg_types, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved Pokémon data with TCG types for {len(pokemon_with_tcg_types)} Pokémon")

if __name__ == "__main__":
    main() 