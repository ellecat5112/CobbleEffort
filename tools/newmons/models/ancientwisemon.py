"""Ancient Wisemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the ancient warrior of steel, a robed sage. A vast green cloak lined in red with gold
borders spreading to the ground, a white surplice with a gold buckle, a hood of shadow where only two yellow eyes
glow under a pale mask-veil, a purple feather fan, and a silver balance held above its head: a sun on one pan, a
crescent moon on the other. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, feathers, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.2)
KIND = "floater"
K = 3
LOOK = ("a robed sage: a vast green cloak lined in red with gold borders, a white surplice, a shadowed hood with two "
        "glowing yellow eyes, a purple feather fan and a silver balance with a sun and a crescent moon")
BASE = {"green": (50, 130, 60), "green_dark": (20, 70, 30), "red": (180, 40, 40), "gold": (230, 186, 60),
        "gold_dark": (160, 112, 26), "white": (246, 246, 250), "white_dark": (190, 196, 214), "shadow": (20, 26, 24),
        "eye": (255, 240, 80), "purple": (140, 70, 170), "purple_dark": (80, 30, 110), "silver": (200, 204, 216),
        "silver_dark": (110, 114, 126), "jewel": (220, 40, 50), "jewel_light": (255, 160, 160)}
SHINY = {"green": (40, 60, 140), "green_dark": (16, 24, 80), "red": (230, 190, 60), "purple": (60, 170, 120),
         "purple_dark": (20, 100, 60)}


def P(v):
    return pal(BASE, SHINY, v)


CLOAK = fabric(P, "green", "green_dark", axis="y", period=3.2)
WHITE = fabric(P, "white", "white_dark", axis="y", period=2.4)
GOLD = metal(P, "gold", dark="gold_dark")
SILVER = metal(P, "silver", dark="silver_dark")
FAN = feathers(P, "purple", "purple_dark", size=(1.2, 2.4), flow=(0, 1))


def cloakf(x, y, z, face, variant, box=None, **k):
    """The cloak: green with a gold border round the hem and a red lining showing on its inner (south) faces."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if v < 1.0 and face not in ("up", "down"):
        return tone(p["gold"], face), None
    if face == "south" and z < 0:
        return tone(p["red"], face), None
    return CLOAK(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ancientwisemon")
    top = m.bone("ancientwisemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    for i in range(14):                                          # the cloak: a cone of panels flaring to the ground
        ang = math.radians(-170 + i * (340 / 13))
        c = (5.0 * math.sin(ang), 52.0, -4.0 * math.cos(ang))
        m.box(bd, c[0] - 2.6, 0.0, c[2], c[0] + 2.6, 52.0, c[2] + 0.8, cloakf,
              rotation=(-14 * math.cos(ang), -math.degrees(ang), -10 * math.sin(ang)), pivot=c)
    m.box(bd, -3.6, 8.0, -4.6, 3.6, 50.0, -3.6, WHITE)                                   # white surplice
    m.box(bd, -1.4, 26.0, -5.2, 1.4, 29.0, -4.4, GOLD)                                    # gold buckle
    spike(m, bd, (0, 26.0, -4.8), (0, -1, 0), 1.6, 4.0, GOLD)
    for sx in (-1, 1):                                           # gold sun-disc clasps
        m.round_box(bd, sx * 3.4, -4.8, 1.4, 0.5, 46.0, 48.8, GOLD, cut=1)
    hd = m.bone("head", bd, (0, 54, 0))
    m.round_box(hd, 0, 0, 3.6, 3.6, 52.0, 60.0, cloakf, cut=1)                            # the hood
    m.box(hd, -2.6, 53.0, -3.8, 2.6, 58.6, -3.0, solid(P, "shadow"))
    for sx in (-1, 1):
        m.box(hd, sx * 1.1 - 0.5, 56.6, -3.9, sx * 1.1 + 0.5, 57.4, -3.7, solid(P, "eye", glow=True))
    m.box(hd, -2.0, 50.0, -4.0, 2.0, 55.0, -3.4, WHITE)                                  # mask-veil over the mouth
    spike(m, hd, (0, 60.0, -1.0), (0, 1, 0), 2.0, 4.0, cloakf, tip=1.0)                  # hood point
    for sx in (-1, 1):                                           # green crest wings on the hood
        rod(m, hd, (sx * 3.4, 58.0, 0), (sx * 6.5, 62.0, 1.0), 1, solid(P, "green"), extend=0.3, t2=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):          # wide sleeves lifted up to the balance
        ab = m.bone(nm, bd, (sx * 5.0, 48.0, 0))
        rod(m, ab, (sx * 5.0, 48.0, 0), (sx * 9.0, 58.0, -1.0), 5, cloakf, extend=0.6)
        m.box(ab, sx * 9.0 - 2.0, 56.5, -2.6, sx * 9.0 + 2.0, 58.0, 0.6, solid(P, "red"))
    sc = m.bone("cap", bd, (0, 64, -1))                          # the silver balance overhead
    m.box(sc, -12.0, 63.4, -1.6, 12.0, 64.6, -0.4, SILVER)
    rod(m, sc, (0, 60.0, -1.0), (0, 66.0, -1.0), 1, SILVER, extend=0.2)
    m.round_box(sc, 0, -1.0, 1.2, 1.2, 66.0, 68.4, gem(P, "jewel", "jewel_light"), cut=1)
    for sx in (-1, 1):
        rod(m, sc, (sx * 12.0, 64.0, -1.0), (sx * 12.0, 60.0, -1.0), 1, SILVER, extend=0.1)
        m.box(sc, sx * 12.0 - 1.2, 57.0, -2.2, sx * 12.0 + 1.2, 60.0, 0.2, solid(P, "purple"))   # tassels
    ball(m, sc, (12.0, 68.0, -1.0), 1.8, solid(P, "gold", glow=True), layers=3)          # the sun
    for i in range(5):                                           # the crescent moon
        a = math.radians(120 + i * 30)
        c = (-12.0 + 2.2 * math.cos(a), 68.0 + 2.2 * math.sin(a), -1.0)
        m.box(sc, c[0] - 0.6, c[1] - 0.6, c[2] - 0.5, c[0] + 0.6, c[1] + 0.6, c[2] + 0.5, GOLD)
    fb = m.bone("fan", bd, (-4, 40, -5))                         # the purple feather fan at its chest
    for i in range(7):
        a = math.radians(-60 + i * 20)
        rod(m, fb, (-4.0, 38.0, -5.4), (-4.0 + 6.0 * math.sin(a), 38.0 + 6.0 * math.cos(a), -5.6), 2, FAN,
            extend=0.2, t2=1)
    return m
