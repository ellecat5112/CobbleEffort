"""Mousense, the Whisker Pokémon (Normal), built from boxes after the concept art the user shared (the art's own name).

A chubby little mouse sitting up, nose in the air with its eyes peacefully closed: cream fur with a light brown back
and cheeks, a pointed snout with a pink nose and a big buck tooth, long pale whiskers fanning out on both sides, big
round dark ears with pink insides, small pink paws and feet, and a long pink tail.

Shiny (from the art): pale blue-white with dark grey ears, magenta ear insides and a dark mask over its eyes.

Front is -z, y is up. 14 units tall to its ears; baseScale 0.42 (0.3 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, mix, rod
from _route import pal, tone
from _sense import closed_eyes, ear_disc, solid, whisker

SCALE = 0.42
HITBOX = [0.4, 0.35]
KIND = "biped"
K = 6
HEIGHT = 14
LOOK = ("a chubby cream mouse sitting up with its eyes closed and nose in the air, long whiskers, big round dark ears, "
        "a buck tooth and pink paws and tail")

BASE = {"fur": (240, 222, 188), "back": (204, 164, 118), "ear": (84, 60, 74), "ear_in": (234, 150, 182),
        "pink": (234, 160, 184), "whisker": (250, 240, 214), "tooth": (252, 252, 252), "line": (66, 46, 44),
        "mask": None}
SHINY = {"fur": (196, 222, 255), "back": (132, 172, 232), "ear": (62, 66, 84), "ear_in": (228, 108, 204),
         "mask": (58, 62, 80), "whisker": (244, 250, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("south", "up") or (face in ("east", "west") and z > 0.2):
        return tone(p["back"], face), None
    return tone(p["fur"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        if closed_eyes(x, y, 1.35, 9.9, 0.7, None):
            return (p["fur"] if p["mask"] else p["line"]), None
        if p["mask"] and abs(x) < 2.3 and 9.3 < y < 10.7:
            return p["mask"], None                                       # the shiny's dark mask
        return tone(p["fur"], face), None
    if face == "up" or face == "south":
        return tone(p["back"], face), None
    return tone(p["fur"], face), None


def build() -> Model:
    m = Model("mousense")
    top = m.bone("mousense", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    m.round_box(bd, 0, 0.4, 3.9, 3.4, 0.8, 6.2, bodyf, cut=1.3)              # chubby round body
    hd = m.bone("head", bd, (0, 6.6, -0.4))
    m.round_box(hd, 0, -0.6, 3, 2.6, 6.4, 11.4, headf, cut=0.8)               # big round head
    m.box(hd, -1, 7.2, -4.4, 1, 9.2, -3, bodyf)                                # little snout
    m.box(hd, -0.5, 8.4, -5, 0.5, 9.4, -4.2, solid(BASE, SHINY, "pink"))      # pink nose
    m.box(hd, -0.5, 6.3, -4.1, 0.5, 7.3, -3.1, solid(BASE, SHINY, "tooth"))   # buck tooth
    for sx in (-1, 1):
        for dy, dz in ((0.5, -0.3), (0, 0), (-0.5, 0.3)):                     # long whiskers
            whisker(m, hd, (sx * 0.9, 8.2 + dy, -4.0), (sx * 7, 8.4 + dy * 2.4, -3.6 + dz), BASE, SHINY, thick=0.22)
        m.box(hd, sx * 2.5 - 2, 10.2, -0.8, sx * 2.5 + 2, 14.2, -0.8, ear_disc(BASE, SHINY, sx * 2.5, 12.2, 2),
              rotation=(0, sx * 10, sx * -14), pivot=(sx * 2.5, 10.6, -0.8))  # big round ears
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                        # paws held in front
        a = m.bone(nm, bd, (sx * 1.6, 5.4, -2.6))
        m.box(a, sx * 1.4 - 0.6, 4.2, -3.8, sx * 1.4 + 0.6, 5.4, -2.6, solid(BASE, SHINY, "pink"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 1.5, -0.5))
        m.box(lg, sx * 1.8 - 1, 0, -3.2, sx * 1.8 + 1, 1, 0.2, solid(BASE, SHINY, "pink"))
    tail = m.bone("tail", bd, (0, 2, 3.4))
    chain(m, tail, [(0, 2, 3.4), (0.6, 1.2, 6), (2, 1.0, 8), (3.6, 1.8, 9.2)], [0.8, 0.7, 0.6], solid(BASE, SHINY, "pink"))
    return m
