"""Shared colours and parts for the Liquor Meadows Pokémon (the user's 18 designs inspired by brewing, distillation and
the culture of alcohol and spirits, in CobbleEffort: Kanto's Liquor Meadows): glass and drinks, oak and iron hoops,
copper and brass, hops, grapes and agave, foam, porcelain and smoke. Each model keeps its own SHINY dict and calls
`palette(shiny)`; the shape helpers are the Nicodex's (`_nico`).
"""
from __future__ import annotations

import math

from _afake import ramp_of, solid_of
from _nico import disc_z, eye_on, puff, ring_pts, translucent, tube_z  # noqa: F401  (re-exported for the models)
from _route import pal, tone

BASE = {
    "glass": (214, 236, 242, 100), "glass_rim": (236, 248, 252, 170), "amber": (214, 136, 40), "amber_light": (240, 182, 80),
    "amber_glass": (214, 136, 40, 170), "wine": (122, 22, 40), "wine_dark": (78, 10, 26), "wine_glass": (150, 30, 54, 190),
    "rose": (246, 150, 170, 140), "rose_solid": (240, 140, 160),
    "gold": (236, 196, 76), "gold_dark": (186, 142, 46), "copper": (196, 108, 60), "copper_dark": (142, 70, 38),
    "copper_light": (232, 150, 96), "brass": (210, 170, 80), "oak": (156, 104, 58), "oak_dark": (108, 68, 36),
    "oak_light": (190, 140, 84), "iron": (92, 92, 100), "iron_light": (140, 140, 150),
    "hop": (150, 196, 72), "hop_dark": (96, 148, 50), "hop_light": (200, 226, 120),
    "grape": (110, 54, 150), "grape_dark": (70, 30, 104), "grape_light": (156, 96, 196), "ivy": (220, 180, 60),
    "foam": (250, 246, 232), "foam_shade": (226, 220, 200), "cream": (240, 226, 196),
    "terracotta": (196, 106, 70), "terracotta_dark": (150, 76, 50), "terracotta_light": (222, 142, 104),
    "agave": (96, 160, 150), "agave_dark": (58, 116, 110), "agave_light": (150, 204, 190),
    "porcelain": (246, 244, 240), "porcelain_shade": (220, 218, 214), "vermilion": (226, 66, 40),
    "neon": (236, 238, 70), "neon_glass": (236, 238, 70, 190), "lemon": (250, 222, 60), "olive": (118, 150, 50),
    "pimento": (214, 50, 40),
    "emerald": (40, 170, 96), "emerald_dark": (20, 110, 64), "emerald_light": (120, 220, 150),
    "louche": (196, 236, 200, 120),
    "silver": (206, 212, 220), "steel": (170, 176, 186), "steel_dark": (104, 110, 122),
    "black": (30, 30, 34), "white": (248, 248, 246), "pupil": (24, 22, 26), "tux": (36, 36, 44), "burgundy": (104, 18, 40),
    "burgundy_glass": (120, 20, 44, 170), "ghost": (226, 232, 246), "ghost_glass": (226, 232, 246, 150),
    "honey": (240, 176, 40), "honey_dark": (196, 128, 24), "bee_brown": (70, 44, 26), "comb": (250, 214, 120, 130),
    "clay": (176, 104, 66), "clay_dark": (130, 72, 44),
    "peat": (98, 70, 46), "peat_dark": (64, 44, 30), "moss": (96, 140, 60), "moss_light": (140, 180, 80),
    "ember": (255, 120, 40), "ember_hot": (255, 210, 90), "smoke": (180, 176, 184, 120), "steam": (240, 244, 250, 120),
    "ice": (200, 236, 255, 150), "ice_solid": (206, 236, 250),
    "violet_glass": (150, 80, 220, 160), "violet": (170, 100, 240), "crystal": (220, 230, 250, 110),
    "fur": (126, 82, 50), "fur_dark": (86, 54, 32), "fur_light": (176, 128, 86),
    "bernard": (170, 92, 44), "bernard_dark": (120, 60, 28), "rosy": (244, 150, 160),
    "coon": (126, 124, 130), "coon_dark": (54, 52, 58), "coon_light": (206, 204, 210),
    "coat": (176, 150, 104), "coat_dark": (130, 108, 72), "hat": (84, 62, 44),
    "flame_blue": (80, 150, 255), "flame_blue_hot": (190, 230, 255), "tan": (214, 190, 140), "pink": (240, 170, 186),
    "green": (80, 160, 70), "red": (210, 50, 44),
}


def palette(shiny):
    """-> (P, solid, ramp) for a model with its own shiny overrides."""
    def P(v):
        return pal(BASE, shiny, v)
    return P, solid_of(P), ramp_of(P)


def glow_of(P, key):
    """A shader painting a glowing palette colour."""
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return c, c
    return s


def toned(P, key):
    """A plain palette colour with the soft top/bottom tone."""
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def tiers(m, bone, profile, shader, cx=0.0, cz=0.0):
    """A round solid of revolution about the y axis: [(y0, y1, r)] stacked round boxes (glasses, pots, bulbs)."""
    for y0, y1, r in profile:
        if r <= 0:
            continue
        m.round_box(bone, cx, cz, r, r, y0, y1, shader, cut=max(0.4, round(r * 0.35, 1)))


def helix(m, bone, c, r, y0, y1, turns, t, shader, n=None):
    """A spiral of rods round the y axis (corkscrew tails, still coils)."""
    n = n or max(6, int(turns * 10))
    pts = []
    for i in range(n + 1):
        a = 2 * math.pi * turns * i / n
        pts.append((c[0] + r * math.cos(a), y0 + (y1 - y0) * i / n, c[2] + r * math.sin(a)))
    for a, b in zip(pts, pts[1:]):
        from _boxmodel import rod
        rod(m, bone, a, b, t, shader, extend=0.5)
