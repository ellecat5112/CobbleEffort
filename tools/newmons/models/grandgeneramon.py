"""Grand Generamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): the overlord carried by its beast: a hulking pale-blue monster whose whole front is a gaping violet maw
ringed with fangs, great dark bat wings, clawed feet, and riding on top a crowd of small figures: a fist-raising
warrior in red, a helmeted knight and a flag. 25 blocks tall.

Front is -z, y is up. 48 units tall; Perfect stage (no level on wikimon).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing, ball
from _digidetail import armour, fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = ("a hulking pale-blue monster whose front is a gaping violet fanged maw, with dark bat wings, carrying a crowd of "
        "small riders on its head")
BASE = {"pale": (190, 200, 240), "pale_dark": (110, 120, 180), "maw": (110, 40, 120), "maw_dark": (50, 14, 60),
        "tooth": (250, 248, 230), "wing": (50, 40, 70), "wing_dark": (24, 18, 34), "red": (200, 40, 40),
        "gold": (240, 200, 70), "steel": (180, 184, 196), "steel_dark": (90, 94, 106), "claw": (250, 220, 120)}
SHINY = {"pale": (240, 190, 140), "pale_dark": (180, 120, 70), "maw": (40, 90, 150)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "pale", "pale_dark", length=1.4, density=2.0)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and math.hypot(x, (y - 20.0) * 0.8) < 8.0:
        return tone(p["maw"] if y > 14.0 else p["maw_dark"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("grandgeneramon")
    top = m.bone("grandgeneramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    ball(m, bd, (0, 20.0, 0), 13.0, bodyf, layers=7, ry=13.0)
    for j in range(12):                                                                  # ring of fangs
        ang = 2 * math.pi * j / 12
        spike(m, bd, (8.0 * math.cos(ang), 20.0 + 6.4 * math.sin(ang), -12.4), (-math.cos(ang), -math.sin(ang), -0.2),
              1.4, 4.0, solid(P, "tooth"), tip=0.8)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 10.0, 26.0, 2.0))
        bat_wing(m, wb, (side * 10.0, 26.0, 2.0), 16.0, 12.0, 4, metal(P, "wing_dark"), skin(P, "wing", dark="wing_dark"),
                 side=side, sweep=10)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 7.0, 8.0, 0))
        rod(m, lg, (sx * 7.0, 9.0, 0), (sx * 8.0, 2.0, -2.0), 4, FUR, extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 8.0 + (j - 1) * 1.6, 0.8, -4.6), (0, -0.2, -1), 1.2, 3.4, solid(P, "claw"), tip=0.8)
    hd = m.bone("head", bd, (0, 33, 0))                                                    # the riders
    m.round_box(hd, -3.0, 0, 1.6, 1.4, 32.0, 38.0, solid(P, "red"), cut=0)
    m.round_box(hd, -3.0, 0, 1.2, 1.2, 38.0, 40.4, skin(P, "pale", dark="pale_dark"), cut=0)
    rod(m, hd, (-3.0, 37.0, 0), (-5.0, 43.0, -1.0), 1, solid(P, "red"), extend=0, t2=1)
    m.round_box(hd, -5.0, -1.0, 1.0, 1.0, 43.0, 45.0, solid(P, "gold"), cut=0)                # raised fist
    m.round_box(hd, 3.0, 0, 1.8, 1.6, 32.0, 38.0, armour(P, "steel", "steel_dark"), cut=0)
    m.round_box(hd, 3.0, 0, 1.6, 1.6, 38.0, 41.0, metal(P, "steel", dark="steel_dark"), cut=0)
    rod(m, hd, (6.0, 32.0, 2.0), (7.0, 46.0, 2.0), 1, solid(P, "steel_dark"), extend=0, t2=1)
    m.box(hd, 7.0, 42.0, 2.0, 11.0, 46.0, 2.4, solid(P, "red"))                                # flag
    return m
