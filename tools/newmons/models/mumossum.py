"""Mumossum, the Mother Pokémon (Normal/Fairy), Obubby evolved: a mother opossum carrying six of her babies. A white
head with a swirl of grey hair, huge dark ears, a pink snout, happy closed eyes and an open, smiling mouth, a black
frilly collar, a grey apron-shaped bib over a white body, a white belly with pink hearts, black arms with her pink hands
clasped, dark legs with pink feet and a long pink ringed tail curling up behind her. Six little Obubbies ride on her:
one on her head between her ears, one on each shoulder, two clinging to her back and one in the curl of her tail.

Front is -z, y is up. 36 units tall to the top baby's ears; baseScale 0.6 (1.3 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix, rod
from _opossum import P, baby, earf, solid, tailf
from _route import tone

SCALE = 0.6
HITBOX = [1.67, 2.17]
KIND = "biped"
K = 4
HEIGHT = 36
LOOK = ("a mother opossum with huge dark ears, a black frilly collar and a pink-hearted belly, smiling, carrying six "
        "of her babies on her head, back and tail")


def heart(u, v, r):
    """Inside a little heart centred at (u, v) = (0, 0), radius r."""
    u, v = u / r, v / r
    return (u * u + v * v - 1) ** 3 - u * u * v ** 3 < 0


def bellyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "east", "west"):
        for hx, hy in ((-3.5, 9), (2.5, 11.5), (4.2, 7.5), (-1, 6.5)):
            u = x - hx if face == "north" else z + 4 - hx * 0.4
            if heart(u, y - hy, 0.9):
                return p["heart"], None
    return tone(p["white"] if face != "down" else p["white_shade"], face), None


def chestf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 3.6 - (22 - y) * 0.15 and y < 22 and \
            not (y < 17.5 and abs(abs(x) - 2.2) < 0.9):
        return tone(p["grey"], face), None                                # the grey apron-shaped bib
    return tone(p["white"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            ex, ey = sx * 1.9, 28.6
            d = abs(y - (ey + 0.5 - abs(x - ex) * 0.55))
            if abs(x - ex) < 1 and d < 0.22:
                return p["eye"], None                                     # happy closed eyes (^ ^)
        if math.hypot(x / 1.1, (y - 25.3) / 0.7) < 1:
            return (p["tongue"] if y < 25.1 else p["mouth"]), None        # open, smiling mouth
    if face in ("up", "north") and y > 30.3 and (x + 1.5) ** 2 + (z + 1.5) ** 2 < 6:
        return tone(p["grey"], face), None                                # grey hair swirl
    return tone(p["white"] if face != "down" else p["white_shade"], face), None


def snoutf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot((x - sx * 0.45) / 0.25, (y - 26.9) / 0.32) < 1:
                return p["nostril"], None
    return tone(p["snout"], face), None


def build() -> Model:
    m = Model("mumossum")
    top = m.bone("mumossum", None, (0, 0, 0))
    for nm, sx in (("leg_left", -1), ("leg_right", 1)):
        lg = m.bone(nm, top, (sx * 2.8, 7, 0))
        m.round_box(lg, sx * 2.8, 0, 2, 2.2, 1.2, 8, solid("leg"), cut=0.6)        # dark legs
        m.box(lg, sx * 2.8 - 1.8, 0, -3.2, sx * 2.8 + 1.8, 1.4, 1.6, solid("foot"))   # pink feet
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0, 6, 5, 5.5, 15.5, bellyf, cut=2)                         # white belly with pink hearts
    m.round_box(bd, 0, 0, 5, 4, 15, 22.5, chestf, cut=1.6)                        # chest with the grey bib
    for i in range(10):                                                           # black frilly collar
        a = 2 * math.pi * i / 10
        cx, cz = 4.6 * math.sin(a), 3.8 * math.cos(a)
        m.box(bd, cx - 1.2, 21.6, cz - 1.2, cx + 1.2, 23.6, cz + 1.2, solid("arm"))
    for nm, sx in (("arm_left", -1), ("arm_right", 1)):
        ar = m.bone(nm, bd, (sx * 4.8, 21, 0))
        rod(m, ar, (sx * 4.8, 21, 0), (sx * 3.8, 17, -3), 2, solid("arm"), extend=0.6)
        rod(m, ar, (sx * 3.8, 17.2, -3), (sx * 0.8, 18.6, -5.2), 1.8, solid("arm"), extend=0.6)
        m.box(ar, sx * 0.9 - 0.9, 18, -6.6, sx * 0.9 + 0.9, 21, -5, solid("snout"))  # pink hands, clasped
    hd = m.bone("head", bd, (0, 24, 0))
    m.round_box(hd, 0, -0.5, 4.2, 4, 23.2, 31.8, headf, cut=1.6)
    m.box(hd, -1.1, 26.2, -5.2, 1.1, 27.7, -4.4, snoutf)                           # pink snout
    for sx in (-1, 1):
        m.box(hd, sx * 3.4 - 3, 29, -1.2, sx * 3.4 + 3, 36, 0.2, earf,
              rotation=(0, 0, sx * 22), pivot=(sx * 3.4, 29.5, -0.5))              # huge dark ears
    tl = m.bone("tail", bd, (0, 9, 4.6))
    pts = [(0, 9, 4.6), (4, 7.5, 7.5), (9, 8.5, 8.5), (12.5, 12, 7), (13, 16.5, 5), (10.5, 19, 4), (8.5, 17, 4.5)]
    for a, b, t in zip(pts, pts[1:], (2.6, 2.4, 2.2, 2, 1.8, 1.6)):
        rod(m, tl, a, b, t, tailf, extend=0.5)                                       # long pink tail curling up
    # six babies: one on her head, four on her back and shoulders, one riding in the curl of her tail
    for i, (c, s) in enumerate((((0, 31, -0.5), 0.5), ((-5.4, 22.5, -0.6), 0.5), ((5.4, 22.5, -0.2), 0.5),
                                ((-2.6, 15.5, 5.6), 0.5), ((2.8, 17, 5.2), 0.5))):
        jb = m.bone(f"joey_{i + 1}", hd if i == 0 else bd, (c[0], c[1], c[2]))
        baby(m, jb, c, s, tail=False)
    jb = m.bone("joey_6", tl, (11.5, 17.5, 5))
    baby(m, jb, (11.4, 15.2, 5.2), 0.5, tail=False)
    return m
