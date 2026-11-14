"""Shared colours and parts for the CobbleEffortian Magnemite line and Magnalien, after the art of the A. Fakemon
fanpage (Magnalien is its name; the forms are its UFO variants of Magnemite and Magneton): silver flying saucers
with big green cyclops eyes, antennae tipped with balls, rings of coloured running lights, and tractor beams.

Shiny: gold hulls with violet eyes.
"""
from __future__ import annotations

import math

from _afake import ramp_of, solid_of
from _boxmodel import mix, rod
from _route import pal, tone

BASE = {"silver": (196, 204, 214), "silver_light": (232, 236, 242), "steel": (124, 132, 146), "dark": (44, 46, 54),
        "eye": (110, 220, 150), "eye_light": (200, 250, 220), "eye_dark": (30, 90, 70), "red": (226, 60, 50),
        "yellow": (250, 222, 70), "green": (90, 200, 80), "beam": (250, 236, 110, 160), "beam_red": (240, 90, 80, 150)}
SHINY = {"silver": (226, 196, 120), "silver_light": (246, 226, 168), "steel": (176, 140, 70), "eye": (190, 120, 240),
         "eye_light": (230, 200, 255), "eye_dark": (80, 40, 120)}


def P(v):
    return pal(BASE, SHINY, v)


solid = solid_of(P)
ramp = ramp_of(P)


def eye_at(p, dx, dy, r):
    """A big glowing green cyclops eye: a light ring, a green iris, a dark pupil dot. -> (colour, glow) or None."""
    d = math.hypot(dx, dy)
    if d > r:
        return None
    if d < r * 0.2:
        return p["eye_dark"], None
    c = p["eye_light"] if d > r * 0.8 or (dx < -r * 0.2 and dy > r * 0.25 and d < r * 0.55) else p["eye"]
    return c, c


def hull(eye=None, band=None, lights=None):
    """Silver hull: a dark band between y band[0] and band[1], an eye on the front at eye = (cx, cy, r), running
    lights round the band = (y, count, radius) coloured red/green/yellow."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if eye and face == "north":
            e = eye_at(p, x - eye[0], y - eye[1], eye[2])
            if e:
                return e
        if band and band[0] <= y <= band[1] and face not in ("up", "down"):
            if lights:
                a = math.atan2(x, -z)
                n = lights[1]
                k_ = round(a / (2 * math.pi) * n)
                if abs(a - k_ * 2 * math.pi / n) < 0.18:
                    c = (p["red"], p["green"], p["yellow"])[k_ % 3]
                    return c, c
            return p["dark"], None
        return tone(p["silver_light"] if face == "up" else p["silver"], face), None
    return s


def antenna(m, bone, base, top, ball=1.4):
    rod(m, bone, base, top, 1.0, solid("steel"), extend=0.3)
    m.round_box(bone, top[0], top[2], ball / 2, ball / 2, top[1] - ball / 2, top[1] + ball / 2, solid("steel"),
                cut=max(0.4, ball * 0.25))


def beam(m, bone, cx, cz, y0, y1, r0, r1, key="beam", steps=3):
    """A translucent tractor beam widening from r0 at y1 (top) to r1 at y0 (bottom)."""
    def s(x, y, z, face, variant, **k):
        return P(variant)[key], None
    h = (y1 - y0) / steps
    for i in range(steps):
        r = r0 + (r1 - r0) * (i + 0.5) / steps
        m.round_box(bone, cx, cz, r, r, y1 - (i + 1) * h, y1 - i * h, s, cut=max(0.5, r * 0.35))


def rainbow(x, y, z, face, variant, **k):
    """Rainbow light by angle round the y axis (orbit rings, halos)."""
    p = P(variant)
    a = (math.atan2(x, z) / (2 * math.pi)) % 1.0
    c = mix(p["yellow"], p["red"], a * 2) if a < 0.5 else mix(p["red"], p["green"], (a - 0.5) * 2)
    return c, c


def ring(m, bone, c, r, t, plane="xz", shader=None, n=20):
    """A ring of rods of radius r round c, in the xz or xy plane."""
    pts = []
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        if plane == "xz":
            pts.append((c[0] + r * math.sin(a), c[1], c[2] + r * math.cos(a)))
        else:
            pts.append((c[0] + r * math.sin(a), c[1] + r * math.cos(a), c[2]))
    for a, b in zip(pts, pts[1:]):
        rod(m, bone, a, b, t, shader or rainbow, extend=0.5)
