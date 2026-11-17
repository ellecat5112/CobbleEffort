"""Dark Superstarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the fallen star. A big five-pointed star body in deep blue and violet with bevelled
facets, enormous red boxing gloves with silver cuffs and studs, chunky red high-top boots with black soles and steel
star buckles, and torn black ribbons streaming from behind it. 25 blocks tall.

Front is -z, y is up. 50 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, cutout, leather, local, metal, noise2, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(25, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a big deep-blue five-pointed star with enormous red boxing gloves, chunky red high-top boots with star buckles "
        "and torn black ribbons streaming behind it")
BASE = {"blue": (50, 60, 150), "blue_dark": (20, 20, 70), "blue_light": (130, 150, 230), "violet": (90, 50, 140),
        "red": (210, 30, 40), "red_dark": (120, 10, 20), "red_light": (255, 120, 120), "black": (30, 30, 34),
        "steel": (210, 214, 226), "steel_dark": (110, 114, 128), "eye": (250, 230, 80)}
SHINY = {"blue": (230, 190, 50), "blue_dark": (150, 100, 10), "blue_light": (255, 240, 160), "violet": (220, 140, 40)}


def P(v):
    return pal(BASE, SHINY, v)


STAR = armour(P, "blue", "blue_dark", light="blue_light", trim="violet", trim_w=0.4)
GLOVE = armour(P, "red", "red_dark", light="red_light")
STEEL = metal(P, "steel", dark="steel_dark")


def ribbonf(x, y, z, face, variant, box=None, **k):
    return tone(P(variant)["black"], face), None


def torn(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return noise2(u * 0.8, v * 0.3, 7) > 0.28


def starf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 2.4) < 0.9 and abs(y - 36.0 - sx * 0.0) < 1.2 and abs(x - sx * 2.4) < 1.6 - abs(y - 36.0):
                return p["eye"], p["eye"]
    return STAR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("darksuperstarmon")
    top = m.bone("darksuperstarmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    c = (0, 32.0, 0)
    m.round_box(bd, 0, 0, 5.6, 4.0, 27.0, 37.0, starf, cut=2)                            # star core
    for i in range(5):                                                                   # five tapering points
        ang = math.radians(90 + i * 72)
        for j, (r0, w) in enumerate(((5.0, 8.0), (8.4, 5.6), (11.4, 3.4), (13.8, 1.6))):
            px, py = c[0] + math.cos(ang) * r0, c[1] + math.sin(ang) * r0
            m.box(bd, px - w / 2, py - 1.8, -3.4 + j * 0.7, px + w / 2, py + 1.8, 3.4 - j * 0.7, starf,
                  rotation=(0, 0, math.degrees(ang) - 90), pivot=(px, py, 0))
    hd = m.bone("head", bd, (0, 39, 0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # boxing gloves
        ab = m.bone(nm, bd, (sx * 9.0, 32.0, 0))
        rod(m, ab, (sx * 7.0, 32.0, 0), (sx * 13.0, 30.0, -2.0), 2, STAR, extend=0.4)
        m.round_box(ab, sx * 13.6, -2.0, 3.0, 3.0, 27.0, 31.0, STEEL, cut=1)             # cuff
        m.round_box(ab, sx * 16.0, -3.0, 5.0, 5.0, 26.0, 37.0, GLOVE, cut=2)
        m.round_box(ab, sx * 16.0, -8.6, 3.0, 1.6, 30.0, 35.0, GLOVE, cut=1)              # knuckles
        for j in range(3):
            m.round_box(ab, sx * (12.0 + j * 2.4), -3.0, 0.8, 0.8, 36.6, 38.0, STEEL, cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                  # high-top boots
        lg = m.bone(nm, top, (sx * 4.0, 22.0, 0))
        rod(m, lg, (sx * 3.0, 26.0, 0), (sx * 5.0, 14.0, 0), 2, STAR, extend=0.4)
        m.round_box(lg, sx * 5.0, 0, 3.6, 3.6, 4.0, 15.0, GLOVE, cut=1)
        m.round_box(lg, sx * 5.0, -2.4, 3.8, 6.0, 0.0, 4.0, GLOVE, cut=1)
        m.box(lg, sx * 5.0 - 3.8, 0.0, -8.4, sx * 5.0 + 3.8, 1.4, 3.6, solid(P, "black"))   # sole
        m.round_box(lg, sx * 5.0, -0.2, 3.9, 3.9, 13.0, 15.0, STEEL, cut=1)
        for j in range(4):                                                               # laces
            m.box(lg, sx * 5.0 - 1.6, 5.0 + j * 2.2, -3.8, sx * 5.0 + 1.6, 5.6 + j * 2.2, -3.4, solid(P, "black"))
        for i in range(5):                                                               # star buckle
            ang = math.radians(90 + i * 72)
            x0, x1 = sorted((sx * 8.6, sx * 9.2))
            m.box(lg, x0, 9.0 + math.sin(ang) * 1.2 - 0.4, math.cos(ang) * 1.2 - 0.4, x1,
                  9.0 + math.sin(ang) * 1.2 + 0.4, math.cos(ang) * 1.2 + 0.4, STEEL)
    for i in range(4):                                                                   # torn ribbons
        rb = m.bone("ribbon_%d" % i, bd, (-3.0 + i * 2.0, 38.0, 3.4))
        x0 = -3.0 + i * 2.0
        m.box(rb, x0 - 0.8, 38.0, 3.6, x0 + 0.8, 38.0, 22.0 + i * 3.0, cutout(torn, ribbonf),
              rotation=(-20 + i * 8, (i - 1.5) * 18, 0), pivot=(x0, 38.0, 3.4))
    return m
