#!/usr/bin/env python3
"""
The Liquor Meadows (0.8.0, the user's design): a tipsy overworld biome of extra-vibrant grass under clear skies, water
the colour of whisky, and giant bottles of drink sticking out of the ground at odd angles instead of trees. The
blocks, features and biome patches are code (Liquor.java, GiantBottleFeature, MultiNoiseBiomeSourceMixin); this
writes the rest: the biome (vanilla plains' carvers, caves, ores and grass/flower features, no trees), whisky ponds,
its configured and placed features, block textures (cork, bottle cap, bottle label), models, blockstates, loot, tags
and lang. Run by make_assets.py.
"""
from __future__ import annotations

import random

from make_ashtray import A, D, MOD, RES, add_tag, clamp, write_json

from PIL import Image

LANG: dict[str, str] = {}
BLOCKS = ["cork", "bottle_cap", "bottle_label"]
BIOME = "liquor_meadows"


def tex_cork(rng):
    img = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            c = (196 + rng.randint(-10, 10), 150 + rng.randint(-10, 10), 98 + rng.randint(-8, 8))
            if rng.random() < 0.18:
                c = (150, 104, 62)                                     # dark cork pits
            elif rng.random() < 0.07:
                c = (226, 186, 132)
            img.putpixel((x, y), clamp(c) + (255,))
    return img


