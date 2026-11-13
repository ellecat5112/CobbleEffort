"""Calligrimm, the Ink Titan Pokémon (Dark/Steel), Incwell evolved: a gargantuan, kaiju-sized mass of ink. A huge
silver pen nib crowns it like a head, flanked by two great horns of glowing yellow ink-fire; two massive arms curl up
from its shoulders, each ending in a claw of three pen nibs; ink tentacles spread out over the ground beneath it; and
in its chest gapes a terrifying maw ringed with jagged shards of broken inkwell glass.

Front is -z, y is up. 50 units tall to the nib's point; baseScale 2.2 (7 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _ink import P, eyef, firef, glassf, inkf, nibf
from _route import tone

SCALE = 2.2
HITBOX = [1.64, 3.09]
KIND = "biped"
K = 3
HEIGHT = 50
LOOK = ("a gargantuan ink kaiju crowned by a huge pen nib and horns of glowing ink-fire, with pen-nib claws and a "
        "gaping maw of broken glass shards in its chest")


def mawf(x, y, z, face, variant, **k):
    """The maw's dark hollow, with a faint glow deep inside."""
    p = P(variant)
    if face == "north" and abs(x) < 3 and abs(y - 21) < 1.6:
        return p["fire"], p["fire"]
    return p["ink_dark"], None


def build() -> Model:
    m = Model("calligrimm")
    top = m.bone("calligrimm", None, (0, 0, 0))
    # ink tentacles spreading over the ground (a skirt that sways)
    sk = m.bone("skirt", top, (0, 6, 0))
    for i in range(9):
        a = i * 2 * math.pi / 9 + 0.2
        r0, r1 = 4, 13 + (i % 3) * 2
        p0 = (r0 * math.sin(a), 6, r0 * math.cos(a))
        p1 = ((r0 + r1) * 0.55 * math.sin(a), 2, (r0 + r1) * 0.55 * math.cos(a))
        p2 = (r1 * math.sin(a), 0.6, r1 * math.cos(a))
        rod(m, sk, p0, p1, 3.4, inkf, extend=0.8)
        rod(m, sk, p1, p2, 2.2, inkf, extend=0.6)
        spike(m, sk, p2, (math.sin(a), 0.6, math.cos(a)), 1.4, 3, inkf)            # curled tips
    bd = m.bone("body", top, (0, 16, 0))
    m.round_box(bd, 0, 0, 8, 6.5, 4, 16, inkf, cut=2.4)                           # the great body
    m.round_box(bd, 0, 0, 9, 7, 15, 28, inkf, cut=2.6)
    m.round_box(bd, 0, 0, 7, 5.6, 27.5, 33, inkf, cut=2)
    # the maw in its chest: a dark hollow ringed with jagged glass shards
    jw = m.bone("jaw", bd, (0, 19, -6.5))
    m.box(bd, -6, 15.5, -7.4, 6, 26, -6.8, mawf)                                   # a huge gaping maw
    for i in range(9):
        x = -5.4 + i * 1.35
        spike(m, bd, (x, 26.2, -7.2), (0.12 * (i - 4), -1, -0.25), 1.4, 3.4 + (i % 2) * 2.2, glassf, tip=0.8)  # upper
        spike(m, jw, (x + 0.6, 15.3, -7.2), (-0.12 * (i - 4), 1, -0.25), 1.4, 3 + ((i + 1) % 2) * 2.4, glassf,
              tip=0.8)                                                            # lower glass fangs
    m.box(jw, -6.6, 13.8, -7.8, 6.6, 15.6, -6.4, inkf)                            # the lower lip
    m.box(bd, -6.6, 26, -7.8, 6.6, 27.6, -6.4, inkf)                              # the upper lip
    for sx in (-1, 1):                                                           # hulking shoulder masses
        m.round_box(bd, sx * 7.5, 0.5, 3.6, 4.4, 22, 30, inkf, cut=1.4)
    # the head: a huge nib crown, glowing eyes, and horns of ink-fire
    hd = m.bone("head", bd, (0, 33, 0))
    m.round_box(hd, 0, -0.5, 5, 4.4, 32.5, 37, inkf, cut=1.6)
    for sx in (-1, 1):
        m.box(hd, sx * 2.2 - 1, 34.4, -4.95, sx * 2.2 + 1, 35.6, -4.6, eyef)
        m.box(hd, sx * 3.8, 33.5, -2.5, sx * 3.8, 50, 2.5, firef("z", 0, 33.5, 16.5, 5),
              rotation=(0, 0, sx * 26), pivot=(sx * 3.8, 34, 0))                   # ink-fire horns (crossed planes)
        m.box(hd, sx * 3.8 - 2.5, 33.5, 0, sx * 3.8 + 2.5, 50, 0, firef("x", sx * 3.8, 33.5, 16.5, 5),
              rotation=(0, 0, sx * 26), pivot=(sx * 3.8, 34, 0))
    m.box(hd, -4.4, 36, -3.6, 4.4, 50, -3.6, nibf(0, 50, 8.8, 14, tip_up=True))   # the nib crown, point up
    # massive arms curling up, each ending in a claw of three pen nibs
    for nm, sx in (("arm_left", -1), ("arm_right", 1)):
        ar = m.bone(nm, bd, (sx * 8.5, 26, 0))
        pts = [(sx * 8.5, 26, 0), (sx * 14, 23, -1), (sx * 18, 27, -2), (sx * 19, 34, -2.5), (sx * 17.5, 40, -3)]
        for a, b, t in zip(pts, pts[1:], (5, 4.6, 4.2, 3.8)):
            rod(m, ar, a, b, t, inkf, extend=1)
        for j, dx in enumerate((-2.2, 0, 2.2)):
            cx = sx * 17.5 + dx
            m.box(ar, cx - 1.4, 40, -3.5, cx + 1.4, 47 + (1.5 if j == 1 else 0), -3.5,
                  nibf(cx, 47 + (1.5 if j == 1 else 0), 2.8, 7 + (1.5 if j == 1 else 0), tip_up=True),
                  rotation=(-10, 0, -dx * 6), pivot=(cx, 40, -3.5))                 # three nib claws
    return m
