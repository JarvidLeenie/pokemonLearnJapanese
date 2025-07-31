#!/usr/bin/env python3
"""
Clean up Pokémon types in JSON file
Remove invalid entries like "Type", "Unknown", etc. from types arrays
"""

import json

def clean_types():
    """Clean up types arrays in the JSON file"""
    
    # Valid Pokémon types
    valid_types = {
        'Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 
        'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 
        'Dragon', 'Dark', 'Steel', 'Fairy'
    }
    
    # Load the JSON file
    with open('pokemon_base_0001_1025_with_types.json', 'r', encoding='utf-8') as f:
        pokemon_data = json.load(f)
    
    # Clean up each Pokémon's types
    cleaned_count = 0
    for pokemon in pokemon_data:
        if 'types' in pokemon:
            original_types = pokemon['types']
            # Filter out invalid types
            cleaned_types = [t for t in original_types if t in valid_types]
            
            if cleaned_types != original_types:
                pokemon['types'] = cleaned_types
                cleaned_count += 1
                print(f"Cleaned {pokemon['english']}: {original_types} -> {cleaned_types}")
    
    # Save the cleaned data
    with open('pokemon_base_0001_1025_with_types.json', 'w', encoding='utf-8') as f:
        json.dump(pokemon_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nCleaned types for {cleaned_count} Pokémon")
    
    # Show some examples
    print("\nExamples of cleaned types:")
    for i, pokemon in enumerate(pokemon_data[:5]):
        print(f"{pokemon['english']}: {pokemon.get('types', [])}")

if __name__ == "__main__":
    clean_types() 