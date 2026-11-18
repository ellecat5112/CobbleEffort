"""Platinum Scumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a gleaming platinum-blue slime of a creature with a pointed swirl on top, goggling eyes, a
huge grin of square teeth and a lolling red tongue, long skeletal steel arms with cuffs and claws, and a little pink
Chuumon riding on its head. 15 blocks tall.

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a gleaming platinum-blue slime with a pointed swirl top, goggling eyes, a grin of square teeth, a red tongue and long skeletal steel arms"
BASE = {"plat": (200, 220, 240), "plat_dark": (130, 150, 180), "white": (250, 250, 255), "eye": (220, 120, 30),
        "black": (20, 20, 24), "tooth": (250, 250, 240), "tongue": (220, 50, 60), "steel": (200, 204, 216),
        "steel_dark": (90, 94, 108), "pink": (240, 140, 180)}
SHINY = {"plat": (240, 220, 160), "plat_dark": (190, 160, 90)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "plat", dark="plat_dark", var=0.02)
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("platinumscumon")
    top = m.bone("platinumscumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 14.0, 0), 7.6, BODY, layers=6, ry=8.0)
    spike(m, bd, (0, 21.0, 0.4), (0.3, 1, 0.2), 3.6, 7.0, BODY, tip=0.8)                    # pointed swirl top
    for sx in (-1, 1):
        ball(m, bd, (sx * 2.6, 17.0, -6.6), 1.6, solid(P, "white"), layers=2, squash=0.6)
        m.box(bd, sx * 2.6 - 0.6, 16.6, -7.65, sx * 2.6 + 0.6, 17.8, -7.5, solid(P, "eye"))
    m.box(bd, -5.0, 10.0, -7.4, 5.0, 13.0, -7.0, solid(P, "black"))                        # grin
    for j in range(7):
        m.box(bd, -4.6 + j * 1.36, 11.6, -7.6, -3.6 + j * 1.36, 13.0, -7.3, solid(P, "tooth"))
    rod(m, bd, (0, 10.6, -7.4), (1.0, 5.0, -9.0), 2, solid(P, "tongue"), extend=0.3, t2=3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # skeletal steel arms
        ab = m.bone(nm, bd, (sx * 7.0, 14.0, 0))
        pts = [(sx * 7.0, 14.0, 0), (sx * 12.0, 18.0, -1.0), (sx * 15.0, 12.0, -3.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 1, STEEL, extend=0.2)
        m.round_box(ab, sx * 12.0, -1.0, 1.4, 1.4, 17.0, 19.0, solid(P, "black"), cut=0)   # cuffs
        for f in range(4):
            spike(m, ab, (sx * 15.0 + (f - 1.5) * 0.8, 11.4, -3.4), (sx * 0.2, -1, -0.4), 0.7, 3.0, STEEL, tip=0.8)
    ball(m, bd, (2.4, 22.6, 2.0), 1.4, solid(P, "pink"), layers=2)                          # little Chuumon rider
    for sx in (-1, 1):
        ball(m, bd, (2.4 + sx * 1.2, 24.0, 2.0), 0.6, solid(P, "pink"), layers=1)
    return m
