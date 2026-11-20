"""Frigid Crest (Ice/Fairy), the ancient paradox Articuno, built from boxes after the art the user shared (the art's
own name; artist not named).

A long-legged feathered raptor: a blue body with a pale icy breast and violet lightning streaks down its flanks, a long
upright neck fringed with icy white feathers, and a small head with a hooked grey beak opening on a red mouth, a black
mask over its yellow, red-rimmed eyes, and a great swept-back crest of dark violet with a black tip. Its short arms
end in grey clawed hands under fringes of icy feathers, its legs are dark grey and scaly with white talons, and from
its hips rises an enormous dark violet plume that loops up over its back and falls to the ground.

Shiny: white plumage with a deep teal crest and plume.

Front is -z, y is up. 48 units tall; about 2.0 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import plane, scales, solid as dsolid
from _route import mix
from _pgen1 import CLEAR, ribbon, smooth_path, tri
from _regi import ellipsoid
from _route import pal, tone

HEIGHT = 48
SCALE = round(2.0 * 16 / HEIGHT, 3)
HITBOX = [1.4, HEIGHT / 16]
KIND = "biped"
K = 3
LOOK = ("a long-legged blue feathered raptor with an icy breast, a black-masked head with a hooked beak and a huge "
        "swept-back violet crest, icy feather fringes and an enormous looping violet plume of a tail")

BASE = {"blue": (98, 166, 228), "blue_dark": (60, 112, 186), "blue_light": (150, 204, 246), "belly": (214, 232, 242),
        "belly_dark": (170, 196, 214), "ice": (232, 246, 252), "ice_dark": (170, 214, 236), "violet": (70, 60, 124),
        "violet_dark": (42, 36, 84), "violet_light": (104, 94, 164), "black": (28, 28, 34), "grey": (110, 110, 122),
        "grey_dark": (76, 76, 88), "leg": (84, 84, 96), "leg_dark": (56, 56, 66), "talon": (240, 240, 244),
        "mouth": (176, 52, 66), "tongue": (226, 120, 130), "eye": (250, 222, 70), "eye_rim": (200, 40, 60)}
SHINY = {"blue": (226, 232, 242), "blue_dark": (172, 184, 204), "blue_light": (246, 250, 255), "belly": (190, 226, 246),
         "belly_dark": (140, 190, 222), "violet": (28, 98, 112), "violet_dark": (16, 62, 74), "violet_light": (60, 140,
                                                                                                          152)}
NECK_TOP = (0, 40.5, -4.6)
HEAD_LEN, HEAD_W, HEAD_H = 7.0, 2.6, 3.2


def P(v):
    return pal(BASE, SHINY, v)


def soft_feathers(key, dark, light=None, w=1.6, h=1.4):
    """Soft overlapping feather rows: a gentle darker curve at each feather's lower edge, lighter tops."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        a, b = plane(x, y, z, face)
        row = math.floor(b / h)
        aa = a + (w * 0.5 if row % 2 else 0)
        lu = ((aa / w) % 1.0) * 2 - 1
        lv = (b / h) % 1.0
        edge = lv < 0.22 + 0.18 * lu * lu
        c = mix(p[key], p[dark], 0.45) if edge else p[key]
        if light and lv > 0.8 and not edge:
            c = mix(c, p[light], 0.35)
        return tone(c, face), None
    return s


FEATHER = soft_feathers("blue", "blue_dark", "blue_light")
BELLY = soft_feathers("belly", "belly_dark", None, w=1.8, h=1.2)
LEG = scales(P, "leg", "leg_dark", size=1.0, rim_mix=0.5)
ICE = dsolid(P, "ice")


