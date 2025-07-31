#!/usr/bin/env python3
"""
Clean footnote references from Pokemon name origin descriptions
Removes patterns like [ 1 ], [ 2 ], [ 3 ] etc. from nameOriginDescription fields
"""

import json
import re

def clean_footnotes(text):
    """Remove footnote references from text"""
    # Remove patterns like [ 1 ], [ 2 ], [ 3 ] etc.
    # This regex matches [ followed by spaces, digits, and spaces, then ]
    cleaned = re.sub(r'\s*\[\s*\d+\s*\]\s*', ' ', text)
    
    # Clean up any double spaces that might result
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # Trim leading/trailing whitespace
    cleaned = cleaned.strip()
    
    return cleaned

def process_name_origins():
    """Process name origins data to remove footnote references"""
    
    # Load the original name origins data
    with open('name_origins_0001_1025.json', 'r', encoding='utf-8') as f:
        origins_data = json.load(f)
    
    cleaned_count = 0
    
    # Process each Pokemon's etymology data
    for pokemon_id, etymology in origins_data.items():
        if 'nameOriginDescription' in etymology:
            original_desc = etymology['nameOriginDescription']
            cleaned_desc = clean_footnotes(original_desc)
            
            # Only update if there was a change
            if cleaned_desc != original_desc:
                etymology['nameOriginDescription'] = cleaned_desc
                cleaned_count += 1
                print(f"Pokemon {pokemon_id}: Cleaned footnote references")
                print(f"  Before: {original_desc[:100]}...")
                print(f"  After:  {cleaned_desc[:100]}...")
                print()
    
    # Save the cleaned data
    with open('name_origins_0001_1025_cleaned.json', 'w', encoding='utf-8') as f:
        json.dump(origins_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nProcessed {len(origins_data)} Pokemon entries")
    print(f"Cleaned footnote references from {cleaned_count} descriptions")
    print("Saved to name_origins_0001_1025_cleaned.json")

if __name__ == '__main__':
    process_name_origins() 