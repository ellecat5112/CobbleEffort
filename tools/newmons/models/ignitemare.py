"""Ignitemare, the Hollow Steed Pokémon (Dark/Fire), the CobbleEffort Mudbray evolved, built from boxes after the
fakemon art by @wescos_region that the user shared (the art's own name), with the user's idea: an almost wendigo-like
fire and dark creature.

A gaunt, towering horse of shadow: a dark navy body with its white ribs and spine showing through as bone plates and
spikes, a long bare horse skull for a head with glowing red eyes in hollow sockets, short branching horns with black
tips, fire snorting from its nostrils, a ragged dark mane with a side-swept forelock (a red streak in it: the emo
Mudbray's fringe, grown out), long thin legs cased in white bone armour split by glowing red cracks, huge white hooked
claw-hooves with black tips, and a spiky dark tail with red marks.

Shiny: charcoal with blue fire, eyes and cracks.

Front is -z, y is up. 47 units tall to the horn tips; baseScale 0.75 (2.2 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _route import pal, tone

SCALE = 0.75
HITBOX = [1.4, 2.4]
KIND = "quadruped"
K = 4
HEIGHT = 47
LOOK = ("a gaunt shadow horse with white ribs and spine showing, a bare horse skull with glowing red eyes and short "
        "black-tipped horns, fire snorting from its nostrils, bone-armoured legs split by glowing cracks and huge "
        "hooked claw-hooves")

BASE = {"body": (30, 30, 54), "body_light": (52, 52, 84), "body_dark": (16, 16, 30), "bone": (234, 230, 216),
        "bone_shade": (182, 176, 160), "tip": (22, 20, 26), "mane": (20, 18, 30), "mane_light": (44, 40, 62),
        "streak": (210, 40, 44), "crack": (236, 52, 30), "crack_core": (255, 170, 80), "eye": (255, 40, 30),
        "socket": (12, 10, 16), "fire": (250, 110, 30), "fire_core": (255, 220, 120)}
SHINY = {"body": (46, 44, 48), "body_light": (74, 72, 78), "body_dark": (24, 22, 26), "mane": (26, 26, 30),
         "mane_light": (58, 58, 66), "streak": (60, 150, 240), "crack": (50, 140, 255), "crack_core": (170, 220, 255),
         "eye": (70, 170, 255), "fire": (60, 130, 255), "fire_core": (200, 236, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "down":
        return p["body_dark"], None
    if face == "up" or y > 29.4:
        return tone(p["body_light"], face), None
    return tone(p["body"], face), None


def bonef(x, y, z, face, variant, **k):
    p = P(variant)
    c = p["bone"] if face in ("up", "north", "east", "west") else p["bone_shade"]
    return tone(c, face), None


def cracked(y, x, z):
    """True on a jagged glowing crack line: bands round the leg, kinked by position."""
    t = y * 0.62 + math.sin(z * 2.3 + x * 1.7) * 0.55 + math.sin(y * 3.1) * 0.25
    return abs((t % 2.4) - 1.2) < 0.16


def legf(x, y, z, face, variant, **k):
    """Shadow flesh with glowing cracks."""
    p = P(variant)
    if face not in ("up", "down") and cracked(y, x, z):
        return p["crack"], p["crack"]
    return tone(p["body"], face), None


def armourf(x, y, z, face, variant, **k):
    """White bone armour split by the same glowing cracks."""
    p = P(variant)
    if face not in ("up", "down") and cracked(y + 0.6, x, z):
        c = p["crack_core"] if abs(math.sin(y * 5.3)) < 0.35 else p["crack"]
        return c, c
    return bonef(x, y, z, face, variant)


def tipf(x, y, z, face, variant, **k):
    """Black horn and claw tips (separate boxes: rod shaders see the box's own axes, not the model's)."""
    return tone(P(variant)["tip"], face), None


def skullf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        d = math.hypot((z + 15.8) / 1.5, (y - 38.4) / 1.05)
        if d < 1:
            if d < 0.45:
                return p["eye"], p["eye"]                                    # glowing eyes deep in the sockets
            return p["socket"], None                                         # hollow sockets
        if -22.5 < z < -15 and abs(y - 35.9 - (z + 15) * -0.05) < 0.16:
            return p["socket"], None                                         # the skull's jawline seam
    if face == "north" and y > 36:
        for sx in (-1, 1):
            if math.hypot((x - sx * 0.85) / 0.4, (y - 37.1) / 0.55) < 1:
                return p["socket"], None                                     # nostril holes
    if face == "up" and -19 < z < -14 and abs(x) < 0.25:
        return p["bone_shade"], None                                         # suture down the brow
    return bonef(x, y, z, face, variant)


def manef(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("up", "east", "west") and math.sin(x * 2.1 + z * 1.3) > 0.55:
        return tone(p["mane_light"], face), None
    return tone(p["mane"], face), None


def forelockf(x, y, z, face, variant, **k):
    p = P(variant)
    if abs(math.sin((y + z) * 0.9)) > 0.86:
        return p["streak"], None                                              # the red streak in its fringe
    return manef(x, y, z, face, variant)


def tailf(x, y, z, face, variant, **k):
    p = P(variant)
    if face not in ("down",) and abs(((z - 10) % 2.6) - 1.3) < 0.28:
        return p["streak"], p["streak"]                                      # red marks down the tail
    return manef(x, y, z, face, variant)


def firef(cu, base_v, height, width):
    """A tongue of fire on a plane (rising along y before the plane is tilted): pale core, cut to a flame shape."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u = x - cu if face in ("north", "south") else z - cu
        t = (y - base_v) / height
        if t < 0 or t > 1:
            return (0, 0, 0, 0), None
        half = width / 2 * (1 - t) ** 0.7 * (0.55 + 0.45 * math.sin(t * 3.1 + 0.4))
        uu = u - math.sin(t * 5.2) * 0.35 * width * t
        if abs(uu) > half:
            return (0, 0, 0, 0), None
        c = p["fire_core"] if abs(uu) < half * 0.45 and t < 0.75 else p["fire"]
        return c, c
    return s


