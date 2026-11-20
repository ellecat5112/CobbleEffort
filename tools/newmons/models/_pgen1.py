"""Shared helpers for the Gen 1 paradox legends (#3185-3194): curved wing bands (a wing as a band hanging off its
arm curve, cut out of an xy plane), polygon cut-outs, starry specks, ribbon tails, segmented robot arms and DNA
double helices.

Planes are xy boxes (seen from the front and back). Their shaders get model coordinates; wing shaders mirror x by
the wing's side so one description serves both wings (u = distance out from the centre line, v = height).
"""
from __future__ import annotations

import colorsys
import math

from _boxmodel import rod, spike
from _regi import speck
from _route import mix, tone

CLEAR = ((0, 0, 0, 0), None)


# ---- curves ---------------------------------------------------------------------------------------------------------

def bezier(pts, n=72):
    """Points along a Bezier curve of any degree through control points pts (2D or 3D)."""
    out = []
    for i in range(n + 1):
        t = i / n
        q = [list(p) for p in pts]
        while len(q) > 1:
            q = [[a + (b - a) * t for a, b in zip(q[j], q[j + 1])] for j in range(len(q) - 1)]
        out.append(tuple(q[0]))
    return out


class Curve2:
    """A 2D curve sampled densely, with right-hand normals (the side the band hangs on) and arc-length t in 0..1."""

    def __init__(self, pts, n=96, flip=False):
        self.p = bezier(pts, n) if len(pts) <= 5 else list(pts)
        L = [0.0]
        for a, b in zip(self.p, self.p[1:]):
            L.append(L[-1] + math.dist(a, b))
        self.len = L[-1]
        self.t = [v / self.len for v in L]
        self.n = []
        for i in range(len(self.p)):
            a, b = self.p[max(0, i - 1)], self.p[min(len(self.p) - 1, i + 1)]
            tx, ty = b[0] - a[0], b[1] - a[1]
            d = math.hypot(tx, ty) or 1.0
            nx, ny = ty / d, -tx / d
            self.n.append((-nx, -ny) if flip else (nx, ny))

    def locate(self, u, v):
        """(t, s, off): t along the curve, s = signed distance along its normal, off = distance past either end."""
        best, bi = 1e9, 0
        for i, (px, py) in enumerate(self.p):
            d = (u - px) ** 2 + (v - py) ** 2
            if d < best:
                best, bi = d, i
        px, py = self.p[bi]
        nx, ny = self.n[bi]
        s = (u - px) * nx + (v - py) * ny
        lat = math.sqrt(max(0.0, best - s * s))
        return self.t[bi], s, lat

    def at(self, t):
        i = min(len(self.p) - 1, max(0, int(round(t * (len(self.p) - 1)))))
        return self.p[i]


def tri(t):
    """A triangle wave: 0 at whole numbers, 1 at halves."""
    return 1 - abs(2 * (t % 1.0) - 1)


def inside(poly, u, v):
    """Point-in-polygon (even-odd)."""
    c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > v) != (y2 > v) and u < (x2 - x1) * (v - y1) / ((y2 - y1) or 1e-9) + x1:
            c = not c
    return c


def scaled(poly, centre, f):
    cx, cy = centre
    return [(cx + (x - cx) * f, cy + (y - cy) * f) for x, y in poly]


# ---- shading --------------------------------------------------------------------------------------------------------

def stars(x, y, z, face, cell=1.7, r=0.3, prob=0.34, salt=0):
    return speck(x, y, z, face, cell=cell, r=r, prob=prob, salt=salt)


def rainbow(t, s=0.78, v=1.0):
    r, g, b = colorsys.hsv_to_rgb(t % 1.0, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))


