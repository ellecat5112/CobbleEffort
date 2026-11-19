"""Vikaralamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the boar general of the Twelve Devas: a hulking boar with a great shaggy brown hide marked with a
silver sigil, huge curved ivory tusks, a grey snout with red nostrils, red eyes, red spikes along its back and short
grey legs. 25 blocks.

Front is -z, y is up. Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import eye, fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a hulking shaggy brown boar with huge curved ivory tusks, a grey snout, red eyes and red spikes along its back"
BASE = {"brown": (120, 90, 60), "brown_dark": (60, 40, 24), "grey": (150, 150, 156), "grey_dark": (80, 80, 86),
        "tusk": (246, 240, 220), "tusk_dark": (200, 180, 130), "red": (210, 50, 50), "eye": (230, 50, 50),
        "pupil": (30, 10, 10), "white": (255, 255, 255), "sigil": (220, 224, 230)}
SHINY = {"brown": (80, 80, 110), "brown_dark": (36, 36, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs(math.hypot(z + 2.0, y - 16.0) - 3.4) < 0.4:
        return tone(p["sigil"], face), None
    return fur(P, "brown", "brown_dark", length=2.0)(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 14.0, y - 16.0, 0.9, "eye", slit=True)
        if c is not None:
            return c, None
    return hidef(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("vikaralamon")
    mats = {"skin": hidef, "belly": hidef, "neck": hidef, "head": headf, "leg": skin(P, "grey", dark="grey_dark"),
            "paw": skin(P, "grey", dark="grey_dark"), "claw": solid(P, "grey_dark"), "tail": hidef}
    a = quadruped(m, mats, "vikaralamon", length=22.0, body_y=13.0, body_rx=9.0, body_ry=9.0, chest_bulk=1.2,
                  neck=((0, 14, -11), (0, 14, -13)), head_len=10.0, head_w=5.6, head_h=7.0, snout=0.5, mouth_open=6,
                  teeth=6, tail=((0, 14, 11),), tail_r=(1.4,), toes=0, claws=False)
    bd, hd = a["body"], a["head"]
    sf = a["snout_front"]
    m.round_box(hd, 0, sf + 1.6, 3.4, 1.6, 9.6, 14.0, skin(P, "grey", dark="grey_dark"), cut=1)   # snout disc
    for sx in (-1, 1):
        m.box(hd, sx * 1.4 - 0.6, 11.0, sf - 0.1, sx * 1.4 + 0.6, 12.6, sf + 0.2, solid(P, "red"))
        pts = [(sx * 4.0, 10.0, sf + 3.0), (sx * 7.0, 9.0, sf + 1.0), (sx * 9.0, 12.0, sf - 1.0), (sx * 9.0, 16.0, sf)]
        for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 3 - i, metal(P, "tusk", dark="tusk_dark"), extend=0.4)
    for j in range(5):
        spike(m, bd, ((j % 2) * 2.0 - 1.0, 21.0 - abs(j - 2) * 0.8, -8.0 + j * 4.0), (0.2 * (j - 2), 1, -0.3), 1.4, 4.0,
              solid(P, "red"), tip=0.8)
    return m
