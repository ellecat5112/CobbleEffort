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


# --- stage 2: gyms, the Elite Four hall, their trainers ------------------------------------------------------------------
# original type-themed leaders (names, looks and teams of our own; Gen 1 Pokémon only), in gym order
LEADERS = [
    # id, title, name, type, accents (wall stripe, floor accent, pillar, light), shirt hue, hair colour, team
    ("shale", "Rock Gym Leader", "Shale", "rock",
     ("minecraft:polished_andesite", "minecraft:cobblestone", "minecraft:stone", "minecraft:lantern"), 30, (70, 50, 36),
     ["geodude level=12", "rhyhorn level=13", "onix level=15"]),
    ("brine", "Water Gym Leader", "Brine", "water",
     ("minecraft:prismarine_bricks", "minecraft:water", "minecraft:dark_prismarine", "minecraft:sea_lantern"), 205, (220, 120, 60),
     ["staryu level=18", "horsea level=18", "starmie level=21"]),
    ("volta", "Electric Gym Leader", "Volta", "electric",
     ("minecraft:waxed_copper_block", "minecraft:waxed_cut_copper", "minecraft:waxed_exposed_copper", "minecraft:redstone_lamp"), 52, (230, 210, 120),
     ["voltorb level=21", "magnemite level=21", "pikachu level=22", "raichu level=24"]),
    ("fern", "Grass Gym Leader", "Fern", "grass",
     ("minecraft:moss_block", "minecraft:moss_block", "minecraft:oak_leaves", "minecraft:shroomlight"), 110, (60, 40, 30),
     ["bellsprout level=27", "oddish level=27", "tangela level=29", "vileplume level=30"]),
    ("nightshade", "Poison Gym Leader", "Nightshade", "poison",
     ("minecraft:purple_terracotta", "minecraft:purple_stained_glass", "minecraft:purpur_pillar", "minecraft:pearlescent_froglight"), 285, (30, 20, 40),
     ["koffing level=34", "grimer level=34", "venomoth level=36", "weezing level=38"]),
    ("aura", "Psychic Gym Leader", "Aura", "psychic",
     ("minecraft:amethyst_block", "minecraft:pink_stained_glass", "minecraft:purpur_block", "minecraft:end_rod"), 330, (240, 230, 240),
     ["kadabra level=38", "mrmime level=38", "slowbro level=40", "alakazam level=43"]),
    ("cinder", "Fire Gym Leader", "Cinder", "fire",
     ("minecraft:nether_bricks", "minecraft:red_terracotta", "minecraft:red_nether_bricks", "minecraft:shroomlight"), 12, (250, 250, 250),
     ["growlithe level=42", "ponyta level=42", "magmar level=44", "rapidash level=45", "arcanine level=47"]),
    ("terra", "Ground Gym Leader", "Terra", "ground",
     ("minecraft:terracotta", "minecraft:coarse_dirt", "minecraft:smooth_sandstone", "minecraft:lantern"), 38, (20, 20, 24),
     ["dugtrio level=47", "marowak level=47", "sandslash level=48", "nidoqueen level=50", "rhydon level=52"]),
]
ELITE = [
    ("frost", "Elite Four", "Frost", "ice", ("minecraft:packed_ice", "minecraft:snow_block", "minecraft:blue_ice", "minecraft:sea_lantern"), 190, (240, 245, 255),
     ["cloyster level=54", "dewgong level=54", "jynx level=56", "lapras level=58"]),
    ("brawn", "Elite Four", "Brawn", "fighting", ("minecraft:stripped_spruce_log", "minecraft:red_wool", "minecraft:spruce_planks", "minecraft:lantern"), 0, (24, 20, 18),
     ["hitmonlee level=55", "hitmonchan level=55", "primeape level=56", "poliwrath level=57", "machamp level=59"]),
    ("wisp", "Elite Four", "Wisp", "ghost", ("minecraft:deepslate_tiles", "minecraft:polished_blackstone", "minecraft:chiseled_deepslate", "minecraft:soul_lantern"), 270, (200, 200, 210),
     ["golbat level=56", "haunter level=56", "arbok level=57", "gengar level=58", "gengar level=60"]),
    ("wyrm", "Elite Four", "Wyrm", "dragon", ("minecraft:purpur_block", "minecraft:end_stone_bricks", "minecraft:obsidian", "minecraft:end_rod"), 250, (180, 40, 40),
     ["dragonair level=58", "dragonair level=58", "aerodactyl level=59", "gyarados level=59", "dragonite level=62"]),
]


