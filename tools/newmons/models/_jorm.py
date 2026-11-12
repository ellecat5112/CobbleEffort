"""Shared helpers for Jormbuoy and Jorminous (from the Zorneo x Norden region fakemon series, used with the creators'
permission): a sea serpent built like a Viking longship. Blue hide with a pale stripe, wooden planks, round Viking
shields, tan spikes and oar fins, and (Jorminous) ghostly sea mist.

Shiny: sea-green hide and pale birch planks.
"""
from __future__ import annotations

import math

from _boxmodel import mix
from _route import pal, tone

BASE = {"blue": (64, 120, 196), "blue_dark": (40, 62, 120), "stripe": (176, 210, 240), "belly": (168, 130, 110),
        "wood": (150, 120, 96), "wood_dark": (106, 82, 64), "tan": (196, 170, 120), "shield": (46, 70, 130),
        "shield_in": (180, 210, 240), "rim": (176, 146, 96), "eye": (220, 240, 90), "tongue": (130, 90, 140),
        "mist": (200, 214, 230), "foam": (220, 232, 244)}
SHINY = {"blue": (60, 160, 120), "blue_dark": (30, 100, 80), "stripe": (190, 240, 210), "belly": (210, 196, 160),
         "wood": (214, 196, 160), "wood_dark": (170, 150, 116), "shield": (30, 110, 90), "eye": (255, 160, 60)}


def P(variant):
    return pal(BASE, SHINY, variant)


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def planks(axis="z"):
    """Wooden planks: lighter boards with dark seams running along `axis`, rivets here and there."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        v = y if face in ("east", "west", "north", "south") else (x if axis == "z" else z)
        if abs(v % 1.6 - 0.8) < 0.12:
            return p["wood_dark"], None
        return tone(p["wood"], face), None
    return s


def hide(belly_below=None, stripe_at=None):
    """Blue hide on top, brownish belly underneath, a pale stripe at height `stripe_at`."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "down" or (belly_below is not None and y < belly_below):
            return tone(p["belly"], face), None
        if stripe_at is not None and abs(y - stripe_at) < 0.35 and face not in ("up", "down"):
            return p["stripe"], None
        return tone(p["blue"] if face != "up" else p["blue_dark"], face), None
    return s


def segmented():
    """A serpent body segment (on a rod): dark blue back, pale stripe, brown banded belly."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "down":
            ring = box is not None and int((box.lo[2] + box.size[2] - z) * 0.7) % 2
            return tone(mix(p["belly"], p["wood_dark"], 0.25 if ring else 0), face), None
        if face == "up":
            return tone(p["blue_dark"], face), None
        if box is not None:
            v = (y - box.lo[1]) / max(box.size[1], 1e-6)
            if v < 0.4:
                return tone(p["belly"], face), None
            if v < 0.52:
                return p["stripe"], None
        return tone(p["blue_dark"], face), None
    return s


def shield(cx, cy, cz, r, facing):
    """A round Viking shield on the face `facing` centred at (cx, cy, cz): a rim, dark field and a pale boss."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == facing:
            u = x - cx if facing in ("north", "south") else z - cz
            d = math.hypot(u, y - cy) / r
            if d <= 1:
                if d > 0.82:
                    return p["rim"], None
                if d < 0.4:
                    return p["shield_in"], None
                return p["shield"], None
            return (0, 0, 0, 0), None
        return tone(p["rim"], face), None
    return s


def oar_blade(x, y, z, face, variant, box=None, **k):
    """An oar fin: a dark blue blade fraying into pale, ghostly foam at its tip."""
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6) if box is not None else 0
    if t > 0.7 and math.sin(y * 5 + x * 3 + z) > 0.2:
        return p["foam"], p["foam"]
    return tone(p["blue_dark"], face), None


def mist(x, y, z, face, variant, **k):
    """Translucent ghostly sea mist (the shell layer), glowing faintly."""
    p = P(variant)
    a = 110 + int(40 * math.sin(x * 0.9 + y * 0.7 + z * 0.5))
    return p["mist"] + (a,), p["mist"]
