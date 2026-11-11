#!/usr/bin/env python3
"""
CobbleEffort: Kanto's assets and data (all original art, painted here): Gen 1 Bricks (black, white, grey), the
glitchy PC (dead and lit, with an animated screen), the Kantonian Orb and Essence of Olde, the Gen 1-styled lab
(a structure template joined to every village's houses), the Kanto dimension (large-biome terrain, its own sky; only
Gen 1 Pokémon spawn there, see KantoEvents), recipes, loot tables, tags and English names.

Usage: python3 tools/make_assets.py
"""
from __future__ import annotations

import gzip
import io
import json
import math
import struct
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "common" / "src" / "main" / "resources"
MOD = "cobbleeffort_kanto"
A = RES / "assets" / MOD
D = RES / "data" / MOD
DATA_VERSION = 3955                                          # Minecraft 1.21.1

BRICKS = {"black": [(14, 14, 18), (34, 34, 40), (58, 58, 66), (90, 90, 100)],
          "grey": [(70, 70, 76), (112, 112, 120), (150, 150, 158), (188, 188, 196)],
          "white": [(150, 150, 156), (200, 200, 206), (228, 228, 232), (250, 250, 252)]}
# the Game Boy's four greens, for Essence of Olde (the oldest colours there are)
DMG = [(15, 56, 15), (48, 98, 48), (139, 172, 15), (155, 188, 15)]

LANG = {
    f"itemGroup.{MOD}": "Kanto",
    f"block.{MOD}.gen1_bricks_black": "Black Gen 1 Bricks",
    f"block.{MOD}.gen1_bricks_white": "White Gen 1 Bricks",
    f"block.{MOD}.gen1_bricks_grey": "Grey Gen 1 Bricks",
    f"block.{MOD}.glitchy_pc": "Glitchy PC",
    f"item.{MOD}.kantonian_orb": "Kantonian Orb",
    f"item.{MOD}.essence_of_olde": "Essence of Olde",
    f"{MOD}.pc.dead": "The screen is dark and fizzing. Something old might wake it...",
    f"{MOD}.pc.woken": "The PC flickers to life. A strange region glows on the screen.",
    f"{MOD}.pc.arrived": "Welcome to Kanto. Use the PC to go home.",
    f"{MOD}.pc.no_kanto": "Kanto can't be reached on this server.",
    f"{MOD}.essence.dropped": "%s left behind Essence of Olde!",
}


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def save(img: Image.Image, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, optimize=True)


