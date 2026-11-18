"""Gold V-dramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the golden Armor dragon: a stocky golden dragon-boy with a white muzzle and chest, red eyes with a scar mark, a great
curved golden horn on its snout and two white horns on its head, a toothy grin, white clawed hands, golden wings
folded at its back and a V-shaped mark on its chest. Adult stage, 15 blocks tall.

Front is -z, y is up. 44 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing, theropod
from _digidetail import metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a stocky golden dragon with a white muzzle and chest, a great curved golden snout horn, two white head horns, "
        "a toothy grin and golden wings")
BASE = {"gold": (240, 200, 60), "gold_dark": (170, 120, 20), "gold_light": (255, 240, 150), "white": (246, 246, 246),
        "white_dark": (190, 190, 200), "eye": (210, 30, 40), "mouth": (130, 20, 30), "tooth": (250, 250, 240),
        "claw": (246, 246, 246), "red": (200, 30, 40)}
SHINY = {"gold": (200, 204, 218), "gold_dark": (120, 124, 138), "gold_light": (250, 250, 255)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = metal(P, "gold", dark="gold_dark", light="gold_light")
WHITE = skin(P, "white", dark="white_dark")


def bellyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(abs(x) - (30.0 - y) * 0.5) < 0.4 and 24.0 < y < 30.0:
        return tone(p["gold"], face), None
    return WHITE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("goldvdramon")
    mats = {"skin": HIDE, "belly": bellyf, "neck": HIDE, "head": HIDE, "jaw": WHITE, "mouth": solid(P, "mouth"),
            "tooth": solid(P, "tooth"), "arm": HIDE, "hand": WHITE, "claw": solid(P, "claw"), "thigh": HIDE,
            "shin": HIDE, "foot": HIDE, "talon": solid(P, "claw"), "tail": HIDE}
    a = theropod(m, mats, "goldvdramon", hip_y=14.0, chest=(0, 26.0, -1.0), body_r=6.0, chest_r=5.6,
                 neck_top=(0, 33.0, -3.0), head_len=8.0, head_w=4.0, head_h=4.6, mouth_open=14, teeth=4,
                 arm_len=8.0, leg_bulk=1.2, tail=((0, 14, 6), (0, 10, 12), (0, 7, 17)), tail_r=(3.0, 2.0, 1.2),
                 digitigrade=False)
    hd, bd = a["head"], a["body"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.5, ez - 0.7, max(sx * ex, sx * (ex + 0.3)), ey + 0.5, ez + 0.7,
              solid(P, "eye"))
        spike(m, hd, (sx * 2.4, ey + 2.6, ez + 2.0), (sx * 0.4, 1, 0.5), 1.4, 6.0, WHITE, tip=0.8)
    sf = (0, ey + 1.0, a["snout_front"] + 1.6)
    pts = [sf, (0, ey + 5.0, sf[2] - 1.0), (0, ey + 9.0, sf[2] + 2.0)]                       # great curved horn
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, 2 - j, metal(P, "gold", dark="gold_dark"), extend=0.4, t2=3 - j)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 30.0, 4.0))
        bat_wing(m, wb, (side * 3.0, 30.0, 4.0), 10.0, 10.0, 3, HIDE, metal(P, "gold", dark="gold_dark"), side=side,
                 sweep=30)
    return m
