"""Gigantler, the Crown Antler Pokémon (Normal), built from boxes after the concept art the user shared (the art's own
name; art by @rontoregion).

A huge, long-legged moose with its head held low and a stern glare: brown fur with a darker zigzag stripe along each
flank, a shoulder hump, a long drooping muzzle with dark zigzag markings, small ears, cream legs with knobbly knees and
hocks, split dark hooves, and three massive crown-like palmate antlers: one spreading out to each side with four tines,
and a tall one rising from the middle of its head like a crown with five lobes.

Shiny: a pale "ghost" moose (grey-white fur, white legs) with golden antlers.

Front is -z, y is up. 50 units tall to the top of the crown; baseScale 0.85 (2.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix, rod
from _route import pal, tone

SCALE = 0.85
HITBOX = [1.6, 2.6]
LIFT = 4
KIND = "quadruped"
K = 4
HEIGHT = 50
LOOK = ("a huge long-legged brown moose with a zigzag flank stripe, cream legs, a lowered head with a stern glare and "
        "three massive crown-like palmate antlers")

BASE = {"fur": (138, 90, 54), "dark": (92, 52, 34), "leg": (240, 226, 168), "leg_shade": (188, 176, 110),
        "hoof": (90, 50, 36), "antler": (248, 236, 170), "antler_base": (196, 184, 112), "eye": (250, 246, 236),
        "iris": (176, 64, 44), "nose": (60, 34, 26)}
SHINY = {"fur": (200, 198, 202), "dark": (120, 118, 132), "leg": (250, 248, 240), "leg_shade": (200, 200, 206),
         "hoof": (70, 66, 74), "antler": (252, 214, 96), "antler_base": (204, 150, 52), "iris": (70, 110, 180)}


def P(v):
    return pal(BASE, SHINY, v)


def zig(z):
    """The flank stripe's centre line: a zigzag along the body."""
    t = (z / 3.2) % 2
    return 21 + LIFT + 1.4 * (t if t < 1 else 2 - t)


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and -7 < z < 7 and abs(y - zig(z)) < 0.75:
        return tone(p["dark"], face), None
    if face == "down":
        return tone(mix(p["fur"], p["dark"], 0.4), face), None
    return tone(p["fur"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        dz, dy = z + 17.2, y - 19 - LIFT
        d = math.hypot(dz / 1.0, dy / 0.65)
        if d < 1:
            if dz < -0.1 and d < 0.62:
                return p["iris"], None
            return p["eye"], None
        if -1.4 < dz < 1.2 and 0.6 < dy < 1.05 - 0.25 * dz:
            return p["dark"], None                                     # stern brow
        if math.hypot(dz, dy) < 1.8:
            return tone(p["dark"], face), None                         # dark patch round the eye
    if face == "up" and abs(((z + 30) % 1.6) - 0.8) < 0.35 and abs(x) < 1.8:
        return tone(p["dark"], face), None                             # zigzag bars on the brow
    return bodyf(x, y, z, face, variant)


def muzzlef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot((x - sx * 0.9) / 0.45, (y - 16.6 - LIFT) / 0.7) < 1:
                return p["nose"], None                                 # nostrils
        if abs(y - 14.3 - LIFT) < 0.2:
            return p["nose"], None                                     # mouth line
    if face == "up":
        t = (z + 30) % 1.8
        if abs(t - 0.9) < 0.35 + 0.2 * abs(x) / 2:
            return tone(p["dark"], face), None                         # zigzag markings down the muzzle
    return bodyf(x, y, z, face, variant)


def legf(x, y, z, face, variant, **k):
    p = P(variant)
    c = p["leg_shade"] if face == "south" else mix(p["leg"], p["leg_shade"], max(0.0, min(1.0, (6 - y) / 12)))
    return tone(c, face), None


def hooff(x, y, z, face, variant, **k):
    return tone(P(variant)["hoof"], face), None


def antlerf(y0, y1):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        t = max(0.0, min(1.0, (y - LIFT - y0) / (y1 - y0)))
        c = mix(p["antler_base"], p["antler"], t ** 0.7)
        if face == "up":
            c = mix(c, (255, 255, 255), 0.15)
        return c, None
    return s


def tine(m, bone, base, d, w, h, shader, thick=2.0):
    """A broad, flat antler tine: a wide base rod and a narrower rounded tip, flat front to back."""
    n = math.sqrt(sum(v * v for v in d))
    u = tuple(v / n for v in d)
    mid = tuple(b + v * h * 0.62 for b, v in zip(base, u))
    end = tuple(b + v * h for b, v in zip(base, u))
    rod(m, bone, base, mid, w, shader, extend=0.5, t2=thick)
    rod(m, bone, tuple(b - v * 0.5 for b, v in zip(mid, u)), end, max(1, w * 0.7), shader, extend=0, t2=thick * 0.8)


def build() -> Model:
    m = Model("gigantler")
    top = m.bone("gigantler", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    m.round_box(bd, 0, 1, 4.6, 9.5, 15, 24, bodyf, cut=2)                       # long body
    m.round_box(bd, 0, -4, 4.3, 5.5, 18, 26.2, bodyf, cut=1.8)                   # shoulder hump
    tail = m.bone("tail", bd, (0, 23, 10.4))
    rod(m, tail, (0, 23.5, 10.2), (0, 21, 12.4), 2, bodyf)

    nk = m.bone("neck", bd, (0, 24, -8))
    rod(m, nk, (0, 24, -8), (0, 19.5, -14), 5, bodyf, t2=5.5)                    # thick neck, head held low
    hd = m.bone("head", nk, (0, 20, -14))
    m.round_box(hd, 0, -16.5, 2.6, 3, 16, 22, headf, cut=1)
    m.round_box(hd, 0, -21, 2.2, 2.6, 13.5, 18.5, muzzlef, cut=0.9)              # long drooping muzzle
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.4, sx * 5), 20, -14.5, max(sx * 2.4, sx * 5), 22, -13.5, bodyf,
              rotation=(0, 0, sx * -20), pivot=(sx * 2.4, 21, -14))              # small ears

    # the antlers: one spreading out to each side, a tall crown in the middle (broad fused palms, lobed tines)
    side = antlerf(22, 35)
    crown = antlerf(22, 46)
    th = math.radians(24)
    for sx in (-1, 1):
        rod(m, hd, (sx * 1.4, 21.5, -15.5), (sx * 3, 23.5, -15.5), 2.2, side)    # pedicel
        rod(m, hd, (sx * 2.8, 23.2, -15.6), (sx * 6.5, 24.6, -16), 2.6, side, t2=2)  # beam
        o = (sx * 6, 24.6, -16)
        dv = (sx * math.cos(th), math.sin(th), 0)                                  # the palm rises outward
        pv = (-sx * math.sin(th), math.cos(th), 0)
        at = lambda u, v: tuple(oo + dd * u + pp * v for oo, dd, pp in zip(o, dv, pv))
        rod(m, hd, at(-0.6, 1.2), at(9.8, 1.2), 2, side, extend=0, t2=9)            # broad palm
        for i, u in enumerate((1.4, 3.9, 6.4, 8.8)):                              # four lobed tines
            d = tuple(pp + dd * (0.05 + 0.2 * i) for pp, dd in zip(pv, dv))
            tine(m, hd, at(u, 4.6), d, 3.4, 3.4 + (0.8 if i in (1, 2) else 0), side)
        tine(m, hd, at(9.4, -0.6), tuple(dd - pp * 0.15 for dd, pp in zip(dv, pv)), 3, 3, side)   # outer lobe
    rod(m, hd, (0, 21.5, -14.6), (0, 31, -14.4), 3.2, crown, t2=2.4)            # crown stem
    m.box(hd, -6.5, 30, -15.5, 6.5, 39, -13.5, crown)                            # crown palm
    tine(m, hd, (0, 38.5, -14.5), (0, 1, 0), 4.2, 7.5, crown)                      # tall middle lobe
    for sx in (-1, 1):
        tine(m, hd, (sx * 3.8, 38.5, -14.5), (sx * 0.15, 1, 0), 3.6, 4.5, crown)
        tine(m, hd, (sx * 6.4, 35, -14.5), (sx * 0.8, 1, 0), 3.2, 4, crown)

    for b in m.boxes:                                                             # lift the body for long legs
        b.lo = (b.lo[0], b.lo[1] + LIFT, b.lo[2])
        if b.pivot is not None:
            b.pivot = (b.pivot[0], b.pivot[1] + LIFT, b.pivot[2])
    for bn in m.bones[1:]:
        bn["pivot"][1] += LIFT
    for nm, lx in (("leg_front_left", -2.8), ("leg_front_right", 2.8)):           # long cream legs
        lz = -6
        lg = m.bone(nm, top, (lx, 16 + LIFT, lz))
        rod(m, lg, (lx, 17 + LIFT, lz), (lx, 12, lz - 0.3), 3, bodyf)
        m.round_box(lg, lx, lz - 0.4, 1.5, 1.5, 8, 12.5, legf, cut=0.5)          # knee
        rod(m, lg, (lx, 8.2, lz - 0.4), (lx, 2, lz), 2, legf)
        for dx in (-0.6, 0.6):
            m.box(lg, lx + dx - 0.5, 0, lz - 1.4, lx + dx + 0.5, 2, lz + 0.6, hooff)   # split hooves
    for nm, lx in (("leg_back_left", -2.8), ("leg_back_right", 2.8)):
        lz = 7.5
        lg = m.bone(nm, top, (lx, 16 + LIFT, lz))
        m.round_box(lg, lx, lz, 1.8, 2.4, 13, 17 + LIFT, bodyf, cut=0.7)        # thigh
        rod(m, lg, (lx, 13.5, lz + 0.5), (lx, 8, lz + 2.2), 2.4, legf)
        m.round_box(lg, lx, lz + 2.2, 1.3, 1.3, 7, 9.5, legf, cut=0.5)          # hock
        rod(m, lg, (lx, 8, lz + 2.2), (lx, 2, lz + 1.2), 2, legf)
        for dx in (-0.6, 0.6):
            m.box(lg, lx + dx - 0.5, 0, lz + 0.2, lx + dx + 0.5, 2, lz + 2.2, hooff)
    return m
