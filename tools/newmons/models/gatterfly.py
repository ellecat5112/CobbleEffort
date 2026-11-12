"""Gatterfly, the Gatling Pokémon (Fire/Bug), hand-built from boxes from the user's design.

A huge butterfly with skin of black coal, glowing cracks running through it: a round coal head with big ruby compound
eyes and curling feelers tipped with embers, a heavy thorax, the glowing segmented abdomen it had as a grub, and long
insect legs with glowing knees. Its arms end in Gatling guns: a coal housing ringed with a red-hot band and a rotating
drum of barrels that glows hotter towards the muzzle, six white-hot bores in its face (the drums spin when it
fires). Its four wings are made of fire: white-hot at the root, orange, then red, with dark veins and a charred edge,
all glowing.

Front is -z, y is up. 36 units tall to its wingtips; baseScale 0.78 (1.75 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, mix
from _coal import COAL, coal, fire, glowing_segment, ruby

SCALE = 0.78
HITBOX = [1.4, 1.8]
KIND = "biped"
K = 3
HEIGHT = 36
LOOK = ("a huge butterfly of black coal with glowing cracks, ruby compound eyes, Gatling-gun arms whose barrel drums "
        "glow white-hot at the muzzle, and four wings made of fire")

GUN = (9.0, 11.0)                    # the guns' drum axis (|x|, y)
DRUM = (-16.0, -8.0)                 # the drum's z range (muzzle, back)
SEGMENTS = [(6.0, 3.5, 3, 7, 13), (9.5, 2.5, 2, 6, 10.5)]


def skin(x, y, z, face, variant, **k):
    return coal(x, y, z, face, variant, cracks=1.0)


def plain(x, y, z, face, variant, **k):
    return coal(x, y, z, face, variant)


def headf(x, y, z, face, variant, **k):
    if face == "north":
        for sx in (-1, 1):
            e = ruby(x - sx * 2.2, y - 24.2, 1.6, 1.9, variant)
            if e:
                return e
    return coal(x, y, z, face, variant)


def ember(x, y, z, face, variant, **k):
    c = fire(0.8, variant)
    return c, c


def legf(x, y, z, face, variant, **k):
    if 4.6 < y < 5.6:                                        # glowing knee
        c = fire(0.6, variant)
        return c, c
    return coal(x, y, z, face, variant)


def abdomen(x, y, z, face, variant, box=None, **k):
    cz_box = box.lo[2] + box.size[2] / 2
    cz, rx, rz, y0, y1 = min(SEGMENTS, key=lambda s: abs(s[0] - cz_box))
    band = max(0.0, 1 - abs(z - cz) / 0.9) if face not in ("north", "south") else 0.6
    return glowing_segment((y - y0) / (y1 - y0), band, variant)


def housing(x, y, z, face, variant, **k):
    if -6.2 < z < -4.8 and face != "north" and face != "south":          # the red-hot band round the gun
        c = fire(0.42, variant)
        return c, c
    return coal(x, y, z, face, variant)


def drum(x, y, z, face, variant, **k):
    gx, gy = math.copysign(GUN[0], x), GUN[1]
    if face == "north":                                      # the muzzle: six white-hot bores round a centre one
        dx, dy = x - gx, y - gy
        r = math.hypot(dx, dy)
        bores = [(1.55 * math.cos(a), 1.55 * math.sin(a)) for a in (i * math.pi / 3 + math.pi / 6 for i in range(6))]
        if r < 0.5 or any(math.hypot(dx - bx, dy - by) < 0.55 for bx, by in bores):
            c = fire(0.95, variant)
            return c, c
        if any(math.hypot(dx - bx, dy - by) < 0.8 for bx, by in bores):
            c = fire(0.55, variant)
            return c, c
        return mix(COAL, (90, 86, 96), 0.4), None
    if face == "south":
        return COAL, None
    t = (DRUM[1] - z) / (DRUM[1] - DRUM[0])                  # 0 at the back, 1 at the muzzle
    ang = math.atan2(y - gy, x - gx)
    groove = abs(math.sin(ang * 3)) < 0.2                    # lines between the barrels
    base = mix((70, 68, 78), (40, 38, 44), 0.6 if groove else 0.0)
    if t > 0.35:
        heat = (t - 0.35) / 0.65
        c = mix(base, fire(0.3 + 0.6 * heat, variant), min(1.0, 0.25 + heat))
        return c, (fire(0.3 + 0.6 * heat, variant) if heat > 0.15 else None)
    return base, None


def wing_shape(u, v, upper):
    """Inside the wing (0..1 from the root's heat outwards) or None. u: distance from the body, v: height."""
    if upper:
        cu, cv, ru, rv, tilt = 8.5, 26.0, 8.6, 9.6, math.radians(28)
    else:
        cu, cv, ru, rv, tilt = 6.0, 12.0, 6.2, 5.4, math.radians(-20)
    du, dv = u - cu, v - cv
    a = du * math.cos(tilt) + dv * math.sin(tilt)
    b = -du * math.sin(tilt) + dv * math.cos(tilt)
    d = math.sqrt((a / ru) ** 2 + (b / rv) ** 2)
    ang = math.atan2(b, a)
    edge = 1 + (0.13 * max(0.0, math.sin(ang * 5 + 0.8)) if upper and b > 0 else 0.04 * math.sin(ang * 7))
    if d > edge:
        return None
    return d / edge


def make_wing(upper):
    root = (0.0, 19.0) if upper else (0.0, 15.0)

    def wing(x, y, z, face, variant, **k):
        u = abs(x) - 2.5
        s = wing_shape(u, y, upper)
        if s is None:
            return (0, 0, 0, 0), None
        if s > 0.9:                                          # the charred edge
            return mix((30, 26, 30), fire(0.15, variant), 0.4), None
        heat = 1 - math.hypot(u - root[0], y - root[1]) / (19.0 if upper else 13.0)
        ang = math.atan2(y - root[1], u - root[0])
        vein = abs(math.sin(ang * 6)) < 0.07 and s > 0.15
        t = 0.2 + 0.85 * max(0.0, heat) + 0.1 * (1 - s)
        c = fire(t, variant)
        if vein:
            c = mix(c, (60, 20, 14) if variant != "shiny" else (14, 20, 60), 0.6)
            return c, None
        return c, c
    return wing


def build() -> Model:
    m = Model("gatterfly")
    top = m.bone("gatterfly", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0, 5, 4, 10, 20, skin, cut=2)                            # thorax
    tail = m.bone("tail", bd, (0, 12, 3))
    for cz, rx, rz, y0, y1 in SEGMENTS:
        m.round_box(tail, 0, cz, rx, rz, y0, y1, abdomen, cut=1)
    hd = m.bone("head", bd, (0, 20, -1))
    m.round_box(hd, 0, -1, 4, 3.5, 20, 27, headf, cut=1)
    for sx in (-1, 1):                                                          # feelers with ember tips
        chain(m, hd, [(sx * 1.5, 26.5, -2), (sx * 3, 30, -3), (sx * 5, 32.5, -1.5)], [1, 1], plain)
        m.box(hd, sx * 5 - 1, 32, -2.5, sx * 5 + 1, 34, -0.5, ember)
    up, low = make_wing(True), make_wing(False)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        w = m.bone(nm, bd, (sx * 2.5, 19, 4.5))
        xa, xb = sorted((sx * 2.5, sx * 20.5))
        m.box(w, xa, 14, 4.5, xb, 36, 4.5, up)
        xa, xb = sorted((sx * 2.5, sx * 15.5))
        m.box(w, xa, 5, 5, xb, 19, 5, low)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        arm = m.bone(nm, bd, (sx * 6.5, 19, 0))
        gx, gy = sx * GUN[0], GUN[1]
        m.round_box(arm, sx * 6.8, 0, 2.5, 2.5, 16, 21, plain, cut=1)        # shoulder
        m.box(arm, sx * 8 - 1.5, 13, -2, sx * 8 + 1.5, 17, 1, plain)          # upper arm
        m.box(arm, gx - 3, gy - 3, DRUM[1], gx + 3, gy + 3, 0, housing)       # gun housing
        sp = m.bone("spin_" + nm.split("_")[1], arm, (gx, gy, -12))
        m.box(sp, gx - 2, gy - 2.5, DRUM[0], gx + 2, gy + 2.5, DRUM[1], drum)
        m.box(sp, gx - 2.5, gy - 2, DRUM[0] - 0.05, gx + 2.5, gy + 2, DRUM[1] - 0.05, drum)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        leg = m.bone(nm, top, (sx * 3, 10.5, 0))
        m.box(leg, sx * 3 - 1, 4.5, -1, sx * 3 + 1, 10.5, 1, legf)
        m.box(leg, sx * 3 - 1, 0.5, -1.5, sx * 3 + 1, 5.5, 0.5, legf)
        m.box(leg, sx * 3 - 1.5, 0, -3, sx * 3 + 1.5, 1, 1, plain)
    return m
