#!/usr/bin/env python3
"""
The Ashtray Wastes (0.7.0, the user's design): a nicotine-blighted overworld biome of ash and tar where giant
cigarettes stick out of the ground. The blocks, features and the biome patches are code (Ashtray.java,
AshtraySurfaceFeature, GiantCigaretteFeature, MultiNoiseBiomeSourceMixin); this writes the rest: the biome (vanilla
desert's carvers, caves and ores, no trees or plants but dead bushes), its configured and placed features, block
textures (ash, cigarette paper, filter, a flickering ember), models, blockstates, loot, tags and lang. Run by
make_assets.py.
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "common" / "src" / "main" / "resources"
MOD = "cobbleeffort_kanto"
A = RES / "assets" / MOD
D = RES / "data" / MOD
LANG: dict[str, str] = {}
BLOCKS = ["ash", "cigarette_paper", "cigarette_filter", "cigarette_ember"]


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def add_tag(path: Path, values):
    """Add values to a tag file, keeping what is already there (other parts of the build write the same tags)."""
    old = json.loads(path.read_text()).get("values", []) if path.exists() else []
    write_json(path, {"replace": False, "values": sorted(set(old) | set(values))})


def clamp(c):
    return tuple(max(0, min(255, int(round(v)))) for v in c)


def tex_ash(rng):
    img = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            g = 128 + rng.randint(-18, 18)
            c = (g + 4, g, g - 4)
            if rng.random() < 0.08:
                c = (70, 66, 64)                                       # dark flecks of burnt tobacco
            elif rng.random() < 0.06:
                c = (188, 184, 178)                                    # pale flakes
            img.putpixel((x, y), clamp(c) + (255,))
    return img


def tex_paper(rng):
    img = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            g = 238 + rng.randint(-5, 5) - (6 if x % 5 == 0 else 0)     # faint fibres
            c = (g, g, g - 3)
            if rng.random() < 0.02:
                c = (214, 200, 168)                                    # a nicotine stain
            img.putpixel((x, y), clamp(c) + (255,))
    return img


def tex_filter(rng):
    img = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            c = (214 + rng.randint(-8, 8), 140 + rng.randint(-8, 8), 70 + rng.randint(-6, 6))
            if rng.random() < 0.16:
                c = (178, 102, 46)                                     # the cork speckle
            elif rng.random() < 0.06:
                c = (240, 196, 130)
            img.putpixel((x, y), clamp(c) + (255,))
    return img


def tex_ember(rng, frames=4):
    img = Image.new("RGBA", (16, 16 * frames))
    cracks = [(rng.randint(0, 15), rng.randint(0, 15)) for _ in range(10)]
    for f in range(frames):
        for y in range(16):
            for x in range(16):
                d = min(math.hypot(x - cx, y - cy) for cx, cy in cracks)
                heat = max(0.0, 1 - d / 4.0) * (0.75 + 0.25 * math.sin(f * 1.6 + x * 0.7 + y * 0.5))
                base = (120, 34, 18) if rng.random() < 0.85 else (70, 60, 56)
                c = tuple(b + (t - b) * heat for b, t in zip(base, (255, 200, 80)))
                img.putpixel((x, f * 16 + y), clamp(c) + (255,))
    return img


def biome():
    vanilla = {
        "lakes": ["minecraft:lake_lava_underground", "minecraft:lake_lava_surface", f"{MOD}:tar_lake_surface",
                  f"{MOD}:ashtray_tar_lake"],
        "ores": ["minecraft:ore_dirt", "minecraft:ore_gravel", "minecraft:ore_granite_upper",
                 "minecraft:ore_granite_lower", "minecraft:ore_diorite_upper", "minecraft:ore_diorite_lower",
                 "minecraft:ore_andesite_upper", "minecraft:ore_andesite_lower", "minecraft:ore_tuff",
                 "minecraft:ore_coal_upper", "minecraft:ore_coal_lower", "minecraft:ore_iron_upper",
                 "minecraft:ore_iron_middle", "minecraft:ore_iron_small", "minecraft:ore_gold",
                 "minecraft:ore_gold_lower", "minecraft:ore_redstone", "minecraft:ore_redstone_lower",
                 "minecraft:ore_diamond", "minecraft:ore_diamond_medium", "minecraft:ore_diamond_large",
                 "minecraft:ore_diamond_buried", "minecraft:ore_lapis", "minecraft:ore_lapis_buried",
                 "minecraft:ore_copper", "minecraft:underwater_magma", "minecraft:disk_sand", "minecraft:disk_clay",
                 "minecraft:disk_gravel"],
    }
    features = [
        [],                                                            # raw generation
        vanilla["lakes"],                                              # lakes: lava, tar
        ["minecraft:amethyst_geode"],
        ["minecraft:monster_room", "minecraft:monster_room_deep"],
        [], [],                                                        # surface structures, strongholds
        vanilla["ores"],
        [],
        ["minecraft:spring_lava"],
        ["minecraft:glow_lichen", "minecraft:patch_dead_bush_2", f"{MOD}:giant_cigarette", f"{MOD}:cigarette_butt"],
        [f"{MOD}:ashtray_surface", "minecraft:freeze_top_layer"],
    ]
    monster = [{"type": f"minecraft:{t}", "weight": w, "minCount": a, "maxCount": b} for t, w, a, b in (
        ("spider", 100, 4, 4), ("zombie", 95, 4, 4), ("skeleton", 100, 4, 4), ("creeper", 100, 4, 4),
        ("slime", 100, 4, 4), ("enderman", 10, 1, 4), ("witch", 5, 1, 1))]
    write_json(D / "worldgen" / "biome" / "ashtray.json", {
        "has_precipitation": False, "temperature": 2.0, "downfall": 0.0,
        "effects": {"sky_color": 0x9C968F, "fog_color": 0x8C857F, "water_color": 0x3B2B1F, "water_fog_color": 0x261A12,
                    "grass_color": 0x8B8676, "foliage_color": 0x7D786A,
                    "particle": {"options": {"type": "minecraft:white_ash"}, "probability": 0.02},
                    "mood_sound": {"sound": "minecraft:ambient.cave", "tick_delay": 6000, "block_search_extent": 8,
                                   "offset": 2.0}},
        "carvers": {"air": ["minecraft:cave", "minecraft:cave_extra_underground", "minecraft:canyon"]},
        "features": features,
        "spawners": {"monster": monster, "creature": [], "ambient": [], "axolotls": [], "underground_water_creature": [],
                     "water_creature": [], "water_ambient": [], "misc": []},
        "spawn_costs": {}})
    for name in ("ashtray_surface", "giant_cigarette", "cigarette_butt"):
        write_json(D / "worldgen" / "configured_feature" / f"{name}.json", {"type": f"{MOD}:{name}", "config": {}})
    write_json(D / "worldgen" / "placed_feature" / "ashtray_surface.json", {"feature": f"{MOD}:ashtray_surface",
                                                                           "placement": []})
    surface = [{"type": "minecraft:in_square"}, {"type": "minecraft:heightmap", "heightmap": "WORLD_SURFACE_WG"},
               {"type": "minecraft:biome"}]
    write_json(D / "worldgen" / "placed_feature" / "giant_cigarette.json", {"feature": f"{MOD}:giant_cigarette",
        "placement": [{"type": "minecraft:rarity_filter", "chance": 2}] + surface})
    write_json(D / "worldgen" / "placed_feature" / "cigarette_butt.json", {"feature": f"{MOD}:cigarette_butt",
        "placement": [{"type": "minecraft:count", "count": 3}] + surface})
    write_json(D / "worldgen" / "placed_feature" / "ashtray_tar_lake.json", {"feature": f"{MOD}:tar_lake",
        "placement": [{"type": "minecraft:rarity_filter", "chance": 5}] + surface})
    add_tag(RES / "data" / "minecraft" / "tags" / "worldgen" / "biome" / "is_overworld.json", [f"{MOD}:ashtray"])
    write_json(D / "tags" / "worldgen" / "biome" / "is_ashtray.json", {"replace": False, "values": [f"{MOD}:ashtray"]})


def build():
    rng = random.Random(7)
    tex = A / "textures" / "block"
    tex.mkdir(parents=True, exist_ok=True)
    tex_ash(rng).save(tex / "ash.png")
    tex_paper(rng).save(tex / "cigarette_paper.png")
    tex_filter(rng).save(tex / "cigarette_filter.png")
    tex_ember(rng).save(tex / "cigarette_ember.png")
    (tex / "cigarette_ember.png.mcmeta").write_text(json.dumps({"animation": {"frametime": 6, "interpolate": True}}) + "\n")
    for b in BLOCKS:
        write_json(A / "blockstates" / f"{b}.json", {"variants": {"": {"model": f"{MOD}:block/{b}"}}})
        write_json(A / "models" / "block" / f"{b}.json", {"parent": "minecraft:block/cube_all",
                                                         "textures": {"all": f"{MOD}:block/{b}"}})
        write_json(A / "models" / "item" / f"{b}.json", {"parent": f"{MOD}:block/{b}"})
        write_json(D / "loot_table" / "blocks" / f"{b}.json", {"type": "minecraft:block", "pools": [{
            "rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{MOD}:{b}"}],
            "conditions": [{"condition": "minecraft:survives_explosion"}]}]})
    add_tag(RES / "data" / "minecraft" / "tags" / "block" / "mineable" / "shovel.json", [f"{MOD}:ash"])
    add_tag(RES / "data" / "minecraft" / "tags" / "block" / "mineable" / "pickaxe.json", [f"{MOD}:cigarette_ember"])
    add_tag(RES / "data" / "minecraft" / "tags" / "block" / "dead_bush_may_place_on.json", [f"{MOD}:ash"])
    LANG.update({f"block.{MOD}.ash": "Ash", f"block.{MOD}.cigarette_paper": "Cigarette Paper",
                 f"block.{MOD}.cigarette_filter": "Cigarette Filter", f"block.{MOD}.cigarette_ember": "Cigarette Ember",
                 f"biome.{MOD}.ashtray": "Ashtray Wastes"})
    biome()


if __name__ == "__main__":
    build()
