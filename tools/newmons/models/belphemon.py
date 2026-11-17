"""Belphemon (Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Demon Lord of Sloth.

make("sleep") = Belphemon: Sleep Mode: a huge dozing ball of dark shaggy fur with two curling ram horns, closed eyes, a
row of white fang-plates round its brow, little violet bat wings, wrapped in chains with a gold alarm clock at its
belly. make("rage") = Belphemon: Rage Mode: awake, a hulking dark muscled demon with ram horns, violet bat wings,
chains on its arms and claws blazing with green fire. make("x") = Belphemon (X-Antibody): gold armour over a black
body, magenta crystal spikes, pink bat wings, chains and horns.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digibody import dome, humanoid, shell
from _digidetail import (Bulge, armour, cutout, flame_inside, fur, gem, local, metal, plane, skin, solid,
                         torso_bulges)
from _route import pal, tone

BASE = {"fur": (80, 70, 70), "fur_dark": (36, 30, 30), "fur_light": (140, 130, 130), "horn": (180, 160, 120),
        "horn_dark": (110, 90, 60), "fang": (246, 244, 236), "violet": (130, 60, 160), "violet_dark": (70, 24, 90),
        "chain": (130, 132, 144), "chain_dark": (60, 62, 70), "gold": (236, 196, 70), "gold_dark": (160, 120, 30),
        "gold_light": (255, 240, 170), "skin": (90, 60, 50), "skin_dark": (40, 24, 20), "skin_light": (160, 120, 100),
        "flame": (130, 255, 100, 220), "flame_core": (230, 255, 200, 235), "pink": (240, 60, 170),
        "pink_light": (255, 180, 230), "black": (30, 26, 30), "red": (220, 30, 40), "eye": (255, 60, 60),
        "wing": (150, 60, 170, 235), "wing_x": (240, 80, 190, 235), "clock": (240, 240, 246)}
SHINY = {"fur": (200, 190, 170), "fur_dark": (140, 130, 110), "fur_light": (240, 236, 220), "violet": (60, 140, 200),
         "violet_dark": (20, 70, 130), "skin": (150, 150, 170), "skin_dark": (80, 80, 100), "flame": (255, 120, 80, 220),
         "gold": (200, 210, 230), "gold_dark": (130, 140, 160), "pink": (90, 220, 230), "wing": (60, 140, 200, 235),
         "wing_x": (90, 220, 230, 235)}


def P(v):
    return pal(BASE, SHINY, v)


CHAIN = metal(P, "chain", dark="chain_dark")
HORN = armour(P, "horn", "horn_dark", seams=(1.4,))


def chain(m, bone, a, b):
    n = max(1, round(math.dist(a, b) / 1.6))
    for j in range(n):
        c = tuple(aa + (bb - aa) * (j + 0.5) / n for aa, bb in zip(a, b))
        m.box(bone, c[0] - 0.6, c[1] - 0.6, c[2] - 0.6, c[0] + 0.6, c[1] + 0.6, c[2] + 0.6, CHAIN,
              rotation=(45 * (j % 2), 45, 0), pivot=c)


def ram_horn(m, bone, sx, base, size=1.0):
    pts = [base]
    for j in range(7):
        ang = j * 0.75
        r = 5.0 * size * (1 - j * 0.08)
        pts.append((base[0] + sx * (2.0 + r * (1 - math.cos(ang))) * size, base[1] + r * math.sin(ang) * 1.1,
                    base[2] + j * 0.8 * size))
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bone, p0, p1, max(1, round((3.4 - j * 0.35) * size)), HORN, extend=0.4)


def wingshader(key):
    return cutout(lambda *q: True, lambda x, y, z, f, variant=None, box=None, **k: (P(variant)[key], None))


def make(name, variant):
    def flamef(x, y, z, face, variant_=None, box=None, **k):
        p = P(k.get("variant", variant_))
        u, v, W, H = local(x, y, z, face, box)
        c = p["flame_core"] if v / max(H, 1e-6) < 0.35 else p["flame"]
        return c, c[:3]

    def build():
        m = Model(name)
        if variant == "sleep":
            top = m.bone(name, None, (0, 0, 0))
            bd = m.bone("body", top, (0, 24, 0))
            FUR = fur(P, "fur", "fur_dark", tip="fur_light", length=2.0)

            def facef(x, y, z, face, variant=None, box=None, **k):
                p = P(variant)
                if face == "north":
                    a, b = plane(x, y, z, face)
                    for sx in (-1, 1):
                        if abs(b - 28.0 + 0.15 * (a - sx * 5.0) ** 2) < 0.35 and abs(a - sx * 5.0) < 3.0:
                            return p["black"], None              # closed sleeping eyes
                    if abs(b - 24.0 - 0.3 * abs(a)) < 0.3 and abs(a) < 2.0:
                        return p["black"], None
                    if 32.0 < b < 37.0 and abs(a + (b - 34.0) * 0.4) < 0.3 + (b - 32.0) * 0.06 and abs(a) < 2.0:
                        return p["red"], None                    # the red scratch marks
                return FUR(x, y, z, face, variant, box=box, **k)
            ball(m, bd, (0, 24.0, 0), 16.0, facef, layers=9, ry=17.0)
            for i in range(10):                                  # white fang-plates round its brow
                ang = math.radians(-70 + i * 15.5)
                c = (14.0 * math.sin(ang), 34.0 + 3.0 * math.cos(ang), -14.0 * math.cos(ang) * 0.7)
                spike(m, bd, c, (math.sin(ang) * 0.3, -0.4, -1), 2.4, 3.0, solid(P, "fang"), tip=0.8)
            for sx in (-1, 1):
                ram_horn(m, bd, sx, (sx * 8.0, 38.0, -2.0), size=1.6)
                wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 14.0, 26.0, 4.0))
                bat_wing(m, wb, (sx * 14.0, 26.0, 4.0), 12.0, 10.0, 3, solid(P, "violet_dark"), wingshader("wing"),
                         side=sx)
            for j in range(5):                                   # chains wrapped round its lower half
                y = 6.0 + j * 2.6
                r = 15.0 - abs(j - 1) * 1.5
                pts = [(r * math.sin(math.radians(a_)), y + (a_ % 60) * 0.02, -r * math.cos(math.radians(a_)))
                       for a_ in range(-160, 181, 40)]
                for p0, p1 in zip(pts, pts[1:]):
                    chain(m, bd, p0, p1)
            m.round_box(bd, 0, -15.6, 3.4, 1.4, 6.0, 12.0, metal(P, "clock", dark="chain_dark"), cut=1)   # alarm clock
            for sx in (-1, 1):
                ball(m, bd, (sx * 2.6, 13.0, -15.6), 1.4, metal(P, "gold", dark="gold_dark"), layers=2)
            for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
                lg = m.bone(nm, top, (sx * 6.0, 6.0, 0))
                m.round_box(lg, sx * 6.0, -2.0, 4.0, 4.0, 0.0, 6.0, FUR, cut=1)
            return m
        x = variant == "x"
        BODY = skin(P, "black" if x else "skin", dark="skin_dark", light="skin_light",
                    bulges=torso_bulges(0, 51.0, 6.2, abs_rows=4), var=0.04)
        ARM = skin(P, "black" if x else "skin", dark="skin_dark", light="skin_light", var=0.04,
                   bulges=[Bulge("north", sx * 10.0, 42.0, 2.2, 4.0, light=0.35, shadow=0.45) for sx in (-1, 1)])
        GOLD = armour(P, "gold", "gold_dark", light="gold_light")
        mats = {"skin": ARM, "chest": GOLD if x else BODY, "abs": BODY, "pelvis": GOLD if x else BODY, "neck": ARM,
                "deltoid": GOLD if x else ARM, "upper_arm": ARM, "forearm": GOLD if x else ARM, "hand": ARM,
                "finger": ARM, "claw": gem(P, "pink", "pink_light") if x else solid(P, "fang"),
                "thigh": GOLD if x else ARM, "knee": GOLD if x else ARM, "shin": GOLD if x else ARM, "calf": ARM,
                "foot": ARM, "talon": gem(P, "pink", "pink_light") if x else solid(P, "fang")}
        a = humanoid(m, mats, bulk=1.4, arm_bulk=1.6, leg_bulk=1.5, digitigrade=True, claws=True, talons=True,
                     name=name, hand_pose="open")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 3.0, 3.0, 54.4, 61.0, GOLD if x else ARM, cut=1)
        m.box(hd, -2.4, 54.6, -4.6, 2.4, 57.0, -3.0, solid(P, "black"))
        for sx in (-1, 1):
            m.box(hd, sx * 1.4 - 0.6, 58.0, -3.7, sx * 1.4 + 0.6, 58.8, -3.5, solid(P, "eye", glow=True))
            ram_horn(m, hd, sx, (sx * 2.4, 60.0, 0.0), size=0.9)
        for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
            wb = m.bone(nm, bd, (sx * 4.0, 49.0, 4.0))
            bat_wing(m, wb, (sx * 4.0, 49.0, 4.0), 30.0, 20.0, 4, solid(P, "black"),
                     wingshader("wing_x" if x else "wing"), side=sx)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):      # chains on its arms
            el, wr = a[nm]["elbow"], a[nm]["wrist"]
            chain(m, a[nm]["bone"], el, (wr[0] + sx * 6.0, wr[1] - 10.0, wr[2] + 4.0))
        if x:                                                    # magenta crystal spikes
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
                sh = a[nm]["shoulder"]
                for j in range(4):
                    spike(m, a[nm]["bone"], (sh[0] + sx * 3.0, 51.0, -1.0 + j * 1.4), (sx * 0.7, 0.7, 0.2), 1.8,
                          7.0 - j, gem(P, "pink", "pink_light"), tip=0.6)
            m.box(bd, -2.0, 44.0, -7.2, 2.0, 48.0, -6.0, gem(P, "pink", "pink_light"))
        else:                                                    # green fire on its claws
            for nm in ("arm_left", "arm_right"):
                h = a[nm]["hand"]
                for ang in (0, 90):
                    m.box(a[nm]["bone"], h[0] - 4.0, h[1] - 8.0, h[2], h[0] + 4.0, h[1] + 4.0, h[2],
                          cutout(flame_inside(4, 0.0, 3), flamef), rotation=(0, ang, 0), pivot=h)
        return m
    return build
