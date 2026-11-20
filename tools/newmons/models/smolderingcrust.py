"""Smoldering Crust (Ground/Dragon), the ancient paradox Groudon, built from boxes after a picture the user shared
(artist not named, no name given; our name).

A primeval Groudon crawling low on four limbs: a broad red hide ridged with grey bone spikes down its back and along
its heavy tail, traced with dark blue lines, its feet ending in black claws. Searing heat pours from the vents on its
back in jagged yellow plumes, and its blunt head carries a ridge of short spikes over glowing yellow eyes.

Shiny: obsidian black with orange heat.

Front is -z, y is up. 36 units tall (to the heat plumes); about 3 blocks tall and 5 long.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _pgen1 import CLEAR, tri
from _rotomform import bolt_shape
from _route import mix, pal, tone

HEIGHT = 36
SCALE = round(3.0 * 16 / HEIGHT, 3)
HITBOX = [3.4, HEIGHT / 16]
KIND = "quadruped"
K = 3
LOOK = ("a primeval red Groudon crawling on four limbs, ridged with grey bone spikes and traced with dark blue lines, "
        "with black claws and jagged yellow heat plumes pouring from its back")

BASE = {"red": (196, 44, 52), "red_dark": (140, 28, 38), "red_light": (226, 90, 96), "line": (40, 56, 120),
        "spike": (196, 196, 204), "spike_dark": (130, 130, 140), "claw": (40, 36, 44), "heat": (255, 236, 140),
        "heat_edge": (240, 190, 60), "eye": (255, 220, 70), "mouth": (90, 20, 26)}
SHINY = {"red": (54, 52, 60), "red_dark": (30, 30, 36), "red_light": (88, 86, 96), "line": (240, 120, 40),
         "heat": (255, 170, 80), "heat_edge": (240, 110, 30), "eye": (255, 150, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def hidef(x, y, z, face, variant, **k):
    """Red hide traced with dark blue lines (Groudon's markings, in loops along the flanks)."""
    p = P(variant)
    if face in ("east", "west", "up"):
        a = z if face != "up" else z
        b = y if face != "up" else abs(x) * 1.6 + 16
        line = 15.5 + 2.2 * math.sin(a * 0.45)
        if abs(b - line) < 0.35 or (abs((a % 7.0) - 3.5) < 0.3 and abs(b - line) < 2.6):
            return p["line"], None
    return tone(p["red_light"] if face == "up" else p["red"], face), None


def legf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red"] if face != "down" else p["red_dark"], face), None


def headf(eye_y, eye_z):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("east", "west") and math.hypot(z - eye_z, (y - eye_y) * 1.6) < 0.7:
            return p["eye"], p["eye"]
        if face == "north" and abs(y - eye_y) < 0.4 and abs(x) > 1.0:
            return p["eye"], p["eye"]
        return tone(p["red"], face), None
    return s


def plumef(w, h, x0, y0, flip=False):
    """A jagged yellow heat plume rising from a vent (an xy plane)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u, v = (x - x0) / w, (y - y0) / h
        if flip:
            u = 1 - u
        if not (0 <= u <= 1 and 0 <= v <= 1) or not bolt_shape(u, v):
            return CLEAR
        c = p["heat"] if 0.35 < u < 0.65 else p["heat_edge"]
        return c, c
    return s


def build() -> Model:
    m = Model("smolderingcrust")
    neck = ((0, 15.0, -17.0), (0, 15.5, -21.0))
    head_len, head_w, head_h = 9.0, 4.6, 4.4
    hx, hy, hz = neck[-1]
    eye_y, eye_z = hy + head_h * 0.25, hz - head_len * 0.35
    mats = {"skin": hidef, "belly": solid("red_dark"), "neck": hidef, "head": headf(eye_y, eye_z),
            "snout": solid("red"), "jaw": solid("red_dark"), "mouth": solid("mouth"), "tooth": solid("spike"),
            "tongue": solid("mouth"), "leg_upper": hidef, "leg_lower": legf, "paw": legf, "claw": solid("claw"),
            "tail": hidef}
    a = quadruped(m, mats, "smolderingcrust", length=32.0, body_y=12.0, body_rx=8.0, body_ry=5.6, chest_bulk=1.12,
                  neck=neck, head_len=head_len, head_w=head_w, head_h=head_h, snout=0.4, mouth_open=8, teeth=4,
                  leg_bulk=1.6, tail=((0, 13.0, 21.0), (0, 11.0, 28.0), (0, 8.0, 34.0), (0, 5.0, 39.0)),
                  tail_r=(4.4, 3.4, 2.4, 1.4), toes=3)
    bd, hd, tl = a["body"], a["head"], a["tail"]
    for i in range(7):                                                           # bone spikes down the back
        z = -12.0 + i * 4.2
        h = 4.6 - abs(i - 2.5) * 0.4
        for sx in (-1, 1):
            spike(m, bd, (sx * 3.0, 17.0, z), (sx * 0.4, 1, 0.4), 2.0, h, solid("spike"), tip=0.8)
    for sx in (-1, 1):                                                           # and on the flanks
        for z in (-8.0, 0.0, 8.0):
            spike(m, bd, (sx * 8.0, 13.0, z), (sx, 0.3, 0.3), 1.8, 3.2, solid("spike"), tip=0.7)
    for i, z in enumerate((20.0, 25.0, 30.0, 35.0)):                             # down the tail
        spike(m, tl, (0, 15.0 - i * 2.4, z), (0, 1, 0.6), 2.2 - i * 0.3, 3.6 - i * 0.5, solid("spike"), tip=0.7)
    top = a["skull_top"]
    for i in range(4):                                                           # ridge of short head spikes
        spike(m, hd, (0, top - 0.2, hz - 3.6 + i * 1.6), (0, 1, 0.5), 1.4, 2.0 + 0.4 * i, solid("spike"), tip=0.6)
    heat = m.bone("mane", bd, (0, 17.0, 0))                                      # heat plumes from the back
    for x0, z, w, h, fl in ((-9.0, -6.0, 9.0, 17.0, False), (-2.5, 0.0, 9.0, 19.0, True), (2.5, 6.0, 9.0, 16.0, False)):
        m.box(heat, x0, 17.0, z, x0 + w, 17.0 + h, z, plumef(w, h, x0, 17.0, fl))
    return m
