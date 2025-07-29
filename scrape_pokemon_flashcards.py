#!/usr/bin/env python3
"""
scrape_pokemon_flashcards.py  –  July 2025

Scrape Bulbapedia master list and JP wiki to generate JSON
for Pokémon Japanese flashcards.

Outputs:
  • pokemon_base_<start>_<end>.json
  • name_origins_<start>_<end>.json

Example:
    python scrape_pokemon_flashcards.py 1 12
"""

import sys, json, time, random, re, pathlib, requests, urllib
from urllib.parse import unquote
from bs4 import BeautifulSoup
from json.decoder import JSONDecodeError

BASE  = "https://bulbapedia.bulbagarden.net"
API   = BASE + "/w/api.php"
LIST  = BASE + "/wiki/List_of_Japanese_Pok%C3%A9mon_names"
HEAD  = { "User-Agent": "PokemonFlashcardsBot/0.3 (contact@example.com)" }
JP_CHARS = r"[一-龯ぁ-んァ-ヶ]"

CACHE = pathlib.Path("cache")
CACHE.mkdir(exist_ok=True)

def cfile(name: str) -> pathlib.Path:
    return CACHE / name

def wait(): time.sleep(0.3)

# ------------------ robust API ------------------
def api_json(params, *, cache=None, retries=3):
    path = cfile(cache) if cache else None
    if path and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))

    for _ in range(retries):
        wait()
        resp = requests.get(API, params=params, headers=HEAD, timeout=20)
        try:
            data = resp.json()
        except JSONDecodeError:
            time.sleep(5 + random.random())
            continue
        if "error" in data:
            print("API error", data["error"].get("code"), "for", params.get("page"))
            return None
        if path:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return data
    return None

# ------------------ master list -----------------
def list_html() -> str:
    p = cfile("list.html")
    if p.exists():
        return p.read_text(encoding="utf-8")
    wait()
    html = requests.get(LIST, headers=HEAD, timeout=20).text
    p.write_text(html, encoding="utf-8")
    return html

def parse_master(start: int, end: int) -> list[dict]:
    """Return rows 001 … end_ndex from ALL generation tables."""
    print("start", start)
    print("end", end)
    soup = BeautifulSoup(list_html(), "html.parser")

    # collect every table whose header row contains “Ndex”
    tables = [
        tbl for tbl in soup.find_all("table")
        if tbl.find("th") and "Ndex" in tbl.find("th").get_text(strip=True)
    ]

    rows_out = []

    data= []
    for table in tables:

        rows = table.select("tbody tr")[2:]
        for tr in rows:
            td = tr.find_all("td")
            if len(td) < 6:
                continue

            ndex_txt = re.sub(r"\D", "", td[0].get_text(strip=True))
            if not ndex_txt:
                continue
            ndex = int(ndex_txt)
            if ndex < start:
                continue
            if ndex > end:
                break

            img = tr.find("img")
            if not img:
                continue
            img_url = ("https:" + img["src"]) if img["src"].startswith("//") else img["src"]

            print("td", td)

            english    = td[2].get_text(strip=True)   # Bulbasaur
            kana_td    = td[3]
            kana_name  = kana_td.get_text(strip=True)  # フシギダネ
            romaji     = td[4].get_text(strip=True)   # Fushigidane
            trademark  = td[5].get_text(strip=True)   # same value on Gen-I rowsk
            print("english", english)
            print("kana_name", kana_name)
            print("romaji", romaji)
            print("trademark", trademark)   

            jp_anchor = kana_td.find("a", href=True)
            print("jp_anchor", jp_anchor)

            if jp_anchor and jp_anchor.has_attr("data-url"):
                jp_page = jp_anchor["data-url"]                # ext-link supplied
                print("jp_page", jp_page)
            else:
                kana_q  = urllib.parse.quote(kana_name)
                jp_page = f"https://wiki.xn--rckteqa2e.com/wiki/{kana_q}"
                print("jp_page", jp_page)


            en_anchor = td[1].find("a", href=True)
            en_page   = BASE + en_anchor["href"] if en_anchor else ""


            data.append({
                "ndex": ndex,
                "english": english,
                "kanaName": kana_name,
                "hepburnName": romaji,          # Fushigidane
                "publishedName": trademark,       # trademarked EN
                "imageUrl": img_url,
                "link": en_page,
                "jpPage": jp_page
            })


    print("data", data)
    return data

