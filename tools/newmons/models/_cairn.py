"""Shared parts for the cairn line (Stackid, Stackoulder, Piloulder; the user's art, artist not named, names kept):
Pokémon made of balanced stones. Smooth river stones in grey, warm brown and olive with fine dark cracks, faces of
dark slanted eyes with a white glint, and mossy green where they've stood a long time.

Shiny: sandstone, terracotta and blue-grey slate."""
from __future__ import annotations

import math

from _afake import ramp_of, solid_of
from _route import pal, tone

BASE = {"grey": (150, 148, 144), "grey_dark": (112, 110, 106), "brown": (162, 138, 116), "brown_dark": (124, 102, 86),
        "olive": (132, 140, 98), "olive_dark": (100, 108, 74), "moss": (108, 138, 78), "slate": (128, 124, 120),
        "eye": (44, 42, 46), "white": (246, 246, 244), "crack": (78, 74, 72)}
SHINY = {"grey": (206, 180, 136), "grey_dark": (168, 142, 102), "brown": (182, 112, 82), "brown_dark": (140, 82, 60),
         "olive": (112, 140, 156), "olive_dark": (82, 106, 120), "moss": (96, 156, 150), "slate": (150, 160, 170),
         "crack": (110, 84, 60)}


def palette():
    def P(v):
        return pal(BASE, SHINY, v)
    return P, solid_of(P), ramp_of(P)


P, solid, ramp = palette()


def coords(x, y, z, face):
    return {"up": (x, z), "down": (x, z), "north": (x, y), "south": (-x, y), "east": (z, y), "west": (-z, y)}[face]


def stone(key, cracks=1.0, extra=None, seed=0.0):
    """A smooth stone, a little darker underneath, with a few fine wandering cracks. `extra(x, y, z, face, p)` paints
    first (a face) and returns a colour or None."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if extra:
            c = extra(x, y, z, face, p)
            if c is not None:
                return c
        a, b = coords(x, y, z, face)
        if cracks and abs(math.sin(a * 0.42 + b * 0.2 + seed) + math.sin(b * 0.7 - a * 0.3 + seed * 1.7)) < 0.07 * cracks:
            return tone(p["crack"], face), None
        dark = key + "_dark" if key + "_dark" in p else key
        return tone(p[dark] if face == "down" else p[key], face), None
    return s


def pebble(m, bone, c, rx, rz, h, shader, cut=None):
    """A smooth flattened stone from y = c[1] up h units: narrower top and bottom layers round its edge."""
    x, y, z = c
    lo, hi = h * 0.25, h * 0.75
    k = cut if cut is not None else max(0.5, round(min(rx, rz) * 0.35, 1))
    m.round_box(bone, x, z, rx * 0.78, rz * 0.78, y, y + lo + 0.05, shader, cut=max(0.4, k * 0.8))
    m.round_box(bone, x, z, rx, rz, y + lo, y + hi, shader, cut=k)
    m.round_box(bone, x, z, rx * 0.78, rz * 0.78, y + hi - 0.05, y + h, shader, cut=max(0.4, k * 0.8))


def slit(p, u, v, w, h):
    """A dark vertical slit eye with a white glint (Stackid's bottom stone, Stackoulder's olive one)."""
    if abs(u) < w and abs(v) < h:
        if abs(u + w * 0.25) < w * 0.3 and v > h * 0.2:
            return p["white"]
        return p["eye"]
    return None


def stern(p, u, v, w, h, side):
    """A dark slanted eye (lower at the inner corner: stern) with a white glint low and inside: the big boulders' eyes."""
    top = h - 0.45 * (w - side * u)                                    # slopes down toward the nose
    if abs(u) < w and -h < v < top:
        if abs(u + side * w * 0.25) < w * 0.35 and -h * 0.55 < v < h * 0.25:
            return p["white"]
        return p["eye"]
    return None


def angry(p, u, v, w, h, side):
    """A white eye under a dark V brow, a dark pupil (Stackid's grumpy middle stone)."""
    brow = h * 0.6 - 0.5 * side * u
    if abs(u) < w * 1.15 and abs(v - brow) < 0.38:
        return p["eye"]
    if abs(u) < w and -h < v < brow - 0.38:
        return p["eye"] if abs(u - side * w * 0.2) < w * 0.45 and v < brow - 0.9 else p["white"]
    return None
