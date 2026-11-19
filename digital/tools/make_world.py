"""The Digital World for CobbleEffort: Digital (0.14.0): its blocks (textures drawn here, original pixel art), the
dimension (dimension type, noise settings copied from vanilla's overworld with our surface rules, a multi-noise biome
list), four biomes (File Island's wireframe plains, the voxel forest, the Server Continent, the Dark Area), their
features, structures (Abandoned Server Terminal, Primary Village, plug-in socket cliff, Dark Tower; templates built
with kanto/tools/make_assets.py's Template), loot tables, Digital-World spawn pools (read from the Digimon species'
labels) and lang. Run by make_assets.py, or alone:

    python3 digital/tools/make_world.py
"""
from __future__ import annotations

import json
import math
import sys
import zipfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent / "common" / "src" / "main" / "resources"
NS = "cobbleeffort_digital"
A = ROOT / "assets" / NS
D = ROOT / "data" / NS
LOOM = Path.home() / ".gradle" / "caches" / "fabric-loom" / "1.21.1" / "minecraft-merged.jar"


def _kanto_writer():
    """The Kanto add-on's structure writer (kanto/tools/make_assets.py: Nbt, Template), loaded by path: this folder
    has a make_assets.py of its own."""
    import importlib.util
    for root in (HERE.parents[1], Path("/home/user/CobbleEffort")):
        f = root / "kanto" / "tools" / "make_assets.py"
        if f.exists():
            spec = importlib.util.spec_from_file_location("kanto_make_assets", f)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod.Nbt, mod.Template
    raise SystemExit("kanto/tools/make_assets.py not found")


Nbt, Template = _kanto_writer()

