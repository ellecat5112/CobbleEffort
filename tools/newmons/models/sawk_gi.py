"""Sawk's Gi form (Fighting/Electric), after @magikdex's Cornera region art: Sawk crackling with lightning. A blue
karateka in a black gi: the V of its open jacket edged with a pale teal collar, a teal belt whose tails are jagged
bolts, black trousers patched with teal triangles, big blue chopping hands, a black headband plate with a long horn
swept up to one side, glaring red eyes, and a great white-teal mane of jagged electric spikes round its head and
shoulders, with more sparking back off its sleeves.

Shiny: a navy body and yellow lightning.

Front is -z, y is up. 39 units tall; baseScale 0.62 (1.5 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _gi import eye_disc, in_tri, near_seg, palette, ring_spikes, seamed, zigzag
from _route import tone

SHINY = {"blue": (40, 58, 120), "blue_dark": (26, 38, 86), "teal": (250, 226, 96), "spark": (255, 250, 200)}
P, solid, ramp = palette(SHINY)
SCALE = 0.62
HITBOX = [1.3, 2.45]
KIND = "biped"
K = 4
HEIGHT = 39
LOOK = ("a blue karateka in a black gi with a teal collar and lightning-bolt belt tails, a horned black headband, red "
        "eyes and a great white-teal mane of jagged electric spikes")
HY = 30.4


def spark(x, y, z, face, variant, box=None, **k):
    """Electric spikes: teal at the root, glowing white at the tips."""
    p = P(variant)
    t = 0.0
    if box is not None:
        t = max(0.0, min(1.0, (box.lo[2] + box.size[2] - z) / max(1e-6, box.size[2])))
    c = p["teal"] if t < 0.3 else p["spark"]
    return c, (c if t >= 0.3 else None)


def gi_top(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and y > 18.6:
        w = (y - 18.6) * 0.62
        if abs(x) < w - 0.7:
            return tone(p["blue"], face), None                             # the chest in the open V
        if abs(x) < w + 0.5:
            return tone(p["teal"], face), None                             # the collar
    return tone(p["black"], face), None


def trousers(x, y, z, face, variant, **k):
    p = P(variant)
    for cy in (5.0, 10.6):                                              # teal triangle patches
        if face in ("north", "east", "west") and in_tri(x if face == "north" else z, y,
                                                      (-1.0, cy - 1.0), (1.0, cy - 1.0), (0.0, cy + 1.2)):
            return tone(p["teal"], face), None
    return tone(p["black"], face), None


def head(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if near_seg(x, y, (sx * 0.5, HY + 0.2), (sx * 2.4, HY + 0.9), 0.55):
                if math.hypot(x - sx * 1.5, y - HY - 0.4) < 0.42:
                    return p["red_eye"], None                            # red eyes in a hard glare
                return p["eye_white"], None
        if abs(x) < 0.25 and HY - 2.6 < y < HY - 0.6:
            return tone(p["blue_dark"], face), None                         # a ridge down the face
    return tone(p["blue"], face), None


def build() -> Model:
    m = Model("sawk_gi")
    top = m.bone("sawk_gi", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    m.round_box(bd, 0, 0.2, 3.8, 2.8, 13.6, 17.4, solid("black"), cut=1.0)        # hips
    m.round_box(bd, 0, 0.2, 4.2, 3.2, 16.6, 18.2, solid("teal"), cut=1.1)         # the teal belt
    m.round_box(bd, 0, 0.2, 4.6, 3.2, 18.0, 25.6, gi_top, cut=1.2)                # the open gi jacket
    zigzag(m, bd, [(1.6, 17.2, -3.0), (4.6, 15.6, -3.4), (3.4, 13.2, -3.0), (7.0, 11.2, -2.0), (5.8, 8.8, -1.2)],
           1.3, spark)                                                            # bolt-shaped belt tails
    zigzag(m, bd, [(2.4, 17.2, -2.6), (6.4, 16.8, -1.2), (5.6, 14.6, 0.6), (9.6, 13.4, 2.0)], 1.2, spark)
    hd = m.bone("head", bd, (0, 25.5, 0))
    m.round_box(hd, 0, -0.2, 1.6, 1.6, 25.0, HY - 3.0, solid("blue"), cut=0.5)           # neck
    m.round_box(hd, 0, -0.4, 2.7, 2.9, HY - 3.6, HY + 2.6, head, cut=1.0)          # a long head
    m.round_box(hd, 0, -0.4, 2.0, 2.2, HY + 2.5, HY + 3.4, head, cut=0.7)
    spike(m, hd, (0, HY - 3.0, -2.8), (0, -0.5, -1), 1.6, 1.8, solid("blue"))      # pointed chin
    m.round_box(hd, 0, -0.4, 3.0, 3.2, HY + 1.0, HY + 2.4, solid("black"), cut=1.1)   # the headband plate
    spike(m, hd, (1.6, HY + 2.0, -1.6), (1.0, 1.0, 0.25), 2.0, 8.0, solid("black"), tip=1.0)  # swept horn
    mane = m.bone("mane", bd, (0, 24, 0))                                        # the electric mane
    ring_spikes(m, mane, 24.6, 4.8, list(range(62, 302, 17)), 6.4, 2.6, spark, out=1.0, rise=0.9,
                sy=lambda i: (i % 3) * 0.9)
    ring_spikes(m, mane, 27.4, 3.8, list(range(90, 280, 30)), 5.6, 2.2, spark, out=0.6, rise=1.2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 5.0, 24.0, 0))
        m.round_box(a, sx * 5.4, 0.2, 1.8, 1.8, 22.2, 25.6, solid("black"), cut=0.7)   # shoulders
        rod(m, a, (sx * 5.6, 23.4, 0.2), (sx * 8.4, 19.2, -0.6), 3.0, solid("black"))   # sleeves
        rod(m, a, (sx * 8.4, 19.2, -0.6), (sx * 7.8, 25.4, -4.0), 2.6, seamed(P, "blue", [("y", 21.4)], dark="blue_dark"))
        m.round_box(a, sx * 7.8, -4.4, 1.5, 0.9, 24.6, 29.8, seamed(P, "blue", [("y", 26.8), ("y", 28.2)],
                                                                   dark="blue_dark"), cut=0.4)   # chopping hands
        m.box(a, sx * 7.8 - (2.4 if sx > 0 else -1.2), 25.0, -4.8, sx * 7.8 - (1.2 if sx > 0 else -2.4), 26.6, -4.0,
              solid("blue"))                                                      # thumbs
        for i in range(3):                                                       # sparks off the sleeves
            spike(m, a, (sx * 8.0, 20.2 + i * 1.0, 0.4), (sx * 0.8, 0.5 + 0.3 * i, 1.0), 1.8, 4.6 + i, spark, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                          # wide stance, baggy trousers
        lg = m.bone(nm, top, (sx * 2.6, 14.5, 0))
        rod(m, lg, (sx * 2.6, 14.8, 0), (sx * 6.2, 8.2, -1.0), 3.8, trousers)
        rod(m, lg, (sx * 6.2, 8.2, -1.0), (sx * 6.8, 2.2, 0.0), 3.4, trousers)
        m.round_box(lg, sx * 6.8, -1.2, 1.8, 2.8, 0, 2.6, seamed(P, "blue", [("z", -1.4), ("z", -3.0)], dark="blue_dark"),
                    cut=0.8)                                                      # blue feet
    return m
