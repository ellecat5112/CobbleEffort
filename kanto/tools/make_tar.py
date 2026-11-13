#!/usr/bin/env python3
"""
Tar (0.6.0, the user's design for CobbleEffort's fossil Pokémon): a thick, sticky black fluid of the overworld,
collected in buckets; a Bucket of Tar is what Petroleodd is revived from at a Fossil Analyzer. The fluid, its block and
bucket are code (Tar.java); this writes everything else: animated still/flowing textures, the bucket icon, blockstate
and models, lang, the Cobblemon fossil entry (+ the #cobblemon:fossils item tag), tar lakes (surface and underground,
like vanilla's lava lakes) and the underground tar pit (moved here from CobbleEffort, its pool now real tar). Run by
make_assets.py.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "common" / "src" / "main" / "resources"
MOD = "cobbleeffort_kanto"
A = RES / "assets" / MOD
D = RES / "data" / MOD
LANG: dict[str, str] = {}

TAR = [(14, 11, 10), (26, 20, 17), (42, 33, 27), (70, 60, 54), (112, 104, 98)]


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def tar_texel(x, y, t, size):
    """A tileable, slowly churning tar surface: dark swirls with a few glossy highlights."""
    u, v = 2 * math.pi * x / size, 2 * math.pi * y / size
    a = (math.sin(u + 0.7 * math.sin(v + t)) + math.sin(2 * v - u + 1.3 * math.cos(t)) +
         0.6 * math.sin(3 * u + 2 * v - 2 * t) + 0.4 * math.cos(u - 3 * v + t))
    i = 0 if a < -1.1 else 1 if a < 0.4 else 2 if a < 1.5 else 3 if a < 2.15 else 4
    return TAR[i] + (255,)


def animated(size, frames, flow):
    img = Image.new("RGBA", (size, size * frames))
    px = img.load()
    for f in range(frames):
        t = 2 * math.pi * f / frames
        for y in range(size):
            for x in range(size):
                yy = (y - f * size // frames) % size if flow else y          # flowing tar slides down the frames
                px[x, f * size + y] = tar_texel(x, yy, 0 if flow else t, size)
    return img


def bucket():
    """A 16x16 bucket icon (painted here): grey metal with a rim and handle, full of glossy black tar."""
    img = Image.new("RGBA", (16, 16))
    px = img.load()
    metal, dark, light = (150, 150, 158), (96, 96, 104), (206, 206, 214)
    for y in range(4, 15):
        w = 6 - (y - 4) // 4                                          # tapering toward the bottom
        for x in range(8 - w, 8 + w):
            px[x, y] = light if x == 8 - w else dark if x == 8 + w - 1 or y == 14 else metal
    for x in range(1, 15):                                            # the rim
        px[x, 4] = light if x < 8 else metal
        px[x, 3] = dark
    for x in range(3, 13):                                            # the tar inside, a highlight on it
        px[x, 5] = TAR[3] + (255,) if x in (5, 6) else TAR[1] + (255,)
    for x in range(2, 14):
        px[x, 4] = TAR[0] + (255,) if 2 < x < 13 else px[x, 4]
    for i, x in enumerate(range(2, 14)):                              # the handle
        y = 2 - int(1.6 * math.sin(math.pi * i / 11))
        if 0 <= y < 16:
            px[x, y] = dark
    return img


def build():
    tex = A / "textures" / "block"
    tex.mkdir(parents=True, exist_ok=True)
    animated(16, 32, False).save(tex / "tar_still.png", optimize=True)
    (tex / "tar_still.png.mcmeta").write_text(json.dumps({"animation": {"frametime": 5, "interpolate": True}}) + "\n")
    animated(32, 16, True).save(tex / "tar_flow.png", optimize=True)
    (tex / "tar_flow.png.mcmeta").write_text(json.dumps({"animation": {"frametime": 6, "interpolate": True}}) + "\n")
    write_json(A / "blockstates" / "tar.json", {"variants": {"": {"model": f"{MOD}:block/tar"}}})
    write_json(A / "models" / "block" / "tar.json", {"textures": {"particle": f"{MOD}:block/tar_still"}})
    (A / "textures" / "item").mkdir(parents=True, exist_ok=True)
    bucket().save(A / "textures" / "item" / "tar_bucket.png", optimize=True)
    write_json(A / "models" / "item" / "tar_bucket.json",
               {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/tar_bucket"}})
    LANG.update({f"block.{MOD}.tar": "Tar", f"fluid.{MOD}.tar": "Tar", f"fluid.{MOD}.flowing_tar": "Tar",
                 f"fluid_type.{MOD}.tar": "Tar", f"item.{MOD}.tar_bucket": "Bucket of Tar",
                 f"{MOD}.fossil.petroleodd.name": "Tar"})
    # the fossil: a Bucket of Tar revives Petroleodd (CobbleEffort's fossil Pokémon) at a Fossil Analyzer
    write_json(D / "fossils" / "petroleodd.json", {"fossils": [f"{MOD}:tar_bucket"], "result": "cobbleeffort:petroleodd"})
    write_json(RES / "data" / "cobblemon" / "tags" / "item" / "fossils.json", {"replace": False, "values": [f"{MOD}:tar_bucket"]})
    # tar lakes, like vanilla's lava lakes: on the surface (added to dry and swampy biomes by Tar.java) and underground
    write_json(D / "worldgen" / "configured_feature" / "tar_lake.json", {"type": "minecraft:lake", "config": {
        "barrier": {"type": "minecraft:simple_state_provider", "state": {"Name": "minecraft:stone"}},
        "fluid": {"type": "minecraft:simple_state_provider", "state": {"Name": f"{MOD}:tar", "Properties": {"level": "0"}}}}})
    write_json(D / "worldgen" / "placed_feature" / "tar_lake_surface.json", {"feature": f"{MOD}:tar_lake", "placement": [
        {"type": "minecraft:rarity_filter", "chance": 12}, {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "WORLD_SURFACE_WG"}, {"type": "minecraft:biome"}]})
    write_json(D / "worldgen" / "placed_feature" / "tar_lake_underground.json", {"feature": f"{MOD}:tar_lake", "placement": [
        {"type": "minecraft:rarity_filter", "chance": 14}, {"type": "minecraft:in_square"},
        {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform", "min_inclusive": {"absolute": -48},
                                                       "max_inclusive": {"absolute": 48}}},
        {"type": "minecraft:environment_scan", "direction_of_search": "down", "max_steps": 32, "target_condition": {
            "type": "minecraft:all_of", "predicates": [
                {"type": "minecraft:not", "predicate": {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"}},
                {"type": "minecraft:inside_world_bounds", "offset": [0, -5, 0]}]}},
        {"type": "minecraft:surface_relative_threshold_filter", "heightmap": "OCEAN_FLOOR_WG", "max_inclusive": -5},
        {"type": "minecraft:biome"}]})
    tar_pit()


def tar_pit():
    """The underground tar pit (from CobbleEffort's fossils.py, where it held Ancient Tar): its pool is real tar now,
    and brushing its gravel turns up bones and coal."""
    sys.path.insert(0, str(HERE.parent.parent / "tools" / "newmons"))
    import fossils
    from make_assets import Nbt
    t = fossils.tar_pit()
    for pos, (name, props, nbt) in list(t.blocks.items()):
        if name in ("minecraft:black_concrete", "minecraft:coal_block") and pos[1] == 2:
            t.set(*pos, f"{MOD}:tar", {"level": "0"})
        elif name == "minecraft:suspicious_gravel":
            t.set(*pos, name, props, dict(nbt, LootTable=f"{MOD}:archaeology/tar_pit"))
    nbt = D / "structure" / "tar_pit.nbt"
    nbt.parent.mkdir(parents=True, exist_ok=True)
    nbt.write_bytes(Nbt.file(t.data()))
    write_json(D / "loot_table" / "archaeology" / "tar_pit.json", {"type": "minecraft:archaeology", "pools": [{"rolls": 1, "entries": [
        {"type": "minecraft:item", "name": "minecraft:bone", "weight": 4}, {"type": "minecraft:item", "name": "minecraft:coal", "weight": 3},
        {"type": "minecraft:item", "name": "minecraft:bone_meal", "weight": 2}, {"type": "minecraft:item", "name": "minecraft:bucket", "weight": 1}]}]})
    write_json(D / "worldgen" / "template_pool" / "tar_pit.json", {"fallback": "minecraft:empty", "elements": [{"weight": 1, "element": {
        "element_type": "minecraft:single_pool_element", "location": f"{MOD}:tar_pit", "processors": "minecraft:empty",
        "projection": "rigid"}}]})
    write_json(D / "tags" / "worldgen" / "biome" / "has_structure" / "tar_pit.json", {"replace": False, "values": ["#minecraft:is_overworld"]})
    write_json(D / "worldgen" / "structure" / "tar_pit.json", {
        "type": "minecraft:jigsaw", "biomes": f"#{MOD}:has_structure/tar_pit", "step": "underground_structures",
        "spawn_overrides": {}, "terrain_adaptation": "none", "start_pool": f"{MOD}:tar_pit", "size": 1,
        "start_height": {"absolute": -34}, "max_distance_from_center": 80, "use_expansion_hack": False})
    write_json(D / "worldgen" / "structure_set" / "tar_pit.json", {
        "structures": [{"structure": f"{MOD}:tar_pit", "weight": 1}],
        "placement": {"type": "minecraft:random_spread", "spacing": 28, "separation": 10, "salt": 30241}})


if __name__ == "__main__":
    build()
