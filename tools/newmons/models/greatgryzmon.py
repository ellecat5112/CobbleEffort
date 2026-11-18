"""Great Gryzmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the great grizzly: a hulking violet-furred bear-man with red legs and arms licked with
black flame patterns, a shaggy white mane round a masked red face, a dark coat with a gold X across the chest, huge
white claws on its feet and one fist sheathed in a riveted gauntlet blazing with fire. 25 blocks tall.

Front is -z, y is up. 56 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import cutout, fabric, flame_inside, fur, local, metal, riveted, skin, solid, strands
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hulking violet bear-man with flame-patterned red limbs, a shaggy white mane, a dark coat with a gold X and "
        "a riveted gauntlet blazing with fire")
BASE = {"violet": (90, 70, 170), "violet_dark": (40, 30, 100), "red": (200, 40, 40), "red_dark": (120, 14, 18),
        "flame": (30, 26, 34), "mane": (236, 230, 220), "mane_dark": (170, 160, 150), "coat": (40, 36, 46),
        "coat_dark": (14, 12, 18), "gold": (240, 200, 60), "claw": (246, 246, 246), "steel": (70, 70, 80),
        "steel_dark": (30, 30, 36), "eye": (250, 220, 60), "fire": (255, 140, 40, 215), "fire_core": (255, 240, 170, 240)}
SHINY = {"violet": (60, 60, 70), "violet_dark": (24, 24, 30), "red": (240, 170, 40), "red_dark": (170, 100, 10)}


def P(v):
    return pal(BASE, SHINY, v)


VIOLET = fur(P, "violet", "violet_dark", length=1.2, density=2.0)
RED0 = fur(P, "red", "red_dark", length=1.0, density=2.0)


def limbf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(((y * 0.6 + abs(x) * 0.4) % 3.4) - 1.7) < 0.35 and face != "down":
        return tone(p["flame"], face), None
    return RED0(x, y, z, face, variant, box=box, **k)


def coatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(abs(x) - (y - 30.0) * 0.45 + 3.0) < 0.6 and 24.0 < y < 44.0:
        return tone(p["gold"], face), None
    return fabric(P, "coat", "coat_dark")(x, y, z, face, variant, box=box, **k)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def build():
    m = Model("greatgryzmon")
    top = m.bone("greatgryzmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    m.round_box(bd, 0, 0.6, 10.0, 8.0, 16.0, 34.0, VIOLET, cut=3)                       # big belly
    m.round_box(bd, 0, 0.6, 10.6, 8.6, 26.0, 44.0, coatf, cut=3)                        # dark coat
    hd = m.bone("head", bd, (0, 44, -2))
    m.round_box(hd, 0, -2.0, 4.0, 3.6, 42.0, 50.0, skin(P, "red", dark="red_dark"), cut=2)
    m.round_box(hd, 0, -5.4, 2.0, 1.4, 43.0, 46.0, solid(P, "mane"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.4), 47.0, -5.7, max(sx * 0.8, sx * 2.4), 47.8, -5.5, solid(P, "eye"))
        m.round_box(hd, sx * 3.4, -1.0, 1.2, 1.0, 49.0, 51.4, VIOLET, cut=0)
    for i in range(16):                                                                   # shaggy white mane
        ang = 2 * math.pi * i / 16
        spike(m, hd, (5.0 * math.cos(ang), 46.0 + 5.0 * math.sin(ang), 0.0), (math.cos(ang), math.sin(ang), 0.4), 2.2,
              6.0, strands(P, "mane", "mane_dark"), tip=0.9)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 10.0, 40.0, 0))
        rod(m, ab, (sx * 10.0, 40.0, 0), (sx * 14.0, 28.0, -4.0), 5, limbf, extend=0.6)
        if sx > 0:                                                                         # blazing gauntlet
            rod(m, ab, (14.0, 28.0, -4.0), (16.0, 32.0, -14.0), 6, riveted(P, "steel", "steel_dark"), extend=0.4)
            for j in range(4):
                spike(m, ab, (14.0 + (j - 1.5) * 1.6, 34.0, -16.0), (0, 0.4, -1), 1.0, 4.0, solid(P, "claw"), tip=0.8)
            for ang in (0, 90):
                m.box(ab, 13.0, 34.0, -16.0, 19.0, 46.0, -16.0, cutout(flame_inside(4, 0.2, 5), firef),
                      rotation=(0, ang, 0), pivot=(16.0, 34.0, -16.0))
        else:
            rod(m, ab, (-14.0, 28.0, -4.0), (-14.0, 16.0, -6.0), 5, limbf, extend=0.6)
            for j in range(4):
                spike(m, ab, (-14.0 + (j - 1.5) * 1.4, 14.0, -6.0), (0, -1, -0.4), 1.0, 5.0, solid(P, "claw"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 6.0, 18.0, 0))
        rod(m, lg, (sx * 6.0, 18.0, 0), (sx * 7.0, 4.0, -1.0), 6, limbf, extend=0.6)
        m.round_box(lg, sx * 7.0, -2.0, 4.0, 5.0, 0.0, 4.0, limbf, cut=1)
        for j in range(4):
            spike(m, lg, (sx * 7.0 + (j - 1.5) * 2.0, 1.0, -6.6), (0, -0.2, -1), 1.2, 4.0, solid(P, "claw"), tip=0.8)
    return m