def leg(m, bone, lx, lz, back):
    """A long thin leg: shadow flesh with cracks, bone armour plates and a huge hooked claw-hoof."""
    if back:
        m.round_box(bone, lx, lz + 0.3, 1.5, 2.1, 17.5, 25, bodyf, cut=0.7)        # lean thigh
        rod(m, bone, (lx, 17, lz + 0.6), (lx, 10, lz + 2.6), 2, legf)
        m.round_box(bone, lx, lz + 2.6, 1.3, 1.3, 9, 11.4, bonef, cut=0.4)         # bony hock
        rod(m, bone, (lx, 10, lz + 2.6), (lx, 3.2, lz + 1.2), 1.8, legf)
        m.box(bone, lx - 1.15, 4, lz + 0.1, lx + 1.15, 9.2, lz + 0.8, armourf, rotation=(-11, 0, 0),
              pivot=(lx, 9, lz + 1.6))                                              # shin armour
    else:
        rod(m, bone, (lx, 25, lz), (lx, 14, lz - 0.6), 2.4, legf)
        m.round_box(bone, lx, lz - 0.6, 1.5, 1.5, 12.6, 15, bonef, cut=0.4)        # bony knee
        rod(m, bone, (lx, 13.4, lz - 0.6), (lx, 3.2, lz), 1.8, legf)
        m.box(bone, lx - 1.15, 4, lz - 1.45, lx + 1.15, 12.4, lz - 0.85, armourf)   # shin armour
        m.box(bone, lx - 1.35, 15.5, lz - 1.6, lx + 1.35, 22, lz - 1.1, armourf)   # forearm armour
    hz = lz + (1.2 if back else 0)
    m.round_box(bone, lx, hz, 1.6, 1.6, 1.4, 4.4, bonef, cut=0.5)                # hoof
    for dx in (-1.0, 0, 1.0):                                                    # three big hooked claws, black tips
        rod(m, bone, (lx + dx, 2.8, hz - 0.8), (lx + dx, 2.4, hz - 3.6), 1.1, bonef, extend=0.3)
        rod(m, bone, (lx + dx, 2.5, hz - 3.4), (lx + dx, 1.0, hz - 4.6), 0.9, bonef, extend=0.1)
        rod(m, bone, (lx + dx, 1.2, hz - 4.5), (lx + dx, 0, hz - 4.9), 0.7, tipf, extend=0.1)


