"""Shared colours and shaders for the eurypterid fossil line (Scorpaddle, Pterygant): ancient sea scorpions, after the
fakemon art the user shared (a DeviantArt piece; artist not named); names and models are our own.

Yellow shells with magenta markings, brown swimming paddles banded with pink, and a pink telson spike on the tail.
Shiny: an aqua shell with orange markings.
"""
from __future__ import annotations

from _boxmodel import mix
from _route import pal, tone

BASE = {"shell": (244, 224, 98), "shell_shade": (212, 188, 70), "shell_light": (252, 242, 160),
        "mark": (196, 88, 138), "mark_light": (226, 132, 172), "paddle": (138, 112, 96), "paddle_dark": (98, 78, 68),
        "band": (210, 112, 150), "spike": (214, 112, 156), "eye": (26, 22, 30), "eye_glint": (240, 238, 244),
        "belly": (236, 214, 120)}
SHINY = {"shell": (122, 212, 222), "shell_shade": (84, 172, 192), "shell_light": (180, 236, 242), "mark": (238, 136, 56),
         "mark_light": (250, 180, 100), "band": (240, 150, 70), "spike": (240, 150, 70), "belly": (150, 220, 226)}


def P(v):
    return pal(BASE, SHINY, v)


def paddlef(band_at=None):
    """Brown paddle, darker underneath, with a pink band across it where `band_at(x, y, z)` says."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if band_at is not None and band_at(x, y, z):
            return tone(p["band"], face), None
        return tone(p["paddle"] if face != "down" else p["paddle_dark"], face), None
    return s


def spikef(x, y, z, face, variant, **k):
    return tone(P(variant)["spike"], face), None


def darkf(x, y, z, face, variant, **k):
    return tone(P(variant)["paddle_dark"], face), None
