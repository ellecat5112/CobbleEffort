"""Flamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
Legendary Warrior of flame's child. A small brown-skinned imp-boy with spiky blazing red-orange hair, big green eyes,
a sly grin, a black collar, red shorts with a cream belt, oversized fists, bare feet and a flame-tipped tail. Child
stage, 1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import cutout, fabric, flame_inside, local, skin, solid, strands
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = ("a small brown imp-boy with spiky blazing red hair, big green eyes, a black collar, red shorts, oversized fists "
        "and a flame-tipped tail")
BASE = {"skin": (170, 110, 70), "skin_dark": (110, 66, 40), "hair": (240, 80, 30), "hair_dark": (180, 30, 14),
        "red": (210, 40, 40), "red_dark": (130, 14, 18), "cream": (240, 226, 180), "black": (30, 28, 30),
        "eye": (70, 200, 90), "pupil": (16, 16, 20), "white": (250, 250, 250), "mouth": (110, 30, 30),
        "fire": (255, 170, 40, 220), "fire_core": (255, 245, 180, 240)}
SHINY = {"hair": (80, 160, 250), "hair_dark": (30, 80, 200), "red": (40, 80, 200), "red_dark": (14, 30, 120)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "skin", dark="skin_dark")
HAIR = strands(P, "hair", "hair_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.8, y - 22.6)
            if d < 0.6:
                return tone(p["pupil"], face), None
            if d < 1.4:
                return tone(p["eye"], face), None
        if abs(y - 19.8) < 0.35 and abs(x - 0.4) < 1.6:
            return tone(p["mouth"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def build():
    m = Model("flamon")
    top = m.bone("flamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    m.round_box(bd, 0, 0, 3.0, 2.2, 9.0, 13.0, fabric(P, "red", "red_dark"), cut=1)          # shorts
    m.round_box(bd, 0, 0, 3.1, 2.3, 12.6, 13.6, solid(P, "cream"), cut=1)                    # belt
    m.round_box(bd, 0, 0, 2.8, 2.0, 13.4, 17.6, SKIN, cut=1)                                 # torso
    m.round_box(bd, 0, 0, 2.0, 2.0, 17.2, 18.4, solid(P, "black"), cut=1)                    # collar
    hd = m.bone("head", bd, (0, 18, 0))
    m.round_box(hd, 0, 0, 4.0, 3.6, 18.0, 25.6, headf, cut=2)
    for sx in (-1, 1):
        spike(m, hd, (sx * 4.0, 23.0, 0.4), (sx, 0.3, 0.2), 1.0, 2.0, SKIN, tip=0.3)          # pointed ears
    for i in range(11):                                                                     # spiky blazing hair
        ang = math.radians(-100 + i * 20)
        spike(m, hd, (2.6 * math.sin(ang), 25.0, 1.0 + 1.6 * math.cos(ang)),
              (math.sin(ang) * 0.6, 1.0, 0.5 + 0.3 * math.cos(ang)), 1.8, 4.6 + (i % 3), HAIR, tip=0.4)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                     # oversized fists
        ab = m.bone(nm, bd, (sx * 3.0, 16.6, 0))
        rod(m, ab, (sx * 3.0, 16.6, 0), (sx * 4.6, 11.4, -0.6), 1, SKIN, extend=0.3, t2=1)
        m.round_box(ab, sx * 5.0, -0.8, 2.0, 2.0, 7.6, 11.6, SKIN, cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6, 9.0, 0))
        rod(m, lg, (sx * 1.6, 9.0, 0), (sx * 1.8, 1.4, 0), 1, SKIN, extend=0.3, t2=1)
        m.round_box(lg, sx * 1.8, -0.8, 1.2, 2.0, 0.0, 1.4, SKIN, cut=0)
    tb = m.bone("tail", bd, (0, 10, 2))
    rod(m, tb, (0, 10.0, 2.0), (0, 13.0, 7.0), 1, SKIN, extend=0.3)
    for ang in (0, 90):
        m.box(tb, -1.5, 13.0, 7.0, 1.5, 17.0, 7.0, cutout(flame_inside(3, 0.1, 5), firef), rotation=(0, ang, 0),
              pivot=(0, 13.0, 7.0))
    return m
