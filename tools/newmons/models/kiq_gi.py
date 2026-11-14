"""Kiq's Gi form (Fighting/Ice), after @magikdex's Cornera region art: Kiq's quilted body grown a mane of white-teal
frost fur over its shoulders and round its waist, icicles hanging from its hips, a black star-shaped mask with long
points round piercing yellow eyes, a black tunic with a teal front panel and teal hem, black wrist bands, palms pressed
together, and long icy belt tails streaming out behind it.

Shiny: lilac frost, pink ice and bluer skin.

Front is -z, y is up. 39 units tall; baseScale 0.66 (1.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _gi import eye_disc, palette, ring_spikes, translucent
from _kiq import HEAD_Y, build_body
from _route import tone

SHINY = {"skin": (156, 198, 222), "skin_shade": (124, 164, 190), "seam": (100, 136, 166), "frost": (232, 216, 252),
         "frost_shade": (196, 170, 236), "ice": (250, 184, 230, 160), "ice_teal": (170, 120, 210)}
P, solid, ramp = palette(SHINY)
SCALE = 0.66
HITBOX = [1.3, 2.45]
KIND = "biped"
K = 4
HEIGHT = 39
LOOK = ("Kiq with a mane of white-teal frost fur, icicles at its hips, a black star mask round piercing yellow eyes, a "
        "teal-panelled black tunic and long icy belt tails streaming behind")
EYES = ((-1.15, HEAD_Y + 0.05), (1.15, HEAD_Y + 0.05))
POINTS = ((0, 6.6), (180, 6.6), (90, 4.6), (270, 2.4), (45, 2.6), (135, 2.6), (225, 2.0), (315, 2.0))


def star(x, y, z, face, variant, **k):
    """The black star mask: a cut-out plane in front of the face, eye holes showing the yellow eyes behind."""
    p = P(variant)
    for ex, ey in EYES:
        if math.hypot(x - ex, (y - ey) * 1.3) < 0.75:
            return (0, 0, 0, 0), None
    u, v = x, y - HEAD_Y
    r, a = math.hypot(u, v), math.degrees(math.atan2(v, u)) % 360
    reach = 1.5
    for deg, length in POINTS:
        da = abs((a - deg + 180) % 360 - 180)
        reach = max(reach, 1.5 + length * max(0.0, 1 - da / 13.0))
    return ((p["black"], None) if r < reach else ((0, 0, 0, 0), None))


def face(x, y, f, p):
    if f != "north":
        return None
    for ex, ey in EYES:
        e = eye_disc(p, x, y, ex, ey, 0.75, "gold_eye", ry=0.6, glint=False)
        if e is not None:
            return e
    return None


def fur(x, y, z, face, variant, box=None, **k):
    """Frost fur: white at the root to teal at the tips."""
    p = P(variant)
    t = 0.0
    if box is not None:
        t = max(0.0, min(1.0, (box.lo[2] + box.size[2] - z) / max(1e-6, box.size[2])))
    c = tuple(int(round(p["frost"][i] * (1 - t) + p["frost_shade"][i] * t)) for i in range(3))
    return tone(c, face), None


def streamer(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["ice_teal"] if int((x + z) * 0.9) % 3 == 0 else p["frost"], face), None


def build() -> Model:
    m = Model("kiq_gi")
    top = m.bone("kiq_gi", None, (0, 0, 0))
    bd, hd = build_body(m, top, P, solid, gi=True, face=face)
    m.box(hd, -8.2, HEAD_Y - 3.8, -3.75, 8.2, HEAD_Y + 6.2, -3.75, star)
    mane = m.bone("mane", bd, (0, 27, 0))                              # frost fur over the shoulders and back
    ring_spikes(m, mane, 27.4, 4.8, list(range(50, 320, 18)), 5.2, 2.6, fur, out=1.0, rise=0.5)
    ring_spikes(m, mane, 29.6, 3.6, list(range(80, 290, 26)), 4.2, 2.2, fur, out=0.8, rise=0.8)
    ring_spikes(m, bd, 19.4, 4.6, list(range(0, 360, 24)), 3.6, 2.2, fur, out=1.0, rise=-0.5)      # waist fringe
    for sx in (-1, 1):                                                  # icicles from the hips
        for dz, ln in ((-1.6, 5.2), (0.4, 6.6), (2.2, 4.4)):
            rod(m, bd, (sx * 5.4, 15.6, dz), (sx * 6.2, 15.6 - ln, dz + 0.3), 1.4, translucent(P, "ice"), extend=0)
    tails = m.bone("tail", bd, (0, 19.5, 3))                            # long icy belt tails streaming behind
    for sx in (-1, 1):
        pts = [(sx * 1.4, 19.6, 3.2), (sx * 4.0, 17.4, 7.6), (sx * 7.4, 16.6, 11.0), (sx * 10.0, 14.0, 14.6)]
        for a, b in zip(pts, pts[1:]):
            rod(m, tails, a, b, 2.4, streamer, extend=0.6, t2=1.0)
        for a in pts[1:]:
            ring = [(a[0] + sx * 1.2, a[1] - 1.0, a[2] + 0.4)]
            rod(m, tails, a, ring[0], 1.2, fur, extend=0)
    return m