def bodyf(x, y, z, face, variant, box=None, **k):
    """Feathered blue, a pale breast on the front, violet lightning streaks down the flanks."""
    p = P(variant)
    if face in ("east", "west"):
        zig = 24.5 + 1.6 * (tri(z / 3.0) - 0.5) + 0.12 * z
        if abs(y - zig) < 0.45 and -2 < z < 8:
            return tone(p["violet"], face), None
    if (face == "north" and y < 31) or (face in ("east", "west") and z < -3.0 and 21 < y < 30):
        if abs(x) < 3.4:
            return BELLY(x, y, z, face, variant, box=box, **k)
    return FEATHER(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    """Blue, a black mask band through the eyes running back to a point; yellow eyes rimmed red."""
    p = P(variant)
    ey, ez = 41.8, -5.0
    if face in ("east", "west"):
        r = math.hypot(z - ez, y - ey)
        if r < 0.55:
            return p["eye"], None
        if r < 0.85:
            return p["eye_rim"], None
        if abs(y - (ey + 0.1 - 0.12 * (z - ez))) < 0.85:
            return p["black"], None
    if face == "north" and abs(y - ey) < 0.8:
        return p["black"], None
    return FEATHER(x, y, z, face, variant, box=box, **k)


def plumef(x, y, z, face, variant, **k):
    """Dark violet plume with long lighter streaks along it (rods: y runs across the ribbon)."""
    p = P(variant)
    yy = y % 1.7
    if face in ("east", "west"):
        if yy < 0.28:
            return tone(p["violet_light"], face), None
        if yy > 1.45:
            return tone(p["violet_dark"], face), None
    return tone(p["violet"], face), None


def crestf(x, y, z, face, variant, **k):
    p = P(variant)
    if z > 2.4:
        return tone(p["black"], face), None
    return tone(p["violet_light"] if face == "up" else p["violet"], face), None


def fringe(base_y, length, teeth, back=False):
    """A hanging fringe of icy feathers cut into points (a zy plane: z along it, hanging down from base_y)."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        z0, L = box.lo[2], box.size[2]
        f = (z - z0) / max(L, 0.01)
        depth = length * (0.45 + 0.55 * tri(f * teeth + 0.5)) * (0.6 + 0.4 * (f if back else 1 - f))
        if base_y - y > depth:
            return CLEAR
        c = p["ice"] if base_y - y > depth * 0.35 else p["blue_light"]
        return c, None
    return s


def build() -> Model:
    m = Model("frigidcrest")
    top = m.bone("frigidcrest", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 24, 1))
    ellipsoid(m, bd, 0, 24.2, 1.6, 4.0, 4.6, 6.4, bodyf, step=1)                     # the compact feathered body
    nk = m.bone("neck", bd, (0, 27, -3.4))
    neck = smooth_path([(0, 26.5, -3.0), (0, 30.5, -4.8), (0, 35.0, -4.8), (0, 39.4, -3.8)], 6)
    ribbon(m, nk, neck, [3.4, 3.2, 3.0, 2.9, 2.8, 2.7, 2.6], bodyf, extend=1.0)
    for i in range(5):                                                         # icy fringe down the back of the neck
        f = i / 4
        q = neck[1 + i]
        for sx in (-0.5, 0.5):
            spike(m, nk, (sx, q[1], q[2] + 1.0), (sx * 0.5, -0.3, 1), 1.0, 2.4 + 0.8 * (1 - f), ICE, tip=0.5)
    hd = m.bone("head", nk, (0, 40, -3.8))
    m.round_box(hd, 0, -4.0, 2.2, 2.6, 39.4, 43.4, headf, cut=1)                   # small head
    rod(m, hd, (0, 41.6, -6.2), (0, 40.4, -9.6), 1.8, dsolid(P, "grey"), extend=0.4, t2=1.8)    # hooked upper beak
    spike(m, hd, (0, 40.6, -9.4), (0, -1, -0.3), 1.2, 1.6, dsolid(P, "grey_dark"))
    rod(m, hd, (0, 39.8, -6.0), (0, 38.6, -8.6), 1.4, dsolid(P, "grey_dark"), extend=0.3, t2=1.0)  # open lower jaw
    m.box(hd, -0.6, 39.0, -8.2, 0.6, 40.8, -6.0, dsolid(P, "mouth"))
    rod(m, hd, (0, 41.8, -6.0), (0, 43.8, -5.2), 1.8, dsolid(P, "grey"), extend=0.4)            # grey casque
    z = -6.0                                                                    # the great swept-back crest
    while z < 6.6:
        f = max(0.0, (z + 6.0) / 12.6)
        hi = 43.4 + 1.0 + 3.0 * min(1.0, f / 0.28) - max(0.0, f - 0.28) * 2.4
        lo = 42.6 + 2.0 * f ** 1.5
        w = 2.8 - 1.6 * f
        m.box(hd, -w / 2, lo, z, w / 2, hi, z + 1.3, crestf)
        z += 1.2
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                       # short arms with clawed hands
        ar = m.bone(nm, bd, (sx * 3.2, 25.6, -3.6))
        el, hand = (sx * 4.2, 22.8, -5.0), (sx * 3.8, 21.6, -7.2)
        rod(m, ar, (sx * 3.2, 25.6, -3.6), el, 2.0, FEATHER, extend=0.6)
        rod(m, ar, el, hand, 1.6, FEATHER, extend=0.5)
        m.box(ar, hand[0] - 0.8, hand[1] - 1.2, hand[2] - 1.0, hand[0] + 0.8, hand[1] + 0.6, hand[2] + 0.6,
              dsolid(P, "grey_dark"))
        for fx in (-0.5, 0.0, 0.5):
            spike(m, ar, (hand[0] + fx, hand[1] - 0.6, hand[2] - 0.8), (0, -0.7, -1), 0.6, 1.8, dsolid(P, "talon"))
        m.box(ar, el[0], el[1] - 3.6, el[2] - 1.0, el[0], el[1] + 0.4, el[2] + 3.2, fringe(el[1] + 0.4, 3.2, 4))
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):                        # bird legs: thigh, shank, foot
        lg = m.bone(nm, bd, (sx * 2.6, 21, 2.4))
        m.round_box(lg, sx * 2.6, 2.2, 1.9, 2.2, 16.4, 22.0, FEATHER, cut=1)        # feathered drumstick
        knee, ank = (sx * 2.8, 16.2, 0.6), (sx * 2.9, 7.4, 3.0)
        rod(m, lg, (sx * 2.7, 17.4, 1.8), knee, 1.8, LEG, extend=0.5)
        rod(m, lg, knee, ank, 1.6, LEG, extend=0.5)
        rod(m, lg, ank, (sx * 2.9, 1.2, 0.6), 1.4, LEG, extend=0.5)
        m.box(lg, sx * 2.9 - 1.2, 0, -0.8, sx * 2.9 + 1.2, 1.6, 1.6, LEG)
        for d in ((-0.45, 0, -1), (0, 0, -1), (0.45, 0, -1)):
            rod(m, lg, (sx * 2.9 + d[0] * 0.8, 0.8, -0.6), (sx * 2.9 + d[0] * 2.4, 0.8, -3.0), 0.9, LEG, extend=0.3)
            spike(m, lg, (sx * 2.9 + d[0] * 2.6, 1.0, -3.0), (d[0] * 0.3, -0.5, -1), 0.9, 1.8, dsolid(P, "talon"),
                  tip=0.4)
        spike(m, lg, (sx * 2.9, 1.0, 1.6), (0, -0.3, 1), 0.8, 1.6, dsolid(P, "talon"))
    for sx in (-1, 1):                                                         # icy tufts on the hips and back
        spike(m, bd, (sx * 3.2, 24.5, 6.4), (sx * 0.5, -0.1, 1), 1.4, 3.2, ICE, tip=0.6)
        spike(m, bd, (sx * 2.8, 22.6, 7.2), (sx * 0.5, -0.5, 1), 1.2, 2.8, ICE, tip=0.5)
    # the enormous plume: back and up from the rump, over in a loop, and down to the ground behind
    tl = m.bone("tail", bd, (0, 24.5, 7.6))
    path = smooth_path([(0, 24.5, 7.4), (0, 26.5, 13.0), (0, 31.0, 19.0), (0, 38.0, 22.5), (0, 43.5, 20.5),
                        (0, 43.0, 15.5), (1.6, 38.0, 12.8), (2.6, 30.0, 12.2), (2.6, 20.0, 12.4), (2.2, 10.0, 12.0),
                        (1.6, 3.0, 11.0)], 22)
    for i, (p0, p1) in enumerate(zip(path, path[1:])):
        f = i / (len(path) - 1)
        w = 3.0 + 3.6 * math.sin(math.pi * min(1.0, f * 1.4)) if f < 0.7 else 3.2 * (1 - f) / 0.3 + 0.8
        rod(m, tl, p0, p1, 3.4 if f < 0.75 else 2.4, plumef, extend=0.8, t2=max(1.6, w))
    return m
