"""Shared parts for the goat-rabbit line (Kidlope, Shadelope, Ghillope; the user's art, artist not named; our names):
black fur with soft grey highlights, long rabbit ears with mauve insides, ridged grey goat horns, grey muzzles, hands and
split hooves, yellow eyes, and leaves: a leafy ruff, vines and a sprouting tail; the last stage wears a ghillie cloak
of leaves bound with vines.

Shiny: chocolate fur and autumn leaves.
"""
from __future__ import annotations

import math

from _afake import ramp_of, solid_of
from _boxmodel import rod, spike
from _route import pal, tone

BASE = {"fur": (42, 40, 46), "fur_light": (74, 72, 80), "grey": (126, 116, 120), "grey_dark": (88, 80, 84),
        "ear": (150, 118, 148), "horn": (112, 104, 106), "horn_dark": (76, 70, 72), "eye": (242, 192, 56),
        "pupil": (30, 26, 28), "white": (250, 250, 246), "leaf": (64, 150, 62), "leaf_light": (112, 192, 84),
        "leaf_dark": (34, 92, 42), "vine": (96, 186, 72)}
SHINY = {"fur": (96, 60, 42), "fur_light": (130, 88, 62), "leaf": (214, 118, 40), "leaf_light": (240, 172, 64),
         "leaf_dark": (150, 66, 30), "vine": (234, 146, 52), "ear": (210, 150, 130)}


def palette():
    def P(v):
        return pal(BASE, SHINY, v)
    return P, solid_of(P), ramp_of(P)


P, solid, ramp = palette()


def furry(key="fur", bands=(), band_key="vine", w=0.45, cross=None):
    """Fur with vine bands round it at heights `bands`, and optional crossing vines on the front: cross = (cy, k) draws
    two diagonals |x| = |y - cy| * k."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        for by in bands:
            if abs(y - by) < w and face not in ("up", "down"):
                return tone(p[band_key], face), None
        if cross and face == "north":
            cy, kk = cross
            if abs(abs(x) - abs(y - cy) * kk) < w:
                return tone(p[band_key], face), None
        return tone(p[key], face), None
    return s


def hoofed(key="grey", split_axis="x", split_at=0.0):
    """A grey hoof or hand with a dark split down the front."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north" and abs((x if split_axis == "x" else z) - split_at) < 0.22:
            return tone(p["grey_dark"], face), None
        return tone(p[key], face), None
    return s


def horn(m, bone, base, out, length, t):
    """A ridged goat horn curling back from `base`, out to the side by `out` (+1/-1)."""
    pts = [base]
    for i in range(1, 4):
        a = i / 3
        pts.append((base[0] + out * length * 0.35 * a, base[1] + length * 0.55 * math.sin(a * 1.4),
                    base[2] + length * 0.75 * a))

    def ridged(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        tz = (z - (box.lo[2] if box else 0))
        return tone(p["horn_dark"] if int(tz * 1.6) % 2 == 0 else p["horn"], face), None
    for (a, b), tt in zip(zip(pts, pts[1:]), (t, t * 0.8, t * 0.6)):
        rod(m, bone, a, b, max(0.8, tt), ridged, extend=0.4)


INNER = "up"                                       # the box face that looks forward once a rod points up


def ear(m, bone, base, d, length, w, t=1.0):
    """A long rabbit ear: black outside, mauve inside on the front face."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == INNER:
            return tone(p["ear"], face), None
        return tone(p["fur"], face), None
    rod(m, bone, base, tuple(b + v * length for b, v in zip(base, d)), w, s, extend=0.2, t2=t)


def ruff(m, bone, cy, r, n, size, shader=None, droop=0.4, phase=0.0):
    """A leafy ruff: n leaf lumps (pointing out and down) round a ring of radius r at height cy."""
    for i in range(n):
        a = 2 * math.pi * (i + phase) / n
        dx, dz = math.sin(a), -math.cos(a)
        spike(m, bone, (dx * r * 0.7, cy, dz * r * 0.7), (dx, -droop, dz), size, size * 1.3,
              shader or solid("leaf" if i % 2 else "leaf_light"), tip=size * 0.55)


def sprig(m, bone, base, d, length, leaves=3):
    """A green vine ending in a little fan of leaves (tails)."""
    end = tuple(b + v * length for b, v in zip(base, d))
    rod(m, bone, base, end, 0.9, solid("vine"), extend=0.2)
    for i in range(leaves):
        a = (i - (leaves - 1) / 2) * 0.8
        spike(m, bone, end, (d[0] + math.sin(a), d[1] + math.cos(a) * 0.6, d[2]), 1.4, 2.4, solid("leaf_light"), tip=0.6)


def eye(p, u, v, r, lid=0.0, slant=0.0):
    """A big yellow eye with a glossy black pupil; `lid` hides its top part (half-lidded), `slant` tilts the lid."""
    if v > r * (1 - 2 * lid) + slant * u:
        return None
    d = math.hypot(u, v)
    if d >= r:
        return None
    if math.hypot(u + r * 0.25, v - r * 0.35) < r * 0.2:
        return p["white"]
    if d < r * 0.5:
        return p["pupil"]
    return p["eye"]
