"""Butenmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the tengu warlord. A stocky armoured warrior in red-lacquered samurai plate laced with green, dark
blue skin, a horned red kabuto with a gold crest over a fierce masked face, great blue-grey feathered wings with red
coverts, a red cape, clawed blue gauntlets and taloned feet, holding a long glaive with a broad black-and-red blade.
35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import cape, dome, humanoid
from _digidetail import armour, fabric, feathers, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a stocky tengu warlord in red-lacquered samurai plate laced with green, a horned red kabuto with a gold crest, "
        "great blue-grey wings, clawed blue gauntlets and a long black-and-red glaive")
BASE = {"red": (200, 40, 40), "red_dark": (110, 14, 18), "red_light": (250, 120, 110), "green": (50, 130, 80),
        "green_dark": (20, 70, 40), "blue": (40, 60, 160), "blue_dark": (16, 24, 80), "blue_light": (100, 130, 220),
        "gold": (240, 196, 60), "gold_dark": (170, 120, 20), "wing": (150, 170, 210), "wing_dark": (80, 100, 150),
        "steel": (204, 208, 220), "steel_dark": (90, 94, 106), "black": (30, 28, 34), "claw": (230, 230, 236),
        "eye": (250, 230, 80)}
SHINY = {"red": (40, 40, 48), "red_dark": (16, 16, 20), "red_light": (110, 110, 124), "wing": (230, 230, 240),
         "wing_dark": (170, 170, 186), "green": (200, 160, 40), "green_dark": (130, 90, 10)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", light="red_light", trim="gold", trim_w=0.35)
SKIN = skin(P, "blue", dark="blue_dark", light="blue_light", var=0.03)
STEEL = metal(P, "steel", dark="steel_dark")


def laced(x, y, z, face, variant, box=None, **k):
    """Samurai plate: red lames laced with green cords."""
    p = P(variant)
    if y % 2.4 < 0.4:
        return tone(p["red_dark"], face), None
    if face in ("north", "south") and (x * 1.2) % 3.0 < 0.4:
        return tone(p["green"], face), None
    return RED(x, y, z, face, variant, box=box, **k)


def bladef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if abs(u / max(W, 1e-6) - 0.5) < 0.12 and 0.2 < v / max(H, 1e-6) < 0.85:
        return tone(p["red"], face), None
    return STEEL(x, y, z, face, variant, box=box, **k) if u < 0.4 else (tone(p["black"], face), None)


def build():
    m = Model("butenmon")
    mats = {"skin": SKIN, "chest": laced, "abs": laced, "pelvis": laced, "deltoid": RED, "upper_arm": SKIN,
            "forearm": SKIN, "hand": SKIN, "finger": SKIN, "claw": solid(P, "claw"), "thigh": fabric(P, "green",
            "green_dark"), "knee": RED, "shin": RED, "calf": RED, "foot": RED, "talon": solid(P, "claw")}
    a = humanoid(m, mats, bulk=1.35, arm_bulk=1.3, leg_bulk=1.3, digitigrade=True, claws=True, talons=True,
                 name="butenmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.4, 60.4, SKIN, cut=1)
    m.box(hd, -2.4, 54.4, -3.6, 2.4, 57.4, -2.8, solid(P, "red_dark"))                   # mask
    for sx in (-1, 1):
        m.box(hd, sx * 1.2 - 0.5, 58.0, -3.3, sx * 1.2 + 0.5, 58.6, -3.1, solid(P, "eye", glow=True))
    dome(m, hd, (0, 59.4, 0), 4.0, 3.4, RED, layers=3)                                   # kabuto
    m.round_box(hd, 0, 0.6, 4.8, 4.4, 57.4, 58.6, RED, cut=1)                            # brim / neck guard
    for sx in (-1, 1):
        rod(m, hd, (sx * 1.4, 62.0, -2.0), (sx * 5.4, 67.0, -3.0), 1, solid(P, "gold"), extend=0.3, t2=2)  # crest
        rod(m, hd, (sx * 3.6, 61.0, 0.6), (sx * 6.0, 64.0, 3.4), 2, RED, extend=0.3)       # horns
    for sx in (-1, 1):                                                                   # big sode pauldrons
        dome(m, bd, (sx * 8.0, 47.0, 0.3), 4.4, 4.0, laced, layers=3)
    for side in (1, -1):                                                                 # great feathered wings
        feather_wing(m, bd, (side * 3.0, 50.0, 3.6), 22.0, 12.0, 3,
                     feathers(P, "wing", "wing_dark", size=(1.6, 3.2)), side=side, sweep=25, droop=0.2)
        feather_wing(m, bd, (side * 3.0, 51.0, 3.2), 10.0, 5.0, 1, feathers(P, "red", "red_dark", size=(1.2, 2.0)),
                     side=side, sweep=20)
    cb = m.bone("cap", bd, (0, 52, 3))
    cape(m, cb, 52.0, 16.0, 36.0, fabric(P, "red", "red_dark", axis="y"), z=4.6, flare=0.6, panels=6, sweep=(0, 3))
    ar = a["arm_right"]                                                                  # the glaive
    h = ar["hand"]
    gb = m.bone("glaive", ar["bone"], h)
    rod(m, gb, (h[0], h[1] - 14.0, h[2]), (h[0], h[1] + 26.0, h[2]), 1, solid(P, "black"), extend=0)
    for y in (h[1] + 6.0, h[1] - 6.0):
        m.box(gb, h[0] - 0.8, y - 0.5, h[2] - 0.8, h[0] + 0.8, y + 0.5, h[2] + 0.8, solid(P, "gold"))
    m.box(gb, h[0] - 1.6, h[1] + 25.0, h[2] - 1.6, h[0] + 1.6, h[1] + 26.6, h[2] + 1.6, STEEL)
    m.box(gb, h[0] - 2.0, h[1] + 26.6, h[2], h[0] + 2.0, h[1] + 40.0, h[2], bladef)
    spike(m, gb, (h[0], h[1] + 40.0, h[2]), (0, 1, 0), 2.0, 3.0, STEEL)
    return m
