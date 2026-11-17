"""Betamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): an amphibian with a fin crest. A squat green body with dark blue stripes along its sides, a broad
grinning mouth with two fangs, red eyes, a tall orange fin crest from brow to back, and four stubby legs with steel
claws. 1 block tall.

Front is -z, y is up. 30 units tall; Child stage. make(x=True): Betamon (X-Antibody) (teal with black stripes, a
yellow-to-red fin, white spikes and violet claws).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import cutout, eye, local, metal, mix, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = ("a squat green amphibian with dark blue side stripes, a broad fanged grin, red eyes, a tall orange fin crest "
        "and stubby legs with steel claws")
BASE = {"green": (70, 170, 70), "green_dark": (30, 100, 30), "stripe": (40, 70, 140), "fin": (250, 120, 40),
        "fin_tip": (250, 80, 30), "fin_root": (250, 200, 80), "claw": (210, 214, 226), "claw_dark": (110, 114, 128),
        "eye": (220, 40, 40), "pupil": (20, 10, 10), "white": (250, 250, 250), "mouth": (100, 30, 30),
        "tooth": (250, 250, 246), "teal": (60, 180, 160), "teal_dark": (20, 110, 100), "spike": (240, 240, 236),
        "violet": (100, 80, 190), "black": (30, 40, 40)}
SHINY = {"green": (230, 170, 60), "green_dark": (170, 110, 20), "fin": (60, 140, 240), "fin_tip": (40, 80, 200),
         "fin_root": (160, 220, 250), "teal": (200, 90, 140), "teal_dark": (130, 40, 90)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    key, dark = ("teal", "teal_dark") if x else ("green", "green_dark")
    HIDE = skin(P, key, dark=dark, var=0.04)

    def stripedf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("east", "west", "up") and abs(((z + y * 0.6) % 4.0) - 2.0) < 0.5:
            return tone(p["black"] if x else p["stripe"], face), None
        return HIDE(xx, y, z, face, variant, box=box, **k)

    def headf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("east", "west"):
            c = eye(p, z + 11.0, y - 13.0, 1.2, "eye")
            if c is not None:
                return c, None
        return stripedf(xx, y, z, face, variant, box=box, **k)

    def finf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(xx, y, z, face, box)
        t = v / max(H, 1e-6)
        c = mix(p["fin_root"], p["fin"], min(1, t * 1.6)) if x else mix(p["fin"], p["fin_tip"], t)
        if (u * 0.8) % 1.6 < 0.2:
            c = mix(c, (0, 0, 0), 0.25)
        return tone(c, face), None

    def fin_shape(xx, y, z, face, box):
        u, v, W, H = local(xx, y, z, face, box)
        t = u / max(W, 1e-6)
        return v / max(H, 1e-6) < 0.25 + 0.75 * (1 - t) ** 0.6

    def build():
        m = Model(name)
        mats = {"skin": stripedf, "belly": skin(P, key, dark=dark), "neck": stripedf, "head": headf, "snout": HIDE,
                "jaw": HIDE, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": HIDE,
                "leg_lower": HIDE, "paw": HIDE, "claw": metal(P, "violet" if x else "claw", dark="claw_dark"),
                "tail": stripedf}
        a = quadruped(m, mats, name, length=16.0, body_y=8.0, body_rx=6.0, body_ry=4.6, chest_bulk=1.1,
                      neck=((0, 9, -9), (0, 10, -10)), head_len=8.0, head_w=4.6, head_h=4.4, snout=0.3,
                      mouth_open=8, teeth=2, leg_len=6.0, leg_bulk=1.2, toes=2,
                      tail=((0, 8, 10), (0, 7, 13)), tail_r=(1.4, 1.0))
        hd = a["head"]
        fb = m.bone("cap", hd, (0, 14, -10))                     # tall fin crest from brow to back
        m.box(fb, 0, 13.0, -12.0, 0, 26.0, 8.0, cutout(fin_shape, finf))
        if x:
            bd = a["body"]
            for sx in (-1, 1):
                for j in range(3):
                    spike(m, bd, (sx * 6.0, 10.0, -6.0 + j * 5.0), (sx, 0.4, 0.2), 1.0, 2.4, solid(P, "spike"))
                spike(m, hd, (sx * 4.4, 11.0, -12.0), (sx, 0.2, -0.3), 1.2, 3.0, solid(P, "violet"))
        return m
    return build


build = make("betamon")