BIOMES = ["file_island", "voxel_forest", "server_continent", "dark_area"]


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def h(*a):
    v = 2166136261
    for x in a:
        v = ((v ^ (int(x) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return v / 0xFFFFFFFF


def C(c, k=1.0, a=255):
    return tuple(max(0, min(255, int(round(v * k)))) for v in c[:3]) + (a,)


def tile(fn, w=16, hh=16):
    im = Image.new("RGBA", (w, hh), (0, 0, 0, 0))
    px = im.load()
    for y in range(hh):
        for x in range(w):
            c = fn(x, y)
            if c is not None:
                px[x, y] = c if len(c) == 4 else C(c)
    return im


def save(im, rel):
    p = A / "textures" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    im.save(p, optimize=True)


# --- block textures -------------------------------------------------------------------------------------------------

def circuit(x, y):
    """A green circuit board: copper traces on a grid, solder pads, a few chips."""
    base = (24, 92, 52) if h(x // 4, y // 4, 1) > 0.15 else (20, 80, 46)
    if (x % 8 == 3 and h(x // 8, y // 2, 2) > 0.3) or (y % 8 == 5 and h(x // 2, y // 8, 3) > 0.3):
        base = (196, 160, 70)
    if (x % 8, y % 8) in ((3, 5), (3, 1), (7, 5)):
        base = (230, 214, 150)
    if 10 <= x <= 13 and 9 <= y <= 12:
        base = (30, 30, 36) if (x, y) != (10, 9) else (220, 220, 220)
    return base


def casing(x, y):
    """A server casing panel: grey with a vent grille, blinking LEDs and a border."""
    if x in (0, 15) or y in (0, 15):
        return (70, 74, 84)
    if 3 <= y <= 9 and 2 <= x <= 13:
        return (40, 42, 48) if y % 2 else (96, 100, 110)
    if y == 12 and x in (3, 5, 7):
        return [(80, 240, 120), (240, 200, 60), (60, 200, 255)][(x - 3) // 2]
    return (120, 124, 134)


def socket(x, y):
    """A plug-in socket panel: casing with two black socket holes."""
    c = casing(x, y)
    for cx, cy in ((5, 7), (10, 7)):
        if abs(x - cx) <= 1 and abs(y - cy) <= 2:
            return (10, 10, 12)
    return c


def wireframe(x, y):
    """A glowing cyan wire cube: bright edges and a diagonal, transparent faces."""
    if x in (0, 15) or y in (0, 15):
        return (90, 240, 255, 255)
    if x == y or x == 15 - y:
        return (60, 200, 240, 200)
    return (0, 0, 0, 0)


def voxel_bark(x, y):
    return (122, 78, 40) if (x // 2 + y // 4) % 3 else (92, 56, 28)


def voxel_top(x, y):
    d = max(abs(x - 7.5), abs(y - 7.5))
    return (150, 104, 60) if int(d) % 3 else (110, 72, 38)


def voxel_leaves(x, y):
    """Chunky 8-bit leaves: 4x4 pixel blocks in three greens."""
    v = h(x // 4, y // 4, 7)
    return (70, 200, 70) if v > 0.6 else (48, 168, 56) if v > 0.25 else (34, 130, 44)


def corrupted(x, y):
    """Corrupted data: black with violet glitch bars and dead pixels."""
    if (y + int(h(y, 3) * 16)) % 7 == 0 and h(x // 3, y, 4) > 0.4:
        return (150, 40, 200)
    if h(x, y, 9) > 0.93:
        return (230, 60, 120)
    return (22, 14, 30) if h(x // 2, y // 2, 5) > 0.3 else (34, 20, 44)


def tower_core(x, y):
    d = math.hypot(x - 7.5, y - 7.5)
    if d < 3:
        return (255, 60, 40) if d < 1.6 else (190, 20, 30)
    return (26, 12, 30) if (x + y) % 5 else (60, 20, 50)


def terminal_side(x, y):
    return (128, 122, 110) if (x // 4 + y // 3) % 2 else (110, 104, 94)


def terminal_front(x, y):
    if 2 <= x <= 13 and 3 <= y <= 10:
        if x in (2, 13) or y in (3, 10):
            return (40, 44, 50)
        return (60, 230, 255) if (x + y * 3) % 7 == 0 else (16, 70, 90)
    return terminal_side(x, y)


def terminal_top(x, y):
    return (90, 240, 255) if x in (7, 8) or y in (7, 8) else (100, 96, 88)


def cradle_wood(x, y):
    return (230, 196, 140) if y % 4 else (200, 160, 100)


def cradle_egg(x, y):
    return (250, 244, 228) if (x * 3 + y * 5) % 11 else (240, 140, 60)


def block_textures():
    for name, fn in (("circuit_block", circuit), ("server_casing", casing), ("socket_block", socket),
                     ("wireframe_block", wireframe), ("voxel_log", voxel_bark), ("voxel_log_top", voxel_top),
                     ("voxel_leaves", voxel_leaves), ("corrupted_data", corrupted), ("dark_tower_core", tower_core),
                     ("ancient_terminal_side", terminal_side), ("ancient_terminal_front", terminal_front),
                     ("ancient_terminal_top", terminal_top), ("digitama_cradle", cradle_wood), ("digitama_cradle_egg", cradle_egg)):
        save(tile(fn), f"block/{name}.png")
    for i in ("dark_spore", "digi_core"):
        pass


def item_textures():
    def spore(x, y):
        d = math.hypot(x - 7.5, y - 8)
        if d > 5.5:
            return None
        if d > 4.6:
            return (20, 8, 24)
        return (200, 40, 90) if h(x, y, 2) > 0.8 else (60, 14, 70) if d > 2.5 else (120, 20, 110)

    def core(x, y):
        d = max(abs(x - 7.5), abs(y - 7.5))
        if d > 6:
            return None
        if d > 5:
            return (30, 34, 44)
        if d < 2.5:
            return (120, 250, 255) if (x + y) % 2 else (60, 200, 240)
        return (90, 96, 110) if (x + y) % 3 else (160, 170, 186)
    save(tile(spore), "item/dark_spore.png")
    save(tile(core), "item/digi_core.png")


def cube(name, tex=None, cutout=False):
    tex = tex or name
    write_json(A / "blockstates" / f"{name}.json", {"variants": {"": {"model": f"{NS}:block/{name}"}}})
    write_json(A / "models" / "block" / f"{name}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{NS}:block/{tex}"},
                                                        **({"render_type": "minecraft:cutout"} if cutout else {})})
    write_json(A / "models" / "item" / f"{name}.json", {"parent": f"{NS}:block/{name}"})


def drop_self(block):
    write_json(D / "loot_table" / "blocks" / f"{block}.json", {"type": "minecraft:block", "pools": [{
        "rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{NS}:{block}"}],
        "conditions": [{"condition": "minecraft:survives_explosion"}]}]})


def block_models():
    for b in ("circuit_block", "server_casing", "socket_block", "corrupted_data", "dark_tower_core"):
        cube(b)
        if b != "dark_tower_core":
            drop_self(b)
    cube("wireframe_block", cutout=True)
    drop_self("wireframe_block")
    cube("voxel_leaves")
    write_json(D / "loot_table" / "blocks" / "voxel_leaves.json", {"type": "minecraft:block", "pools": [{
        "rolls": 1, "entries": [{"type": "minecraft:alternatives", "children": [
            {"type": "minecraft:item", "name": f"{NS}:voxel_leaves", "conditions": [{"condition": "minecraft:any_of", "terms": [
                {"condition": "minecraft:match_tool", "predicate": {"items": "minecraft:shears"}},
                {"condition": "minecraft:match_tool", "predicate": {"predicates": {"minecraft:enchantments": [
                    {"enchantments": "minecraft:silk_touch", "levels": {"min": 1}}]}}}]}]},
            {"type": "minecraft:item", "name": "minecraft:stick", "conditions": [
                {"condition": "minecraft:table_bonus", "enchantment": "minecraft:fortune", "chances": [0.02, 0.022, 0.025, 0.033, 0.1]}]}]}]}]})
    write_json(A / "blockstates" / "voxel_log.json", {"variants": {
        "axis=y": {"model": f"{NS}:block/voxel_log"}, "axis=z": {"model": f"{NS}:block/voxel_log", "x": 90},
        "axis=x": {"model": f"{NS}:block/voxel_log", "x": 90, "y": 90}}})
    write_json(A / "models" / "block" / "voxel_log.json", {"parent": "minecraft:block/cube_column", "textures": {
        "end": f"{NS}:block/voxel_log_top", "side": f"{NS}:block/voxel_log"}})
    write_json(A / "models" / "item" / "voxel_log.json", {"parent": f"{NS}:block/voxel_log"})
    drop_self("voxel_log")
    # the dark tower core drops nothing (breaking it summons the guardian)
    write_json(D / "loot_table" / "blocks" / "dark_tower_core.json", {"type": "minecraft:block", "pools": []})
    # the terminal: a pedestal with a screen on the front
    write_json(A / "blockstates" / "ancient_terminal.json", {"variants": {
        f"facing={f}": {"model": f"{NS}:block/ancient_terminal", **({"y": y} if y else {})}
        for f, y in (("north", 0), ("east", 90), ("south", 180), ("west", 270))}})
    write_json(A / "models" / "block" / "ancient_terminal.json", {"parent": "minecraft:block/orientable", "textures": {
        "front": f"{NS}:block/ancient_terminal_front", "side": f"{NS}:block/ancient_terminal_side",
        "top": f"{NS}:block/ancient_terminal_top"}})
    write_json(A / "models" / "item" / "ancient_terminal.json", {"parent": f"{NS}:block/ancient_terminal"})
    drop_self("ancient_terminal")
    # cradles: a wooden crib, with an egg in it when "egg=true"
    crib = [{"from": [1, 0, 1], "to": [15, 2, 15], "faces": {f: {"texture": "#wood"} for f in ("north", "south", "east", "west", "up", "down")}},
            {"from": [1, 2, 1], "to": [15, 6, 2], "faces": {f: {"texture": "#wood"} for f in ("north", "south", "east", "west", "up")}},
            {"from": [1, 2, 14], "to": [15, 6, 15], "faces": {f: {"texture": "#wood"} for f in ("north", "south", "east", "west", "up")}},
            {"from": [1, 2, 2], "to": [2, 6, 14], "faces": {f: {"texture": "#wood"} for f in ("north", "south", "east", "west", "up")}},
            {"from": [14, 2, 2], "to": [15, 6, 14], "faces": {f: {"texture": "#wood"} for f in ("north", "south", "east", "west", "up")}}]
    egg = [{"from": [5, 2, 5], "to": [11, 10, 11], "faces": {f: {"texture": "#egg"} for f in ("north", "south", "east", "west", "up")}},
           {"from": [6, 10, 6], "to": [10, 11, 10], "faces": {f: {"texture": "#egg"} for f in ("north", "south", "east", "west", "up")}}]
    tx = {"wood": f"{NS}:block/digitama_cradle", "egg": f"{NS}:block/digitama_cradle_egg", "particle": f"{NS}:block/digitama_cradle"}
    write_json(A / "models" / "block" / "digitama_cradle_empty.json", {"parent": "minecraft:block/block", "textures": tx, "elements": crib})
    write_json(A / "models" / "block" / "digitama_cradle_egg.json", {"parent": "minecraft:block/block", "textures": tx, "elements": crib + egg})
    for name in ("digitama_cradle", "wild_digitama_cradle"):
        write_json(A / "blockstates" / f"{name}.json", {"variants": {
            "egg=true": {"model": f"{NS}:block/digitama_cradle_egg"}, "egg=false": {"model": f"{NS}:block/digitama_cradle_empty"}}})
        write_json(A / "models" / "item" / f"{name}.json", {"parent": f"{NS}:block/digitama_cradle_egg"})
        drop_self(name)
    for i in ("dark_spore", "digi_core"):
        write_json(A / "models" / "item" / f"{i}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/{i}"}})


# --- the dimension --------------------------------------------------------------------------------------------------

def vanilla(path):
    return json.loads(zipfile.ZipFile(LOOM).read(path))


def biomes():
    plains = vanilla("data/minecraft/worldgen/biome/plains.json")
    looks = {  # sky, fog, water, water fog, grass, foliage, particle
        "file_island": (0x7FD8FF, 0xC0F0FF, 0x30E8FF, 0x0A5070, 0x6EE860, 0x5AD850, ("minecraft:glow", 0.0012)),
        "voxel_forest": (0x7FC8FF, 0xB8E8D8, 0x30E8FF, 0x0A5070, 0x38C048, 0x2FB040, None),
        "server_continent": (0x70A0FF, 0xB0C8E8, 0x30E8FF, 0x0A5070, 0x9CB070, 0x88A060, ("minecraft:electric_spark", 0.0008)),
        "dark_area": (0x1A0A26, 0x2A1238, 0x401060, 0x10041A, 0x402050, 0x301840, ("minecraft:ash", 0.02)),
    }
    veg_plain = [f for f in plains["features"][9] if f != "minecraft:trees_plains"]
    ours9 = {"file_island": ["wireframe_patch"], "voxel_forest": ["voxel_tree", "wireframe_patch"],
             "server_continent": ["server_rack"], "dark_area": ["corrupted_spike"]}
    for b, (sky, fog, water, wfog, grass, foliage, part) in looks.items():
        feats = [list(step) for step in plains["features"]]
        if b != "dark_area":
            feats[1] = feats[1] + [f"{NS}:data_lake"]
        feats[6] = feats[6] + [f"{NS}:chrome_digizoid_ore"]
        if b == "dark_area":
            feats[9] = ["minecraft:glow_lichen"]
        elif b == "server_continent":
            feats[9] = ["minecraft:glow_lichen", "minecraft:patch_grass_plain"]
        else:
            feats[9] = list(veg_plain)
        feats[9] += [f"{NS}:{f}" for f in ours9[b]]
        effects = {"sky_color": sky, "fog_color": fog, "water_color": water, "water_fog_color": wfog,
                   "grass_color": grass, "foliage_color": foliage,
                   "mood_sound": {"block_search_extent": 8, "offset": 2.0, "sound": "minecraft:ambient.cave", "tick_delay": 6000}}
        if part:
            effects["particle"] = {"options": {"type": part[0]}, "probability": part[1]}
        write_json(D / "worldgen" / "biome" / f"{b}.json", {
            "has_precipitation": b != "dark_area", "temperature": 0.7 if b != "dark_area" else 1.2,
            "downfall": 0.6 if b != "server_continent" else 0.1, "effects": effects,
            "spawners": {k: [] for k in plains["spawners"]}, "spawn_costs": {},
            "carvers": plains["carvers"], "features": feats})
    # features
    cf, pf = D / "worldgen" / "configured_feature", D / "worldgen" / "placed_feature"
    state = lambda n, props=None: {"Name": n, **({"Properties": props} if props else {})}
    simple = lambda n, props=None: {"type": "minecraft:simple_state_provider", "state": state(n, props)}
    write_json(cf / "voxel_tree.json", {"type": "minecraft:tree", "config": {
        "ignore_vines": True, "force_dirt": False, "decorators": [],
        "dirt_provider": simple("minecraft:dirt"), "trunk_provider": simple(f"{NS}:voxel_log", {"axis": "y"}),
        "foliage_provider": simple(f"{NS}:voxel_leaves", {"distance": "7", "persistent": "false", "waterlogged": "false"}),
        "trunk_placer": {"type": "minecraft:giant_trunk_placer", "base_height": 14, "height_rand_a": 5, "height_rand_b": 4},
        "foliage_placer": {"type": "minecraft:blob_foliage_placer", "radius": 5, "offset": 0, "height": 5},
        "minimum_size": {"type": "minecraft:two_layers_feature_size", "limit": 1, "lower_size": 1, "upper_size": 2}}})
    write_json(pf / "voxel_tree.json", {"feature": f"{NS}:voxel_tree", "placement": [
        {"type": "minecraft:count", "count": {"type": "minecraft:weighted_list", "distribution": [
            {"weight": 3, "data": 1}, {"weight": 1, "data": 2}]}},
        {"type": "minecraft:in_square"}, {"type": "minecraft:surface_water_depth_filter", "max_water_depth": 0},
        {"type": "minecraft:heightmap", "heightmap": "OCEAN_FLOOR"},
        {"type": "minecraft:block_predicate_filter", "predicate": {"type": "minecraft:would_survive", "state": state("minecraft:oak_sapling", {"stage": "0"})}},
        {"type": "minecraft:biome"}]})
    write_json(cf / "wireframe_patch.json", {"type": "minecraft:random_patch", "config": {
        "tries": 12, "xz_spread": 5, "y_spread": 1, "feature": {"feature": {"type": "minecraft:simple_block", "config": {
            "to_place": simple(f"{NS}:wireframe_block")}}, "placement": [{"type": "minecraft:block_predicate_filter",
                                                                          "predicate": {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"}}]}}})
    write_json(pf / "wireframe_patch.json", {"feature": f"{NS}:wireframe_patch", "placement": [
        {"type": "minecraft:rarity_filter", "chance": 6}, {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"}, {"type": "minecraft:biome"}]})
    for name, block, lo, hi, count in (("server_rack", "server_casing", 2, 5, 3), ("corrupted_spike", "corrupted_data", 3, 9, 4)):
        write_json(cf / f"{name}.json", {"type": "minecraft:block_column", "config": {
            "direction": "up", "prioritize_tip": False,
            "allowed_placement": {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"},
            "layers": [{"height": {"type": "minecraft:uniform", "min_inclusive": lo, "max_inclusive": hi},
                        "provider": simple(f"{NS}:{block}")}]}})
        write_json(pf / f"{name}.json", {"feature": f"{NS}:{name}", "placement": [
            {"type": "minecraft:count", "count": count}, {"type": "minecraft:in_square"},
            {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"}, {"type": "minecraft:biome"}]})
    write_json(cf / "data_lake.json", {"type": "minecraft:lake", "config": {
        "fluid": simple("minecraft:water", {"level": "0"}), "barrier": simple(f"{NS}:wireframe_block")}})
    write_json(pf / "data_lake.json", {"feature": f"{NS}:data_lake", "placement": [
        {"type": "minecraft:rarity_filter", "chance": 12}, {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "WORLD_SURFACE_WG"}, {"type": "minecraft:biome"}]})


def dimension():
    write_json(D / "dimension_type" / "digital_world.json", dict(vanilla("data/minecraft/dimension_type/overworld.json"),
                                                                 has_raids=False, bed_works=True))
    ns = vanilla("data/minecraft/worldgen/noise_settings/overworld.json")
    floor = lambda depth=0: {"type": "minecraft:stone_depth", "offset": depth, "surface_type": "floor", "add_surface_depth": False,
                             "secondary_depth_range": 0}
    under = {"type": "minecraft:stone_depth", "offset": 0, "surface_type": "floor", "add_surface_depth": True,
             "secondary_depth_range": 0}
    block = lambda n: {"type": "minecraft:block", "result_state": {"Name": n}}
    biome = lambda b: {"type": "minecraft:biome", "biome_is": [f"{NS}:{b}"]}
    above = {"type": "minecraft:above_preliminary_surface"}
    ours = [
        {"type": "minecraft:condition", "if_true": above, "then_run": {"type": "minecraft:sequence", "sequence": [
            {"type": "minecraft:condition", "if_true": biome("server_continent"), "then_run": {"type": "minecraft:sequence", "sequence": [
                {"type": "minecraft:condition", "if_true": floor(), "then_run": block(f"{NS}:circuit_block")},
                {"type": "minecraft:condition", "if_true": under, "then_run": block(f"{NS}:server_casing")}]}},
            {"type": "minecraft:condition", "if_true": biome("dark_area"), "then_run": {"type": "minecraft:sequence", "sequence": [
                {"type": "minecraft:condition", "if_true": floor(), "then_run": block(f"{NS}:corrupted_data")},
                {"type": "minecraft:condition", "if_true": under, "then_run": block("minecraft:blackstone")}]}}]}}]
    ns["surface_rule"] = {"type": "minecraft:sequence", "sequence": ours + [ns["surface_rule"]]}
    write_json(D / "worldgen" / "noise_settings" / "digital_world.json", ns)
    pts = []

    def add(b, t, hum, weird=(-1.0, 0.72), cont=(-1.2, 1.2), ero=(-1.0, 1.0)):
        pts.append({"biome": f"{NS}:{b}", "parameters": {"temperature": list(t), "humidity": list(hum), "continentalness": list(cont),
                                                        "erosion": list(ero), "weirdness": list(weird), "depth": 0, "offset": 0}})
    add("file_island", (-1.0, 0.2), (-1.0, 0.25))
    add("voxel_forest", (-1.0, 1.0), (0.25, 1.0))
    add("server_continent", (0.2, 1.0), (-1.0, 0.25))
    add("dark_area", (-1.0, 1.0), (-1.0, 1.0), weird=(0.72, 1.0))
    write_json(D / "dimension" / "digital_world.json", {"type": f"{NS}:digital_world", "generator": {
        "type": "minecraft:noise", "settings": f"{NS}:digital_world", "biome_source": {"type": "minecraft:multi_noise", "biomes": pts}}})
    tags = D / "tags" / "worldgen" / "biome"
    write_json(tags / "is_digital_world.json", {"replace": False, "values": [f"{NS}:{b}" for b in BIOMES]})
    for b in BIOMES:
        write_json(tags / f"is_{b}.json", {"replace": False, "values": [f"{NS}:{b}"]})


# --- structures -----------------------------------------------------------------------------------------------------

def server_terminal():
    """An abandoned server room: circuit floor, broken casing walls, rows of racks, cobwebs, a loot chest, a rescue
    cradle and the Ancient Terminal on the back wall."""
    W, H, Dp = 11, 7, 11
    t = Template((W, H, Dp))
    for x in range(W):
        for z in range(Dp):
            t.set(x, 0, z, f"{NS}:circuit_block")
            for y in range(1, H):
                wall = x in (0, W - 1) or z in (0, Dp - 1)
                broken = h(x, y, z, 3) < 0.18 + y * 0.06
                if wall and not broken:
                    t.set(x, y, z, f"{NS}:server_casing" if y < H - 1 else f"{NS}:socket_block")
                elif not wall:
                    t.set(x, y, z, "minecraft:air")
    for z in (3, 7):
        for x in (2, 3, 4, 6, 7, 8):
            for y in (1, 2):
                if h(x, y, z, 5) > 0.15:
                    t.set(x, y, z, f"{NS}:server_casing")
    for (x, y, z) in ((1, 3, 1), (9, 4, 2), (1, 2, 8), (8, 3, 9), (5, 4, 5)):
        t.set(x, y, z, "minecraft:cobweb")
    t.set(5, 1, Dp - 2, f"{NS}:ancient_terminal", {"facing": "north"})
    t.set(1, 1, 5, "minecraft:chest", {"facing": "east", "type": "single", "waterlogged": "false"},
          {"LootTable": f"{NS}:chests/server_terminal"})
    t.set(9, 1, 5, f"{NS}:wild_digitama_cradle", {"egg": "true"})
    t.set(5, 1, 0, "minecraft:air")
    t.set(5, 2, 0, "minecraft:air")
    return t


def primary_village():
    """Primary Village: a soft meadow of pastel toy blocks round rows of Digitama cradles, two little huts."""
    W, Dp = 23, 23
    t = Template((W, 8, Dp))
    pastel = ["minecraft:pink_concrete", "minecraft:light_blue_concrete", "minecraft:yellow_concrete", "minecraft:lime_concrete",
              "minecraft:white_concrete"]
    for x in range(W):
        for z in range(Dp):
            nursery = 6 <= x <= 16 and 7 <= z <= 15
            path = (x == 11 or z == 11) and not nursery
            t.set(x, 0, z, "minecraft:white_wool" if nursery else "minecraft:pink_concrete" if path else "minecraft:moss_block")
            for y in range(1, 8):
                t.set(x, y, z, "minecraft:air")
    for i, (x, z) in enumerate((x, z) for x in range(7, 16, 2) for z in (8, 11, 14)):
        t.set(x, 1, z, f"{NS}:digitama_cradle", {"egg": "true"})
    for (x, z) in ((2, 3), (4, 19), (19, 4), (20, 18), (11, 2), (2, 12), (20, 11)):
        t.set(x, 1, z, pastel[int(h(x, z) * 5)])
        if h(x, z, 2) > 0.5:
            t.set(x, 2, z, pastel[int(h(x, z, 3) * 5)])
    for (hx, hz) in ((2, 6), (16, 17)):
        for x in range(hx, hx + 5):
            for z in range(hz, hz + 4):
                edge = x in (hx, hx + 4) or z in (hz, hz + 3)
                for y in range(1, 4):
                    t.set(x, y, z, pastel[(x + z) % 5] if edge else "minecraft:air")
                t.set(x, 4, z, "minecraft:white_wool")
        t.set(hx + 2, 1, hz, "minecraft:air")
        t.set(hx + 2, 2, hz, "minecraft:air")
        t.set(hx + 2, 1, hz + 2, "minecraft:chest", {"facing": "north", "type": "single", "waterlogged": "false"},
              {"LootTable": f"{NS}:chests/primary_village"})
    return t


def socket_cliff():
    """A plug-in socket cliff: a casing monolith faced with socket panels, cables trailing down its sides."""
    W, H, Dp = 12, 18, 7
    t = Template((W, H, Dp))
    for x in range(W):
        for z in range(Dp):
            top = H - 1 - int(3 * h(x // 3, z // 2, 8))
            for y in range(top):
                face = z == 0 or x in (0, W - 1)
                t.set(x, y, z, f"{NS}:socket_block" if face and y % 4 == 2 and 1 < x < W - 2 else f"{NS}:server_casing")
    for x in (2, 6, 9):                          # cables down the front
        for y in range(1, 13 - x % 4):
            t.set(x, y, 0, "minecraft:black_concrete")
    return t


def dark_tower():
    """A Dark Tower: a tapering obsidian spire banded with black glass 'wireframe' and crying obsidian, a ladder up
    the hollow core to a chamber holding the core block and a chest."""
    W, H = 9, 40
    t = Template((W, H, W))
    c = W // 2
    for y in range(H):
        r = 4 - (y * 3) // H                      # half-width 4 at the base to 1 at the top
        for x in range(c - r, c + r + 1):
            for z in range(c - r, c + r + 1):
                edge = x in (c - r, c + r) or z in (c - r, c + r)
                if y in (0, 33):
                    t.set(x, y, z, "minecraft:obsidian")
                elif edge:
                    band = y % 6 == 3
                    t.set(x, y, z, "minecraft:black_stained_glass" if band else
                          "minecraft:crying_obsidian" if h(x, y, z, 4) > 0.86 else "minecraft:obsidian")
                elif y < 33 or y > 33:
                    t.set(x, y, z, "minecraft:air")
    for y in range(1, 34):                       # a ladder up the hollow core, on an obsidian spine
        t.set(c, y, c, "minecraft:ladder", {"facing": "south", "waterlogged": "false"})
        if y < 33:
            t.set(c, y, c - 1, "minecraft:obsidian")
    t.set(c, 34, c + 1, f"{NS}:dark_tower_core")
    t.set(c - 1, 34, c - 1, "minecraft:chest", {"facing": "east", "type": "single", "waterlogged": "false"},
          {"LootTable": f"{NS}:chests/dark_tower"})
    r = 4 - (3 * (H - 1)) // H
    for x in range(c - r, c + r + 1):
        for z in range(c - r, c + r + 1):
            t.set(x, H - 1, z, "minecraft:obsidian")
    t.set(c, 1, c - 4, "minecraft:air")
    t.set(c, 2, c - 4, "minecraft:air")
    return t


def colosseum():
    """The Colosseum: a round arena of smooth stone ringed by stepped stone-brick stands, with three marked podiums
    where its Tamers wait (Tamers.java spawns them when someone comes near)."""
    R = 14
    W = 2 * R + 1
    t = Template((W, 8, W))
    c = R
    for x in range(W):
        for z in range(W):
            d = math.hypot(x - c, z - c)
            if d > R + 0.5:
                continue
            t.set(x, 0, z, "minecraft:smooth_stone" if d < 9.5 else "minecraft:stone_bricks")
            for y in range(1, 8):
                t.set(x, y, z, "minecraft:air")
            if d >= 10.5:
                step = min(5, int(d - 10.5) + 1)
                gate = abs(x - c) <= 1 or abs(z - c) <= 1
                for y in range(1, step + 1):
                    if not gate:
                        t.set(x, y, z, "minecraft:stone_brick_stairs" if y == step and d < R else "minecraft:stone_bricks",
                              {"facing": "north", "half": "bottom", "shape": "straight", "waterlogged": "false"} if y == step and d < R else None)
            if 9.5 <= d < 10.5:
                t.set(x, 0, z, "minecraft:chiseled_stone_bricks")
    for dx, dz, col in ((-5, 0, "minecraft:red_concrete"), (0, -5, "minecraft:blue_concrete"), (5, 0, "minecraft:yellow_concrete")):
        for ox in (-1, 0, 1):
            for oz in (-1, 0, 1):
                t.set(c + dx + ox, 0, c + dz + oz, col)
    for ang in range(0, 360, 45):
        x, z = int(round(c + math.cos(math.radians(ang)) * (R - 1))), int(round(c + math.sin(math.radians(ang)) * (R - 1)))
        t.set(x, 6, z, "minecraft:lantern", {"hanging": "false", "waterlogged": "false"})
        t.set(x, 5, z, "minecraft:stone_bricks")
    return t


STRUCTURES = {  # name: (builder, biomes, spacing, separation, salt, terrain adaptation, start y)
    "server_terminal": (server_terminal, ["#minecraft:is_forest", "#minecraft:is_taiga", "#minecraft:is_savanna", "#minecraft:is_badlands",
                                          "minecraft:plains", "minecraft:desert", "minecraft:meadow", "minecraft:snowy_plains",
                                          f"#{NS}:is_digital_world"], 36, 12, 7331, "beard_thin", 0),
    "primary_village": (primary_village, [f"{NS}:file_island"], 24, 8, 7332, "beard_thin", 0),
    "socket_cliff": (socket_cliff, [f"{NS}:server_continent"], 10, 4, 7333, "beard_thin", 0),
    "colosseum": (colosseum, ["minecraft:plains", "minecraft:sunflower_plains", "minecraft:savanna", "minecraft:desert",
                              "minecraft:meadow"], 56, 20, 7335, "beard_thin", 0),
    "dark_tower": (dark_tower, ["#minecraft:is_forest", "#minecraft:is_taiga", "#minecraft:is_savanna", "#minecraft:is_badlands",
                                "minecraft:plains", "minecraft:desert", "minecraft:meadow", f"{NS}:dark_area"], 48, 16, 7334, "beard_thin", 0),
}


def structures():
    for name, (builder, biomes, spacing, sep, salt, adapt, y) in STRUCTURES.items():
        t = builder()
        p = D / "structure" / f"{name}.nbt"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(Nbt.file(t.data()))
        write_json(D / "worldgen" / "template_pool" / f"{name}.json", {"fallback": "minecraft:empty", "elements": [{
            "weight": 1, "element": {"element_type": "minecraft:single_pool_element", "location": f"{NS}:{name}",
                                     "processors": "minecraft:empty", "projection": "rigid"}}]})
        write_json(D / "tags" / "worldgen" / "biome" / "has_structure" / f"{name}.json", {"replace": False, "values": biomes})
        write_json(D / "worldgen" / "structure" / f"{name}.json", {
            "type": "minecraft:jigsaw", "biomes": f"#{NS}:has_structure/{name}", "step": "surface_structures",
            "spawn_overrides": {}, "terrain_adaptation": adapt, "start_pool": f"{NS}:{name}", "size": 1,
            "start_height": {"absolute": y}, "project_start_to_heightmap": "WORLD_SURFACE_WG",
            "max_distance_from_center": 80, "use_expansion_hack": False})
        write_json(D / "worldgen" / "structure_set" / f"{name}.json", {
            "structures": [{"structure": f"{NS}:{name}", "weight": 1}],
            "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": sep, "salt": salt}})
        print(f"  {name}: {t.size}, {len(t.blocks)} blocks")


def loot():
    n = lambda s: f"{NS}:{s}"
    item = lambda i, w, lo=1, hi=1: {"type": "minecraft:item", "name": i, "weight": w,
                                     "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi}}]}
    tables = {
        "server_terminal": [(3, 6, [item(n("vaccine_fragment"), 10, 2, 5), item(n("data_fragment"), 10, 2, 5), item(n("virus_fragment"), 10, 2, 5),
                                    item(n("digi_core"), 8, 1, 2), item(n("chrome_digizoid_ingot"), 3), item(n("high_speed_plugin"), 4),
                                    item(n("metal_armor"), 4), item(n("recovery_disk"), 4), item("minecraft:redstone", 8, 3, 9)]),
                            (1, 1, [item(n("digiegg_of_courage"), 3), item(n("digiegg_of_friendship"), 3), item(n("vaccine_chip"), 2),
                                    item(n("data_chip"), 2), item(n("virus_chip"), 2), item(n("digimon_tag"), 1),
                                    *[item(n(f"crest_of_{c}"), 1) for c in CREST_LOOK], {"type": "minecraft:empty", "weight": 14}])],
        "primary_village": [(2, 4, [item(n("digimeat"), 10, 2, 6), item(n("super_carrot"), 4, 1, 2), item(n("sirloin"), 2),
                                    item(n("digitama"), 2), item(n("wireframe_ball"), 6, 2, 4)])],
        "dark_tower": [(3, 5, [item(n("virus_fragment"), 10, 3, 8), item(n("dark_spore"), 4), item(n("chrome_digizoid_ingot"), 4, 1, 2),
                               item(n("virus_chip"), 3), item(n("dot_virus"), 4), item(n("bug_card"), 4), item(n("giga_destroyer"), 3)])],
    }
    for name, pools in tables.items():
        write_json(D / "loot_table" / "chests" / f"{name}.json", {"type": "minecraft:chest", "pools": [
            {"rolls": {"type": "minecraft:uniform", "min": lo, "max": hi}, "entries": entries} for lo, hi, entries in pools]})


# --- spawns: every Digimon by its labels -----------------------------------------------------------------------------

STAGE_BUCKET = {"digimon_baby2": ("common", 3.0, "3-10"), "digimon_child": ("common", 5.0, "8-22"),
                "digimon_adult": ("uncommon", 2.5, "20-35"), "digimon_perfect": ("rare", 0.8, "35-50"),
                "digimon_ultimate": ("ultra-rare", 0.2, "50-65")}
TYPE_BIOME = {"water": "file_island", "ice": "file_island", "normal": "file_island", "fairy": "file_island", "flying": "file_island",
              "grass": "voxel_forest", "bug": "voxel_forest", "poison": "voxel_forest", "ground": "voxel_forest",
              "steel": "server_continent", "electric": "server_continent", "psychic": "server_continent", "rock": "server_continent",
              "fire": "server_continent", "fighting": "server_continent", "dragon": "server_continent",
              "dark": "dark_area", "ghost": "dark_area"}


def spawns():
    sp_dir = ROOT / "data" / "cobbleeffort" / "species"
    out, dark = [], []
    for f in sorted(sp_dir.glob("*/*.json")):
        d = json.loads(f.read_text())
        labels = set(d.get("labels", []))
        if "digimon" not in labels or "legendary" in labels:
            continue
        stage = next((s for s in STAGE_BUCKET if s in labels), None)
        if stage is None:
            continue
        bucket, weight, lv = STAGE_BUCKET[stage]
        sid = f"cobbleeffort:{f.stem}"
        home = TYPE_BIOME.get(d.get("primaryType", "normal"), "file_island")
        virus = "digimon_virus" in labels
        biomes = [f"#{NS}:is_{home}"] + ([f"#{NS}:is_dark_area"] if virus and home != "dark_area" else [])
        if home == "dark_area" and not virus:
            biomes = [f"#{NS}:is_file_island"]
        out.append({"id": f"digital-{f.stem}", "pokemon": sid, "presets": ["natural"], "type": "pokemon", "context": "grounded",
                    "bucket": bucket, "level": lv, "weight": weight, "condition": {"biomes": biomes}})
    for sid, w in (("picodevimon", 12.0), ("bakemon", 10.0)):
        dark.append({"id": f"digital-dark-{sid}", "pokemon": f"cobbleeffort:{sid}", "presets": ["natural"], "type": "pokemon",
                     "context": "grounded", "bucket": "common", "level": "12-30", "weight": w,
                     "condition": {"biomes": [f"#{NS}:is_dark_area"]}})
    write_json(ROOT / "data" / "cobbleeffort" / "spawn_pool_world" / "digital_world.json",
               {"enabled": True, "neededInstalledMods": [], "neededUninstalledMods": [], "spawns": out + dark})
    print(f"  spawns: {len(out)} Digimon in the Digital World, {len(dark)} Dark Area regulars")


CREST_HOW = {"courage": "Charges when you win a battle with a Pokémon down to a quarter of its HP.",
             "friendship": "Charges as you feed and train your Pokémon.",
             "love": "Charges when eggs and Digitama hatch.",
             "knowledge": "Charges as you scan new species with the Digivice and craft chips and cards.",
             "sincerity": "Charges as you harvest ripe crops.",
             "reliability": "Charges when you trade, and when you win battles beside other players.",
             "hope": "Charges when you win a battle with one Pokémon left standing.",
             "light": "Charges when you win battles by day under open sky."}
LANG = {
    f"item.{NS}.digimon_tag": "Tag",
    **{f"item.{NS}.crest_of_{c}": f"Crest of {c.title()}" for c in CREST_HOW},
    **{f"{NS}.crest.{c}": c.title() for c in CREST_HOW},
    **{f"{NS}.crest.{c}.how": t for c, t in CREST_HOW.items()},
    f"{NS}.crest.tooltip": "Hold a Tag in your other hand and use the Crest to socket it.",
    f"{NS}.crest.tag_tooltip": "Wear it (Accessories necklace slot) or carry it. Full: use it on your Digimon to digivolve it a stage, or warp for free with the Digivice (sneak), up to two stages from Adult.",
    f"{NS}.crest.empty_tag": "No Crest socketed.",
    f"{NS}.crest.tag_line": "Crest of %s: %s%%",
    f"{NS}.crest.need_tag": "Hold a Tag in your other hand to socket the Crest.",
    f"{NS}.crest.socketed": "Socketed the Crest of %s.",
    f"{NS}.crest.charging": "Crest of %s: %s%%",
    f"{NS}.crest.full": "Your Crest of %s is shining! Your Digimon can reach Ultimate and Mega.",
    f"{NS}.crest.not_full": "The Crest isn't charged yet (%s%%).",
    f"{NS}.crest.evolved": "%s digivolves with the power of the Crest of %s!",
    f"{NS}.raid.started": "A Digital Rift is tearing open: %s is coming through near %s, %s!",
    f"{NS}.raid.boss": "%s (phase %s/%s)",
    f"{NS}.raid.bar": "Raid: %s (phase %s/%s)",
    f"{NS}.raid.phase": "The raid boss reformats its data: phase %s/%s!",
    f"{NS}.raid.beaten": "The raid boss is deleted! Everyone who fought it shares the spoils.",
    f"{NS}.raid.gone": "The raid boss slips back through the rift.",
    f"{NS}.raid.reward": "Raid reward: Chrome Digizoid, a Crest and a Digi-Core.",
    "gamerule.digitalDigitization": "Raid bosses digitize the land round their rift",
    "gamerule.digitalMoveGriefing": "Digimon attacks change the world (fire, glass, blasts, puddles)",
    "gamerule.digitalDigimonOnly": "Only Digimon spawn in the wild (other spawns become Digimon)",
    "gamerule.digitalNoWildDigimon": "No wild Digimon outside the Digital World",
    "gamerule.digitalAutoHatch": "Warm Digitama hatch by themselves",
    "gamerule.digitalDigitamaHatchSeconds": "Seconds a Digitama must be carried before it hatches",
    "gamerule.digitalDigitamaDropChance": "Chance (%) a defeated Digimon leaves a Digitama",
    "gamerule.digitalFreeDigivolution": "Digivolving and Bio-Merge cost no Tamer Energy",
    "gamerule.digitalRaids": "Demon Lord and Royal Knight raids start by themselves",
    "gamerule.digitalRifts": "Rifts to the Digital World open by themselves",
    "gamerule.digitalDarkTowerAura": "Dark Towers stop Digimon digivolving nearby",
    "gamerule.digitalStrictCatching": "Perfect and stronger Digimon need a Chrome Digizoid Ball",
    f"block.{NS}.circuit_block": "Circuit Block",
    f"block.{NS}.server_casing": "Server Casing",
    f"block.{NS}.socket_block": "Plug-in Socket",
    f"block.{NS}.wireframe_block": "Wireframe Block",
    f"block.{NS}.voxel_log": "Voxel Log",
    f"block.{NS}.voxel_leaves": "Voxel Leaves",
    f"block.{NS}.corrupted_data": "Corrupted Data",
    f"block.{NS}.dark_tower_core": "Dark Tower Core",
    f"block.{NS}.ancient_terminal": "Ancient Terminal",
    f"block.{NS}.digitama_cradle": "Digitama Cradle",
    f"block.{NS}.wild_digitama_cradle": "Abandoned Digitama Cradle",
    f"item.{NS}.dark_spore": "Dark Spore",
    f"item.{NS}.dark_spore.tooltip": "Use it on your Digimon: rewrites it to Virus and forces a Virus digivolution, if it has one.",
    f"item.{NS}.digi_core": "Digi-Core",
    f"item.{NS}.digi_core.tooltip": "The heart of an old server. Crafts Ancient Terminals.",
    f"biome.{NS}.file_island": "File Island",
    f"biome.{NS}.voxel_forest": "Voxel Forest",
    f"biome.{NS}.server_continent": "Server Continent",
    f"biome.{NS}.dark_area": "Dark Area",
    f"{NS}.world.missing": "The Digital World isn't loaded on this server.",
    f"{NS}.world.arrived": "You were digitized into the Digital World!",
    f"{NS}.world.rift_opened": "A Digital Rift tore open nearby!",
    f"{NS}.world.data_stream": "Data stream: Tamer Energy %s/%s",
    f"{NS}.world.terminal_needs_digivice": "The terminal hums. Use it holding a Digivice.",
    f"{NS}.cradle.price": "Trade %s Digi-Meat for this Digitama (use the meat on the cradle).",
    f"{NS}.cradle.empty": "The cradle is empty. A new Digitama will turn up in time.",
    f"{NS}.cradle.traded": "You traded for a Digitama!",
    f"{NS}.cradle.rescued": "You rescued an abandoned Digitama!",
    f"{NS}.tower.broken": "The Dark Tower's core shatters... and its guardian answers!",
    f"{NS}.tower.guardian": "Guardian %s",
    f"{NS}.tower.cleared": "The Dark Tower's guardian is beaten: its aura is gone.",
    f"{NS}.spore.none": "%s has no Virus digivolution to force.",
    f"{NS}.spore.used": "The Dark Spore takes hold of %s!",
    f"{NS}.merchant.name": "Shady %s",
    f"{NS}.merchant.appears": "Someone shady is lurking nearby...",
    f"{NS}.guard.name": "Primary Village Guard",
    f"structure.{NS}.colosseum": "Colosseum",
}


CREST_LOOK = {  # crest: (colour, symbol painter) -- original symbols on a rounded tag
    "courage": (240, 130, 40), "friendship": (60, 120, 220), "love": (220, 60, 90), "knowledge": (150, 80, 200),
    "sincerity": (60, 180, 90), "reliability": (90, 110, 140), "hope": (240, 210, 60), "light": (250, 190, 220)}


def crest_symbol(name, x, y):
    u, v = x - 7.5, y - 8
    if name == "courage":       # a sun: disc and rays
        return math.hypot(u, v) < 2.3 or (abs(u) < 0.6 or abs(v) < 0.6 or abs(abs(u) - abs(v)) < 0.6) and math.hypot(u, v) < 4.2
    if name == "friendship":    # two linked rings
        return 1.2 < math.hypot(u + 1.4, v) < 2.4 or 1.2 < math.hypot(u - 1.4, v) < 2.4
    if name == "love":          # a heart
        return (math.hypot(u + 1.5, v + 1.2) < 1.7 or math.hypot(u - 1.5, v + 1.2) < 1.7
                or (-1.2 <= v <= 3.2 and abs(u) < 3.1 * (1 - (v + 1.2) / 4.4)))
    if name == "knowledge":     # a diamond with a dot
        return abs(u) + abs(v) < 3.6 and not (abs(u) + abs(v) < 2.2 and math.hypot(u, v) > 0.8)
    if name == "sincerity":     # a drop
        return math.hypot(u, v - 0.8) < 2.4 or (v < 0.8 and abs(u) < (v + 3.5) * 0.6)
    if name == "reliability":   # a cross of bars
        return (abs(u) < 0.9 and abs(v) < 3.5) or (abs(v) < 0.9 and abs(u) < 3.5)
    if name == "hope":          # a star
        a = math.atan2(v, u)
        return math.hypot(u, v) < 2.0 + 1.6 * abs(math.cos(a * 2.5))
    return 1.8 < math.hypot(u, v) < 3.4 or math.hypot(u, v) < 0.9   # light: a halo


def crest_icon(name):
    col = CREST_LOOK[name]

    def f(x, y):
        u, v = abs(x - 7.5), abs(y - 8)
        if u > 6 or v > 6.5 or (u > 4.5 and v > 5):
            return None
        if u > 5 or v > 5.5 or (u > 3.8 and v > 4.6):
            return (70, 60, 40)
        if crest_symbol(name, x, y):
            return C(col, 1.0)
        return (210, 190, 120) if (x + y) % 7 else (230, 214, 150)
    return tile(f)


def tag_icon():
    def f(x, y):
        if y <= 6 and abs((x - 7.5) ** 2 / 25 + (y - 7) ** 2 / 36 - 1) < 0.18:
            return (200, 200, 210)                       # the chain
        if 7 <= y <= 14 and 4 <= x <= 11:
            edge = x in (4, 11) or y in (7, 14)
            return (70, 76, 90) if edge else (170, 176, 190) if (x + y) % 5 else (220, 224, 236)
        return None
    return tile(f)


def build():
    for c in CREST_LOOK:
        save(crest_icon(c), f"item/crest_of_{c}.png")
        write_json(A / "models" / "item" / f"crest_of_{c}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/crest_of_{c}"}})
    save(tag_icon(), "item/digimon_tag.png")
    write_json(A / "models" / "item" / "digimon_tag.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/digimon_tag"}})
    write_json(ROOT / "data" / "accessories" / "tags" / "item" / "necklace.json", {"replace": False, "values": [f"{NS}:digimon_tag"]})
    write_json(D / "recipe" / "digimon_tag.json", {
        "type": "minecraft:crafting_shaped", "category": "misc", "pattern": [" S ", "S S", " I "],
        "key": {"S": {"item": "minecraft:chain"}, "I": {"item": f"{NS}:chrome_digizoid_ingot"}},
        "result": {"id": f"{NS}:digimon_tag", "count": 1}})
    block_textures()
    item_textures()
    block_models()
    biomes()
    dimension()
    structures()
    loot()
    spawns()
    write_json(D / "recipe" / "ancient_terminal.json", {
        "type": "minecraft:crafting_shaped", "category": "misc", "pattern": ["SGS", "SCS", "SSS"],
        "key": {"S": {"item": "minecraft:smooth_stone"}, "G": {"item": "minecraft:glass_pane"}, "C": {"item": f"{NS}:digi_core"}},
        "result": {"id": f"{NS}:ancient_terminal", "count": 1}})
    write_json(D / "recipe" / "digi_core.json", {
        "type": "minecraft:crafting_shaped", "category": "misc", "pattern": ["RDR", "DCD", "RDR"],
        "key": {"R": {"item": "minecraft:redstone"}, "D": {"item": f"{NS}:data_fragment"}, "C": {"item": f"{NS}:chrome_digizoid_ingot"}},
        "result": {"id": f"{NS}:digi_core", "count": 1}})
    tags = ROOT / "data" / "minecraft" / "tags" / "block"
    for tag, vals in (("mineable/pickaxe", ["circuit_block", "server_casing", "socket_block", "corrupted_data", "dark_tower_core",
                                            "ancient_terminal", "wireframe_block"]),
                      ("mineable/axe", ["voxel_log", "digitama_cradle", "wild_digitama_cradle"]),
                      ("mineable/hoe", ["voxel_leaves"]), ("logs", ["voxel_log"]), ("leaves", ["voxel_leaves"]),
                      ("needs_diamond_tool", ["dark_tower_core"])):
        p = tags / f"{tag}.json"
        obj = json.loads(p.read_text()) if p.exists() else {"replace": False, "values": []}
        obj["values"] = sorted(set(obj["values"]) | {f"{NS}:{v}" for v in vals})
        write_json(p, obj)
    return LANG


if __name__ == "__main__":
    lang = build()
    f = A / "lang" / "en_us.json"
    d = json.loads(f.read_text()) if f.exists() else {}
    d.update(lang)
    write_json(f, dict(sorted(d.items())))
