"""Spirit Evolution and Bio-Merge for CobbleEffort: Digital (0.17.0): the twenty Spirit items (Human and Beast, ten
elements; icons drawn here, original pixel art), the spirit's hotbar item, ten elemental Spirit Temples (structures
built with kanto/tools/make_assets.py's Template, one structure set), their loot tables, crafting recipes and lang.
Run by make_assets.py, or alone.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from make_world import A, D, NS, Nbt, Template, C, h, save, tile, write_json

ELEMENTS = {  # element: (base colour, Human spirit Digimon, Beast spirit Digimon)
    "flame": ((236, 96, 32), "Agnimon", "Vritramon"),
    "light": ((250, 226, 110), "Wolfmon", "Garummon"),
    "ice": ((140, 214, 255), "Chackmon", "Blizzarmon"),
    "wind": ((132, 232, 170), "Fairimon", "Shutumon"),
    "thunder": ((250, 214, 40), "Blitzmon", "Bolgmon"),
    "darkness": ((120, 60, 170), "Duskmon", "Velgrmon"),
    "earth": ((170, 116, 62), "Grottomon", "Gigasmon"),
    "wood": ((70, 170, 64), "Arbormon", "Petaldramon"),
    "water": ((44, 124, 232), "Ranamon", "Calamaramon"),
    "steel": ((176, 182, 198), "Mercurymon", "Sephirothmon"),
}

# --- icons --------------------------------------------------------------------------------------------------------------

def symbol(el, x, y):
    """The element's mark in the 16 x 16 icon, centred on (7.5, 7.5); True where it's drawn."""
    cx, cy = x - 7.5, y - 7.5
    r = math.hypot(cx, cy)
    a = math.atan2(cy, cx)
    if el == "flame":                       # a tongue of flame, wide at the bottom
        w = (cy + 4.5) * 0.42
        return -4.5 <= cy <= 3.5 and abs(cx + math.sin(cy * 0.9) * 0.6) <= w
    if el == "light":                       # an eight-point star
        return math.sqrt(abs(cx)) + math.sqrt(abs(cy)) <= 2.35 or (r < 3.0 and abs(abs(cx) - abs(cy)) < 0.6 and r > 1.6)
    if el == "ice":                         # a snowflake: three crossed bars with ticks
        if r > 4.3:
            return False
        for k in range(3):
            t = math.radians(90 + 60 * k)
            d = abs(cx * math.sin(t) - cy * math.cos(t))
            if d < 0.6:
                return True
        return 2.2 < r < 3.0 and abs(math.sin(a * 6)) < 0.35
    if el == "wind":                        # a spiral swirl
        if r > 4.4 or r < 0.6:
            return r < 0.6
        turn = (a + math.pi) / (2 * math.pi)
        return abs(((r - turn * 1.6) % 1.6) - 0.8) < 0.42
    if el == "thunder":                     # a zig-zag bolt
        pts = [(1.5, -4.5), (-1.5, -0.3), (0.8, -0.3), (-1.5, 4.5)]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            dx, dy = x1 - x0, y1 - y0
            t = max(0, min(1, ((cx - x0) * dx + (cy - y0) * dy) / (dx * dx + dy * dy)))
            if math.hypot(cx - (x0 + t * dx), cy - (y0 + t * dy)) < 0.85:
                return True
        return False
    if el == "darkness":                    # a crescent moon
        return r <= 4.2 and math.hypot(cx - 1.6, cy - 1.0) > 3.3
    if el == "earth":                       # a mountain with a snowless peak
        return cy <= 3.5 and cy >= -3.5 + abs(cx) * 1.1 and abs(cx) <= 4.5
    if el == "wood":                        # a leaf with its vein
        u, v = (cx + cy) / 1.414, (cy - cx) / 1.414
        return (u / 4.6) ** 2 + (v / 2.3) ** 2 <= 1 and not (abs(v) < 0.35 and -3 < u < 3)
    if el == "water":                       # a droplet
        if cy >= 0:
            return math.hypot(cx, cy - 0.6) <= 3.3
        return abs(cx) <= (cy + 4.8) * 0.62 and cy >= -4.8
    # steel: a gear
    tooth = (math.cos(a * 8) > 0.2)
    return (r <= (4.4 if tooth else 3.3)) and r > 1.3


def spirit_icon(el, beast):
    base = ELEMENTS[el][0]
    frame = (70, 34, 96) if beast else (250, 238, 200)
    frame_dark = (34, 14, 46) if beast else (176, 150, 90)

    def f(x, y):
        cx, cy = x - 7.5, y - 7.5
        # a rounded hexagonal tablet
        hexd = max(abs(cx) * 0.95 + abs(cy) * 0.35, abs(cy) * 0.9)
        if hexd > 7.4:
            return None
        if hexd > 6.3:
            return C(frame_dark if (x + y) % 5 == 0 or cy > 4 else frame)
        if symbol(el, x, y):
            if beast:
                return C(base, 1.25 if cy < 0 else 1.05)
            return C((255, 255, 255)) if hexd < 3 and el in ("darkness",) else C(base, 1.35)
        shade = 0.55 + 0.25 * (1 - (cy + 7.5) / 15)
        if beast:
            shade *= 0.55
        glint = 1.25 if (cx - cy) > 6.2 and hexd < 6.0 else 1.0
        return C(base, shade * glint)
    return tile(f)


def attack_icon():
    def f(x, y):
        cx, cy = x - 7.5, y - 7.5
        r = math.hypot(cx, cy)
        if r > 7.2:
            return None
        if r > 6.2:
            return C((40, 200, 255))
        t = 1 - r / 6.2
        return C((120 + 135 * t, 230, 255), 0.6 + 0.5 * t, 255) if abs(math.sin(math.atan2(cy, cx) * 3 + r * 0.8)) > 0.35 or r < 2.5 \
            else C((20, 90, 160))
    return tile(f)

# --- temples ------------------------------------------------------------------------------------------------------------

def P(block, **props):
    return (block, props or None)


PALETTE = {  # element: floor, wall, pillar, accent, light
    "flame": ("minecraft:smooth_red_sandstone", "minecraft:red_nether_bricks", "minecraft:chiseled_red_sandstone",
              "minecraft:orange_stained_glass", "minecraft:shroomlight"),
    "light": ("minecraft:smooth_quartz", "minecraft:quartz_bricks", P("minecraft:quartz_pillar", axis="y"),
              "minecraft:yellow_stained_glass", "minecraft:glowstone"),
    "ice": ("minecraft:packed_ice", "minecraft:blue_ice", "minecraft:packed_ice", "minecraft:light_blue_stained_glass", "minecraft:sea_lantern"),
    "wind": ("minecraft:calcite", "minecraft:polished_diorite", P("minecraft:birch_log", axis="y"), "minecraft:lime_stained_glass",
             P("minecraft:verdant_froglight", axis="y")),
    "thunder": ("minecraft:waxed_cut_copper", "minecraft:waxed_copper_block", "minecraft:waxed_chiseled_copper",
                "minecraft:yellow_stained_glass", P("minecraft:ochre_froglight", axis="y")),
    "darkness": ("minecraft:polished_blackstone", "minecraft:polished_blackstone_bricks", "minecraft:obsidian",
                 "minecraft:purple_stained_glass", P("minecraft:pearlescent_froglight", axis="y")),
    "earth": ("minecraft:packed_mud", "minecraft:mud_bricks", "minecraft:dripstone_block", "minecraft:brown_stained_glass", "minecraft:glowstone"),
    "wood": ("minecraft:moss_block", "minecraft:mossy_stone_bricks", P("minecraft:oak_log", axis="y"),
             P("minecraft:oak_leaves", persistent="true", distance="1", waterlogged="false"), P("minecraft:verdant_froglight", axis="y")),
    "water": ("minecraft:prismarine_bricks", "minecraft:prismarine", "minecraft:dark_prismarine", "minecraft:light_blue_stained_glass",
              "minecraft:sea_lantern"),
    "steel": ("minecraft:polished_andesite", "minecraft:polished_deepslate", "minecraft:deepslate_tiles", "minecraft:light_gray_stained_glass",
              "minecraft:sea_lantern"),
}


MARK = {"light": ("minecraft:yellow_concrete", None), "ice": ("minecraft:light_blue_concrete", None)}


def temple(el):
    """A Spirit Temple: an 11 x 11 shrine of the element's stone on a raised floor, four tall corner pillars, low walls
    open at the front, a stepped roof with a glass lantern on top, the element's mark laid in the floor and the spirit
    chest on a pedestal at the back (loot table chests/spirit_temple_<element>)."""
    W, H = 11, 10
    t = Template((W, H, W))
    floor, wall, pillar, accent, light = (b if isinstance(b, tuple) else (b, None) for b in PALETTE[el])

    def put(x, y, z, b):
        t.set(x, y, z, b[0], b[1])

    for x in range(W):
        for z in range(W):
            put(x, 0, z, floor)
            for y in range(1, H):
                t.set(x, y, z, "minecraft:air")
    # the element's mark in the floor (the icon symbol scaled to 7 x 7 in the middle)
    for x in range(2, 9):
        for z in range(2, 9):
            if symbol(el, (x - 2) * 15 / 6, (z - 2) * 15 / 6):
                put(x, 0, z, MARK.get(el, wall))
    for (x, z) in ((0, 0), (0, W - 1), (W - 1, 0), (W - 1, W - 1)):
        for y in range(1, 6):
            put(x, y, z, pillar)
        put(x, 6, z, light)
    for i in range(1, W - 1):
        for y in (1, 2):
            for (x, z) in ((i, W - 1), (0, i), (W - 1, i)):
                put(x, y, z, wall)
            if not 4 <= i <= 6:
                put(i, y, 0, wall)
        put(i, 3, W - 1, accent if i % 2 else wall)
        put(0, 3, i, accent if i % 2 else wall)
        put(W - 1, 3, i, accent if i % 2 else wall)
    # the stepped roof
    for step, y in enumerate(range(6, 10)):
        lo, hi = step, W - 1 - step
        for x in range(lo, hi + 1):
            for z in range(lo, hi + 1):
                if x in (lo, hi) or z in (lo, hi):
                    put(x, y, z, wall)
                elif y == 9:
                    put(x, y, z, accent)
    put(W // 2, 9, W // 2, light)
    # pedestal, chest and two guardian posts at the door
    put(5, 1, 8, pillar)
    t.set(5, 2, 8, "minecraft:chest", {"facing": "north", "type": "single", "waterlogged": "false"},
          {"LootTable": f"{NS}:chests/spirit_temple_{el}"})
    put(4, 1, 8, light)
    put(6, 1, 8, light)
    for x in (3, 7):
        put(x, 1, 0, pillar)
        put(x, 2, 0, pillar)
        put(x, 3, 0, light)
    return t


TEMPLE_BIOMES = {
    "flame": ["minecraft:desert", "minecraft:badlands", f"{NS}:server_continent"],
    "light": ["minecraft:meadow", "minecraft:cherry_grove", "minecraft:sunflower_plains", "minecraft:flower_forest", f"{NS}:file_island"],
    "ice": ["minecraft:snowy_plains", "minecraft:ice_spikes", "minecraft:snowy_taiga", "minecraft:snowy_beach", f"{NS}:file_island"],
    "wind": ["minecraft:windswept_hills", "minecraft:windswept_gravelly_hills", "minecraft:windswept_forest", "minecraft:windswept_savanna",
             f"{NS}:file_island"],
    "thunder": ["minecraft:savanna", "minecraft:savanna_plateau", "minecraft:plains", f"{NS}:server_continent"],
    "darkness": ["minecraft:dark_forest", f"{NS}:dark_area"],
    "earth": ["minecraft:wooded_badlands", "minecraft:eroded_badlands", "minecraft:stony_shore", f"{NS}:server_continent"],
    "wood": ["#minecraft:is_jungle", "minecraft:forest", "minecraft:birch_forest", "minecraft:old_growth_birch_forest", f"{NS}:voxel_forest"],
    "water": ["minecraft:beach", "minecraft:swamp", f"{NS}:file_island"],
    "steel": ["#minecraft:is_taiga", f"{NS}:server_continent"],
}


def structures():
    for el in ELEMENTS:
        name = f"spirit_temple_{el}"
        t = temple(el)
        p = D / "structure" / f"{name}.nbt"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(Nbt.file(t.data()))
        write_json(D / "worldgen" / "template_pool" / f"{name}.json", {"fallback": "minecraft:empty", "elements": [{
            "weight": 1, "element": {"element_type": "minecraft:single_pool_element", "location": f"{NS}:{name}",
                                     "processors": "minecraft:empty", "projection": "rigid"}}]})
        write_json(D / "tags" / "worldgen" / "biome" / "has_structure" / f"{name}.json", {"replace": False, "values": TEMPLE_BIOMES[el]})
        write_json(D / "worldgen" / "structure" / f"{name}.json", {
            "type": "minecraft:jigsaw", "biomes": f"#{NS}:has_structure/{name}", "step": "surface_structures",
            "spawn_overrides": {}, "terrain_adaptation": "beard_thin", "start_pool": f"{NS}:{name}", "size": 1,
            "start_height": {"absolute": 0}, "project_start_to_heightmap": "WORLD_SURFACE_WG",
            "max_distance_from_center": 80, "use_expansion_hack": False})
    # one set for all ten: a placement tries the temples in turn until one fits the biome there
    write_json(D / "worldgen" / "structure_set" / "spirit_temples.json", {
        "structures": [{"structure": f"{NS}:spirit_temple_{el}", "weight": 1} for el in ELEMENTS],
        "placement": {"type": "minecraft:random_spread", "spacing": 28, "separation": 9, "salt": 7340}})
    print(f"  spirit temples: {len(ELEMENTS)}")


HUMAN_INGREDIENT = {"flame": "minecraft:blaze_powder", "light": "minecraft:glowstone_dust", "ice": "minecraft:packed_ice",
                    "wind": "minecraft:feather", "thunder": "minecraft:lightning_rod", "darkness": "minecraft:ink_sac",
                    "earth": "minecraft:flint", "wood": "#minecraft:saplings", "water": "minecraft:prismarine_shard",
                    "steel": "minecraft:iron_ingot"}
BEAST_INGREDIENT = {"flame": "minecraft:magma_block", "light": "minecraft:glowstone", "ice": "minecraft:blue_ice",
                    "wind": "minecraft:breeze_rod", "thunder": "minecraft:copper_block", "darkness": "minecraft:crying_obsidian",
                    "earth": "minecraft:dripstone_block", "wood": "#minecraft:logs", "water": "minecraft:nautilus_shell",
                    "steel": "minecraft:iron_block"}


def ing(i):
    return {"tag": i[1:]} if i.startswith("#") else {"item": i}


def recipes_and_loot():
    n = lambda s: f"{NS}:{s}"
    item = lambda i, w, lo=1, hi=1: {"type": "minecraft:item", "name": i, "weight": w,
                                     "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi}}]}
    for el in ELEMENTS:
        write_json(D / "recipe" / f"human_spirit_of_{el}.json", {
            "type": "minecraft:crafting_shaped", "category": "misc", "pattern": ["EGE", "GCG", "EGE"],
            "key": {"E": ing(HUMAN_INGREDIENT[el]), "G": {"item": "minecraft:gold_ingot"}, "C": {"item": n("digi_core")}},
            "result": {"id": n(f"human_spirit_of_{el}"), "count": 1}})
        write_json(D / "recipe" / f"beast_spirit_of_{el}.json", {
            "type": "minecraft:crafting_shaped", "category": "misc", "pattern": ["BIB", "ICI", "BIB"],
            "key": {"B": ing(BEAST_INGREDIENT[el]), "I": {"item": n("chrome_digizoid_ingot")}, "C": {"item": n("digi_core")}},
            "result": {"id": n(f"beast_spirit_of_{el}"), "count": 1}})
        write_json(D / "loot_table" / "chests" / f"spirit_temple_{el}.json", {"type": "minecraft:chest", "pools": [
            {"rolls": 1, "entries": [item(n(f"human_spirit_of_{el}"), 3), item(n(f"beast_spirit_of_{el}"), 2)]},
            {"rolls": {"type": "minecraft:uniform", "min": 2, "max": 4}, "entries": [
                item(n("digi_core"), 6, 1, 2), item(n("vaccine_fragment"), 8, 2, 4), item(n("data_fragment"), 8, 2, 4),
                item(n("virus_fragment"), 8, 2, 4), item(n("chrome_digizoid_ingot"), 2),
                item(HUMAN_INGREDIENT[el] if not HUMAN_INGREDIENT[el].startswith("#") else "minecraft:oak_sapling", 10, 2, 6)]}]})


LANG = {
    f"{NS}.spirit.becomes": "Spirit of %s",
    f"{NS}.spirit.attack_tooltip": "Your spirit's power. It vanishes when the spirit leaves.",
    f"{NS}.spirit.already": "You're already transformed.",
    f"{NS}.spirit.evolved": "%s Spirit Evolved into %s!",
    f"{NS}.spirit.merged": "%s Bio-Merged into %s!",
    f"{NS}.spirit.ended": "The spirit returns to rest.",
    f"{NS}.spirit.gauge": "%s  [%s%s]  %ss",
    f"{NS}.spirit.bond": "%s needs a perfect bond to Bio-Merge (friendship %s/255).",
    f"{NS}.spirit.dash": "Spirit Dash",
    f"{NS}.spirit.revert": "Release the Spirit",
    "item." + NS + ".spirit_attack": "Spirit Power",
    f"{NS}.spirit.attack.flame": "Flame Burst",
    f"{NS}.spirit.attack.light": "Light Arrows",
    f"{NS}.spirit.attack.ice": "Frost Flurry",
    f"{NS}.spirit.attack.wind": "Gale Shot",
    f"{NS}.spirit.attack.thunder": "Thunder Strike",
    f"{NS}.spirit.attack.darkness": "Shadow Skull",
    f"{NS}.spirit.attack.earth": "Quake Slam",
    f"{NS}.spirit.attack.wood": "Thorn Spores",
    f"{NS}.spirit.attack.water": "Tidal Rush",
    f"{NS}.spirit.attack.steel": "Metal Volley",
    f"{NS}.spirit.gift.flame": "Fire resistance; a burst of flame that sets foes alight.",
    f"{NS}.spirit.gift.light": "Flight; a fan of light arrows.",
    f"{NS}.spirit.gift.ice": "Resistance; a freezing flurry that slows.",
    f"{NS}.spirit.gift.wind": "Flight; wind charges.",
    f"{NS}.spirit.gift.thunder": "Speed II; lightning where you look.",
    f"{NS}.spirit.gift.darkness": "Night vision; a wave of shadow that withers foes.",
    f"{NS}.spirit.gift.earth": "Haste II; a slam that throws foes up.",
    f"{NS}.spirit.gift.wood": "Regeneration; poisoning thorn spores.",
    f"{NS}.spirit.gift.water": "Water breathing and Dolphin's Grace; a tidal push that puts out fires.",
    f"{NS}.spirit.gift.steel": "Resistance II; a volley of metal shards.",
}
for _el, (_c, _hu, _be) in ELEMENTS.items():
    LANG[f"item.{NS}.human_spirit_of_{_el}"] = f"Human Spirit of {_el.capitalize()}"
    LANG[f"item.{NS}.beast_spirit_of_{_el}"] = f"Beast Spirit of {_el.capitalize()}"


def build():
    for el in ELEMENTS:
        for kind, beast in (("human", False), ("beast", True)):
            name = f"{kind}_spirit_of_{el}"
            save(spirit_icon(el, beast), f"item/{name}.png")
            write_json(A / "models" / "item" / f"{name}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/{name}"}})
    save(attack_icon(), "item/spirit_attack.png")
    write_json(A / "models" / "item" / "spirit_attack.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/spirit_attack"}})
    structures()
    recipes_and_loot()
    return LANG


if __name__ == "__main__":
    lang = build()
    f = A / "lang" / "en_us.json"
    d = json.loads(f.read_text()) if f.exists() else {}
    d.update(lang)
    write_json(f, dict(sorted(d.items())))
