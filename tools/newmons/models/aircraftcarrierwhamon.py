"""Aircraft Carrier Whamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the manga art on wikimon.net): a great whale carrying a warship's flight deck on its back. A slate-grey whale with a
pale grooved throat, a wide gaping mouth of fangs, small eyes and broad flippers; on its back a planked flight deck
with runway markings, an island tower with a windowed bridge and radar mast, deck cannons and running lights; a broad
fluked tail behind. 25 blocks long.

Front is -z, y is up. 30 units tall, 64 long; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, eye, local, metal, mix, mul, plane, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(25 * 30 / 64, HEIGHT, 3.4)
KIND = "floater"
K = 3
LOOK = ("a great whale carrying a flight deck: slate-grey with a pale grooved throat, a gaping fanged mouth, broad "
        "flippers, a planked runway with markings, an island tower with a windowed bridge and radar mast, deck cannons "
        "and running lights")

BASE = {"whale": (96, 110, 128), "whale_dark": (54, 62, 76), "whale_light": (150, 166, 186), "belly": (214, 220, 226),
        "groove": (150, 160, 170), "mouth": (150, 50, 70), "teeth": (246, 244, 236), "eye": (40, 40, 50),
        "pupil": (10, 10, 14), "white": (255, 255, 255), "deck": (120, 100, 80), "deck_dark": (80, 64, 50),
        "steel": (150, 156, 166), "steel_dark": (90, 96, 108), "steel_light": (210, 214, 222), "mark": (240, 230, 200),
        "window": (120, 200, 240), "light": (255, 80, 60), "cannon": (60, 64, 72)}
SHINY = {"whale": (60, 80, 150), "whale_dark": (30, 40, 90), "whale_light": (120, 150, 220), "deck": (60, 60, 64),
         "deck_dark": (30, 30, 34), "steel": (190, 160, 90), "steel_dark": (130, 100, 40)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "whale", dark="whale_dark", light="whale_light", var=0.06)
STEEL = armour(P, "steel", "steel_dark", light="steel_light", panel=(4.0, 3.0), rivets=True)
METAL = metal(P, "steel", dark="steel_dark", light="steel_light")


def bodyf(x, y, z, face, variant, box=None, **k):
    """The whale: grey, a pale belly with long grooves running down the throat."""
    p = P(variant)
    if face == "down" or (face in ("east", "west", "north") and y < 6.5):
        col = p["belly"]
        if (x * 1.2) % 1.6 < 0.3 and z < 6:
            col = p["groove"]
        return tone(col, face), None
    return HIDE(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 22.0, y - 11.5, 1.0, "eye")
        if c is not None:
            return c, None
    return bodyf(x, y, z, face, variant, box=box, **k)


def mouthf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "up":
        return tone(p["mouth"], face), None
    return bodyf(x, y, z, face, variant, box=box, **k)


def deckf(x, y, z, face, variant, box=None, **k):
    """The flight deck: planks, a dashed centre line and edge lines, a landing circle."""
    p = P(variant)
    if face == "up":
        if abs(x) < 0.3 and (z % 3.0) < 1.6:
            return p["mark"], None
        if abs(abs(x) - 6.2) < 0.25:
            return p["mark"], None
        if abs(math.hypot(x, z - 10.0) - 3.0) < 0.3:
            return p["mark"], None
        plank = (z % 1.4) < 0.12 or ((x + (math.floor(z / 1.4) % 2) * 2) % 4.0) < 0.1
        return tone(p["deck_dark"] if plank else p["deck"], face), None
    return STEEL(x, y, z, face, variant, box=box, **k)


def towerf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and 25.0 < y < 26.4 and (x + z) % 1.2 < 0.8:
        return p["window"], p["window"]
    return STEEL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("aircraftcarrierwhamon")
    top = m.bone("aircraftcarrierwhamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for z0, z1, rx, y1 in ((-14, -4, 9.0, 16.0), (-4, 8, 10.0, 17.0), (8, 18, 8.6, 15.0), (18, 26, 6.0, 12.5)):
        m.round_box(bd, 0, (z0 + z1) / 2, rx, (z1 - z0) / 2, 2.0, y1, bodyf, cut=3)
    hd = m.bone("head", bd, (0, 10, -14))
    m.round_box(hd, 0, -22.0, 8.4, 8.0, 7.5, 15.5, headf, cut=3)                  # the upper head
    jw = m.bone("jaw", hd, (0, 7.5, -14))
    m.round_box(jw, 0, -21.0, 8.0, 7.0, 2.0, 7.5, mouthf, cut=3)                  # the lower jaw, hanging open
    for i in range(12):                                                         # fangs along both jaws
        ang = math.radians(-80 + i * (160 / 11))
        px, pz = 7.6 * math.sin(ang), -22.0 - 7.2 * math.cos(ang)
        spike(m, hd, (px, 7.6, pz), (0, -1, 0), 1.2, 2.2, solid(P, "teeth"), tip=0.3)
        spike(m, jw, (px * 0.95, 7.2, pz + 0.6), (0, 1, 0), 1.0, 1.8, solid(P, "teeth"), tip=0.3)
    # the flight deck, island tower and cannons
    dk = m.bone("deck", bd, (0, 17, 4))
    m.box(dk, -7.0, 16.0, -10.0, 7.0, 18.0, 24.0, deckf)
    m.box(dk, -6.0, 13.0, -8.0, 6.0, 16.2, 22.0, STEEL)                         # hull under the deck
    m.box(dk, 3.6, 18.0, 4.0, 6.6, 24.5, 12.0, towerf)                          # the island
    m.box(dk, 3.2, 24.5, 4.6, 7.0, 27.0, 11.0, towerf)                          # the bridge, windowed
    rod(m, dk, (5.0, 27.0, 8.0), (5.0, 31.0, 8.0), 1, METAL, extend=0.0)        # radar mast
    m.box(dk, 3.6, 30.0, 7.6, 6.4, 30.6, 8.4, METAL)
    for sx in (-1, 1):
        for zz in (-6.0, 4.0, 16.0):
            rod(m, dk, (sx * 6.8, 17.0, zz), (sx * 9.0, 17.5, zz - 2.5), 1, solid(P, "cannon"), extend=0.2)
        for zz in (-8.0, 0.0, 8.0, 16.0, 23.0):
            m.box(dk, sx * 7.0 - 0.3, 17.2, zz - 0.3, sx * 7.0 + 0.3, 17.8, zz + 0.3, solid(P, "light", glow=True))
    # flippers and the fluked tail
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        f = m.bone(nm, bd, (sx * 9.0, 6.0, -6.0))
        rod(m, f, (sx * 9.0, 6.0, -6.0), (sx * 17.0, 1.0, 0.0), 6, HIDE, extend=0.5, t2=1.5)
    tl = m.bone("tail", bd, (0, 8, 26))
    rod(m, tl, (0, 8.0, 26.0), (0, 8.0, 34.0), 7, HIDE, extend=0.6, t2=5)
    for sx in (-1, 1):
        rod(m, tl, (0, 8.0, 33.0), (sx * 9.0, 9.5, 40.0), 6, HIDE, extend=0.4, t2=1.2)
    return m
