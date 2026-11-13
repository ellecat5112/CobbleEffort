"""Pterygant, the Sea Scorpion Pokémon (Bug/Water), Scorpaddle evolved: a giant eurypterid. A broad, flattened
yellow head shield with spiked points and magenta triangle markings, two dark eyes and short dark feelers at the
front, a body of overlapping spiked yellow plates, each marked with magenta, great brown swimming paddles banded with
pink sweeping back on both sides, small dark walking legs underneath and a long segmented brown tail ending in a pink
telson spike raised behind it.

Front is -z, y is up. 22 units tall to the spike's tip, 40 long; baseScale 0.75 (1.9 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix, rod, spike
from _eurypterid import P, darkf, paddlef, spikef
from _route import tone

SCALE = 0.75
HITBOX = [1.4, 0.9]
KIND = "floater"
K = 4
HEIGHT = 22
LOOK = ("a giant yellow sea scorpion with a spiked head shield and overlapping plates marked magenta, great brown "
        "swimming paddles banded pink and a long segmented tail ending in a pink telson spike")


def platef(z0):
    """A yellow plate with a magenta triangle pointing forward on top, darker at its back edge."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "up":
            t = z - z0                                                   # 0 at the plate's front
            if t > 0 and abs(x) < t * 0.45 and t < 3.5:
                return tone(p["mark"], face), None
        if face in ("east", "west", "up") and z > z0 + 4.2:
            return tone(p["shell_shade"], face), None
        if face == "down":
            return tone(p["belly"], face), None
        return tone(p["shell_light"] if face == "up" else p["shell"], face), None
    return s


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot((x - sx * 2.2) / 0.9, (y - 4.4) / 1.0) < 1:
                return (p["eye_glint"] if math.hypot(x - sx * 2.2 + 0.3, y - 4.8) < 0.3 else p["eye"]), None
        if abs(x) < 1.2 - (y - 5.5) * 0.4 and y > 5:
            return tone(p["mark"], face), None
    if face == "up":
        if abs(x) < (z + 13) * 0.5 and -13 < z < -9:
            return tone(p["mark"], face), None                           # magenta triangle on the head shield
    if face == "down":
        return tone(p["belly"], face), None
    return tone(p["shell_light"] if face == "up" else p["shell"], face), None


def banded(x, y, z):
    return abs(((z + x * 0.3) % 3.4) - 2.6) < 0.45


def build() -> Model:
    m = Model("pterygant")
    top = m.bone("pterygant", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    hd = m.bone("head", bd, (0, 5, -9))
    m.round_box(hd, 0, -10.5, 6, 3.6, 1.5, 7, headf, cut=1.8)                     # broad head shield
    for sx in (-1, 1):
        spike(m, hd, (sx * 5, 5.5, -10), (sx * 0.6, 0.8, 0.4), 2.2, 3.5, platef(-14), tip=1)   # spiked corners
        rod(m, hd, (sx * 1.2, 3, -14), (sx * 2.8, 1, -17.5), 0.6, darkf, extend=0.2)            # short feelers
        rod(m, hd, (sx * 2.2, 2, -13.5), (sx * 4.5, 0, -15.5), 0.6, darkf, extend=0.2)
    spike(m, hd, (0, 6.8, -11), (0, 1, 0.5), 2.6, 3, platef(-14), tip=1.2)
    # overlapping plates down the body, each a little narrower, with spiked sides
    for i, (z0, w, hgt) in enumerate(((-7.5, 6.4, 9), (-2.5, 6, 8.6), (2.5, 5.2, 8), (7, 4.2, 7.2))):
        m.round_box(bd, 0, z0 + 2.6, w, 2.8, 1.5, hgt, platef(z0), cut=1.4)
        for sx in (-1, 1):
            spike(m, bd, (sx * (w - 0.8), hgt - 1, z0 + 2), (sx * 0.8, 0.5, 0.8), 2, 3.2, platef(z0), tip=0.9)
        spike(m, bd, (0, hgt - 0.3, z0 + 2), (0, 1, 0.8), 2.2, 2.6 - i * 0.3, platef(z0), tip=0.9)
    # great banded swimming paddles sweeping back
    for nm, sx in (("arm_left", -1), ("arm_right", 1)):
        ar = m.bone(nm, bd, (sx * 6, 4, -4))
        pts = [(sx * 6, 4, -4), (sx * 10, 4.5, -1), (sx * 13, 4.5, 3), (sx * 15, 4, 8)]
        for a, b, t in zip(pts, pts[1:], (2, 2.2, 2.6)):
            rod(m, ar, a, b, t, paddlef(banded), extend=0.6, t2=1.2)
        m.box(ar, sx * 15 - 2.2, 3.4, 6.5, sx * 15 + 2.2, 4.6, 12, paddlef(banded),
              rotation=(0, sx * -20, 0), pivot=(sx * 15, 4, 8))                  # the paddle blade
    for sx in (-1, 1):                                                           # small dark walking legs
        for z in (-8, -5, -2):
            rod(m, bd, (sx * 4, 2, z), (sx * 7, 0, z - 1.5), 0.8, darkf, extend=0.2)
    # the long segmented tail, raised, ending in the pink telson spike
    tl = m.bone("tail", bd, (0, 5, 10))
    pts = [(0, 5, 10), (0, 6.5, 14), (0, 8.5, 18), (0, 11, 21.5), (0, 14, 24)]
    for a, b, t in zip(pts, pts[1:], (3.4, 3, 2.6, 2.2)):
        rod(m, tl, a, b, t, paddlef(lambda x, y, z: (z % 4) < 0.6), extend=0.6)
    for a in pts[1:4]:
        for sx in (-1, 1):
            spike(m, tl, (sx * 1.2, a[1] + 0.6, a[2]), (sx * 0.8, 0.6, 0.5), 1, 2.2, darkf)   # little side spines
    spike(m, tl, (0, 13.6, 23.6), (0, 0.9, 0.7), 1.6, 9, spikef, tip=0.8)       # pink telson spike
    return m
