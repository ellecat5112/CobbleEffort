"""Shared palette and pieces for the Meicoomon line (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): golden-orange fur with black tiger stripes, white fluffy cheeks and chest, green eyes, and the long
ribbon-like ears banded orange and black with a zigzag, ending in little claws."""
from __future__ import annotations

import math

from _boxmodel import rod, spike
from _digidetail import fur, local, solid
from _route import pal, tone

BASE = {"orange": (245, 160, 40), "orange_dark": (190, 100, 14), "yellow": (250, 220, 90), "yellow_dark": (200, 160, 40),
        "white": (248, 246, 240), "white_dark": (200, 196, 186), "black": (30, 28, 30), "eye": (60, 190, 80),
        "pupil": (10, 40, 14), "pink": (240, 120, 160), "mouth": (200, 70, 90), "claw": (220, 220, 230),
        "orb": (240, 120, 240), "red": (230, 40, 60), "violet": (130, 90, 220)}
SHINY = {"orange": (120, 170, 240), "orange_dark": (50, 90, 180), "yellow": (190, 220, 255), "yellow_dark": (110, 140, 210),
         "eye": (230, 120, 220)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "orange", "orange_dark", length=1.2, density=2.4)
WHITE = fur(P, "white", "white_dark", length=1.4, density=2.2)
YEL = fur(P, "yellow", "yellow_dark", length=1.0, density=2.6)


def striped(base=FUR, period=3.0, width=0.45):
    """Fur with black tiger stripes running round the body."""
    def f(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face not in ("down", "north") and abs(((y * 0.7 + abs(x) * 0.35 + z * 0.15) % period) - period / 2) < width:
            return tone(p["black"], face), None
        return base(x, y, z, face, variant, box=box, **k)
    return f


def ribbonf(x, y, z, face, variant, box=None, **k):
    """The ribbon ears: orange with black edges and a black zigzag down the middle."""
    p = P(variant)
    if box is not None:
        u, v, W, H = local(x, y, z, face, box)
        a = max(W, H)
        along, across = (u, v / max(H, 1e-6)) if W >= H else (v, u / max(W, 1e-6))
        if across < 0.15 or across > 0.85 or abs(across - 0.5 - 0.25 * (abs((along * 0.6) % 2.0 - 1.0) - 0.5)) < 0.08:
            return tone(p["black"], face), None
    return tone(p["orange"], face), None


def ribbon(m, bone, pts, width, claw=True):
    """A long flat ribbon ear along `pts` (rods 1 thick, `width` wide), ending in two little claws."""
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bone, p0, p1, 1, ribbonf, extend=0.3, t2=width)
    if claw:
        e, d = pts[-1], [b - a for a, b in zip(pts[-2], pts[-1])]
        for s in (-1, 1):
            spike(m, bone, e, (d[0] + s * 0.4, d[1] + s * 0.4, d[2]), 0.8, 2.4, solid(P, "claw"), tip=0.8)


def cat_eye(m, bone, cx, cy, z, sx, w=1.6, h=1.8):
    """A big green eye with a dark pupil (front plate)."""
    x0, x1 = sorted((cx, cx + sx * w))
    m.box(bone, x0, cy, z, x1, cy + h, z + 0.1, solid(P, "eye"))
    px = cx + sx * w * 0.55
    m.box(bone, min(px, px + sx * 0.6), cy + h * 0.25, z - 0.05, max(px, px + sx * 0.6), cy + h * 0.8, z + 0.05,
          solid(P, "pupil"))
