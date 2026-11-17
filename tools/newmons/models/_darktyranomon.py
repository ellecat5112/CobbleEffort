"""Shared builder for Dark Tyranomon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): a dark
grey tyrannosaur striped in red with a ribbed pale belly, green leaf-like dorsal spikes, a fanged red mouth, steel claws
and a brown leather belt round its hips. make(x=True): the X-Antibody form, a crouching black tyrannosaur with glowing
red stripes, green crystal back spines, a red X scar, steel-clawed gauntlets and glowing green flames at its claws and
tail tip. Shiny: rusty brown.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import theropod
from _digidetail import cutout, flame_inside, gem, leather, local, metal, scales, skin, solid
from _route import pal, tone

BASE = {"grey": (80, 82, 92), "grey_dark": (34, 34, 40), "grey_light": (150, 152, 166), "black": (34, 32, 38),
        "black_dark": (12, 12, 16), "black_light": (90, 90, 104), "red": (200, 40, 40), "belly": (210, 210, 220),
        "belly_dark": (150, 150, 166), "green": (90, 200, 80), "green_dark": (30, 120, 40), "brown": (140, 100, 60),
        "brown_dark": (80, 50, 24), "steel": (210, 214, 226), "steel_dark": (110, 114, 128), "mouth": (180, 30, 40),
        "tooth": (250, 250, 246), "eye": (90, 160, 230), "flame": (90, 250, 180, 210), "flame_core": (220, 255, 240, 240)}
SHINY = {"grey": (150, 100, 60), "grey_dark": (90, 50, 24), "grey_light": (220, 170, 120), "black": (120, 70, 40),
         "black_dark": (60, 30, 14), "green": (230, 160, 40), "green_dark": (160, 90, 10)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    key, dark = ("black", "black_dark") if x else ("grey", "grey_dark")
    HIDE = scales(P, key, dark, size=1.6, light="grey_light", rim_mix=0.3)
    BELLY = skin(P, "belly", dark="belly_dark", var=0.03)
    STEEL = metal(P, "steel", dark="steel_dark")

    def striped(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("east", "west", "up") and (y * 0.7 + z * 0.5) % 4.0 < 0.7:
            c = p["red"]
            return (c, c) if x else (tone(c, face), None)
        return HIDE(xx, y, z, face, variant, box=box, **k)

    def flamef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(xx, y, z, face, box)
        c = p["flame_core"] if v / max(H, 1e-6) < 0.3 else p["flame"]
        return c, c[:3]

    def build():
        m = Model(name)
        mats = {"skin": striped, "belly": BELLY, "neck": striped, "head": striped, "snout": HIDE, "jaw": HIDE,
                "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": striped, "hand": HIDE, "claw": STEEL,
                "thigh": striped, "shin": HIDE, "foot": HIDE, "talon": STEEL, "tail": striped, "tail_tip": HIDE}
        a = theropod(m, mats, name, hip_y=16.0 if x else 19.0, hip_z=3.0, chest=(0, 26.0 if x else 31.0, -4.0),
                     body_r=6.6, chest_r=6.4, neck_top=(0, 30.0 if x else 38.0, -10.0 if x else -5.0), head_len=12.0,
                     head_w=4.4, head_h=4.4, mouth_open=26, teeth=6, arm_len=10.0, arm_bulk=1.3, leg_bulk=1.5,
                     stance=5.0, tail=((0, 16, 10), (2, 14, 18), (5, 16, 25), (8, 22, 30), (10, 28, 31)),
                     tail_r=(4.4, 3.4, 2.4, 1.6, 1.0))
        bd, hd = a["body"], a["head"]
        for j in range(6):                                                         # dorsal spikes
            t = j / 5
            p = (0, (30.0 if x else 37.0) - 16.0 * t, -2.0 + 12.0 * t)
            spike(m, bd, p, (0, 1, 0.4), 2.4, 3.6, gem(P, "green", "green_dark", glow=x) if x else
                  solid(P, "green"), tip=0.6)
        ex, ey, ez = a["eye"]
        for sx in (-1, 1):
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.4,
                  ez + 0.8, solid(P, "eye"))
        if not x:                                                                  # leather belt
            m.round_box(bd, 0, 3.0, 7.0, 6.0, 15.0, 18.0, leather(P, "brown", "brown_dark", stitch="steel"), cut=2)
        else:
            for nm in ("arm_left", "arm_right"):                                   # green flames at the claws
                h = a[nm]["hand"]
                for ang in (0, 90):
                    m.box(a[nm]["bone"], h[0] - 2.4, h[1], h[2] - 1.0, h[0] + 2.4, h[1] + 8.0, h[2] - 1.0,
                          cutout(flame_inside(3, 0.2, 1), flamef), rotation=(0, ang, 0), pivot=(h[0], h[1], h[2] - 1.0))
            e = a["tail_pts"][-1]
            for ang in (0, 90):
                m.box(a["tail_tip"], e[0] - 3.0, e[1], e[2], e[0] + 3.0, e[1] + 10.0, e[2],
                      cutout(flame_inside(4, 0.2, 3), flamef), rotation=(0, ang, 0), pivot=e)
        return m
    return build