def h(*a):
    v = 2166136261
    for x in a:
        v = ((v ^ (int(x) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return v / 0xFFFFFFFF


# --- textures ----------------------------------------------------------------------------------------------------------
def bricks(pal):
    """Chunky 8-bit bricks: a dark mortar grid, each brick lit at its top-left edge and dithered in two shades."""
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            row = y // 4
            ox = (x + (4 if row % 2 else 0)) % 8
            if y % 4 == 3 or ox == 7:
                c = pal[0]                                       # mortar
            elif y % 4 == 0 or ox == 0:
                c = pal[3]                                       # lit edge
            else:
                c = pal[2] if (x + y) % 2 == 0 or h(x // 8, row) > 0.5 else pal[1]
            im.putpixel((x, y), c + (255,))
    return im


def pc_side():
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            c = (196, 192, 180)
            if x in (0, 15) or y in (0, 15):
                c = (120, 116, 108)
            elif y in (3, 4) and 3 <= x <= 12 and x % 2:
                c = (90, 88, 84)                                 # vents
            im.putpixel((x, y), c + (255,))
    return im


def pc_front(frame=None):
    """The monitor: a beige bezel and a CRT. Dead: dark with faint static. Lit: a garbled map of a region, scanlines
    and glitch bars that jump between frames."""
    im = pc_side()
    for y in range(2, 11):
        for x in range(2, 14):
            if frame is None:
                k = h(x, y, 3)
                c = (24, 26, 30) if k > 0.12 else (60, 64, 70)
            else:
                # a tiny overhead map: water, land, a route, towns; offset by a glitch on some rows
                shift = 2 if h(y, frame, 7) > 0.75 else 0
                gx = (x + shift) % 16
                land = math.sin(gx * 0.7 + y * 0.4) + math.cos(y * 0.9 - gx * 0.3) > 0.2
                c = (96, 200, 120) if land else (70, 120, 220)
                if y == 6 and 3 <= gx <= 12:
                    c = (230, 210, 140)                          # a route
                if (gx, y) in ((4, 4), (11, 8), (8, 3)):
                    c = (240, 70, 70)                            # towns
                if y % 2 == 0:
                    c = tuple(int(v * 0.82) for v in c)          # scanlines
                if h(x, y, frame, 11) > 0.93:
                    c = (255, 0, 255) if h(x, frame) > 0.5 else (0, 255, 255)   # glitch pixels
            im.putpixel((x, y), c + (255,))
    for x in range(4, 12):
        im.putpixel((x, 12), (90, 88, 84, 255))                  # the keyboard slot
    im.putpixel((12, 13), (90, 255, 120, 255) if frame is not None else (60, 70, 60, 255))   # power light
    return im


def orb():
    """The Kantonian Orb: a glass sphere holding a swirl of the Distortion World's violet and the Game Boy's green."""
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(16):
        for x in range(16):
            dx, dy = x - 7.5, y - 7.5
            r = math.hypot(dx, dy)
            if r > 6.6:
                continue
            ang = math.atan2(dy, dx) + r * 0.5
            swirl = 0.5 + 0.5 * math.sin(ang * 2)
            c = tuple(int(DMG[2][i] * swirl + (120, 50, 190)[i] * (1 - swirl)) for i in range(3))
            if r > 5.8:
                c = (40, 20, 60)
            if (x, y) in ((5, 4), (5, 5), (6, 4)):
                c = (240, 255, 240)
            im.putpixel((x, y), c + (255,))
    return im


def essence():
    """Essence of Olde: a wisp in a bottle, in the Game Boy's four greens."""
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(1, 16):
        for x in range(16):
            neck = 6 <= x <= 9 and 1 <= y <= 4
            body = math.hypot(x - 7.5, (y - 10) * 1.15) <= 5.4 and y >= 4
            if not (neck or body):
                continue
            c = DMG[0] if (neck and y == 1) else DMG[1]
            if body and math.hypot(x - 7.5, (y - 10) * 1.15) > 4.6:
                c = DMG[0]
            wisp = abs(x - 7.5 - 1.6 * math.sin(y * 0.9)) < 1.2 and 6 <= y <= 13
            if wisp:
                c = DMG[3] if y % 2 else DMG[2]
            im.putpixel((x, y), c + (255,))
    return im


def icon():
    im = pc_front(1).resize((128, 128), Image.NEAREST)
    return im


# --- structure templates (NBT) ------------------------------------------------------------------------------------------
class Nbt:
    """A minimal NBT writer: ints, strings, lists and compounds (all a structure template needs)."""

    @staticmethod
    def name(s):
        b = s.encode("utf-8")
        return struct.pack(">H", len(b)) + b

    @classmethod
    def tag_type(cls, v):
        return 3 if isinstance(v, int) else 8 if isinstance(v, str) else 9 if isinstance(v, list) else 10

    @classmethod
    def payload(cls, v):
        t = cls.tag_type(v)
        if t == 3:
            return struct.pack(">i", v)
        if t == 8:
            return cls.name(v)
        if t == 9:
            et = cls.tag_type(v[0]) if v else 0
            return struct.pack(">bi", et, len(v)) + b"".join(cls.payload(x) for x in v)
        out = b""
        for k, x in v.items():
            out += struct.pack(">b", cls.tag_type(x)) + cls.name(k) + cls.payload(x)
        return out + b"\x00"

    @classmethod
    def file(cls, root):
        return gzip.compress(struct.pack(">b", 10) + cls.name("") + cls.payload(root), mtime=0)


class Template:
    def __init__(self, size):
        self.size = size
        self.blocks = {}                                         # (x, y, z) -> (name, props, nbt)

    def set(self, x, y, z, name, props=None, nbt=None):
        self.blocks[(x, y, z)] = (name, props or {}, nbt)

    def fill(self, x0, y0, z0, x1, y1, z1, name, props=None):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    self.set(x, y, z, name, props)

    def data(self):
        palette, index, blocks = [], {}, []
        for pos in sorted(self.blocks, key=lambda p: (p[1], p[2], p[0])):
            name, props, nbt = self.blocks[pos]
            key = (name, tuple(sorted(props.items())))
            if key not in index:
                index[key] = len(palette)
                palette.append({"Name": name, **({"Properties": dict(sorted(props.items()))} if props else {})})
            entry = {"pos": list(pos), "state": index[key]}
            if nbt:
                entry["nbt"] = nbt
            blocks.append(entry)
        return {"DataVersion": DATA_VERSION, "size": list(self.size), "palette": palette, "blocks": blocks, "entities": []}


def lab():
    """A Gen 1-styled research lab (an original layout): grey brick walls with black corner pillars and trim, a two-tier
    roof, a chequered floor, bookcases, counters, a central table, hanging lanterns, and the glitchy PC on the back wall
    facing the door. The entrance jigsaw sits in front of the door (z = 0), where the village street joins it."""
    W, H, Dp = 13, 8, 12
    t = Template((W, H, Dp))
    B, Wt, G = f"{MOD}:gen1_bricks_black", f"{MOD}:gen1_bricks_white", f"{MOD}:gen1_bricks_grey"
    z0, z1 = 1, Dp - 1
    # floor: black border, white/grey chequers inside
    for x in range(W):
        for z in range(z0, z1 + 1):
            edge = x in (0, W - 1) or z in (z0, z1)
            t.set(x, 0, z, B if edge else (Wt if (x + z) % 2 == 0 else G))
    # walls and interior air
    for y in range(1, 5):
        for x in range(W):
            for z in range(z0, z1 + 1):
                wall = x in (0, W - 1) or z in (z0, z1)
                corner = x in (0, W - 1) and z in (z0, z1)
                if wall:
                    t.set(x, y, z, B if (corner or y == 4) else G)
                else:
                    t.set(x, y, z, "minecraft:air")
    # windows: sides and front
    for z in (4, 5, 7, 8):
        for y in (2, 3):
            t.set(0, y, z, "minecraft:glass")
            t.set(W - 1, y, z, "minecraft:glass")
    for x in (2, 3, 9, 10):
        for y in (2, 3):
            t.set(x, y, z0, "minecraft:glass")
    # the door
    door = {"facing": "south", "hinge": "left", "open": "false", "powered": "false"}
    t.set(6, 1, z0, "minecraft:oak_door", dict(door, half="lower"))
    t.set(6, 2, z0, "minecraft:oak_door", dict(door, half="upper"))
    t.set(5, 3, z0, B)
    t.set(7, 3, z0, B)
    # roof: white bricks with a black rim, and a raised grey middle
    for x in range(W):
        for z in range(z0, z1 + 1):
            t.set(x, 5, z, B if (x in (0, W - 1) or z in (z0, z1)) else Wt)
    for x in range(2, W - 2):
        for z in range(z0 + 3, z1 - 2):
            t.set(x, 6, z, B if x in (2, W - 3) or z in (z0 + 3, z1 - 3) else G)
    # interior: the PC on the back wall, bookcases either side
    t.set(6, 1, z1 - 1, f"{MOD}:glitchy_pc", {"facing": "south", "lit": "false"})
    for x in (1, 2, 3, 9, 10, 11):
        for y in (1, 2, 3):
            t.set(x, y, z1 - 1, "minecraft:bookshelf")
    for z in range(3, 8):
        t.set(W - 2, 1, z, "minecraft:bookshelf")
        t.set(W - 2, 2, z, "minecraft:bookshelf")
    # counters along the left wall (machines and drawers)
    for z, block in ((3, "minecraft:smoker"), (4, "minecraft:barrel"), (5, "minecraft:cartography_table"),
                     (6, "minecraft:barrel"), (7, "minecraft:smithing_table")):
        props = {"facing": "east", "lit": "false"} if block == "minecraft:smoker" else {"facing": "up", "open": "false"} if block == "minecraft:barrel" else {}
        t.set(1, 1, z, block, props)
    # the central table, with a lectern and a brewing stand
    for x in (5, 6, 7):
        t.set(x, 1, 6, "minecraft:smooth_quartz")
    t.set(4, 1, 6, "minecraft:lectern", {"facing": "east", "has_book": "false", "powered": "false"})
    t.set(8, 1, 6, "minecraft:brewing_stand", {"has_bottle_0": "false", "has_bottle_1": "false", "has_bottle_2": "false"})
    # plants by the door, lanterns overhead
    for x in (2, W - 3):
        t.set(x, 1, z0 + 1, "minecraft:potted_fern")
    for x in (3, 9):
        t.set(x, 4, 6, "minecraft:lantern", {"hanging": "true", "waterlogged": "false"})
    t.set(6, 4, 4, "minecraft:lantern", {"hanging": "true", "waterlogged": "false"})
    # the village street joins here
    t.set(6, 0, 0, "minecraft:jigsaw", {"orientation": "north_up"},
          {"id": "minecraft:jigsaw", "name": "minecraft:building_entrance", "target": "minecraft:empty",
           "pool": "minecraft:empty", "final_state": "minecraft:dirt_path", "joint": "rollable",
           "placement_priority": 0, "selection_priority": 0})
    return t


# --- data ----------------------------------------------------------------------------------------------------------------
def build():
    for colour, pal in BRICKS.items():
        save(bricks(pal), A / "textures" / "block" / f"gen1_bricks_{colour}.png")
        name = f"gen1_bricks_{colour}"
        write_json(A / "blockstates" / f"{name}.json", {"variants": {"": {"model": f"{MOD}:block/{name}"}}})
        write_json(A / "models" / "block" / f"{name}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{MOD}:block/{name}"}})
        write_json(A / "models" / "item" / f"{name}.json", {"parent": f"{MOD}:block/{name}"})
        write_json(D / "loot_table" / "blocks" / f"{name}.json", {"type": "minecraft:block", "pools": [
            {"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{MOD}:{name}"}], "conditions": [{"condition": "minecraft:survives_explosion"}]}]})
        dye = {"black": "black_dye", "white": "white_dye", "grey": "gray_dye"}[colour]
        write_json(D / "recipe" / f"{name}.json", {"type": "minecraft:crafting_shaped", "category": "building",
                                                   "pattern": ["BBB", "BDB", "BBB"],
                                                   "key": {"B": {"item": "minecraft:stone_bricks"}, "D": {"item": f"minecraft:{dye}"}},
                                                   "result": {"id": f"{MOD}:{name}", "count": 8}})
    # the PC
    save(pc_side(), A / "textures" / "block" / "glitchy_pc_side.png")
    save(pc_front(None), A / "textures" / "block" / "glitchy_pc_front.png")
    frames = [pc_front(f) for f in range(4)]
    strip = Image.new("RGBA", (16, 64))
    for i, f in enumerate(frames):
        strip.paste(f, (0, i * 16))
    save(strip, A / "textures" / "block" / "glitchy_pc_front_on.png")
    (A / "textures" / "block" / "glitchy_pc_front_on.png.mcmeta").write_text(json.dumps({"animation": {"frametime": 4}}) + "\n")
    for name, front in (("glitchy_pc", "glitchy_pc_front"), ("glitchy_pc_on", "glitchy_pc_front_on")):
        write_json(A / "models" / "block" / f"{name}.json", {"parent": "minecraft:block/orientable", "textures": {
            "front": f"{MOD}:block/{front}", "side": f"{MOD}:block/glitchy_pc_side", "top": f"{MOD}:block/glitchy_pc_side"}})
    rot = {"north": 0, "east": 90, "south": 180, "west": 270}
    write_json(A / "blockstates" / "glitchy_pc.json", {"variants": {
        f"facing={f},lit={lit}": dict({"model": f"{MOD}:block/glitchy_pc{'_on' if lit == 'true' else ''}"}, **({"y": r} if r else {}))
        for f, r in rot.items() for lit in ("false", "true")}})
    write_json(A / "models" / "item" / "glitchy_pc.json", {"parent": f"{MOD}:block/glitchy_pc"})
    write_json(D / "loot_table" / "blocks" / "glitchy_pc.json", {"type": "minecraft:block", "pools": [
        {"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{MOD}:glitchy_pc"}], "conditions": [{"condition": "minecraft:survives_explosion"}]}]})
    write_json(D / "recipe" / "glitchy_pc.json", {"type": "minecraft:crafting_shaped", "category": "misc",
                                                 "pattern": ["GGG", "GPG", "IRI"],
                                                 "key": {"G": {"item": f"{MOD}:gen1_bricks_grey"}, "P": {"item": "minecraft:glass_pane"},
                                                         "I": {"item": "minecraft:iron_ingot"}, "R": {"item": "minecraft:redstone"}},
                                                 "result": {"id": f"{MOD}:glitchy_pc", "count": 1}})
    # items
    save(orb(), A / "textures" / "item" / "kantonian_orb.png")
    save(essence(), A / "textures" / "item" / "essence_of_olde.png")
    for item in ("kantonian_orb", "essence_of_olde"):
        write_json(A / "models" / "item" / f"{item}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{item}"}})
    write_json(D / "recipe" / "kantonian_orb.json", {"type": "minecraft:crafting_shapeless", "category": "misc",
                                                    "ingredients": [{"item": "cobbleeffort_distortion:distortion_crystal"},
                                                                    {"item": f"{MOD}:essence_of_olde"}],
                                                    "result": {"id": f"{MOD}:kantonian_orb", "count": 1}})
    save(icon(), A / "icon.png")
    # tags: a pickaxe mines them all
    write_json(RES / "data" / "minecraft" / "tags" / "block" / "mineable" / "pickaxe.json",
               {"replace": False, "values": [f"{MOD}:gen1_bricks_{c}" for c in BRICKS] + [f"{MOD}:glitchy_pc"]})
    # the lab
    p = D / "structure" / "village" / "gen1_lab.nbt"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(Nbt.file(lab().data()))
    # the Kanto dimension: large-biome terrain (so it isn't the overworld again), overworld sky
    write_json(D / "dimension_type" / "kanto.json", {
        "ultrawarm": False, "natural": True, "coordinate_scale": 1.0, "has_skylight": True, "has_ceiling": False,
        "ambient_light": 0.0, "monster_spawn_light_level": {"type": "minecraft:uniform", "min_inclusive": 0, "max_inclusive": 7},
        "monster_spawn_block_light_limit": 0, "piglin_safe": False, "bed_works": True, "respawn_anchor_works": False,
        "has_raids": True, "logical_height": 384, "min_y": -64, "height": 384,
        "infiniburn": "#minecraft:infiniburn_overworld", "effects": "minecraft:overworld"})
    write_json(D / "dimension" / "kanto.json", {"type": f"{MOD}:kanto", "generator": {
        "type": "minecraft:noise", "settings": "minecraft:large_biomes",
        "biome_source": {"type": "minecraft:multi_noise", "preset": "minecraft:overworld"}}})
    lang = A / "lang" / "en_us.json"
    write_json(lang, dict(sorted(LANG.items())))


if __name__ == "__main__":
    build()
