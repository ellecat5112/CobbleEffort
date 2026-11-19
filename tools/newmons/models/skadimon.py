"""Skadimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the snow goddess on her cloud: a round royal-blue robed figure with gold trim and a white bow, riding a
great white cloud, a glass snow-globe dome for a head with a little skull inside and a star on top, puffed violet
sleeves and white gloves, a long ice-crystal wand, diamond-patterned legs in blue boots on great curved ice skate
blades, and long blue ribbons trailing. 35 blocks.

Front is -z, y is up. 56 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, gem, metal, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a snow goddess in a royal-blue robe riding a white cloud, a snow-globe dome head, an ice-crystal wand and curved ice skate blades"
BASE = {"blue": (50, 60, 170), "blue_dark": (20, 24, 90), "violet": (120, 80, 190), "gold": (236, 200, 80),
        "white": (248, 250, 255), "white_dark": (200, 210, 230), "ice": (150, 220, 250), "glass": (210, 240, 255, 150),
        "skull": (240, 240, 236), "black": (30, 30, 36), "lilac": (190, 170, 230)}
SHINY = {"blue": (180, 50, 90), "blue_dark": (100, 20, 50), "violet": (240, 150, 90)}


def P(v):
    return pal(BASE, SHINY, v)


ROBE = fabric(P, "blue", "blue_dark", axis="y", period=3.0)


def legf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["violet"] if (int(y * 0.8 + x * 0.8) + int(y * 0.8 - x * 0.8)) % 2 else p["lilac"], face), None


def build():
    m = Model("skadimon")
    top = m.bone("skadimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    for c, r in (((0, 22.0, 0), 12.0), ((-10.0, 22.0, 2.0), 7.0), ((10.0, 22.0, 2.0), 7.0), ((0, 22.0, 8.0), 8.0)):
        ball(m, bd, c, r, fabric(P, "white", "white_dark", axis="y"), layers=3, ry=3.6)   # cloud
    m.round_box(bd, 0, 0, 10.0, 8.0, 25.0, 34.0, ROBE, cut=3)                               # round robe
    m.round_box(bd, 0, 0, 10.4, 8.4, 33.0, 34.6, solid(P, "gold"), cut=3)
    m.box(bd, -2.0, 30.0, -8.6, 2.0, 32.4, -8.2, solid(P, "white"))                          # white bow
    hd = m.bone("head", bd, (0, 35, 0))
    ball(m, hd, (0, 39.0, 0), 4.6, solid(P, "glass"), layers=4)                               # snow-globe dome
    ball(m, hd, (0, 38.6, 0), 2.0, solid(P, "skull"), layers=2)
    for sx in (-1, 1):
        m.box(hd, sx * 0.8 - 0.4, 38.8, -2.1, sx * 0.8 + 0.4, 39.6, -1.9, solid(P, "black"))
    for j in range(5):
        ang = math.radians(90 + j * 72)
        spike(m, hd, (0, 45.0, 0), (math.cos(ang), math.sin(ang), 0), 0.8, 1.6, solid(P, "gold"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 9.0, 32.0, 0))
        ball(m, ab, (sx * 11.0, 32.0, 0), 3.0, fabric(P, "violet", "blue_dark", axis="y"), layers=2)
        rod(m, ab, (sx * 11.0, 32.0, 0), (sx * 15.0, 38.0, -2.0), 2, fabric(P, "violet", "blue_dark"), extend=0.3)
        ball(m, ab, (sx * 16.0, 39.0, -2.6), 1.8, solid(P, "white"), layers=2)
    rod(m, "arm_right", (-16.0, 30.0, -2.6), (-16.0, 54.0, -2.6), 1, metal(P, "gold"), extend=0.2)   # ice wand
    ball(m, "arm_right", (-16.0, 55.0, -2.6), 2.0, gem(P, "ice", "white"), layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 4.0, 20.0, 0))
        rod(m, lg, (sx * 4.0, 20.0, 0), (sx * 6.0, 8.0, -2.0), 2, legf, extend=0.3)
        m.round_box(lg, sx * 6.0, -2.6, 1.8, 2.6, 4.0, 8.0, solid(P, "blue"), cut=0)
        for j in range(5):                                                               # curved skate blade
            ang = math.radians(-60 + j * 30)
            m.box(lg, sx * 6.0 - 0.4, 3.0 + 3.0 * math.sin(ang) - 0.6, -2.6 - 6.0 * math.cos(ang) - 1.2,
                  sx * 6.0 + 0.4, 3.0 + 3.0 * math.sin(ang) + 0.6, -2.6 - 6.0 * math.cos(ang) + 1.2, gem(P, "ice", "white"))
    for sx in (-1, 1):                                                                   # trailing ribbons
        rod(m, bd, (sx * 8.0, 26.0, 6.0), (sx * 20.0, 14.0, 10.0), 1, solid(P, "blue"), extend=0.2, t2=3)
    return m
