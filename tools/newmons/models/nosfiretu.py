"""Nosfiretu, the Vampire Bat Pokémon (Fire/Flying), Operbat evolved, after the art of the A. Fakemon fanpage (the
art's own name): a tall, gaunt red vampire bat standing with its arms crossed over its chest, its face hidden behind a
golden mask with flaring horns like a crown of flame, narrow purple eyes and a fanged open mouth, silver-white spikes
sweeping back from its head. Its wings wrap round it like a great purple cape lined with gold, tattered at the hem,
with white claws on top, and its long segmented tail curls on the ground.

Shiny: deep blue with a crimson cape and pale gold.

Front is -z, y is up. 39 units tall to its wing claws; baseScale 0.72 (1.75 m).
"""
from __future__ import annotations

from _boxmodel import Model, mix, rod, spike
from _firebat import P, membrane, segments, solid, tongues
from _route import tone

SCALE = 0.72
HITBOX = [1.6, 2.4]
KIND = "biped"
K = 3
HEIGHT = 39
LOOK = ("a tall gaunt red vampire bat with crossed arms, a golden horned mask with purple eyes and fangs, silver spikes "
        "on its head, a great purple cape of wings lined with gold, and a long segmented tail")


def maskf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.2, y - 29.3
            if (dx / 0.95) ** 2 + ((dy + dx * sx * 0.35) / 0.42) ** 2 < 1:
                return p["eye_purple"], None                                  # narrow slanted eyes
        if (x / 1.4) ** 2 + ((y - 27.2) / 0.8) ** 2 < 1:
            if abs(y - 27.2) > 0.45 and int((x + 1.4) / 0.7) % 2 == 0:
                return p["white"], None                                       # fangs
            return p["mouth"], None
        return tone(p["yellow"], face), None
    if face == "up" or (face in ("east", "west") and z < -1.4):
        return tone(p["yellow"], face), None
    return tone(p["red"], face), None


def cape_colour(p, u, y, top, bottom):
    if u < 0.12 or y < bottom + 1.2:
        return p["orange"] if y < bottom + 1.2 else p["yellow"]               # the golden lining and hem
    return p["purple_light"] if y > top - 1.5 else p["purple"]


def build() -> Model:
    m = Model("nosfiretu")
    top = m.bone("nosfiretu", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    m.round_box(bd, 0, 0.5, 3.2, 2.4, 13.0, 26.0, solid("red"), cut=1.0)       # its gaunt body

    hd = m.bone("head", bd, (0, 26, -0.5))
    m.round_box(hd, 0, -0.5, 2.8, 2.8, 26.0, 31.5, maskf, cut=0.8)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.8, 29.5, -2.6), (sx * 1, 0.4, -0.2), 1.2, 3.0, solid("yellow"), tip=0.6)   # mask flares
        spike(m, hd, (sx * 1.4, 31.4, -2.0), (sx * 0.5, 1, 0.1), 1.4, 4.2, solid("yellow"), tip=0.8)    # its horns
        for dz, dx in ((0.6, 1.0), (2.0, 2.0)):                                # silver spikes sweeping back
            spike(m, hd, (sx * dx, 31.0, dz), (sx * 0.4, 0.7, 0.8), 1.6, 5.0, solid("claw"), tip=0.8)
    spike(m, hd, (0, 31.5, -2.6), (0, 1, -0.2), 1.4, 3.4, solid("yellow"), tip=0.7)

    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 2.0, 13, 1))
        rod(m, lb, (sx * 2.0, 13.0, 1.0), (sx * 2.6, 7.0, -1.2), 2.4, solid("red"), extend=0.4)
        rod(m, lb, (sx * 2.6, 7.0, -1.2), (sx * 2.4, 1.0, 0.8), 2.0, solid("red"), extend=0.4)
        for d in ((-0.4, -0.2, -1), (0.4, -0.2, -1), (0, -0.2, 1)):
            spike(m, lb, (sx * 2.4, 0.8, 0.6), d, 1.0, 2.0, solid("red_dark"))

        ar = m.bone(f"arm_{side}", bd, (sx * 3.4, 25, 0))                       # arms crossed over its chest
        rod(m, ar, (sx * 3.4, 25.0, 0.0), (sx * 3.8, 19.6, -2.6), 1.8, solid("red"), extend=0.4)
        rod(m, ar, (sx * 3.8, 19.6, -2.6), (-sx * 2.2, 23.0 - (sx > 0) * 1.2, -3.4 - (sx > 0) * 0.6), 1.6,
            solid("red_light"), extend=0.4)

        w = m.bone(f"wing_{side}", bd, (sx * 3.0, 25, 2))                       # the cape of wings
        rod(m, w, (sx * 3.0, 25.0, 2.0), (sx * 5.0, 34.0, 3.0), 1.6, solid("purple_dark"), extend=0.4)
        for d in ((sx * 0.3, 1, 0), (sx * 0.7, 1, 0.3), (0, 1, 0.5)):
            spike(m, w, (sx * 5.0, 34.0, 3.0), d, 1.4, 4.0, solid("claw"), tip=0.7)
        x0, x1 = sorted((sx * 1.0, sx * 12.0))
        m.box(w, x0, 2.0, 3.4, x1, 35.0, 3.4, membrane(
            1.0, 12.0, lambda u: 25.0 + 9.0 * min(1.0, u / 0.25) - max(0.0, u - 0.25) / 0.75 * 12.0,
            lambda u: 6.0 + 10.0 * u - tongues(u, [(0.08, 4, 0.1), (0.3, 5, 0.1), (0.5, 5, 0.1), (0.7, 4.5, 0.1),
                                                     (0.9, 4, 0.1)]),
            cape_colour), rotation=(0, -sx * 28, 0), pivot=(sx * 1.0, 20.0, 3.4))

    tl = m.bone("tail", bd, (0, 13, 2))
    pts = [(0, 13.0, 2.0), (1.0, 8.0, 7.0), (4.0, 3.0, 10.0), (8.0, 1.5, 9.0), (10.0, 3.0, 6.0)]
    for a, b, t in zip(pts, pts[1:], (2.2, 2.0, 1.8, 1.4)):
        rod(m, tl, a, b, t, segments("red", "red_dark"), extend=0.5)
    return m
