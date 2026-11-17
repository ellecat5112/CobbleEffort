"""Dark Lizamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the smouldering lizard. A hunched lizard wrapped in shaggy dark-red fur that rises off it in flame-
like tufts, its head covered by a cracked gold bone skull mask with burning red eyes, smoke puffing from its jaws, and
long curved ivory claws. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import fur, metal, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a hunched lizard in shaggy dark-red flame-like fur with a cracked gold bone skull mask, burning red eyes and "
        "long curved ivory claws")
BASE = {"fur": (120, 40, 26), "fur_dark": (54, 14, 10), "fur_light": (190, 80, 50), "mask": (226, 200, 140),
        "mask_dark": (150, 120, 70), "claw": (240, 230, 206), "eye": (250, 50, 40), "mouth": (100, 20, 20),
        "tooth": (250, 248, 240), "smoke": (220, 220, 226, 170)}
SHINY = {"fur": (50, 60, 110), "fur_dark": (16, 20, 50), "fur_light": (100, 120, 190)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", tip="fur_light", length=2.0)
MASK = metal(P, "mask", dark="mask_dark", streak=2.0)
TUFT = strands(P, "fur", "fur_dark", tip="fur_light")


def maskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "north") and abs(abs(x) - 2.6) < 1.2 and abs(y - 33.4) < 0.7 and z < -6.0:
        return p["eye"], p["eye"]
    if abs((x * 1.3 + y * 0.7) % 5.0 - 2.5) < 0.12 and face == "up":
        return tone(p["mask_dark"], face), None                       # cracks
    return MASK(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("darklizamon")
    mats = {"skin": FUR, "belly": FUR, "neck": FUR, "head": maskf, "snout": maskf, "jaw": maskf,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": FUR, "hand": FUR,
            "claw": solid(P, "claw"), "thigh": FUR, "shin": FUR, "foot": FUR, "talon": solid(P, "claw"), "tail": FUR,
            "tail_tip": FUR}
    a = theropod(m, mats, "darklizamon", hip_y=14.0, hip_z=3.0, chest=(0, 24.0, -3.0), body_r=6.0, chest_r=6.4,
                 neck_top=(0, 30.0, -6.0), head_len=10.0, head_w=4.0, head_h=4.0, mouth_open=20, teeth=5,
                 arm_len=11.0, arm_bulk=1.3, leg_bulk=1.3, stance=4.6,
                 tail=((0, 13, 9), (2, 9, 15), (4, 5, 21), (6, 3, 27)), tail_r=(4.0, 3.0, 2.0, 1.2))
    bd, hd = a["body"], a["head"]
    for nm in ("arm_left", "arm_right"):                                       # long curved claws
        h = a[nm]["hand"]
        for j in range(3):
            pts = [(h[0] + (j - 1) * 1.2, h[1] - 1.0, h[2] - 1.0)]
            for s in range(1, 4):
                t = s / 3
                pts.append((pts[0][0], h[1] - 1.0 - 6.0 * t, h[2] - 1.0 - 4.0 * t * t))
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, a[nm]["bone"], p0, p1, 1, solid(P, "claw"), extend=0.3)
    for i in range(22):                                                        # flame-like fur tufts
        t = i / 21
        ang = (i * 2.4) % (2 * math.pi)
        base = (5.6 * math.sin(ang) * (1 - 0.3 * t), 12.0 + 16.0 * t, -2.0 + 5.6 * math.cos(ang) * 0.7)
        d = (math.sin(ang) * 0.8, 1.0, math.cos(ang) * 0.4 + 0.4)
        spike(m, bd, base, d, 2.2, 4.0 + (i % 4) * 1.2, TUFT, tip=0.2)
    for i in range(5):                                                         # mane of tufts behind the mask
        spike(m, hd, ((i - 2) * 1.4, 34.0, -3.0), ((i - 2) * 0.3, 1, 0.6), 1.8, 5.0, TUFT, tip=0.2)
    ex = a["eye"]
    pb = m.bone("smoke", hd, (ex[0], ex[1] - 2.0, ex[2] - 6.0))                # a puff of smoke
    for j in range(3):
        m.round_box(pb, -1.6 - j * 1.6, ex[2] - 8.0 - j * 1.0, 1.0 + j * 0.3, 1.0 + j * 0.3, ex[1] - 2.4 + j * 0.6,
                    ex[1] - 0.6 + j * 0.8, solid(P, "smoke"), cut=1)
    return m
