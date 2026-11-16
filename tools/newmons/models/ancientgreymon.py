"""Ancient Greymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the ancient warrior of flame, a dragon in crimson armour. A white dragon-skull helm
with a blond mane, gold-trimmed crimson plates over its chest, shoulders and legs, gold claws, a long crimson tail
and two great wings of living flame. 35 blocks tall.

Front is -z, y is up. 58 units tall (the wings); Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digibody import dome, shell
from _digidetail import armour, cutout, eye, flame_inside, local, metal, mix, scales, solid, strands
from _route import pal, tone

HEIGHT = 58
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a dragon in gold-trimmed crimson armour: a white dragon-skull helm with a blond mane, gold claws, a long "
        "crimson tail and two great wings of living flame")
BASE = {"red": (190, 30, 30), "red_dark": (100, 12, 12), "red_light": (240, 100, 80), "gold": (236, 190, 60),
        "gold_dark": (160, 112, 26), "gold_light": (255, 240, 170), "white": (240, 240, 236), "white_dark": (170, 170, 176),
        "hide": (150, 36, 30), "hide_dark": (80, 14, 12), "mane": (250, 220, 90), "mane_dark": (220, 150, 40),
        "flame": (255, 140, 40, 220), "flame_core": (255, 230, 120, 235), "mouth": (110, 20, 30), "eye": (60, 200, 255),
        "pupil": (20, 10, 10), "tongue": (220, 80, 90)}
SHINY = {"red": (40, 40, 50), "red_dark": (16, 16, 22), "red_light": (110, 110, 130), "hide": (50, 50, 60),
         "hide_dark": (20, 20, 26), "flame": (80, 170, 255, 220), "flame_core": (190, 235, 255, 235),
         "mane": (230, 230, 240), "mane_dark": (170, 170, 190)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", light="red_light", trim="gold")
HIDE = scales(P, "hide", "hide_dark", size=1.8, rim_mix=0.4)
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
SKULL = armour(P, "white", "white_dark")
MANE = strands(P, "mane", "mane_dark", tip="gold_light")


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["flame_core"] if v / max(H, 1e-6) < 0.35 else p["flame"]
    return c, c[:3]


def build():
    m = Model("ancientgreymon")
    mats = {"skin": HIDE, "belly": RED, "neck": HIDE, "head": SKULL, "snout": SKULL, "jaw": HIDE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "white"), "tongue": solid(P, "tongue"), "arm": RED,
            "hand": HIDE, "claw": GOLD, "thigh": RED, "shin": RED, "foot": HIDE, "talon": GOLD, "tail": HIDE,
            "tail_tip": HIDE}
    a = theropod(m, mats, "ancientgreymon", hip_y=18.0, hip_z=4.0, chest=(0, 26.0, -6.0), body_r=7.0, chest_r=7.0,
                 neck_top=(0, 32.0, -12.0), head_len=12.0, head_w=4.4, head_h=4.6, mouth_open=14, arm_len=11.0,
                 arm_bulk=1.4, leg_bulk=1.5, stance=5.4,
                 tail=((0, 16, 12), (2, 13, 20), (5, 10, 27), (8, 8, 33), (10, 7, 38)), tail_r=(5, 4, 3, 2, 1.2))
    hd = a["head"]
    z0, z1 = a["skull_z"]
    top = a["skull_top"]
    for sx in (-1, 1):                                           # skull helm horns + eye
        spike(m, hd, (sx * 3.6, top - 0.6, z1 - 1.0), (sx * 0.6, 0.5, 1), 1.6, 5.0, SKULL, tip=0.8)
    spike(m, hd, (0, top, a["snout_front"] + 3.0), (0, 1, -0.3), 1.4, 2.6, SKULL)
    mane = m.bone("mane", hd, (0, top, z1))
    for i in range(14):                                          # blond mane streaming back
        ang = math.radians(-70 + i * 10.8)
        base = (3.4 * math.sin(ang), top - 1.0 + math.cos(ang), z1 - 1.0)
        tip = (base[0] * 2.2, base[1] + 3.0 * math.cos(ang), base[2] + 9.0 + (i % 3) * 2)
        rod(m, mane, base, tip, 2, MANE, extend=0.3, t2=2)
    bd = a["body"]
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):          # pauldrons with horns
        ab = a[nm]
        dome(m, ab["bone"], (ab["shoulder"][0] + sx * 1.0, ab["shoulder"][1] + 0.5, ab["shoulder"][2]), 4.0, 3.4, RED)
        spike(m, ab["bone"], (ab["shoulder"][0] + sx * 3.0, ab["shoulder"][1] + 2.0, ab["shoulder"][2] + 1.0),
              (sx * 0.5, 0.6, 0.6), 1.8, 4.0, GOLD, tip=0.8)
    shell(m, bd, (0, 0, -5.0), 7.4, 21.0, 30.0, -70, 70, 7, 1.2, RED)                   # breastplate
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # wings of flame
        wb = m.bone(nm, bd, (sx * 4.0, 29.0, 0.0))
        for j, (ang, dz) in enumerate(((10, 0.0), (35, 2.0), (60, 4.0))):
            x0, x1 = sorted((sx * 4.0, sx * 26.0))
            m.box(wb, x0, 22.0, dz, x1, 52.0, dz, cutout(flame_inside(5, sx * 0.3, j + 2), flamef),
                  rotation=(-15, 0, -sx * (ang - 30)), pivot=(sx * 4.0, 29.0, dz))
    return m
