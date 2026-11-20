"""Bristle Horn's Sky Forme (Rock/Flying), built from boxes after sub_arashii's art (@MadZygardeCore). The Land Forme
is bristlehorn.py.

Taking wing, Bristle Horn stands up into a white-bodied bird. Broad brown wings spread from its shoulders, their long
feathers tipped red; a crest of red-tipped brown spikes sweeps back from its head past its grey horn, white feathered
ears flare out beside its orange eyes, and its blue-grey legs hang above a fan of red tail feathers.

Shiny: sandy wings with teal tips.

Front is -z, y is up. 28 units tall (wings up); about 1.4 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR
from _regi import ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 28
SCALE = round(1.4 * 16 / HEIGHT, 3)
HITBOX = [1.0, 22 / 16]
KIND = "floater"
K = 4
LOOK = ("a white-bodied bird Shaymin with broad red-tipped brown wings, a crest of red-tipped spikes, a grey horn, white "
        "feathered ears and a fan of red tail feathers")

BASE = {"white": (248, 246, 250), "white_dark": (206, 204, 220), "brown": (128, 104, 86), "brown_dark": (92, 72, 60),
        "grey": (176, 170, 172), "tip": (226, 70, 60), "horn": (150, 150, 168), "leg": (96, 104, 140),
        "eye": (240, 150, 50), "pupil": (40, 30, 30), "nose": (40, 34, 40), "line": (70, 56, 50)}
SHINY = {"brown": (206, 176, 120), "brown_dark": (160, 130, 84), "tip": (60, 190, 190)}
CY = 13.0


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    return lit(p["white"], face, y, CY, 5), None


def facef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            r = math.hypot(x - sx * 1.3, y - 21.0)
            if r < 0.4:
                return p["pupil"], None
            if r < 0.8:
                return p["eye"], None
        if abs(x) < 0.4 and abs(y - 19.6) < 0.3:
            return p["nose"], None
    return lit(p["white"], face, y, 20, 3), None


def spikef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    d = (box.lo[2] + box.size[2] - z) / max(box.size[2], 0.01)
    return tone(p["tip"] if d > 0.55 else p["brown"], face), None


def wingf(side, cx, cy, n=6, rmax=13.0):
    """A broad wing (an xy plane): a fan of long brown feathers from the shoulder, each tipped red, grey-white
    coverts near the root."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        dx, dy = side * (x - cx), y - cy
        r = math.hypot(dx, dy)
        a = math.degrees(math.atan2(dy, dx))
        if not (-40 <= a <= 70) or r < 1.0:
            return CLEAR
        f = (a + 40) / 110 * n
        i = math.floor(f)
        off = f - i - 0.5
        R = rmax * (0.78 + 0.22 * math.sin(math.pi * (i + 0.5) / n)) * (1 - 0.5 * off * off)
        if r > R:
            return CLEAR
        if abs(off) > 0.46:
            return p["line"], None
        t = r / R
        if t < 0.35:
            return p["white_dark"], None
        if t > 0.84:
            return p["tip"], None
        return p["brown"], None
    return s


def build() -> Model:
    m = Model("bristlehorn_sky")
    top = m.bone("bristlehorn_sky", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    ellipsoid(m, bd, 0, CY, 0.4, 3.6, 4.8, 3.6, bodyf, step=1)                       # white body
    hd = m.bone("head", bd, (0, 17.6, -0.4))
    ellipsoid(m, hd, 0, 20.4, -0.8, 3.0, 2.8, 2.8, facef, step=1)                    # head
    spike(m, hd, (0, 22.4, -2.6), (0.2, 1, -0.3), 1.6, 5.0, solid("horn"), tip=0.8) # grey horn
    for i in range(6):                                                           # crest of red-tipped spikes
        a = math.radians(30 + i * 24)
        spike(m, hd, (math.cos(a) * 1.6, 22.4, 0.4), (math.cos(a) * 0.9, 0.7, 1), 1.6, 4.6 + (i % 2) * 1.4, spikef,
              tip=0.6)
    for sx in (-1, 1):                                                           # white feathered ears
        rod(m, hd, (sx * 2.6, 21.6, -0.4), (sx * 7.6, 25.0, 1.2), 1.0, solid("white"), extend=0.4, t2=2.6)
        spike(m, hd, (sx * 7.6, 25.0, 1.2), (sx * 1, 0.5, 0.3), 1.4, 2.6, solid("white"), tip=0.6)
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):                        # broad red-tipped wings
        wg = m.bone(nm, bd, (sx * 3.0, 16.0, 1.0))
        x0, x1 = sorted((sx * 3.0, sx * 17.0))
        m.box(wg, x0, 6.0, 1.4, x1, 28.0, 1.4, wingf(sx, sx * 3.0, 15.0, rmax=14.0))
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):                          # blue-grey legs
        lg = m.bone(nm, bd, (sx * 1.6, 9.0, 0.4))
        rod(m, lg, (sx * 1.6, 9.0, 0.4), (sx * 1.8, 4.6, -0.4), 1.4, solid("leg"), extend=0.4)
        spike(m, lg, (sx * 1.8, 5.0, -0.4), (sx * 0.4, -0.5, 0.6), 1.4, 2.4, spikef, tip=0.6)
    tl = m.bone("tail", bd, (0, 10.0, 3.0))                                         # fan of red tail feathers
    for i in range(5):
        a = math.radians(-50 + i * 25)
        spike(m, tl, (0, 10.0, 3.0), (math.sin(a) * 0.8, -0.8, 1), 1.6, 5.6, spikef, tip=0.8)
    return m
