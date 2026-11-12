"""Fossils for CobbleEffort's fossil Pokémon: the fossil items, where they are found, and Cobblemon's fossil entries.

Data only (no code): a fossil item is a vanilla item (echo shard) carrying our custom data, a name, lore and its own
icon (custom_model_data on the echo shard's model); Cobblemon's fossil entries match it with an item predicate on that
custom data, so the Fossil Analyzer and Restoration Tank revive it like any fossil. The items are found by brushing
suspicious gravel in two structures of our own (archaeology loot tables):

  tar_pit      deep underground (y -34), a cavern with a pool of black tar beside lava pockets, bubbling magma and
               old bones sticking out; brushing the gravel at the tar's edge gives Ancient Tar (Petroleodd)
  spire_stump  in forests and swamps, a petrified Prototaxites stump with rings on its top, glowing froglight
               "mycelium" and a fallen spire segment; brushing the gravel round it gives a Spire Fossil (Mycolith)

Structure templates are written with the Kanto add-on's NBT writer (kanto/tools/make_assets.py).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
RES = ROOT / "src" / "main" / "resources"
MOD = "cobbleeffort"
sys.path.insert(0, str(ROOT / "kanto" / "tools"))
from make_assets import Nbt, Template  # noqa: E402

BASE_ITEM = "minecraft:echo_shard"
CMD_BASE = 794800

FOSSILS = {
    "petroleodd": {"key": "tar", "item": "ancient_tar", "name": "Ancient Tar", "cmd": 1, "structure": "tar_pit",
                   "fossil_name": "Ancient Tar",
                   "lore": "A lump of tar from a pit beside deep lava. Old bones stir inside it. Revive it at a "
                           "Restoration Tank."},
    "mycolith": {"key": "spire", "item": "spire_fossil", "name": "Spire Fossil", "cmd": 2, "structure": "spire_stump",
                 "fossil_name": "Spire Fossil",
                 "lore": "A petrified, ring-banded log that looks like wood, but is a mass of tiny tubes inside. "
                         "Revive it at a Restoration Tank."},
}


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1) + "\n")


def components(f):
    return {
        "minecraft:custom_name": json.dumps({"translate": f"item.{MOD}.{f['item']}", "italic": False}),
        "minecraft:lore": [json.dumps({"translate": f"item.{MOD}.{f['item']}.tooltip", "color": "gray", "italic": False})],
        "minecraft:custom_model_data": CMD_BASE + f["cmd"],
        "minecraft:rarity": "uncommon",
        "minecraft:max_stack_size": 16,
        "minecraft:custom_data": {"cobbleeffort_fossil": f["key"]},
    }


def stack(f):
    return {"id": BASE_ITEM, "count": 1, "components": components(f)}


# --- icons -------------------------------------------------------------------------------------------------------

def icon_tar():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y in range(16):
        for x in range(16):
            if 4 <= y <= 14 and 3 + (y - 4) * 0.15 <= x <= 12 - (y - 4) * 0.15:      # the bucket
                c = (150, 156, 168) if x in (3, 4) or y == 14 else (120, 126, 138)
                if y <= 6:
                    c = (34, 32, 38) if 5 <= x <= 10 else c                           # tar at the top
                px[x, y] = c + (255,)
    for x, y in ((6, 5), (9, 6)):
        px[x, y] = (200, 204, 220, 255)                                              # glossy shine
    for i in range(6):                                                               # a bone poking out
        px[8 + i // 2, 4 - i // 2] = (236, 224, 190, 255)
    for x, y in ((11, 0), (12, 1), (10, 0), (12, 0)):
        px[x, y] = (236, 224, 190, 255)
    return img


def icon_spire():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y in range(16):
        for x in range(16):
            r = math.hypot(x - 7.5, (y - 7.5) * 1.15)
            if r > 7.2:
                continue
            c = (104, 96, 90) if int(r * 1.3) % 2 else (150, 142, 130)                   # concentric rings
            if r > 6.3:
                c = (80, 72, 66)                                                     # bark
            if (x * 7 + y * 13) % 17 == 0 and r < 6:
                c = (170, 90, 230) if (x + y) % 2 else (250, 170, 60)                # mycelium specks
            px[x, y] = c + (255,)
    return img


# --- structures ----------------------------------------------------------------------------------------------------

def brushable(t, x, y, z, loot):
    t.set(x, y, z, "minecraft:suspicious_gravel", {"dusted": "0"},
          {"id": "minecraft:brushable_block", "LootTable": loot})


def h(*a):
    n = math.sin(sum(v * k for v, k in zip(a, (12.9898, 78.233, 37.719, 4.581)))) * 43758.5453
    return n - math.floor(n)


def tar_pit():
    W, H = 23, 12
    c = W // 2
    t = Template((W, H, W))
    for x in range(W):
        for z in range(W):
            dx, dz = x - c, z - c
            d = math.hypot(dx, dz)
            if d > 11:
                continue
            for y in range(H):
                if (d / 11) ** 2 + ((y - 3) / 8) ** 2 < 1 and y >= 3:
                    t.set(x, y, z, "minecraft:air")                          # the cavern
            floor = "minecraft:blackstone" if h(x, z) > 0.4 else "minecraft:basalt"
            t.set(x, 0, z, "minecraft:deepslate")
            t.set(x, 1, z, floor, {"axis": "y"} if floor == "minecraft:basalt" else None)
            if d < 6.5:                                                      # the tar pool
                t.set(x, 2, z, "minecraft:black_concrete" if h(x, z, 2) > 0.18 else "minecraft:coal_block")
            elif d < 7.5:
                t.set(x, 2, z, "minecraft:polished_blackstone")
            else:
                t.set(x, 2, z, "minecraft:magma_block" if h(x, z, 3) > 0.86 else floor,
                      {"axis": "y"} if floor == "minecraft:basalt" and h(x, z, 3) <= 0.86 else None)
    for lx, lz in ((c + 9, c), (c - 7, c - 6), (c - 4, c + 8)):             # lava pockets beside the tar
        for x in range(lx - 1, lx + 2):
            for z in range(lz - 1, lz + 2):
                if 0 <= x < W and 0 <= z < W:
                    t.set(x, 2, z, "minecraft:lava", {"level": "0"})
                    t.set(x, 1, z, "minecraft:basalt", {"axis": "y"})
    for bx, bz, hgt in ((c - 2, c + 1, 3), (c + 2, c - 2, 4), (c + 3, c + 3, 2), (c - 4, c - 3, 2)):   # old bones
        for y in range(3, 3 + hgt):
            t.set(bx, y, bz, "minecraft:bone_block", {"axis": "y"})
    for i in range(-3, 4):                                                   # a rib arching out of the tar
        t.set(c + i, 3 + int(3 - abs(i) * 0.9), c - 4, "minecraft:bone_block", {"axis": "x"})
    for gx, gz in ((c + 7, c + 2), (c - 7, c + 1), (c + 1, c + 7), (c - 2, c - 7), (c + 5, c - 5)):
        brushable(t, gx, 2, gz, f"{MOD}:archaeology/tar_pit")
    return t


def spire_stump():
    W, H = 15, 12
    c = W // 2
    t = Template((W, H, W))
    for x in range(W):
        for z in range(W):
            d = math.hypot(x - c, z - c)
            if d < 6.5:
                t.set(x, 0, z, "minecraft:coarse_dirt" if h(x, z) > 0.5 else "minecraft:mud")
                if 3.2 < d < 6.3 and h(x, z, 5) > 0.82:
                    t.set(x, 1, z, "minecraft:brown_mushroom" if h(x, z, 6) > 0.4 else "minecraft:red_mushroom")
    top = 9
    for x in range(W):
        for z in range(W):
            d = math.hypot(x - c, z - c)
            if d < 2.9:
                for y in range(1, top + 1):
                    name = "minecraft:polished_tuff" if y == top else ("minecraft:tuff_bricks" if (y + int(d)) % 3 == 0 else "minecraft:tuff")
                    if y < top and abs(math.sin(x * 1.3 + z * 0.7 + y * 0.9)) < 0.08:
                        name = "minecraft:pearlescent_froglight" if (x + y) % 2 else "minecraft:ochre_froglight"
                    t.set(x, y, z, name, {"axis": "y"} if "froglight" in name else None)
    for i in range(7):                                                       # a fallen spire segment
        t.set(c + 3 + i, 1, c + 4, "minecraft:tuff")
        t.set(c + 3 + i, 1, c + 5, "minecraft:tuff" if i % 3 else "minecraft:ochre_froglight", None if i % 3 else {"axis": "x"})
        t.set(c + 3 + i, 2, c + 4, "minecraft:tuff_bricks" if i % 2 else "minecraft:tuff")
    for gx, gz in ((c - 3, c), (c + 3, c - 1), (c, c - 3), (c + 1, c + 3)):
        brushable(t, gx, 0, gz, f"{MOD}:archaeology/spire_stump")
    return t


STRUCTURES = {
    "tar_pit": {"build": tar_pit, "biomes": ["#minecraft:is_overworld"], "step": "underground_structures",
                "adapt": "none", "height": {"absolute": -34}, "project": None, "spacing": 28, "separation": 10,
                "salt": 30241},
    "spire_stump": {"build": spire_stump, "biomes": ["minecraft:swamp", "minecraft:mangrove_swamp", "minecraft:dark_forest",
                                                     "minecraft:old_growth_spruce_taiga", "minecraft:old_growth_pine_taiga",
                                                     "minecraft:forest", "minecraft:birch_forest", "minecraft:taiga"],
                    "step": "surface_structures", "adapt": "beard_thin", "height": {"absolute": 0},
                    "project": "WORLD_SURFACE_WG", "spacing": 32, "separation": 12, "salt": 30242},
}

LOOT = {
    "tar_pit": [("fossil:petroleodd", 3), ("minecraft:bone", 4), ("minecraft:coal", 3), ("minecraft:bone_meal", 2),
                ("minecraft:black_dye", 1)],
    "spire_stump": [("fossil:mycolith", 3), ("minecraft:brown_mushroom", 3), ("minecraft:stick", 2),
                    ("minecraft:tuff", 2), ("minecraft:bone_meal", 1)],
}


def build(lang):
    data, assets = RES / "data" / MOD, RES / "assets" / MOD
    for sp, f in FOSSILS.items():
        write_json(data / "fossils" / f"{sp}.json", {
            "result": f"{MOD}:{sp}",
            "fossils": [{"item": BASE_ITEM, "nbt": json.dumps({"cobbleeffort_fossil": f["key"]}).replace('"cobbleeffort_fossil"', "cobbleeffort_fossil")}]})
        lang[f"{MOD}.fossil.{sp}.name"] = f["fossil_name"]
        lang[f"item.{MOD}.{f['item']}"] = f["name"]
        lang[f"item.{MOD}.{f['item']}.tooltip"] = f["lore"]
        tex = assets / "textures" / "item" / f"{f['item']}.png"
        tex.parent.mkdir(parents=True, exist_ok=True)
        (icon_tar if f["key"] == "tar" else icon_spire)().save(tex)
        write_json(assets / "models" / "item" / f"{f['item']}.json",
                   {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{f['item']}"}})
    write_json(RES / "assets" / "minecraft" / "models" / "item" / "echo_shard.json", {
        "parent": "minecraft:item/generated", "textures": {"layer0": "minecraft:item/echo_shard"},
        "overrides": [{"predicate": {"custom_model_data": CMD_BASE + f["cmd"]}, "model": f"{MOD}:item/{f['item']}"}
                      for f in FOSSILS.values()]})
    for name, entries in LOOT.items():
        pool = []
        for item, w in entries:
            if item.startswith("fossil:"):
                f = FOSSILS[item.split(":")[1]]
                pool.append({"type": "minecraft:item", "name": BASE_ITEM, "weight": w,
                             "functions": [{"function": "minecraft:set_components", "components": components(f)}]})
            else:
                pool.append({"type": "minecraft:item", "name": item, "weight": w})
        write_json(data / "loot_table" / "archaeology" / f"{name}.json",
                   {"type": "minecraft:archaeology", "pools": [{"rolls": 1, "entries": pool}]})
    for name, s in STRUCTURES.items():
        nbt = data / "structure" / "fossil" / f"{name}.nbt"
        nbt.parent.mkdir(parents=True, exist_ok=True)
        nbt.write_bytes(Nbt.file(s["build"]().data()))
        write_json(data / "worldgen" / "template_pool" / "fossil" / f"{name}.json", {
            "fallback": "minecraft:empty",
            "elements": [{"weight": 1, "element": {"element_type": "minecraft:single_pool_element",
                                                   "location": f"{MOD}:fossil/{name}", "processors": "minecraft:empty",
                                                   "projection": "rigid"}}]})
        write_json(data / "tags" / "worldgen" / "biome" / "has_structure" / f"{name}.json",
                   {"replace": False, "values": s["biomes"]})
        struct = {"type": "minecraft:jigsaw", "biomes": f"#{MOD}:has_structure/{name}", "step": s["step"],
                  "spawn_overrides": {}, "terrain_adaptation": s["adapt"], "start_pool": f"{MOD}:fossil/{name}",
                  "size": 1, "start_height": s["height"], "max_distance_from_center": 80, "use_expansion_hack": False}
        if s["project"]:
            struct["project_start_to_heightmap"] = s["project"]
        write_json(data / "worldgen" / "structure" / f"{name}.json", struct)
        write_json(data / "worldgen" / "structure_set" / f"{name}.json", {
            "structures": [{"structure": f"{MOD}:{name}", "weight": 1}],
            "placement": {"type": "minecraft:random_spread", "spacing": s["spacing"], "separation": s["separation"],
                          "salt": s["salt"]}})
    write_json(HERE / "creative_items.json", [stack(f) for f in FOSSILS.values()])
