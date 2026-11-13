"""Nest structures for CobbleEffort's bird Pokémon (data only).

  pinbird_nest  a rocky crag in open country (plains, meadows, savannas, windswept hills) with a spiral of ledges up
                its side and a great hay nest on top, a chest of berries and feathers in the middle. The pinbird line
                (Pinlet, Pinnant, Pennacrest) spawns only at these nests.

Written like the fossil structures (fossils.write_structure, the Kanto add-on's NBT writer).
"""
from __future__ import annotations

import math

from fossils import MOD, RES, Template, h, write_json, write_structure

LOOT = {
    "pinbird_nest": [
        {"rolls": {"min": 3, "max": 6}, "entries": [
            {"type": "minecraft:item", "name": "minecraft:feather", "weight": 6,
             "functions": [{"function": "minecraft:set_count", "count": {"min": 1, "max": 4}}]},
            {"type": "minecraft:item", "name": "minecraft:wheat", "weight": 4,
             "functions": [{"function": "minecraft:set_count", "count": {"min": 2, "max": 6}}]},
            {"type": "minecraft:item", "name": "minecraft:wheat_seeds", "weight": 3,
             "functions": [{"function": "minecraft:set_count", "count": {"min": 2, "max": 5}}]},
            {"type": "minecraft:item", "name": "minecraft:sweet_berries", "weight": 3,
             "functions": [{"function": "minecraft:set_count", "count": {"min": 1, "max": 4}}]},
            {"type": "minecraft:item", "name": "cobblemon:oran_berry", "weight": 3},
            {"type": "minecraft:item", "name": "cobblemon:pecha_berry", "weight": 3},
            {"type": "minecraft:item", "name": "cobblemon:cheri_berry", "weight": 2},
            {"type": "minecraft:item", "name": "cobblemon:razz_berry", "weight": 2},
            {"type": "minecraft:item", "name": "cobblemon:sitrus_berry", "weight": 1},
            {"type": "minecraft:item", "name": "minecraft:egg", "weight": 2}]},
        {"rolls": 1, "entries": [
            {"type": "minecraft:item", "name": "cobblemon:sharp_beak", "weight": 1},
            {"type": "minecraft:item", "name": "cobblemon:poke_ball", "weight": 3,
             "functions": [{"function": "minecraft:set_count", "count": {"min": 1, "max": 3}}]},
            {"type": "minecraft:empty", "weight": 6}]}],
}


def pinbird_nest():
    W, H = 17, 19
    c = W // 2
    top = 13
    t = Template((W, H, W))
    rocks = ["minecraft:stone", "minecraft:andesite", "minecraft:cobblestone", "minecraft:tuff",
             "minecraft:mossy_cobblestone", "minecraft:stone"]
    for y in range(top + 1):                                              # a rough crag, leaning a little and tapering
        r = 6.8 - 0.3 * y
        cx, cz = c + 0.06 * y, c - 0.04 * y
        for x in range(W):
            for z in range(W):
                d = math.hypot(x - cx, z - cz)
                lump = (h(x // 2, y // 2, z // 2) - 0.5) * 2.2 + (h(x, y, z) - 0.5) * 0.8
                if d < r + lump:
                    t.set(x, y, z, rocks[int(h(x, z, y, 3) * len(rocks)) % len(rocks)])
    for i in range(18):                                                   # a spiral of ledges up its side
        a = i * 0.9
        y = 1 + int(i * 0.68)
        r = 7.3 - 0.3 * y
        x, z = round(c + 0.06 * y + r * math.cos(a)), round(c - 0.04 * y + r * math.sin(a))
        if 0 <= x < W and 0 <= z < W and y < top and (x, y, z) not in t.blocks and (x, y - 1, z) not in t.blocks:
            t.set(x, y, z, "minecraft:stone_slab", {"type": "bottom", "waterlogged": "false"})
    nx, nz = c + 0.06 * top, c - 0.04 * top
    for x in range(W):                                                    # the great hay nest, overhanging the top
        for z in range(W):
            d = math.hypot(x - nx, z - nz)
            if d < 5.6:
                t.set(x, top + 1, z, "minecraft:hay_block", {"axis": "y"})
            if 3.4 < d < 5.6:
                ax = "x" if abs(x - nx) < abs(z - nz) else "z"
                t.set(x, top + 2, z, "minecraft:hay_block", {"axis": ax})
                if 4.0 < d < 5.3 and h(x, z, 9) > 0.4:
                    t.set(x, top + 3, z, "minecraft:hay_block", {"axis": "z" if ax == "x" else "x"})
            if 5.0 < d < 5.9 and h(x, z, 11) > 0.55:
                t.set(x, top, z, "minecraft:hay_block", {"axis": "y"})      # straw hanging over the edge
    t.set(round(nx), top + 2, round(nz), "minecraft:chest", {"facing": "north", "type": "single", "waterlogged": "false"},
          {"id": "minecraft:chest", "LootTable": f"{MOD}:chests/pinbird_nest"})
    return t


STRUCTURES = {
    "pinbird_nest": {"build": pinbird_nest,
                     "biomes": ["minecraft:plains", "minecraft:sunflower_plains", "minecraft:meadow",
                                "minecraft:savanna", "minecraft:savanna_plateau", "minecraft:windswept_savanna",
                                "minecraft:windswept_hills", "minecraft:windswept_gravelly_hills"],
                     "step": "surface_structures", "adapt": "beard_thin", "height": {"absolute": 0},
                     "project": "WORLD_SURFACE_WG", "spacing": 26, "separation": 9, "salt": 30245},
}


def build(lang):
    data = RES / "data" / MOD
    for name, pools in LOOT.items():
        write_json(data / "loot_table" / "chests" / f"{name}.json", {"type": "minecraft:chest", "pools": pools})
    for name, s in STRUCTURES.items():
        write_structure(name, s, "nest")
