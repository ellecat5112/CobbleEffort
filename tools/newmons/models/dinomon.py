"""Dinomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the primeval tyrant. An upright crimson tyrannosaur with a black ribbed belly plate, a crown of
flaming golden spikes, steel claws and talons, a long tail tipped with a jade fan, surrounded by a great sphere of
roiling orange fire from which eight huge ivory horns jut outward. 35 blocks tall.

Front is -z, y is up. 52 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import cutout, flame_inside, local, metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 52
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("an upright crimson tyrannosaur with a black ribbed belly, a crown of flaming gold spikes, a jade-tipped tail and "
        "a great sphere of orange fire bristling with huge ivory horns")
BASE = {"red": (190, 40, 30), "red_dark": (90, 10, 10), "red_light": (240, 120, 90), "black": (40, 36, 40),
        "black_dark": (12, 10, 12), "gold": (250, 200, 50), "jade": (60, 200, 150), "ivory": (240, 236, 220),
        "ivory_dark": (170, 160, 140), "steel": (200, 204, 214), "steel_dark": (100, 104, 114),
        "fire": (255, 150, 30, 200), "fire_core": (255, 240, 140, 230), "mouth": (130, 20, 30), "tooth": (250, 250, 246),
        "eye": (250, 220, 60)}
SHINY = {"red": (40, 60, 150), "red_dark": (10, 20, 70), "red_light": (120, 150, 230), "fire": (120, 200, 255, 200),
         "fire_core": (230, 250, 255, 230)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "red", "red_dark", size=1.6, light="red_light", rim_mix=0.3)
STEEL = metal(P, "steel", dark="steel_dark")


def bellyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["black_dark"] if y % 2.0 < 0.5 else p["black"], face), None


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.35 else p["fire"]
    return c, c[:3]


def build():
    m = Model("dinomon")
    mats = {"skin": HIDE, "belly": bellyf, "neck": HIDE, "head": HIDE, "snout": HIDE, "jaw": HIDE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": HIDE, "hand": HIDE, "claw": STEEL,
            "thigh": HIDE, "shin": HIDE, "foot": HIDE, "talon": STEEL, "tail": HIDE, "tail_tip": HIDE}
    a = theropod(m, mats, "dinomon", hip_y=18.0, hip_z=2.0, chest=(0, 32.0, -2.0), body_r=6.6, chest_r=6.6,
                 neck_top=(0, 40.0, -4.0), head_len=10.0, head_w=4.0, head_h=4.4, mouth_open=20, teeth=5, arm_len=10.0,
                 arm_bulk=1.4, leg_bulk=1.6, stance=5.0,
                 tail=((0, 18, 8), (0, 22, 15), (0, 30, 20), (0, 40, 22), (0, 48, 20)), tail_r=(4.0, 3.0, 2.2, 1.6, 1.0))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.6,
              solid(P, "eye", glow=True))
    for i in range(7):                                                       # crown of flaming gold spikes
        ang = math.radians(-90 + i * 30)
        spike(m, hd, (2.6 * math.sin(ang), ey + 2.0, ez + 2.0 + 2.0 * math.cos(ang)), (math.sin(ang) * 0.5, 1, 0.4),
              1.2, 5.0, solid(P, "gold", glow=True), tip=0.3)
    e = a["tail_pts"][-1]
    for j in range(5):                                                       # jade tail fan
        spike(m, a["tail_tip"], e, (-0.6 + j * 0.3, 0.6, 0.6), 1.0, 5.0, solid(P, "jade"), tip=0.3)
    fb = m.bone("fire", bd, (0, 26, 2))                                      # sphere of fire + ivory horns
    for i in range(10):
        ang = 2 * math.pi * i / 10
        cx, cz = 16.0 * math.cos(ang), 2.0 + 16.0 * math.sin(ang)
        m.box(fb, cx - 6.0, 12.0, cz, cx + 6.0, 40.0, cz, cutout(flame_inside(5, 0.0, i), firef),
              rotation=(0, -math.degrees(ang) + 90, 0), pivot=(cx, 12.0, cz))
    for i in range(8):
        ang = 2 * math.pi * i / 8 + 0.3
        d = (math.cos(ang), 0.25 * math.sin(3 * ang), math.sin(ang))
        spike(m, fb, (12.0 * d[0], 26.0 + 6.0 * d[1], 2.0 + 12.0 * d[2]), d, 3.0, 12.0,
              metal(P, "ivory", dark="ivory_dark"), tip=1.0)
    return m
