"""Ancient Mermaimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the ancient warrior of water, a mermaid in a blue scaled bodysuit. A fish-crest helm
with fin ears, long silver hair, blue gauntlets, a fish tail of teal scales ending in a broad blue fluke, finned
arms and a long gold trident. 35 blocks tall.

Front is -z, y is up. 72 units tall (the trident); Ultimate stage. Official outfit only.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, cutout, local, metal, scales, skin, solid, strands
from _route import pal, tone

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 1.6)
KIND = "floater"
K = 3
LOOK = ("a mermaid warrior in a blue scaled bodysuit: a fish-crest helm, long silver hair, blue gauntlets, a teal "
        "scaled fish tail with a broad fluke and a long gold trident")
BASE = {"blue": (60, 110, 200), "blue_dark": (24, 50, 120), "blue_light": (130, 180, 250), "teal": (60, 170, 170),
        "teal_dark": (20, 90, 100), "hair": (220, 224, 236), "hair_dark": (150, 156, 180), "gold": (236, 190, 60),
        "gold_dark": (160, 112, 26), "gold_light": (255, 240, 170), "skin": (240, 214, 200), "skin_dark": (200, 160, 150),
        "fin": (90, 140, 230, 220), "fin_dark": (40, 70, 160, 230), "eye": (40, 200, 255)}
SHINY = {"blue": (180, 50, 90), "blue_dark": (100, 20, 50), "blue_light": (240, 120, 160), "teal": (230, 150, 70),
         "teal_dark": (150, 80, 30), "fin": (230, 90, 130, 220), "fin_dark": (150, 30, 70, 230)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT = scales(P, "blue", "blue_dark", size=1.2, light="blue_light", rim_mix=0.5)
TAIL = scales(P, "teal", "teal_dark", size=1.6, rim_mix=0.6)
HAIR = strands(P, "hair", "hair_dark")
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
ARMOUR = armour(P, "blue", "blue_dark", light="blue_light", trim="gold")


def finf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if (u * 1.2) % 2.0 < 0.3:
        return p["fin_dark"], None
    return p["fin"], None


def fin_shape(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    t = u / max(W, 1e-6)
    return v / max(H, 1e-6) < 1 - abs(((t * 4) % 1) - 0.5) * 0.6


def build():
    m = Model("ancientmermaimon")
    mats = {"skin": SUIT, "chest": ARMOUR, "abs": SUIT, "pelvis": SUIT, "neck": skin(P, "skin", dark="skin_dark"),
            "deltoid": ARMOUR, "upper_arm": SUIT, "forearm": ARMOUR, "hand": SUIT, "finger": SUIT, "thigh": TAIL,
            "knee": TAIL, "shin": TAIL, "calf": TAIL, "foot": TAIL, "toe": TAIL}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.78, leg_bulk=0.9, name="ancientmermaimon", hand_pose="open",
                 chest_depth=0.9)
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.2, 2.4, 54.5, 60.5, ARMOUR, cut=1)
    m.box(hd, -1.8, 56.6, -2.7, 1.8, 57.8, -2.3, solid(P, "eye", glow=True))
    for i in range(5):                                           # spiny fish crest
        spike(m, hd, (0, 60.0 - i * 0.8, -1.0 + i * 1.2), (0, 1, 0.4), 1.2, 3.6 - i * 0.4, ARMOUR)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.2, sx * 5.2), 56.0, -1.0, max(sx * 2.2, sx * 5.2), 61.0, -1.0, cutout(fin_shape, finf),
              rotation=(0, sx * 30, 0), pivot=(sx * 2.2, 58.0, -1.0))
    hr = m.bone("mane", hd, (0, 59, 2))
    for i in range(9):                                           # long silver hair down its back
        x = -3.2 + i * 0.8
        rod(m, hr, (x, 59.0, 1.5), (x * 1.6, 34.0 - (i % 3) * 3, 6.0 + (i % 2)), 2, HAIR, extend=0.3)
    tl = m.bone("tail", bd, (0, 30, 0))                          # one fish tail wrapping both legs, then the fluke
    for i in range(9):
        y0 = 30.0 - i * 3.2
        r = 4.6 - i * 0.38
        m.round_box(tl, 0, -0.4 + i * 0.25, r, r * 0.8, y0 - 3.4, y0, TAIL, cut=max(1, round(r * 0.3)))
    for sx in (-1, 1):
        m.box(tl, min(0, sx * 9.0), 0.0, 2.8, max(0, sx * 9.0), 9.0, 2.8, cutout(fin_shape, finf), rotation=(-30, 0, sx * 35),
              pivot=(0, 2.0, 2.8))
    for nm in ("arm_left", "arm_right"):                         # arm fins
        el = a[nm]["elbow"]
        sx = 1 if nm == "arm_left" else -1
        m.box(a[nm]["bone"], min(el[0], el[0] + sx * 4.0), el[1] - 6.0, el[2] + 1.0, max(el[0], el[0] + sx * 4.0),
              el[1] + 1.0, el[2] + 1.0,
              cutout(fin_shape, finf), rotation=(0, sx * 70, 0), pivot=el)
    ar = a["arm_right"]                                          # the gold trident
    h = ar["hand"]
    tr = m.bone("staff", ar["bone"], h)
    rod(m, tr, (h[0], h[1] - 22.0, h[2]), (h[0], h[1] + 40.0, h[2]), 1, GOLD, extend=0)
    for dx in (-2.0, 0.0, 2.0):
        rod(m, tr, (h[0], h[1] + 38.0, h[2]), (h[0] + dx, h[1] + 44.0, h[2]), 1, GOLD, extend=0.3)
        spike(m, tr, (h[0] + dx, h[1] + 44.0, h[2]), (0, 1, 0), 1.0, 2.0, GOLD)
    return m
