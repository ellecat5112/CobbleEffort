"""Arkhai Angemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a principality angel. Orange-red plate armour over a long white robe, a gold crowned
helm with tall spikes, white wings spreading behind, a gold belt and an orange tabard, and a tall golden torch-staff
burning with flame, wound with a green ribbon. 25 blocks tall.

Front is -z, y is up. 72 units tall (the torch); Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import armour, cutout, fabric, feathers, flame_inside, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 72
SCALE, HITBOX = sized(25, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a principality angel: orange-red plate armour over a long white robe, a gold crowned helm, white wings and a "
        "golden torch-staff wound with a green ribbon")
BASE = {"orange": (226, 90, 40), "orange_dark": (140, 40, 16), "orange_light": (250, 160, 100), "white": (250, 250, 252),
        "white_dark": (196, 200, 216), "gold": (236, 196, 70), "gold_dark": (160, 120, 30), "gold_light": (255, 240, 170),
        "green": (60, 170, 110), "green_dark": (20, 100, 60), "flame": (255, 150, 40, 220),
        "flame_core": (255, 230, 120, 235), "hair": (250, 220, 120), "hair_dark": (200, 150, 60)}
SHINY = {"orange": (60, 110, 200), "orange_dark": (24, 50, 130), "orange_light": (130, 180, 250),
         "flame": (90, 180, 255, 220), "flame_core": (200, 240, 255, 235)}


def P(v):
    return pal(BASE, SHINY, v)


ORANGE = armour(P, "orange", "orange_dark", light="orange_light", trim="gold")
ROBE = fabric(P, "white", "white_dark", axis="y", period=2.8)
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
WING = feathers(P, "white", "white_dark", size=(1.4, 3.0), flow=(0, -1))


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["flame_core"] if v / max(H, 1e-6) < 0.35 else p["flame"]
    return c, c[:3]


def build():
    m = Model("arkhaiangemon")
    mats = {"skin": ROBE, "chest": ORANGE, "abs": ORANGE, "pelvis": ORANGE, "neck": ROBE, "deltoid": ORANGE,
            "upper_arm": ROBE, "forearm": ORANGE, "hand": ROBE, "finger": ROBE, "thigh": ROBE, "knee": ROBE,
            "shin": ROBE, "calf": ROBE, "foot": GOLD, "toe": GOLD}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.0, leg_bulk=1.0, name="arkhaiangemon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.4, 2.6, 54.6, 60.8, ORANGE, cut=1)
    m.box(hd, -2.6, 58.6, -2.9, 2.6, 60.2, 2.9, GOLD)                                    # gold crown band
    for i in range(7):                                           # tall crown spikes
        ang = math.radians(-60 + i * 20)
        spike(m, hd, (2.4 * math.sin(ang), 60.0, -2.4 * math.cos(ang) * 0.6), (0, 1, 0), 1.0, 3.0 + (i % 2) * 2,
              GOLD)
    for i in range(6):
        x = -2.0 + i * 0.8
        rod(m, hd, (x, 58.0, 2.0), (x * 1.2, 48.0, 4.0), 2, strands(P, "hair", "hair_dark"), extend=0.3)
    shell(m, bd, (0, 0, 0.6), 5.0, 42.0, 51.0, -85, 85, 9, 1.2, ORANGE)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        sh = a[nm]["shoulder"]
        dome(m, a[nm]["bone"], (sh[0] + sx * 1.2, 50.0, 0.3), 3.8, 3.4, ORANGE, layers=3)
    m.box(bd, -4.8, 31.0, -4.2, 4.8, 33.4, 4.0, GOLD)                                    # gold belt
    m.box(bd, -2.4, 10.0, -4.6, 2.4, 31.0, -4.0, ORANGE)                                  # tabard
    sk = m.bone("skirt", bd, (0, 32, 0))
    for i in range(10):                                          # the long white robe sweeping back
        ang = math.radians(-162 + i * 36)
        back = 0.5 + 0.5 * math.cos(ang)
        c = (4.6 * math.sin(ang), 32.0, -4.0 * math.cos(ang))
        m.box(sk, c[0] - 1.8, 0.0, c[2], c[0] + 1.8, 32.0, c[2] + 0.8, ROBE,
              rotation=(-12 * math.cos(ang) - 10 * back, -math.degrees(ang), 0), pivot=c)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # white wings
        wb = m.bone(nm, bd, (sx * 3.0, 49.0, 3.0))
        rod(m, wb, (sx * 3.0, 49.0, 3.0), (sx * 16.0, 64.0, 7.0), 2, WING, extend=0.3)
        for i in range(11):
            t = i / 10
            base = (sx * (3.0 + 13.0 * t), 49.0 + 15.0 * t, 3.0 + 4.0 * t)
            ln = 10.0 + 16.0 * t
            m.box(wb, base[0] - 1.8, base[1] - ln, base[2], base[0] + 1.8, base[1], base[2], WING,
                  rotation=(-10, 0, -sx * (50 - 35 * t)), pivot=base)
    ar = a["arm_right"]                                          # the torch-staff
    h = ar["hand"]
    st = m.bone("staff", ar["bone"], h)
    rod(m, st, (h[0], h[1] - 26.0, h[2]), (h[0], h[1] + 40.0, h[2]), 1, GOLD, extend=0)
    for i in range(3):
        m.round_box(st, h[0], h[2], 1.2 + i * 0.6, 1.2 + i * 0.6, h[1] + 38.0 + i * 1.2, h[1] + 39.2 + i * 1.2, GOLD,
                    cut=1)
    for ang in (0, 60, 120):
        m.box(st, h[0] - 3.0, h[1] + 41.0, h[2], h[0] + 3.0, h[1] + 50.0, h[2], cutout(flame_inside(3, 0.2, 5), flamef),
              rotation=(0, ang, 0), pivot=(h[0], h[1] + 41.0, h[2]))
    for i in range(10):                                          # the green ribbon wound round it
        t = i / 9
        ang = t * 6.0
        p0 = (h[0] + 2.0 * math.cos(ang), h[1] + 36.0 - 50.0 * t, h[2] + 2.0 * math.sin(ang))
        p1 = (h[0] + 2.0 * math.cos(ang + 0.6), h[1] + 36.0 - 50.0 * (t + 0.11), h[2] + 2.0 * math.sin(ang + 0.6))
        rod(m, st, p0, p1, 1, fabric(P, "green", "green_dark"), extend=0.2, t2=2)
    return m
