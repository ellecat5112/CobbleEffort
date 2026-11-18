"""Jougamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the moon goddess Chang'e among the Olympos: a slender warrior in close-fitting golden armour with
a rabbit-eared golden helm and a blue visor, a long pink braid tied with a red tassel, pale blue sash ribbons and a
dark under-suit, sitting on a great golden crescent moon engraved with rabbits. 35 blocks tall.

Front is -z, y is up. 64 units tall (the moon); Ultimate stage. Built as officially drawn (fully armoured).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, metal, solid, strands
from _dorbickmon import mount
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = ("a slender warrior in golden armour with a rabbit-eared helm and a long pink braid, sitting on a great golden "
        "crescent moon")
BASE = {"gold": (240, 200, 80), "gold_dark": (160, 120, 30), "gold_light": (255, 240, 180), "dark": (40, 40, 56),
        "dark_light": (90, 90, 110), "blue": (90, 170, 240), "pink": (240, 120, 170), "pink_dark": (180, 60, 110),
        "red": (200, 40, 50), "sash": (200, 230, 250), "sash_dark": (140, 180, 220), "eye": (200, 240, 255)}
SHINY = {"gold": (220, 224, 236), "gold_dark": (130, 136, 156), "gold_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light", trim="dark", trim_w=0.2)
MOON = metal(P, "gold", dark="gold_dark", light="gold_light")


def build():
    m = Model("jougamon")
    top = m.bone("jougamon", None, (0, 0, 0))
    mb = m.bone("moon", top, (0, 30, 6))
    n = 16                                                                           # crescent moon (faces front)
    for i in range(n):
        a0 = math.radians(-150 + 240 * i / n)
        a1 = math.radians(-150 + 240 * (i + 1) / n)
        w = 2.0 + 4.0 * math.sin(math.pi * (i + 0.5) / n)
        p0 = (30.0 * math.sin(a0) * 0.9, 34.0 - 30.0 * math.cos(a0), 6.0)
        p1 = (30.0 * math.sin(a1) * 0.9, 34.0 - 30.0 * math.cos(a1), 6.0)
        rod(m, mb, p0, p1, max(1, round(w)), MOON, extend=0.6, t2=2)
    i_box, i_bone = len(m.boxes), len(m.bones)                                      # the seated goddess
    mats = {"skin": GOLD, "chest": GOLD, "abs": fabric(P, "dark", "dark_light"), "pelvis": GOLD, "neck": GOLD,
            "deltoid": GOLD, "upper_arm": GOLD, "forearm": GOLD, "hand": GOLD, "finger": GOLD, "thigh": GOLD,
            "knee": GOLD, "shin": GOLD, "calf": GOLD, "foot": GOLD, "toe": GOLD}
    a = humanoid(m, mats, bulk=0.75, arm_bulk=0.78, leg_bulk=0.8, name="goddess")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, GOLD, cut=1)
    m.round_box(hd, 0, -2.8, 2.0, 0.4, 56.6, 57.8, solid(P, "blue"), cut=0)
    for sx in (-1, 1):                                                               # rabbit ears
        m.round_box(hd, sx * 1.4, 0.4, 0.8, 0.6, 59.6, 67.0, GOLD, cut=0)
        m.round_box(hd, sx * 1.4, -0.3, 0.4, 0.2, 61.0, 66.0, solid(P, "blue"), cut=0)
    bp = [(0, 58.0, 2.6), (1.0, 48.0, 5.0), (2.0, 36.0, 6.0), (3.0, 26.0, 4.0)]      # long pink braid
    for p0, p1 in zip(bp, bp[1:]):
        rod(m, hd, p0, p1, 2, strands(P, "pink", "pink_dark"), extend=0.4)
    m.round_box(hd, 3.0, 4.0, 1.0, 1.0, 26.0, 28.4, solid(P, "red"), cut=0)
    for j in range(2):                                                               # sash ribbons
        rod(m, bd, (-2.0 + j * 4.0, 34.0, 2.0), (-4.0 + j * 10.0, 14.0, 4.0), 1, fabric(P, "sash", "sash_dark"), extend=0.3,
            t2=2)
    m.boxes[i_box:] = [b for b in m.boxes[i_box:] if b.bone not in ("leg_left", "leg_right")]
    m.bones[i_bone:] = [b for b in m.bones[i_bone:] if b["name"] not in ("leg_left", "leg_right")]
    for sx in (-1, 1):                                                               # seated legs
        rod(m, bd, (sx * 2.4, 33.0, 0.0), (sx * 2.8, 33.0, -9.0), 3, GOLD, extend=0.6)
        rod(m, bd, (sx * 2.8, 33.0, -9.0), (sx * 3.0, 20.0, -10.0), 2, GOLD, extend=0.4)
        m.round_box(bd, sx * 3.0, -11.4, 1.4, 2.2, 18.0, 20.4, solid(P, "dark"), cut=0)
    mount(m, i_box, i_bone, -26.0, 0.0, "moon")
    return m
