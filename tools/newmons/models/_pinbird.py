"""Shared colours, shaders and parts for the pinbird line (Pinlet, Pinnant, Pennacrest), after the bird family art the
user shared (artist not named), inspired by pin-tailed birds such as the pin-tailed whydah: red-brown plumage, a white
face, bib and neck, brown wings with red coverts, big grey eyes, a yellow beak and feet, and long tail streamers banded
black and grey (red-tipped on Pennacrest). They raise their chicks in great hay nests on top of rocky crags.

Shiny: slate blue plumage, grey wings and gold-banded streamers.
"""
from __future__ import annotations

import math

from _boxmodel import mix, rod
from _route import pal, tone

BASE = {"red": (190, 66, 40), "red_dark": (140, 44, 30), "red_light": (222, 106, 70), "brown": (178, 112, 58),
        "brown_light": (214, 160, 92), "white": (250, 246, 240), "white_shade": (222, 214, 206), "grey": (156, 158, 164),
        "grey_dark": (98, 100, 108), "black": (30, 30, 34), "beak": (238, 200, 84), "feet": (234, 206, 122),
        "pupil": (34, 34, 40), "glint": (255, 236, 120), "iris": (156, 158, 164),
        "iris_dark": (98, 100, 108)}
SHINY = {"red": (64, 96, 156), "red_dark": (42, 64, 116), "red_light": (110, 146, 206), "brown": (118, 124, 138),
         "brown_light": (162, 168, 182), "grey": (222, 190, 96), "grey_dark": (176, 142, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def redf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "down":
        return p["red_dark"], None
    return tone(p["red"], face), None


def whitef(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["white"] if face in ("up", "north", "east", "west") else p["white_shade"], face), None


def beakf(x, y, z, face, variant, **k):
    return tone(P(variant)["beak"], face), None


def feetf(x, y, z, face, variant, **k):
    return tone(P(variant)["feet"], face), None


def blackf(x, y, z, face, variant, **k):
    return tone(P(variant)["black"], face), None


def eye(face, x, y, ex, ey, r, variant, star=False):
    """A big grey eye on a north face at (ex, ey): grey iris with a dark rim and pupil and a glint (a star for a chick).
    Returns a colour or None when (x, y) is outside it."""
    p = P(variant)
    if face != "north":
        return None
    d = math.hypot(x - ex, y - ey) / r
    if d >= 1:
        return None
    gx, gy = x - ex + r * 0.3, y - ey - r * 0.3
    if star:
        a = math.atan2(gy, gx)
        if math.hypot(gx, gy) < r * (0.22 + 0.14 * math.cos(5 * a)):
            return p["glint"]
    elif math.hypot(gx, gy) < r * 0.2:
        return (255, 255, 255)
    if d > 0.8:
        return p["iris_dark"]
    if d < 0.32:
        return p["pupil"]
    return p["iris"]


def bodyf(bib_top, bib_x=99, chevrons=()):
    """Red-brown plumage with a white bib on the front below bib_top (narrower than bib_x), and black chevron marks
    at (x, y) places on it."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north" and y < bib_top and abs(x) < bib_x:
            for cx, cy in chevrons:
                dx = x - cx
                if abs(dx) < 1.4 and abs((y - cy) - (-0.55 * abs(dx) if cx == 0 else 0.5 * dx * (1 if cx > 0 else -1))) < 0.32:
                    return p["black"], None
            return tone(p["white"], face), None
        return redf(x, y, z, face, variant)
    return s


def wingf(x0, x1, z0, z1, feathers=5, tip_white=False):
    """A spread wing on a plane in xz (pre-rotation): leading edge at z0, trailing edge at z1, from the body at x0 to the
    tip at x1. Red coverts along the leading edge, brown flight feathers whose trailing edge is cut into points."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u = (x - x0) / (x1 - x0)                                           # 0 at the body, 1 at the tip
        if u < -0.05 or u > 1.05:
            return (0, 0, 0, 0), None
        f = (u * feathers) % 1.0
        back = z1 - (z1 - z0) * (0.08 + 0.32 * abs(f - 0.5) * 2) - (z1 - z0) * 0.25 * u ** 2
        if (z - z0) / (z1 - z0) > (back - z0) / (z1 - z0):
            return (0, 0, 0, 0), None                                      # cut to pointed feathers
        t = (z - z0) / (z1 - z0)
        if t < 0.38 - 0.18 * u:
            return tone(p["red"], face), None                              # coverts
        if tip_white and (back - z) < (z1 - z0) * 0.18:
            return p["white"], None
        return (p["brown_light"] if (back - z) < (z1 - z0) * 0.12 else p["brown"]), None
    return s


def bandf(period=2.4, black_share=0.5):
    """Streamer bands, black and grey (rods: z runs along the rod)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        c = p["black"] if (z % period) < period * black_share else p["grey"]
        return tone(c, face), None
    return s


def streamer(m, bone, pts, t0, t1, tip=None, period=2.4):
    """A long banded tail streamer along the points, tapering from t0 to t1, with a pointed tip (red if tip == 'red',
    else black)."""
    n = len(pts) - 1
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        t = t0 + (t1 - t0) * i / max(1, n - 1)
        rod(m, bone, a, b, max(0.6, t), bandf(period), extend=0.3, t2=max(0.4, t * 0.45))
    a, b = pts[-2], pts[-1]
    d = [bb - aa for aa, bb in zip(a, b)]
    ln = math.sqrt(sum(v * v for v in d)) or 1
    end = tuple(bb + v / ln * 2.2 for bb, v in zip(b, d))
    rod(m, bone, b, end, max(0.5, t1 * 0.7), redf if tip == "red" else blackf, extend=0.1, t2=max(0.3, t1 * 0.3))
