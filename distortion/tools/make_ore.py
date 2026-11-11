#!/usr/bin/env python3
"""
Distortion Crystal ore: stone and deepslate variants, a little rarer than coal at coal's heights (y 0-192), mined
with at least a stone pickaxe, dropping 2-4 Distortion Shards (Fortune adds more; Silk Touch keeps the ore). Shards
craft the Distortion Crystal (4 shards round an amethyst shard) and the Distortion Band (gold, shards and a crystal).
Textures are painted here (original art). Run by make_assets.py (or alone).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "common" / "src" / "main" / "resources"
MOD = "cobbleeffort_distortion"
A = RES / "assets" / MOD
D = RES / "data" / MOD
ORES = ["distortion_crystal_ore", "deepslate_distortion_crystal_ore"]

LANG = {
    f"block.{MOD}.distortion_crystal_ore": "Distortion Crystal Ore",
    f"block.{MOD}.deepslate_distortion_crystal_ore": "Deepslate Distortion Crystal Ore",
    f"item.{MOD}.distortion_shard": "Distortion Shard",
}


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")


def h(*a):
    v = 2166136261
    for x in a:
        v = ((v ^ (int(x) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return v / 0xFFFFFFFF


def clamp(c):
    return tuple(max(0, min(255, int(round(v)))) for v in c) + (255,)


# crystal colours: the Distortion World's violet-black with a magenta glint (shiny-ish teal accents)
CRYSTAL = [(40, 16, 60), (92, 36, 140), (160, 70, 220), (236, 170, 255)]


def rock(base, streaks):
    """A stone texture: mottled grey, darker cracks (deepslate: horizontal streaks)."""
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            k = 0.88 + 0.22 * h(x // 2, y // 2, 3) + 0.08 * (h(x, y, 5) - 0.5)
            if streaks and (y + int(2 * h(x // 4, 1))) % 5 == 0:
                k *= 0.82
            if not streaks and h(x, y, 9) > 0.93:
                k *= 0.7
            im.putpixel((x, y), clamp([c * k for c in base]))
    return im


def crystals(im, seed):
    """Clusters of faceted crystals breaking through the rock."""
    spots = [(4, 4, 2.6), (11, 6, 2.2), (6, 11, 2.4), (12, 12, 1.8)]
    for cx, cy, r in spots:
        for y in range(16):
            for x in range(16):
                dx, dy = x - cx, y - cy
                d = abs(dx) + abs(dy) * 0.8                    # a diamond: a facet look
                if d <= r:
                    t = d / r
                    idx = 3 if t < 0.2 and dx <= 0 else 2 if t < 0.55 else 1
                    if dx > 0 and dy > 0:
                        idx = max(0, idx - 1)                  # the shaded facet
                    im.putpixel((x, y), CRYSTAL[idx] + (255,))
                elif d <= r + 0.8:
                    im.putpixel((x, y), CRYSTAL[0] + (255,))   # the dark rim
    return im


def shard():
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(2, 15):
        for x in range(3, 13):
            # a long faceted shard, leaning right
            c = 8 + (y - 8) * 0.25
            w = 3.6 * (1 - abs(y - 8.5) / 7.5)
            if abs(x - c) <= w:
                left = x < c
                t = abs(x - c) / max(w, 0.1)
                idx = 3 if (left and t < 0.35 and y < 9) else 2 if left else 1
                if t > 0.8:
                    idx = 0
                im.putpixel((x, y), CRYSTAL[idx] + (255,))
    return im


def build():
    stone = crystals(rock((126, 126, 126), False), 1)
    deep = crystals(rock((78, 78, 84), True), 2)
    for name, img in (("distortion_crystal_ore", stone), ("deepslate_distortion_crystal_ore", deep)):
        p = A / "textures" / "block" / f"{name}.png"
        p.parent.mkdir(parents=True, exist_ok=True)
        img.save(p, optimize=True)
    (A / "textures" / "item").mkdir(parents=True, exist_ok=True)
    shard().save(A / "textures" / "item" / "distortion_shard.png", optimize=True)
    for ore in ORES:
        write_json(A / "blockstates" / f"{ore}.json", {"variants": {"": {"model": f"{MOD}:block/{ore}"}}})
        write_json(A / "models" / "block" / f"{ore}.json", {"parent": "minecraft:block/cube_all",
                                                         "textures": {"all": f"{MOD}:block/{ore}"}})
        write_json(A / "models" / "item" / f"{ore}.json", {"parent": f"{MOD}:block/{ore}"})
        # 2-4 shards, more with Fortune (like a vanilla ore), the ore itself with Silk Touch
        write_json(D / "loot_table" / "blocks" / f"{ore}.json", {"type": "minecraft:block", "pools": [{"rolls": 1, "entries": [{
            "type": "minecraft:alternatives", "children": [
                {"type": "minecraft:item", "name": f"{MOD}:{ore}", "conditions": [{"condition": "minecraft:match_tool", "predicate": {
                    "predicates": {"minecraft:enchantments": [{"enchantments": "minecraft:silk_touch", "levels": {"min": 1}}]}}}]},
                {"type": "minecraft:item", "name": f"{MOD}:distortion_shard", "functions": [
                    {"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 2, "max": 4}},
                    {"function": "minecraft:apply_bonus", "enchantment": "minecraft:fortune", "formula": "minecraft:ore_drops"},
                    {"function": "minecraft:explosion_decay"}]}]}]}]})
        for kind, cook in (("smelting", 200), ("blasting", 100)):
            write_json(D / "recipe" / f"distortion_shard_from_{kind}_{ore}.json", {
                "type": f"minecraft:{kind}", "category": "misc", "ingredient": {"item": f"{MOD}:{ore}"},
                "result": {"id": f"{MOD}:distortion_shard"}, "experience": 0.7, "cookingtime": cook})
    write_json(A / "models" / "item" / "distortion_shard.json", {"parent": "minecraft:item/generated",
                                                                "textures": {"layer0": f"{MOD}:item/distortion_shard"}})
    tags = RES / "data" / "minecraft" / "tags" / "block"
    pick = json.loads((tags / "mineable" / "pickaxe.json").read_text()) if (tags / "mineable" / "pickaxe.json").exists() else {"replace": False, "values": []}
    pick["values"] = sorted(set(pick["values"]) | {f"{MOD}:{o}" for o in ORES})
    write_json(tags / "mineable" / "pickaxe.json", pick)
    write_json(tags / "needs_stone_tool.json", {"replace": False, "values": [f"{MOD}:{o}" for o in ORES]})
    # world generation: veins a bit smaller and fewer than coal's lower band (coal: 20 veins of 17, y 0-192)
    write_json(D / "worldgen" / "configured_feature" / "distortion_crystal_ore.json", {"type": "minecraft:ore", "config": {
        "size": 12, "discard_chance_on_air_exposure": 0.0, "targets": [
            {"target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"},
             "state": {"Name": f"{MOD}:distortion_crystal_ore"}},
            {"target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:deepslate_ore_replaceables"},
             "state": {"Name": f"{MOD}:deepslate_distortion_crystal_ore"}}]}})
    write_json(D / "worldgen" / "placed_feature" / "distortion_crystal_ore.json", {
        "feature": f"{MOD}:distortion_crystal_ore", "placement": [
            {"type": "minecraft:count", "count": 16}, {"type": "minecraft:in_square"},
            {"type": "minecraft:height_range", "height": {"type": "minecraft:trapezoid",
                                                          "min_inclusive": {"absolute": 0}, "max_inclusive": {"absolute": 192}}},
            {"type": "minecraft:biome"}]})
    # recipes: the crystal (4 shards round an amethyst shard) and the band (gold, shards, a crystal)
    write_json(D / "recipe" / "distortion_crystal.json", {
        "type": "minecraft:crafting_shaped", "category": "misc", "pattern": [" S ", "SAS", " S "],
        "key": {"S": {"item": f"{MOD}:distortion_shard"}, "A": {"item": "minecraft:amethyst_shard"}},
        "result": {"id": f"{MOD}:distortion_crystal", "count": 1}})
    write_json(D / "recipe" / "distortion_band.json", {
        "type": "minecraft:crafting_shaped", "category": "misc", "pattern": ["GSG", "SCS", "GSG"],
        "key": {"G": {"item": "minecraft:gold_ingot"}, "S": {"item": f"{MOD}:distortion_shard"}, "C": {"item": f"{MOD}:distortion_crystal"}},
        "result": {"id": f"{MOD}:distortion_band", "count": 1}})


if __name__ == "__main__":
    build()
