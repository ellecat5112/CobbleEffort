"""Amaterasumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the sun goddess of the Digital World. A slender figure in crimson and white armour with gold
trim, a gold sun-ray crown, a white skirt-guard, two huge gold sun discs on its back whose rays spread like organ
pipes, a yin-yang mark at the heart of each and long red-and-gold claws hanging beneath them. 35 blocks tall.

Front is -z, y is up. 74 units tall (the rays); Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import armour, fabric, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 74
SCALE, HITBOX = sized(35, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("the sun goddess: slender crimson-and-white armour with gold trim, a gold sun-ray crown, two huge gold sun "
        "discs of spreading rays on its back with yin-yang hearts and long red-and-gold claws beneath them")
BASE = {"red": (190, 30, 40), "red_dark": (110, 14, 20), "red_light": (240, 90, 90), "white": (246, 244, 240),
        "white_dark": (190, 186, 196), "gold": (232, 186, 60), "gold_dark": (160, 112, 30), "gold_light": (255, 236, 160),
        "black": (28, 26, 30), "skin": (246, 220, 200), "skin_dark": (210, 170, 150), "eye": (60, 140, 220)}
SHINY = {"red": (40, 60, 160), "red_dark": (16, 26, 90), "red_light": (100, 130, 230), "gold": (214, 218, 230),
         "gold_dark": (140, 146, 162), "gold_light": (250, 252, 255)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", light="red_light", trim="gold")
WHITE = armour(P, "white", "white_dark", trim="gold")
WHITE_PLAIN = armour(P, "white", "white_dark")
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
FACE = skin(P, "skin", dark="skin_dark", var=0.02)


def discf(x, y, z, face, variant, box=None, **k):
    """A sun disc: concentric gold rings, a yin-yang at the centre of its outer face."""
    p = P(variant)
    if face in ("north", "south"):
        u, v, W, H = local(x, y, z, face, box)
        du, dv = u - W / 2, v - H / 2
        r = math.hypot(du, dv)
        R = min(W, H) * 0.24
        if r < R:
            upper = dv > 0
            side = (math.hypot(du, dv - R / 2) < R / 2) or (not (math.hypot(du, dv + R / 2) < R / 2) and du < 0)
            dot = math.hypot(du, dv - R / 2) < R * 0.14 or math.hypot(du, dv + R / 2) < R * 0.14
            return tone(p["white"] if side != dot else p["black"], face), None
        if abs((r % 1.6) - 0.8) < 0.18:
            return tone(p["gold_dark"], face), None
    return GOLD(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("amaterasumon")
    mats = {"skin": WHITE_PLAIN, "chest": RED, "abs": WHITE_PLAIN, "pelvis": RED, "neck": WHITE_PLAIN,
            "deltoid": RED, "upper_arm": WHITE_PLAIN, "forearm": RED, "hand": WHITE_PLAIN, "finger": WHITE_PLAIN,
            "thigh": WHITE, "knee": GOLD, "shin": RED, "calf": RED, "foot": GOLD, "toe": GOLD}
    a = humanoid(m, mats, bulk=0.82, arm_bulk=0.8, leg_bulk=0.85, name="amaterasumon", hand_pose="open")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.2, 2.4, 54.5, 60.5, FACE, cut=1)
    for sx in (-1, 1):
        m.box(hd, sx * 0.9 - 0.5, 57.4, -2.5, sx * 0.9 + 0.5, 58.0, -2.3, solid(P, "eye"))
    m.box(hd, -2.6, 59.0, -2.8, 2.6, 61.6, 2.8, GOLD)                                    # gold helm band
    for i in range(9):                                           # sun-ray crown
        ang = math.radians(-60 + i * 15)
        rod(m, hd, (2.0 * math.sin(ang), 61.0, 0.4), (6.0 * math.sin(ang), 61.0 + 6.0 * math.cos(ang), 1.6), 1,
            GOLD, extend=0.2)
    shell(m, bd, (0, 0, 0.4), 4.4, 42.0, 50.5, -80, 80, 7, 1.0, RED)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        sh = a[nm]["shoulder"]
        dome(m, a[nm]["bone"], (sh[0] + sx * 0.8, 49.5, 0.2), 3.0, 2.8, RED, layers=3)
    sk = m.bone("skirt", bd, (0, 32, 0))
    for i in range(10):                                          # white skirt guard in plates
        ang = math.radians(-162 + i * 36)
        c = (4.6 * math.sin(ang), 32.0, -4.0 * math.cos(ang))
        m.box(sk, c[0] - 1.7, 22.0, c[2], c[0] + 1.7, 32.0, c[2] + 0.8, WHITE,
              rotation=(-10 * math.cos(ang), -math.degrees(ang), 0), pivot=c)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # the two sun discs and their rays
        wb = m.bone(nm, bd, (sx * 6.0, 46.0, 5.0))
        c = (sx * 16.0, 40.0, 7.0)
        rod(m, wb, (sx * 4.0, 46.0, 4.0), c, 3, GOLD, extend=0.3)
        m.round_box(wb, c[0], c[2] + 1.0, 8.0, 1.6, c[1] - 8.0, c[1] + 8.0, discf, cut=3)
        for i in range(13):                                      # ray pipes fanning up and out
            ang = math.radians(-70 + i * 11.5)
            ln = 18.0 + 12.0 * math.cos(math.radians(-70 + i * 11.5) * 1.2)
            b = (c[0] + 7.0 * math.sin(ang), c[1] + 7.0 * math.cos(ang), c[2] + 2.0)
            tip = (b[0] + ln * math.sin(ang) * 0.35 + sx * 2.0, b[1] + ln * math.cos(ang), b[2] + 1.0)
            rod(m, wb, b, tip, 2, GOLD, extend=0.2)
        for j in range(3):                                       # long claws hanging below each disc
            base = (c[0] + (j - 1) * 4.0, c[1] - 8.0, c[2])
            rod(m, wb, base, (base[0] + sx * 1.5, base[1] - 10.0, base[2] - 2.0), 2, GOLD, extend=0.3)
            spike(m, wb, (base[0] + sx * 1.5, base[1] - 10.0, base[2] - 2.0), (0, -1, -0.3), 1.6, 6.0,
                  solid(P, "red"), tip=0.8)
    return m
