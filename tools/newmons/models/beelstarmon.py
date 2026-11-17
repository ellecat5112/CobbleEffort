"""Beel Starmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a Demon Lord gunslinger, in her official outfit: a black leather bodysuit with straps and a
long tattered black coat, a blue star-marked helm-mask over long blond hair, two long-barrelled pistols and two
floating blue star-helmets (her Star-bits) circling her. 35 blocks tall.

Front is -z, y is up. 68 units tall; Ultimate stage. Official outfit only. make(x=True): Beel Starmon (X-Antibody)
(violet-black armour plates and two great wings of violet feathers; a long rifle).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import armour, cutout, feathers, leather, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 68
SCALE, HITBOX = sized(35, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a Demon Lord gunslinger in a black leather bodysuit and tattered coat, a blue star-marked helm-mask over long "
        "blond hair, two long pistols and two floating blue star-helmets")
BASE = {"black": (36, 34, 42), "black_light": (110, 108, 126), "blue": (40, 70, 170), "blue_dark": (16, 30, 90),
        "blue_light": (110, 150, 240), "hair": (246, 226, 150), "hair_dark": (200, 170, 90), "skin": (246, 224, 210),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "star": (220, 40, 40), "violet": (110, 70, 170),
        "violet_dark": (50, 24, 90), "eye": (255, 220, 60)}
SHINY = {"black": (230, 226, 236), "black_light": (255, 255, 255), "blue": (180, 40, 60), "blue_dark": (100, 14, 24),
         "blue_light": (250, 130, 140), "violet": (40, 150, 130), "violet_dark": (16, 80, 70)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    SUIT = leather(P, "black", "black_light", stitch="steel")
    BLUE = armour(P, "blue", "blue_dark", light="blue_light")
    STEEL = metal(P, "steel", dark="steel_dark")
    HAIR = strands(P, "hair", "hair_dark")

    def starhelm(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(xx, y, z, face, box)
        du, dv = u - W / 2, v - H / 2
        ang = math.atan2(dv, du)
        r = math.hypot(du, dv)
        if face in ("north", "south") and r < min(W, H) * 0.3 * (0.55 + 0.45 * abs(math.cos(2.5 * ang))):
            return tone(p["star"], face), None
        return BLUE(xx, y, z, face, variant, box=box, **k)

    def torn(xx, y, z, face, box):
        u, v, W, H = local(xx, y, z, face, box)
        return v / max(H, 1e-6) > 0.14 * abs(math.sin((box.lo[0] + u) * 2.2)) + 0.03

    def pistol(m, bone, h, d):
        rod(m, bone, (h[0], h[1] - 1.0, h[2]), (h[0], h[1] + 1.4, h[2] + 1.0), 1, SUIT, extend=0)
        rod(m, bone, (h[0], h[1] + 1.0, h[2]), (h[0] + d[0] * 12, h[1] + 1.0 + d[1] * 12, h[2] + d[2] * 12), 1,
            STEEL, extend=0, t2=2)

    def build():
        m = Model(name)
        ARM = armour(P, "violet", "violet_dark", light="black_light") if x else SUIT
        mats = {"skin": SUIT, "chest": ARM, "abs": SUIT, "pelvis": SUIT, "neck": SUIT, "deltoid": ARM,
                "upper_arm": SUIT, "forearm": ARM, "hand": SUIT, "finger": SUIT, "thigh": SUIT, "knee": ARM,
                "shin": SUIT, "calf": SUIT, "foot": SUIT, "toe": SUIT}
        a = humanoid(m, mats, bulk=0.8, arm_bulk=0.78, leg_bulk=0.9, name=name, hand_pose="fist", chest_depth=0.9)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, 0, 2.2, 2.4, 54.5, 60.5, solid(P, "skin"), cut=1)
        m.box(hd, -2.4, 56.6, -2.8, 2.4, 61.2, 2.6, BLUE)                                 # helm-mask
        m.box(hd, -1.8, 57.6, -3.0, 1.8, 58.4, -2.8, solid(P, "eye", glow=True))
        spike(m, hd, (0, 61.0, -1.0), (0, 1, 0.6), 1.6, 4.0, BLUE)
        hr = m.bone("mane", hd, (0, 59, 2))
        for i in range(11):                                      # long blond hair
            xx = -3.2 + i * 0.64
            rod(m, hr, (xx, 59.0, 1.6), (xx * 1.6, 26.0 - (i % 3) * 3, 6.0), 2, HAIR, extend=0.3)
        for sx in (-1, 1):                                       # straps
            rod(m, bd, (sx * 4.0, 50.0, -3.4), (-sx * 3.6, 34.0, -3.8), 1, leather(P, "black", "black_light"),
                extend=0.2, t2=1)
        cb = m.bone("cap", bd, (0, 51, 3))
        if x:                                                    # two great wings of violet feathers
            F = feathers(P, "violet", "violet_dark", size=(1.6, 3.2), flow=(0, -1))
            for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
                wb = m.bone(nm, bd, (sx * 3.0, 49.0, 3.0))
                for i in range(11):
                    t = i / 10
                    base = (sx * (3.0 + 14.0 * t), 49.0 + 18.0 * t, 3.0 + 5.0 * t)
                    ln = 14.0 + 18.0 * t
                    m.box(wb, base[0] - 1.9, base[1] - ln, base[2], base[0] + 1.9, base[1], base[2], F,
                          rotation=(-10, 0, -sx * (45 - 30 * t)), pivot=base)
        else:
            cape(m, cb, 52.0, 16.0, 46.0, cutout(torn, leather(P, "black", "black_light")), z=4.4, flare=1.0,
                 panels=8, sweep=(0, 8))
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            h = a[nm]["hand"]
            if x and sx < 0:
                rod(m, a[nm]["bone"], h, (h[0] + 2.0, h[1] + 4.0, h[2] - 24.0), 1, STEEL, extend=0, t2=2)   # rifle
            else:
                pistol(m, a[nm]["bone"], h, (sx * 0.2, 0.0, -1.0))
        for i, c in enumerate(((-12.0, 60.0, -2.0), (13.0, 22.0, -4.0))):   # Star-bits
            sb = m.bone(f"ring_star{i}", bd, c)
            m.round_box(sb, c[0], c[2], 2.8, 2.6, c[1] - 2.6, c[1] + 2.6, starhelm, cut=1)
            spike(m, sb, (c[0], c[1] + 2.4, c[2]), (0, 1, 0.6), 1.2, 2.4, BLUE)
        return m
    return build


build = make("beelstarmon")
