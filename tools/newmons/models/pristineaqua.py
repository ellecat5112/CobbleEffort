"""Pristine Aqua (Water/Rock), the ancient paradox Kyogre, built from boxes after @MadZygardeCore's art (sub_arashii;
the art's own name).

A primeval Kyogre of slate blue: a broad whale body with a white mouth and lips, fierce red eyes, a red line running
from its eyes along its flanks, and red ringed markings on its great pectoral fins, which end in rows of heavy black
claws. A ridged three-pronged fluke trails behind.

Shiny: sea-green with gold markings.

Front is -z, y is up. 17 units tall; about 2.1 blocks tall and 4 long.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _kyogre import CY, FIN_LEN, FIN_W, body, dorsal, fin_box, fluke
from _regi import lit
from _route import pal, tone

HEIGHT = 17
SCALE = round(2.1 * 16 / HEIGHT, 3)
HITBOX = [3.2, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a primeval slate-blue Kyogre with a white mouth, red eyes, a red flank line, red ringed markings on its great "
        "fins and rows of heavy black claws")

BASE = {"slate": (86, 128, 176), "slate_dark": (56, 88, 130), "slate_light": (130, 170, 210), "white": (236, 240, 246),
        "red": (214, 54, 66), "eye": (220, 40, 50), "pupil": (40, 16, 20), "claw": (50, 54, 64),
        "claw_light": (150, 156, 170)}
SHINY = {"slate": (70, 150, 130), "slate_dark": (44, 108, 94), "slate_light": (120, 196, 176), "red": (236, 186, 60),
         "eye": (236, 186, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def hullf(x, y, z, face, variant, **k):
    """Slate blue; a white mouth across the front, red eyes above it, a red line from the eyes down the flanks."""
    p = P(variant)
    if face == "north" and z < -6:
        if abs(y - (CY - 0.6)) < 0.6 and abs(x) < 6.0:
            return p["slate_dark"], None                                    # the mouth line
        if y < CY - 0.6:
            return lit(p["white"], face, y, CY, 6), None
        for sx in (-1, 1):
            r = math.hypot(x - sx * 3.6, y - (CY + 2.4))
            if r < 0.6:
                return p["pupil"], None
            if r < 1.2:
                return p["eye"], p["eye"]
    if face in ("east", "west"):
        line = CY + 2.0 - 0.18 * (z + 8.0)
        if abs(y - line) < 0.4 and z > -9:
            return p["red"], None
        if y < CY - 1.2 and z < -4:
            return lit(p["white"], face, y, CY, 6), None
    return lit(p["slate"] if face != "down" else p["white"], face, y, CY, 6), None


def finf(sx):
    """A pectoral fin: slate, with a red ring and three red lines to its edge on its top face."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u = sx * (x - sx * 6.0)                                              # out along the fin
        w = z - (box.lo[2] + box.size[2] / 2)                                # across it
        if face in ("up", "down"):
            r = math.hypot(u - 6.0, w)
            if abs(r - 2.2) < 0.4:
                return p["red"], None
            if r > 2.2 and u > 6.0 and min(abs(w), abs(w - (u - 6.0) * 0.8), abs(w + (u - 6.0) * 0.8)) < 0.35:
                return p["red"], None
        return tone(p["slate"] if face != "down" else p["slate_dark"], face), None
    return s


def build() -> Model:
    m = Model("pristineaqua")
    top = m.bone("pristineaqua", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    body(m, bd, hullf)
    dorsal(m, bd, solid("slate_dark"))
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                         # great clawed pectoral fins
        fn = m.bone(nm, bd, (sx * 6.0, 8.0, -1.0))
        fin_box(m, fn, sx, finf(sx))
        a, d = math.radians(22.0), math.radians(18.0)
        for i in range(4):                                                     # heavy black claws on the fin's edge
            w = -FIN_W / 2 + 1.2 + i * (FIN_W - 2.4) / 3
            lx, lz = FIN_LEN, w                                                # in the fin's own frame
            px = sx * 6.0 + sx * lx * math.cos(a) * math.cos(d)
            py = 8.0 - lx * math.sin(d)
            pz = -1.0 + lz - lx * math.sin(a)
            spike(m, fn, (px, py, pz), (sx * 0.5, -0.9, -0.4), 1.8, 3.8, solid("claw"), tip=0.7)
    tl = m.bone("tail", bd, (0, CY, 11.0))
    fluke(m, tl, solid("slate_dark"))
    return m