# ------------------ Name origin ----------------
def origin_html(slug: str) -> str:
    meta = api_json({"action":"parse","page":slug,"prop":"sections",
                     "format":"json","formatversion":2}, cache=f"idx_{slug}.json")
    if not meta:
        return ""
    idx = next((s["index"] for s in meta["parse"]["sections"]
                if s["line"].lower().startswith("name origin")), None)
    if idx is None:
        return ""
    sec = api_json({"action":"parse","page":slug,"prop":"text","section":idx,
                    "format":"json","formatversion":2},
                   cache=f"sec_{slug}_{idx}.json")
    return sec["parse"]["text"] if sec else ""

def clean_origin(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    paras = [p.get_text(" ", strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
    if not paras:
        return ""
    jp = [p for p in paras if re.search(JP_CHARS, p)]
    keep = jp if jp else (paras[:2] if len(paras) > 1 else paras[:1])
    return "  ".join(keep)

# ------------------ JP wiki elements ----------
import re, urllib.parse, pathlib, requests
from bs4 import BeautifulSoup

import re, urllib.parse, pathlib, requests
from bs4 import BeautifulSoup

def jp_elements(url: str) -> list[str]:
    """
    Return a list like
        ["フシギダネ", "不思議", "種"]
    or for Butterfree:
        ["バタフリー", "butterfly (英語: 蝶)", "free (英語: 自由な)"]
    """
    if not url:
        return []

    cache = cfile("jp_" + pathlib.Path(url).name + ".html")
    if cache.exists():
        html = cache.read_text(encoding="utf-8")
    else:
        try:
            wait()
            html = requests.get(url, headers=HEAD, timeout=15).text  # 15-s hard cap
        except requests.exceptions.RequestException as exc:
            print("⚠️  JP page fetch failed:", url.split('/')[-1], exc)
            return []               # silently skip this Pokémon
        cache.write_text(html, encoding="utf-8")

    soup = BeautifulSoup(html, "html.parser")

    # find the heading 「名称と由来」 then the first table after it
    heading = soup.find(lambda tag: tag.name in {"h2", "h3"}
                        and "名称と由来" in tag.get_text())
    if not heading:
        return []

    tbl = heading.find_next("table")
    if not tbl:
        return []

    # first <tr> that actually has an origin cell (>=3 <td>)
    row = next((tr for tr in tbl.find_all("tr") if len(tr.find_all("td")) >= 3), None)
    if not row:
        return []

    cells = row.find_all("td")
    if len(cells) < 4:
        return []

    # Get Japanese name (column 3) and etymology elements (column 4)
    japanese_name = cells[2].get_text(strip=True)
    origin_cell = cells[3].get_text(strip=True)

    # split on 、 (primary) or ・ / • (fallback)
    parts = re.split(r"[、・•]", origin_cell)
    etymology_elements = [p.strip() for p in parts if p.strip()]
    
    # Return both the Japanese name and etymology elements
    return [japanese_name] + etymology_elements
 

# ------------------ orchestrator -------------
def scrape(start: int, end: int):
    base = [r for r in parse_master(start, end) if start <= r["ndex"] <= end]
    origins = {}
    for row in base:
        slug = unquote(pathlib.Path(row["link"]).name)
        desc = clean_origin(origin_html(slug))
        elements = jp_elements(row["jpPage"])
        origins[row["ndex"]] = {
            "nameOriginDescription": desc,
            "nameOriginElements": elements
        }
    return base, origins

def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    end   = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    base, orig = scrape(start, end)
    tag = f"{start:04d}_{end:04d}"
    with open(f"pokemon_base_{tag}.json", "w", encoding="utf-8") as f:
        json.dump(base, f, ensure_ascii=False, indent=2)
    with open(f"name_origins_{tag}.json", "w", encoding="utf-8") as f:
        json.dump(orig, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(base)} Pokémon (Ndex {start}-{end}).")

if __name__ == "__main__":
    main()

