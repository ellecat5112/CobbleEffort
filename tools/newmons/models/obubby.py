"""Obubby, the Joey Pokémon (Normal): a baby opossum. A big round white head with a grey band low down, huge dark
round ears, a pink pig-like snout, big dark eyes and pink blush, a little curl of hair on top, a small white body with
a grey band, little dark arms hugging its long pink ringed tail, which curls round in front of it, and pink feet.

Front is -z, y is up. 16 units tall to the ear tips; baseScale 0.55 (0.4 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _opossum import P, baby, baby_bodyf, baby_headf, earf, snoutf, solid, tailf

SCALE = 0.55
HITBOX = [0.6, 0.6]
KIND = "biped"
K = 6
HEIGHT = 16
LOOK = ("a baby opossum with a big round white head, huge dark ears, a pink snout and blush, and a long pink tail "
        "it hugs in front of it")


def build() -> Model:
    m = Model("obubby")
    top = m.bone("obubby", None, (0, 0, 0))
    s = 1.25
    for nm, sx in (("leg_left", -1), ("leg_right", 1)):
        lg = m.bone(nm, top, (sx * 1.6, 1, -1))
        m.box(lg, sx * 1.6 - 0.9, 0, -2.8, sx * 1.6 + 0.9, 1.2, -0.4, solid("foot"))
    bd = m.bone("body", top, (0, 3, 0))
    m.round_box(bd, 0, 0, 2.3 * s, 2.0 * s, 0.6 * s, 4.2 * s, baby_bodyf(0, s), cut=1)
    hd = m.bone("head", bd, (0, 5, 0))
    m.round_box(hd, 0, 0, 3.7 * s, 3.3 * s, 3.6 * s, 9.8 * s, baby_headf(0, 0, 0, s), cut=1.6)
    m.box(hd, -0.9 * s, 5.6 * s, -3.9 * s, 0.9 * s, 6.8 * s, -3.2 * s, snoutf(0, 6.2 * s, s))
    for sx in (-1, 1):
        m.box(hd, sx * 2.4 * s - 2.1 * s, 8.4 * s, -0.6 * s, sx * 2.4 * s + 2.1 * s, 13 * s, 0.6 * s, earf,
              rotation=(0, 0, sx * 24), pivot=(sx * 2.4 * s, 8.8 * s, 0))
    rod(m, hd, (0, 9.6 * s, 0), (0.6 * s, 11.4 * s, -0.3 * s), 0.6, solid("grey_dark"), extend=0.2)
    for nm, sx in (("arm_left", -1), ("arm_right", 1)):
        ar = m.bone(nm, bd, (sx * 2, 4.5, -1.5))
        m.box(ar, sx * 2 - 0.7, 2.2, -3.4, sx * 2 + 0.7, 4.6, -1.8, solid("arm"))   # little dark arms
    tl = m.bone("tail", bd, (0, 1.5, 2.4))
    pts = [(0, 1.5, 2.4), (3, 1.2, 2.4), (4.2, 1.6, -1), (2.6, 3.4, -3.6), (0.4, 4.4, -4.4), (-1.6, 5.4, -4)]
    for a, b, t in zip(pts, pts[1:], (1.8, 1.7, 1.6, 1.4, 1.1)):
        rod(m, tl, a, b, t, tailf, extend=0.4)                                       # the tail it hugs
    return m