def _block(name):
    """(name, props) for an accent block, with the properties it needs."""
    props = {}
    if name == "minecraft:redstone_lamp":
        props = {"lit": "true"}
    elif name in ("minecraft:lantern", "minecraft:soul_lantern"):
        props = {"hanging": "false", "waterlogged": "false"}
    elif name == "minecraft:oak_leaves":
        props = {"distance": "1", "persistent": "true", "waterlogged": "false"}
    elif name in ("minecraft:stripped_spruce_log", "minecraft:purpur_pillar", "minecraft:quartz_pillar", "minecraft:pearlescent_froglight",
                  "minecraft:ochre_froglight", "minecraft:verdant_froglight", "minecraft:stripped_cherry_log", "minecraft:stripped_birch_log"):
        props = {"axis": "y"}
    elif name == "minecraft:end_rod":
        props = {"facing": "up"}
    return name, props


def gym(leader):
    """A gym (original layout): Gen 1 Brick walls with a stripe of the type's block, an arena floor with a white
    centre line and accent panels, accent pillars down both sides with lights, flanking pillars at the door, and the
    leader's raised platform at the back. Returns (template, leader position)."""
    _, _, _, _, (stripe, floor, pillar, light), _, _, _ = leader
    W, H, Dp = 15, 9, 21
    t = Template((W, H, Dp))
    B, Wt, G = f"{MOD}:gen1_bricks_black", f"{MOD}:gen1_bricks_white", f"{MOD}:gen1_bricks_grey"
    for x in range(W):
        for z in range(Dp):
            edge = x in (0, W - 1) or z in (0, Dp - 1)
            t.set(x, 0, z, B if edge else (Wt if x == W // 2 else G))
            if not edge and x in (3, 4, W - 5, W - 4) and 4 <= z <= Dp - 6:
                t.set(x, 0, z, *_block(floor))                       # the accent panels
    for y in range(1, H - 1):
        for x in range(W):
            for z in range(Dp):
                wall = x in (0, W - 1) or z in (0, Dp - 1)
                if wall:
                    corner = x in (0, W - 1) and z in (0, Dp - 1)
                    if corner or y == H - 2:
                        t.set(x, y, z, B)
                    elif y == 3:
                        t.set(x, y, z, *_block(stripe))            # the type's stripe round the walls
                    else:
                        t.set(x, y, z, G)
                else:
                    t.set(x, y, z, "minecraft:air")
    for x in range(W):
        for z in range(Dp):
            t.set(x, H - 1, z, B if (x in (0, W - 1) or z in (0, Dp - 1)) else Wt)
    # windows
    for z in range(4, Dp - 4, 4):
        for y in (4, 5):
            t.set(0, y, z, "minecraft:glass")
            t.set(W - 1, y, z, "minecraft:glass")
    # the door (front, z = 0) with flanking pillars
    door = {"facing": "south", "hinge": "left", "open": "false", "powered": "false"}
    cx = W // 2
    t.set(cx, 1, 0, "minecraft:iron_door", dict(door, half="lower"))
    t.set(cx, 2, 0, "minecraft:iron_door", dict(door, half="upper"))
    for x in (cx - 2, cx + 2):
        for y in (1, 2, 3):
            t.set(x, y, 1, *_block(pillar))
        t.set(x, 4, 1, *_block(light))
    # pillars with lights down both sides
    for z in range(5, Dp - 4, 4):
        for x in (2, W - 3):
            for y in (1, 2, 3, 4):
                t.set(x, y, z, *_block(pillar))
            t.set(x, 5, z, *_block(light))
    # the leader's platform at the back
    for x in range(cx - 3, cx + 4):
        for z in range(Dp - 5, Dp - 1):
            t.set(x, 1, z, *_block(stripe) if (x in (cx - 3, cx + 3) or z == Dp - 5) else (Wt, {}))
    for x in (cx - 2, cx + 2):
        t.set(x, 2, Dp - 2, *_block(light))
    return t, (cx, 2, Dp - 3)


def elite_hall(members=None):
    """The Elite Four hall (original): a long Gen 1 Brick hall with four rooms, two each side of a central aisle, each
    room themed by its member's type; the members stand at the far end of their rooms. Returns (template, positions)."""
    W, H, Dp = 31, 10, 25
    t = Template((W, H, Dp))
    B, Wt, G = f"{MOD}:gen1_bricks_black", f"{MOD}:gen1_bricks_white", f"{MOD}:gen1_bricks_grey"
    for x in range(W):
        for z in range(Dp):
            t.set(x, 0, z, B if x in (0, W - 1) or z in (0, Dp - 1) else (Wt if 13 <= x <= 17 else G))
            t.set(x, H - 1, z, B if x in (0, W - 1) or z in (0, Dp - 1) else Wt)
    for y in range(1, H - 1):
        for x in range(W):
            for z in range(Dp):
                wall = x in (0, W - 1) or z in (0, Dp - 1)
                inner = x in (12, 18) or (z == 12 and (x < 12 or x > 18))
                if wall or inner:
                    t.set(x, y, z, B if (y == H - 2 or (wall and x in (0, W - 1) and z in (0, Dp - 1))) else G)
                else:
                    t.set(x, y, z, "minecraft:air")
    door = {"facing": "south", "hinge": "left", "open": "false", "powered": "false"}
    for dx in (14, 16):
        t.set(dx, 1, 0, "minecraft:iron_door", dict(door, half="lower", hinge="left" if dx == 14 else "right"))
        t.set(dx, 2, 0, "minecraft:iron_door", dict(door, half="upper", hinge="left" if dx == 14 else "right"))
    t.set(15, 1, 0, G)
    t.set(15, 2, 0, G)
    rooms = [(1, 11, 1, 11), (19, 29, 1, 11), (1, 11, 13, 23), (19, 29, 13, 23)]
    positions = []
    for (x0, x1, z0, z1), member in zip(rooms, members or ELITE):
        _, _, _, _, (stripe, floor, pillar, light), _, _, _ = member
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                t.set(x, 0, z, *_block(floor) if (x + z) % 3 else _block(stripe))
        # the room's door onto the aisle
        side = x1 + 1 if x0 < 12 else x0 - 1
        cz = (z0 + z1) // 2
        for y in (1, 2):
            t.set(side, y, cz, "minecraft:air")
        for z in (z0 + 1, z1 - 1):
            for x in (x0 + 1, x1 - 1):
                for y in (1, 2, 3):
                    t.set(x, y, z, *_block(pillar))
                t.set(x, 4, z, *_block(light))
        far = x0 + 1 if x0 < 12 else x1 - 1
        positions.append((far, 1, cz))
    for z in range(3, Dp - 2, 4):
        t.set(15, 6, z, "minecraft:lantern", {"hanging": "true", "waterlogged": "false"})
    return t, positions


def trainer_skin(hue, hair):
    """Cobblemon's trainer skin recoloured: the shirt in the type's hue, darker trousers, and the leader's hair."""
    import colorsys
    import zipfile
    jar = next(Path("/tmp/claude-0").glob("**/dist_deps/Cobblemon-fabric-1.8.4*.jar"))
    src = Image.open(io.BytesIO(zipfile.ZipFile(jar).read("assets/cobblemon/textures/npcs/standard/trainer.png"))).convert("RGBA")
    out = src.copy()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = src.getpixel((x, y))
            if a == 0:
                continue
            hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            deg = hh * 360
            if ss > 0.35 and 160 <= deg <= 200:                   # the shirt
                nr, ng, nb = colorsys.hsv_to_rgb(hue / 360, min(1, ss * 0.9), vv)
            elif ss > 0.3 and 215 <= deg <= 275:                  # the trousers
                nr, ng, nb = colorsys.hsv_to_rgb(hue / 360, 0.45, vv * 0.55)
            elif vv < 0.33 and 10 <= deg <= 40 and y < 32:         # the hair
                k = vv / 0.33
                nr, ng, nb = [(c / 255) * (0.6 + 0.6 * k) for c in hair]
            else:
                continue
            out.putpixel((x, y), tuple(max(0, min(255, int(c * 255))) for c in (nr, ng, nb)) + (a,))
    return out


def trainers():
    """Every leader and Elite Four member: an NPC class (Cobblemon's npc data: name, team, battle), a dialogue, a
    variation (Cobblemon's trainer model with the recoloured skin) and the skin."""
    for lid, title, name, typ, _, hue, hair, team in LEADERS + ELITE:
        nid = f"{MOD}:{lid}"
        full = f"{title} {name}"
        write_json(D / "npcs" / f"{lid}.json", {
            "names": [full], "hitbox": "player", "canDespawn": False, "autoHealParty": True,
            "battleConfiguration": {"canChallenge": True},
            "interaction": {"type": "dialogue", "dialogue": nid},
            "party": {"type": "simple", "pokemon": team}, "skill": 3 if title != "Elite Four" else 5, "presets": []})
        intro = (f"I'm {name}, keeper of this gym's {typ.title()}-type trial. Show me your team!" if title != "Elite Four"
                 else f"You've reached the Elite Four. I am {name}, master of {typ.title()} types. Ready?")
        write_json(D / "dialogues" / f"{lid}.json", {
            "pages": [{"id": "intro", "speaker": "npc", "lines": [intro],
                       "input": {"type": "option", "vertical": False, "options": [
                           {"value": "battle", "text": "Battle!", "action": ["q.dialogue.close();", "q.npc.start_battle(q.player, 'singles');"]},
                           {"value": "later", "text": "Not yet", "action": ["q.dialogue.close();"]}]}}],
            "speakers": {"npc": {"face": "q.npc.face(false);", "name": {"type": "expression", "expression": "q.npc.name"}}}})
        write_json(A / "bedrock" / "npcs" / "variations" / f"{lid}.json", {"name": nid, "order": 0, "variations": [
            {"aspects": [], "layers": [], "model": "cobblemon:trainer.geo", "poser": "cobblemon:standard",
             "texture": f"{MOD}:textures/npcs/{lid}.png"}]})
        save(trainer_skin(hue, hair), A / "textures" / "npcs" / f"{lid}.png")


BADGE_COLOURS = {   # type -> (dark, mid, light)
    "rock": ((70, 60, 50), (140, 124, 104), (210, 196, 170)), "water": ((20, 50, 120), (50, 120, 220), (170, 220, 255)),
    "electric": ((120, 90, 0), (240, 200, 30), (255, 250, 170)), "grass": ((20, 80, 30), (70, 170, 60), (180, 240, 150)),
    "poison": ((60, 20, 80), (150, 70, 190), (230, 170, 250)), "psychic": ((120, 30, 80), (240, 100, 170), (255, 200, 230)),
    "fire": ((130, 30, 10), (240, 100, 30), (255, 220, 120)), "ground": ((90, 60, 30), (190, 140, 80), (240, 210, 150)),
}
BADGE_SHAPES = {   # an original emblem per type, as a function (x, y) -> inside? on a 16x16 grid centred at 7.5
    "rock": lambda x, y: abs(x - 7.5) + abs(y - 7.5) <= 7 and abs(x - 7.5) <= 5.5 and abs(y - 7.5) <= 5.5,     # an octagon
    "water": lambda x, y: (x - 7.5) ** 2 + (y - 9.5) ** 2 <= 22 or (abs(x - 7.5) <= (y - 1) * 0.55 and 1 <= y <= 9),  # a drop
    "electric": lambda x, y: (4 <= x <= 10 and 1 <= y <= 8 and x - 4 >= (y - 1) * 0.3 and x <= 10 - (y - 1) * 0.4) or
                             (5 <= x <= 11 and 7 <= y <= 14 and x >= 5 + (y - 7) * 0.5 and x <= 11 - (y - 7) * 0.2),  # a bolt
    "grass": lambda x, y: ((x - 7.5) * 0.8 + (y - 7.5) * 0.6) ** 2 / 36 + ((x - 7.5) * 0.6 - (y - 7.5) * 0.8) ** 2 / 9 <= 1,  # a leaf
    "poison": lambda x, y: (x - 6.5) ** 2 + (y - 8.5) ** 2 <= 22 or (x - 11) ** 2 + (y - 4) ** 2 <= 6,         # two bubbles
    "psychic": lambda x, y: ((x - 7.5) / 7) ** 2 + ((y - 7.5) / 4.5) ** 2 <= 1,                               # an eye
    "fire": lambda x, y: (x - 7.5) ** 2 + (y - 10) ** 2 <= 20 or (abs(x - 7.5 - (y - 8) * 0.25) <= (y - 1) * 0.5 and 1 <= y <= 10),  # a flame
    "ground": lambda x, y: abs(x - 7.5) <= 6.5 - abs(y - 7.5) * 0.9 and 2 <= y <= 13,                         # a diamond
}


def badge(typ):
    """A gym badge (original emblems): a type-coloured shape with a rim, a lit upper left and a highlight glint."""
    dark, mid, light = BADGE_COLOURS[typ]
    inside = BADGE_SHAPES[typ]
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(16):
        for x in range(16):
            if not inside(x, y):
                continue
            rim = not all(inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if rim:
                c = dark
            else:
                lit = (x - 7.5) + (y - 7.5) < -2
                c = light if lit else mid
            im.putpixel((x, y), c + (255,))
    # the eye's pupil, the glint
    if typ == "psychic":
        for y in range(6, 10):
            for x in range(6, 10):
                if (x - 7.5) ** 2 + (y - 7.5) ** 2 <= 3.5:
                    im.putpixel((x, y), dark + (255,))
    return im


def ribbon():
    """The Champion Ribbon: a gold rosette with red tails."""
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    gold = [(120, 80, 10), (220, 170, 40), (255, 236, 140)]
    red = [(110, 10, 20), (200, 30, 40)]
    for y in range(8, 16):
        for x in (4, 5, 6, 9, 10, 11):
            left = x < 8
            off = (y - 8) // 3
            xx = x - off if left else x + off
            if 0 <= xx < 16 and not (y == 15 and x in (5, 10)):
                im.putpixel((xx, y), red[1 if x in (5, 10) else 0] + (255,))
    for y in range(16):
        for x in range(16):
            d = ((x - 7.5) ** 2 + (y - 6) ** 2) ** 0.5
            ang = math.atan2(y - 6, x - 7.5)
            r = 5.6 + 0.8 * math.cos(ang * 8)
            if d <= r:
                c = gold[0] if d > r - 1 else gold[2] if (x - 7.5) + (y - 6) < -1.5 else gold[1]
                if d < 2:
                    c = red[1]
                im.putpixel((x, y), c + (255,))
    return im


def badges():
    for typ in BADGE_SHAPES:
        save(badge(typ), A / "textures" / "item" / f"{typ}_badge.png")
        write_json(A / "models" / "item" / f"{typ}_badge.json", {"parent": "minecraft:item/generated",
                                                               "textures": {"layer0": f"{MOD}:item/{typ}_badge"}})
        LANG[f"item.{MOD}.{typ}_badge"] = f"{typ.title()} Badge"
    save(ribbon(), A / "textures" / "item" / "champion_ribbon.png")
    write_json(A / "models" / "item" / "champion_ribbon.json", {"parent": "minecraft:item/generated",
                                                              "textures": {"layer0": f"{MOD}:item/champion_ribbon"}})
    LANG[f"item.{MOD}.champion_ribbon"] = "Kanto Champion Ribbon"


def sites():
    """The nine buildings in Kanto: their templates and where their trainers stand (KantoGyms reads sites.json and
    builds them once, around Kanto's centre, the first time someone arrives)."""
    out = []
    for i, leader in enumerate(LEADERS):
        t, pos = gym(leader)
        p = D / "structure" / "gym" / f"{leader[3]}.nbt"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(Nbt.file(t.data()))
        ang = math.radians(i * 45)
        out.append({"id": leader[3], "label": f"{leader[3].title()} Gym", "template": f"{MOD}:gym/{leader[3]}",
                    "size": list(t.size), "x": int(round(math.sin(ang) * 320)), "z": int(round(-math.cos(ang) * 320)),
                    "trainers": [{"npc": f"{MOD}:{leader[0]}", "pos": list(pos), "yaw": 180, "badge": f"{leader[3]}_badge"}]})
    t, positions = elite_hall()
    p = D / "structure" / "gym" / "elite_four.nbt"
    p.write_bytes(Nbt.file(t.data()))
    out.append({"id": "elite_four", "label": "Elite Four", "template": f"{MOD}:gym/elite_four", "size": list(t.size), "x": 0, "z": 0,
                "trainers": [{"npc": f"{MOD}:{m[0]}", "pos": list(pos), "yaw": -90 if pos[0] < 12 else 90, "elite": True}
                             for m, pos in zip(ELITE, positions)]})
    write_json(D / "kanto" / "sites.json", out)
    return out


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
    trainers()
    sites()
    badges()
    LANG.update({
        f"{MOD}.gyms.list": "Kanto's gyms and the Elite Four (x, z): %s",
        f"{MOD}.gyms.building": "Kanto's gyms are being built...",
        f"{MOD}.badge.earned": "You earned the %s! (%s of 8)",
        f"{MOD}.elite.locked": "The Elite Four only face trainers with all 8 Kanto badges (you have %s).",
        f"{MOD}.elite.beaten": "%s of the Elite Four defeated (%s of 4).",
        f"{MOD}.champion": "You defeated the whole Elite Four: you're Kanto's Champion!",
    })
    import make_kantonian                                   # stage 3: ore, metal, armor
    make_kantonian.build()
    LANG.update(make_kantonian.LANG)
    import make_regions                                     # 0.3.0: Johto to Paldea, landmarks and portals
    make_regions.build()
    LANG.update(make_regions.LANG)
    import make_leagues                                     # 0.4.0: every region's gyms and Elite Four
    make_leagues.build()
    LANG.update(make_leagues.LANG)
    lang = A / "lang" / "en_us.json"
    write_json(lang, dict(sorted(LANG.items())))


if __name__ == "__main__":
    build()