def build() -> Model:
    m = Model("ignitemare")
    top = m.bone("ignitemare", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    m.round_box(bd, 0, -0.5, 3.6, 9, 22.5, 30, bodyf, cut=2)                   # gaunt body
    m.round_box(bd, 0, -6.5, 3.9, 3.4, 22, 30.6, bodyf, cut=1.4)               # chest
    for sx in (-1, 1):                                                          # ribs showing through as bone plates
        for i in range(5):
            z = -6.2 + i * 2.1
            m.box(bd, min(sx * 3.5, sx * 4.05), 23.6 + i * 0.25, z, max(sx * 3.5, sx * 4.05), 29.4, z + 0.9, bonef)
        m.box(bd, min(sx * 2.6, sx * 3.75), 26, 4.8, max(sx * 2.6, sx * 3.75), 30.4, 8.4, bonef)   # hip bones
    m.box(bd, -0.6, 29.8, -7, 0.6, 30.5, 8, bonef)                              # the spine down its back
    for i in range(7):                                                          # bone spikes along the spine
        z = -5.5 + i * 2.1
        spike(m, bd, (0, 30.2, z), (0, 1, 0.45), 1.1, 2.2 + (i % 2) * 1.0, bonef, tip=0.6)
    tl = m.bone("tail", bd, (0, 28.5, 8.6))                                     # spiky dark tail
    pts = [(0, 28.8, 8.4), (0, 27.5, 12.5), (0, 24.5, 15.5), (0, 20.5, 17.2)]
    for a, b, t in zip(pts, pts[1:], (2.2, 1.9, 1.5)):
        rod(m, tl, a, b, t, tailf, extend=0.4)
    for a, b in zip(pts, pts[1:]):
        mid = tuple((u + v) / 2 for u, v in zip(a, b))
        for sx in (-1, 1):
            spike(m, tl, mid, (sx * 1, 0.4, 0.5), 0.8, 2.2, manef)
    spike(m, tl, pts[-1], (0, -1, 0.3), 1.2, 2.5, manef, tip=0.6)

    nk = m.bone("neck", bd, (0, 29, -7.5))
    rod(m, nk, (0, 28.5, -7.5), (0, 36.5, -12), 3.4, bodyf, t2=3.8)             # long thin neck
    mn = m.bone("mane", nk, (0, 32, -9))
    for i in range(6):                                                          # a ragged dark mane of spikes
        t = i / 5
        base = (0, 30 + t * 7.2, -8.3 - t * 4.2)
        spike(m, mn, base, (0, 0.55, 1), 1.4, 3.2 + (i % 2) * 1.6, manef, tip=0.7)
        for sx in (-1, 1):
            spike(m, mn, (sx * 0.8, base[1] - 0.5, base[2] + 0.4), (sx * 0.7, 0.3, 1), 1, 2.6, manef)

    hd = m.bone("head", nk, (0, 37, -12))
    m.round_box(hd, 0, -15.6, 2.4, 3.6, 35.2, 40.2, skullf, cut=1)              # the long bare skull
    m.round_box(hd, 0, -21, 1.8, 2.8, 34.8, 37.9, skullf, cut=0.7)              # muzzle
    for sx in (-1, 1):
        m.box(hd, sx * 0.9 - 0.25, 34.3, -23.4, sx * 0.9 + 0.25, 34.9, -22.6, bonef)      # fangs
        m.box(hd, sx * 1.4 - 0.2, 34.4, -21.4, sx * 1.4 + 0.2, 34.9, -20.8, bonef)
        rod(m, hd, (sx * 1.5, 39.8, -13.6), (sx * 3, 43.2, -11.6), 1.2, bonef, extend=0.3)  # short branching horns
        rod(m, hd, (sx * 2.9, 43, -11.7), (sx * 3.25, 45.4, -12.2), 0.9, bonef, extend=0.2)
        rod(m, hd, (sx * 3.25, 45.2, -12.2), (sx * 3.45, 46.8, -12.5), 0.8, tipf, extend=0.1)
        rod(m, hd, (sx * 2.9, 43, -11.7), (sx * 4.0, 44.1, -10.4), 0.8, bonef, extend=0.2)
        rod(m, hd, (sx * 3.9, 44, -10.5), (sx * 4.7, 44.7, -9.6), 0.7, tipf, extend=0.1)
        m.box(hd, min(sx * 2.2, sx * 3.6), 39, -12.8, max(sx * 2.2, sx * 3.6), 41.6, -12.2, manef,
              rotation=(0, 0, sx * -24), pivot=(sx * 2.2, 39.5, -12.5))            # ears
    rod(m, hd, (-0.6, 40.4, -13.6), (2.4, 37.2, -16.8), 1.3, forelockf, extend=0.4, t2=2.6)   # side-swept forelock
    jw = m.bone("jaw", hd, (0, 35.2, -14))
    m.box(jw, -1.5, 33.4, -23, 1.5, 34.5, -14.5, bonef)                         # lower jaw
    m.box(jw, -1.3, 34.5, -22.6, 1.3, 34.8, -15, flatdark)                      # the dark of the mouth
    for sx in (-1, 1):                                                          # fire snorting from the nostrils
        m.box(hd, sx * 0.85, 37.2, -26.3, sx * 0.85, 44.2, -22.3, firef(-24.3, 37.2, 7, 3.6),
              rotation=(62, 0, 0), pivot=(sx * 0.85, 37.2, -24.3))
        m.box(hd, sx * 0.85 - 1.8, 37.2, -24.3, sx * 0.85 + 1.8, 44.2, -24.3, firef(sx * 0.85, 37.2, 7, 3.6),
              rotation=(62, 0, 0), pivot=(sx * 0.85, 37.2, -24.3))

    for nm, lx, lz, back in (("leg_front_left", -2.4, -6.5, False), ("leg_front_right", 2.4, -6.5, False),
                             ("leg_back_left", -2.4, 6.4, True), ("leg_back_right", 2.4, 6.4, True)):
        lg = m.bone(nm, top, (lx, 24, lz))
        leg(m, lg, lx, lz, back)
    return m


def flatdark(x, y, z, face, variant, **k):
    return P(variant)["socket"], None
