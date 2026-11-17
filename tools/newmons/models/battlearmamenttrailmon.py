"""Battle Armament Trailmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the art on wikimon.net, a
manga drawing): an armoured war-train. A long streamlined locomotive body with a glazed cockpit nose and a face in its
lower front, layered steel armour plates with rivets, rows of round ports, turrets of long cannons along its back
and side gun pods, running on heavy wheels along its own rails. 15 blocks tall.

Front is -z, y is up. 34 units tall (very long); Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, local, metal, plane, riveted, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("an armoured war-train: a streamlined locomotive with a glazed cockpit nose and a face below, layered riveted "
        "plates, round ports, turrets of long cannons and heavy wheels")
BASE = {"steel": (190, 194, 206), "steel_dark": (90, 94, 106), "steel_light": (240, 242, 250), "glass": (90, 140, 180),
        "glass_dark": (40, 70, 100), "black": (30, 30, 36), "eye": (255, 200, 60), "red": (200, 40, 40)}
SHINY = {"steel": (170, 140, 90), "steel_dark": (100, 70, 30), "steel_light": (240, 210, 150)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = riveted(P, "steel", "steel_dark", light="steel_light", spacing=2.4)
HULL = armour(P, "steel", "steel_dark", light="steel_light", seams=(3.0,))
GUN = metal(P, "steel", dark="steel_dark", light="steel_light")


def glassf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    if (a % 3.0) < 0.4 or (b % 3.0) < 0.4:
        return tone(p["steel_dark"], face), None                 # window frames
    return tone(p["glass"], face), None


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 3.0) < 1.2 and abs(y - 10.0) < 0.6:
                return p["eye"], p["eye"]
        if abs(y - 6.6) < 0.4 and abs(x) < 3.0:
            return p["black"], None
    return PLATE(x, y, z, face, variant, box=box, **k)


def portsf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        a, b = plane(x, y, z, face)
        if math.hypot((a % 3.4) - 1.7, b - 16.0) < 0.9:
            return p["black"], None
    return HULL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("battlearmamenttrailmon")
    top = m.bone("battlearmamenttrailmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.box(bd, -7.0, 4.0, -18.0, 7.0, 22.0, 30.0, portsf)                                # main hull
    m.box(bd, -7.6, 12.0, -18.0, 7.6, 14.0, 30.0, PLATE)                                # armour belt
    m.box(bd, -7.0, 4.0, -24.0, 7.0, 14.0, -18.0, facef)                                # lower face
    m.box(bd, -6.0, 14.0, -26.0, 6.0, 22.0, -16.0, glassf, rotation=(-25, 0, 0), pivot=(0, 14.0, -18.0))   # cockpit
    m.box(bd, -5.0, 22.0, -12.0, 5.0, 27.0, 26.0, HULL)                                 # upper deck
    for j, z in enumerate((-6.0, 6.0, 18.0)):                    # cannon turrets on the back
        m.round_box(bd, 0, z, 3.6, 3.6, 27.0, 30.0, PLATE, cut=1)
        for dx in (-1.2, 1.2):
            rod(m, bd, (dx, 29.0, z), (dx * 1.4, 31.0, z - 14.0), 1, GUN, extend=0)
    for sx in (-1, 1):                                           # side gun pods
        for z in (-8.0, 4.0, 16.0):
            m.round_box(bd, sx * 8.6, z, 1.6, 2.2, 8.0, 12.0, PLATE, cut=1)
            rod(m, bd, (sx * 8.6, 10.0, z), (sx * 12.0, 10.0, z - 2.0), 1, GUN, extend=0)
        for z in (-14.0, -6.0, 2.0, 10.0, 18.0, 26.0):           # wheels
            m.round_box(bd, sx * 7.4, z, 0.8, 3.0, 0.0, 6.0, solid(P, "black"), cut=1)
    for sx in (-1, 1):                                           # rails under it
        m.box(top, sx * 5.0 - 0.6, -1.0, -30.0, sx * 5.0 + 0.6, 0.0, 36.0, GUN)
    return m
