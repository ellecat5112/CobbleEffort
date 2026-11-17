"""Captain Hookmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the pirate captain. A lean pirate in a black tricorn hat with a skull-and-crossbones,
long grey hair, a black greatcoat with gold trim swept back like a cape, a red scarf, a white shirt and belted brown
trousers, boots, a steel cannon for a left arm, and a huge steel anchor-hook on a chain in the right hand.
25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import fabric, leather, local, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean pirate in a skull tricorn and black gold-trimmed greatcoat, a red scarf, a steel cannon arm and a huge "
        "anchor-hook on a chain")
BASE = {"coat": (34, 32, 40), "coat_dark": (14, 14, 18), "gold": (230, 186, 60), "red": (200, 30, 40),
        "red_dark": (120, 10, 20), "shirt": (236, 232, 222), "shirt_dark": (190, 184, 170), "brown": (140, 90, 50),
        "brown_dark": (80, 50, 24), "steel": (200, 204, 216), "steel_dark": (90, 94, 106), "skin": (220, 180, 150),
        "skin_dark": (170, 130, 100), "hair": (190, 190, 200), "hair_dark": (130, 130, 140), "white": (250, 250, 250),
        "eye": (240, 60, 40)}
SHINY = {"coat": (130, 20, 30), "coat_dark": (70, 8, 14), "red": (40, 40, 48), "red_dark": (16, 16, 20)}


def P(v):
    return pal(BASE, SHINY, v)


COAT = fabric(P, "coat", "coat_dark", axis="y", period=3.0)
SHIRT = fabric(P, "shirt", "shirt_dark", axis="y", period=1.6)
TROUSER = fabric(P, "brown", "brown_dark", axis="y", period=2.2)
STEEL = metal(P, "steel", dark="steel_dark")


def hatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 1.4 and 61.4 < y < 64.0:          # skull and crossbones
        if (abs(x) < 0.9 and y > 62.4) or abs(abs(x) - (y - 61.4) * 0.6) < 0.25:
            return tone(p["white"], face), None
    u, v, W, H = local(x, y, z, face, box)
    if v < 0.4 or v > H - 0.4:
        return tone(p["gold"], face), None
    return COAT(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("captainhookmon")
    mats = {"skin": skin(P, "skin", dark="skin_dark"), "chest": SHIRT, "abs": SHIRT, "pelvis": leather(P, "brown", "brown_dark"),
            "deltoid": COAT, "upper_arm": COAT, "forearm": COAT, "thigh": TROUSER, "knee": TROUSER, "shin": leather(P, "brown_dark", "coat"),
            "calf": leather(P, "brown_dark", "coat"), "foot": leather(P, "brown_dark", "coat"),
            "toe": leather(P, "brown_dark", "coat")}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.0, leg_bulk=1.0, name="captainhookmon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.4, 60.4, skin(P, "skin", dark="skin_dark"), cut=1)
    m.box(hd, -2.2, 57.6, -3.0, 2.2, 58.4, -2.8, solid(P, "coat"))                       # shadowed brow
    m.box(hd, 0.6, 57.8, -3.1, 1.6, 58.2, -3.0, solid(P, "eye", glow=True))
    for i in range(8):                                                                   # long grey hair
        ang = math.radians(-120 + i * 34)
        rod(m, hd, (2.4 * math.sin(ang), 59.6, 2.4 * math.cos(ang) * -1 + 0.6),
            (3.4 * math.sin(ang), 52.0, 2.0 + abs(math.cos(ang))), 1, strands(P, "hair", "hair_dark"), extend=0.3, t2=2)
    hat = m.bone("hat", hd, (0, 60, 0))                                                  # tricorn
    m.round_box(hat, 0, 0.0, 6.0, 5.0, 60.2, 61.2, hatf, cut=2)
    m.round_box(hat, 0, 0.0, 3.4, 3.2, 61.0, 64.6, hatf, cut=1)
    for sx in (-1, 1):
        m.box(hat, min(sx * 3.0, sx * 6.6), 60.8, -1.0, max(sx * 3.0, sx * 6.6), 63.4, 1.0, hatf,
              rotation=(0, 0, -sx * 20), pivot=(sx * 3.0, 61.0, 0))
    m.round_box(bd, 0, -0.4, 2.8, 2.8, 51.0, 53.6, fabric(P, "red", "red_dark"), cut=1)     # red scarf
    rod(m, bd, (1.0, 52.0, -3.0), (3.0, 46.0, -4.0), 1, fabric(P, "red", "red_dark"), extend=0, t2=2)
    cb = m.bone("cap", bd, (0, 52, 3))                                                   # the greatcoat
    cape(m, cb, 52.0, 18.0, 44.0, COAT, z=4.0, flare=0.9, panels=8, sweep=(0, 8), seed=5)
    for sx in (-1, 1):
        m.box(bd, min(sx * 4.4, sx * 6.4), 28.0, -4.0, max(sx * 4.4, sx * 6.4), 51.0, -3.4, COAT,
              rotation=(-4, sx * 16, 0), pivot=(sx * 5.0, 51.0, -3.6))
        m.box(bd, min(sx * 4.4, sx * 4.9), 28.0, -4.2, max(sx * 4.4, sx * 4.9), 51.0, -4.0, solid(P, "gold"),
              rotation=(-4, sx * 16, 0), pivot=(sx * 5.0, 51.0, -3.6))
    al = a["arm_left"]                                                                   # the cannon arm
    el, h = al["elbow"], al["hand"]
    m.round_box(al["bone"], h[0], h[2], 2.6, 2.6, h[1] - 6.0, el[1] - 2.0, STEEL, cut=1)
    m.round_box(al["bone"], h[0], h[2], 1.4, 1.4, h[1] - 6.4, h[1] - 5.6, solid(P, "coat"), cut=1)
    ar = a["arm_right"]                                                                  # anchor-hook on a chain
    h = ar["hand"]
    hb = m.bone("anchor", ar["bone"], h)
    for j in range(6):
        y0 = h[1] - 2.0 - j * 2.2
        m.box(hb, h[0] - 0.5, y0 - 1.6, h[2] - 0.5, h[0] + 0.5, y0, h[2] + 0.5, STEEL,
              rotation=(0, 90 * (j % 2), 0), pivot=(h[0], y0, h[2]))
    shank_top, base = (h[0], h[1] - 14.0, h[2]), (h[0], h[1] - 30.0, h[2] - 2.0)
    rod(m, hb, shank_top, base, 2, STEEL, extend=0)
    for sx in (-1, 1):
        rod(m, hb, base, (h[0] + sx * 6.0, base[1] + 5.0, h[2] - 2.0), 2, STEEL, extend=0.4)
        spike(m, hb, (h[0] + sx * 6.0, base[1] + 5.0, h[2] - 2.0), (0, 1, 0), 1.6, 3.0, STEEL)
    m.box(hb, h[0] - 4.0, shank_top[1] - 1.0, h[2] - 0.6, h[0] + 4.0, shank_top[1], h[2] + 0.6, STEEL)
    spike(m, hb, base, (0, -1, 0), 2.0, 3.0, STEEL)
    return m
