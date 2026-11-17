"""Blitzmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Hybrid warrior of thunder. Navy-blue beetle armour trimmed in gold: a horned helm with a split
V crest over a dark visor, a huge rounded right shoulder plate with a back-swept spike, a gold breastplate and belt of
gold segments, a silver-banded left forearm ending in a crackling fist, navy legs banded gold and pointed gold-toed
boots, with lightning arcing round it. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid
from _digidetail import armour, cutout, local, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a navy-and-gold beetle-armoured warrior of thunder: a horned helm with a split V crest, a huge rounded "
        "shoulder plate, a gold breastplate and belt, a crackling fist and pointed gold-toed boots")
BASE = {"navy": (52, 52, 150), "navy_dark": (20, 20, 70), "navy_light": (120, 120, 210), "gold": (250, 200, 50),
        "gold_dark": (180, 120, 20), "silver": (210, 214, 226), "silver_dark": (110, 114, 128), "visor": (40, 40, 60),
        "eye": (250, 250, 220), "bolt": (255, 250, 140, 200), "bolt_core": (255, 255, 240, 240), "under": (60, 60, 80)}
SHINY = {"navy": (150, 30, 40), "navy_dark": (70, 10, 16), "navy_light": (220, 100, 110), "gold": (220, 224, 236),
         "gold_dark": (130, 134, 150), "bolt": (160, 220, 255, 200)}


def P(v):
    return pal(BASE, SHINY, v)


NAVY = armour(P, "navy", "navy_dark", light="navy_light", trim="gold", trim_w=0.4)
GOLD = armour(P, "gold", "gold_dark")
SILVER = metal(P, "silver", dark="silver_dark")
UNDER = solid(P, "under")


def banded(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y % 5.0 < 1.4:
        return tone(p["gold"], face), None
    return NAVY(x, y, z, face, variant, box=box, **k)


def boltf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    c = p["bolt_core"]
    return c, c[:3]


def zigzag(x, y, z, face, box):
    """A lightning bolt: a zigzag stroke down the plane."""
    u, v, W, H = local(x, y, z, face, box)
    t = v / max(H, 1e-6)
    centre = 0.5 + 0.3 * (((t * 4) % 1) - 0.5) * (1 if int(t * 4) % 2 else -1)
    return abs(u / max(W, 1e-6) - centre) < 0.09


def build():
    m = Model("blitzmon")
    mats = {"skin": UNDER, "chest": GOLD, "abs": NAVY, "pelvis": GOLD, "neck": UNDER, "deltoid": NAVY,
            "upper_arm": SILVER, "forearm": banded, "hand": GOLD, "finger": GOLD, "thigh": NAVY, "knee": GOLD,
            "shin": banded, "calf": NAVY, "foot": NAVY, "toe": GOLD}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.2, leg_bulk=1.15, name="blitzmon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0.0, 3.0, 3.2, 54.0, 61.4, NAVY, cut=1)                            # helm
    m.box(hd, -2.4, 56.4, -3.6, 2.4, 58.2, -3.0, solid(P, "visor"))
    for sx in (-1, 1):
        m.box(hd, sx * 1.2 - 0.5, 57.0, -3.7, sx * 1.2 + 0.5, 57.6, -3.5, solid(P, "eye", glow=True))
        rod(m, hd, (sx * 0.8, 61.0, -1.6), (sx * 4.0, 68.0, -2.4), 2, NAVY, extend=0.3, t2=3)   # split V crest
        spike(m, hd, (sx * 3.0, 58.0, 0), (sx, 0.3, 0.4), 1.6, 2.6, GOLD)
    rod(m, hd, (0, 58.6, -3.4), (0, 63.2, -5.4), 2, GOLD, extend=0.3)                     # nose horn
    # the huge rounded right shoulder plate with a back-swept spike
    ar = a["arm_right"]
    sh = ar["shoulder"]
    dome(m, ar["bone"], (sh[0] - 2.0, 47.0, 0.4), 6.4, 6.0, NAVY, layers=5)
    spike(m, ar["bone"], (sh[0] - 4.0, 51.0, 2.0), (-0.9, 0.5, 0.6), 3.0, 9.0, NAVY, tip=1.2)
    al = a["arm_left"]
    m.round_box(al["bone"], al["shoulder"][0] + 1.0, 0.3, 3.2, 3.0, 46.5, 52.0, NAVY, cut=1)
    # gold belt of segments
    for i in range(10):
        ang = math.radians(i * 36)
        c = (5.4 * math.sin(ang), 33.0, 0.4 - 3.9 * math.cos(ang))
        m.box(bd, c[0] - 1.5, 31.4, c[2] - 0.6, c[0] + 1.5, 34.6, c[2] + 0.6, GOLD,
              rotation=(0, -math.degrees(ang), 0), pivot=c)
    # pointed boots
    for nm in ("leg_left", "leg_right"):
        lg = a[nm]
        an = lg["ankle"]
        spike(m, lg["bone"], (an[0], 1.4, an[2] - 3.0), (0, 0, -1), 3.0, 4.6, GOLD, tip=1.0)
    # lightning: bolt planes round its left fist and down its side
    h = al["hand"]
    for j, ang in enumerate((0, 60, 120)):
        m.box(al["bone"], h[0] - 3.0, h[1] - 8.0, h[2], h[0] + 3.0, h[1] + 8.0, h[2], cutout(zigzag, boltf),
              rotation=(0, ang, 20 * (j - 1)), pivot=(h[0], h[1], h[2]))
    for sx in (-1, 1):
        m.box(bd, sx * 9.0 - 2.0, 14.0, 0.0, sx * 9.0 + 2.0, 30.0, 0.0, cutout(zigzag, boltf),
              rotation=(0, 30 * sx, 0), pivot=(sx * 9.0, 22.0, 0))
    return m
