"""Gattai Ancient Volcamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the official art on wikimon.net): Ancient Volcamon combined and set ablaze: the cratered rock giant with its small
horned head, its whole body wrapped in towering orange flames. 35 blocks tall.

Front is -z, y is up. 70 units tall (the flames included); Ultimate stage (no level on wikimon). Built on the Ancient
Volcamon model with flames added.
"""
from __future__ import annotations

from _digi import sized
from _digidetail import cutout, flame_inside, local
from _variant import clone

_V = clone("ancientvolcamon", "gattaiancientvolcamon",
           base={"fire": (255, 150, 30, 215), "fire_core": (255, 240, 170, 235)},
           shiny={"fire": (90, 170, 255, 215), "fire_core": (220, 240, 255, 235)})
HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = _V.KIND
K = _V.K
ANIM = getattr(_V, "ANIM", {"leg_amp": 8})
LOOK = "a cratered rock giant with a small horned head, its whole body wrapped in towering orange flames"


def firef(x, y, z, face, variant, box=None, **k):
    p = _V.P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def build():
    m = _V.build()
    spots = [(-14.0, 6.0, 0.0), (14.0, 6.0, 0.0), (-16.0, 24.0, -2.0), (16.0, 24.0, -2.0), (-10.0, 40.0, 2.0),
             (10.0, 40.0, 2.0), (0.0, 46.0, 6.0), (-6.0, 14.0, -8.0), (6.0, 14.0, -8.0)]
    for j, at in enumerate(spots):
        for ang in (0, 90):
            m.box("body", at[0] - 4.0, at[1], at[2], at[0] + 4.0, at[1] + 14.0, at[2],
                  cutout(flame_inside(4, 0.1, j + 3), firef), rotation=(0, ang, 0), pivot=at)
    return m
