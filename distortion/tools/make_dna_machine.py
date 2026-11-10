#!/usr/bin/env python3
"""
The DNA machine's assets and data: the cloning tank Mewtwo comes from in the first movie (a tall glass cylinder of
glowing fluid on a heavy steel base, a domed cap trailing cables, a control panel with status lights), two blocks
tall, and the Mew DNA item. Textures are painted here (original art), plus the block models, blockstates, item
models, loot table, recipe, mining tag and English names. Run by make_assets.py (or alone).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "common" / "src" / "main" / "resources"
MOD = "cobbleeffort_distortion"
A = RES / "assets" / MOD
D = RES / "data" / MOD

LANG = {
    f"block.{MOD}.dna_machine": "DNA Machine",
    f"item.{MOD}.mew_dna": "Mew DNA",
    f"{MOD}.dna.filled": "DNA: %s / %s",
    f"{MOD}.dna.needs": "The tank needs %s more Mew DNA.",
    f"{MOD}.dna.select_mew": "Select Mew in your party, then use the DNA machine.",
    f"{MOD}.dna.not_mew": "%s can't go in: only Mew's DNA matches.",
    f"{MOD}.dna.inserted": "Mew floats into the tank... Come back in five minutes.",
    f"{MOD}.dna.working": "Still growing: %s min %s s left.",
    f"{MOD}.dna.done": "Something stirs in the DNA machine. Mewtwo has awoken!",
    f"{MOD}.dna.not_yours": "This isn't your Pokémon.",
    f"{MOD}.dna.retrieved": "%s joined you.",
    f"{MOD}.dna.dropped": "Your Mew left %s Mew DNA behind.",
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


def shade(c, f, alpha=255):
    return tuple(max(0, min(255, int(round(v * f)))) for v in c[:3]) + (alpha,)


# --- textures ----------------------------------------------------------------------------------------------------------
def metal():
    """Dark gun-metal plates: a seam across the middle, bevelled edges, rivets in the corners."""
    im = Image.new("RGBA", (16, 16))
    base = (64, 70, 82)
    for y in range(16):
        for x in range(16):
            f = 1.0 + 0.04 * (h(x, y, 1) - 0.5)
            if x == 0 or y == 0:
                f *= 1.25
            elif x == 15 or y == 15 or y == 8:
                f *= 0.7
            if (x, y) in ((2, 2), (13, 2), (2, 13), (13, 13), (2, 10), (13, 10)):
                f *= 1.45
            im.putpixel((x, y), shade(base, f))
    return im


def trim():
    """The brushed-steel collar and cap ring, with a band of hazard-orange."""
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            if 6 <= y <= 9:
                c = (214, 120, 40) if (x + y) % 6 < 3 else (52, 46, 44)
                im.putpixel((x, y), shade(c, 1.0))
            else:
                im.putpixel((x, y), shade((150, 156, 168), 0.9 + 0.12 * ((x * 3 + y) % 5 == 0) + (0.15 if y in (0, 10) else 0)))
    return im


def glass():
    """Heavy lab glass: faint teal tint, a brighter rim, and two diagonal highlights."""
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(16):
        for x in range(16):
            a, c = 34, (190, 240, 240)
            if x in (0, 15):
                a = 110
            if (x + y) % 16 in (3, 4) or (x + y) % 16 == 10:
                a, c = 120, (240, 255, 255)
            im.putpixel((x, y), c + (a,))
    return im


def panel():
    """The control panel: a dark screen with a green readout line and status lights."""
    im = Image.new("RGBA", (16, 16), (24, 28, 34, 255))
    for x in range(1, 15):
        for y in range(2, 9):
            im.putpixel((x, y), (16, 40, 34, 255))
        y = 5 + int(round(2 * math.sin(x * 0.9)))
        im.putpixel((x, y), (120, 255, 170, 255))
    for i, c in enumerate([(255, 70, 70), (255, 200, 60), (90, 255, 120), (80, 200, 255)]):
        im.putpixel((2 + i * 3, 12), c + (255,))
        im.putpixel((3 + i * 3, 12), shade(c, 0.6))
    for x in range(16):
        im.putpixel((x, 0), (90, 96, 108, 255))
        im.putpixel((x, 15), (16, 18, 22, 255))
    return im


def cable():
    """Ribbed black rubber cable."""
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            f = 0.75 + 0.5 * (1 - abs(x - 7.5) / 8) + (0.18 if y % 4 == 0 else 0)
            im.putpixel((x, y), shade((36, 38, 44), f))
    return im


def fluid():
    """The tank's fluid: deep teal brightening upwards, a faint DNA double helix and bubbles (32x32, scrolls)."""
    im = Image.new("RGBA", (32, 32))
    for y in range(32):
        for x in range(32):
            k = 0.75 + 0.25 * math.sin(y / 32 * 2 * math.pi + x * 0.2)
            c = (60 * k, 210 * k, 170 * k)
            for ph in (0, math.pi):
                hx = 16 + 9 * math.sin(y / 32 * 4 * math.pi + ph)
                if abs(x - hx) < 1.2:
                    c = (200, 255, 230)
            if y % 4 == 0 and min(abs(x - (16 + 9 * math.sin(y / 32 * 4 * math.pi))), 99) < 9 and x % 2 == 0 \
                    and abs(x - 16) <= abs(9 * math.sin(y / 32 * 4 * math.pi)):
                c = (150, 255, 210)                               # the rungs
            if h(x // 2, y // 2, 7) > 0.985:
                c = (230, 255, 250)
            im.putpixel((x, y), shade(c, 1.0))
    return im


def mew_dna_icon():
    """A stoppered vial of glowing pink fluid with a double helix in it."""
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(2, 15):
        for x in range(5, 11):
            edge = x in (5, 10) or y == 14
            if y <= 3:
                c = (120, 84, 60, 255) if x not in (5, 10) else (0, 0, 0, 0)    # cork
            elif edge:
                c = (210, 230, 240, 255)
            else:
                k = (y - 4) / 10
                c = (int(255 - 40 * k), int(140 - 60 * k), int(200 - 30 * k), 255)
                hx = 7.5 + 1.6 * math.sin(y * 1.1)
                hx2 = 7.5 - 1.6 * math.sin(y * 1.1)
                if abs(x - hx) < 0.6 or abs(x - hx2) < 0.6:
                    c = (255, 240, 250, 255)
            im.putpixel((x, y), c)
    im.putpixel((6, 6), (255, 255, 255, 255))
    return im


def machine_icon():
    """The machine in the inventory: steel base, glass tank of teal fluid with a pink silhouette, domed cap."""
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(16):
        for x in range(16):
            c = None
            if y >= 13 and 2 <= x <= 13:
                c = shade((70, 76, 90), 1.2 if y == 13 else 0.9)
            elif y == 12 and 3 <= x <= 12:
                c = (214, 120, 40, 255) if x % 3 else (52, 46, 44, 255)
            elif 3 <= y <= 11 and 4 <= x <= 11:
                if x in (4, 11):
                    c = (200, 235, 240, 255)
                else:
                    c = shade((60, 210, 170), 0.8 + 0.25 * (11 - y) / 8)
                    if 6 <= x <= 9 and 5 <= y <= 9 and not (y == 5 and x in (6, 9)):
                        c = (240, 150, 210, 255)                 # the Pokémon inside
            elif y == 2 and 3 <= x <= 12:
                c = (150, 156, 168, 255)
            elif y in (0, 1) and 5 <= x <= 10:
                c = shade((64, 70, 82), 1.1)
            if c:
                im.putpixel((x, y), c)
    return im


# --- models ------------------------------------------------------------------------------------------------------------
def el(frm, to, tex, faces=("north", "south", "east", "west", "up", "down"), **extra):
    return dict({"from": frm, "to": to, "faces": {f: {"texture": f"#{tex}"} for f in faces}}, **extra)


def glass_walls(y0, y1):
    return [el([2, y0, 2], [14, y1, 2.4], "glass"), el([2, y0, 13.6], [14, y1, 14], "glass"),
            el([2, y0, 2.4], [2.4, y1, 13.6], "glass"), el([13.6, y0, 2.4], [14, y1, 13.6], "glass")]


def ribs(y0, y1):
    return [el([x, y0, z], [x + 1, y1, z + 1], "metal") for x, z in ((1.5, 1.5), (13.5, 1.5), (1.5, 13.5), (13.5, 13.5))]


def models():
    tex = {"metal": f"{MOD}:block/dna_machine_metal", "trim": f"{MOD}:block/dna_machine_trim",
           "glass": f"{MOD}:block/dna_machine_glass", "panel": f"{MOD}:block/dna_machine_panel",
           "cable": f"{MOD}:block/dna_machine_cable", "particle": f"{MOD}:block/dna_machine_metal"}
    lower = [el([0, 0, 0], [16, 3, 16], "metal"), el([1, 3, 1], [15, 6, 15], "trim"),
             el([4, 1, -0.4], [12, 5.5, 0], "panel", faces=("north",)),
             el([14.3, 3, 7], [15.6, 16, 9], "cable"), el([0.4, 3, 7], [1.7, 16, 9], "cable"),
             el([6.5, 3, 14.3], [9.5, 16, 15.6], "cable")] + glass_walls(6, 16) + ribs(6, 16)
    upper = glass_walls(0, 10) + ribs(0, 10) + [
        el([14.3, 0, 7], [15.6, 11, 9], "cable"), el([0.4, 0, 7], [1.7, 11, 9], "cable"),
        el([6.5, 0, 14.3], [9.5, 11, 15.6], "cable"),
        el([1, 10, 1], [15, 12, 15], "trim"), el([0, 12, 0], [16, 15, 16], "metal"),
        el([4, 15, 4], [12, 16, 12], "metal"), el([6, 16, 6], [10, 17.5, 10], "trim"),
        el([10, 15.5, 7], [17.5, 17, 9], "cable"), el([-1.5, 15.5, 7], [6, 17, 9], "cable")]
    for half, elements in (("lower", lower), ("upper", upper)):
        write_json(A / "models" / "block" / f"dna_machine_{half}.json",
                   {"render_type": "minecraft:translucent", "ambientocclusion": False, "textures": tex, "elements": elements})
    rot = {"north": 0, "east": 90, "south": 180, "west": 270}
    write_json(A / "blockstates" / "dna_machine.json", {"variants": {
        f"facing={f},half={half}": dict({"model": f"{MOD}:block/dna_machine_{half}"}, **({"y": r} if r else {}))
        for f, r in rot.items() for half in ("lower", "upper")}})
    for item in ("dna_machine", "mew_dna"):
        write_json(A / "models" / "item" / f"{item}.json", {"parent": "minecraft:item/generated",
                                                           "textures": {"layer0": f"{MOD}:item/{item}"}})


def data():
    write_json(D / "loot_table" / "blocks" / "dna_machine.json", {
        "type": "minecraft:block", "pools": [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{MOD}:dna_machine"}],
                                              "conditions": [{"condition": "minecraft:block_state_property", "block": f"{MOD}:dna_machine",
                                                              "properties": {"half": "lower"}},
                                                             {"condition": "minecraft:survives_explosion"}]}]})
    write_json(D / "recipe" / "dna_machine.json", {
        "type": "minecraft:crafting_shaped", "category": "misc", "pattern": ["IGI", "GDG", "IRI"],
        "key": {"I": {"item": "minecraft:iron_block"}, "G": {"item": "minecraft:glass"}, "D": {"item": "minecraft:diamond"},
                "R": {"item": "minecraft:redstone_block"}},
        "result": {"id": f"{MOD}:dna_machine", "count": 1}})
    write_json(RES / "data" / "minecraft" / "tags" / "block" / "mineable" / "pickaxe.json",
               {"replace": False, "values": [f"{MOD}:dna_machine"]})


def build():
    for name, img in (("dna_machine_metal", metal()), ("dna_machine_trim", trim()), ("dna_machine_glass", glass()),
                      ("dna_machine_panel", panel()), ("dna_machine_cable", cable()), ("dna_fluid", fluid())):
        save(img, A / "textures" / "block" / f"{name}.png")
    save(mew_dna_icon(), A / "textures" / "item" / "mew_dna.png")
    save(machine_icon(), A / "textures" / "item" / "dna_machine.png")
    models()
    data()


if __name__ == "__main__":
    build()
