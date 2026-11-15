"""Digimon facts from wikimon.net (the user's chosen source for the crossover's evolutions): levels, attributes,
types, fields, weight, variants, attack technique names and the Evolves From / Evolves To lists.

    python3 tools/digimon/wikimon.py fetch A [B ...]     # page wikitext -> the cache (scratch, never committed)
    python3 tools/digimon/wikimon.py parse               # cache -> tools/digimon/data/wikimon.json (facts only)
    python3 tools/digimon/wikimon.py image <Name> ...    # reference art -> the cache (to model from; never shipped)

Only facts are committed (names, levels, evolution links), never wikimon's text or images. Evolution entries that
are card-game catch-alls ("Any Red Lv.2 Digimon ...") are dropped; each kept entry records whether only Digimon Card
Game cards back it (`card`), whether it is bold on wikimon (`main`: the usual line), a DNA partner (`with`) and a
Warp Evolution (`warp`: skipping stages).
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "wikimon.json"
CACHE = Path(os.environ.get("WIKIMON_CACHE", "/tmp/wikimon_cache"))
API = "https://wikimon.net/api.php"
UA = {"User-Agent": "CobbleEffort-research/1.0"}


def api(**params):
    url = API + "?" + urllib.parse.urlencode(dict(params, format="json"))
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())


def page_path(name):
    return CACHE / "pages" / (name.replace("/", "_") + ".json")


def fetch(letters):
    (CACHE / "pages").mkdir(parents=True, exist_ok=True)
    lst = CACHE / "list.json"
    if not lst.exists():
        lst.write_text(json.dumps(api(action="parse", page="List_of_Digimon", prop="wikitext")))
    t = json.loads(lst.read_text())["parse"]["wikitext"]["*"]
    secs = re.split(r"^==([A-Z0-9#]+)==\s*$", t, flags=re.M)
    by = {secs[i]: re.findall(r"\|n=([^\n|]+)", secs[i + 1]) for i in range(1, len(secs), 2)}
    (CACHE / "list_by_letter.json").write_text(json.dumps(by, ensure_ascii=False))
    for letter in letters:
        for n in by.get(letter, []):
            p = page_path(n)
            if p.exists():
                continue
            p.write_text(json.dumps(api(action="parse", page=n, prop="wikitext", redirects=1)))
            time.sleep(1.0)
        print(letter, len(by.get(letter, [])), "pages")


def field(t, key):
    m = re.search(r"^\|" + re.escape(key) + r"=([^\n]*)", t, re.M)
    if not m:
        return None
    v = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>|\{\{[^{}]*\}\}", "", m.group(1)).strip()
    return v or None


def numbered(t, key, n=12):
    out = []
    for i in range(1, n + 1):
        v = field(t, f"{key}{i}")
        if v and v not in out:
            out.append(re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", v))
    return out


def section(t, title):
    m = re.search(r"^==\s*" + re.escape(title) + r"\s*==\s*$(.*?)(?=^=)", t, re.M | re.S)
    return m.group(1) if m else ""


def evolutions(text):
    out = []
    for line in text.splitlines():
        if not line.startswith("*"):
            continue
        m = re.search(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]", line)
        if not m or m.group(1).startswith(("Digimon Card Game", "Evolution")) or "Any " in line[:m.end() + 8]:
            continue
        target = m.group(1).strip()
        refs = re.findall(r"\{\{(?:ref|rfc)\|([^}]*)\}\}", line)
        card = bool(refs) and all("DCG" in r for r in refs)
        partner = None
        rest = line[m.end():]
        w = re.search(r"with\s+(?:'''\s*)?\[\[([^\]|#]+)", rest)
        if w and not w.group(1).startswith("Evolution"):
            partner = w.group(1).strip()
        out.append({"name": target, "main": line[:m.start()].rstrip().endswith("'''"), "card": card,
                    **({"with": partner} if partner else {}), **({"warp": True} if "Warp Evolution" in rest else {})})
    seen, uniq = set(), []
    for e in out:
        k = (e["name"], e.get("with"))
        if k not in seen:
            seen.add(k)
            uniq.append(e)
    return uniq


def techniques(t):
    m = re.search(r"^=Attack Techniques=\s*$(.*?)(?=^=[^=])", t, re.M | re.S)
    if not m:
        return []
    names = re.findall(r"^\|name\d*=([^\n]+)", m.group(1), re.M)
    return [re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", n).strip() for n in names]


def parse():
    facts = {}
    for p in sorted((CACHE / "pages").glob("*.json")):
        d = json.loads(p.read_text())
        if "parse" not in d:
            continue
        t = d["parse"]["wikitext"]["*"]
        name = d["parse"]["title"]
        facts[name] = {
            "levels": numbered(t, "l"), "attributes": numbered(t, "a"), "types": numbered(t, "t"),
            "fields": numbered(t, "f"), "groups": numbered(t, "g"), "weight": field(t, "w"),
            "image": field(t, "image"), "variants": numbered(t, "s", 30),
            "techniques": techniques(t),
            "from": evolutions(section(t, "Evolves From")), "to": evolutions(section(t, "Evolves To")),
        }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(facts, indent=1, ensure_ascii=False, sort_keys=True) + "\n")
    print(len(facts), "Digimon ->", OUT)


def image(names):
    (CACHE / "images").mkdir(parents=True, exist_ok=True)
    facts = json.loads(OUT.read_text())
    for n in names:
        f = facts[n]["image"]
        info = api(action="query", titles="File:" + f, prop="imageinfo", iiprop="url")
        url = next(iter(info["query"]["pages"].values()))["imageinfo"][0]["url"]
        dst = CACHE / "images" / (n.replace("/", "_").replace(":", "") + os.path.splitext(f)[1])
        dst.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        print(dst)
        time.sleep(0.5)


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    {"fetch": fetch, "parse": lambda _: parse(), "image": image}[cmd](args)
