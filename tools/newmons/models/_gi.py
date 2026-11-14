"""Shared colours and parts for the Cornera fighters (after @magikdex's Cornera region art): Chawp, Kiq, and the Gi
forms of Sawk, Kiq and Throh. Pale grey-blue quilted skin with seam lines, white plates and bandages, grey shorts with
black cuffs, black gis with white or teal belts; electric sparks (Sawk), frost fur and icicles (Kiq), flames (Throh).

Each model keeps its own SHINY dict and calls `palette(shiny)`.
"""
from __future__ import annotations

import math

from _afake import ramp_of, solid_of
from _boxmodel import rod, spike
from _route import pal, tone

BASE = {
    # Chawp / Kiq: quilted grey-blue skin
    "skin": (192, 212, 212), "skin_shade": (156, 178, 182), "seam": (120, 140, 146),
    "plate": (244, 244, 240), "shorts": (206, 206, 196), "black": (38, 38, 44), "mask": (62, 64, 70),
    "eye": (118, 124, 130), "eye_white": (250, 250, 250), "pupil": (28, 28, 32), "mouth": (92, 62, 70),
    "white": (244, 244, 240), "band": (40, 40, 46),
    # Sawk's Gi: blue skin, black gi, teal belt, white-teal sparks, red eyes
    "blue": (56, 106, 208), "blue_dark": (36, 70, 150), "teal": (150, 222, 222), "spark": (236, 252, 255),
    "red_eye": (222, 52, 40),
    # Throh's Gi: red skin, black gi, white lapels, flames, blue eyes
    "red": (214, 86, 72), "red_dark": (160, 56, 50), "flame": (252, 128, 36), "flame_hot": (255, 216, 84),
    "blue_eye": (90, 172, 242),
    # Kiq's Gi: frost fur, icicles, black star mask, teal tunic panel, yellow eyes
    "frost": (216, 244, 248), "frost_shade": (164, 214, 226), "ice": (176, 232, 252, 160), "ice_teal": (112, 196, 208),
    "gold_eye": (242, 202, 60),
}


def palette(shiny):
    """-> (P, solid, ramp) for a model with its own shiny overrides."""
    def P(v):
        return pal(BASE, shiny, v)
    return P, solid_of(P), ramp_of(P)


NORMAL_AXIS = {"east": "x", "west": "x", "up": "y", "down": "y", "north": "z", "south": "z"}


def seamed(P, key, lines, dark="seam", w=0.24, extra=None):
    """Quilted skin: `key` with seam lines where a coordinate is near a value (lines = [(axis, value)]). A face never
    gets a seam along its own normal axis (that would paint it whole). `extra(x, y, z, face, p)` may paint first."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if extra:
            c = extra(x, y, z, face, p)
            if c is not None:
                return (c if len(c) == 2 and isinstance(c[0], tuple) else (tone(c, face), None))
        pos = {"x": x, "y": y, "z": z}
        for ax, v in lines:
            if NORMAL_AXIS[face] != ax and abs(pos[ax] - v) < w:
                return tone(p[dark], face), None
        return tone(p[key], face), None
    return s


def glow(P, key):
    """A palette colour that glows."""
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return c, c
    return s


def translucent(P, key, glowing=False):
    """A see-through palette colour (RGBA): goes to the translucent shell layer."""
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return c, (c[:3] if glowing else None)
    return s


def fan(m, bone, base, n, length, width, shader, spread=0.6, up=(0, 1, 0), tip=0.45):
    """A fan of spikes from one point (flames, sparks, fur)."""
    for i in range(n):
        a = (i - (n - 1) / 2) * spread
        d = (math.sin(a) + up[0], math.cos(a) * up[1] + 0.2, up[2])
        spike(m, bone, base, d, width, length * (0.75 + 0.25 * math.cos(a)), shader, tip=width * tip)


def ring_spikes(m, bone, cy, r, degs, length, width, shader, out=1.0, rise=0.6, tip=0.45, cz=0.0, sy=None):
    """Spikes standing out from a ring round the y axis (angle 0 = front, -z; 90 = +x)."""
    for i, deg in enumerate(degs):
        a = math.radians(deg)
        dx, dz = math.sin(a), -math.cos(a)
        y = cy + (sy(i) if sy else 0)
        spike(m, bone, (dx * r, y, cz + dz * r), (dx * out, rise, dz * out), width, length, shader, tip=width * tip)


def zigzag(m, bone, pts, t, shader):
    """A jagged lightning-bolt rod through points."""
    for a, b in zip(pts, pts[1:]):
        rod(m, bone, a, b, t, shader, extend=0.6)


def eye_disc(p, x, y, cx, cy, r, iris, pupil=True, ry=None, glint=True):
    """A round eye at (cx, cy) on a front face -> colour or None: white, then iris, pupil and a glint."""
    ry = ry or r
    d = math.hypot((x - cx) / r, (y - cy) / ry)
    if d >= 1:
        return None
    if glint and math.hypot(x - (cx + r * 0.3), y - (cy + ry * 0.35)) < r * 0.22:
        return p["eye_white"]
    if pupil and d < 0.35:
        return p["pupil"]
    if d < 0.72:
        return p[iris]
    return p["eye_white"]


def in_tri(x, y, a, b, c):
    """Is (x, y) inside triangle abc?"""
    def side(p, q, r):
        return (p[0] - r[0]) * (q[1] - r[1]) - (q[0] - r[0]) * (p[1] - r[1])
    d1, d2, d3 = side((x, y), a, b), side((x, y), b, c), side((x, y), c, a)
    neg = d1 < 0 or d2 < 0 or d3 < 0
    pos = d1 > 0 or d2 > 0 or d3 > 0
    return not (neg and pos)


def near_seg(x, y, a, b, w):
    """Is (x, y) within w of segment ab?"""
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    t = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / max(1e-9, dx * dx + dy * dy)))
    return math.hypot(x - ax - t * dx, y - ay - t * dy) < w
