"""Arpsant, the Harpist Pokémon (Grass/Psychic), Whissant evolved, after the art of the A. Fakemon fanpage (the art's
own name): a slender green songbird standing tall on yellow legs, with a sweeping white crest tipped orange and red,
a narrow yellow eye, a sharp pale beak, a white collar of feathers, an orange belly and long green wings and tail. It
holds a lyre made from a curved twig strung with orange leaves.

Shiny: rose-pink with a lilac belly.

Front is -z, y is up. 25 units tall; baseScale 0.6 (0.95 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _route import tone
from _songbird import P, ramp, solid

SCALE = 0.6
HITBOX = [0.9, 1.55]
KIND = "biped"
K = 4
HEIGHT = 25
LOOK = ("a slender green songbird with a white crest tipped orange, a narrow yellow eye, a white feather collar, an "
        "orange belly and a lyre of a curved twig strung with orange leaves")


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and y < 12.5 and abs(x) < 1.8:
        return tone(p["orange"], face), None
    return tone(p["green"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") or face == "north":
        a = z if face != "north" else x * (1 if x > 0 else -1) - 2.2
        dz, dy = (z + 0.6, y - 21.2) if face != "north" else (abs(x) - 1.4, y - 21.2)
        if (dz / 0.9) ** 2 + (dy / 0.6) ** 2 < 1:
            return (p["pupil"] if abs(dz) < 0.16 else p["eye"]), None         # narrow yellow eyes
    return tone(p["green_light"] if face == "up" else p["green"], face), None


def build() -> Model:
    m = Model("arpsant")
    top = m.bone("arpsant", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    m.round_box(bd, 0, 0.4, 2.8, 3.2, 7.0, 15.0, bodyf, cut=1.2)
    for d in ((-1, 0.2, -0.6), (1, 0.2, -0.6), (0, -0.6, -1)):                   # the white feather collar
        spike(m, bd, (d[0] * 1.6, 14.6, -2.0), d, 1.6, 1.8, solid("white"))
    rod(m, bd, (0, 9.0, 3.0), (0, 4.6, 9.6), 2.6, ramp("green", "red"), extend=0.4, t2=0.8)   # tail

    hd = m.bone("head", bd, (0, 15, -0.5))
    rod(m, hd, (0, 14.6, -0.4), (0, 19.0, -1.0), 2.0, solid("green"), extend=0.6)              # neck
    m.round_box(hd, 0, -1.0, 2.4, 2.6, 18.6, 23.6, headf, cut=0.8)
    spike(m, hd, (0, 21.0, -3.4), (0, -0.1, -1), 1.4, 3.0, solid("beak"), tip=0.6)            # sharp beak
    rod(m, hd, (0, 23.2, -1.4), (0, 24.6, 3.6), 2.8, ramp("white", "orange", 0.5), extend=0.4, t2=1.0)   # crest
    spike(m, hd, (0, 24.4, 3.4), (0, 0.3, 1), 1.4, 1.8, solid("red"))

    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 1.2, 8, 0.6))
        rod(m, lb, (sx * 1.2, 8.0, 0.6), (sx * 1.4, 4.0, -0.4), 1.4, solid("leg"), extend=0.4)
        rod(m, lb, (sx * 1.4, 4.0, -0.4), (sx * 1.6, 0.6, 0.2), 1.2, solid("leg"), extend=0.4)
        for d in ((-0.3, -0.2, -1), (0.3, -0.2, -1)):
            spike(m, lb, (sx * 1.6, 0.6, 0.0), d, 0.9, 1.6, solid("claw"))
        ar = m.bone(f"arm_{side}", bd, (sx * 2.8, 14, 0))
        rod(m, ar, (sx * 2.8, 14.0, 0.0), (sx * 4.0, 7.0, 3.4), 3.0, ramp("green", "green_dark"), extend=0.4, t2=1.0)
    ar = "arm_left"                                                             # the leafy lyre
    pts = [(-3.6, 8.0, -3.4), (-4.4, 12.0, -4.0), (-4.6, 16.0, -4.2), (-3.6, 19.6, -4.4), (-2.0, 21.0, -4.6)]
    for a, b in zip(pts, pts[1:]):
        rod(m, ar, a, b, 1.0, solid("stick"), extend=0.4)
    for y in (10.0, 12.6, 15.2, 17.8):
        spike(m, ar, (-4.2, y, -4.0), (1, 0.15, 0), 1.0, 2.4, solid("orange"))  # orange leaf strings
    return m
