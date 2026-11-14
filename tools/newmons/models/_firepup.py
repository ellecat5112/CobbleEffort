"""Shared colours for the second A. Fakemon fire starter line (Flachiko, Blaxer, Cerbego), after the art of the A.
Fakemon fanpage (@a.fakemon; names and types from its art): red-and-white fire dogs with yellow faces and legs: a
grumpy pup with a flame tail, a boxer in a spiked collar and a hellhound wreathed in purple ghost-fire, two ghostly
heads flaring beside its own.

Shiny: charcoal fur with spectral green ghost-fire.
"""
from __future__ import annotations

from _afake import ramp_of, solid_of
from _boxmodel import mix
from _route import along, pal, tone

BASE = {"red": (222, 72, 52), "red_dark": (170, 42, 36), "white": (250, 244, 236), "yellow": (250, 210, 82),
        "orange": (244, 150, 60), "flame_tip": (252, 220, 120), "lilac": (184, 164, 222), "paw": (150, 70, 50),
        "pupil": (30, 24, 24), "nose": (40, 30, 30), "mouth": (90, 30, 30), "claw": (160, 120, 230),
        "ghost": (160, 120, 240, 150), "ghost_glow": (196, 160, 255)}
SHINY = {"red": (70, 70, 84), "red_dark": (44, 44, 56), "orange": (120, 120, 140), "flame_tip": (190, 190, 210),
         "ghost": (120, 230, 150, 150), "ghost_glow": (160, 255, 190), "claw": (120, 230, 150), "lilac": (150, 220, 170)}


def P(v):
    return pal(BASE, SHINY, v)


solid = solid_of(P)
ramp = ramp_of(P)


def flame(x, y, z, face, variant, box=None, **k):
    """A flame spike: red at the root, orange, a glowing yellow tip."""
    p = P(variant)
    t = along(z, box)
    c = mix(p["red"], p["orange"], t * 2) if t < 0.5 else mix(p["orange"], p["flame_tip"], (t - 0.5) * 2)
    return tone(c, face), (c if t > 0.6 else None)


def ghost(x, y, z, face, variant, **k):
    p = P(variant)
    return p["ghost"], None


def wisp(x, y, z, face, variant, **k):
    p = P(variant)
    return p["ghost_glow"], p["ghost_glow"]


def fur(top_key, bottom_key, split):
    """Two-tone fur: top_key above y = split (and on top faces), bottom_key below."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        return tone(p[top_key] if face == "up" or (face != "down" and y > split) else p[bottom_key], face), None
    return s
