#!/usr/bin/env python3
"""
Add hiragana readings to Pokemon JSON data
Converts katakana names to hiragana for pronunciation
"""

import json

def katakana_to_hiragana(text):
    """Convert katakana to hiragana"""
    katakana_to_hiragana_map = {
        'ア': 'あ', 'イ': 'い', 'ウ': 'う', 'エ': 'え', 'オ': 'お',
        'カ': 'か', 'キ': 'き', 'ク': 'く', 'ケ': 'け', 'コ': 'こ',
        'サ': 'さ', 'シ': 'し', 'ス': 'す', 'セ': 'せ', 'ソ': 'そ',
        'タ': 'た', 'チ': 'ち', 'ツ': 'つ', 'テ': 'て', 'ト': 'と',
        'ナ': 'な', 'ニ': 'に', 'ヌ': 'ぬ', 'ネ': 'ね', 'ノ': 'の',
        'ハ': 'は', 'ヒ': 'ひ', 'フ': 'ふ', 'ヘ': 'へ', 'ホ': 'ほ',
        'マ': 'ま', 'ミ': 'み', 'ム': 'む', 'メ': 'め', 'モ': 'も',
        'ヤ': 'や', 'ユ': 'ゆ', 'ヨ': 'よ',
        'ラ': 'ら', 'リ': 'り', 'ル': 'る', 'レ': 'れ', 'ロ': 'ろ',
        'ワ': 'わ', 'ヲ': 'を', 'ン': 'ん',
        'ガ': 'が', 'ギ': 'ぎ', 'グ': 'ぐ', 'ゲ': 'げ', 'ゴ': 'ご',
        'ザ': 'ざ', 'ジ': 'じ', 'ズ': 'ず', 'ゼ': 'ぜ', 'ゾ': 'ぞ',
        'ダ': 'だ', 'ヂ': 'ぢ', 'ヅ': 'づ', 'デ': 'で', 'ド': 'ど',
        'バ': 'ば', 'ビ': 'び', 'ブ': 'ぶ', 'ベ': 'べ', 'ボ': 'ぼ',
        'パ': 'ぱ', 'ピ': 'ぴ', 'プ': 'ぷ', 'ペ': 'ぺ', 'ポ': 'ぽ',
        'ァ': 'ぁ', 'ィ': 'ぃ', 'ゥ': 'ぅ', 'ェ': 'ぇ', 'ォ': 'ぉ',
        'ャ': 'ゃ', 'ュ': 'ゅ', 'ョ': 'ょ',
        'ッ': 'っ',
        'ー': 'ー'  # Long vowel mark stays the same
    }
    
    result = ""
    for char in text:
        result += katakana_to_hiragana_map.get(char, char)
    
    return result

def process_pokemon_data():
    """Process Pokemon data to add hiragana readings"""
    
    # Load the original Pokemon data
    with open('pokemon_base_0001_1025.json', 'r', encoding='utf-8') as f:
        pokemon_data = json.load(f)
    
    # Process each Pokemon
    for pokemon in pokemon_data:
        ndex = pokemon['ndex']
        kana_name = pokemon['kanaName']
        
        # Convert katakana to hiragana
        hiragana = katakana_to_hiragana(kana_name)
        
        # Add the hiragana field
        pokemon['hiragana'] = hiragana
        
        print(f"{ndex:03d}: {kana_name} -> {hiragana}")
    
    # Save the updated data
    with open('pokemon_base_0001_1025_with_hiragana.json', 'w', encoding='utf-8') as f:
        json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nProcessed {len(pokemon_data)} Pokemon")
    print("Saved to pokemon_base_0001_1025_with_hiragana.json")

if __name__ == '__main__':
    process_pokemon_data() 