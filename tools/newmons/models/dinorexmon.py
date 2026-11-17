"""Dinorexmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the burrowing tyrant. A low, crouching dinosaur of rough green scales with a yellow belly, a broad
fanged head with a frilled green crest and spikes behind its jaws, and enormous ivory sickle claws on its arms that
it drags through the earth, with a thick tail stretched out behind. 35 blocks tall.

Front is -z, y is up. 34 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import scales, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a low crouching dinosaur of rough green scales with a yellow belly, a frilled crest, a fanged head and enormous "
        "ivory sickle claws dragged through the earth")
BASE = {"green": (50, 120, 70), "green_dark": (16, 56, 30), "green_light": (120, 190, 130), "yellow": (210, 200, 110),
        "yellow_dark": (150, 130, 60), "ivory": (240, 236, 220), "ivory_dark": (170, 160, 140), "mouth": (180, 40, 50),
        "tooth": (250, 250, 246), "eye": (250, 200, 40)}
SHINY = {"green": (180, 140, 60), "green_dark": (100, 70, 20), "green_light": (230, 200, 130)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "green", "green_dark", size=1.6, light="green_light", rim_mix=0.4)
BELLY = skin(P, "yellow", dark="yellow_dark")
IVORY = skin(P, "ivory", dark="ivory_dark", var=0.03)


def build():
    m = Model("dinorexmon")
    mats = {"skin": HIDE, "belly": BELLY, "neck": HIDE, "head": HIDE, "snout": HIDE, "jaw": HIDE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": HIDE, "hand": HIDE, "claw": IVORY,
            "thigh": HIDE, "shin": HIDE, "foot": HIDE, "talon": IVORY, "tail": HIDE, "tail_tip": HIDE}
    a = theropod(m, mats, "dinorexmon", hip_y=12.0, hip_z=4.0, chest=(0, 18.0, -6.0), body_r=6.6, chest_r=6.6,
                 neck_top=(0, 25.0, -12.0), head_len=11.0, head_w=4.4, head_h=4.4, mouth_open=28, teeth=6,
                 arm_len=8.0, arm_bulk=1.6, leg_bulk=1.6, stance=5.4,
                 tail=((0, 12, 11), (0, 10, 19), (0, 8, 27), (0, 6, 35)), tail_r=(4.4, 3.4, 2.4, 1.4))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.6,
              solid(P, "eye", glow=True))
        for j in range(3):                                                    # spikes behind the jaws
            spike(m, hd, (sx * 4.0, ey - 1.0 - j * 1.2, ez + 3.0 + j), (sx, -0.2, 0.6), 1.0, 3.0, IVORY, tip=0.25)
    for i in range(6):                                                        # frilled crest
        spike(m, hd, (0, ey + 2.0, ez + i * 1.4), (0, 1, 0.8), 2.2, 5.0 - i * 0.5, HIDE, tip=0.4)
    for i in range(9):                                                        # back spikes
        t = i / 8
        p = (0, 23.0 - 9.0 * t, -6.0 + 30.0 * t)
        spike(m, bd if i < 5 else a["tail"], p, (0, 1, 0.4), 2.0, 3.6 - 2.0 * t, HIDE, tip=0.5)
    for nm in ("arm_left", "arm_right"):                                      # enormous ivory sickle claws
        ar = a[nm]
        h = ar["hand"]
        sx = 1 if h[0] > 0 else -1
        for j in range(3):
            pts = [(h[0] + sx * j * 1.6, h[1] - 1.0, h[2] - 1.0)]
            for s in range(1, 4):
                t = s / 3
                pts.append((pts[0][0] + sx * 2.0 * t, h[1] - 1.0 - 4.0 * math.sin(t * 1.6), h[2] - 1.0 - 12.0 * t))
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, ar["bone"], p0, p1, 1, IVORY, extend=0.4, t2=3)
    return m
