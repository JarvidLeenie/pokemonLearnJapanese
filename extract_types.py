#!/usr/bin/env python3
"""
Extract Pokémon types and type information from Bulbapedia
Scrapes individual Pokémon pages for their types and the main type page for type details
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
    "User-Agent": "PokemonTypeExtractor/1.0 (contact@example.com)"
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

def extract_type_info_from_types_page(html_content):
    """Extract type information from the main types page"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Look for the types in the sidebar or main content
    types_info = {}
    
    # Find type elements with their colors
    # Look for patterns like: background: #3FA129 for Grass, etc.
    type_patterns = {
        'Normal': '#9FA19F',
        'Fire': '#E62829', 
        'Water': '#2980EF',
        'Electric': '#F8D030',
        'Grass': '#3FA129',
        'Ice': '#3DCEF3',
        'Fighting': '#FF8000',
        'Poison': '#9141CB',
        'Ground': '#915121',
        'Flying': '#81B9EF',
        'Psychic': '#EF4179',
        'Bug': '#91A119',
        'Rock': '#AFA981',
        'Ghost': '#704170',
        'Dragon': '#7038F8',
        'Dark': '#504843',
        'Steel': '#60A1B8',
        'Fairy': '#EF70EF'
    }
    
    # Look for type icons and names in the page
    for type_name, color in type_patterns.items():
        # Look for type elements with this background color
        type_elements = soup.find_all(attrs={'style': re.compile(f'background.*{color}', re.IGNORECASE)})
        
        if type_elements:
            # Find the type name within these elements
            for element in type_elements:
                type_link = element.find('a', href=re.compile(f'/{type_name}_\\(type\\)'))
                if type_link:
                    # Extract icon URL if available
                    icon_img = element.find('img')
                    icon_url = None
                    if icon_img and icon_img.get('src'):
                        icon_url = urljoin(BASE_URL, icon_img['src'])
                    
                    types_info[type_name] = {
                        'name': type_name,
                        'color': color,
                        'icon_url': icon_url
                    }
                    break
    
    print(f"Found {len(types_info)} types from types page")
    return types_info

def extract_pokemon_types_from_page(html_content, pokemon_name):
    """Extract Pokémon types from the infobox Type section"""
    soup = BeautifulSoup(html_content, 'html.parser')
    types = []
    
    # Valid Pokémon types
    valid_types = {
        'Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 
        'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 
        'Dragon', 'Dark', 'Steel', 'Fairy'
    }
    
    # Look for the infobox with class "roundy infobox"
    infobox = soup.find('table', class_='roundy infobox')
    if not infobox:
        return types
    
    # Find the Type section in the infobox
    type_section = None
    for row in infobox.find_all('tr'):
        # Look for the row that contains "Type" in bold
        type_header = row.find('b')
        if type_header and 'Type' in type_header.get_text():
            type_section = row
            break
    
    if not type_section:
        return types
    
    # Find the type cells in the Type section
    # Look for td elements with background colors (type buttons)
    type_cells = type_section.find_all('td', style=lambda style: style and 'background:' in style)
    
    for cell in type_cells:
        # Extract the type name from the link text
        type_link = cell.find('a')
        if type_link:
            type_name = type_link.get_text(strip=True)
            # Only add if it's a valid type and not already in the list
            if type_name in valid_types and type_name not in types:
                types.append(type_name)
    
    return types

def main():
    """Main function to extract types and Pokémon type information"""
    
    # Load existing Pokémon data
    with open('pokemon_base_0001_1025.json', 'r', encoding='utf-8') as f:
        pokemon_data = json.load(f)
    
    print("Extracting type information...")
    
    # Get types page
    types_url = f"{BASE_URL}/wiki/Type"
    types_html = get_page_content(types_url, "types_page")
    types_info = extract_type_info_from_types_page(types_html)
    
    # Save type information
    with open('types_info.json', 'w', encoding='utf-8') as f:
        json.dump(types_info, f, indent=2, ensure_ascii=False)
    
    print(f"Saved type information for {len(types_info)} types")
    
    print("\nExtracting Pokémon types...")
    
    # Process each Pokémon
    pokemon_with_types = []
    
    for pokemon in pokemon_data:
        pokemon_name = pokemon['english'].lower()
        pokemon_url = pokemon.get('link', '')
        
        if not pokemon_url:
            print(f"No URL found for {pokemon['english']}")
            continue
        
        # Get Pokémon page
        cache_name = f"pokemon_{pokemon_name}"
        try:
            pokemon_html = get_page_content(pokemon_url, cache_name)
            pokemon_types = extract_pokemon_types_from_page(pokemon_html, pokemon['english'])
            
            # Add types to Pokémon data
            pokemon_with_types.append({
                **pokemon,
                'types': pokemon_types
            })
            
            # Small delay to be respectful
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Error processing {pokemon['english']}: {e}")
            # Add Pokémon without types
            pokemon_with_types.append({
                **pokemon,
                'types': []
            })
    
    # Save Pokémon data with types
    with open('pokemon_base_0001_1025_with_types.json', 'w', encoding='utf-8') as f:
        json.dump(pokemon_with_types, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved Pokémon data with types for {len(pokemon_with_types)} Pokémon")
    
    # Print summary
    type_counts = {}
    for pokemon in pokemon_with_types:
        for pokemon_type in pokemon['types']:
            type_counts[pokemon_type] = type_counts.get(pokemon_type, 0) + 1
    
    print("\nType distribution:")
    for pokemon_type, count in sorted(type_counts.items()):
        print(f"  {pokemon_type}: {count} Pokémon")

if __name__ == "__main__":
    main() 