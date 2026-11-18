"""Pico Devimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a little round blue imp with a stitched mouth full of grinning teeth, yellow eyes, a white skull
mark on its brow, twisted antenna-horns, tattered blue bat wings, and pale clawed hands and feet with red claws.
1 block tall.

Front is -z, y is up. 24 units tall; Child stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "floater"
K = 3
LOOK = "a little round blue imp with a grinning stitched mouth, yellow eyes, a skull mark, twisted horns and tattered bat wings"
BASE = {"blue": (60, 70, 160), "blue_dark": (24, 30, 90), "yellow": (250, 210, 50), "white": (246, 246, 250),
        "pale": (200, 210, 240), "red": (200, 40, 40), "black": (20, 20, 24), "wing": (70, 90, 190)}
SHINY = {"blue": (150, 60, 90), "blue_dark": (80, 20, 40), "wing": (190, 80, 110)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "blue", dark="blue_dark")


def build():
    m = Model("picodevimon")
    top = m.bone("picodevimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 11.0, 0), 5.0, BODY, layers=5, ry=4.6)
    for sx in (-1, 1):
        m.box(bd, sx * 2.0 - 1.0, 12.0, -4.9, sx * 2.0 + 1.0, 13.4, -4.75, solid(P, "yellow"))
        m.box(bd, sx * 2.0 - 0.3, 12.2, -4.95, sx * 2.0 + 0.3, 13.2, -4.9, solid(P, "black"))
        pts = [(sx * 1.6, 15.4, 0), (sx * 2.6, 18.0, 0.4), (sx * 1.6, 20.0, 0.6), (sx * 2.8, 21.4, 0.8)]
        for p0, p1 in zip(pts, pts[1:]):                                                 # twisted horns
            rod(m, bd, p0, p1, 1, solid(P, "black"), extend=0.1)
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 4.4, 9.0, -1.0))
        ball(m, ab, (sx * 5.6, 7.0, -1.6), 1.6, skin(P, "pale", dark="blue_dark"), layers=2)
        spike(m, ab, (sx * 6.0, 5.6, -2.0), (sx * 0.2, -1, -0.4), 0.9, 2.4, solid(P, "red"), tip=0.8)
        lg = m.bone("leg_left" if sx > 0 else "leg_right", top, (sx * 2.0, 6.0, 0))
        ball(m, lg, (sx * 2.4, 5.0, -0.6), 1.4, skin(P, "pale", dark="blue_dark"), layers=2)
        spike(m, lg, (sx * 2.6, 3.8, -1.4), (0, -1, -0.4), 0.8, 2.0, solid(P, "red"), tip=0.8)
    m.box(bd, -3.0, 8.6, -4.85, 3.0, 9.4, -4.65, solid(P, "black"))                        # grinning mouth
    for j in range(6):
        m.box(bd, -2.6 + j * 1.0, 8.8, -4.9, -2.0 + j * 1.0, 9.4, -4.85, solid(P, "white"))
    m.box(bd, -0.8, 14.4, -4.5, 0.8, 15.6, -4.3, solid(P, "white"))                        # skull mark
    wb = m.bone("wings", bd, (0, 12, 3))
    for side in (1, -1):
        bat_wing(m, wb, (side * 3.0, 12.0, 3.0), 14.0, 10.0, 4, solid(P, "black"), skin(P, "wing", dark="blue_dark"),
                 side=side, sweep=10)
    return m
