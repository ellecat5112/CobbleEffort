"""Fishugly, the Gawkfish Pokémon (Water/Ground), Fangfosh evolved, after the art of the A. Fakemon fanpage (the art's
own name): a gangly creature that walks on two long blue fin-legs, a big green fish head with a grimace of jagged
fangs, black-ringed eyes with a bar across them and a dark streak below, a black mop of fins at the back of its head
with pale spines, black fins at its jaw and long blue arm-fins hanging down to its knees.

Shiny: violet limbs and a rose head.

Front is -z, y is up. 27 units tall to the top of its head fins; baseScale 0.48 (0.8 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _fishface import P, fin, grimace, ring_eye, solid
from _route import tone

SCALE = 0.48
HITBOX = [1.0, 1.65]
KIND = "biped"
K = 4
HEIGHT = 27
LOOK = ("a gangly walker on two long blue fin-legs with a big green fish head, a grimace of jagged fangs, black-ringed "
        "eyes, a black mop of fins and long blue arm-fins")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        g = grimace(p, x, y, 3.3, 18.0, 21.2, pointed=True)
        if g:
            return g, None
    if face in ("east", "west"):
        e = ring_eye(p, z + 2.6, y - 22.8, 1.9)
        if e:
            return e, None
        if abs(z + 2.6) < 0.4 and 19.4 < y < 21.0:
            return p["black"], None                                           # the dark streak under its eye
    return tone(p["green"], face), None


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and 12.5 < y < 16.5 and abs(((y - 12.5) % 1.4) - 0.7 + (z * 0.4)) < 0.16:
        return p["cream"], None                                               # pale slashes down its sides
    return tone(p["blue"], face), None


def legf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y - (box.lo[1] + box.size[1] * 0.5)) < 0.3:
        return p["cream"], None
    return tone(p["blue"], face), None


def build() -> Model:
    m = Model("fishugly")
    top = m.bone("fishugly", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 13, 0))
    m.round_box(bd, 0, 0.6, 3.0, 2.6, 11.5, 18.0, bodyf, cut=1.0)
    m.box(bd, 0, 11.5, 2.6, 0, 18.0, 7.0, fin(                                  # a fin down its back
        lambda a, b: a > 2.6 and b - 11.5 < (7.0 - a) * 1.4, lambda p, a, b: p["green"] if b > 16 else p["blue"]))

    hd = m.bone("head", bd, (0, 18, 0))
    m.round_box(hd, 0, -1.5, 4.0, 4.6, 17.0, 25.0, headf, cut=1.4)             # the big fish head
    m.round_box(hd, 0, 4.4, 3.4, 2.4, 19.0, 25.4, solid("black"), cut=1.0)     # its black mop of fins
    for sx in (-1, 1):
        for y in (21.0, 24.0):
            spike(m, hd, (sx * 1.6, y, 6.4), (sx * 0.3, 0.3, 1), 1.0, 2.0, solid("cream"))   # pale spines
        spike(m, hd, (sx * 4.0, 19.4, 0.0), (sx * 1, -0.2, 0.4), 2.2, 2.6, solid("black"))    # jaw fins

    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 2.0, 12, 0))
        rod(m, lb, (sx * 2.0, 12.0, 0.0), (sx * 3.0, 2.4, 0.4), 2.6, legf, extend=0.6)   # long fin-legs
        m.round_box(lb, sx * 3.0, -1.4, 2.2, 3.2, 0.0, 1.6, solid("blue_dark"), cut=0.8)  # flat fin feet
        ar = m.bone(f"arm_{side}", bd, (sx * 3.4, 17, -0.5))
        rod(m, ar, (sx * 3.4, 17.0, -0.5), (sx * 5.6, 11.0, -2.4), 2.2, solid("blue"), extend=0.4)
        rod(m, ar, (sx * 5.6, 11.0, -2.4), (sx * 7.0, 5.0, -1.0), 2.0, solid("blue"), extend=0.4)
        for d in ((sx * 0.3, -1, -0.4), (sx * 0.2, -1, 0.0), (sx * 0.3, -1, 0.4)):
            spike(m, ar, (sx * 7.0, 5.0, -1.0), d, 1.2, 2.6, solid("blue_dark"))   # finned fingers
    return m
