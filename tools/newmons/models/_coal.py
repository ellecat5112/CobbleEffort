"""Shaders shared by the coal butterfly line (Coalarva, Cinderoon, Gatterfly): coal skin, fire, rubies, ash.

Shaders return (colour, glow): colour RGB or RGBA (alpha 0 cuts the texel out, an alpha between 0 and 255 puts it on
the translucent shell layer), glow an RGB for the emissive layer or None.

Shiny: blue fire (navy -> blue -> cyan -> white) and sapphire eyes; the coal stays black.
"""
from __future__ import annotations

import math

from _boxmodel import mix

COAL = (40, 38, 44)
COAL_LIGHT = (68, 66, 76)
COAL_DARK = (22, 20, 26)
FIRE = [(110, 14, 10), (200, 40, 20), (245, 110, 30), (255, 190, 60), (255, 244, 200)]
FIRE_SHINY = [(16, 22, 90), (30, 70, 200), (40, 160, 245), (120, 230, 255), (235, 252, 255)]


def fire(t, variant):
    """The fire ramp at t in 0..1 (0 deep ember, 1 white-hot)."""
    ramp = FIRE_SHINY if variant == "shiny" else FIRE
    t = max(0.0, min(1.0, t)) * (len(ramp) - 1)
    i = min(int(t), len(ramp) - 2)
    return mix(ramp[i], ramp[i + 1], t - i)


def hashf(x, y, z):
    """A stable pseudo-random value in 0..1 for a model position (rounded to the texel's unit cell)."""
    n = math.sin(math.floor(x) * 12.9898 + math.floor(y) * 78.233 + math.floor(z) * 37.719) * 43758.5453
    return n - math.floor(n)


def coal(x, y, z, face, variant, cracks=0.0, **k):
    """Lumpy black coal: facets of slightly lighter coal, and (with `cracks` > 0) thin glowing cracks."""
    h = hashf(x * 0.5, y * 0.5, z * 0.5)
    col = COAL_LIGHT if h > 0.72 else (COAL_DARK if h < 0.18 else COAL)
    if face == "up":
        col = mix(col, COAL_LIGHT, 0.35)
    if cracks:
        w = abs(math.sin(x * 0.9 + z * 0.7 + 1.7 * math.sin(y * 0.6)) * math.cos(y * 0.8 - z * 0.5))
        if w < 0.06 * cracks:
            c = fire(0.65, variant)
            return c, c
    return col, None


def ruby(dx, dy, rx, ry, variant):
    """A faceted ruby eye centred at (0, 0) with radii rx, ry -> (colour, glow) or None outside it."""
    d = (dx / rx) ** 2 + (dy / ry) ** 2
    if d > 1:
        return None
    if variant == "shiny":
        base, hi, glow = (30, 60, 200), (190, 220, 255), (60, 120, 255)
    else:
        base, hi, glow = (190, 16, 40), (255, 190, 200), (255, 40, 70)
    if dx < -0.25 * rx and dy > 0.2 * ry and d < 0.35:
        return hi, hi
    facet = 0.85 + 0.15 * math.copysign(1, dx * dy)
    col = tuple(int(c * facet) for c in base)
    if d > 0.75:
        col = mix(col, (60, 4, 14) if variant != "shiny" else (10, 14, 60), 0.6)
    return col, glow


def glowing_segment(t_y, band, variant, seam=False):
    """A glowing abdomen segment: t_y is the height across the segment (0 bottom .. 1 top), band how close the texel
    is to the segment's middle ring (1 on it). Dark ember underneath, orange above, a yellow-hot ring round the middle."""
    if seam:
        c = fire(0.05, variant)
        return c, None
    t = 0.12 + 0.3 * t_y + 0.45 * band ** 2
    c = fire(t, variant)
    return c, fire(t, variant)
