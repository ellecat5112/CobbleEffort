"""Meicoomon's Unnamed Child Form (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard
after the official art on wikimon.net): a small pale-yellow pup-like creature sitting up, with a big round head, two
long floppy ears tipped brown, big teal-green eyes, a little smile, a white chest and white paws. 1 block tall.

Front is -z, y is up. 20 units tall; Child stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import solid
from _meicoo import P, YEL, cat_eye, WHITE
from _route import tone

HEIGHT = 20
SCALE, HITBOX = sized(1, HEIGHT, 1.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a small pale-yellow pup with a big round head, long floppy brown-tipped ears, big teal-green eyes and white paws"


def earf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y < 6.6:
        return tone((120, 80, 50), face), None
    return YEL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("meicoomonsunnamedchildform")
    top = m.bone("meicoomonsunnamedchildform", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 5.0, 0.6), 3.4, YEL, layers=4, ry=3.4)
    ball(m, bd, (0, 5.4, -1.6), 2.2, WHITE, layers=3, ry=2.4, squash=0.5)
    hd = m.bone("head", bd, (0, 9, 0))
    ball(m, hd, (0, 13.0, 0), 5.2, YEL, layers=5, ry=4.6, squash=0.9)
    for sx in (-1, 1):
        cat_eye(m, hd, sx * 0.8, 12.6, -4.75, sx, w=1.8, h=2.2)
        eb = m.bone("ear_left" if sx > 0 else "ear_right", hd, (sx * 4.0, 15.0, 0))
        rod(m, eb, (sx * 4.0, 15.6, 0), (sx * 6.4, 9.0, 0.4), 2, earf, extend=0.4, t2=3)
        rod(m, eb, (sx * 6.4, 9.0, 0.4), (sx * 6.6, 5.6, 0.6), 2, earf, extend=0.4, t2=3)
    m.box(hd, -0.9, 10.6, -4.75, 0.9, 11.0, -4.6, solid(P, "mouth"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 2.4, 6.0, -1.0))
        rod(m, ab, (sx * 2.4, 6.4, -1.0), (sx * 2.6, 2.6, -2.6), 2, YEL, extend=0.3)
        m.box(ab, sx * 2.6 - 1.0, 1.2, -3.8, sx * 2.6 + 1.0, 2.6, -2.0, WHITE)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lb = m.bone(nm, top, (sx * 2.2, 3.0, 1.0))
        rod(m, lb, (sx * 2.2, 4.0, 1.0), (sx * 2.8, 1.0, -0.6), 2, YEL, extend=0.3)
        m.box(lb, sx * 2.8 - 1.2, 0.0, -2.4, sx * 2.8 + 1.2, 1.4, 0.4, WHITE)
    return m
