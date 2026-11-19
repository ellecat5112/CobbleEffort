"""Shared helpers for the paradox Regis (#3179-3184): Braille-style glowing dot faces, glowing parts flecked with
white specks (the art's look for their energy), ellipsoids from stacked rounded slices, and threaded drill cones."""
from __future__ import annotations

import math

from _boxmodel import rod

# each Regi's dots, as offsets in model units from the pattern's centre (x right as you look at it is -x in the model,
# so these are drawn mirrored where it matters; the patterns are symmetric)
CROSS = [(0, 2.6), (0, -2.6), (-2.6, 0), (2.6, 0), (-5.0, 0), (5.0, 0), (0, 0)]               # Regice
HEX = [(0, 0)] + [(3.4 * math.cos(math.radians(a)), 3.4 * math.sin(math.radians(a))) for a in range(0, 360, 60)]
H = [(-1.5, 1.8), (1.5, 1.8), (-1.5, 0), (0, 0), (1.5, 0), (-1.5, -1.8), (1.5, -1.8)]        # Regirock


def dot_at(dx, dy, pattern, r, scale=1.0):
    """True if (dx, dy) lies on one of the pattern's dots."""
    return any((dx - px * scale) ** 2 + (dy - py * scale) ** 2 < r * r for px, py in pattern)


def _hash(a, b, c=0):
    h = (a * 73856093) ^ (b * 19349663) ^ (c * 83492791)
    h = (h ^ (h >> 13)) * 1274126177
    return ((h ^ (h >> 16)) & 0xFFFF) / 65535.0


def face_uv(x, y, z, face):
    if face in ("north", "south"):
        return x, y
    if face in ("east", "west"):
        return z, y
    return x, z


def speck(x, y, z, face, cell=1.8, r=0.34, prob=0.42, salt=0):
    """A sparse white fleck pattern for glowing parts: one fleck in some cells of a grid over the face."""
    u, v = face_uv(x, y, z, face)
    iu, iv = math.floor(u / cell), math.floor(v / cell)
    fs = {"north": 1, "south": 2, "east": 3, "west": 4, "up": 5, "down": 6}[face] + salt * 7
    if _hash(iu, iv, fs) > prob:
        return False
    cu = (iu + 0.25 + 0.5 * _hash(iu, iv, fs + 101)) * cell
    cv = (iv + 0.25 + 0.5 * _hash(iu, iv, fs + 202)) * cell
    rr = r * (0.7 + 0.6 * _hash(iu, iv, fs + 303))
    return (u - cu) ** 2 + (v - cv) ** 2 < rr * rr


def glowing(P, key, fleck="fleck", light=None):
    """A glowing energy shader in palette colour `key`, flecked with white; `light` tints the top faces."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if speck(x, y, z, face):
            c = p[fleck]
        elif light and face == "up":
            c = p[light]
        else:
            c = p[key]
        return c, c
    return s


def half(v):
    return round(v * 2) / 2


def ellipsoid(m, bone, cx, cy, cz, rx, ry, rz, shader, step=2, cut=0.36, squash=1.0):
    """An ellipsoid from rounded slices of whole-unit height `step`, symmetric about x = cx (radii to half units)."""
    n = max(2, round(2 * ry / step))
    y0 = cy - n * step / 2
    for i in range(n):
        ya = y0 + i * step
        t = (ya + step / 2 - cy) / ry
        f = math.sqrt(max(0.0, 1 - t * t)) ** squash
        ax, az = max(0.5, half(rx * f * 1.04)), max(0.5, half(rz * f * 1.04))
        c = max(0.5, round(min(ax, az) * cut * 2) / 2)
        if min(ax, az) <= 1.0:
            m.box(bone, cx - ax, ya, cz - az, cx + ax, ya + step, cz + az, shader)
        else:
            m.round_box(bone, cx, cz, ax, az, ya, ya + step, shader, cut=min(c, min(ax, az) - 0.5))


def threads(m, bone, base, d, r0, r1, n, pitch, shader, tip=0.0, tip_w=1.4, groove=None):
    """A threaded drill: n rings along d from radius r0 to r1 (each ring a short rod), then a point of length tip.
    With `groove`, a narrower dark core runs under the rings so the gaps between them read as grooves."""
    L = math.sqrt(sum(v * v for v in d))
    u = tuple(v / L for v in d)
    at = lambda s_: tuple(b + uu * s_ for b, uu in zip(base, u))
    for i in range(n):
        r = r0 + (r1 - r0) * i / max(1, n - 1)
        w = max(1.0, round(2 * r))
        a, b_ = at(pitch * i), at(pitch * i + pitch * 0.62)
        rod(m, bone, a, b_, w, shader, extend=0.0)
        rod(m, bone, a, b_, max(1.0, w - 2), shader, extend=0.0, t2=w + 1)          # crossed: a rounder ring
        if groove:
            rod(m, bone, at(pitch * i), at(pitch * (i + 1)), max(1.0, w - 2), groove, extend=0.2)
    if tip:
        e = at(pitch * n)
        rod(m, bone, e, tuple(b + uu * tip * 0.6 for b, uu in zip(e, u)), max(1.0, round(r1)), shader, extend=0.2)
        e2 = tuple(b + uu * tip * 0.55 for b, uu in zip(e, u))
        rod(m, bone, e2, tuple(b + uu * tip * 0.45 for b, uu in zip(e2, u)), tip_w, shader, extend=0.1)


def lit(c, face, y, cy, ry):
    """Even light for a stack of slices: cancel the painter's lit tops / dark undersides (which stripe a sliced ball)
    and shade by height instead (lighter above the middle, darker below)."""
    if face == "up":
        f = 0.9
    elif face == "down":
        f = 1.12
    else:
        f = 0.94 + 0.08 * max(-1.0, min(1.0, (y - cy) / ry))
    return tuple(max(0, min(255, int(round(v * f)))) for v in c[:3])
