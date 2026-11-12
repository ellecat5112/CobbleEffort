"""Shaders shared by the fossil lines: glossy black tar with bones in it (Petroleodd, Petroleossil) and petrified
fungal stone with glowing mycelium (Mycolith, Taxitower).

Shiny: amber tar with ivory bones; pale chalk stone with teal-and-pink mycelium.
"""
from __future__ import annotations

import math

from _boxmodel import mix
from _route import pal, tone

TAR = {"tar": (30, 28, 34), "tar_light": (72, 70, 82), "shine": (200, 204, 220), "bone": (236, 224, 190),
       "bone_dark": (176, 160, 120), "fossil": (192, 128, 70), "fossil_dark": (130, 80, 44), "hole": (26, 20, 18),
       "eye": (250, 250, 250), "red": (230, 40, 40), "tooth": (232, 210, 170)}
TAR_SHINY = {"tar": (120, 70, 20), "tar_light": (180, 120, 40), "shine": (255, 230, 160), "fossil": (226, 214, 190),
             "fossil_dark": (168, 150, 120), "red": (90, 230, 255)}

STONE = {"stone": (122, 116, 110), "stone_dark": (86, 82, 80), "stone_light": (160, 152, 140), "ring": (104, 96, 90),
         "myc1": (170, 90, 230), "myc2": (250, 170, 60), "root": (100, 84, 70), "eye": (240, 200, 110),
         "shelf": (150, 120, 90), "shelf_dark": (110, 86, 64), "spore": (255, 210, 90), "slate": (90, 96, 108)}
STONE_SHINY = {"stone": (206, 200, 188), "stone_dark": (160, 154, 144), "stone_light": (236, 230, 220),
               "ring": (180, 172, 160), "myc1": (60, 220, 200), "myc2": (250, 120, 180), "eye": (120, 240, 230),
               "spore": (140, 240, 220), "slate": (176, 180, 186)}


def hashf(x, y, z):
    n = math.sin(math.floor(x) * 12.9898 + math.floor(y) * 78.233 + math.floor(z) * 37.719) * 43758.5453
    return n - math.floor(n)


def tar(x, y, z, face, variant, **k):
    """Glossy black tar: little white highlights here and there, lighter on top."""
    p = pal(TAR, TAR_SHINY, variant)
    if face in ("up", "north", "west") and hashf(x * 3.1, y * 3.1, z * 3.1) > 0.985:
        return p["shine"], None
    c = p["tar_light"] if face == "up" and hashf(x * 0.5 + 3, y, z * 0.5) > 0.6 else p["tar"]
    return tone(c, face), None


def bone(x, y, z, face, variant, **k):
    p = pal(TAR, TAR_SHINY, variant)
    return tone(p["bone"] if face != "down" else p["bone_dark"], face), None


def fossil(x, y, z, face, variant, **k):
    """Brown fossil bone, with darker cracks between plates."""
    p = pal(TAR, TAR_SHINY, variant)
    if abs(math.sin(x * 0.8 + z * 0.6) * math.cos(y * 0.7)) < 0.05:
        return p["fossil_dark"], None
    return tone(p["fossil"], face), None


def mycelium_stone(x, y, z, face, variant, rings=None, **k):
    """Weathered stone bark cracked with glowing purple and amber mycelial threads; concentric rings on top faces
    centred on `rings` (x, z)."""
    p = pal(STONE, STONE_SHINY, variant)
    if face == "up" and rings is not None:
        r = math.hypot(x - rings[0], z - rings[1])
        return (p["ring"] if int(r * 1.4) % 2 else p["stone_light"]), None
    w = abs(math.sin(x * 0.7 + z * 0.9 + 2.1 * math.sin(y * 0.35)) * math.cos(y * 0.9 - x * 0.4))
    if face not in ("up", "down") and w < 0.045:
        c = p["myc1"] if math.sin(y * 0.5 + x) > 0 else p["myc2"]
        return c, c
    stripe = int(y * 0.8 + hashf(x * 0.3, 0, z * 0.3) * 1.5) % 3 == 0          # bark-like bands
    c = p["stone_dark"] if stripe else p["stone"]
    return tone(c, face), None
