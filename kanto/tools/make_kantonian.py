#!/usr/bin/env python3
"""
Stage 3 of CobbleEffort: Kanto: Kantonian ore (stone and deepslate, Kanto only, a little more common than iron: iron's
three vein bands with 20% more veins), raw Kantonian -> Kantonian ingots (and a storage block), and Kantonian armor.
The armor's plain set is crafted like iron armor; an outfit is crafted with a dye or wool of its colour in the shape's
gap (helmet "III/IXI", chestplate "IXI/III/III", leggings "III/IXI/I I", boots "IXI/I I"). Outfits are original
Kanto-flavoured looks (trainer classes, not characters). All art is painted here. Run by make_assets.py.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "common" / "src" / "main" / "resources"
MOD = "cobbleeffort_kanto"
A = RES / "assets" / MOD
D = RES / "data" / MOD
LANG: dict[str, str] = {}

# the metal: a cool blue-steel (Kanto's Game Boy greys with a blue cast)
METAL = [(28, 32, 48), (70, 82, 112), (124, 140, 176), (190, 204, 232), (240, 246, 255)]
PIECES = ["helmet", "chestplate", "leggings", "boots"]
PIECE_NAMES = {"helmet": "Helmet", "chestplate": "Chestplate", "leggings": "Leggings", "boots": "Boots"}


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def save(img, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, optimize=True)


def h(*a):
    v = 2166136261
    for x in a:
        v = ((v ^ (int(x) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return v / 0xFFFFFFFF


def clamp(c, a=255):
    return tuple(max(0, min(255, int(round(v)))) for v in c[:3]) + (a,)


def shade(c, k):
    return tuple(v * k for v in c)


# --- ore, raw, ingot, block ---------------------------------------------------------------------------------------------
def rock(base, streaks):
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            k = 0.88 + 0.22 * h(x // 2, y // 2, 11) + 0.08 * (h(x, y, 13) - 0.5)
            if streaks and (y + int(2 * h(x // 4, 7))) % 5 == 0:
                k *= 0.82
            if not streaks and h(x, y, 17) > 0.93:
                k *= 0.7
            im.putpixel((x, y), clamp(shade(base, k)))
    return im


def nuggets(im):
    """Chunky square nuggets of the metal, lit top-left (8-bit style), with a dark outline."""
    for cx, cy, w, hh in ((3, 3, 3, 2), (10, 2, 2, 3), (6, 7, 3, 3), (12, 9, 2, 2), (2, 11, 3, 2), (8, 12, 2, 2)):
        for y in range(cy - 1, cy + hh + 1):
            for x in range(cx - 1, cx + w + 1):
                if not (0 <= x < 16 and 0 <= y < 16):
                    continue
                inside = cx <= x < cx + w and cy <= y < cy + hh
                if not inside:
                    if (x in (cx - 1, cx + w)) and (y in (cy - 1, cy + hh)):
                        continue
                    im.putpixel((x, y), clamp(METAL[0]))
                else:
                    c = METAL[4] if (x == cx and y == cy) else METAL[3] if (x == cx or y == cy) else METAL[2]
                    if x == cx + w - 1 and y == cy + hh - 1:
                        c = METAL[1]
                    im.putpixel((x, y), clamp(c))
    return im


def raw():
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    blobs = [(5.5, 8.5, 4.2), (10, 6.5, 3.6), (9.5, 10.5, 3.2)]
    for y in range(16):
        for x in range(16):
            d = min(((x - bx) ** 2 + (y - by) ** 2) ** 0.5 - r for bx, by, r in blobs)
            if d <= 0:
                lit = (x + y) < 13
                c = METAL[3] if (lit and d < -1.2 and h(x, y, 3) > 0.5) else METAL[2] if d < -0.8 else METAL[1]
                if h(x, y, 5) > 0.86:
                    c = (110, 92, 80)                          # bits of rock
                im.putpixel((x, y), clamp(c))
            elif d <= 0.9:
                im.putpixel((x, y), clamp(METAL[0]))
    return im


def ingot():
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    # an isometric-ish bar (like vanilla's): top face, front face, outline
    for y in range(16):
        for x in range(16):
            u, v = x - y * 0.5, y
            top = 5 <= v <= 8 and 0 <= u + 2 <= 11 - (8 - v) * 0.0 and x >= 2 + (8 - v) and x <= 13 - (v - 5) * 0
            front = 9 <= v <= 11 and 2 <= x <= 12 - (v - 9) * 0
            if top and x <= 14:
                c = METAL[4] if v == 5 or x == 2 + (8 - v) else METAL[3]
                im.putpixel((x, y), clamp(c))
            elif front:
                c = METAL[2] if v < 11 else METAL[1]
                if x == 12:
                    c = METAL[1]
                im.putpixel((x, y), clamp(c))
    # outline
    px = im.load()
    out = im.copy()
    for y in range(16):
        for x in range(16):
            if px[x, y][3]:
                continue
            if any(0 <= x + dx < 16 and 0 <= y + dy < 16 and px[x + dx, y + dy][3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out.putpixel((x, y), clamp(METAL[0]))
    return out


def block():
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            edge = x in (0, 15) or y in (0, 15)
            c = METAL[1] if edge else METAL[3] if (x == 1 or y == 1) else METAL[2]
            if not edge and (x + y) % 7 == 0 and 3 < x < 13 and 3 < y < 13:
                c = METAL[3]                                    # a diagonal sheen
            if 6 <= x <= 9 and 6 <= y <= 9:                     # a Kanto-PC-ish rivet square
                c = METAL[0] if x in (6, 9) or y in (6, 9) else METAL[4]
            im.putpixel((x, y), clamp(c))
    return im


# --- armor: worn textures -----------------------------------------------------------------------------------------------
# outfit id -> (name, colour word (dye/wool), palette)
OUTFITS = {
    "trainer": ("Trainer", "red", {"cap": (200, 40, 40), "cap2": (245, 245, 245), "shirt": (30, 30, 36), "jacket": (200, 40, 40),
                                   "trim": (245, 245, 245), "pants": (54, 72, 140), "belt": (30, 30, 36), "shoe": (200, 40, 40), "sole": (240, 240, 240)}),
    "ace": ("Ace", "blue", {"cap": (40, 70, 170), "cap2": (40, 70, 170), "shirt": (240, 240, 240), "jacket": (40, 70, 170),
                            "trim": (240, 240, 240), "pants": (30, 30, 36), "belt": (200, 170, 60), "shoe": (30, 30, 36), "sole": (90, 90, 96)}),
    "professor": ("Professor", "white", {"hair": (170, 170, 176), "shirt": (200, 120, 130), "jacket": (244, 244, 240),
                                         "trim": (200, 200, 196), "pants": (120, 84, 54), "belt": (60, 40, 26), "shoe": (90, 60, 36), "sole": (50, 34, 22)}),
    "hiker": ("Hiker", "brown", {"cap": (120, 84, 50), "cap2": (90, 60, 34), "shirt": (70, 120, 60), "jacket": (186, 150, 100),
                                 "trim": (120, 84, 50), "pants": (110, 80, 50), "belt": (60, 40, 26), "shoe": (80, 54, 30), "sole": (40, 30, 20)}),
    "swimmer": ("Swimmer", "light_blue", {"cap": (90, 180, 230), "goggles": (30, 30, 40), "lens": (150, 230, 255), "shirt": (90, 180, 230),
                                          "jacket": (90, 180, 230), "trim": (250, 250, 250), "pants": (30, 70, 160), "belt": (250, 250, 250),
                                          "shoe": (40, 110, 200), "sole": (30, 70, 160)}),
    "biker": ("Biker", "black", {"cap": (24, 24, 28), "visor": (60, 70, 90), "shirt": (60, 60, 66), "jacket": (24, 24, 28),
                                 "trim": (190, 190, 200), "pants": (40, 44, 60), "belt": (190, 190, 200), "shoe": (24, 24, 28), "sole": (60, 60, 66)}),
    "bug_catcher": ("Bug Catcher", "lime", {"cap": (230, 200, 110), "cap2": (200, 60, 50), "shirt": (120, 200, 60), "jacket": (120, 200, 60),
                                            "trim": (250, 250, 240), "pants": (200, 180, 120), "belt": (120, 90, 50), "shoe": (60, 130, 60), "sole": (240, 240, 230)}),
    "engineer": ("Engineer", "yellow", {"cap": (240, 200, 30), "cap2": (220, 180, 20), "shirt": (60, 90, 160), "jacket": (240, 120, 30),
                                        "trim": (220, 220, 225), "pants": (60, 90, 160), "belt": (40, 50, 80), "shoe": (110, 74, 40), "sole": (40, 30, 20)}),
    "psychic": ("Psychic", "purple", {"cap": (110, 50, 150), "shirt": (60, 24, 90), "jacket": (110, 50, 150), "trim": (230, 190, 70),
                                      "pants": (110, 50, 150), "belt": (230, 190, 70), "shoe": (40, 20, 50), "sole": (25, 12, 30)}),
}
PLAIN = {"cap": METAL[2], "cap2": METAL[3], "shirt": METAL[1], "jacket": METAL[2], "trim": (240, 240, 244),
         "pants": METAL[2], "belt": (20, 20, 26), "shoe": METAL[1], "sole": (20, 20, 26)}


def boxes(u, v, w, hgt, d):
    """A box's six faces as (name, x0, y0, width, height) on the texture (Minecraft's box UV)."""
    return [("top", u + d, v, w, d), ("bottom", u + d + w, v, w, d), ("right", u, v + d, d, hgt), ("front", u + d, v + d, w, hgt),
            ("left", u + d + w, v + d, d, hgt), ("back", u + d + w + d, v + d, w, hgt)]


def paint_box(im, u, v, w, hgt, d, fn):
    """fn(face, x, y, fw, fh) -> colour or None, per texel of each face (x, y local to the face)."""
    for face, x0, y0, fw, fh in boxes(u, v, w, hgt, d):
        for y in range(fh):
            for x in range(fw):
                c = fn(face, x, y, fw, fh)
                if c is not None:
                    # a gentle shade: lit top, darker sides and lower rows (matches vanilla armor's look)
                    k = {"top": 1.08, "bottom": 0.7, "front": 1.0, "back": 0.86, "left": 0.92, "right": 0.92}[face]
                    k *= 1.0 - 0.012 * y if face not in ("top", "bottom") else 1
                    k *= 0.97 + 0.06 * h(x0 + x, y0 + y, 29)
                    im.putpixel((x0 + x, y0 + y), clamp(shade(c, k)))


def outline_dark(c):
    return shade(c, 0.55)


def helmet_fn(o, pal):
    def f(face, x, y, fw, fh):
        if o == "professor":                                 # neat grey hair, no hat
            if face in ("top",):
                return pal["hair"]
            if face == "front":
                return pal["hair"] if y < 2 else None
            if face in ("left", "right", "back"):
                return pal["hair"] if y < (6 if face == "back" else 4) else None
            return None
        if o == "swimmer":                                   # a swim cap and goggles
            if face in ("top", "back", "left", "right"):
                if face != "top" and y >= 4:
                    return pal["goggles"] if y == 4 and face in ("left", "right") else None
                return pal["cap"]
            if face == "front":
                if y < 3:
                    return pal["cap"]
                if y == 3:
                    return pal["goggles"]
                if y == 4:
                    return pal["lens"] if x in (1, 2, 5, 6) else pal["goggles"]
                return None
            return None
        if o == "biker":                                     # a full helmet with a visor
            if face == "bottom":
                return None
            if face == "front":
                return pal["visor"] if 2 <= y <= 4 and 1 <= x <= 6 else pal["cap"] if (y < 2 or x in (0, 7) or y == 5) else None
            return pal["cap"] if (y < 7 or face == "top") else None
        if o == "psychic":                                   # a hood
            if face == "bottom":
                return None
            if face == "front":
                return pal["cap"] if (y < 1 or x in (0, 7)) else (pal["trim"] if y == 1 else None)
            return pal["cap"]
        if o == "engineer":                                  # a hard hat with a ridge
            if face == "top":
                return pal["cap2"] if x in (3, 4) else pal["cap"]
            if face in ("front", "back", "left", "right"):
                if y < 3:
                    return pal["cap2"] if (face in ("front", "back") and x in (3, 4)) else pal["cap"]
                if y == 3:
                    return outline_dark(pal["cap"])
            return None
        if o in ("hiker", "bug_catcher"):                    # a round hat with a band
            if face == "top":
                return pal["cap"]
            if face in ("front", "back", "left", "right"):
                if y < 2:
                    return pal["cap"]
                if y == 2:
                    return pal["cap2"]
                if y == 3:
                    return outline_dark(pal["cap"])
            return None
        # caps (plain, trainer, ace): crown and a front panel
        if face == "top":
            return pal["cap"]
        if face == "front":
            if y < 3:
                return pal.get("cap2", pal["cap"]) if 2 <= x <= 5 else pal["cap"]
            if y == 3:
                return outline_dark(pal["cap"])
            return None
        if face in ("back", "left", "right"):
            return pal["cap"] if y < 3 else (outline_dark(pal["cap"]) if y == 3 else None)
        return None
    return f


def torso_fn(o, pal, arms=False):
    """The chestplate on the body (and arms)."""
    def f(face, x, y, fw, fh):
        if face in ("top", "bottom") and not arms:
            return pal["jacket"]
        if arms:
            if face == "bottom":
                return None
            long = o in ("professor", "ace", "biker", "psychic", "trainer")
            if o == "swimmer":
                return pal["jacket"] if y < 4 else None
            if not long and y >= 5:
                return None
            if long and y >= 10:
                return pal["trim"] if y == 10 else None
            return pal["jacket"] if not (o == "engineer") else pal["shirt"]
        open_front = o in ("trainer", "ace", "professor", "hiker", "biker", "engineer")
        if face == "front":
            if o == "swimmer":
                return pal["trim"] if y % 4 == 2 else pal["jacket"]
            if o == "psychic":
                return pal["trim"] if x in (3, 4) else pal["jacket"]
            if open_front and 3 <= x <= 4:
                return pal["shirt"] if o != "trainer" else (pal["trim"] if x == 3 else pal["shirt"])
            if o == "engineer" and y in (5, 6):
                return pal["trim"]                          # reflective stripes
            if o == "biker" and (x, y) in ((1, 2), (6, 2), (1, 5), (6, 5)):
                return pal["trim"]                          # studs
            if o == "bug_catcher" and y == 0:
                return pal["trim"]
            return pal["jacket"]
        if face == "back":
            if o == "engineer" and y in (5, 6):
                return pal["trim"]
            if o == "professor" and y >= 9:
                return outline_dark(pal["jacket"])
            return pal["jacket"]
        if o == "engineer" and y in (5, 6):
            return pal["trim"]
        return pal["jacket"]
    return f


def legs_fn(o, pal, waist=False):
    def f(face, x, y, fw, fh):
        if waist:                                           # the leggings' belt round the body
            if face in ("top", "bottom"):
                return None
            if y < 8:
                return pal["jacket"] if (o in ("professor", "psychic") and face != "front") else None
            return pal["belt"] if y == 8 else pal["pants"]
        if face == "top":
            return None
        short = o in ("hiker", "bug_catcher", "swimmer")
        if short and y >= (5 if o != "swimmer" else 3):
            return None
        if o == "psychic":
            return pal["trim"] if y == 11 else pal["pants"]
        if o == "professor" and y < 5 and face in ("back",):
            return outline_dark(pal["jacket"])
        if o in ("trainer",) and face == "front" and y == 6:
            return shade(pal["pants"], 0.85)                # a knee crease
        return pal["pants"]
    return f


def boots_fn(o, pal):
    def f(face, x, y, fw, fh):
        if face == "top":
            return None
        if face == "bottom":
            return pal["sole"]
        top = 6 if o in ("hiker", "biker", "engineer") else 8
        if o == "swimmer":
            top = 9
        if y < top:
            return None
        if y == 11:
            return pal["sole"]
        if o == "trainer" and y == top:
            return pal["sole"]                              # white laces line
        return pal["shoe"]
    return f


def worn(o, pal):
    """The two armor layers: layer_1 (helmet, chestplate on body and arms, boots on legs), layer_2 (leggings)."""
    l1 = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    l2 = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    paint_box(l1, 0, 0, 8, 8, 8, helmet_fn(o, pal))
    paint_box(l1, 16, 16, 8, 12, 4, torso_fn(o, pal))
    paint_box(l1, 40, 16, 4, 12, 4, torso_fn(o, pal, arms=True))
    paint_box(l1, 0, 16, 4, 12, 4, boots_fn(o, pal))
    paint_box(l2, 16, 16, 8, 12, 4, legs_fn(o, pal, waist=True))
    paint_box(l2, 0, 16, 4, 12, 4, legs_fn(o, pal))
    return l1, l2


# --- armor: item icons ------------------------------------------------------------------------------------------------
ICONS = {
    "helmet": ["................",
               "................",
               "................",
               "....########....",
               "...#aaaaaaaa#...",
               "..#aAAAAAAAAa#..",
               "..#aAAbbbbAAa#..",
               "..#aAAbbbbAAa#..",
               "..#aAA####AAa#..",
               "..#aA#....#Aa#..",
               "..#a#......#a#..",
               "..###......###..",
               "................",
               "................",
               "................",
               "................"],
    "chestplate": ["................",
                   "..###......###..",
                   ".#aa#......#aa#.",
                   ".#aAA######AAa#.",
                   ".#aAAAAbbAAAAa#.",
                   ".#aAAAAbbAAAAa#.",
                   ".###AAAbbAAA###.",
                   "...#AAAbbAAA#...",
                   "...#AAAbbAAA#...",
                   "...#AAAbbAAA#...",
                   "...#ccccccccc#..",
                   "...#AAAAAAAAA#..",
                   "...#AAAAAAAAA#..",
                   "...###########..",
                   "................",
                   "................"],
    "leggings": ["................",
                 "...##########...",
                 "...#cccccccc#...",
                 "...#aAAAAAAA#...",
                 "...#aAAA#AAA#...",
                 "...#aAA##AAA#...",
                 "...#aAA##AAA#...",
                 "...#aAA##AAA#...",
                 "...#aAA##AAA#...",
                 "...#aAA##AAA#...",
                 "...#aAA##AAA#...",
                 "...#aAA##AAA#...",
                 "...#aAA##AAA#...",
                 "...####..####...",
                 "................",
                 "................"],
    "boots": ["................",
              "................",
              "................",
              "................",
              "................",
              "..####....####..",
              "..#aA#....#aA#..",
              "..#aA#....#aA#..",
              "..#aA#....#aA#..",
              "..#aA#....#aA#..",
              "..#aAA#...#aAA#.",
              ".#aAAAA#..#aAAA#",
              ".#ccccc#..#cccc#",
              ".#######..######",
              "................",
              "................"],
}


def icon(piece, pal):
    main = {"helmet": pal.get("cap", pal.get("hair")), "chestplate": pal["jacket"], "leggings": pal["pants"], "boots": pal["shoe"]}[piece]
    accent = {"helmet": pal.get("cap2", pal.get("lens", pal.get("visor", pal.get("trim", main)))), "chestplate": pal["shirt"],
              "leggings": pal["pants"], "boots": pal["shoe"]}[piece]
    trim = {"helmet": main, "chestplate": pal["trim"], "leggings": pal["belt"], "boots": pal["sole"]}[piece]
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(ICONS[piece]):
        for x, ch in enumerate(row):
            c = {"#": outline_dark(outline_dark(main)), "a": shade(main, 1.25), "A": main, "b": accent, "c": trim}.get(ch)
            if c is not None:
                im.putpixel((x, y), clamp(c))
    return im


# --- data -------------------------------------------------------------------------------------------------------------
SHAPES = {"helmet": (["III", "I I"], ["III", "IXI"]), "chestplate": (["I I", "III", "III"], ["IXI", "III", "III"]),
          "leggings": (["III", "I I", "I I"], ["III", "IXI", "I I"]), "boots": (["I I", "I I"], ["IXI", "I I"])}


def build():
    for name, img in (("kantonian_ore", nuggets(rock((126, 126, 126), False))),
                      ("deepslate_kantonian_ore", nuggets(rock((78, 78, 84), True))), ("kantonian_block", block())):
        save(img, A / "textures" / "block" / f"{name}.png")
        write_json(A / "blockstates" / f"{name}.json", {"variants": {"": {"model": f"{MOD}:block/{name}"}}})
        write_json(A / "models" / "block" / f"{name}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{MOD}:block/{name}"}})
        write_json(A / "models" / "item" / f"{name}.json", {"parent": f"{MOD}:block/{name}"})
    save(raw(), A / "textures" / "item" / "raw_kantonian.png")
    save(ingot(), A / "textures" / "item" / "kantonian_ingot.png")
    for item in ("raw_kantonian", "kantonian_ingot"):
        write_json(A / "models" / "item" / f"{item}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{item}"}})
    LANG.update({f"block.{MOD}.kantonian_ore": "Kantonian Ore", f"block.{MOD}.deepslate_kantonian_ore": "Deepslate Kantonian Ore",
                 f"block.{MOD}.kantonian_block": "Block of Kantonian", f"item.{MOD}.raw_kantonian": "Raw Kantonian",
                 f"item.{MOD}.kantonian_ingot": "Kantonian Ingot"})
    # loot: like iron ore (raw drop, Fortune, Silk Touch keeps the ore); the block drops itself
    for ore in ("kantonian_ore", "deepslate_kantonian_ore"):
        write_json(D / "loot_table" / "blocks" / f"{ore}.json", {"type": "minecraft:block", "pools": [{"rolls": 1, "entries": [{
            "type": "minecraft:alternatives", "children": [
                {"type": "minecraft:item", "name": f"{MOD}:{ore}", "conditions": [{"condition": "minecraft:match_tool", "predicate": {
                    "predicates": {"minecraft:enchantments": [{"enchantments": "minecraft:silk_touch", "levels": {"min": 1}}]}}}]},
                {"type": "minecraft:item", "name": f"{MOD}:raw_kantonian", "functions": [
                    {"function": "minecraft:apply_bonus", "enchantment": "minecraft:fortune", "formula": "minecraft:ore_drops"},
                    {"function": "minecraft:explosion_decay"}]}]}]}]})
        for kind, cook in (("smelting", 200), ("blasting", 100)):
            write_json(D / "recipe" / f"kantonian_ingot_from_{kind}_{ore}.json", {
                "type": f"minecraft:{kind}", "category": "misc", "ingredient": {"item": f"{MOD}:{ore}"},
                "result": {"id": f"{MOD}:kantonian_ingot"}, "experience": 0.7, "cookingtime": cook})
    for kind, cook in (("smelting", 200), ("blasting", 100)):
        write_json(D / "recipe" / f"kantonian_ingot_from_{kind}_raw_kantonian.json", {
            "type": f"minecraft:{kind}", "category": "misc", "ingredient": {"item": f"{MOD}:raw_kantonian"},
            "result": {"id": f"{MOD}:kantonian_ingot"}, "experience": 0.7, "cookingtime": cook})
    write_json(D / "loot_table" / "blocks" / "kantonian_block.json", {"type": "minecraft:block", "pools": [
        {"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{MOD}:kantonian_block"}], "conditions": [{"condition": "minecraft:survives_explosion"}]}]})
    write_json(D / "recipe" / "kantonian_block.json", {"type": "minecraft:crafting_shaped", "category": "building",
                                                      "pattern": ["III", "III", "III"], "key": {"I": {"item": f"{MOD}:kantonian_ingot"}},
                                                      "result": {"id": f"{MOD}:kantonian_block", "count": 1}})
    write_json(D / "recipe" / "kantonian_ingot_from_block.json", {"type": "minecraft:crafting_shapeless", "category": "misc",
                                                                 "ingredients": [{"item": f"{MOD}:kantonian_block"}],
                                                                 "result": {"id": f"{MOD}:kantonian_ingot", "count": 9}})
    tags = RES / "data" / "minecraft" / "tags" / "block"
    blocks = [f"{MOD}:kantonian_ore", f"{MOD}:deepslate_kantonian_ore", f"{MOD}:kantonian_block"]
    pick = json.loads((tags / "mineable" / "pickaxe.json").read_text())
    pick["values"] = sorted(set(pick["values"]) | set(blocks))
    write_json(tags / "mineable" / "pickaxe.json", pick)
    write_json(tags / "needs_stone_tool.json", {"replace": False, "values": blocks})
    # world generation: iron's three bands, 20% more veins, placed only in Kanto (cobbleeffort_kanto:in_kanto)
    for name, size, count, height in (
            ("kantonian_ore_upper", 9, 108, {"type": "minecraft:trapezoid", "min_inclusive": {"absolute": 80}, "max_inclusive": {"absolute": 384}}),
            ("kantonian_ore_middle", 9, 12, {"type": "minecraft:trapezoid", "min_inclusive": {"absolute": -24}, "max_inclusive": {"absolute": 56}}),
            ("kantonian_ore_small", 4, 12, {"type": "minecraft:uniform", "min_inclusive": {"above_bottom": 0}, "max_inclusive": {"absolute": 72}})):
        write_json(D / "worldgen" / "configured_feature" / f"{name}.json", {"type": "minecraft:ore", "config": {
            "size": size, "discard_chance_on_air_exposure": 0.0, "targets": [
                {"target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"},
                 "state": {"Name": f"{MOD}:kantonian_ore"}},
                {"target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:deepslate_ore_replaceables"},
                 "state": {"Name": f"{MOD}:deepslate_kantonian_ore"}}]}})
        write_json(D / "worldgen" / "placed_feature" / f"{name}.json", {"feature": f"{MOD}:{name}", "placement": [
            {"type": f"{MOD}:in_kanto"}, {"type": "minecraft:count", "count": count}, {"type": "minecraft:in_square"},
            {"type": "minecraft:height_range", "height": height}, {"type": "minecraft:biome"}]})
    # armor
    sets = [("kantonian", "Kantonian", None, PLAIN)] + [(f"kantonian_{o}", f"{n} Kantonian", colour, pal) for o, (n, colour, pal) in OUTFITS.items()]
    for mid, label, colour, pal in sets:
        o = mid.replace("kantonian_", "") if colour else "plain"
        l1, l2 = worn(o, pal)
        save(l1, A / "textures" / "models" / "armor" / f"{mid}_layer_1.png")
        save(l2, A / "textures" / "models" / "armor" / f"{mid}_layer_2.png")
        for piece in PIECES:
            item = f"{mid}_{piece}"
            save(icon(piece, pal), A / "textures" / "item" / f"{item}.png")
            write_json(A / "models" / "item" / f"{item}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{item}"}})
            LANG[f"item.{MOD}.{item}"] = f"{label} {PIECE_NAMES[piece]}"
            plain_shape, outfit_shape = SHAPES[piece]
            key = {"I": {"item": f"{MOD}:kantonian_ingot"}}
            if colour:
                key["X"] = [{"item": f"minecraft:{colour}_dye"}, {"item": f"minecraft:{colour}_wool"}]
            write_json(D / "recipe" / f"{item}.json", {"type": "minecraft:crafting_shaped", "category": "equipment",
                                                      "pattern": outfit_shape if colour else plain_shape, "key": key,
                                                      "result": {"id": f"{MOD}:{item}", "count": 1}})
    # armor tags: the vanilla enchantable/trim tags so they enchant and trim like any armor
    items = RES / "data" / "minecraft" / "tags" / "item"
    by = {p: [f"{MOD}:{m}_{p}" for m, *_ in sets] for p in PIECES}
    for tag, members in (("head_armor", by["helmet"]), ("chest_armor", by["chestplate"]), ("leg_armor", by["leggings"]),
                         ("foot_armor", by["boots"]), ("trimmable_armor", sum(by.values(), [])),
                         ("enchantable/head_armor", by["helmet"]), ("enchantable/chest_armor", by["chestplate"]),
                         ("enchantable/leg_armor", by["leggings"]), ("enchantable/foot_armor", by["boots"]),
                         ("enchantable/armor", sum(by.values(), [])), ("enchantable/equippable", sum(by.values(), [])),
                         ("enchantable/durability", sum(by.values(), []))):
        write_json(items / f"{tag}.json", {"replace": False, "values": members})
    return sets


if __name__ == "__main__":
    build()
