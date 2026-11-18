"""Petit Mamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a little imp: a round violet devil with a jester-like hood of long floppy ears, big pink eyes, a
fanged grin, a red bat symbol on its brow, small orange bat wings, a pointed tail and a lollipop clutched in its hand.
1 block tall.

Front is -z, y is up. 28 units tall; Child stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "floater"
K = 3
LOOK = "a little round violet imp with floppy jester ears, big pink eyes, a fanged grin, small orange bat wings and a lollipop"
BASE = {"violet": (120, 90, 190), "violet_dark": (60, 40, 120), "cream": (250, 236, 220), "pink": (240, 90, 160),
        "red": (210, 40, 60), "orange": (240, 160, 50), "white": (250, 250, 250), "black": (24, 22, 30),
        "candy": (250, 200, 220)}
SHINY = {"violet": (90, 170, 110), "violet_dark": (30, 100, 50)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "violet", dark="violet_dark")


def build():
    m = Model("petitmamon")
    top = m.bone("petitmamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 9.0, 0.4), 3.6, BODY, layers=4, ry=4.0)
    hd = m.bone("head", bd, (0, 13, 0))
    ball(m, hd, (0, 16.0, -0.4), 4.6, BODY, layers=5, ry=4.0)
    m.round_box(hd, 0, -3.4, 3.4, 1.2, 13.4, 17.6, skin(P, "cream", dark="violet_dark"), cut=1)   # face
    for sx in (-1, 1):
        m.box(hd, sx * 1.4 - 0.8, 15.4, -4.75, sx * 1.4 + 0.8, 17.0, -4.6, solid(P, "pink"))
        m.box(hd, sx * 1.4 - 0.3, 15.8, -4.8, sx * 1.4 + 0.3, 16.6, -4.75, solid(P, "black"))
        pts = [(sx * 2.4, 19.0, 0), (sx * 6.0, 21.0, 0.4), (sx * 9.0, 18.0, 0.6)]
        for p0, p1 in zip(pts, pts[1:]):                                                 # floppy jester ears
            rod(m, hd, p0, p1, 2, BODY, extend=0.3, t2=3)
        x0, x1 = sorted((sx * 2.0, sx * 7.0))                                            # small bat wings
        m.box(bd, x0, 8.0, 3.2, x1, 12.0, 3.2, solid(P, "orange"), rotation=(0, 0, sx * 20), pivot=(sx * 2.0, 10.0, 3.2))
    m.box(hd, -1.0, 18.4, -4.2, 1.0, 19.2, -4.0, solid(P, "red"))                          # bat symbol
    m.box(hd, -1.6, 13.8, -4.75, 1.6, 14.4, -4.6, solid(P, "black"))
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.0, 14.4, -4.7), (0, -1, 0), 0.8, 0.8, solid(P, "white"), tip=0.8)
    al = m.bone("arm_left", bd, (3.4, 10.0, -1.0))
    rod(m, al, (3.4, 10.0, -1.0), (5.0, 8.0, -2.0), 1, BODY, extend=0.2, t2=1)
    rod(m, al, (5.0, 8.0, -2.0), (5.4, 14.0, -2.0), 1, solid(P, "white"), extend=0.1)      # lollipop
    ball(m, al, (5.4, 15.4, -2.0), 1.4, solid(P, "candy"), layers=2, squash=0.4)
    tb = m.bone("tail", bd, (0, 6, 3))
    rod(m, tb, (0, 6.0, 3.0), (2.0, 3.0, 6.0), 1, BODY, extend=0.2, t2=1)
    spike(m, tb, (2.0, 3.0, 6.0), (0.4, -0.3, 1), 1.0, 1.6, solid(P, "red"), tip=0.8)
    return m