def tex_cap(rng):
    img = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            crimp = (x // 2) % 2 == 0                                  # crimped ridges
            g = 1.0 if crimp else 0.82
            c = tuple(v * g + rng.randint(-6, 6) for v in (232, 190, 70))
            if y in (0, 15):
                c = (168, 128, 40)
            img.putpixel((x, y), clamp(c) + (255,))
    return img


def tex_label(rng):
    img = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            g = 236 + rng.randint(-5, 5)
            c = (g, g - 8, g - 26)                                     # cream paper
            if y in (2, 13):
                c = (170, 40, 40)                                      # printed rules
            elif 5 <= y <= 10 and 3 <= x <= 12 and (x + y) % 3 == 0:
                c = (60, 50, 44)                                       # lettering
            img.putpixel((x, y), clamp(c) + (255,))
    return img


def biome():
    ores = ["minecraft:ore_dirt", "minecraft:ore_gravel", "minecraft:ore_granite_upper", "minecraft:ore_granite_lower",
            "minecraft:ore_diorite_upper", "minecraft:ore_diorite_lower", "minecraft:ore_andesite_upper",
            "minecraft:ore_andesite_lower", "minecraft:ore_tuff", "minecraft:ore_coal_upper", "minecraft:ore_coal_lower",
            "minecraft:ore_iron_upper", "minecraft:ore_iron_middle", "minecraft:ore_iron_small", "minecraft:ore_gold",
            "minecraft:ore_gold_lower", "minecraft:ore_redstone", "minecraft:ore_redstone_lower", "minecraft:ore_diamond",
            "minecraft:ore_diamond_medium", "minecraft:ore_diamond_large", "minecraft:ore_diamond_buried",
            "minecraft:ore_lapis", "minecraft:ore_lapis_buried", "minecraft:ore_copper", "minecraft:underwater_magma",
            "minecraft:disk_sand", "minecraft:disk_clay", "minecraft:disk_gravel"]
    # vanilla plains' features in plains' order (feature order must agree across biomes), its trees left out, ours last
    features = [
        [],
        ["minecraft:lake_lava_underground", "minecraft:lake_lava_surface", f"{MOD}:liquor_pond"],
        ["minecraft:amethyst_geode"],
        ["minecraft:monster_room", "minecraft:monster_room_deep"],
        [], [],
        ores,
        [],
        ["minecraft:spring_water", "minecraft:spring_lava"],
        ["minecraft:glow_lichen", "minecraft:patch_tall_grass_2", "minecraft:flower_plains", "minecraft:patch_grass_plain",
         "minecraft:patch_sugar_cane", "minecraft:patch_pumpkin", f"{MOD}:giant_bottle", f"{MOD}:fallen_bottle"],
        ["minecraft:freeze_top_layer"],
    ]
    creature = [{"type": f"minecraft:{t}", "weight": w, "minCount": a, "maxCount": b} for t, w, a, b in (
        ("sheep", 12, 4, 4), ("pig", 10, 4, 4), ("chicken", 10, 4, 4), ("cow", 8, 4, 4), ("horse", 5, 2, 6),
        ("donkey", 1, 1, 3))]
    monster = [{"type": f"minecraft:{t}", "weight": w, "minCount": a, "maxCount": b} for t, w, a, b in (
        ("spider", 100, 4, 4), ("zombie", 95, 4, 4), ("zombie_villager", 5, 1, 1), ("skeleton", 100, 4, 4),
        ("creeper", 100, 4, 4), ("slime", 100, 4, 4), ("enderman", 10, 1, 4), ("witch", 5, 1, 1))]
    write_json(D / "worldgen" / "biome" / f"{BIOME}.json", {
        "has_precipitation": False, "temperature": 0.9, "downfall": 0.4,
        "effects": {"sky_color": 0x62B0FF, "fog_color": 0xCDE6FF,
                    "water_color": 0xC9802A, "water_fog_color": 0x7A4210,     # whisky
                    "grass_color": 0x3FE53A, "foliage_color": 0x2FD94C,       # extra vibrant
                    "mood_sound": {"sound": "minecraft:ambient.cave", "tick_delay": 6000, "block_search_extent": 8,
                                   "offset": 2.0}},
        "carvers": {"air": ["minecraft:cave", "minecraft:cave_extra_underground", "minecraft:canyon"]},
        "features": features,
        "spawners": {"monster": monster, "creature": creature, "ambient": [{"type": "minecraft:bat", "weight": 10,
                                                                            "minCount": 8, "maxCount": 8}],
                     "axolotls": [], "underground_water_creature": [{"type": "minecraft:glow_squid", "weight": 10,
                                                                      "minCount": 4, "maxCount": 6}],
                     "water_creature": [], "water_ambient": [], "misc": []},
        "spawn_costs": {}})
    for name in ("giant_bottle", "fallen_bottle"):
        write_json(D / "worldgen" / "configured_feature" / f"{name}.json", {"type": f"{MOD}:{name}", "config": {}})
    write_json(D / "worldgen" / "configured_feature" / "liquor_pond.json", {"type": "minecraft:lake", "config": {
        "barrier": {"type": "minecraft:simple_state_provider", "state": {"Name": "minecraft:grass_block",
                                                                         "Properties": {"snowy": "false"}}},
        "fluid": {"type": "minecraft:simple_state_provider", "state": {"Name": "minecraft:water",
                                                                       "Properties": {"level": "0"}}}}})
    surface = [{"type": "minecraft:in_square"}, {"type": "minecraft:heightmap", "heightmap": "WORLD_SURFACE_WG"},
               {"type": "minecraft:biome"}]
    write_json(D / "worldgen" / "placed_feature" / "giant_bottle.json", {"feature": f"{MOD}:giant_bottle",
        "placement": [{"type": "minecraft:rarity_filter", "chance": 2}] + surface})
    write_json(D / "worldgen" / "placed_feature" / "fallen_bottle.json", {"feature": f"{MOD}:fallen_bottle",
        "placement": [{"type": "minecraft:rarity_filter", "chance": 2}] + surface})
    write_json(D / "worldgen" / "placed_feature" / "liquor_pond.json", {"feature": f"{MOD}:liquor_pond",
        "placement": [{"type": "minecraft:rarity_filter", "chance": 3}] + surface})
    add_tag(RES / "data" / "minecraft" / "tags" / "worldgen" / "biome" / "is_overworld.json", [f"{MOD}:{BIOME}"])
    write_json(D / "tags" / "worldgen" / "biome" / "is_liquor.json", {"replace": False, "values": [f"{MOD}:{BIOME}"]})


def build():
    rng = random.Random(11)
    tex = A / "textures" / "block"
    tex.mkdir(parents=True, exist_ok=True)
    tex_cork(rng).save(tex / "cork.png")
    tex_cap(rng).save(tex / "bottle_cap.png")
    tex_label(rng).save(tex / "bottle_label.png")
    for b in BLOCKS:
        write_json(A / "blockstates" / f"{b}.json", {"variants": {"": {"model": f"{MOD}:block/{b}"}}})
        write_json(A / "models" / "block" / f"{b}.json", {"parent": "minecraft:block/cube_all",
                                                         "textures": {"all": f"{MOD}:block/{b}"}})
        write_json(A / "models" / "item" / f"{b}.json", {"parent": f"{MOD}:block/{b}"})
        write_json(D / "loot_table" / "blocks" / f"{b}.json", {"type": "minecraft:block", "pools": [{
            "rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{MOD}:{b}"}],
            "conditions": [{"condition": "minecraft:survives_explosion"}]}]})
    add_tag(RES / "data" / "minecraft" / "tags" / "block" / "mineable" / "axe.json", [f"{MOD}:cork"])
    add_tag(RES / "data" / "minecraft" / "tags" / "block" / "mineable" / "pickaxe.json", [f"{MOD}:bottle_cap"])
    LANG.update({f"block.{MOD}.cork": "Cork", f"block.{MOD}.bottle_cap": "Bottle Cap",
                 f"block.{MOD}.bottle_label": "Bottle Label", f"biome.{MOD}.{BIOME}": "Liquor Meadows"})
    biome()


if __name__ == "__main__":
    build()
