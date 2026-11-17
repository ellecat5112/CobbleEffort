"""Buraimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the ronin eagle. A lean bird-man warrior with tawny feathers and a long white beard, a battered
woven straw hat, a red-and-gold flame-patterned hakama with a gold-trimmed robe, great brown wings, taloned bird
feet, and two long katanas, one drawn in each hand. 25 blocks tall.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import dome, humanoid
from _digidetail import fabric, feathers, local, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean ronin eagle-man with tawny feathers, a long white beard, a battered straw hat, a red flame-patterned "
        "hakama, great brown wings and a katana in each hand")
BASE = {"tawny": (200, 150, 90), "tawny_dark": (130, 80, 40), "tawny_light": (240, 200, 140), "beard": (240, 236, 226),
        "beard_dark": (180, 170, 156), "straw": (200, 160, 90), "straw_dark": (130, 96, 40), "red": (190, 40, 40),
        "red_dark": (110, 14, 20), "gold": (240, 190, 60), "flame": (250, 170, 40), "wing": (160, 100, 50),
        "wing_dark": (90, 50, 20), "steel": (214, 218, 228), "steel_dark": (110, 114, 128), "talon": (200, 120, 90),
        "hilt": (40, 40, 50), "eye": (250, 200, 60), "pupil": (30, 20, 10), "beak": (240, 200, 80)}
SHINY = {"tawny": (110, 110, 130), "tawny_dark": (60, 60, 76), "tawny_light": (180, 180, 200), "red": (40, 80, 170),
         "red_dark": (14, 34, 100), "wing": (70, 70, 90), "wing_dark": (30, 30, 40)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "tawny", "tawny_dark", size=(1.2, 2.0), tip="tawny_light")
STEEL = metal(P, "steel", dark="steel_dark")


def hakamaf(x, y, z, face, variant, box=None, **k):
    """Red hakama with gold flame tongues licking up from the hem."""
    p = P(variant)
    fl = 4.0 + 3.0 * abs(math.sin(x * 0.9 + z * 0.9))
    if y < 12.0 + fl and y > 10.0 + fl * 0.6 and face not in ("up", "down"):
        return tone(p["flame"], face), None
    return fabric(P, "red", "red_dark", axis="y", period=2.0)(x, y, z, face, variant, box=box, **k)


def strawf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (math.atan2(x, z) * 6 + math.hypot(x, z) * 0.6) % 1
    return tone(p["straw_dark"] if t < 0.22 else p["straw"], face), None


def katana(m, bone, h, d):
    n = math.sqrt(sum(c * c for c in d))
    u = tuple(c / n for c in d)
    rod(m, bone, tuple(a - b * 3.0 for a, b in zip(h, u)), tuple(a + b * 1.0 for a, b in zip(h, u)), 1,
        solid(P, "hilt"), extend=0)
    m.box(bone, h[0] - 1.0, h[1] - 1.0, h[2] - 1.0, h[0] + 1.0, h[1] + 1.0, h[2] + 1.0, solid(P, "gold"))
    rod(m, bone, tuple(a + b * 1.0 for a, b in zip(h, u)), tuple(a + b * 24.0 for a, b in zip(h, u)), 1, STEEL,
        extend=0, t2=1)


def build():
    m = Model("buraimon")
    mats = {"skin": FEATH, "chest": fabric(P, "red", "red_dark"), "abs": fabric(P, "red", "red_dark"),
            "pelvis": solid(P, "gold"), "thigh": hakamaf, "knee": hakamaf, "shin": hakamaf, "calf": hakamaf,
            "foot": solid(P, "talon"), "talon": solid(P, "talon"), "hand": FEATH, "finger": FEATH}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.1, leg_bulk=1.15, digitigrade=True, talons=True, name="buraimon",
                 hand_pose="fist")
    bd = a["body"]
    for sx in (-1, 1):                                                                  # robe lapels, gold trim
        x0, x1 = sorted((sx * 0.4, sx * 5.4))
        m.box(bd, x0, 34.0, -4.9, x1, 51.0, -4.4, solid(P, "gold"), rotation=(0, 0, sx * 18), pivot=(sx * 0.4, 51, 0))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.4, 61.0, FEATH, cut=1)
    spike(m, hd, (0, 57.6, -3.2), (0, -0.5, -1), 1.8, 3.0, solid(P, "beak"), tip=0.5)  # hooked beak
    for sx in (-1, 1):
        m.box(hd, sx * 1.3 - 0.5, 58.6, -3.3, sx * 1.3 + 0.5, 59.2, -3.1, solid(P, "eye", glow=True))
    beard = strands(P, "beard", "beard_dark")
    for i in range(7):                                                                  # the long white beard
        x = -2.4 + i * 0.8
        rod(m, hd, (x, 56.4, -2.6), (x * 1.2, 45.0 + abs(x), -4.6), 1, beard, extend=0.3, t2=2)
    hat = m.bone("hat", hd, (0, 61, 0))                                                 # battered straw hat
    for i, (r, y0, y1) in enumerate(((8.0, 60.6, 61.6), (4.6, 61.6, 63.0), (3.2, 63.0, 64.4))):
        m.round_box(hat, 0, 0, r, r, y0, y1, strawf, cut=max(1, round(r * 0.35)))
    for side in (1, -1):                                                                # great brown wings
        feather_wing(m, bd, (side * 3.0, 48.0, 3.6), 20.0, 10.0, 3, feathers(P, "wing", "wing_dark", size=(1.6, 3.0)),
                     side=side, sweep=30, droop=0.4)
    katana(m, a["arm_right"]["bone"], a["arm_right"]["hand"], (-0.6, 0.2, -1))
    katana(m, a["arm_left"]["bone"], a["arm_left"]["hand"], (0.5, -0.3, -0.8))
    return m
