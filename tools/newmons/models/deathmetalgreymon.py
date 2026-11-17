"""Death Metal Greymon (a Digimon of the CobbleEffort: Digital crossover; after the manga art on wikimon.net, the C'mon
Digimon story, where Deathmon takes Metal Greymon's shape): a cyborg tyrannosaur gone feral. A hunched ash-grey
dinosaur with a wild mane of spiky hair, a cracked steel helmet over a jaw of enormous jagged fangs, a round staring
cyber-eye pod on its shoulder, a steel chest plate, a spiked steel claw arm, steel knee and tail spikes and ragged
black bat wings. 25 blocks tall.

Front is -z, y is up. 48 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing, theropod
from _digidetail import armour, cutout, local, metal, noise2, scales, solid, strands
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a hunched ash-grey cyborg tyrannosaur with a wild spiky mane, a cracked steel helmet, enormous jagged fangs, "
        "a cyber-eye pod, a spiked steel claw arm and ragged black bat wings")
BASE = {"hide": (130, 128, 136), "hide_dark": (60, 58, 66), "hide_light": (196, 194, 204), "hair": (220, 220, 226),
        "hair_dark": (110, 110, 120), "steel": (200, 204, 216), "steel_dark": (90, 94, 106), "black": (36, 34, 40),
        "black_dark": (10, 10, 14), "mouth": (110, 20, 30), "tooth": (250, 248, 240), "eye": (250, 60, 40),
        "lens": (30, 30, 34)}
SHINY = {"hide": (150, 100, 70), "hide_dark": (80, 46, 26), "hide_light": (220, 170, 130), "hair": (250, 230, 150)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "hide", "hide_dark", size=1.6, light="hide_light", rim_mix=0.3)
STEEL = metal(P, "steel", dark="steel_dark")
PLATE = armour(P, "steel", "steel_dark", rivets=True)
HAIR = strands(P, "hair", "hair_dark")


def wingf(x, y, z, face, variant, box=None, **k):
    return tone(P(variant)["black"], face), None


def tatter(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return noise2(u * 0.7, v * 0.5, 17) < 0.8


def build():
    m = Model("deathmetalgreymon")
    mats = {"skin": HIDE, "belly": HIDE, "neck": HIDE, "head": PLATE, "snout": PLATE, "jaw": HIDE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": HIDE, "hand": HIDE, "claw": STEEL,
            "thigh": HIDE, "shin": HIDE, "foot": HIDE, "talon": STEEL, "tail": HIDE, "tail_tip": HIDE}
    a = theropod(m, mats, "deathmetalgreymon", hip_y=18.0, hip_z=3.0, chest=(0, 30.0, -3.0), body_r=7.0, chest_r=7.4,
                 neck_top=(0, 36.0, -7.0), head_len=12.0, head_w=5.0, head_h=5.0, mouth_open=30, teeth=7,
                 arm_len=10.0, arm_bulk=1.4, leg_bulk=1.6, stance=5.0,
                 tail=((0, 18, 10), (2, 15, 18), (5, 12, 26), (8, 10, 33)), tail_r=(4.4, 3.4, 2.4, 1.4))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.8,
              solid(P, "eye", glow=True))
    for i in range(14):                                                        # wild spiky mane
        ang = math.radians(-80 + i * 12)
        spike(m, hd, (3.0 * math.sin(ang), ey + 2.0, ez + 2.0 + 2.0 * abs(math.cos(ang))),
              (math.sin(ang) * 0.8, 0.8, 0.8), 1.6, 6.0 + (i % 3) * 2.0, HAIR, tip=0.2)
    for j in range(6):                                                         # enormous jagged fangs
        for sx in (-1, 1):
            spike(m, hd, (sx * 3.0, ey - 3.0, ez - 3.0 - j * 1.4), (sx * 0.1, -1, -0.1), 1.2, 3.0 - (j % 2),
                  solid(P, "tooth"), tip=0.25)
    m.round_box(bd, 0, -6.0, 5.4, 2.0, 24.0, 32.0, PLATE, cut=1)                # chest plate
    pod = (6.6, 34.0, -1.0)                                                    # cyber-eye pod on the shoulder
    m.round_box(bd, pod[0], pod[2], 2.6, 2.6, pod[1] - 2.6, pod[1] + 2.6, STEEL, cut=1)
    m.box(bd, pod[0] - 1.6, pod[1] - 1.6, pod[2] - 2.9, pod[0] + 1.6, pod[1] + 1.6, pod[2] - 2.5, solid(P, "lens"))
    m.box(bd, pod[0] - 0.6, pod[1] - 0.6, pod[2] - 3.0, pod[0] + 0.6, pod[1] + 0.6, pod[2] - 2.8,
          solid(P, "eye", glow=True))
    ar = a["arm_right"]                                                        # spiked steel claw arm
    h = ar["hand"]
    m.round_box(ar["bone"], h[0], h[2], 3.0, 3.0, h[1] - 1.0, h[1] + 5.0, PLATE, cut=1)
    for j in range(3):
        spike(m, ar["bone"], (h[0] + (j - 1) * 1.4, h[1] - 1.0, h[2] - 1.0), (0, -1, -0.5), 1.2, 7.0, STEEL, tip=0.2)
    for nm in ("leg_left", "leg_right"):
        kn = a[nm]["knee"]
        spike(m, a[nm]["bone"], kn, (0, 0.3, -1), 1.6, 3.6, STEEL, tip=0.2)
    for p in a["tail_pts"][1:]:
        spike(m, a["tail"], p, (0, 1, 0.3), 1.4, 3.0, STEEL, tip=0.2)
    for side in (1, -1):                                                       # ragged black bat wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 34.0, 4.0))
        bat_wing(m, wb, (side * 4.0, 34.0, 4.0), 20.0, 18.0, 4, STEEL, cutout(tatter, wingf), side=side, sweep=25)
    return m
