"""Apollomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Olympus god of the sun, a lion-warrior wrapped in fire. Crimson-and-orange armour with gold
claws and talons, a lion's face inside a wild mane of golden flame, a glowing sun orb held in a gold frame above its
back, flames streaming from its arms and a great sweeping tail of fire. 35 blocks tall.

Front is -z, y is up. 76 units tall (the sun frame); Ultimate stage.
make(variant): "whispered" = Apollomon: Whispered (blue flames, blue-and-teal armour); "darkness" = Apollomon
Darkness Mode (black-and-gold armour, no flames, a huge black battle-axe).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import dome, humanoid, shell
from _digidetail import armour, cutout, flame_inside, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 76
SCALE, HITBOX = sized(35, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("the sun god: crimson-and-orange armour, a lion's face in a mane of golden flame, a glowing sun orb in a gold "
        "frame above its back, flames streaming from its arms and a great tail of fire")
BASE = {"red": (200, 50, 30), "red_dark": (120, 20, 10), "red_light": (250, 130, 80), "orange": (240, 140, 40),
        "gold": (240, 196, 60), "gold_dark": (170, 120, 30), "gold_light": (255, 240, 170), "white": (246, 244, 236),
        "white_dark": (190, 186, 180), "face": (230, 170, 110), "eye": (255, 240, 120),
        "flame": (255, 170, 40, 220), "flame_core": (255, 240, 150, 235), "orb": (255, 220, 120),
        "mane": (255, 200, 60), "mane_dark": (240, 120, 30)}
SHINY = {"red": (60, 60, 70), "red_dark": (24, 24, 30), "red_light": (130, 130, 150), "flame": (255, 90, 160, 220),
         "flame_core": (255, 200, 230, 235), "mane": (255, 140, 200), "mane_dark": (220, 60, 140), "orb": (255, 180, 220)}
WHISPER = {"red": (40, 90, 170), "red_dark": (16, 40, 100), "red_light": (110, 170, 240), "orange": (60, 180, 200),
           "flame": (80, 190, 255, 220), "flame_core": (200, 245, 255, 235), "mane": (90, 170, 255),
           "mane_dark": (40, 90, 210), "orb": (160, 230, 255), "face": (120, 140, 200)}
WHISPER_SHINY = {"red": (110, 40, 150), "red_dark": (60, 16, 90), "red_light": (190, 120, 230),
                 "flame": (190, 110, 255, 220), "flame_core": (240, 210, 255, 235), "mane": (190, 120, 255),
                 "mane_dark": (120, 60, 210), "orb": (230, 200, 255)}
DARK = {"red": (36, 36, 44), "red_dark": (12, 12, 16), "red_light": (100, 100, 120), "orange": (60, 60, 70),
        "mane": (40, 40, 50), "mane_dark": (20, 20, 26), "face": (60, 56, 70), "eye": (255, 60, 40)}
DARK_SHINY = {"red": (220, 220, 230), "red_dark": (150, 150, 166), "red_light": (255, 255, 255),
              "gold": (200, 60, 60), "gold_dark": (130, 20, 20), "gold_light": (250, 140, 140)}


def make(name, variant=None):
    base, shiny = {None: ({}, SHINY), "whispered": (WHISPER, WHISPER_SHINY), "darkness": (DARK, DARK_SHINY)}[variant]
    B = dict(BASE, **base)

    def P(v):
        return pal(B, dict(B, **shiny), v) if v == "shiny" else pal(B, {}, v)

    RED = armour(P, "red", "red_dark", light="red_light", trim="gold")
    RED_PLAIN = armour(P, "red", "red_dark", light="red_light")
    GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
    MANE = strands(P, "mane", "mane_dark", tip="gold_light")
    fire = variant != "darkness"

    def flamef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p["flame_core"] if v / max(H, 1e-6) < 0.35 else p["flame"]
        return c, c[:3]

    def facef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and abs(y - 58.0) < 0.4 and 0.6 < abs(x) < 1.8:
            return p["eye"], p["eye"]
        return solid(P, "face")(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": RED_PLAIN, "chest": RED, "abs": RED_PLAIN, "pelvis": RED, "neck": RED_PLAIN, "deltoid": RED,
                "upper_arm": RED_PLAIN, "forearm": RED, "hand": RED_PLAIN, "finger": GOLD, "claw": GOLD,
                "thigh": RED, "knee": GOLD, "shin": RED, "calf": RED_PLAIN, "foot": solid(P, "white"), "talon": GOLD}
        a = humanoid(m, mats, bulk=1.15, arm_bulk=1.25, leg_bulk=1.25, digitigrade=True, claws=True, talons=True,
                     name=name, hand_pose="open")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 2.6, 2.8, 54.6, 60.6, facef, cut=1)
        m.box(hd, -1.6, 54.8, -5.2, 1.6, 57.4, -2.6, solid(P, "face"))                   # lion muzzle
        mane = m.bone("mane", hd, (0, 58, 1))
        for i in range(18):                                      # the mane (of flame, or dark spikes)
            ang = math.radians(i * 20)
            base = (3.0 * math.cos(ang), 58.0 + 3.0 * math.sin(ang), 0.5)
            tip = (base[0] * 3.2, base[1] + 6.0 * math.sin(ang) + 2.0, 4.0 + (i % 3))
            rod(m, mane, base, tip, 2, MANE, extend=0.3, t2=2)
        shell(m, bd, (0, 0, 0.6), 5.6, 42.0, 51.0, -85, 85, 9, 1.2, RED)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab, sh = a[nm]["bone"], a[nm]["shoulder"]
            dome(m, ab, (sh[0] + sx * 1.6, 50.0, 0.3), 4.6, 4.2, RED, layers=4)
            for j in range(3):
                spike(m, ab, (sh[0] + sx * 3.4, 51.0, -1.6 + j * 1.6), (sx * 0.7, 0.6, 0), 1.6, 4.0, GOLD, tip=0.6)
            wr = a[nm]["wrist"]
            shell(m, ab, (wr[0], 0, wr[2]), 2.4, 29.0, 36.0, -180, 180, 6, 1.0, GOLD)
            if fire:
                x0, x1 = sorted((wr[0], wr[0] + sx * 12.0))
                m.box(ab, x0, 26.0, wr[2] - 4.0, x1, 46.0, wr[2] - 4.0, cutout(flame_inside(4, sx * 0.3, 2), flamef))
        sb = m.bone("cap", bd, (0, 50, 4))                       # the sun frame above its back
        m.box(sb, -0.8, 48.0, 4.0, 0.8, 66.0, 5.6, GOLD)
        for sx in (-1, 1):
            rod(m, sb, (0, 64.0, 5.0), (sx * 7.0, 72.0, 5.0), 2, GOLD, extend=0.3)
            rod(m, sb, (sx * 7.0, 72.0, 5.0), (sx * 4.0, 76.0, 5.0), 2, GOLD, extend=0.3)
            rod(m, sb, (0, 64.0, 5.0), (sx * 7.0, 60.0, 5.0), 2, GOLD, extend=0.3)
        ball(m, sb, (0, 69.0, 5.0), 3.4, solid(P, "orb", glow=fire), layers=4)
        tl = m.bone("tail", bd, (0, 31, 4))
        if fire:                                                 # tail of fire sweeping round
            for j, ang in enumerate((0, 50, 100)):
                m.box(tl, -7.0, 2.0, 6.0, 7.0, 34.0, 6.0, cutout(flame_inside(5, 0.3, j + 4), flamef),
                      rotation=(30, 30 + ang * 0.3, 0), pivot=(0, 31, 6))
        else:                                                    # Darkness Mode: the great black axe
            ar = a["arm_right"]
            h = ar["hand"]
            ax = m.bone("axe", ar["bone"], h)
            rod(m, ax, (h[0], h[1] - 20.0, h[2]), (h[0], h[1] + 30.0, h[2]), 2, GOLD, extend=0)
            for i in range(8):
                t = i / 7
                ang = math.radians(-70 + 140 * t)
                r0 = 6.0
                c = (h[0] - 2.0 - 12.0 * math.cos(ang) * 0.9, h[1] + 22.0 + 14.0 * math.sin(ang), h[2])
                m.box(ax, min(h[0] - 1.0, c[0]), c[1] - 1.6, c[2] - 0.6, max(h[0] - 1.0, c[0]), c[1] + 1.6,
                      c[2] + 0.6, armour(P, "red", "red_dark", light="red_light", trim="white"))
        return m
    return build, P


build, P = make("apollomon")
