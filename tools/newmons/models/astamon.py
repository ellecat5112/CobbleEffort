"""Astamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a demon lord dressed like a gangster. A dark helm with a skull mask and a mane of shaggy grey hair,
a long tattered coat of red and grey over a violet pinstripe suit, a red scarf, small violet bat wings at its back,
pointed shoes and a drum-magazine submachine gun. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digibody import humanoid
from _digidetail import cutout, fabric, local, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a gangster demon lord: a skull-masked helm with shaggy grey hair, a long tattered red-and-grey coat over a "
        "violet pinstripe suit, small bat wings and a drum-magazine submachine gun")
BASE = {"suit": (80, 70, 150), "suit_dark": (40, 34, 90), "stripe": (150, 140, 210), "coat": (190, 60, 50),
        "coat_dark": (110, 26, 20), "grey": (190, 190, 196), "grey_dark": (120, 120, 130), "skull": (230, 226, 216),
        "black": (30, 30, 36), "gun": (70, 66, 64), "gun_dark": (30, 28, 28), "wood": (120, 70, 40),
        "wing": (130, 60, 170, 230), "eye": (255, 60, 60)}
SHINY = {"suit": (40, 40, 50), "suit_dark": (16, 16, 22), "stripe": (200, 60, 60), "coat": (40, 90, 170),
         "coat_dark": (16, 40, 100)}


def P(v):
    return pal(BASE, SHINY, v)


COAT = fabric(P, "coat", "coat_dark", axis="y", period=2.6)
HAIR = strands(P, "grey", "grey_dark")
GUN = metal(P, "gun", dark="gun_dark", streak=2.0)


def suitf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if (u % 1.6) < 0.22 and face not in ("up", "down"):
        return tone(p["stripe"], face), None
    return fabric(P, "suit", "suit_dark", axis="y", period=3.0)(x, y, z, face, variant, box=box, **k)


def coatf(x, y, z, face, variant, box=None, **k):
    """The tattered coat: red with grey panels, a ragged hem cut out."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if (box.lo[0] + u) % 6.0 < 2.0:
        return fabric(P, "grey", "grey_dark", axis="y")(x, y, z, face, variant, box=box, **k)
    return COAT(x, y, z, face, variant, box=box, **k)


def torn(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.12 * abs(math.sin((box.lo[0] + u) * 1.9)) + 0.05 * abs(math.sin(u * 4.3))


def build():
    m = Model("astamon")
    mats = {"skin": suitf, "chest": suitf, "abs": suitf, "pelvis": suitf, "neck": solid(P, "black"),
            "deltoid": coatf, "upper_arm": coatf, "forearm": coatf, "hand": solid(P, "black"),
            "finger": solid(P, "black"), "thigh": suitf, "knee": suitf, "shin": suitf, "calf": suitf,
            "foot": solid(P, "black"), "toe": solid(P, "black")}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=1.0, leg_bulk=0.9, name="astamon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.6, 60.6, solid(P, "black"), cut=1)
    m.box(hd, -1.8, 54.4, -3.2, 1.8, 58.4, -2.6, solid(P, "skull"))                      # skull mask
    for sx in (-1, 1):
        m.box(hd, sx * 0.9 - 0.5, 57.0, -3.3, sx * 0.9 + 0.5, 57.8, -3.1, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.8, 60.4, 0), (sx * 0.4, 1, 0.2), 1.2, 3.0, solid(P, "black"))    # ears
    hr = m.bone("mane", hd, (0, 58, 1))
    for i in range(16):                                          # shaggy grey mane
        ang = math.radians(-120 + i * 16)
        base = (2.4 * math.sin(ang), 58.0, -2.4 * math.cos(ang) * 0.6 + 0.6)
        tip = (5.0 * math.sin(ang), 48.0 + (i % 3) * 2, -3.0 * math.cos(ang) * 0.6 + 2.6)
        rod(m, hr, base, tip, 2, HAIR, extend=0.3)
    sk = m.bone("skirt", bd, (0, 50, 0))
    for i in range(10):                                          # the long tattered coat
        ang = math.radians(-150 + i * 33)
        c = (5.2 * math.sin(ang), 50.0, -4.4 * math.cos(ang))
        if math.cos(ang) < -0.75:
            continue
        m.box(sk, c[0] - 2.0, 6.0, c[2], c[0] + 2.0, 50.0, c[2] + 0.8, cutout(torn, coatf),
              rotation=(-8 * math.cos(ang), -math.degrees(ang), 0), pivot=c)
    m.box(bd, -3.0, 46.0, -5.0, 3.0, 51.0, -4.0, fabric(P, "coat", "coat_dark"))          # red scarf
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        wb = m.bone(nm, bd, (sx * 3.0, 48.0, 4.6))
        bat_wing(m, wb, (sx * 3.0, 48.0, 4.6), 12.0, 8.0, 3, solid(P, "black"),
                 cutout(lambda *q: True, lambda x, y, z, f, variant=None, box=None, **k: (P(variant)["wing"], None)),
                 side=sx)
    ar = a["arm_right"]                                          # the submachine gun
    h = ar["hand"]
    gb = m.bone("gun", ar["bone"], h)
    m.box(gb, h[0] - 0.8, h[1] - 1.0, h[2] - 12.0, h[0] + 0.8, h[1] + 1.4, h[2] + 4.0, GUN)
    rod(m, gb, (h[0], h[1] + 0.2, h[2] - 12.0), (h[0], h[1] + 0.2, h[2] - 18.0), 1, GUN, extend=0)
    m.round_box(gb, h[0], h[2] - 5.0, 1.2, 2.6, h[1] - 4.0, h[1] - 0.8, GUN, cut=1)       # drum magazine
    m.box(gb, h[0] - 0.6, h[1] - 3.0, h[2] + 4.0, h[0] + 0.6, h[1] + 1.0, h[2] + 8.0, solid(P, "wood"))
    return m
