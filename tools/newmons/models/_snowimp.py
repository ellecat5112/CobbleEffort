"""Shared parts for the snow imp line (Fridgimp, Freelzebub; the user's "Snowy Routes" art, artist not named, names
kept): periwinkle-blue imps with frosty pale-blue highlights and icy spikes, curled horns; Fridgimp has a big red
frostbitten nose and red eyes, Freelzebub grows into a lanky devil with great horns, yellow eyes and a spade tail.

Shiny: pale lilac with mint ice and gold eyes."""
from __future__ import annotations

import math

from _afake import ramp_of, solid_of
from _boxmodel import rod, spike
from _route import pal, tone

BASE = {"blue": (124, 140, 214), "blue_dark": (80, 92, 170), "blue_deep": (52, 58, 120), "ice": (214, 232, 252),
        "ice_mid": (168, 196, 240), "red": (222, 58, 58), "red_light": (255, 120, 110), "eye": (232, 52, 40),
        "yellow": (250, 214, 60), "pupil": (24, 22, 36), "white": (250, 250, 252), "mouth": (40, 30, 60)}
SHINY = {"blue": (196, 168, 226), "blue_dark": (146, 116, 186), "blue_deep": (98, 76, 140), "ice": (214, 250, 236),
         "ice_mid": (160, 228, 206), "eye": (250, 196, 50), "yellow": (250, 196, 50)}


def palette():
    def P(v):
        return pal(BASE, SHINY, v)
    return P, solid_of(P), ramp_of(P)


P, solid, ramp = palette()


def frosty(key="blue", y_light=None):
    """Blue skin, darker underneath, a pale frosty sheen on top faces (above y_light, if given)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "up" and (y_light is None or y > y_light):
            return tone(p["ice_mid"], face), None
        if face == "down":
            return tone(p["blue_deep"], face), None
        return tone(p[key], face), None
    return s


def icicle(m, bone, base, d, w, h):
    """An icy spike: blue at its root, frosty pale toward the tip."""
    spike(m, bone, base, d, w, h, ramp("blue", "ice"), tip=max(0.6, w * 0.5))


def horn(m, bone, pts, ts):
    """A curved horn through pts, darker at the root, pale at the tip."""
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        t = ts[min(i, len(ts) - 1)]
        rod(m, bone, a, b, t, solid("blue_deep" if i == 0 else "blue_dark" if i < len(pts) - 2 else "ice_mid"), extend=0.4)


def slant_eye(p, u, v, r, key="eye", side=1, angry=0.5):
    """A slanted almond eye (higher at the outer corner) with a dark slit pupil."""
    if v > r * 0.55 - angry * side * u * 0.6 or v < -r * 0.6 or abs(u) > r:
        return None
    if abs(u - side * r * 0.1) < r * 0.22:
        return p["pupil"]
    return p[key]
