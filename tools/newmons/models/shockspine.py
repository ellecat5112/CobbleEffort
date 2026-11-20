"""Shock Spine (Electric/Fighting), the ancient paradox Zapdos, built from boxes after the art the user shared (the
art's own name; artist not named).

A four-legged spinosaur: a long black crocodile snout gaping on a pink mouth, a fierce red-rimmed yellow eye, and a
great ruff of spiky yellow fur round its head and neck, streaked with dark blue lightning marks like the yellow fur
of its body. A huge jagged black sail rises from its back with a darker zigzag at its heart. Black legs end in
yellow claws, a spiky yellow ruff tipped in blue bristles round its hips, and its long black tail curls up behind.

Shiny: navy hide with pale icy fur.

Front is -z, y is up. 50 units tall (to the sail's tip); about 2.6 blocks tall and 4 long.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _digidetail import fur, solid as dsolid, skin
from _pgen1 import CLEAR, inside, tri
from _route import pal, tone

HEIGHT = 50
SCALE = round(2.6 * 16 / HEIGHT, 3)
HITBOX = [3.2, HEIGHT / 16]
KIND = "quadruped"
K = 3
LOOK = ("a four-legged spinosaur with a gaping black crocodile snout, a ruff of spiky yellow fur streaked with blue "
        "lightning, a huge jagged black sail and black legs with yellow claws")

BASE = {"fur": (250, 214, 104), "fur_dark": (214, 164, 60), "fur_light": (255, 238, 160), "bolt": (40, 58, 108),
        "black": (44, 40, 42), "black_dark": (24, 22, 24), "black_light": (74, 68, 70), "claw": (224, 182, 62),
        "mouth": (200, 108, 118), "mouth_dark": (120, 40, 52), "eye": (250, 220, 70), "eye_rim": (210, 40, 46),
        "blue_tip": (36, 70, 150)}
SHINY = {"fur": (222, 238, 248), "fur_dark": (170, 196, 218), "fur_light": (246, 252, 255), "bolt": (60, 150, 220),
         "black": (34, 44, 76), "black_dark": (18, 24, 46), "black_light": (60, 74, 112), "claw": (150, 220, 250),
         "blue_tip": (90, 200, 250)}
SAIL = [(-14, 24), (-11, 40), (-6.5, 36), (-2, 50), (2, 40), (6, 47), (8.5, 38.5), (12.5, 42), (16, 24)]
W_MARK = [(-6, 32), (-4, 40), (-1, 34), (1, 41), (4, 33), (2.5, 29), (1, 33.5), (-1, 29), (-3, 35), (-4.5, 29)]


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", tip="fur_light", length=1.4, density=1.6, flow=(0, -1))
HIDE = skin(P, "black", dark="black_dark", light="black_light", var=0.08)


def upperleg(x, y, z, face, variant, **k):
    """Yellow fur where the leg meets the body, black hide below."""
    if y > 15.0:
        return bodyf(x, y, z, face, variant, **k)
    return HIDE(x, y, z, face, variant, **k)


def bodyf(x, y, z, face, variant, **k):
    """Yellow fur streaked with dark blue lightning bolts down the flanks."""
    p = P(variant)
    if face in ("east", "west", "up"):
        for c0, ph in ((22.0, 0.0), (17.0, 0.4)):
            if abs(y - (c0 + 1.4 * (tri(z / 3.2 + ph) - 0.5))) < 0.3 and -12 < z < 12 and (z % 9) < 6:
                return tone(p["bolt"], face), None
    return FUR(x, y, z, face, variant, **k)


def sailf(x, y, z, face, variant, **k):
    p = P(variant)
    if not inside(SAIL, z, y):
        return CLEAR
    if inside(W_MARK, z, y):
        return p["black_dark"], None
    lit_ = 1.0 + 0.05 * math.sin(z * 0.9 + y * 0.4)
    c = tuple(min(255, int(v * lit_)) for v in p["black"])
    return c, None


def headf(eye_y, eye_z):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("east", "west"):
            dz, dy = z - eye_z, y - eye_y
            r = math.hypot(dz * 0.7, dy)
            if r < 0.6:
                return p["eye"], None
            if r < 0.95 or (abs(dy - dz * 0.35) < 0.3 and -3.5 < dz < -0.6):
                return p["eye_rim"], None                                   # red rim + a slash forward
        return HIDE(x, y, z, face, variant, **k)
    return s


def snoutf(x, y, z, face, variant, **k):
    """Black, notched along its top edge."""
    p = P(variant)
    if face == "up" and (z % 1.8) < 0.5:
        return p["black_light"], None
    return tone(p["black"], face), None


def tuft(m, bone, base, d, w, h, tipkey="blue_tip"):
    n = math.sqrt(sum(v * v for v in d))
    u = tuple(v / n for v in d)
    mid = tuple(b + uu * h * 0.62 for b, uu in zip(base, u))
    end = tuple(b + uu * h for b, uu in zip(base, u))
    rod(m, bone, base, mid, w, FUR, extend=0.2)
    rod(m, bone, mid, end, max(0.6, w * 0.45), dsolid(P, tipkey), extend=0.2)


def build() -> Model:
    m = Model("shockspine")
    mats = {"skin": bodyf, "belly": bodyf, "neck": bodyf, "head": None, "snout": snoutf, "jaw": snoutf,
            "mouth": dsolid(P, "mouth_dark"), "tooth": dsolid(P, "claw"), "tongue": dsolid(P, "mouth"),
            "leg_upper": None, "leg_lower": HIDE, "paw": HIDE, "claw": dsolid(P, "claw"), "tail": HIDE}
    neck = ((0, 25.0, -18.0), (0, 27.5, -22.5))
    head_len, head_w, head_h = 13.5, 4.0, 5.6
    hx, hy, hz = neck[-1]
    eye_y, eye_z = hy + head_h * 0.25, hz - head_len * 0.35
    mats["head"] = headf(eye_y, eye_z)
    mats["leg_upper"] = upperleg
    a = quadruped(m, mats, "shockspine", length=30.0, body_y=18.5, body_rx=6.6, body_ry=6.8, chest_bulk=1.15,
                  neck=neck, head_len=head_len, head_w=head_w, head_h=head_h, snout=1.05, mouth_open=28, teeth=0,
                  leg_bulk=1.4, tail=((0, 23.0, 22.0), (0, 26.0, 30.0), (0, 30.0, 37.0), (0, 35.5, 42.0)),
                  tail_r=(3.6, 2.6, 1.8, 1.0), toes=3)
    bd, hd, nk = a["body"], a["head"], a["neck"]
    m.box(bd, 0, 22, -14, 0, 51, 16, sailf)                                          # the great sail
    for zz in range(-12, 15, 3):                                                     # its root along the spine
        m.box(bd, -0.8, 24.0, zz, 0.8, 26.5 + 2 * tri(zz / 6.0), zz + 3, HIDE)
    # the ruff of spiky yellow fur round the head and neck
    for i in range(14):
        ang = math.radians(-100 + i * (200 / 13))
        d = (math.sin(ang), math.cos(ang) * 0.9 + 0.15, 0.9)
        base = (d[0] * 3.2, hy + 1.0 + d[1] * 3.0, hz + 1.0)
        tuft(m, hd, base, d, 1.8, 5.2 + 1.4 * tri(i / 2.5), "fur_light")
    for i in range(10):
        ang = math.radians(-120 + i * (240 / 9))
        d = (math.sin(ang), math.cos(ang) * 0.8, 0.5)
        tuft(m, nk, (d[0] * 4.8, 23.5 + d[1] * 4.0, -16.0), d, 2.0, 5.0 + 1.6 * tri(i / 3.0), "fur_light")
    for zz in (-6.0, 0.0, 6.0):                                                     # fur tufts on the flanks
        for sx in (-1, 1):
            tuft(m, bd, (sx * 6.6, 20.5, zz), (sx, 0.4, 0.5), 1.6, 3.6, "fur_light")
    for i in range(11):                                                             # the blue-tipped hip ruff
        ang = math.radians(-110 + i * (220 / 10))
        d = (math.sin(ang), math.cos(ang) * 0.9, 1.0)
        tuft(m, bd, (d[0] * 5.8, 20.5 + d[1] * 4.8, 13.5), d, 1.8, 5.6 + 1.8 * tri(i / 2.0))
    for i, zz in enumerate((20.0, 25.0, 30.0, 34.0)):                                # notches down the tail
        spike(m, a["tail"], (0, 24.4 + i * 1.5 + (2.0 - i * 0.4), zz), (0, 1, 0.6), 1.4, 1.6, HIDE)
    return m
