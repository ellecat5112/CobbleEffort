"""Iron Ascent (Dragon/Steel), the future paradox Rayquaza, built from boxes after @pokefeast's art (the art's own
name).

A robot Rayquaza coiled into a great ring: a long white body jointed in black and traced with glowing cyan circuit
lines, with panes of translucent cyan glass floating along it like fins. Its head is a smooth white helmet with a
glowing cyan orb of an eye, under two long navy blades that sweep up and back in a V; little white arms hang beneath.

Shiny: black plating with gold circuits and amber glass.

Front is -z, y is up. 44 units tall; about 4.8 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR, inside
from _regi import ellipsoid, lit
from _route import pal, tone
from _serpent import at, ring_path, serpent, tangent

HEIGHT = 44
SCALE = round(4.8 * 16 / HEIGHT, 3)
HITBOX = [2.6, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a white robot Rayquaza coiled into a great ring, traced with glowing cyan circuits, with floating panes of cyan "
        "glass, a white helmet head with a cyan orb eye and two long navy blades")

BASE = {"white": (236, 238, 244), "white_dark": (190, 196, 210), "black": (34, 34, 40), "cyan": (90, 220, 250),
        "cyan_light": (200, 246, 255), "glass": (110, 220, 250, 150), "glass_edge": (60, 180, 230, 210),
        "navy": (36, 40, 120), "navy_light": (70, 80, 170)}
SHINY = {"white": (50, 50, 60), "white_dark": (30, 30, 38), "cyan": (255, 196, 60), "cyan_light": (255, 236, 160),
         "glass": (255, 180, 70, 150), "glass_edge": (230, 140, 40, 210)}
RC = (0, 21.0, 4.0)     # the ring's centre
RR = 13.0


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def bodyf(x, y, z, face, variant, box=None, **k):
    """White plating jointed in black, with a glowing cyan circuit line along each side (rods: z along the rod)."""
    p = P(variant)
    d = box.lo[2] + box.size[2] - z
    if (d % 4.0) < 0.5:
        return tone(p["black"], face), None
    cy = box.lo[1] + box.size[1] / 2
    if face in ("east", "west", "up") and abs((y - cy) if face != "up" else (x - (box.lo[0] + box.size[0] / 2))) < 0.3:
        return p["cyan"], p["cyan"]
    return tone(p["white"] if face != "down" else p["white_dark"], face), None


def panef(x, y, z, face, variant, box=None, **k):
    """A floating diamond pane of translucent cyan glass (an xy plane), with a brighter rim."""
    p = P(variant)
    cx, cy = box.lo[0] + box.size[0] / 2, box.lo[1] + box.size[1] / 2
    u, v = abs(x - cx) / (box.size[0] / 2), abs(y - cy) / (box.size[1] / 2)
    if u + v > 1.0:
        return CLEAR
    if u + v > 0.82:
        return p["glass_edge"], None
    return p["glass"], None


def bladef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and ((z % 1.4) < 0.3):
        return tone(p["navy_light"], face), None
    return tone(p["navy"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    return lit(p["white"], face, y, 21.4, 4), None


def build() -> Model:
    m = Model("ironascent")
    top = m.bone("ironascent", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 21, 0))
    tl = m.bone("tail", bd, (RC[0] - RR, RC[1], RC[2]))
    # from the head down round a great ring and out into a tail
    ring = ring_path(RC, RR, -100, 250, 14)
    ctrl = [(0, 19.0, -6.0), (0, 12.0, -1.0)] + ring[1:] + [(-8.0, 30.0, 7.0), (-2.0, 33.0, 9.0)]
    pts = serpent(m, [(0.0, bd), (0.7, tl)], ctrl, 40, 5.0, 2.2, bodyf)
    for i, f in enumerate((0.12, 0.26, 0.4, 0.54, 0.68, 0.82, 0.94)):              # floating panes of cyan glass
        q = at(pts, f)
        dx, dy = q[0] - RC[0], q[1] - RC[1]
        r = math.hypot(dx, dy) or 1.0
        out = (dx / r, dy / r)
        c = (q[0] + out[0] * 4.6, q[1] + out[1] * 4.6, q[2] + 0.8)
        s = 3.2 - 0.25 * (i % 3)
        m.box(bd if f < 0.7 else tl, c[0] - s, c[1] - s * 1.3, c[2], c[0] + s, c[1] + s * 1.3, c[2], panef)
    end, d = at(pts, 1.0), tangent(pts, 0.98)
    spike(m, tl, end, d, 2.0, 4.0, solid("white"), tip=0.8)
    hd = m.bone("head", bd, (0, 20.0, -6.0))
    ellipsoid(m, hd, 0, 21.4, -9.4, 4.2, 3.8, 5.4, headf, step=1)                  # smooth white helmet
    m.round_box(hd, 0, -15.6, 2.6, 2.4, 19.0, 22.2, solid("white_dark"), cut=0.8)   # snout
    for sx in (-1, 1):
        ellipsoid(m, hd, sx * 3.6, 22.0, -10.6, 1.4, 1.4, 1.4, solid("cyan", True), step=1)   # cyan orb eyes
        rod(m, hd, (sx * 1.4, 24.6, -8.0), (sx * 4.4, 36.0, -2.0), 1.8, bladef, extend=0.4, t2=2.8)   # navy blades
        spike(m, hd, (sx * 4.4, 36.0, -2.0), (sx * 0.24, 1, 0.5), 1.6, 3.0, bladef, tip=0.6)
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                           # little white arms
        ar = m.bone(nm, bd, (sx * 2.4, 15.0, -3.0))
        rod(m, ar, (sx * 2.4, 15.0, -3.0), (sx * 5.0, 11.6, -6.0), 1.6, solid("white"), extend=0.3)
        ellipsoid(m, ar, sx * 5.0, 11.2, -6.2, 1.1, 1.1, 1.1, solid("black"), step=1)
    return m
