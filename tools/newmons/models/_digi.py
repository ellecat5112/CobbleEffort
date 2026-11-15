"""Shared parts for the Digimon crossover's Agumon line (CobbleEffort: Digital; models built by hand after the
official Digimon art the user shared, no pixels copied): palette, tiger stripes, claws, eyes and teeth.

Shiny: the "Black" colours (charcoal hides with crimson stripes), and for the Omegamon the white and black swap."""
from __future__ import annotations

import math

from _afake import solid_of
from _boxmodel import spike
from _route import pal, tone

BASE = {"pink": (246, 178, 200), "pink_dark": (214, 128, 160), "red": (210, 34, 44), "red_dark": (140, 20, 30),
        "orange": (246, 170, 34), "orange_dark": (214, 126, 24), "belly": (252, 212, 110), "stripe": (40, 104, 196),
        "claw": (240, 240, 244), "claw_dark": (170, 170, 182), "eye": (110, 220, 190), "pupil": (20, 20, 24),
        "white": (250, 250, 250), "mouth": (180, 40, 60), "tongue": (226, 90, 110), "teeth": (246, 244, 236),
        "helmet": (96, 64, 46), "helmet_dark": (66, 42, 30), "horn": (156, 120, 92), "horn_tip": (210, 196, 176),
        "metal": (186, 190, 200), "metal_dark": (110, 114, 126), "metal_light": (228, 232, 238),
        "wing": (112, 72, 176), "wing_dark": (72, 44, 120), "glow": (255, 70, 70), "flame": (255, 150, 40),
        "mech": (204, 30, 36), "mech_dark": (130, 16, 24), "mech_light": (240, 90, 90), "joint": (70, 72, 82),
        "knight": (238, 238, 242), "knight_dark": (168, 170, 182), "gold": (226, 180, 56), "gold_dark": (164, 120, 30),
        "cape": (40, 38, 46), "cape_light": (70, 68, 80), "blade": (246, 220, 120), "lion": (214, 36, 40),
        "cannon": (88, 90, 100), "cannon_dark": (52, 54, 62)}
SHINY = {"pink": (176, 176, 186), "pink_dark": (130, 130, 140), "orange": (64, 62, 70), "orange_dark": (40, 38, 46),
         "belly": (110, 108, 118), "stripe": (196, 40, 60), "eye": (240, 200, 60), "helmet": (40, 38, 44),
         "helmet_dark": (24, 22, 28), "wing": (60, 60, 70), "wing_dark": (30, 30, 36), "mech": (40, 40, 48),
         "mech_dark": (22, 22, 28), "mech_light": (90, 90, 104), "knight": (44, 42, 50), "knight_dark": (24, 24, 30),
         "cape": (236, 236, 242), "cape_light": (200, 200, 210)}


def P(v):
    return pal(BASE, SHINY, v)


solid = solid_of(P)


def striped(key="orange", stripe="stripe", every=5.0, width=1.0, belly=None, seed=0.0, sides_only=True):
    """A hide with wavy tiger stripes across it (on its sides, back and tail, not its belly)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if belly and face in ("north", "down"):
            return tone(p[belly], face), None
        if (not sides_only or face in ("east", "west", "up", "south")):
            t = y + z * 0.35 + 0.6 * math.sin(x * 0.7 + z * 0.5 + seed)
            if (t % every) < width and abs(x) > 0.6:
                return tone(p[stripe], face), None
        return tone(p[key], face), None
    return s


def eye(p, du, dv, r, iris="eye"):
    """A round eye: white rim, coloured iris, black pupil and a glint."""
    d = math.hypot(du, dv)
    if d > r:
        return None
    if d > r * 0.82:
        return p["pupil"]
    if math.hypot(du + r * 0.3, dv - r * 0.3) < r * 0.2:
        return p["white"]
    if d < r * 0.4:
        return p["pupil"]
    return p[iris]


def claw_fan(m, bone, base, d, n, w, h, spread, side=(1, 0, 0), key="claw"):
    """n white claws from `base` along d, spread along `side`."""
    for k in range(n):
        o = (k - (n - 1) / 2) * spread
        b = tuple(base[i] + side[i] * o for i in range(3))
        spike(m, bone, b, d, w, h, solid(key), tip=max(0.4, w * 0.35))


def teeth_row(m, bone, pts, d, w, h):
    for q in pts:
        spike(m, bone, q, d, w, h, solid("teeth"), tip=max(0.3, w * 0.3))
