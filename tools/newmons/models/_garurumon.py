"""Shared builder for Garurumon and its variants (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a lean, powerful wolf with white fur striped blue, a shaggy mane of blade-like fur spikes along its
shoulders and back, a long curling striped tail, red-pink claws and blue fox-fire breath. Looks: "base"; "black" (black
fur striped white); "x" (the X-Antibody: lavender-grey shaggy fur, a row of great steel spikes along its back bound
with a red-striped band, steel claws); "gururu" (Gururumon: white fur striped deep blue, red eyes, violet claws).
Shiny: base <-> black; x and gururu turn golden.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _digidetail import cutout, flame_inside, fur, local, metal, solid
from _route import pal, tone

LOOKS = {"base": {"fur": (230, 234, 250), "fur_dark": (160, 170, 210), "stripe": (60, 80, 180)},
         "black": {"fur": (50, 48, 54), "fur_dark": (20, 18, 24), "stripe": (230, 230, 236)},
         "x": {"fur": (190, 190, 220), "fur_dark": (130, 130, 170), "stripe": (150, 150, 190)},
         "gururu": {"fur": (236, 238, 248), "fur_dark": (170, 176, 206), "stripe": (30, 50, 150)}}
COMMON = {"claw": (220, 90, 140), "eye": (250, 200, 40), "mouth": (130, 20, 40), "tooth": (250, 250, 246),
          "steel": (200, 206, 220), "steel_dark": (90, 96, 110), "band": (200, 30, 40), "fire": (110, 190, 255, 210),
          "fire_core": (230, 245, 255, 235)}


def make(name, look="base"):
    base = dict(COMMON, **LOOKS[look])
    if look in ("x", "gururu"):
        shiny = dict(base, fur=(240, 210, 120), fur_dark=(190, 150, 60), stripe=(170, 110, 40))
    else:
        shiny = dict(COMMON, **LOOKS["black" if look == "base" else "base"])
    if look == "gururu":
        base["eye"] = (220, 30, 40)
        base["claw"] = (110, 70, 170)
    if look == "x":
        base["claw"] = (220, 220, 200)

    def P(v):
        return pal(base, shiny, v)

    FUR0 = fur(P, "fur", "fur_dark", length=1.4, density=2.2)

    def furf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face != "down" and abs(((z * 0.45 + y * 0.25 + abs(x) * 0.15) % 3.4) - 1.7) < 0.42:
            return tone(p["stripe"], face), None
        return FUR0(x, y, z, face, variant, box=box, **k)

    def firef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p["fire_core"] if u / max(W, 1e-6) > 0.7 else p["fire"]
        return c, c[:3]

    def build():
        m = Model(name)
        mats = {"skin": furf, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "claw": solid(P, "claw")}
        a = quadruped(m, mats, name, length=30.0, body_y=17.0, body_rx=5.6, body_ry=5.4, chest_bulk=1.3,
                      neck=((0, 21, -13), (0, 24, -17)), head_len=11.0, head_w=3.4, head_h=3.8, snout=0.9,
                      mouth_open=16, teeth=6, leg_bulk=1.3, toes=4,
                      tail=((0, 20, 15), (3, 24, 20), (6, 27, 23), (8, 28, 19), (7, 25, 16)),
                      tail_r=(2.0, 1.6, 1.4, 1.2, 1.0))
        bd, hd = a["body"], a["head"]
        ex, ey, ez = a["eye"]
        for sx in (-1, 1):
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4,
                  ez + 0.6, solid(P, "eye"))
            spike(m, hd, (sx * 2.0, ey + 3.0, ez + 2.0), (sx * 0.4, 1, 0.5), 1.8, 4.0, furf, tip=0.9)   # ears
        if look == "x":                                                                  # steel back spikes
            m.round_box(bd, 0, -6.0, 6.2, 1.6, 15.0, 23.4, metal(P, "band", dark="steel_dark"), cut=1)
            for j in range(6):
                spike(m, bd, ((j % 2 - 0.5) * 2.0, 22.0, -10.0 + j * 2.6), ((j % 2 - 0.5) * 0.6, 1, -0.5), 1.8,
                      12.0 - abs(j - 2) * 1.6, metal(P, "steel", dark="steel_dark"), tip=0.9)
        else:                                                                             # blade-like fur mane
            for side in (-1, 1):
                for j in range(5):
                    spike(m, bd, (side * 4.4, 22.0, -10.0 + j * 3.0), (side * 0.6, 1, 0.4), 1.8, 7.0 - j * 0.6,
                          furf, tip=0.9)
        if look == "base":                                                                # fox-fire breath
            sf = (0, a["mouth_y"], a["snout_front"])
            for ang in (0, 90):
                m.box(hd, sf[0] - 2.0, sf[1] - 2.0, sf[2] - 7.0, sf[0] + 2.0, sf[1] + 2.0, sf[2],
                      cutout(flame_inside(3, 0.1, 6), firef), rotation=(0, 0, ang), pivot=sf)
        return m

    return build
