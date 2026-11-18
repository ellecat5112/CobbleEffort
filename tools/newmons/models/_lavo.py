"""Shared builder for Lavorvomon and Lavogaritamon (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the lava rock dragons: black volcanic rock plates split by glowing orange magma cracks, yellow horns and
claws, ash smoke. Lavorvomon = a low four-legged rock dragon with a horned head and a hooked yellow tail tip.
Lavogaritamon = an upright rock bird-dragon with vast spiky black wings tipped with fire, flaming talons and a long
spiked tail. Shiny: blue magma.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing, quadruped, theropod
from _digidetail import cutout, flame_inside, local, solid
from _route import pal, tone

BASE = {"rock": (50, 46, 50), "rock_dark": (18, 16, 20), "rock_light": (100, 94, 98), "magma": (255, 120, 30),
        "magma_light": (255, 220, 120), "yellow": (250, 200, 50), "yellow_dark": (190, 130, 20), "eye": (250, 200, 40),
        "mouth": (180, 40, 30), "tooth": (250, 230, 200), "fire": (255, 150, 40, 210), "fire_core": (255, 240, 180, 240)}
SHINY = {"magma": (60, 160, 255), "magma_light": (190, 230, 255), "fire": (90, 170, 255, 210)}


def P(v):
    return pal(BASE, SHINY, v)


def rockf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    cell = math.sin(x * 1.3 + y * 0.7) + math.sin(y * 1.1 - z * 0.9) + math.sin(z * 1.2 + x * 0.5)
    if abs(cell) < 0.18:
        return tone(p["magma_light"], face), p["magma"]
    if abs(cell) < 0.32:
        return tone(p["magma"], face), p["magma"]
    return tone(p["rock_light"] if face == "up" else p["rock"], face), None


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


FIRE = cutout(flame_inside(4, 0.1, 6), firef)
CLAW = solid(P, "yellow")


def make(name, bird=False):
    def build():
        m = Model(name)
        if not bird:
            mats = {"skin": rockf, "belly": rockf, "neck": rockf, "head": rockf, "snout": rockf, "jaw": rockf,
                    "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": rockf, "leg_lower": rockf,
                    "paw": rockf, "claw": CLAW, "tail": rockf}
            a = quadruped(m, mats, name, length=26.0, body_y=13.0, body_rx=5.4, body_ry=5.0, chest_bulk=1.3,
                          neck=((0, 17, -12), (0, 19, -15)), head_len=9.0, head_w=3.6, head_h=3.8, snout=0.7,
                          mouth_open=12, teeth=4, leg_bulk=1.3, toes=3,
                          tail=((0, 14, 13), (0, 14, 19), (0, 17, 24), (0, 22, 26)), tail_r=(2.4, 1.8, 1.2, 1.0))
            bd, hd = a["body"], a["head"]
            ex, ey, ez = a["eye"]
            for sx in (-1, 1):
                m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.4,
                      ez + 0.8, solid(P, "eye", glow=True))
                for j in range(2):
                    spike(m, hd, (sx * 2.0, ey + 1.6, ez + 1.0 + j * 2.4), (sx * 0.4, 1, 0.5), 1.4, 4.0 - j, CLAW, tip=0.8)
            for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
                w = a[nm]["wrist"]
                for j in range(3):
                    spike(m, a[nm]["bone"], (w[0] + (j - 1) * 1.4, 1.0, w[2] - 2.4), (0, -0.3, -1), 1.2, 3.6, CLAW, tip=0.8)
            for i in range(7):
                spike(m, bd, (0, 18.0, -9.0 + i * 3.0), (0.2 * (i % 2), 1, 0.4), 1.4, 3.0, rockf, tip=0.8)
            spike(m, a["tail"], a["tail_pts"][-1], (0, 1, -0.4), 1.6, 4.0, CLAW, tip=0.8)
            for j in range(3):
                for rot in (0, 90):
                    m.box(bd, -1.6 + j * 1.0, 18.0, -4.0 + j * 6.0, 1.6 + j * 1.0, 24.0, -4.0 + j * 6.0, FIRE,
                          rotation=(0, rot, 0), pivot=(j * 1.0, 18.0, -4.0 + j * 6.0))
            return m
        mats = {"skin": rockf, "belly": rockf, "neck": rockf, "head": rockf, "snout": rockf, "jaw": rockf,
                "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": rockf, "hand": rockf, "claw": CLAW,
                "thigh": rockf, "shin": rockf, "foot": rockf, "talon": CLAW, "tail": rockf, "tail_tip": rockf}
        a = theropod(m, mats, name, hip_y=18.0, chest=(0, 28.0, -3.0), body_r=4.6, chest_r=5.0, neck_top=(0, 36.0, -7.0),
                     head_len=8.0, head_w=3.0, head_h=3.4, mouth_open=20, teeth=4, arm_len=6.0, arm_bulk=0.8,
                     leg_bulk=1.1, stance=4.0, tail=((0, 16, 8), (0, 12, 15), (0, 9, 22), (0, 8, 29)),
                     tail_r=(2.4, 1.8, 1.2, 0.9))
        bd, hd = a["body"], a["head"]
        ex, ey, ez = a["eye"]
        for sx in (-1, 1):
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.8,
                  solid(P, "eye", glow=True))
        for side in (1, -1):                                                         # vast spiky wings, fire tips
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 31.0, 1.0))
            feather_wing(m, wb, (side * 3.0, 31.0, 1.0), 26.0, 12.0, 3, rockf, side=side, sweep=10, droop=14.0)
            for j in range(4):
                tip = (side * (12.0 + j * 4.0), 44.0 - j * 2.0, 3.0)
                for rot in (0, 90):
                    m.box(wb, tip[0] - 1.6, tip[1], tip[2], tip[0] + 1.6, tip[1] + 5.0, tip[2], FIRE, rotation=(0, rot, 0),
                          pivot=tip)
        for p in a["tail_pts"][1:]:
            spike(m, a["tail"], p, (0, 1, 0.4), 1.0, 2.4, CLAW, tip=0.8)
        for nm in ("leg_left", "leg_right"):                                         # flaming talons
            ank = a[nm]["ankle"]
            for rot in (0, 90):
                m.box(a[nm]["bone"], ank[0] - 2.0, 0.0, ank[2] - 2.0, ank[0] + 2.0, 5.0, ank[2] - 2.0, FIRE, rotation=(0, rot, 0),
                      pivot=(ank[0], 0.0, ank[2] - 2.0))
        return m

    return build
