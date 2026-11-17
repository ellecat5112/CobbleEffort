"""Breakdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the colossal demolition dragon. A low hulking machine-dragon of mud-camouflaged plating over a
dark green chassis on caterpillar treads, two long hydraulic necks ending in drill-snouted heads with toothed jaws,
two huge steel drills mounted on its arms, black exhaust fins, an armoured cab and orange warning lamps.
35 blocks tall.

Front is -z, y is up. 40 units tall, very long; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import lerp
from _digidetail import armour, fbm, local, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = ("a colossal demolition dragon: mud-camouflaged plating on a dark green tracked chassis, two hydraulic necks "
        "with drill-snouted toothed heads, two huge arm drills, black exhaust fins and orange warning lamps")
BASE = {"camo": (150, 140, 90), "camo_dark": (90, 80, 50), "camo_light": (200, 190, 140), "green": (60, 90, 60),
        "green_dark": (24, 40, 26), "steel": (200, 204, 214), "steel_dark": (90, 94, 104), "black": (30, 30, 36),
        "orange": (250, 110, 30), "tooth": (240, 236, 220), "mouth": (80, 20, 20), "eye": (250, 60, 40)}
SHINY = {"camo": (170, 180, 200), "camo_dark": (100, 110, 130), "camo_light": (220, 230, 245), "green": (110, 40, 40),
         "green_dark": (50, 14, 14)}


def P(v):
    return pal(BASE, SHINY, v)


GREEN = armour(P, "green", "green_dark", rivets=True)
STEEL = metal(P, "steel", dark="steel_dark")


def camof(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    n = fbm(x * 0.18, y * 0.18, z * 0.18, 11)
    col = p["camo_dark"] if n < 0.4 else p["camo_light"] if n > 0.62 else p["camo"]
    return tone(col, face), None


def drillf(x, y, z, face, variant, box=None, **k):
    """A drill: steel with a dark spiral groove."""
    p = P(variant)
    t = (y * 0.9 + math.atan2(x, z) * 1.2) % 1.6
    return tone(p["steel_dark"] if t < 0.4 else p["steel"], face), None


def treadf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    rib = (z if face in ("east", "west", "up", "down") else y) % 2.0 < 0.8
    return tone(p["black"] if rib else p["steel_dark"], face), None


def drill(m, bone, base, d, length, r):
    """A tapering drill from `base` along d, as stepped rods."""
    n = math.sqrt(sum(c * c for c in d))
    u = tuple(c / n for c in d)
    steps = 5
    for i in range(steps):
        a = tuple(b + u[j] * length * i / steps for j, b in enumerate(base))
        b2 = tuple(b + u[j] * length * (i + 1) / steps for j, b in enumerate(base))
        rod(m, bone, a, b2, max(1, round(2 * r * (1 - i / steps))), drillf, extend=0.3)
    spike(m, bone, tuple(b + u[j] * length for j, b in enumerate(base)), u, 1.0, 2.0, drillf)


def build():
    m = Model("breakdramon")
    top = m.bone("breakdramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 4.0, 10.0, 14.0, 8.0, 22.0, GREEN, cut=3)                     # the chassis
    m.round_box(bd, 0, 2.0, 9.0, 11.0, 18.0, 28.0, camof, cut=3)                     # camo hull
    m.box(bd, -5.0, 22.0, -10.0, 5.0, 28.0, -4.0, camof)                              # armoured cab
    for sx in (-1, 1):
        m.box(bd, sx * 3.0 - 1.0, 28.0, -8.0, sx * 3.0 + 1.0, 29.4, -6.0, solid(P, "orange", glow=True))
        for j in range(3):                                                           # black exhaust fins
            m.box(bd, sx * 6.0 - 0.4, 26.0, 6.0 + j * 4.0, sx * 6.0 + 0.4, 34.0 - j, 9.0 + j * 4.0,
                  solid(P, "black"), rotation=(-20, 0, sx * 15), pivot=(sx * 6.0, 26.0, 7.0 + j * 4.0))
    # caterpillar treads (as leg bones so the rig shuffles them)
    for sx, fz, nm in ((1, -8.0, "leg_front_left"), (-1, -8.0, "leg_front_right"), (1, 10.0, "leg_back_left"),
                       (-1, 10.0, "leg_back_right")):
        lg = m.bone(nm, top, (sx * 11.0, 6.0, fz))
        x0, x1 = sorted((sx * 8.0, sx * 15.0))
        m.box(lg, x0, 0.0, fz - 8.0, x1, 10.0, fz + 8.0, treadf)
        m.box(lg, min(x0, x1) - 0.4, 3.0, fz - 6.0, max(x0, x1) + 0.4, 7.0, fz + 6.0, GREEN)
    # two hydraulic necks ending in drill-snouted heads
    for k, (sx, top_p) in enumerate(((1, (8.0, 38.0, -22.0)), (-1, (-10.0, 34.0, -24.0)))):
        nk = m.bone(f"neck_{k}", bd, (sx * 4.0, 26.0, -6.0))
        pts = [(sx * 4.0, 26.0, -6.0), lerp((sx * 4.0, 26.0, -6.0), top_p, 0.5), top_p]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, nk, p0, p1, 4, camof, extend=0.6)
            rod(m, nk, p0, p1, 2, STEEL, extend=0.8)
        hd = m.bone("head" if k == 0 else f"head_{k}", nk, top_p)
        hx, hy, hz = top_p
        m.round_box(hd, hx, hz, 3.0, 3.4, hy - 2.0, hy + 3.0, camof, cut=1)
        m.box(hd, hx - 2.4, hy - 1.0, hz - 7.0, hx + 2.4, hy + 1.6, hz - 1.0, camof)           # upper snout
        jw = m.bone(f"jaw_{k}", hd, (hx, hy - 1.0, hz - 1.0))
        m.box(jw, hx - 2.0, hy - 2.6, hz - 6.4, hx + 2.0, hy - 1.2, hz - 1.0, camof, rotation=(22, 0, 0),
              pivot=(hx, hy - 1.0, hz - 1.0))
        m.box(hd, hx - 2.0, hy - 1.4, hz - 6.6, hx + 2.0, hy - 1.0, hz - 1.0, solid(P, "mouth"))
        for i in range(4):
            for ex in (-1.6, 1.6):
                spike(m, hd, (hx + ex, hy - 1.0, hz - 6.0 + i * 1.3), (0, -1, 0), 0.8, 1.2, solid(P, "tooth"))
        for ex in (-2.4, 2.4):
            m.box(hd, hx + ex - 0.3, hy + 1.0, hz - 2.0, hx + ex + 0.3, hy + 1.8, hz - 1.0,
                  solid(P, "eye", glow=True))
        drill(m, hd, (hx, hy + 1.0, hz - 6.0), (0, 0.1, -1), 7.0, 1.6)
    # two huge arm drills
    for k, sx in enumerate((1, -1)):
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 10.0, 20.0, -10.0))
        rod(m, ab, (sx * 10.0, 20.0, -10.0), (sx * 13.0, 14.0, -18.0), 4, GREEN, extend=0.6)
        m.round_box(ab, sx * 13.0, -19.0, 3.0, 3.0, 11.0, 17.0, camof, cut=1)
        drill(m, ab, (sx * 13.0, 14.0, -21.0), (sx * 0.15, 0.25, -1), 14.0, 3.0)
    return m
