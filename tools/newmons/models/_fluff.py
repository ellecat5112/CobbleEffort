"""Shared parts for the fluff line (Fluffear, Coateary; the user's "Snowy Routes" art, artist not named, names kept):
snow-white fluff with soft blue shadows, pale-blue skin and paws, big purple eyes, a pink nose, blue pom-poms.

Shiny: cream fluff with a rose-pink trim and amber eyes."""
from __future__ import annotations

import math

from _afake import ramp_of, round_eye, solid_of
from _boxmodel import rod
from _route import pal, tone

BASE = {"white": (250, 250, 254), "shade": (232, 238, 250), "shade_dark": (184, 200, 232), "blue": (120, 172, 234),
        "blue_dark": (78, 122, 196), "skin": (176, 208, 244), "skin_dark": (140, 176, 226), "pink": (240, 150, 172),
        "inner": (214, 194, 244), "iris": (128, 84, 196), "pupil": (40, 26, 70), "eye_white": (252, 252, 255)}
SHINY = {"white": (252, 246, 232), "shade": (238, 224, 200), "shade_dark": (220, 200, 170), "blue": (238, 128, 160),
         "blue_dark": (200, 90, 126), "skin": (246, 196, 206), "skin_dark": (228, 160, 178), "iris": (210, 140, 50),
         "inner": (250, 210, 220)}


def palette():
    def P(v):
        return pal(BASE, SHINY, v)
    return P, solid_of(P), ramp_of(P)


P, solid, ramp = palette()


def fluff(key="white"):
    """Soft fluff: tufts as soft scallops of shade, bluer underneath."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "down":
            return tone(p["shade_dark"], face), None
        a = {"up": x + z, "north": x + y * 0.5, "south": -x + y * 0.5, "east": z + y * 0.5, "west": -z + y * 0.5}[face]
        b = {"up": x - z, "north": y, "south": y, "east": y, "west": y}[face]
        if math.sin(a * 1.6) * 0.5 + math.sin(b * 1.9 + a * 0.4) * 0.5 > 0.72:
            return tone(p["shade"], face), None
        return tone(p[key], face), None
    return s


def eye(p, u, v, r):
    """A big purple eye with a glint."""
    return round_eye(u, v, r, p, "iris", pupil="pupil", white="eye_white", iris_frac=0.8, pupil_frac=0.42)


def pompom(m, bone, c, r, key="blue"):
    """A round pom-pom."""
    x, y, z = c
    m.round_box(bone, x, z, r * 0.7, r * 0.7, y - r, y - r * 0.55, solid(key), cut=max(0.4, round(r * 0.3, 1)))
    m.round_box(bone, x, z, r, r, y - r * 0.6, y + r * 0.6, solid(key), cut=max(0.5, round(r * 0.4, 1)))
    m.round_box(bone, x, z, r * 0.7, r * 0.7, y + r * 0.55, y + r, solid(key), cut=max(0.4, round(r * 0.3, 1)))


def boa(m, bone, pts, t, key="white"):
    """A thick fluffy fur boa through pts."""
    for a, b in zip(pts, pts[1:]):
        rod(m, bone, a, b, t, fluff(key), extend=t * 0.5, t2=t)
