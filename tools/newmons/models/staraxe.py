"""Star Axe (a Digimon of the CobbleEffort: Digital crossover; built after the anime still on wikimon.net, its only
picture): a living battle-axe: a huge curved silver blade set with a wavy golden inlay, a gold star at the head of
its haft and a red-and-blue grip. 1 block. Child stage (no level on wikimon; by analogy with Rare Star Sword).

Front is -z, y is up. 32 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import metal, solid
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "floater"
K = 3
LOOK = "a living battle-axe: a huge curved silver blade with a wavy golden inlay, a gold star at the haft's head and a red-and-blue grip"
BASE = {"silver": (220, 224, 236), "silver_dark": (120, 124, 140), "gold": (250, 220, 60), "gold_dark": (190, 150, 20),
        "red": (210, 40, 40), "blue": (40, 60, 180)}
SHINY = {"silver": (250, 200, 120), "silver_dark": (180, 120, 50), "gold": (200, 220, 250)}


def P(v):
    return pal(BASE, SHINY, v)


def bladef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs(z + 4.0 + 1.6 * math.sin(y * 0.8)) < 1.6:
        return tone(p["gold"], face), None
    return metal(P, "silver", dark="silver_dark")(x, y, z, face, variant, box=box, **k)


def gripf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red"] if (y % 3.0) < 1.5 else p["blue"], face), None


def build():
    m = Model("staraxe")
    top = m.bone("staraxe", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    rod(m, bd, (0, 2.0, 0), (0, 28.0, 0), 1, gripf, extend=0.2)                               # haft
    for j in range(9):                                                                   # curved blade
        ang = math.radians(-80 + j * 20)
        c = (0, 22.0 + 9.0 * math.sin(ang), -3.0 - 7.0 * math.cos(ang))
        m.box(bd, -0.6, c[1] - 2.0, c[2] - 2.6, 0.6, c[1] + 2.0, c[2] + 2.6, bladef)
    for j in range(5):                                                                   # gold star at the head
        ang = math.radians(90 + j * 72)
        spike(m, bd, (0, 29.0, 0), (0, math.sin(ang), math.cos(ang)), 1.4, 2.6, metal(P, "gold", dark="gold_dark"),
              tip=0.8)
    return m
