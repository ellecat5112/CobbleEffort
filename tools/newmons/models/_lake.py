"""Shared parts for the paradox lake trio (#3211-3213: Scaled Acuity, Sparkling Verity, Sunken Valor, after
@Alex_LR04's art): a little floating body with stubby arms and legs, two long tails that end in three teardrop lobes
set with red gems, the red gem on the brow and teal spotted shoulder fins.

Shaders are made from the species' palette function P (keys: skin, skin_dark, red, red_light, line, teal, teal_dark,
teal_light).
"""
from __future__ import annotations

import math

from _boxmodel import rod, spike
from _pgen1 import CLEAR, inside, smooth_path
from _regi import ellipsoid, lit, speck
from _route import mix, tone


def solid(P, key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def skin(P, cy, ry):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        return lit(p["skin"], face, y, cy, ry), None
    return s


def gem(P):
    """A red gem: lighter where it catches the light."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("up", "north"):
            return p["red_light"], p["red_light"]
        return p["red"], p["red"]
    return s


def scallop(u, v, w=1.6, h=1.2):
    """True on the rim of overlapping round scales in rows (u across, v up)."""
    row = math.floor(v / h)
    cu = (u + (row % 2) * w / 2) % w - w / 2
    dv = v - row * h
    return abs(math.hypot(cu, dv * 1.25) - w / 2) < 0.17


def trident(P, ex, ey, ang, L=3.2, W=1.5):
    """Three teardrop lobes fanned from (ex, ey) round the angle `ang` (degrees, in the xy plane), on an xy plane:
    pale with a darker rim and a red gem in each."""
    lobes = []
    for da, f in ((-58, 0.82), (0, 1.15), (58, 0.82)):
        a = math.radians(ang + da)
        lobes.append((math.cos(a), math.sin(a), L * f))

    def s(x, y, z, face, variant, **k):
        p = P(variant)
        dx, dy = x - ex, y - ey
        if math.hypot(dx, dy) < 0.9:
            return tone(p["skin"], face), None
        for ux, uy, Ll in lobes:
            along = dx * ux + dy * uy
            across = -dx * uy + dy * ux
            if not 0 <= along <= Ll:
                continue
            t = along / Ll
            w = W * math.sqrt(t) * (1 - t) / 0.385 * (Ll / L) ** 0.5
            if abs(across) > w:
                continue
            if math.hypot((t - 0.5) * Ll / 0.62, across / max(0.3, w * 0.42)) < 1.0:
                return p["red"], p["red"]
            if abs(across) > w - 0.3:
                return p["line"], None
            return tone(p["skin"], face), None
        return CLEAR
    return s


def tail(m, bone, ctrl, w0, w1, P, n=18, lobe=4.0):
    """A tail through ctrl, tapering w0 -> w1, ending in three gem lobes (a plane facing the front)."""
    pts = smooth_path(ctrl, n)
    sk = skin(P, ctrl[0][1], 6)
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        f = i / (len(pts) - 2)
        rod(m, bone, a, b, max(1.0, round((w0 + (w1 - w0) * f) * 2) / 2), sk, extend=0.6)
    e, q = pts[-1], pts[-3]
    ang = math.degrees(math.atan2(e[1] - q[1], e[0] - q[0]))
    r = lobe * 1.35
    m.box(bone, e[0] - r, max(0.0, e[1] - r), e[2], e[0] + r, e[1] + r, e[2],
          trident(P, e[0], e[1], ang, L=lobe, W=lobe * 0.45))
    return pts


def fin(P, poly, side):
    """A teal shoulder fin cut out of an xy plane (poly in (u, v), u = side * x): dark spots, lighter rim near the
    root."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u = side * x
        if not inside(poly, u, y):
            return CLEAR
        if speck(u, y, 0, "north", cell=1.5, r=0.42, prob=0.5):
            return p["teal_dark"], None
        return tone(p["teal"], face), None
    return s


def fins(m, bone, poly, z, P):
    """Both shoulder fins (poly in (u, v), u outward)."""
    u0, u1 = min(q[0] for q in poly), max(q[0] for q in poly)
    v0, v1 = min(q[1] for q in poly), max(q[1] for q in poly)
    for side in (-1, 1):
        x0, x1 = sorted((side * u0, side * u1))
        m.box(bone, x0, v0, z, x1, v1, z, fin(P, poly, side))


def body(m, bd, cy, P):
    """Torso, stubby three-fingered arms and little legs."""
    sk = skin(P, cy, 3.4)
    ellipsoid(m, bd, 0, cy, 0.2, 2.4, 3.2, 2.2, sk, step=1)
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):
        a0 = (sx * 2.0, cy + 1.8, -0.4)
        a1 = (sx * 3.8, cy + 0.2, -1.6)
        ar = m.bone(nm, bd, a0)
        rod(m, ar, a0, a1, 1.2, sk, extend=0.3)
        for f in (-1, 0, 1):
            spike(m, ar, a1, (sx * 0.5, -0.7, -0.5 + f * 0.6), 0.7, 1.2, sk)
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):
        lg = m.bone(nm, bd, (sx * 1.1, cy - 2.6, 0))
        rod(m, lg, (sx * 1.1, cy - 2.4, 0), (sx * 1.5, cy - 4.6, -0.6), 1.2, sk, extend=0.3)


def brow_gem(m, hd, base, d, P, w=1.4, h=3.0):
    spike(m, hd, base, d, w, h, gem(P), tip=max(0.6, w * 0.5))
