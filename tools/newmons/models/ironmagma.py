"""Iron Magma (Steel/Fire), the future paradox Groudon, built from boxes after Cupnoodlez's art (the art's own name).

A robot Groudon crouched on thick legs: red armour plates veined with glowing yellow magma, a dark navy belly and
inner limbs, and round navy ports ringed in glowing yellow at its shoulders and hips. A crown of red spikes rises
over a glowing yellow visor on its head, dark navy spikes run down its back and its long armoured tail, and its
hands and feet end in pale icy-blue crystal claws.

Shiny: steel-grey plates with cyan magma.

Front is -z, y is up. 40 units tall; about 3.4 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import theropod
from _regi import ellipsoid
from _route import pal, tone

HEIGHT = 40
SCALE = round(3.4 * 16 / HEIGHT, 3)
HITBOX = [2.6, HEIGHT / 16]
KIND = "biped"
K = 3
LOOK = ("a crouching robot Groudon of red armour veined with glowing magma, a navy belly, glowing ringed ports, a "
        "crown of red spikes over a glowing visor, navy back spikes and icy-blue crystal claws")

BASE = {"red": (232, 72, 62), "red_dark": (176, 46, 42), "red_light": (250, 118, 96), "navy": (40, 44, 96),
        "navy_light": (70, 76, 140), "magma": (255, 222, 96), "magma_light": (255, 246, 190), "ice": (186, 214, 236),
        "ice_light": (230, 244, 252), "black": (30, 28, 36)}
SHINY = {"red": (150, 156, 172), "red_dark": (104, 110, 128), "red_light": (196, 202, 216), "magma": (90, 230, 255),
         "magma_light": (200, 250, 255)}
HIP_Y = 15.0
NECK_TOP = (0, 31.0, -6.0)


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def armourf(x, y, z, face, variant, **k):
    """Red armour veined with glowing yellow magma cracks."""
    p = P(variant)
    a, b = {"north": (x, y), "south": (-x, y), "east": (z, y), "west": (-z, y)}.get(face, (x, z))
    crack = abs(math.sin(a * 0.42 + math.sin(b * 0.33) * 1.7)) < 0.13 or abs(math.sin(b * 0.38 + a * 0.12 + 1.3)) < 0.07
    if crack:
        return p["magma"], p["magma"]
    return tone(p["red_light"] if face == "up" else p["red"], face), None


def bellyf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["navy"], face), None


def headf(x, y, z, face, variant, **k):
    """Red armour with a glowing yellow visor band across the eyes."""
    p = P(variant)
    if face in ("north", "east", "west") and abs(y - (NECK_TOP[1] + 2.2)) < 0.5 and z < NECK_TOP[2] - 0.5:
        return p["magma"], p["magma"]
    return armourf(x, y, z, face, variant)


def portf(axis):
    """A round navy port ringed in glowing yellow (on the face named by axis)."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in axis:
            cx = box.lo[0] + box.size[0] / 2
            cy = box.lo[1] + box.size[1] / 2
            cz = box.lo[2] + box.size[2] / 2
            a = (z - cz) if face in ("east", "west") else (x - cx)
            r = math.hypot(a, y - cy)
            R = min(box.size[1], box.size[2] if face in ("east", "west") else box.size[0]) / 2
            if R * 0.6 < r < R * 0.85:
                return p["magma"], p["magma"]
        return tone(p["navy"], face), None
    return s


def build() -> Model:
    m = Model("ironmagma")
    mats = {"skin": armourf, "belly": bellyf, "neck": armourf, "head": headf, "snout": armourf, "jaw": armourf,
            "mouth": solid("black"), "tooth": solid("ice_light"), "tongue": solid("navy"), "arm": armourf,
            "hand": armourf, "claw": solid("ice"), "thigh": armourf, "shin": armourf, "foot": armourf,
            "talon": solid("ice"), "tail": armourf, "tail_tip": armourf}
    a = theropod(m, mats, "ironmagma", hip_y=HIP_Y, hip_z=3.0, chest=(0, 25.0, -2.6), body_r=8.0, chest_r=7.4,
                 neck_top=NECK_TOP, head_len=9.0, head_w=4.4, head_h=5.0, mouth_open=12, teeth=4, arm_len=9.0,
                 arm_bulk=1.6, fingers=3, leg_bulk=1.8, toes=3, stance=6.0,
                 tail=((0, 14.0, 12.0), (0, 10.0, 19.0), (0, 7.0, 26.0), (0, 5.0, 33.0)),
                 tail_r=(5.6, 4.4, 3.0, 1.8))
    bd, hd, tl = a["body"], a["head"], a["tail"]
    top = a["skull_top"]
    for i, (dx, h) in enumerate(((-2.4, 4.6), (-0.8, 6.0), (0.8, 6.0), (2.4, 4.6))):   # crown of red spikes
        spike(m, hd, (dx, top - 0.2, NECK_TOP[2] - 1.0), (dx * 0.12, 1, 0.3), 1.8, h, armourf, tip=0.8)
    for i in range(6):                                                             # navy spikes down its back
        y, z = 30.0 - i * 2.6, -1.0 + i * 2.6
        spike(m, bd, (0, y, z + 6.0), (0, 0.8, 1), 2.2, 4.6 - i * 0.2, solid("navy"), tip=0.8)
    for i, q in enumerate(a["tail_pts"][1:4]):                                     # and its tail
        spike(m, tl, (q[0], q[1] + 2.4 - i * 0.6, q[2]), (0, 1, 0.7), 2.0 - i * 0.3, 4.4 - i * 0.6, solid("navy"),
              tip=0.7)
    for sx in (-1, 1):                                                             # glowing ringed ports
        x0, x1 = sorted((sx * 7.4, sx * 8.6))
        m.box(bd, x0, 21.0, -5.0, x1, 26.0, 0.0, portf(("east", "west")))
        leg = a["leg_left" if sx > 0 else "leg_right"]
        x0, x1 = sorted((sx * 8.2, sx * 9.2))
        m.box(leg["bone"], x0, HIP_Y - 4.0, 0.0, x1, HIP_Y + 1.0, 5.0, portf(("east", "west")))
    return m
