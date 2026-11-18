"""Mercurymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Olympos XII messenger, a wild crouching warrior wearing a teal dragon-wolf head as a helmet
with a great shaggy green mane streaming back, tan skin stitched with X marks, a fur wrap, a big studded leather
gauntlet on his left arm, a curling teal spiral tendril, purple-and-white clawed boots and a long dagger in his right
hand. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fur, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a wild warrior in a teal dragon-wolf helmet with a shaggy green mane, stitched tan skin, a fur wrap, a studded "
        "leather gauntlet, clawed purple boots and a long dagger")
BASE = {"tan": (220, 170, 130), "tan_dark": (150, 100, 70), "teal": (60, 170, 160), "teal_dark": (20, 90, 90),
        "green": (110, 200, 120), "green_dark": (40, 120, 60), "fur": (230, 220, 200), "fur_dark": (160, 150, 130),
        "leather": (110, 70, 50), "leather_dark": (50, 30, 20), "steel": (220, 224, 236), "steel_dark": (110, 114, 126),
        "violet": (150, 60, 160), "violet_dark": (80, 20, 90), "stitch": (40, 30, 30), "eye": (250, 60, 60),
        "mouth": (150, 20, 40), "tooth": (250, 250, 240)}
SHINY = {"teal": (200, 90, 60), "teal_dark": (110, 40, 20), "green": (240, 200, 90), "green_dark": (170, 120, 30)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN0 = skin(P, "tan", dark="tan_dark")
HELM = armour(P, "teal", "teal_dark", trim="green", trim_w=0.25)
MANE = strands(P, "green", "green_dark")
FUR = fur(P, "fur", "fur_dark", length=1.4)
LEATHER = leather(P, "leather", "leather_dark", stitch="steel")
BOOT = armour(P, "violet", "violet_dark", trim="fur", trim_w=0.3)


def skinf(x, y, z, face, variant, box=None, **k):
    """Tan skin with stitched X marks here and there."""
    p = P(variant)
    cx, cy = round(x / 4.0) * 4.0, round(y / 5.0) * 5.0
    if face in ("north", "south", "east", "west") and (int(cx + cy) % 3 == 0):
        dx, dy = x - cx, y - cy
        if abs(dx) < 0.9 and abs(dy) < 0.9 and (abs(dx - dy) < 0.22 or abs(dx + dy) < 0.22):
            return tone(p["stitch"], face), None
    return SKIN0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("mercurymon")
    mats = {"skin": skinf, "chest": skinf, "abs": skinf, "pelvis": FUR, "neck": skinf, "deltoid": FUR,
            "upper_arm": skinf, "forearm": skinf, "hand": skinf, "finger": skinf, "claw": solid(P, "steel"),
            "thigh": skinf, "knee": BOOT, "shin": BOOT, "calf": BOOT, "foot": BOOT, "talon": solid(P, "steel")}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.05, leg_bulk=1.05, claws=True, talons=True, name="mercurymon")
    bd = a["body"]
    for sx in (-1, 1):                                                                 # fur wrap across the chest
        m.box(bd, min(sx * 0.0, sx * 6.0), 42.0, -4.8, max(sx * 0.0, sx * 6.0), 45.0, -3.6, FUR,
              rotation=(0, 0, sx * 30), pivot=(0, 46.0, -4.0))
    m.round_box(bd, 0, 0.4, 5.4, 4.0, 28.0, 33.0, FUR, cut=1)                          # fur loincloth
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 53.8, 59.0, skinf, cut=1)                        # face under the helm
    m.box(hd, -1.8, 57.0, -3.3, 1.8, 57.8, -3.1, solid(P, "eye", glow=True))
    m.round_box(hd, 0, -1.0, 3.4, 3.8, 58.0, 62.0, HELM, cut=1)                         # dragon-wolf helmet
    m.round_box(hd, 0, -6.4, 2.4, 2.8, 58.4, 61.0, HELM, cut=1)                         # helm snout
    m.box(hd, -2.0, 57.6, -9.0, 2.0, 58.4, -3.8, HELM)                                  # lower helm jaw
    for j in range(4):
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.8, 58.4, -8.6 + j * 1.2), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.6, sx * 2.6), 60.0, -6.6, max(sx * 1.6, sx * 2.6), 60.8, -6.4, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.4, 61.6, -2.0), (sx * 0.5, 0.7, 0.6), 1.4, 5.0, HELM, tip=0.8)          # helm horns
    mb = m.bone("mane", hd, (0, 61, 2))
    for row in range(3):                                                                # great shaggy green mane
        for i in range(9):
            ang = math.radians(-80 + i * 20)
            spike(m, mb, (3.0 * math.sin(ang), 61.0 - row * 3.0, 1.0 + row),
                  (math.sin(ang) * 0.8, 0.4 - row * 0.5, 1.0), 2.0, 14.0 - row * 2.0 - abs(i - 4) * 0.8, MANE, tip=0.8)
    al = a["arm_left"]                                                                  # studded leather gauntlet
    el, wr = al["elbow"], al["wrist"]
    rod(m, al["bone"], el, wr, 6, LEATHER, extend=0.8)
    for j in range(3):
        spike(m, al["bone"], ((el[0] + wr[0]) / 2 + 2.8, el[1] - 3.0 - j * 2.4, -0.6), (1, 0, 0), 1.0, 1.6,
              solid(P, "steel"), tip=0.8)
    for j in range(8):                                                                  # spiral tendril
        ang = j * 0.9
        p0 = (wr[0] + 4.0 + 2.0 * math.cos(ang) * (1 - j / 10), wr[1] + 6.0 + j * 1.2, wr[2] + 2.0 * math.sin(ang))
        p1 = (wr[0] + 4.0 + 2.0 * math.cos(ang + 0.9) * (1 - (j + 1) / 10), wr[1] + 7.2 + j * 1.2,
              wr[2] + 2.0 * math.sin(ang + 0.9))
        rod(m, al["bone"], p0, p1, 1, solid(P, "teal"), extend=0.2)
    ar = a["arm_right"]                                                                 # long dagger
    h = ar["hand"]
    rod(m, ar["bone"], (h[0], h[1], h[2] - 1.0), (h[0] - 1.0, h[1] - 3.0, h[2] - 3.0), 1, LEATHER, extend=0.3)
    m.box(ar["bone"], h[0] - 2.4, h[1] - 3.6, h[2] - 4.0, h[0] + 0.4, h[1] - 2.8, h[2] - 3.0, metal(P, "steel"))
    rod(m, ar["bone"], (h[0] - 1.0, h[1] - 3.2, h[2] - 3.5), (h[0] - 8.0, h[1] - 14.0, h[2] - 8.0), 1,
        metal(P, "steel", dark="steel_dark"), extend=0.2, t2=2)
    return m
