"""Scorpaddle, the Sea Scorpion Pokémon (Bug/Water): a round little eurypterid revived from a Telson Fossil. A
domed yellow shell in ringed segments with a stepped magenta stripe down the middle, two shiny dark eyes at the
front, two big brown swimming paddles and two smaller ones at the back, little legs underneath and a thin pink telson
spike standing up from its tail.

Front is -z, y is up. 14 units tall to the spike's tip; baseScale 0.55 (0.4 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix, rod, spike
from _eurypterid import P, darkf, paddlef, spikef
from _route import tone

SCALE = 0.55
HITBOX = [0.6, 0.4]
KIND = "floater"
K = 6
HEIGHT = 14
LOOK = ("a round yellow sea scorpion with a stepped magenta stripe down its ringed shell, big dark eyes, brown "
        "swimming paddles and a pink telson spike")


def shellf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot((x - sx * 1.6) / 0.8, (y - 3.4) / 1.0)
            if d < 1:
                return (p["eye_glint"] if math.hypot(x - sx * 1.6 + 0.3, y - 3.8) < 0.3 else p["eye"]), None
    seg = (z + 4.5) % 1.8
    w = 1.0 + 0.5 * (int((z + 4.5) / 1.8) % 2)                           # the stripe steps wider and narrower
    if face == "up" and abs(x) < w:
        return tone(p["mark"] if seg > 0.25 else p["mark_light"], face), None
    if face == "north" and abs(x) < 1.0 and y > 4.6:
        return tone(p["mark"], face), None
    if face in ("up", "east", "west") and seg < 0.25:
        return tone(p["shell_shade"], face), None                       # ring seams between segments
    if face == "down":
        return tone(p["belly"], face), None
    return tone(p["shell_light"] if face == "up" else p["shell"], face), None


def build() -> Model:
    m = Model("scorpaddle")
    top = m.bone("scorpaddle", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    m.round_box(bd, 0, 0, 4.5, 4.5, 0.8, 5.5, shellf, cut=1.8)                  # domed shell
    m.round_box(bd, 0, 0.3, 3.4, 3.6, 5.2, 6.8, shellf, cut=1.4)
    for nm, sx in (("arm_left", -1), ("arm_right", 1)):                          # big front paddles
        ar = m.bone(nm, bd, (sx * 4, 3, -1))
        rod(m, ar, (sx * 4, 3, -1.5), (sx * 8, 3.8, -3), 1.4, paddlef(), extend=0.3, t2=0.8)
        m.box(ar, sx * 7.6 - 1.2, 3.2, -4.6, sx * 7.6 + 1.2, 3.8, -1.8, paddlef(),
              rotation=(0, sx * 20, 0), pivot=(sx * 7.6, 3.5, -3.2))              # paddle blade
    for sx in (-1, 1):
        rod(m, bd, (sx * 4, 2.4, 2.5), (sx * 7, 3, 4), 1.2, paddlef(), extend=0.3, t2=0.7)   # smaller back paddles
        for z in (-2.5, -0.5):
            rod(m, bd, (sx * 3, 1, z), (sx * 4.5, 0, z - 0.8), 0.8, darkf, extend=0.2)    # little legs
    tl = m.bone("tail", bd, (0, 5, 4))
    rod(m, tl, (0, 5, 4), (0, 7, 5.5), 1.6, paddlef(), extend=0.3)                # tail base
    spike(m, tl, (0, 6.8, 5.4), (0, 1, 0.35), 1.2, 7, spikef, tip=0.6)           # pink telson spike
    return m
