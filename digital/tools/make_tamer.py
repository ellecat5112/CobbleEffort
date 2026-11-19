"""Tamer basics for CobbleEffort: Digital (0.13.0): attribute fragments and chips, Digi-Meat / Sirloin / Super Carrots
and their crops, the training gym blocks, the Digiball tiers (recoloured from Cobblemon's Poke Ball, CC BY-NC) and
Chrome Digizoid (ore, raw, ingot, block, world generation). Textures are drawn here (original pixel art).
Run by make_assets.py with the Cobblemon jar (the balls), or alone for everything else.
"""
from __future__ import annotations

import colorsys
import json
import math
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "common" / "src" / "main" / "resources"
NS = "cobbleeffort_digital"
A = ROOT / "assets" / NS
D = ROOT / "data" / NS

ATTR = {  # attribute: (dark, mid, light, glow)
    "vaccine": ((20, 70, 150), (40, 130, 230), (150, 215, 255), (230, 250, 255)),
    "data": ((16, 90, 40), (40, 170, 70), (150, 240, 150), (230, 255, 230)),
    "virus": ((80, 16, 90), (160, 40, 170), (240, 120, 230), (255, 220, 250)),
}
TRAINING = ["punching_bag", "treadmill", "waterfall", "meditation_mat", "target_dummy"]
BALLS = {"wireframe_ball": "Wireframe Ball", "data_net_ball": "Data-Net Ball", "chrome_digizoid_ball": "Chrome Digizoid Ball"}
CHROME_ORES = ["chrome_digizoid_ore", "deepslate_chrome_digizoid_ore"]


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


def new(w=16, hh=16):
    return Image.new("RGBA", (w, hh), (0, 0, 0, 0))


def save(im, rel):
    p = A / "textures" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    im.save(p, optimize=True)


