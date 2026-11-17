"""Barbamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Demon Lord of Greed. An old sorcerer hidden in a dark robe under a great mantle patterned with
red-and-black sawtooth bands and studded with gold-ringed red jewels, a bird-skull mask with a long white beard
spilling to its feet, small red bat wings, steel claws and a long staff topped with a caged red orb. 35 blocks tall.

Front is -z, y is up. 68 units tall; Ultimate stage. make(x=True): Barbamon (X-Antibody) (a crimson-and-violet robe
with a gold front band, a halo of crimson light rays behind it and a glowing seal floating over its head).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digibody import humanoid, shell
from _digidetail import armour, cutout, fabric, gem, local, metal, plane, solid, strands
from _route import pal, tone

HEIGHT = 68
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "floater"
K = 3
LOOK = ("the Demon Lord of Greed: an old sorcerer in a dark robe under a sawtooth-patterned mantle with red jewels, a "
        "bird-skull mask with a long white beard, red bat wings, steel claws and a staff with a caged red orb")
BASE = {"robe": (50, 50, 90), "robe_dark": (20, 20, 44), "red": (200, 40, 40), "red_dark": (110, 14, 20),
        "black": (30, 28, 34), "gold": (230, 186, 60), "gold_dark": (150, 110, 30), "beard": (236, 236, 240),
        "beard_dark": (170, 170, 186), "skull": (240, 236, 220), "skull_dark": (170, 160, 140), "steel": (200, 204, 216),
        "steel_dark": (100, 104, 116), "jewel": (220, 30, 40), "jewel_light": (255, 160, 160), "green": (90, 120, 70),
        "violet": (110, 60, 150), "violet_dark": (50, 24, 80), "ray": (255, 60, 120, 170), "seal": (255, 80, 200)}
SHINY = {"robe": (90, 40, 40), "robe_dark": (40, 14, 14), "red": (60, 140, 220), "red_dark": (20, 70, 140),
         "jewel": (60, 200, 120), "jewel_light": (190, 255, 210), "ray": (90, 200, 255, 170), "seal": (90, 220, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    ROBE = fabric(P, "violet" if x else "robe", "violet_dark" if x else "robe_dark", axis="y", period=2.8)
    BEARD = strands(P, "beard", "beard_dark")
    STEEL = metal(P, "steel", dark="steel_dark")
    GOLD = metal(P, "gold", dark="gold_dark")
    JEWEL = gem(P, "jewel", "jewel_light")

    def mantlef(xx, y, z, face, variant, box=None, **k):
        """The mantle: red-and-black sawtooth bands, gold edging."""
        p = P(variant)
        u, v, W, H = local(xx, y, z, face, box)
        if min(u, W - u) < 0.4:
            return tone(p["gold"], face), None
        if x:
            return ROBE(xx, y, z, face, variant, box=box, **k)
        zig = abs(((u * 0.7) % 2.0) - 1.0)
        band = (v * 0.45) % 2.0
        return tone(p["red"] if band < zig + 0.2 else p["black"], face), None

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 30, 0))
        for i in range(12):                                      # the long robe
            ang = math.radians(-165 + i * 30)
            c = (4.6 * math.sin(ang), 46.0, -4.0 * math.cos(ang))
            m.box(bd, c[0] - 1.6, 4.0, c[2], c[0] + 1.6, 46.0, c[2] + 0.8, ROBE,
                  rotation=(-6 * math.cos(ang), -math.degrees(ang), -4 * math.sin(ang)), pivot=c)
        m.round_box(bd, 0, 0, 4.4, 3.6, 30.0, 50.0, ROBE, cut=1)
        for i in range(14):                                      # the great patterned mantle
            ang = math.radians(-170 + i * (340 / 13))
            c = (6.4 * math.sin(ang), 50.0, -5.6 * math.cos(ang))
            m.box(bd, c[0] - 2.2, 30.0, c[2], c[0] + 2.2, 51.0, c[2] + 0.8, mantlef,
                  rotation=(-20 * math.cos(ang), -math.degrees(ang), -14 * math.sin(ang)), pivot=c)
        for i in range(6):                                       # gold-ringed jewels on the mantle front
            sx = -1 if i % 2 else 1
            c = (sx * (2.4 + (i // 2) * 2.2), 47.0 - (i // 2) * 1.6, -6.4)
            ball(m, bd, c, 1.0, JEWEL, layers=2)
        hd = m.bone("head", bd, (0, 52, -1))
        m.round_box(hd, 0, -1.0, 2.4, 2.6, 51.0, 57.0, armour(P, "skull", "skull_dark"), cut=1)
        rod(m, hd, (0, 55.0, -3.4), (0, 52.0, -8.0), 2, armour(P, "skull", "skull_dark"), extend=0.3)   # beak
        m.round_box(hd, 0, -0.4, 3.2, 3.2, 56.0, 59.0, ROBE, cut=1)                    # hood
        for sx in (-1, 1):
            m.box(hd, sx * 1.0 - 0.4, 54.6, -3.7, sx * 1.0 + 0.4, 55.4, -3.5, solid(P, "jewel", glow=True))
        bb = m.bone("mane", hd, (0, 51, -3))
        for i in range(9):                                       # the long white beard
            xx = -2.4 + i * 0.6
            rod(m, bb, (xx, 52.0, -3.6), (xx * 1.6, 10.0 + (i % 3) * 3, -5.0 - (i % 2)), 2, BEARD, extend=0.3)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):     # sleeves and steel claws
            ab = m.bone(nm, bd, (sx * 6.0, 47.0, 0))
            h = (sx * 13.0, 40.0, -4.0)
            rod(m, ab, (sx * 6.0, 47.0, 0), h, 4, ROBE, extend=0.5)
            for f in range(4):
                spike(m, ab, h, (sx * 0.6, 0.2 * (f - 1.5), -0.8 + f * 0.3), 0.8, 3.6, STEEL, tip=0.4)
        for sx, nm in ((1, "wing_left"), (-1, "wing_right")):    # small red bat wings
            wb = m.bone(nm, bd, (sx * 3.0, 50.0, 4.0))
            bat_wing(m, wb, (sx * 3.0, 50.0, 4.0), 16.0, 10.0, 4, solid(P, "red_dark"),
                     cutout(lambda *q: True, lambda xx, y, z, f, variant=None, box=None, **k: (P(variant)["red"], None)),
                     side=sx)
        st = m.bone("staff", "arm_right", (-13.0, 40.0, -4.0))   # the staff with a caged red orb
        rod(m, st, (-13.0, 4.0, -4.0), (-13.0, 64.0, -4.0), 1, GOLD, extend=0)
        ball(m, st, (-13.0, 66.0, -4.0), 1.8, JEWEL, layers=3)
        for j in range(4):
            ang = math.radians(j * 90)
            rod(m, st, (-13.0, 63.0, -4.0), (-13.0 + 2.4 * math.cos(ang), 68.0, -4.0 + 2.4 * math.sin(ang)), 1,
                STEEL, extend=0.1)
        if x:                                                    # crimson light rays and a glowing seal
            m.box(bd, -2.4, 30.0, -6.6, 2.4, 50.0, -5.8, GOLD)                            # gold front band
            ray = m.bone("cap", bd, (0, 48, 6))
            for j in range(8):
                ang = math.radians(j * 45 + 22)
                c = (0.0, 48.0, 7.0)
                m.box(ray, -1.4, 48.0, 7.0, 1.4, 70.0, 7.0,
                      lambda xx, y, z, face, variant=None, box=None, **k: (P(variant)["ray"], P(variant)["ray"][:3]),
                      rotation=(0, 0, math.degrees(ang)), pivot=c)
            sl = m.bone("ring_seal", hd, (0, 64, -2))
            for j in range(10):
                ang = math.radians(j * 36)
                c = (3.4 * math.cos(ang), 64.0 + 3.4 * math.sin(ang), -2.0)
                m.box(sl, c[0] - 0.6, c[1] - 0.6, c[2] - 0.2, c[0] + 0.6, c[1] + 0.6, c[2] + 0.2,
                      solid(P, "seal", glow=True))
        return m
    return build


build = make("barbamon")
