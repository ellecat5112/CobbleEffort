"""Murasamemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a cursed swordsman beast-man: a lean dark-grey body marked with glowing blue tattoos, a wolfish
head with long swept-back white hair and pointed ears, baggy dark trousers belted with a gold buckle, black sleeves
and boots with gold bands, clawed feet, a long thin tail, and a gigantic black sword with a violet-edged blade
decorated with gold flame marks slung over its shoulder. 25 blocks tall.

Front is -z, y is up. 70 units tall (the sword); Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, leather, local, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a lean dark-grey beast-man with glowing blue tattoos, long white hair, baggy trousers, gold-banded black boots, "
        "a thin tail and a gigantic black sword over its shoulder")
BASE = {"grey": (90, 92, 104), "grey_dark": (44, 46, 56), "tattoo": (90, 170, 250), "hair": (236, 236, 240),
        "hair_dark": (170, 170, 180), "cloth": (70, 64, 74), "cloth_dark": (30, 26, 34), "gold": (230, 190, 70),
        "black": (30, 28, 34), "violet": (130, 80, 190), "eye": (250, 220, 60), "claw": (240, 236, 220)}
SHINY = {"grey": (190, 160, 120), "grey_dark": (120, 90, 50), "tattoo": (240, 90, 70), "violet": (230, 160, 60)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN0 = skin(P, "grey", dark="grey_dark")
CLOTH = fabric(P, "cloth", "cloth_dark")
BLACK = leather(P, "black", "black", stitch="gold")


def skinf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs(math.sin(x * 1.1 + y * 0.6) + math.cos(y * 0.9 - z * 0.7)) < 0.12:
        return p["tattoo"], p["tattoo"]
    return SKIN0(x, y, z, face, variant, box=box, **k)


def bladef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if box is None or face in ("up", "down"):
        return tone(p["black"], face), None
    u, v, W, H = local(x, y, z, face, box)
    across, along = (v / max(H, 1e-6), u) if W >= H else (u / max(W, 1e-6), v)
    if across < 0.14 or across > 0.86:
        return tone(p["violet"], face), None
    if abs((along % 6.0) - 3.0) < 0.9 and abs(across - 0.5) < 0.18:
        return tone(p["gold"], face), None
    return tone(p["black"], face), None


def build():
    m = Model("murasamemon")
    mats = {"skin": skinf, "chest": skinf, "abs": skinf, "pelvis": CLOTH, "neck": skinf, "deltoid": skinf,
            "upper_arm": skinf, "forearm": BLACK, "hand": skinf, "finger": skinf, "claw": solid(P, "claw"),
            "thigh": CLOTH, "knee": CLOTH, "shin": BLACK, "calf": BLACK, "foot": skinf, "talon": solid(P, "claw")}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.0, leg_bulk=1.05, claws=True, talons=True, digitigrade=True,
                 name="murasamemon")
    bd = a["body"]
    for sx in (-1, 1):                                                                   # baggy trousers
        lg = a["leg_left" if sx > 0 else "leg_right"]["bone"]
        m.round_box(lg, sx * 3.2, -0.6, 3.4, 3.6, 18.0, 30.0, CLOTH, cut=1)
    m.round_box(bd, 0, 0.4, 5.2, 3.8, 31.0, 33.0, leather(P, "black", "black"), cut=1)  # belt
    m.box(bd, -1.2, 31.2, -4.3, 1.2, 32.8, -4.1, solid(P, "gold"))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.6, 3.0, 54.0, 60.0, skinf, cut=1)
    m.round_box(hd, 0, -4.0, 1.6, 1.6, 54.4, 57.0, SKIN0, cut=1)                          # wolfish muzzle
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.0), 57.6, -3.7, max(sx * 0.8, sx * 2.0), 58.4, -3.5, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.4, 59.0, 0.6), (sx * 0.5, 1, 0.4), 1.4, 4.0, SKIN0, tip=0.8)  # pointed ears
    for i in range(9):                                                                   # long swept white hair
        ang = math.radians(-70 + i * 17.5)
        rod(m, hd, (2.4 * math.sin(ang), 59.6, 1.0), (5.0 * math.sin(ang), 46.0 - abs(i - 4), 8.0), 1,
            strands(P, "hair", "hair_dark"), extend=0.2, t2=2)
    tb = m.bone("tail", bd, (0, 31, 3))                                                  # thin tail
    pts = [(0, 31.0, 3.0), (3.0, 24.0, 9.0), (6.0, 18.0, 12.0), (8.0, 16.0, 16.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, SKIN0, extend=0.2)
    ar = a["arm_right"]                                                                  # gigantic sword
    h = ar["hand"]
    rod(m, ar["bone"], (h[0], h[1] - 3.0, h[2]), (h[0], h[1] + 2.0, h[2]), 1, solid(P, "black"), extend=0.2)
    m.box(ar["bone"], h[0] - 2.4, h[1] + 2.0, h[2] - 1.0, h[0] + 2.4, h[1] + 3.0, h[2] + 1.0, solid(P, "gold"))
    m.box(ar["bone"], h[0] - 3.4, h[1] + 3.0, h[2] - 0.6, h[0] + 3.4, h[1] + 44.0, h[2] + 0.6, bladef,
          rotation=(0, 0, -50), pivot=(h[0], h[1] + 2.5, h[2]))
    return m