def outline(im, col=(24, 20, 28)):
    """A dark outline round every opaque area (item sprites)."""
    w, hh = im.size
    src = im.copy()
    px, sp = im.load(), src.load()
    for y in range(hh):
        for x in range(w):
            if sp[x, y][3]:
                continue
            if any(0 <= x + dx < w and 0 <= y + dy < hh and sp[x + dx, y + dy][3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = C(col)
    return im


# --- attribute data ------------------------------------------------------------------------------------------------

def fragment(attr):
    """A jagged data shard with binary bits glowing inside."""
    dk, md, lt, gl = ATTR[attr]
    im = new()
    px = im.load()
    for y in range(2, 15):
        for x in range(3, 14):
            u, v = x - 8.5, y - 8.5
            r = 5.4 - 0.9 * abs(math.sin(math.atan2(v, u) * 3 + 0.5))      # three-pointed, jagged
            d = math.hypot(u * 1.05, v * 0.9)
            if d > r:
                continue
            c = lt if (u + v) < -2 else md if (u - v * 0.3) < 2 else dk
            if d > r - 1.0:
                c = dk
            px[x, y] = C(c)
    for (x, y) in ((6, 6), (8, 5), (7, 8), (9, 8), (10, 10), (6, 10), (8, 11)):
        if px[x, y][3]:
            px[x, y] = C(gl)
    return outline(im)


def chip(attr):
    """A square circuit chip: pins on all sides, the attribute's colour in the core, a gold contact."""
    dk, md, lt, gl = ATTR[attr]
    im = new()
    px = im.load()
    for y in range(3, 13):
        for x in range(3, 13):
            px[x, y] = C((44, 46, 56) if (x in (3, 12) or y in (3, 12)) else (70, 74, 86))
    for i in range(4, 12, 2):
        for (x, y) in ((i, 2), (i, 13), (2, i), (13, i)):
            px[x, y] = C((210, 200, 150))
    for y in range(5, 11):
        for x in range(5, 11):
            px[x, y] = C(lt if (x + y) < 12 else md if (x + y) < 16 else dk)
    px[6, 6] = C(gl)
    px[7, 6] = C(gl)
    px[10, 10] = C((240, 200, 60))
    return outline(im)


# --- food ---------------------------------------------------------------------------------------------------------------

MEAT = [(110, 44, 22), (168, 72, 34), (212, 110, 58), (240, 160, 110)]
BONE = [(170, 160, 140), (225, 218, 200), (250, 246, 236)]


def digimeat():
    """The classic manga meat: a round brown chunk on a bone, sticking out both ends."""
    im = new()
    px = im.load()
    for t in range(-7, 8):                                   # the bone, along the diagonal
        x, y = 8 + t * 0.62, 8 - t * 0.62
        for w in (-0.5, 0.5):
            xi, yi = int(round(x + w)), int(round(y + w))
            if 0 <= xi < 16 and 0 <= yi < 16:
                px[xi, yi] = C(BONE[1])
    for (x, y) in ((2, 13), (1, 13), (2, 14), (3, 14), (13, 2), (14, 2), (13, 1), (12, 1)):   # knuckles
        px[x, y] = C(BONE[2])
    for y in range(16):
        for x in range(16):
            u, v = x - 8, y - 8
            a, b = (u - v) / 1.414, (u + v) / 1.414
            if (a / 5.6) ** 2 + (b / 4.4) ** 2 <= 1:
                k = 3 if (a < -2 and b < -1) else 2 if b < 1 else 1
                if (a / 5.6) ** 2 + (b / 4.4) ** 2 > 0.78:
                    k = 0
                px[x, y] = C(MEAT[k])
    return outline(im, (50, 20, 10))


def sirloin():
    """A marbled steak with a fat rim."""
    im = new()
    px = im.load()
    for y in range(16):
        for x in range(16):
            u, v = (x - 7.5) / 6.8, (y - 8.2) / 5.2
            d = u * u + v * v + 0.25 * u * v
            if d > 1:
                continue
            if d > 0.78:
                c = (246, 232, 214)                               # fat
            else:
                marbled = h(x, y // 2, 7) > 0.8 or (x + 2 * y) % 7 == 0
                c = (250, 214, 210) if marbled else (196, 52, 58) if u + v < 0.3 else (160, 36, 44)
            px[x, y] = C(c)
    return outline(im, (70, 20, 24))


def super_carrot():
    """A carrot glowing gold, with a sparkle."""
    im = new()
    px = im.load()
    for y in range(4, 16):
        w = max(0.6, 3.2 * (1 - (y - 4) / 12))
        for x in range(16):
            dx = x - (9 - (y - 4) * 0.35)
            if abs(dx) <= w:
                c = (255, 214, 80) if dx < -w * 0.3 else (250, 150, 30) if dx < w * 0.4 else (200, 96, 20)
                if (y + int(x)) % 4 == 0 and abs(dx) < w - 0.5:
                    c = (220, 120, 24)
                px[x, y] = C(c)
    for (x, y) in ((9, 3), (10, 2), (11, 1), (8, 2), (7, 1), (10, 3), (12, 2)):
        px[x, y] = C((70, 190, 60) if (x + y) % 2 else (40, 140, 40))
    for (x, y) in ((3, 4), (3, 6), (2, 5), (4, 5), (13, 9)):
        px[x, y] = C((255, 250, 200))
    return outline(im, (80, 40, 10))


def crop_stage(kind, stage):
    """Crop textures (4 stages, like carrots): green sprouts; the last stage shows the harvest."""
    im = new()
    px = im.load()
    for x0 in (2, 6, 10, 13):
        hgt = 3 + stage * 3 + int(h(x0, stage) * 2)
        for y in range(16 - hgt, 16):
            px[x0, y] = C((60, 150, 50) if y % 3 else (40, 120, 40))
            if y % 4 == 0 and x0 + 1 < 16:
                px[x0 + 1, y] = C((90, 180, 70))
    if stage == 3:
        if kind == "digimeat":
            for cx, cy in ((4, 7), (11, 6)):
                for y in range(16):
                    for x in range(16):
                        if ((x - cx) / 2.6) ** 2 + ((y - cy) / 2.1) ** 2 <= 1:
                            px[x, y] = C(MEAT[2] if x < cx else MEAT[1])
                px[cx, cy - 3] = C(BONE[2])
                px[cx, cy - 4] = C(BONE[1])
                px[cx, cy + 3] = C(BONE[1])
        else:
            for cx in (3, 8, 12):
                for y in range(11, 16):
                    for x in range(cx - 1, cx + 2):
                        px[x, y] = C((250, 160, 40) if x == cx - 1 else (230, 120, 24))
                px[cx, 10] = C((255, 230, 120))
    return im


# --- Digivice and Digi-Modify cards ---------------------------------------------------------------------------------

def digivice():
    """A handheld V-pet style Digivice: rounded white-grey shell, a green-grey screen with a tiny Digimon, three buttons,
    a cyan trim and a strap ring."""
    im = new()
    px = im.load()
    for y in range(2, 15):
        for x in range(3, 14):
            u, v = (x - 8) / 5.6, (y - 8.4) / 6.6
            if u * u + v * v > 1.0 or (abs(u) > 0.92 and abs(v) > 0.75):
                continue
            c = (226, 230, 236) if x < 8 else (196, 200, 210)
            if u * u + v * v > 0.8:
                c = (40, 200, 240)                                # the trim
            px[x, y] = C(c)
    for y in range(5, 10):
        for x in range(5, 12):
            px[x, y] = C((150, 176, 120) if (x, y) not in ((7, 7), (8, 6), (9, 7), (8, 8), (7, 8), (9, 8)) else (40, 60, 30))
    for x in range(5, 12):
        px[x, 4] = C((90, 96, 110))
        px[x, 10] = C((90, 96, 110))
    for (x, y) in ((6, 12), (8, 12), (10, 12)):
        px[x, y] = C((240, 80, 60) if x == 8 else (60, 70, 90))
    px[8, 1] = C((180, 184, 196))
    px[7, 1] = C((180, 184, 196))
    return outline(im)


CARDS = {  # card: (frame colour, icon painter)
    "high_speed_plugin": (60, 150, 240),
    "metal_armor": (150, 156, 170),
    "giga_destroyer": (220, 60, 50),
    "recovery_disk": (60, 190, 90),
    "dot_virus": (110, 60, 170),
    "bug_card": (200, 160, 30),
}


def card(name):
    """A Digi-Modify card: a white card with a coloured frame, a chip stripe along one edge and the card's icon."""
    frame = CARDS[name]
    im = new()
    px = im.load()
    for y in range(1, 15):
        for x in range(3, 13):
            edge = x in (3, 12) or y in (1, 14)
            px[x, y] = C(frame if edge or y <= 2 else (244, 244, 236))
    for y in range(4, 13):
        px[4, y] = C((210, 180, 70) if y % 2 else (150, 120, 40))              # the swipe strip
    ic = {
        "high_speed_plugin": [(x, y) for y in range(5, 12) for x in range(6, 12) if (x - y + 20) % 3 == 0 and x - 6 <= 5 - abs(y - 8)],
        "metal_armor": [(x, y) for y in range(5, 12) for x in range(6, 12) if abs(x - 8.5) <= 3 - max(0, y - 9) * 1.2],
        "giga_destroyer": [(x, y) for y in range(5, 12) for x in (7, 10) if not (y == 5 and x == 10)],
        "recovery_disk": [(x, y) for y in range(6, 12) for x in range(6, 12)],
        "dot_virus": [(x, y) for y in range(5, 12) for x in range(6, 12) if (x + y) % 2 == 0],
        "bug_card": [(x, y) for y in range(5, 12) for x in range(6, 12) if abs(x - 8.5) + abs(y - 8) * 0.8 < 3 and (x, y) not in ((8, 8), (9, 8))],
    }[name]
    for (x, y) in ic:
        c = frame
        if name == "recovery_disk" and 7 <= x <= 10 and 6 <= y <= 7:
            c = (200, 200, 210)                                                   # the disk's shutter
        if name == "giga_destroyer" and y == 5:
            c = (250, 200, 60)                                                    # missile tips
        px[x, y] = C(c)
    return outline(im)


def digiegg(colour, accent, symbol):
    """A Digi-Egg (Digimental): an egg-shaped metal shell, a pair of horn fins and the crest's symbol on the front."""
    im = new()
    px = im.load()
    for y in range(2, 15):
        for x in range(3, 13):
            u, v = (x - 7.5) / 4.8, (y - 8.8) / 6.2
            v *= 1.0 + 0.2 * (v < 0)
            d = u * u + v * v
            if d > 1:
                continue
            k = 1.15 if (u < -0.2 and v < -0.2) else 0.85 if (u > 0.3) else 1.0
            px[x, y] = C(colour, k)
    for (x, y) in ((3, 4), (4, 3), (12, 4), (11, 3), (3, 5), (12, 5)):
        px[x, y] = C(accent)
    for (x, y) in symbol:
        px[x, y] = C(accent)
    return outline(im)


SUN = [(7, 7), (8, 7), (7, 8), (8, 8), (7, 9), (8, 9), (6, 8), (9, 8), (7, 6), (8, 10), (5, 6), (10, 6), (5, 10), (10, 10)]
CROSS = [(7, 6), (8, 6), (7, 7), (8, 7), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (7, 9), (8, 9), (7, 10), (8, 10)]


# --- training gym --------------------------------------------------------------------------------------------------

def tile(fn):
    im = new()
    px = im.load()
    for y in range(16):
        for x in range(16):
            px[x, y] = C(fn(x, y))
    return im


def training_textures():
    t = {}
    t["punching_bag"] = tile(lambda x, y: (176, 40, 34) if (y % 5) else (120, 24, 20) if x % 2 else (230, 210, 180))
    t["punching_bag_top"] = tile(lambda x, y: (60, 60, 66) if 5 <= x <= 10 and 5 <= y <= 10 else (150, 34, 30))
    t["training_wood"] = tile(lambda x, y: (150, 108, 64) if (x + int(h(y, 3) * 3)) % 5 else (110, 76, 44))
    t["training_metal"] = tile(lambda x, y: (150, 156, 166) if (x + y) % 9 else (190, 196, 206))
    t["treadmill_belt"] = tile(lambda x, y: (40, 40, 46) if y % 4 else (70, 70, 78))
    t["treadmill_panel"] = tile(lambda x, y: (40, 230, 120) if 4 <= x <= 11 and 5 <= y <= 9 and (x + y) % 2 else (54, 58, 70))
    t["waterfall_rock"] = tile(lambda x, y: (110, 112, 116) if h(x // 2, y // 2, 4) > 0.3 else (84, 86, 90))
    t["meditation_mat"] = tile(lambda x, y: (220, 180, 60) if x in (0, 15) or y in (0, 15) else
                               (250, 230, 140) if abs(math.hypot(x - 7.5, y - 7.5) - 4.2) < 0.7 else (120, 50, 150))
    t["target_dummy"] = tile(lambda x, y: [(230, 40, 40), (245, 240, 230)][int(math.hypot(x - 7.5, y - 7.5) / 1.6) % 2])
    t["target_straw"] = tile(lambda x, y: (220, 190, 90) if (x + 2 * y) % 5 else (180, 150, 60))
    for k, im in t.items():
        save(im, f"block/{k}.png")
    # the waterfall's falling water: an animated strip (4 frames)
    water = Image.new("RGBA", (16, 64))
    px = water.load()
    for f in range(4):
        for y in range(16):
            for x in range(16):
                streak = ((y - f * 4) % 16 + int(h(x, 9) * 16)) % 16
                c = (210, 240, 255) if streak < 2 else (70, 140, 230) if x % 3 else (90, 170, 245)
                px[x, f * 16 + y] = C(c, a=230)
    save(water, "block/waterfall_water.png")
    p = A / "textures" / "block" / "waterfall_water.png.mcmeta"
    write_json(p, {"animation": {"frametime": 3}})


def el(fr, to, tex, faces="nsewud", uv=None):
    out = {"from": fr, "to": to, "faces": {}}
    names = {"n": "north", "s": "south", "e": "east", "w": "west", "u": "up", "d": "down"}
    for f in faces:
        out["faces"][names[f]] = {"texture": f"#{tex}"}
    return out


def training_models():
    """Block models (elements, facing north) and blockstates rotated by facing."""
    models = {
        "punching_bag": {"textures": {"bag": f"{NS}:block/punching_bag", "top": f"{NS}:block/punching_bag_top",
                                      "metal": f"{NS}:block/training_metal", "particle": f"{NS}:block/punching_bag"},
                         "elements": [el([4.5, 2, 4.5], [11.5, 13, 11.5], "bag", "nsew"),
                                      el([4.5, 2, 4.5], [11.5, 13, 11.5], "top", "ud"),
                                      el([7.5, 13, 7.5], [8.5, 16, 8.5], "metal"),
                                      el([5.5, 1, 5.5], [10.5, 2, 10.5], "top")]},
        "treadmill": {"textures": {"belt": f"{NS}:block/treadmill_belt", "metal": f"{NS}:block/training_metal",
                                   "panel": f"{NS}:block/treadmill_panel", "particle": f"{NS}:block/training_metal"},
                      "elements": [el([0, 0, 1], [16, 3, 15], "metal", "nsewd"), el([1, 3, 2], [15, 3.5, 15], "belt", "u"),
                                   el([1, 3, 1], [2, 14, 2.5], "metal"), el([14, 3, 1], [15, 14, 2.5], "metal"),
                                   el([1, 12, 1], [15, 14, 3], "panel", "nsud"), el([0, 3, 1], [1, 3.5, 15], "metal")]},
        "waterfall": {"textures": {"rock": f"{NS}:block/waterfall_rock", "water": f"{NS}:block/waterfall_water",
                                   "particle": f"{NS}:block/waterfall_rock"},
                      "elements": [el([0, 0, 0], [16, 16, 16], "rock"), el([3, 0, -0.01], [13, 16, 0], "water", "n")]},
        "meditation_mat": {"textures": {"mat": f"{NS}:block/meditation_mat", "particle": f"{NS}:block/meditation_mat"},
                           "elements": [el([0, 0, 0], [16, 1, 16], "mat")]},
        "target_dummy": {"textures": {"target": f"{NS}:block/target_dummy", "straw": f"{NS}:block/target_straw",
                                      "wood": f"{NS}:block/training_wood", "particle": f"{NS}:block/target_straw"},
                         "elements": [el([7, 0, 7], [9, 8, 9], "wood"), el([2, 6, 6], [14, 16, 10], "straw", "ewud"),
                                      el([2, 6, 6], [14, 16, 10], "target", "ns")]},
    }
    for k, m in models.items():
        write_json(A / "models" / "block" / f"{k}.json", {"parent": "minecraft:block/block", **m})
        write_json(A / "models" / "item" / f"{k}.json", {"parent": f"{NS}:block/{k}"})
        write_json(A / "blockstates" / f"{k}.json", {"variants": {
            f"facing={f}": {"model": f"{NS}:block/{k}", **({"y": y} if y else {})}
            for f, y in (("north", 0), ("east", 90), ("south", 180), ("west", 270))}})
        drop_self(k)


def drop_self(block):
    write_json(D / "loot_table" / "blocks" / f"{block}.json", {"type": "minecraft:block", "pools": [{
        "rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{NS}:{block}"}],
        "conditions": [{"condition": "minecraft:survives_explosion"}]}]})


# --- Chrome Digizoid --------------------------------------------------------------------------------------------------

CHROME = [(70, 78, 96), (140, 150, 170), (200, 210, 226), (248, 252, 255)]


def rock(base, streaks):
    im = new()
    for y in range(16):
        for x in range(16):
            k = 0.88 + 0.22 * h(x // 2, y // 2, 3) + 0.08 * (h(x, y, 5) - 0.5)
            if streaks and (y + int(2 * h(x // 4, 1))) % 5 == 0:
                k *= 0.82
            if not streaks and h(x, y, 9) > 0.93:
                k *= 0.7
            im.putpixel((x, y), C(base, k))
    return im


def chrome_flecks(im):
    for cx, cy in ((4, 5), (11, 4), (7, 11), (12, 12), (3, 12)):
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if abs(dx) + abs(dy) <= 1 + (cx % 2):
                    k = 3 if (dx, dy) == (-1, -1) or (dx, dy) == (0, -1) else 2 if dx <= 0 else 1
                    im.putpixel((cx + dx, cy + dy), C(CHROME[k]))
    return im


def chrome_items():
    raw = new()
    for y in range(16):
        for x in range(16):
            d = ((x - 8) / 5.5) ** 2 + ((y - 8.5) / 4.6) ** 2 + 0.3 * h(x // 2, y // 2, 2)
            if d <= 1:
                raw.putpixel((x, y), C(CHROME[3 if d < 0.25 and x < 8 else 2 if x + y < 15 else 1]))
    outline(raw, CHROME[0])
    ingot = new()
    for y in range(4, 12):
        if y < 7:                                            # the bevelled top face, leaning back
            x0, x1 = 4 + (7 - y), 12 + (7 - y) - 1
            col = CHROME[3] if y == 4 else CHROME[2]
        else:                                                # the front face
            x0, x1 = 2, 12
            col = CHROME[2] if y < 9 else CHROME[1]
        for x in range(x0, x1 + 1):
            ingot.putpixel((x, y), C(col))
        if y >= 7:
            for x in range(13, 13 + max(0, 4 - (y - 7))):    # the shaded end
                if x < 16 and y - 7 + (x - 13) < 5:
                    ingot.putpixel((x, y), C(CHROME[1] if y < 10 else CHROME[0]))
    for x in (4, 5, 6):
        ingot.putpixel((x, 8), C((255, 255, 255)))
    outline(ingot, CHROME[0])
    block = tile(lambda x, y: CHROME[0] if x in (0, 15) or y in (0, 15) else CHROME[3] if x == 1 or y == 1 else
                 CHROME[1] if x in (7, 8) or y in (7, 8) else CHROME[2])
    save(raw, "item/raw_chrome_digizoid.png")
    save(ingot, "item/chrome_digizoid_ingot.png")
    save(block, "block/chrome_digizoid_block.png")
    save(chrome_flecks(rock((126, 126, 126), False)), "block/chrome_digizoid_ore.png")
    save(chrome_flecks(rock((78, 78, 84), True)), "block/deepslate_chrome_digizoid_ore.png")
    for b in CHROME_ORES + ["chrome_digizoid_block"]:
        write_json(A / "blockstates" / f"{b}.json", {"variants": {"": {"model": f"{NS}:block/{b}"}}})
        write_json(A / "models" / "block" / f"{b}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{NS}:block/{b}"}})
        write_json(A / "models" / "item" / f"{b}.json", {"parent": f"{NS}:block/{b}"})
    drop_self("chrome_digizoid_block")
    for ore in CHROME_ORES:
        write_json(D / "loot_table" / "blocks" / f"{ore}.json", {"type": "minecraft:block", "pools": [{"rolls": 1, "entries": [{
            "type": "minecraft:alternatives", "children": [
                {"type": "minecraft:item", "name": f"{NS}:{ore}", "conditions": [{"condition": "minecraft:match_tool", "predicate": {
                    "predicates": {"minecraft:enchantments": [{"enchantments": "minecraft:silk_touch", "levels": {"min": 1}}]}}}]},
                {"type": "minecraft:item", "name": f"{NS}:raw_chrome_digizoid", "functions": [
                    {"function": "minecraft:apply_bonus", "enchantment": "minecraft:fortune", "formula": "minecraft:ore_drops"},
                    {"function": "minecraft:explosion_decay"}]}]}]}]})
    for src in ["raw_chrome_digizoid"] + CHROME_ORES:
        for kind, cook in (("smelting", 200), ("blasting", 100)):
            write_json(D / "recipe" / f"chrome_digizoid_ingot_from_{kind}_{src}.json", {
                "type": f"minecraft:{kind}", "category": "misc", "ingredient": {"item": f"{NS}:{src}"},
                "result": {"id": f"{NS}:chrome_digizoid_ingot"}, "experience": 1.0, "cookingtime": cook})
    write_json(D / "recipe" / "chrome_digizoid_block.json", {
        "type": "minecraft:crafting_shaped", "category": "building", "pattern": ["III", "III", "III"],
        "key": {"I": {"item": f"{NS}:chrome_digizoid_ingot"}}, "result": {"id": f"{NS}:chrome_digizoid_block", "count": 1}})
    write_json(D / "recipe" / "chrome_digizoid_ingot_from_block.json", {
        "type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [{"item": f"{NS}:chrome_digizoid_block"}],
        "result": {"id": f"{NS}:chrome_digizoid_ingot", "count": 9}})
    # world generation: deep and a little rarer than diamond (diamond: 7 veins of 4 and more below y 16)
    write_json(D / "worldgen" / "configured_feature" / "chrome_digizoid_ore.json", {"type": "minecraft:ore", "config": {
        "size": 4, "discard_chance_on_air_exposure": 0.5, "targets": [
            {"target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"},
             "state": {"Name": f"{NS}:chrome_digizoid_ore"}},
            {"target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:deepslate_ore_replaceables"},
             "state": {"Name": f"{NS}:deepslate_chrome_digizoid_ore"}}]}})
    write_json(D / "worldgen" / "placed_feature" / "chrome_digizoid_ore.json", {
        "feature": f"{NS}:chrome_digizoid_ore", "placement": [
            {"type": "minecraft:count", "count": 4}, {"type": "minecraft:in_square"},
            {"type": "minecraft:height_range", "height": {"type": "minecraft:trapezoid",
                                                          "min_inclusive": {"absolute": -64}, "max_inclusive": {"absolute": 8}}},
            {"type": "minecraft:biome"}]})


# --- balls (recoloured from Cobblemon's Poke Ball) ---------------------------------------------------------------------

def recolour_ball(im: Image.Image, style: str) -> Image.Image:
    """Poke Ball -> a tier: the red top becomes the tier's look, the band and white bottom follow."""
    im = im.convert("RGBA")
    px = im.load()
    w, hh = im.size
    for y in range(hh):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            hu, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            top = s > 0.45 and (hu < 0.06 or hu > 0.92)
            white = s < 0.2 and v > 0.7
            if style == "wireframe_ball":                       # black, traced with a cyan wire grid
                grid = (x % 4 == 0) or (y % 4 == 0)
                if top or white:
                    c = (60, 240, 255) if grid else (16, 24, 34) if top else (34, 46, 60)
                    px[x, y] = C(c, 0.75 + 0.25 * v, a)
                elif v < 0.25:
                    px[x, y] = C((60, 240, 255), 0.6, a)
            elif style == "data_net_ball":                       # green top with a diagonal net, grey bottom
                net = (x + y) % 5 == 0 or (x - y) % 5 == 0
                if top:
                    px[x, y] = C((230, 255, 230) if net else (40, 170, 70), 0.7 + 0.3 * v, a)
                elif white:
                    px[x, y] = C((200, 206, 210), v, a)
                elif v < 0.25:
                    px[x, y] = C((20, 60, 30), 1, a)
            else:                                                 # chrome: polished silver top, dark steel band
                if top:
                    t = (x * 0.8 + y) / max(1, w + hh) * 6
                    k = 0.75 + 0.35 * abs(math.sin(t * math.pi))
                    px[x, y] = C((200, 210, 226), k * (0.8 + 0.2 * v), a)
                elif white:
                    px[x, y] = C((120, 130, 150), 0.7 + 0.3 * v, a)
                elif v < 0.25:
                    px[x, y] = C((30, 34, 44), 1, a)
    return im


def balls(jar):
    def img(path):
        import io
        return Image.open(io.BytesIO(jar.read("assets/cobblemon/" + path)))

    for name in BALLS:
        out = {
            f"item/poke_balls/{name}.png": recolour_ball(img("textures/item/poke_balls/poke_ball.png"), name),
            f"item/poke_balls/models/{name}.png": recolour_ball(img("textures/item/poke_balls/models/poke_ball.png"), name),
            f"poke_balls/{name}.png": recolour_ball(img("textures/poke_balls/poke_ball.png"), name),
            f"gui/ball/{name}.png": recolour_ball(img("textures/gui/ball/poke_ball.png"), name),
        }
        for rel, im in out.items():
            save(im, rel)
        write_json(A / "models/item" / f"{name}.json",
                   {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/poke_balls/{name}"}})
        write_json(A / "models/item" / f"{name}_model.json",
                   {"parent": "cobblemon:item/poke_ball_model", "textures": {"layer0": f"{NS}:item/poke_balls/models/{name}"}})
        write_json(A / "bedrock/poke_balls/variations" / f"0_{name}_base.json",
                   {"order": 0, "pokeball": f"{NS}:{name}", "variations": [
                       {"aspects": [], "layers": [], "model": "cobblemon:poke_ball.geo", "poser": "cobblemon:poke_ball",
                        "texture": f"{NS}:textures/poke_balls/{name}.png"}]})


# --- recipes, tags, lang ------------------------------------------------------------------------------------------------

def shaped(name, pattern, key, result, count=1, cat="misc"):
    write_json(D / "recipe" / f"{name}.json", {"type": "minecraft:crafting_shaped", "category": cat, "pattern": pattern,
                                               "key": {k: {"item": v} for k, v in key.items()},
                                               "result": {"id": result, "count": count}})


def shapeless(name, items, result, count=1, cat="misc"):
    write_json(D / "recipe" / f"{name}.json", {"type": "minecraft:crafting_shapeless", "category": cat,
                                               "ingredients": [{"item": i} for i in items],
                                               "result": {"id": result, "count": count}})


def recipes():
    n = lambda s: f"{NS}:{s}"
    shapeless("wireframe_ball", ["cobblemon:poke_ball", "minecraft:glass_pane", "minecraft:redstone"], n("wireframe_ball"))
    shaped("wireframe_ball_x4", ["GRG", "RBR", "GRG"], {"G": "minecraft:glass_pane", "R": "minecraft:redstone",
                                                         "B": "cobblemon:great_ball"}, n("wireframe_ball"), 4)
    shapeless("data_net_ball", ["cobblemon:great_ball", n("vaccine_fragment"), n("data_fragment"), n("virus_fragment"),
                                "minecraft:string"], n("data_net_ball"), 2)
    shapeless("chrome_digizoid_ball", ["cobblemon:ultra_ball", n("chrome_digizoid_ingot")], n("chrome_digizoid_ball"), 2)
    for a in ATTR:
        shaped(f"{a}_chip", ["FFF", "FGF", "FFF"], {"F": n(f"{a}_fragment"), "G": "minecraft:gold_ingot"}, n(f"{a}_chip"))
    shaped("digivice", ["IGI", "RCR", "IBI"], {"I": "minecraft:iron_ingot", "G": "minecraft:glass_pane", "R": "minecraft:redstone",
                                                "C": n("chrome_digizoid_ingot"), "B": "minecraft:stone_button"}, n("digivice"))
    shapeless("high_speed_plugin", ["minecraft:paper", n("data_fragment"), "minecraft:sugar"], n("high_speed_plugin"), 2)
    shapeless("metal_armor", ["minecraft:paper", n("vaccine_fragment"), "minecraft:iron_ingot"], n("metal_armor"), 2)
    shapeless("giga_destroyer", ["minecraft:paper", n("virus_fragment"), "minecraft:gunpowder", "minecraft:gunpowder"], n("giga_destroyer"), 2)
    shapeless("recovery_disk", ["minecraft:paper", n("data_fragment"), "minecraft:glistering_melon_slice"], n("recovery_disk"), 2)
    shapeless("dot_virus", ["minecraft:paper", n("virus_fragment"), "minecraft:glow_ink_sac"], n("dot_virus"), 2)
    shapeless("bug_card", ["minecraft:paper", n("virus_fragment"), "minecraft:spider_eye"], n("bug_card"), 2)
    shapeless("digimeat", ["minecraft:beef", "minecraft:bone_meal"], n("digimeat"), 1, "food")
    shapeless("super_carrot", ["minecraft:golden_carrot", n("data_fragment")], n("super_carrot"), 1, "food")
    shaped("punching_bag", [" C ", "LWL", "LWL"], {"C": "minecraft:chain", "L": "minecraft:leather", "W": "minecraft:red_wool"},
           n("punching_bag"), 1, "building")
    shaped("treadmill", ["I  ", "IRI", "BBB"], {"I": "minecraft:iron_ingot", "R": "minecraft:redstone", "B": "minecraft:black_wool"},
           n("treadmill"), 1, "building")
    shaped("waterfall", ["CWC", "C C", "CCC"], {"C": "minecraft:mossy_cobblestone", "W": "minecraft:water_bucket"},
           n("waterfall"), 1, "building")
    shaped("meditation_mat", ["PGP"], {"P": "minecraft:purple_carpet", "G": "minecraft:gold_nugget"}, n("meditation_mat"), 1, "building")
    shaped("target_dummy", [" T ", " H ", " S "], {"T": "minecraft:target", "H": "minecraft:hay_block", "S": "minecraft:stick"},
           n("target_dummy"), 1, "building")


def merge_tag(path: Path, values):
    obj = json.loads(path.read_text()) if path.exists() else {"replace": False, "values": []}
    obj["values"] = sorted(set(obj["values"]) | set(values))
    write_json(path, obj)


def tags():
    b = ROOT / "data" / "minecraft" / "tags" / "block"
    merge_tag(b / "mineable" / "pickaxe.json", [f"{NS}:{x}" for x in CHROME_ORES + ["chrome_digizoid_block", "treadmill", "waterfall"]])
    merge_tag(b / "mineable" / "axe.json", [f"{NS}:punching_bag", f"{NS}:target_dummy"])
    merge_tag(b / "needs_iron_tool.json", [f"{NS}:{x}" for x in CHROME_ORES + ["chrome_digizoid_block"]])
    merge_tag(b / "crops.json", [f"{NS}:digimeat_crop", f"{NS}:super_carrot_crop"])
    merge_tag(b / "maintains_farmland.json", [f"{NS}:digimeat_crop", f"{NS}:super_carrot_crop"])
    merge_tag(ROOT / "data" / "cobblemon" / "tags" / "item" / "poke_balls.json", [f"{NS}:{x}" for x in BALLS])


def crops():
    for kind in ("digimeat", "super_carrot"):
        for s in range(4):
            save(crop_stage(kind, s), f"block/{kind}_crop_stage{s}.png")
            write_json(A / "models" / "block" / f"{kind}_crop_stage{s}.json",
                       {"parent": "minecraft:block/crop", "textures": {"crop": f"{NS}:block/{kind}_crop_stage{s}"}})
        write_json(A / "blockstates" / f"{kind}_crop.json", {"variants": {
            f"age={a}": {"model": f"{NS}:block/{kind}_crop_stage{min(3, a // 2)}"} for a in range(8)}})
        ripe = {"condition": "minecraft:block_state_property", "block": f"{NS}:{kind}_crop", "properties": {"age": "7"}}
        pools = [
            {"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{NS}:{kind}"}]},
            {"rolls": 1, "conditions": [ripe], "entries": [{"type": "minecraft:item", "name": f"{NS}:{kind}", "functions": [
                {"function": "minecraft:apply_bonus", "enchantment": "minecraft:fortune",
                 "formula": "minecraft:binomial_with_bonus_count", "parameters": {"extra": 3, "probability": 0.5714286}}]}]},
        ]
        if kind == "digimeat":
            pools.append({"rolls": 1, "conditions": [ripe, {"condition": "minecraft:random_chance", "chance": 0.05}],
                          "entries": [{"type": "minecraft:item", "name": f"{NS}:sirloin"}]})
        write_json(D / "loot_table" / "blocks" / f"{kind}_crop.json",
                   {"type": "minecraft:block", "functions": [{"function": "minecraft:explosion_decay"}], "pools": pools})


LANG = {
    f"item.{NS}.dot_virus": "Digi-Modify: Dot Virus",
    f"item.{NS}.dot_virus.tooltip": "Pixelates the foe for 3 turns: half Attack, no special moves",
    f"item.{NS}.bug_card": "Digi-Modify: Bug Card",
    f"item.{NS}.bug_card.tooltip": "Bugs the foe for 3 turns: the attribute triangle is inverted for it",
    f"item.{NS}.digiegg_of_courage": "Digi-Egg of Courage",
    f"item.{NS}.digiegg_of_courage.tooltip": "Use it on a V-mon: it armor-digivolves into Fladramon.",
    f"item.{NS}.digiegg_of_friendship": "Digi-Egg of Friendship",
    f"item.{NS}.digiegg_of_friendship.tooltip": "Use it on a V-mon: it armor-digivolves into Lighdramon.",
    f"{NS}.digivice.jogress": "%s DNA-digivolves into %s!",
    "cobblemon.move.dotvirus": "Dot Virus",
    "cobblemon.move.dotvirus.desc": "Compresses the target into 8-bit dot data for 3 turns: its Attack is halved and it can't use special moves.",
    "cobblemon.move.bugcode": "Bug Code",
    "cobblemon.move.bugcode.desc": "Writes a bug into the target's data for 3 turns, inverting its attribute advantages.",
    "cobblemon.battle.start.bugcode": "%1$s's data is bugged: its attribute advantages are turned around!",
    "cobblemon.battle.end.bugcode": "%1$s's data was debugged.",
    "cobblemon.battle.activate.fieldboost": "%1$s draws power from the battleground!",
    f"item.{NS}.digivice": "Digivice",
    f"item.{NS}.high_speed_plugin": "Digi-Modify: High-Speed Plug-In",
    f"item.{NS}.high_speed_plugin.tooltip": "Speed +2",
    f"item.{NS}.metal_armor": "Digi-Modify: Metal Armor",
    f"item.{NS}.metal_armor.tooltip": "Defense +2, Sp. Def +1",
    f"item.{NS}.giga_destroyer": "Digi-Modify: Giga Destroyer",
    f"item.{NS}.giga_destroyer.tooltip": "Attack +1, Sp. Atk +1, and its hits land critically more often",
    f"item.{NS}.recovery_disk": "Digi-Modify: Recovery Disk",
    f"item.{NS}.recovery_disk.tooltip": "Restores half its HP and cures its status",
    f"{NS}.card.how": "In battle, with a Digivice in your inventory: use it on your Digimon (takes your turn).",
    f"{NS}.card.no_digivice": "You need a Digivice to swipe Digi-Modify cards.",
    f"{NS}.digivice.energy": "Tamer Energy: %s/%s",
    f"{NS}.digivice.status": "Digivice: Tamer Energy %s/%s. Your Digimon:",
    f"{NS}.digivice.tooltip_scan": "Use it on a Digimon to scan it; use it in the air for your party's data.",
    f"{NS}.digivice.tooltip_pc": "Sneak and use it to open your PC from anywhere.",
    f"{NS}.digivice.tooltip_warp": "In battle, use it on your Digimon to warp-digivolve it a stage (%s energy), or two stages while sneaking (%s); with a Jogress partner at hand it DNA-digivolves instead.",
    f"{NS}.digivice.scan_title": "Digivice scan: %s",
    f"{NS}.digivice.beats": " Its attribute beats %s.",
    f"{NS}.digivice.evolves_into": " Digivolves into:",
    f"{NS}.digivice.evolves_from": " Digivolves from: ",
    f"{NS}.digivice.no_evolutions": " No further digivolutions.",
    f"{NS}.digivice.warped": "%s warp-digivolves into %s!",
    f"{NS}.digivice.already_warped": "%s has already digivolved in this battle.",
    f"{NS}.digivice.no_warp": "%s has no digivolution it can warp to.",
    f"{NS}.digivice.no_warp_two": "%s can't warp two stages up.",
    f"{NS}.digivice.low_energy": "Not enough Tamer Energy (%s; it takes %s).",
    f"{NS}.digivice.dark_tower": "A Dark Tower's aura blocks the digivolution!",
    f"{NS}.stage.baby1": "Baby I (Fresh)",
    f"{NS}.stage.baby2": "Baby II (In-Training)",
    f"{NS}.stage.child": "Child (Rookie)",
    f"{NS}.stage.adult": "Adult (Champion)",
    f"{NS}.stage.perfect": "Perfect (Ultimate)",
    f"{NS}.stage.ultimate": "Ultimate (Mega)",
    f"{NS}.stage.super_ultimate": "Super Ultimate",
    f"{NS}.req.level": "level %s",
    f"{NS}.req.attribute": "%s attribute",
    f"{NS}.req.properties": "%s",
    f"{NS}.req.other": "%s",
    "cobblemon.battle.activate.warpdigivolution": "%1$s's data surges with power!",
    f"item.{NS}.wireframe_ball": "Wireframe Ball",
    f"item.{NS}.data_net_ball": "Data-Net Ball",
    f"item.{NS}.chrome_digizoid_ball": "Chrome Digizoid Ball",
    f"item.{NS}.vaccine_fragment": "Vaccine Fragment",
    f"item.{NS}.data_fragment": "Data Fragment",
    f"item.{NS}.virus_fragment": "Virus Fragment",
    f"item.{NS}.vaccine_chip": "Vaccine Chip",
    f"item.{NS}.data_chip": "Data Chip",
    f"item.{NS}.virus_chip": "Virus Chip",
    f"item.{NS}.digimeat": "Digi-Meat",
    f"item.{NS}.sirloin": "Sirloin",
    f"item.{NS}.super_carrot": "Super Carrot",
    f"block.{NS}.digimeat_crop": "Digi-Meat",
    f"block.{NS}.super_carrot_crop": "Super Carrots",
    f"block.{NS}.punching_bag": "Punching Bag",
    f"block.{NS}.treadmill": "Treadmill",
    f"block.{NS}.waterfall": "Training Waterfall",
    f"block.{NS}.meditation_mat": "Meditation Mat",
    f"block.{NS}.target_dummy": "Target Dummy",
    f"block.{NS}.chrome_digizoid_ore": "Chrome Digizoid Ore",
    f"block.{NS}.deepslate_chrome_digizoid_ore": "Deepslate Chrome Digizoid Ore",
    f"block.{NS}.chrome_digizoid_block": "Block of Chrome Digizoid",
    f"item.{NS}.raw_chrome_digizoid": "Raw Chrome Digizoid",
    f"item.{NS}.chrome_digizoid_ingot": "Chrome Digizoid Ingot",
    f"{NS}.use.not_yours": "That isn't your Pokémon.",
    f"{NS}.use.in_battle": "Not during a battle.",
    f"{NS}.use.not_digimon": "%s isn't a Digimon: it can't read attribute data.",
    f"{NS}.attribute.vaccine": "Vaccine",
    f"{NS}.attribute.data": "Data",
    f"{NS}.attribute.virus": "Virus",
    f"{NS}.attribute.free": "Free",
    f"{NS}.attribute.variable": "Variable",
    f"{NS}.attribute.already": "%s is already %s.",
    f"{NS}.attribute.rewritten": "%s's attribute was rewritten: it is now %s!",
    f"{NS}.attribute.absorbed": "%s absorbed the %s data (%s/%s).",
    f"{NS}.attribute.fragment_tooltip": "Use it on your Digimon: %2$s in a row rewrite its attribute to %1$s.",
    f"{NS}.attribute.chip_tooltip": "Use it on your Digimon: rewrites its attribute to %s at once, opening its %1$s digivolutions.",
    f"{NS}.attribute.beats": "%s beats %s in battle (1.25x damage).",
    f"{NS}.food.full": "%s is full.",
    f"{NS}.food.fed": "%s enjoyed it!",
    f"{NS}.food.fed_evs": "%s enjoyed it! (+%s EVs)",
    f"{NS}.food.tooltip": "Feed it to your Pokémon (use it on them): fills them up and raises friendship.",
    f"{NS}.food.ev": "+%s %s EVs",
    f"{NS}.training.punching_bag": "punching bag",
    f"{NS}.training.treadmill": "treadmill",
    f"{NS}.training.waterfall": "training waterfall",
    f"{NS}.training.meditation_mat": "meditation mat",
    f"{NS}.training.target_dummy": "target dummy",
    f"{NS}.training.start": "%s steps up to the %s (%s)! Use it again while the marker is in the green.",
    f"{NS}.training.perfect": "Perfect! %s gained %s %s EVs.",
    f"{NS}.training.good": "Good! %s gained %s %s EVs.",
    f"{NS}.training.miss": "Missed... %s gained %s %s EV.",
    f"{NS}.training.maxed": "%s can't train its %s any further.",
    f"{NS}.training.timeout": "Too slow: the round is over.",
    f"{NS}.training.no_partner": "You need a healthy Pokémon in your party to train.",
    f"{NS}.catch.too_strong": "The %s's data is too strong: only a Chrome Digizoid Ball can hold an Ultimate or Mega.",
    "cobblemon.battle.activate.attributeadvantage": "%1$s's attribute has the upper hand!",
    "cobblemon.battle.activate.attributedisadvantage": "%1$s's attribute is at a disadvantage...",
    f"item.{NS}.digiball.tooltip": "Three times as good as a Poké Ball on Digimon below Ultimate.",
    f"item.{NS}.wireframe_ball.tooltip": "Four times as good on In-Training and Rookie Digimon.",
    f"item.{NS}.data_net_ball.tooltip": "Four times as good on Champion Digimon.",
    f"item.{NS}.chrome_digizoid_ball.tooltip": "Four times as good on Ultimate and Mega Digimon, and the only ball that can catch them.",
}


def build(jar=None):
    for a in ATTR:
        save(fragment(a), f"item/{a}_fragment.png")
        save(chip(a), f"item/{a}_chip.png")
        for k in ("fragment", "chip"):
            write_json(A / "models" / "item" / f"{a}_{k}.json",
                       {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/{a}_{k}"}})
    save(digivice(), "item/digivice.png")
    for c in CARDS:
        save(card(c), f"item/{c}.png")
    save(digiegg((230, 120, 40), (250, 220, 90), SUN), "item/digiegg_of_courage.png")
    save(digiegg((50, 120, 220), (230, 240, 255), CROSS), "item/digiegg_of_friendship.png")
    save(digimeat(), "item/digimeat.png")
    save(sirloin(), "item/sirloin.png")
    save(super_carrot(), "item/super_carrot.png")
    for i in ("digimeat", "sirloin", "super_carrot", "raw_chrome_digizoid", "chrome_digizoid_ingot", "digivice", "digiegg_of_courage", "digiegg_of_friendship", *CARDS):
        write_json(A / "models" / "item" / f"{i}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/{i}"}})
    crops()
    training_textures()
    training_models()
    chrome_items()
    recipes()
    tags()
    if jar is not None:
        balls(jar)
    return LANG


if __name__ == "__main__":
    import sys
    import zipfile
    lang = build(zipfile.ZipFile(sys.argv[1]) if len(sys.argv) > 1 else None)
    f = A / "lang" / "en_us.json"
    d = json.loads(f.read_text()) if f.exists() else {}
    d.update(lang)
    write_json(f, dict(sorted(d.items())))
