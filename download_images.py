#!/usr/bin/env python3
"""
download_images.py - Download Pokémon images and update JSON

Downloads images from imageUrl fields in pokemon_base JSON files
and updates the imageUrl to point to local files.
"""

import json
import requests
import pathlib
import time
import sys
from urllib.parse import urlparse

def download_image(url: str, local_path: pathlib.Path) -> bool:
    """Download an image from URL to local path."""
    try:
        headers = {
            "User-Agent": "PokemonFlashcardsBot/0.3 (contact@example.com)"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        local_path.write_bytes(response.content)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def process_json_file(json_file: str):
    """Process a JSON file, download images, and update imageUrl fields."""
    
    # Create images directory
    images_dir = pathlib.Path("images")
    images_dir.mkdir(exist_ok=True)
    
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Processing {len(data)} Pokémon...")
    
    success_count = 0
    failed_count = 0
    
    for pokemon in data:
        ndex = pokemon["ndex"]
        english_name = pokemon["english"]
        image_url = pokemon["imageUrl"]
        
        # Extract filename from URL
        parsed_url = urlparse(image_url)
        filename = pathlib.Path(parsed_url.path).name
        
        # Create local path
        local_path = images_dir / filename
        
        print(f"Downloading {ndex:04d} {english_name}...")
        
        # Download the image
        if download_image(image_url, local_path):
            # Update the imageUrl to point to local file
            pokemon["imageUrl"] = f"images/{filename}"
            success_count += 1
        else:
            failed_count += 1
        
        # Small delay to be respectful to the server
        time.sleep(0.1)
    
    # Save the updated JSON
    output_file = json_file.replace('.json', '_with_local_images.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nDownload complete!")
    print(f"Successfully downloaded: {success_count}")
    print(f"Failed downloads: {failed_count}")
    print(f"Updated JSON saved to: {output_file}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python download_images.py <json_file>")
        print("Example: python download_images.py pokemon_base_0001_1025.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    if not pathlib.Path(json_file).exists():
        print(f"Error: File {json_file} not found")
        sys.exit(1)
    
    process_json_file(json_file)

if __name__ == "__main__":
    main() 