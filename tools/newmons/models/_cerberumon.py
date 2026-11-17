"""Shared builder for Cerberumon (CobbleEffort: Digital; hand-built after the official art on wikimon.net).

"base": a lean black hound of the underworld on four legs, steel-grey armour plates, red-lined joints, a fanged
snarling head with a second head growing from its shoulder, long steel claws on the forelegs and a whip tail.
"x": the X-Antibody form, a hulking dark-violet armoured beast bristling with huge blade spikes, long steel claws and
a spiked tail. "werewolf": Werewolf Mode, a black armoured wolf-man whose arms end in two great wolf heads with red
jaws and steel teeth, clawed digitigrade legs and a segmented tail.
Shiny: white with blue lining.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _digibody import humanoid
from _digidetail import armour, fur, metal, solid
from _route import pal, tone

BASE = {"black": (44, 44, 52), "black_dark": (14, 14, 18), "black_light": (110, 112, 128), "steel": (196, 200, 214),
        "steel_dark": (90, 94, 108), "red": (190, 40, 40), "red_dark": (100, 14, 16), "violet": (70, 50, 130),
        "violet_dark": (24, 16, 60), "violet_light": (140, 110, 220), "teal": (60, 220, 200), "eye": (250, 220, 60),
        "mouth": (120, 20, 30), "tooth": (246, 246, 246)}
SHINY = {"black": (230, 230, 240), "black_dark": (150, 150, 170), "black_light": (255, 255, 255), "red": (40, 110, 230),
         "red_dark": (14, 50, 140), "violet": (200, 200, 220), "violet_dark": (120, 120, 140)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "black", "black_dark", tip="black_light", length=1.2)
PLATE = armour(P, "black", "black_dark", light="black_light", trim="red", trim_w=0.3)
VIOLET = armour(P, "violet", "violet_dark", light="violet_light", trim="teal", trim_w=0.25)
STEEL = metal(P, "steel", dark="steel_dark")
RED = armour(P, "red", "red_dark")


def wolf_head(m, bone, c, s, d, mats):
    """A wolf head at c, scale s, facing along d (+1: -z, -1: +z): skull, snout, open jaw, teeth, ears, eyes."""
    cx, cy, cz = c
    f = -1 if d > 0 else 1
    m.round_box(bone, cx, cz, 3.0 * s, 3.4 * s, cy - 2.2 * s, cy + 2.4 * s, mats["head"], cut=1)
    z0, z1 = sorted((cz + f * 2.0 * s, cz + f * 8.0 * s))
    m.box(bone, cx - 1.8 * s, cy - 0.4 * s, z0, cx + 1.8 * s, cy + 1.4 * s, z1, mats["head"])
    m.box(bone, cx - 1.6 * s, cy - 2.4 * s, z0, cx + 1.6 * s, cy - 1.2 * s, z1, mats["jaw"],
          rotation=(-f * 14, 0, 0), pivot=(cx, cy - 1.0 * s, cz + f * 2.0 * s))
    m.box(bone, cx - 1.5 * s, cy - 1.2 * s, z0, cx + 1.5 * s, cy - 0.4 * s, z1, solid(P, "mouth"))
    for i in range(4):
        zz = cz + f * (3.0 + i * 1.4) * s
        for sx in (-1, 1):
            spike(m, bone, (cx + sx * 1.3 * s, cy - 0.4 * s, zz), (0, -1, 0), 0.6 * s, 1.2 * s, solid(P, "tooth"))
    for sx in (-1, 1):
        spike(m, bone, (cx + sx * 2.0 * s, cy + 2.2 * s, cz - f * 0.6 * s), (sx * 0.3, 1, -f * 0.4), 1.4 * s, 3.4 * s,
              mats["head"], tip=0.4)
        m.box(bone, cx + sx * 1.9 * s - 0.4, cy + 1.0 * s, cz + f * 2.2 * s - 0.4, cx + sx * 1.9 * s + 0.4,
              cy + 1.6 * s, cz + f * 2.2 * s + 0.4, solid(P, "eye", glow=True))


def make(name, variant="base"):
    def build():
        m = Model(name)
        if variant == "werewolf":
            mats = {"skin": PLATE, "chest": PLATE, "abs": FUR, "pelvis": PLATE, "neck": FUR, "hand": STEEL,
                    "finger": STEEL, "claw": STEEL, "thigh": FUR, "knee": RED, "shin": PLATE, "calf": PLATE,
                    "foot": PLATE, "talon": STEEL}
            a = humanoid(m, mats, bulk=1.05, arm_bulk=1.1, leg_bulk=1.05, digitigrade=True, claws=True, talons=True,
                         name=name)
            bd = a["body"]
            hd = m.bone("head", bd, (0, 55, 0))
            wolf_head(m, hd, (0, 57.0, -0.6), 0.9, 1, {"head": PLATE, "jaw": RED})
            for nm in ("arm_left", "arm_right"):                         # wolf-head gauntlets
                ab = a[nm]
                h = ab["hand"]
                sx = 1 if nm == "arm_left" else -1
                m.round_box(ab["bone"], h[0], h[2], 3.0, 3.0, h[1] - 2.0, ab["elbow"][1] - 2.0, RED, cut=1)
                wolf_head(m, ab["bone"], (h[0] + sx * 1.0, h[1] - 1.0, h[2] - 2.0), 1.7, 1,
                          {"head": PLATE, "jaw": RED})
            tl = m.bone("tail", bd, (0, 31, 3))
            pts = [(0, 31.0, 3.0), (3.0, 26.0, 8.0), (8.0, 22.0, 12.0), (14.0, 22.0, 14.0)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, tl, p0, p1, 3 - j, PLATE, extend=0.5)
            return m
        x = variant == "x"
        BODY = VIOLET if x else PLATE
        mats = {"skin": BODY, "belly": RED if not x else VIOLET, "neck": FUR if not x else VIOLET, "head": BODY,
                "snout": BODY, "jaw": RED, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"),
                "leg_upper": BODY, "leg_lower": FUR if not x else VIOLET, "paw": BODY, "claw": STEEL,
                "tail": BODY}
        a = quadruped(m, mats, name, length=26.0 if not x else 30.0, body_y=14.0 if not x else 18.0,
                      body_rx=5.4 if not x else 7.4, body_ry=5.4 if not x else 7.0, chest_bulk=1.25,
                      neck=((0, 18, -13), (0, 20, -17)) if not x else ((0, 24, -16), (0, 26, -21)),
                      head_len=10.0, head_w=3.4, head_h=3.8, snout=0.6, mouth_open=18, teeth=5, leg_bulk=1.3,
                      toes=3, tail=((0, 18, 16), (3, 22, 22), (8, 24, 26), (13, 22, 28)),
                      tail_r=(1.6, 1.2, 1.0, 0.8))
        bd, hd = a["body"], a["head"]
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.4, a["skull_top"] - 0.4, a["head_c"][2] + 1.0), (sx * 0.3, 1, 0.4), 1.4, 3.6, BODY)
            for nm in ("leg_front_left", "leg_front_right"):              # long steel claws on the forelegs
                lg = a[nm]
                w = lg["wrist"]
                for j in range(3):
                    spike(m, lg["bone"], (w[0] + (j - 1) * 1.0, 1.2, w[2] - 2.4), (0, -0.1, -1), 1.0,
                          5.0 if not x else 8.0, STEEL, tip=0.3)
        if not x:                                                         # the second head on its shoulder
            nb = m.bone("head_2", bd, (-4.0, 20.0, -9.0))
            wolf_head(m, nb, (-5.0, 22.0, -12.0), 0.8, 1, {"head": PLATE, "jaw": RED})
            for j in range(5):
                spike(m, bd, (0, 21.0, -8.0 + j * 4.0), (0, 1, 0.5), 1.6, 2.6, STEEL)
        else:                                                             # huge blade spikes
            for j, (px, py, pz, d) in enumerate(((0, 26, -6, (0, 1, 0.4)), (4, 25, -2, (0.6, 1, 0.3)),
                                                  (-4, 25, -2, (-0.6, 1, 0.3)), (5, 24, 6, (0.8, 0.8, 0.6)),
                                                  (-5, 24, 6, (-0.8, 0.8, 0.6)), (0, 26, 8, (0, 1, 0.8)),
                                                  (7, 20, -10, (1, 0.6, -0.2)), (-7, 20, -10, (-1, 0.6, -0.2)))):
                spike(m, bd, (px, py, pz), d, 2.6, 9.0 + (j % 3) * 2.0, STEEL, tip=0.8)
            for p in a["tail_pts"][1:]:
                spike(m, a["tail"], p, (0, 1, 0.3), 1.4, 3.0, STEEL)
        return m
    return build
