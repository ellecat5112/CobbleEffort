"""Armamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a living arsenal. Steel-blue armour bristling with blades on every surface: blade fins on its
helm and shoulders, spikes down its arms and legs, two long swords held crossed and great bladed wings of steel
behind it. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage. make(burst=True): Armamon: Burst Mode (bronze-gold armour, a
crimson cape, flames behind and a ring of floating swords).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, dome, humanoid, shell
from _digidetail import armour, cutout, fabric, flame_inside, local, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a living arsenal in steel-blue armour bristling with blades, holding two long swords crossed, with great "
        "bladed steel wings")
BASE = {"armour": (70, 100, 150), "armour_dark": (24, 36, 70), "armour_light": (150, 190, 240), "blade": (210, 220, 236),
        "blade_dark": (110, 120, 140), "accent": (180, 60, 220), "eye": (90, 240, 160), "cape": (110, 20, 30),
        "cape_dark": (50, 6, 12), "flame": (255, 180, 50, 220), "flame_core": (255, 240, 150, 235)}
SHINY = {"armour": (40, 40, 48), "armour_dark": (14, 14, 18), "armour_light": (110, 110, 130), "accent": (240, 200, 60),
         "eye": (255, 80, 80)}
BURST = {"armour": (170, 130, 60), "armour_dark": (90, 60, 20), "armour_light": (240, 210, 130), "accent": (200, 40, 40)}
BURST_SHINY = {"armour": (180, 180, 196), "armour_dark": (100, 100, 116), "armour_light": (250, 250, 255),
               "cape": (30, 40, 110), "cape_dark": (10, 14, 50), "flame": (90, 180, 255, 220),
               "flame_core": (200, 240, 255, 235)}


def make(name, burst=False):
    B = dict(BASE, **(BURST if burst else {}))
    S = BURST_SHINY if burst else SHINY

    def P(v):
        return pal(B, S, v)

    ARM = armour(P, "armour", "armour_dark", light="armour_light", trim="accent", trim_w=0.35)
    ARM_PLAIN = armour(P, "armour", "armour_dark", light="armour_light")
    BLADE = metal(P, "blade", dark="blade_dark", light="armour_light")
    CAPE = fabric(P, "cape", "cape_dark", axis="y", period=3.0)

    def flamef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p["flame_core"] if v / max(H, 1e-6) < 0.35 else p["flame"]
        return c, c[:3]

    def sword(m, bone, hilt, d, length):
        n = math.sqrt(sum(q * q for q in d))
        u = tuple(q / n for q in d)
        tip = tuple(h + q * length for h, q in zip(hilt, u))
        guard = tuple(h + q * 1.0 for h, q in zip(hilt, u))
        rod(m, bone, tuple(h - q * 3.0 for h, q in zip(hilt, u)), hilt, 1, ARM_PLAIN, extend=0)
        rod(m, bone, guard, tip, 1, BLADE, extend=0, t2=2)
        spike(m, bone, tip, u, 1.0, 2.0, BLADE)

    def build():
        m = Model(name)
        mats = {"skin": ARM_PLAIN, "chest": ARM, "abs": ARM_PLAIN, "pelvis": ARM, "neck": ARM_PLAIN, "deltoid": ARM,
                "upper_arm": ARM_PLAIN, "forearm": ARM, "hand": ARM_PLAIN, "finger": ARM_PLAIN, "thigh": ARM,
                "knee": BLADE, "shin": ARM, "calf": ARM_PLAIN, "foot": ARM, "toe": BLADE, "talon": BLADE}
        a = humanoid(m, mats, bulk=1.1, arm_bulk=1.15, leg_bulk=1.15, name=name, hand_pose="fist", talons=True)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.6, 60.6, ARM, cut=1)
        m.box(hd, -1.8, 57.4, -3.3, 1.8, 58.2, -2.9, solid(P, "eye", glow=True))
        for i in range(5):                                       # blade fins on the helm
            ang = math.radians(-50 + i * 25)
            spike(m, hd, (2.0 * math.sin(ang), 60.0, 0.5), (math.sin(ang), 1, 0.6), 1.0, 5.0 + (i % 2) * 2, BLADE)
        shell(m, bd, (0, 0, 0.6), 5.6, 42.0, 51.0, -85, 85, 9, 1.2, ARM)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab, sh = a[nm]["bone"], a[nm]["shoulder"]
            dome(m, ab, (sh[0] + sx * 1.6, 50.0, 0.3), 4.4, 4.0, ARM, layers=3)
            for j in range(3):
                spike(m, ab, (sh[0] + sx * 3.4, 52.0, -1.6 + j * 1.6), (sx, 0.5, 0.2), 1.0, 5.0, BLADE)
            el, wr = a[nm]["elbow"], a[nm]["wrist"]
            for j in range(3):                                   # spikes down the forearm
                p = tuple(e + (w - e) * (j + 0.5) / 3 for e, w in zip(el, wr))
                spike(m, ab, p, (sx, 0.2, 0.3), 1.0, 3.0, BLADE)
            h = a[nm]["hand"]
            sword(m, ab, h, (-sx * 0.6, 0.5 if sx > 0 else -0.6, -1), 30.0)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg, kn = a[nm]["bone"], a[nm]["knee"]
            spike(m, lg, (kn[0], 18.5, kn[2] - 2.6), (0, 0.4, -1), 1.6, 3.6, BLADE)
            for j in range(3):
                spike(m, lg, (kn[0] + sx * 2.0, 6.0 + j * 4.0, 0.0), (sx, 0.2, 0.2), 1.0, 2.6, BLADE)
        for sx, nm in ((1, "wing_left"), (-1, "wing_right")):    # bladed wings
            wb = m.bone(nm, bd, (sx * 3.0, 49.0, 3.0))
            for i in range(6):
                ang = math.radians(10 + i * 14)
                ln = 22.0 - i * 1.4
                base = (sx * 3.0, 49.0, 3.0 + i * 0.4)
                tip = (sx * (3.0 + ln * math.cos(ang)), 49.0 + ln * math.sin(ang), 6.0 + i)
                rod(m, wb, base, tip, 2, BLADE, extend=0.3, t2=1)
        if burst:
            cb = m.bone("cap", bd, (0, 51, 4))
            cape(m, cb, 52.0, 18.0, 48.0, CAPE, z=5.0, flare=0.8, panels=8, sweep=(0, 4))
            for i in range(8):                                   # the ring of floating swords
                ang = math.radians(i * 45)
                c = (20.0 * math.cos(ang), 44.0 + 18.0 * math.sin(ang), 8.0)
                sword(m, bd, (c[0], c[1] + 8.0, c[2]), (0, -1, 0), 14.0)
            for j, ang in enumerate((-30, 0, 30)):
                m.box(bd, -14.0, 40.0, 7.0 + j, 14.0, 70.0, 7.0 + j, cutout(flame_inside(6, 0.1, j), flamef),
                      rotation=(0, 0, ang), pivot=(0, 52.0, 7.0 + j))
        return m
    return build, P


build, P = make("armamon")
