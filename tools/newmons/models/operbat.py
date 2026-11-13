"""Operbat, the Opera Bat Pokémon (Fire/Flying), Sounflame evolved, after the art of the A. Fakemon fanpage (the art's
own name): a red bat standing tall with a hooded, cat-eared head, an ornate golden mask with curling horns and fangs
over its face, half-closed purple eyes and a white ruffled collar. A yellow cloak hangs in tatters down its front, its
raised wings are red with white claws on top and flames licking up from their tattered lower edges, and its long thin
tail ends in a flame.

Shiny: deep blue with pale cyan flames and gold.

Front is -z, y is up. 28 units tall to its wing claws; baseScale 0.5 (0.9 m).
"""
from __future__ import annotations

from _boxmodel import Model, mix, rod, spike
from _firebat import P, flame_spot, membrane, solid, tongues
from _route import tone

SCALE = 0.5
HITBOX = [1.3, 1.75]
KIND = "biped"
K = 4
HEIGHT = 28
LOOK = ("a red bat in a golden opera mask with curling horns, half-closed purple eyes, a white ruffled collar, a "
        "tattered yellow cloak, raised red wings licked by flames and a flame-tipped tail")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and y < 21.4 - max(0.0, abs(x) - 1.2) * 0.8:
        for sx in (-1, 1):
            dx, dy = x - sx * 1.3, y - 19.4
            if (dx / 0.9) ** 2 + (dy / 0.5) ** 2 < 1:
                return (p["eye_purple"] if dy < 0.1 else p["red_dark"]), None   # half-closed eyes
        return tone(p["yellow"], face), None                                  # the golden mask
    return tone(p["red_light"] if face == "up" else p["red"], face), None


def wing_colour(p, u, y, top, bottom):
    if y < 10.5 and flame_spot(u * 12, y):
        return p["yellow"]
    if y < 10.5:
        return p["orange"]
    return p["red"] if y < top - 1.2 else p["red_light"]


def cloak_colour(p, u, y, top, bottom):
    return mix(p["yellow_light"], p["yellow"], min(1.0, (top - y) / 10))


def build() -> Model:
    m = Model("operbat")
    top = m.bone("operbat", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    m.round_box(bd, 0, 0.5, 2.8, 2.2, 7.5, 16.0, solid("red"), cut=1.0)
    m.box(bd, -3.6, 1.0, -2.7, 3.6, 15.0, -2.7, membrane(                      # the tattered yellow cloak
        0.0, 3.6, lambda u: 15.0, lambda u: 6.0 - tongues(u, [(0.1, 5, 0.18), (0.5, 4.5, 0.2), (0.9, 5, 0.18)]),
        cloak_colour))
    m.round_box(bd, 0, -1.4, 2.2, 1.6, 14.5, 17.0, solid("white"), cut=0.8)     # its ruffled collar
    for d in ((-1, 0.3, -0.6), (1, 0.3, -0.6), (0, -0.6, -1)):
        spike(m, bd, (d[0] * 1.2, 15.4, -2.6), d, 1.6, 1.8, solid("white"))

    hd = m.bone("head", bd, (0, 17, -0.5))
    m.round_box(hd, 0, -0.5, 3.2, 3.0, 16.6, 22.6, headf, cut=1.2)
    m.box(hd, -1.4, 17.0, -4.4, 1.4, 19.0, -3.2, solid("yellow"))              # the mask's muzzle
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 22.0, 0.0), (sx * 0.5, 1, 0.1), 2.4, 4.0, solid("red"), tip=1.2)   # cat-like ears
        spike(m, hd, (sx * 2.6, 20.6, -3.2), (sx * 0.6, 1, -0.3), 1.0, 2.6, solid("yellow"))       # curling horns
        spike(m, hd, (sx * 0.8, 17.1, -4.2), (0, -1, -0.2), 0.8, 1.2, solid("white"))               # fangs

    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 1.6, 8, 1))
        rod(m, lb, (sx * 1.6, 8.0, 1.0), (sx * 2.2, 3.6, -0.6), 1.8, solid("red"), extend=0.4)
        rod(m, lb, (sx * 2.2, 3.6, -0.6), (sx * 2.4, 0.6, 0.4), 1.6, solid("red"), extend=0.3)
        for dx in (-0.8, 0.8):
            spike(m, lb, (sx * 2.4 + dx, 0.6, 0.0), (dx * 0.3, -0.2, -1), 1.0, 1.8, solid("red_dark"))

        ar = m.bone(f"arm_{side}", bd, (sx * 2.8, 15, 0.5))                     # raised wings
        rod(m, ar, (sx * 2.8, 15.0, 0.5), (sx * 7.0, 22.0, 1.5), 2.0, solid("red"), extend=0.4)
        rod(m, ar, (sx * 7.0, 22.0, 1.5), (sx * 9.6, 21.0, 1.8), 1.6, solid("red"), extend=0.3)
        for dx in (0.0, 2.2):                                                  # white claws on top
            spike(m, ar, (sx * (6.8 + dx), 22.2 - dx * 0.4, 1.6), (sx * 0.3, 1, 0), 1.6, 2.6, solid("white"), tip=0.8)
        x0, x1 = sorted((sx * 2.8, sx * 10.0))
        m.box(ar, x0, 0.0, 2.4, x1, 23.0, 2.4, membrane(
            2.8, 10.0, lambda u: 15.0 + 7.0 * min(1.0, u / 0.6) - max(0.0, u - 0.6) * 3.0,
            lambda u: 6.0 - tongues(u, [(0.15, 5, 0.12), (0.4, 6, 0.12), (0.65, 5.5, 0.12), (0.9, 4.5, 0.12)]),
            wing_colour))

    tl = m.bone("tail", bd, (0, 9, 2))
    rod(m, tl, (0, 9.0, 2.0), (-2.0, 6.0, 9.0), 1.4, solid("red"), extend=0.4)
    rod(m, tl, (-2.0, 6.0, 9.0), (-6.0, 7.0, 13.0), 1.2, solid("red"), extend=0.3)
    for d, h, key in (((0, 1, 0.2), 3.2, "yellow"), ((-0.5, 0.8, 0.3), 2.4, "orange"), ((0.5, 0.8, 0.2), 2.4, "orange")):
        spike(m, tl, (-6.2, 7.2, 13.2), d, 2.0, h, solid(key, glow=True), tip=0.9)   # the flame on its tail
    return m
