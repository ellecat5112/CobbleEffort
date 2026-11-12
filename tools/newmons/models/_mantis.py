"""Shaders shared by the mantis line (Prayling, Mawntis, Mantasma): leaf-green chitin, brown bands, pale stripes, leaf
fronds, teeth, and Mantasma's ghostly glow. None of them has eyes: the line is blind (its ability, Blindsight, makes
every move it uses hit).

Shaders return (colour, glow) like the coal line's: RGBA alpha 0 cuts out, alpha between 0 and 255 is the translucent
shell layer (Mantasma's spectral blades), glow an RGB for the emissive layer.

Shiny: an orchid mantis: petal pink and white, its ghostly glow violet.
"""
from __future__ import annotations

import math

from _boxmodel import mix

BASE = {"green": (150, 200, 96), "green_light": (196, 228, 124), "green_dark": (86, 140, 60), "brown": (132, 94, 62),
        "brown_dark": (84, 58, 40), "pale": (238, 234, 152), "leg": (54, 42, 38), "tooth": (246, 240, 222),
        "maw": (58, 18, 64), "maw_glow": (150, 70, 210), "ghost": (160, 255, 210), "claw": (150, 104, 70)}
SHINY = {"green": (240, 172, 204), "green_light": (252, 222, 234), "green_dark": (200, 112, 152), "brown": (176, 96, 136),
         "brown_dark": (120, 60, 96), "pale": (255, 250, 255), "leg": (96, 52, 84), "maw_glow": (210, 110, 255),
         "ghost": (210, 160, 255), "claw": (200, 120, 160)}


def P(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def along(z, box):
    """How far a texel is along a rod box (0 at its start point, 1 at its end): rods run along -z before rotating."""
    return (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)


def chitin(x, y, z, face, variant, key="green", **k):
    """Smooth chitin: lighter on top, darker underneath."""
    pal = P(variant)
    c = pal[key]
    if face == "up":
        return mix(c, pal["green_light"] if key == "green" else (255, 255, 255), 0.25), None
    if face == "down":
        return mix(c, (0, 0, 0), 0.2), None
    return c, None


def striped(key, stripes=(0.3, 0.55, 0.8), width=0.08, glow=False, tip=None):
    """A rod shader: chitin with pale bands round it at the given places along it (glowing ghostly if `glow`), and a
    brown claw tip past `tip`."""
    def s(x, y, z, face, variant, box=None, **k):
        pal = P(variant)
        t = along(z, box)
        if tip is not None and t > tip:
            return pal["claw"], None
        if face not in ("north", "south") and any(abs(t - c) < width for c in stripes):
            return pal["pale"], (pal["ghost"] if glow else None)
        return chitin(x, y, z, face, variant, key)
    return s


def frond(origin, leaves, length, width):
    """A flat plane of leaflets fanning out from `origin` (x, z) along the given angles (degrees from +z): each a
    pointed leaf with a darker midrib. Outside them the plane is cut away."""
    ox, oz = origin

    def s(x, y, z, face, variant, **k):
        pal = P(variant)
        for ang in leaves:
            a = math.radians(ang)
            dx, dz = x - ox, z - oz
            u = dx * math.sin(a) + dz * math.cos(a)             # along the leaf
            v = dx * math.cos(a) - dz * math.sin(a)             # across it
            if 0 <= u <= length:
                w = width * math.sin(math.pi * u / length) ** 0.8
                if abs(v) <= w:
                    if abs(v) < 0.18:
                        return pal["green_dark"], None
                    return mix(pal["green"], pal["green_light"], u / length * 0.6), None
        return (0, 0, 0, 0), None
    return s


def tooth(x, y, z, face, variant, **k):
    pal = P(variant)
    return (pal["tooth"] if face != "down" else mix(pal["tooth"], (0, 0, 0), 0.15)), None


def maw(glow=False):
    """Inside the mouth: dark (glowing ghostly in Mantasma's) on the front, plain dark chitin on the sides."""
    def s(x, y, z, face, variant, **k):
        pal = P(variant)
        if face != "north":
            return pal["green_dark"], None
        return pal["maw"], (pal["maw_glow"] if glow else None)
    return s


def spectral(x, y, z, face, variant, **k):
    """Mantasma's ghost blades: translucent, glowing."""
    pal = P(variant)
    return pal["ghost"] + (150,), pal["ghost"]


def spikef(x, y, z, face, variant, **k):
    pal = P(variant)
    return pal["pale"], None
