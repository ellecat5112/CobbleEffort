#!/usr/bin/env python3
"""Writes the item list of the "CobbleEffort" creative inventory tab (src/main/resources/cobbleeffort_creative_tab.json).

The tab (src/main/java/io/github/cobbleeffort/CreativeTab.java) shows each collection's cosmetic items, by collection
number (from tools/collections/*.json). Each entry is an item stack in the 1.21.1 format; one the game can't make is
simply left out of the tab. Run by generate.py build.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RES = ROOT / "src" / "main" / "resources"
MOD = "cobbleeffort"


def main():
    configs = [json.loads(p.read_text()) for p in sorted((HERE / "collections").glob("*.json"))]
    configs.sort(key=lambda c: c.get("readme", {}).get("number", 999))
    items, seen = [], set()
    for cfg in configs:
        for item in cfg["cosmetic_items"]:
            if item not in seen:
                seen.add(item)
                items.append({"id": item, "count": 1})
    icon = items[0]                                     # the first collection's item
    out = RES / f"{MOD}_creative_tab.json"
    out.write_text(json.dumps({"icon": icon, "items": items}, indent=1) + "\n")
    lang = RES / "assets" / MOD / "lang" / "en_us.json"
    data = json.loads(lang.read_text())
    data[f"itemGroup.{MOD}"] = "CobbleEffort"
    lang.write_text(json.dumps(dict(sorted(data.items())), indent=1) + "\n")
    print(f"creative tab: {len(items)} items")


if __name__ == "__main__":
    main()
