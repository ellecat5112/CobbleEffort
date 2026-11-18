"""Mummymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a tall gaunt mummy wrapped head to foot in grubby bandages bound with black belts, a violet scarf, red
eyes peering from the wrappings, a hooked cane of red-and-white snakes on its head, long black claws, a shotgun held
in one hand and two black horn-spikes on its shoulders. 25 blocks tall.

Front is -z, y is up. 70 units tall; Perfect stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, leather, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a tall gaunt mummy wrapped in grubby bandages and black belts, a violet scarf, red eyes, long black claws, "
        "shoulder horn-spikes and a shotgun")
BASE = {"band": (230, 224, 206), "band_dark": (170, 160, 136), "black": (30, 28, 34), "violet": (110, 70, 150),
        "violet_dark": (54, 30, 80), "eye": (230, 30, 40), "steel": (120, 124, 136), "steel_dark": (50, 54, 64),
        "wood": (140, 90, 50), "red": (200, 40, 40), "white": (240, 240, 240)}
SHINY = {"band": (200, 210, 230), "band_dark": (130, 140, 170), "violet": (60, 140, 90), "violet_dark": (20, 80, 40)}


def P(v):
    return pal(BASE, SHINY, v)


BAND0 = fabric(P, "band", "band_dark", axis="x", period=1.4)


def bandf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs((y % 9.0) - 4.5) < 0.5:
        return tone(p["black"], face), None                                              # black belts
    return BAND0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("mummymon")
    mats = {"skin": bandf, "claw": solid(P, "black")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.75, leg_bulk=0.8, claws=True, name="mummymon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.4, bandf, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 57.4, -2.9, max(sx * 0.6, sx * 1.6), 58.0, -2.8, solid(P, "eye", glow=True))
        spike(m, bd, (sx * 6.4, 51.0, 0.0), (sx * 0.6, 1, -0.1), 1.6, 6.0, solid(P, "black"), tip=0.8)  # horn-spikes
    for j in range(2):                                                                   # snake cane hooks
        sx = 1 if j else -1
        pts = [(sx * 0.6, 60.0, 0), (sx * 0.8, 64.0, 0), (sx * 2.4, 66.0, 0), (sx * 3.4, 64.6, 0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "red" if j else "white"), extend=0.2)
    m.round_box(bd, 0, 0.0, 2.8, 2.8, 50.0, 53.4, fabric(P, "violet", "violet_dark"), cut=1)   # violet scarf
    m.box(bd, 1.0, 34.0, 3.0, 3.0, 52.0, 3.4, fabric(P, "violet", "violet_dark"))
    al = a["arm_left"]                                                                   # shotgun
    h = al["hand"]
    m.box(al["bone"], h[0] - 0.8, h[1] - 4.0, h[2] - 1.0, h[0] + 0.8, h[1] + 1.0, h[2] + 1.0, solid(P, "wood"))
    rod(m, al["bone"], (h[0], h[1] + 1.0, h[2]), (h[0], h[1] + 18.0, h[2] - 2.0), 1, metal(P, "steel", dark="steel_dark"),
        extend=0.2, t2=2)
    return m
