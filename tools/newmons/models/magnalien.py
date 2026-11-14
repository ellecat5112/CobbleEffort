"""Magnalien, the Mothership Pokémon (Electric/Psychic), CobbleEffortian Magneton evolved, after the art of the A.
Fakemon fanpage (the art's own name): a great silver mothership: a wide saucer ringed with a dark band of red, green
and yellow running lights, a ridged dome with one huge green eye under a dark brow, an antenna crowned with a halo of
rainbow light, four little saucer pods (like Magnemite) docked round its rim with their own coloured eyes and
antennae, thrusters glowing yellow and red, and a shimmering rainbow tractor beam that it stands on.

Shiny: a gold hull with a violet eye.

Front is -z, y is up. 30 units tall; baseScale 1.2 (2.25 m). A floater.
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix, rod, spike
from _route import tone
from _ufo import P, antenna, beam, eye_at, hull, ring, solid

SCALE = 1.2
HITBOX = [2.6, 1.85]
KIND = "floater"
K = 3
HEIGHT = 30
LOOK = ("a great silver mothership with a ring of coloured running lights, a ridged dome with one huge green eye, a "
        "rainbow halo, four little docked saucer pods and a rainbow tractor beam")
L = 6.0


def domef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        e = eye_at(p, x, y - (15.6 + L), 2.6)
        if e:
            return e
        if abs(math.hypot(x, y - (15.6 + L)) - 3.6) < 0.5 and y > 15.6 + L:
            return p["dark"], None                                            # the dark brow arch
    if face in ("up", "east", "west", "south") and abs(((y - (14.0 + L)) % 2.2) - 1.1) < 0.3:
        return p["dark"], None                                                # ridges round the dome
    return tone(p["silver_light"] if face == "up" else p["silver"], face), None


def rainbow_beam(x, y, z, face, variant, **k):
    p = P(variant)
    t = max(0.0, min(1.0, y / (6.0 + L)))
    c = mix(p["green"], p["yellow"], t * 2) if t < 0.5 else mix(p["yellow"], p["red"], (t - 0.5) * 2)
    return c + (130,), None


def build() -> Model:
    m = Model("magnalien")
    top = m.bone("magnalien", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10 + L, 0))
    m.round_box(bd, 0, 0, 10.0, 10.0, 7.6 + L, 12.4 + L, hull(band=(9.0 + L, 11.0 + L), lights=(0, 12, 10)), cut=3.4)
    m.round_box(bd, 0, 0, 7.0, 7.0, 4.6 + L, 7.8 + L, solid("dark"), cut=2.4)               # dark underbelly
    hd = m.bone("head", bd, (0, 14 + L, 0))
    m.round_box(hd, 0, 0.6, 7.0, 6.6, 12.2 + L, 19.6 + L, domef, cut=2.4)                   # the ridged dome
    antenna(m, hd, (0, 19.4 + L, 0.6), (0, 24.0 + L, 1.0), 2.0)
    ring(m, hd, (0, 23.4 + L, 1.0), 4.0, 0.8, plane="xz", n=16)                             # the rainbow halo

    for i, (x, z, key) in enumerate(((-10.6, -4.0, "yellow"), (10.6, -4.0, "red"), (-9.0, 6.0, "red"),
                                     (9.0, 6.0, "green"))):
        pd = m.bone(f"pod_{i}", bd, (x, 9 + L, z))                                          # docked saucer pods
        m.round_box(pd, x, z, 2.4, 2.4, 7.8 + L, 12.4 + L, hull(), cut=1.0)
        m.box(pd, x - 1.0, 9.0 + L, z - 2.6, x + 1.0, 11.0 + L, z - 2.4, solid(key, glow=True))
        antenna(m, pd, (x, 12.2 + L, z), (x + (0.8 if x > 0 else -0.8), 14.8 + L, z), 1.0)

    for sx, key in ((-1, "beam"), (1, "beam_red")):                                         # thruster glow
        beam(m, bd, sx * 7.0, 4.0, 0.6 + L, 7.0 + L, 1.0, 2.2, key=key, steps=2)
    m.round_box(bd, 0, 0, 2.4, 2.4, 1.6, 4.8 + L, rainbow_beam, cut=0.8)                   # the rainbow tractor beam
    m.round_box(bd, 0, 0, 4.4, 4.4, 0.0, 1.8, rainbow_beam, cut=1.4)
    return m
