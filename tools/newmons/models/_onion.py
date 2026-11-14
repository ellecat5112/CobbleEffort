"""Shared colours and parts for the onion line (Tearion, Shallorn, Pungallium), after the art of the A. Fakemon fanpage
(names ours): a little white onion that never stops crying, a brown shallot with droopy leaves and a root moustache,
and a green bulb under a great stinking purple allium flower-head.

Shiny: a red onion line: rose-red bulbs and a golden flower-head.
"""
from __future__ import annotations

import math

from _afake import ramp_of, solid_of
from _route import pal, tone

BASE = {"white": (240, 236, 214), "white_shade": (214, 206, 176), "green": (128, 196, 88), "green_dark": (70, 140, 72),
        "green_light": (196, 228, 120), "brown": (130, 100, 76), "brown_dark": (92, 70, 54), "orange": (240, 140, 90),
        "orange_light": (250, 186, 140), "purple": (140, 110, 220), "purple_dark": (96, 72, 176),
        "purple_light": (184, 160, 240), "tear": (170, 220, 250), "pupil": (40, 34, 40), "bulb": (96, 160, 80),
        "stink": (170, 140, 230, 150)}
SHINY = {"white": (226, 150, 170), "white_shade": (196, 110, 136), "brown": (150, 60, 80), "brown_dark": (110, 40, 60),
         "purple": (236, 196, 80), "purple_dark": (196, 150, 50), "purple_light": (250, 226, 140),
         "bulb": (176, 80, 110), "stink": (240, 210, 110, 150)}


def P(v):
    return pal(BASE, SHINY, v)


solid = solid_of(P)
ramp = ramp_of(P)


def teary_eye(p, dx, dy, r, closed=False):
    """A big watery eye (or a squeezed-shut one) with a tear streaming down below it. -> colour or None."""
    if closed:
        if abs(math.hypot(dx, dy + r * 0.6) - r * 0.6) < 0.18 and dy > -r * 0.6:
            return p["pupil"]
        if abs(dx) < 0.3 and -r * 3.0 < dy < -r * 0.4:
            return p["tear"]
        return None
    d = math.hypot(dx, dy)
    if d < r:
        if math.hypot(dx + r * 0.3, dy - r * 0.3) < r * 0.3:
            return p["white"]
        return p["pupil"] if d < r * 0.55 else p["tear"]
    if abs(dx) < 0.3 and -r * 3.2 < dy < -r * 0.8:
        return p["tear"]                                                       # the tear streaming down
    return None


def bulb(m, bone, cy, r, h, shader, tip=None):
    """An onion bulb: stacked rounded slices, widest a little below the middle, narrowing to a neck."""
    n = max(4, int(h / 1.8))
    for i in range(n):
        t = (i + 0.5) / n
        rr = r * math.sin(math.pi * min(1.0, t * 0.95 + 0.05)) ** 0.6 * (1 - 0.35 * max(0.0, t - 0.6))
        if rr < 0.6:
            continue
        y0 = cy - h / 2 + i * h / n
        m.round_box(bone, 0, 0, rr, rr, y0, y0 + h / n, shader, cut=max(0.5, rr * 0.35))
