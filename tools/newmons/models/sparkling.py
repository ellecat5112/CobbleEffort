"""Sparkling, the Starling Pokémon (Electric/Flying; the user's design, our name): a tiny round black starling with a
yellow hood that sweeps back into a pointed crest, a dark grey mask with huge glowing magenta eyes, a short black beak,
white patches on its wings, a stubby tail and thin pale legs. Alone it is timid; with its ability Murmuration it calls
thousands of its kind into its giant Swarm Form (sparkling_swarm.py).

Front is -z, y is up. 9 units tall; baseScale 0.55 (0.3 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _route import tone
from _starling import P, eye_on, solid

SCALE = 0.55
HITBOX = [0.5, 0.56]
KIND = "biped"
K = 8
HEIGHT = 9
LOOK = ("a tiny round black starling with a yellow hood and crest, huge glowing magenta eyes in a dark mask, white wing "
        "patches and thin pale legs")
HY = 6.6


def head(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        e = eye_on(p, z + 1.1, y - HY + 0.1, 1.2)
        if e:
            return e
        if y < HY + 1.2 and z < 0.4:
            return tone(p["mask"], face), None                       # the dark mask round its eyes
    if face == "north":
        for sx in (-1, 1):                                           # the big eyes wrap round the front corners
            e = eye_on(p, x - sx * 1.45, y - HY - 0.1, 0.85)
            if e:
                return e
        if y < HY + 1.0:
            return tone(p["mask"], face), None
    if y > HY + 0.6 or z > 0.4:
        return tone(p["yellow"], face), None                         # the yellow hood over its head and nape
    return tone(p["charcoal"], face), None


def body(x, y, z, face, variant, **k):
    p = P(variant)
    if z > 0.8 and y > 4.4:
        return tone(p["yellow"], face), None                         # the hood runs down its back
    return tone(p["black"] if y > 2.6 else p["charcoal"], face), None


def wing(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y - 3.8) < 0.8 and -0.6 < z < 1.4:
        return tone(p["white"], face), None                          # the white wing patch
    return tone(p["black"], face), None


def build() -> Model:
    m = Model("sparkling")
    top = m.bone("sparkling", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3.5, 0))
    m.round_box(bd, 0, 0.2, 2.2, 2.6, 1.6, 5.4, body, cut=0.8)
    hd = m.bone("head", bd, (0, 5.4, -0.4))
    m.round_box(hd, 0, -0.4, 2.2, 2.0, HY - 1.8, HY + 2.0, head, cut=0.8)
    spike(m, hd, (0, HY + 1.8, 0.4), (0, 1.0, 0.7), 1.6, 2.4, solid("yellow"), tip=0.8)      # the pointed crest
    spike(m, hd, (0, HY - 0.6, -2.2), (0, -0.25, -1), 1.2, 1.8, solid("beak"), tip=0.6)       # the beak
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        w = m.bone(nm, bd, (sx * 2.2, 4.6, 0))
        x0, x1 = sorted((sx * 2.0, sx * 2.9))
        m.box(w, x0, 2.6, -1.0, x1, 5.0, 2.4, wing)
    tl = m.bone("tail", bd, (0, 2.8, 2.6))
    m.box(tl, -1.0, 2.4, 2.4, 1.0, 3.2, 4.8, solid("black"), rotation=(-20, 0, 0), pivot=(0, 2.8, 2.6))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 0.9, 1.8, 0))
        rod(m, lg, (sx * 0.9, 1.8, 0.2), (sx * 1.0, 0.3, 0.0), 0.6, solid("leg"), extend=0.2)
        m.box(lg, sx * 1.0 - 0.5, 0, -1.2, sx * 1.0 + 0.5, 0.5, 0.6, solid("leg"))             # toes
    return m
