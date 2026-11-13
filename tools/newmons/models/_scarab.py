"""Shared colours and parts for the dragon beetle line (Larvorub, Ovarupa, Dracarabo), after the fakemon art by
@artworks218_ (Ozera region; names kept, used with the creator's permission): a horned grub with clover-pupilled green
eyes, an orange pupa wrapped round its own head, and a beetle whose great horn has grown into a dragon's skull.

Shiny: the orange turns teal and the brown deep navy, with pink eyes.
"""
from __future__ import annotations

import math

from _boxmodel import mix, rod
from _route import along, pal, tone

BASE = {"brown": (88, 62, 52), "brown_dark": (58, 40, 34), "body": (198, 190, 210), "body_shade": (168, 160, 184),
        "cream": (242, 236, 224), "yellow": (246, 216, 96), "yellow_dark": (206, 170, 56), "yellow_light": (252, 238, 160),
        "ochre": (204, 170, 66), "eye": (132, 216, 78), "eye_dark": (66, 146, 58), "eye_light": (190, 240, 140),
        "orange": (236, 112, 70), "orange_dark": (196, 80, 52), "orange_light": (248, 150, 104),
        "inner": (150, 64, 46), "lavender": (204, 194, 222), "mark": (250, 222, 120)}
SHINY = {"brown": (54, 60, 96), "brown_dark": (36, 40, 68), "eye": (250, 140, 190), "eye_dark": (196, 74, 136),
         "eye_light": (255, 200, 226), "orange": (64, 184, 172), "orange_dark": (40, 142, 136),
         "orange_light": (112, 214, 200), "inner": (30, 96, 100), "ochre": (230, 180, 70)}


def P(v):
    return pal(BASE, SHINY, v)


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def horn_tip(x, y, z, face, variant, box=None, **k):
    """A yellow horn tip with a darker chevron band near its base and a pale point."""
    p = P(variant)
    t = along(z, box)
    if 0.12 < t < 0.3:
        return tone(p["yellow_dark"], face), None
    if t > 0.82:
        return tone(p["yellow_light"], face), None
    return tone(p["yellow"], face), None


def horn(m, bone, root, knee, tip, t_base, t_tip):
    """A two-part horn: brown from root to knee, then a yellow chevroned tip."""
    rod(m, bone, root, knee, t_base, solid("brown"), extend=0.4)
    rod(m, bone, knee, tip, t_tip, horn_tip, extend=0.2)


def clover(dx, dy, s=1.0):
    """A four-leaf clover pupil (Larvorub's eyes)."""
    if math.hypot(dx, dy) < 0.45 * s:
        return True
    return any(math.hypot(dx - ox * s, dy - oy * s) < 0.5 * s for ox, oy in ((0.6, 0), (-0.6, 0), (0, 0.6), (0, -0.6)))


def eye_colour(p, inside_pupil, light):
    if inside_pupil:
        return p["eye_dark"]
    return mix(p["eye"], p["eye_light"], light)


def slab_xy(m, bone, cx, cy, rx, ry, z0, z1, shader, cut=None):
    """A slab along z rounded in its cross-section (two crossed boxes): for bodies that run front to back."""
    cut = max(1, round(min(rx, ry) * 0.3)) if cut is None else cut
    m.box(bone, cx - rx, cy - ry + cut, z0, cx + rx, cy + ry - cut, z1, shader)
    m.box(bone, cx - rx + cut, cy - ry, z0 - 0.05, cx + rx - cut, cy + ry, z1 - 0.05, shader)


def lemniscate(dx, dy, a):
    """Inside a filled infinity sign of half-width a."""
    r2 = dx * dx + dy * dy
    return r2 * r2 <= a * a * (dx * dx - dy * dy * 2.2)
