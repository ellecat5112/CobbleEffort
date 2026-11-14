"""Shared parts for Bootlegger and Moonshiner (the user's design): bandit raccoons, grey with a black mask, a ringed
tail and ceramic jugs (cream with brown tops)."""
from __future__ import annotations

from _boxmodel import Model, rod
from _liquor import palette, tiers
from _route import tone

SHINY = {"coon": (196, 140, 90), "coon_dark": (120, 70, 40), "coon_light": (240, 210, 170)}
P, solid, ramp = palette(SHINY)


def maskface(cx, eye_y, s=1.0):
    def f(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                if abs(x - cx - sx * 1.2 * s) < 0.45 * s and abs(y - eye_y) < 0.45 * s:
                    return p["amber_light"], p["amber_light"]                 # eyes shining in the dark
            if abs(y - eye_y) < 0.9 * s and abs(x - cx) < 2.6 * s:
                return p["coon_dark"], None                                   # the bandit mask
            if y < eye_y - 1.0 * s:
                return tone(p["coon_light"], face), None
        return tone(p["coon"], face), None
    return f


def ringtail(m, bone, a, b, t):
    """A banded tail (alternating grey and black rods)."""
    n = 5
    for i in range(n):
        p0 = tuple(a[j] + (b[j] - a[j]) * i / n for j in range(3))
        p1 = tuple(a[j] + (b[j] - a[j]) * (i + 1) / n for j in range(3))
        rod(m, bone, p0, p1, t * (1 - 0.08 * i), solid("coon_dark" if i % 2 else "coon"), extend=0.2)


def jug(m, bone, cx, y0, cz, s):
    tiers(m, bone, [(y0, y0 + 2.4 * s, 1.3 * s), (y0 + 2.4 * s, y0 + 3.0 * s, 0.8 * s), (y0 + 3.0 * s, y0 + 3.6 * s, 0.5 * s)],
          solid("cream"), cx=cx, cz=cz)
    tiers(m, bone, [(y0 + 3.0 * s, y0 + 3.6 * s, 0.55 * s)], solid("clay_dark"), cx=cx, cz=cz)