def flat(P, key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def starry(P, key, star="star", glow=False, light=None):
    """A colour flecked with glowing white stars."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if stars(x, y, z, face):
            return p[star], p[star]
        c = p[light] if (light and face == "up") else p[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def banded(P, a, b, period=2.0, share=0.5, axis="z", glow_b=False):
    """Bands of two colours along a rod (rods: z runs along the rod) or along y."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        w = z if axis == "z" else y
        if (w % period) < period * share:
            return tone(p[a], face), None
        c = p[b]
        return (c, c) if glow_b else (tone(c, face), None)
    return s


# ---- parts ----------------------------------------------------------------------------------------------------------

def plane_xy(m, bone, x0, x1, y0, y1, z, shader, rotation=None, pivot=None):
    x0, x1 = sorted((x0, x1))
    m.box(bone, x0, y0, z, x1, y1, z, shader, rotation=rotation, pivot=pivot)


def band_wing(m, bone, side, curve_pts, width, z, shader_for, extent, rotation=None, pivot=None):
    """A wing band cut out of an xy plane. curve_pts: the arm curve in (u, v) (u outward); width(t) the band's width
    along it; shader_for(curve, width) -> shader(x, y, z, face, variant, u=..., **k) gets u = side * x; extent =
    (u0, u1, v0, v1) of the plane."""
    c = Curve2(curve_pts)
    sh = shader_for(c, width)

    def s(x, y, zz, face, variant, **k):
        return sh(x, y, zz, face, variant, u=side * x, **k)
    u0, u1, v0, v1 = extent
    plane_xy(m, bone, side * u0, side * u1, v0, v1, z, s, rotation=rotation, pivot=pivot)
    return c


def ribbon(m, bone, pts, widths, shader, extend=0.6):
    """Square rods along a path, thickness per point (tails, tubes)."""
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        w = (widths[i] + widths[i + 1]) / 2
        rod(m, bone, a, b, max(1.0, round(w * 2) / 2), shader, extend=extend)


def smooth_path(ctrl, n):
    """n+1 points along a Catmull-Rom spline through ctrl (3D)."""
    pts = [ctrl[0]] + list(ctrl) + [ctrl[-1]]
    out = []
    segs = len(ctrl) - 1
    for i in range(n + 1):
        f = i / n * segs
        j = min(segs - 1, int(f))
        t = f - j
        p0, p1, p2, p3 = pts[j], pts[j + 1], pts[j + 2], pts[j + 3]
        out.append(tuple(0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t * t
                                + (-a + 3 * b - 3 * c + d) * t ** 3) for a, b, c, d in zip(p0, p1, p2, p3)))
    return out


def helix(m, bone, base, d, length, r, turns, strand, rung, segs=None, rungs=None, w=0.9, phase=0.0):
    """A DNA double helix from `base` along direction d: two strands of short rods spiralling round the axis, joined
    by rungs. strand/rung are shaders; they get t (0..1 along the helix) through the rod's position, so colour them
    by distance from `base` (use helix_t)."""
    L = math.sqrt(sum(v * v for v in d))
    a = tuple(v / L for v in d)
    ref = (0, 0, 1) if abs(a[2]) < 0.9 else (1, 0, 0)
    b1 = (a[1] * ref[2] - a[2] * ref[1], a[2] * ref[0] - a[0] * ref[2], a[0] * ref[1] - a[1] * ref[0])
    n1 = math.sqrt(sum(v * v for v in b1))
    b1 = tuple(v / n1 for v in b1)
    b2 = (a[1] * b1[2] - a[2] * b1[1], a[2] * b1[0] - a[0] * b1[2], a[0] * b1[1] - a[1] * b1[0])
    segs = segs or max(8, int(turns * 10))
    rungs = rungs or max(4, int(turns * 5))

    def pt(t, k):
        ang = 2 * math.pi * turns * t + phase + k * math.pi
        return tuple(bb + aa * length * t + r * (math.cos(ang) * u1 + math.sin(ang) * u2)
                     for bb, aa, u1, u2 in zip(base, a, b1, b2))
    for k in (0, 1):
        for i in range(segs):
            rod(m, bone, pt(i / segs, k), pt((i + 1) / segs, k), w, strand, extend=0.5)
    for i in range(rungs):
        t = (i + 0.5) / rungs
        rod(m, bone, pt(t, 0), pt(t, 1), max(0.6, w * 0.7), rung, extend=0.0)


def claws(m, bone, ankle, dirs, w, h, shader, tip=None):
    for d in dirs:
        spike(m, bone, ankle, d, w, h, shader, tip=tip)


def hue_of(rgb, dh):
    r, g, b = (v / 255 for v in rgb[:3])
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    r, g, b = colorsys.hsv_to_rgb((h + dh) % 1.0, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))


__all__ = ["CLEAR", "bezier", "Curve2", "tri", "inside", "scaled", "stars", "rainbow", "flat", "starry", "banded",
           "plane_xy", "band_wing", "ribbon", "smooth_path", "helix", "claws", "hue_of", "mix", "tone"]
