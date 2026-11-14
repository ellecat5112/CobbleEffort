"""Shared colours and parts for Hopple and Rabbrute (Sundor Region art, names kept): grey rabbit fur, pale ear
insides, white fluff, red eyes. Rabbrute, the "family" form, is many Hopples fused into one titan: its fur is dotted
with little bunny faces (white tufts with red eyes)."""
from __future__ import annotations

from _afake import ramp_of, solid_of
from _route import pal, tone

BASE = {"fur": (122, 120, 140), "fur_dark": (78, 74, 88), "fur_light": (166, 164, 184), "belly": (196, 194, 214),
        "inner": (214, 212, 222), "fluff": (236, 236, 244), "eye": (214, 64, 64), "eye_light": (255, 160, 150),
        "white": (250, 250, 250), "pupil": (40, 30, 40), "dot": (220, 60, 60)}


def palette(shiny):
    def P(v):
        return pal(BASE, shiny, v)
    return P, solid_of(P), ramp_of(P)


def dotted(P, key, spacing=1.6, phase=0.0):
    """Fur dotted with the little red eyes of the fused bunnies (glowing faintly)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u = (x if face in ("north", "south", "up", "down") else z) + phase
        v = y if face not in ("up", "down") else z
        if abs((u % spacing) - spacing / 2) < 0.28 and abs((v % (spacing * 1.3)) - spacing * 0.65) < 0.28 \
                and (int(u // spacing) + int(v // (spacing * 1.3))) % 3 == 0:
            return p["dot"], p["dot"]
        return tone(p[key], face), None
    return s
