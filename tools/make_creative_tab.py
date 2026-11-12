#!/usr/bin/env python3
"""Writes the item list of the "CobbleEffort" creative inventory tab (src/main/resources/cobbleeffort_creative_tab.json).

The tab (src/main/java/io/github/cobbleeffort/CreativeTab.java) shows, in order: each collection's cosmetic items
(by collection number, from tools/collections/*.json) and then every Paradox mega stone (from tools/megas/build.py,
the same stacks their recipes make). Each entry is an item stack in the 1.21.1 format; one the game can't make
(a mega stone without Mega Showdown) is simply left out of the tab. Run by generate.py build and tools/megas/build.py.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RES = ROOT / "src" / "main" / "resources"
MOD = "cobbleeffort"
sys.path.insert(0, str(HERE / "megas"))


def main():
    import build as megas
    configs = [json.loads(p.read_text()) for p in sorted((HERE / "collections").glob("*.json"))]
    configs.sort(key=lambda c: c.get("readme", {}).get("number", 999))
    items, seen = [], set()
    for cfg in configs:
        for item in cfg["cosmetic_items"]:
            if item not in seen:
                seen.add(item)
                items.append({"id": item, "count": 1})
    stones = [{"id": "minecraft:amethyst_shard", "count": 1, "components": megas.stone_components(sp)} for sp in megas.built()]
    items += stones
    fossils = HERE / "newmons" / "creative_items.json"         # CobbleEffort's fossil items (tools/newmons/fossils.py)
    if fossils.exists():
        items += json.loads(fossils.read_text())
    # the icon: the first stone's look only (no Mega Showdown components, so it shows without that mod too)
    icon = ({"id": "minecraft:amethyst_shard", "count": 1,
             "components": {"minecraft:custom_model_data": stones[0]["components"]["minecraft:custom_model_data"]}}
            if stones else items[0])
    out = RES / f"{MOD}_creative_tab.json"
    out.write_text(json.dumps({"icon": icon, "items": items}, indent=1) + "\n")
    lang = RES / "assets" / MOD / "lang" / "en_us.json"
    data = json.loads(lang.read_text())
    data[f"itemGroup.{MOD}"] = "CobbleEffort"
    lang.write_text(json.dumps(dict(sorted(data.items())), indent=1) + "\n")
    print(f"creative tab: {len(items)} items")


if __name__ == "__main__":
    main()
