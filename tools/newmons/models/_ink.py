"""Shared colours and shaders for the ink line (Incl, Incwell, Calligrimm), after the fakemon art the user shared (the
art's own names; artist not named), with the user's ideas: an ink blob with a calligraphy pen nib for a face, then
rising out of an inkwell, then a gargantuan ink kaiju with pen nibs for claws and a maw of broken glass shards.

Glossy purple-black ink, silver nibs with a dark slit and breather hole, glowing yellow eyes and ink-fire.
Shiny: royal-blue ink and gold nibs.
"""
from __future__ import annotations

import math

from _boxmodel import mix
from _route import pal, tone

BASE = {"ink": (40, 26, 58), "ink_light": (82, 62, 112), "ink_dark": (22, 14, 32), "nib": (206, 210, 216),
        "nib_shade": (150, 156, 166), "nib_dark": (40, 36, 48), "eye": (252, 214, 70), "eye_glow": (255, 220, 80),
        "fire": (250, 200, 50), "fire_core": (255, 244, 170), "glass": (196, 226, 236), "glass_edge": (236, 248, 252),
        "bottle_cap": (90, 70, 56)}
SHINY = {"ink": (30, 46, 120), "ink_light": (70, 100, 190), "ink_dark": (16, 24, 70), "nib": (236, 200, 96),
         "nib_shade": (196, 156, 60), "eye": (120, 240, 250), "eye_glow": (140, 250, 255), "fire": (110, 220, 250),
         "fire_core": (220, 252, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def inkf(x, y, z, face, variant, **k):
    """Glossy ink: a soft highlight streak on top and the upper fronts, deep shadow underneath."""
    p = P(variant)
    if face == "down":
        return p["ink_dark"], None
    if face in ("up", "north", "east", "west") and math.sin(x * 0.9 + z * 0.5) * math.sin(y * 0.55 + z * 0.3) > 0.72:
        return p["ink_light"], None
    return tone(p["ink"], face), None


def nibf(cx, tip_y, w, h, tip_up=False):
    """A pen nib plate on the xy plane: a pointed shield of silver with a dark slit from the tip and a breather hole.
    cx: centre x, tip_y: y of the point, w/h: width and height (the point is at tip_y, the wide end h below it if tip_up, else above)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        t = (tip_y - y) / h if tip_up else (y - tip_y) / h       # 0 at the point, 1 at the wide end
        t = -t if t < 0 else t
        if face in ("north", "south"):
            half = w / 2 * min(1.0, t * 1.6)
            if abs(x - cx) > half + 0.05:
                return (0, 0, 0, 0), None                            # cut to the nib's shape
            hole_t = 0.55
            if math.hypot((x - cx) / (w * 0.09), (t - hole_t) * h / (w * 0.09)) < 1:
                return p["nib_dark"], None                           # breather hole
            if abs(x - cx) < 0.18 * max(1, w / 6) and t < hole_t:
                return p["nib_dark"], None                           # the slit
            return (p["nib"] if abs(x - cx) < half * 0.55 else p["nib_shade"]), None
        return tone(p["nib_shade"], face), None
    return s


def eyef(x, y, z, face, variant, **k):
    p = P(variant)
    return p["eye"], p["eye_glow"]


def firef(axes_u, cu, base_v, height, width=3.0):
    """A glowing tongue of ink-fire on a plane: yellow edged, pale core, cut to a flame shape rising from base_v,
    centred on u = cu along the plane's horizontal axis."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u = {"x": x, "z": z}[axes_u] - cu
        t = (y - base_v) / height
        if t < 0 or t > 1:
            return (0, 0, 0, 0), None
        half = width / 2 * (1 - t) ** 0.8 * (0.6 + 0.4 * math.sin(t * 3.1))
        uu = u - math.sin(t * 2.4) * 1.2
        if abs(uu) > half:
            return (0, 0, 0, 0), None
        c = p["fire_core"] if abs(uu) < half * 0.4 else p["fire"]
        return c, c
    return s


def glassf(x, y, z, face, variant, **k):
    """Broken glass: translucent (the shell layer), brighter at the edges."""
    p = P(variant)
    edge = (abs(x * 3.1 + z * 1.7) % 1.0) < 0.12
    return (p["glass_edge"] if edge else p["glass"]) + ((200,) if edge else (130,)), None
