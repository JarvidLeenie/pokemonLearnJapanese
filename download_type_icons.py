#!/usr/bin/env python3
"""
Download type icons and update types_info.json with local paths
"""

import json
import requests
import pathlib
import os
from urllib.parse import urlparse

def download_type_icons():
    """Download type icons and update types_info.json"""
    
    # Load the types info
    with open('types_info.json', 'r', encoding='utf-8') as f:
        types_data = json.load(f)
    
    # Create images directory if it doesn't exist
    images_dir = pathlib.Path('images')
    images_dir.mkdir(exist_ok=True)
    
    # Download each type icon
    for type_name, type_info in types_data.items():
        if 'icon_url' in type_info and type_info['icon_url']:
            icon_url = type_info['icon_url']
            
            # Extract filename from URL
            parsed_url = urlparse(icon_url)
            filename = os.path.basename(parsed_url.path)
            
            # Create local path
            local_path = f"images/{filename}"
            
            # Download the icon
            try:
                print(f"Downloading {type_name} icon: {filename}")
                response = requests.get(icon_url, headers={
                    'User-Agent': 'PokemonTypeIconDownloader/1.0'
                })
                response.raise_for_status()
                
                # Save the icon
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                
                # Update the types_info.json with local path
                types_data[type_name]['icon_url'] = local_path
                
                print(f"  ✓ Downloaded to {local_path}")
                
            except Exception as e:
                print(f"  ✗ Failed to download {type_name} icon: {e}")
    
    # Save the updated types_info.json
    with open('types_info.json', 'w', encoding='utf-8') as f:
        json.dump(types_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nUpdated types_info.json with local icon paths")

if __name__ == "__main__":
    download_type_icons() 