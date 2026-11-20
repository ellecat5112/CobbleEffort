"""Iron Epoch (Steel/Electric), the future paradox Dialga, built from boxes after the art the user shared (artist and
name not given; our name).

A Dialga of rose-pink alloy plated in gleaming white, standing before a great translucent dial that hangs at its
back like a clock face, ringed and ticked in pink. Shards of pink crystal burst out from the dial's centre, and
lilac and blue lightning crackles from its rim. White crest blades sweep back from its head, a pink core glows in the
white frame on its chest, and its lower legs are sheathed in crystals of pink, orange, violet and blue.

Shiny: a silver body before a golden dial.

Front is -z, y is up. 60 units tall (to its lightning); about 6.0 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _dialga import BODY_Y, dialga
from _pgen1 import CLEAR, tri
from _regi import _hash, lit
from _route import mix, pal, tone

HEIGHT = 60
SCALE = round(6.0 * 16 / HEIGHT, 3)
HITBOX = [3.0, HEIGHT / 16]
KIND = "quadruped"
K = 3
LOOK = ("a rose-pink and white robot Dialga before a great translucent clock dial bursting with pink crystal shards "
        "and crackling lightning, its lower legs sheathed in many-coloured crystals")

BASE = {"pink": (232, 168, 198), "pink_dark": (186, 112, 152), "mauve": (160, 146, 186), "white": (246, 244, 252),
        "white_dark": (200, 198, 220), "core": (255, 220, 240), "core_rim": (250, 120, 180), "eye": (200, 30, 70),
        "dial": (255, 206, 230, 110), "dial_ring": (250, 130, 186, 220), "dial_tick": (255, 255, 255, 230),
        "shard": (240, 96, 160), "shard_light": (255, 190, 220), "bolt": (196, 176, 255), "bolt_blue": (150, 210, 255),
        "c_pink": (244, 120, 176), "c_orange": (250, 176, 96), "c_violet": (176, 120, 226), "c_blue": (120, 166, 244)}
SHINY = {"pink": (196, 200, 214), "pink_dark": (140, 146, 166), "mauve": (110, 116, 140), "core_rim": (255, 196, 70),
         "dial": (255, 230, 150, 110), "dial_ring": (240, 180, 50, 220), "shard": (240, 170, 40),
         "shard_light": (255, 230, 150)}
DC = (0.0, 37.0)        # the dial's centre (x, y)
DZ = 8.0                # its plane
DR = 15.0               # its radius
RAYS = [(a, 4.0 + 5.0 * _hash(i, 7) % 1.0) for i, a in enumerate((20, 62, 105, 150, 200, 238, 290, 330))]


def P(v):
    return pal(BASE, SHINY, v)


def pinkf(x, y, z, face, variant, **k):
    p = P(variant)
    return lit(p["pink"], face, y, BODY_Y, 10), None


def whitef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        return p["white"], None
    return tone(p["white"] if face != "down" else p["white_dark"], face), None


def thighf(x, y, z, face, variant, **k):
    """Upper legs: pink, plated white down their fronts."""
    if face == "north":
        return whitef(x, y, z, face, variant)
    return pinkf(x, y, z, face, variant)


def bellyf(x, y, z, face, variant, **k):
    return tone(P(variant)["mauve"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(z + 18.6, y - (BODY_Y + 26.4)) < 0.9:
        return p["eye"], p["eye"]
    if y > BODY_Y + 26.0:
        return whitef(x, y, z, face, variant)
    return pinkf(x, y, z, face, variant)


def coref(x, y, z, face, variant, **k):
    p = P(variant)
    r = math.hypot(x, (y - BODY_Y - 0.4) * 0.75)
    c = p["core"] if r < 1.6 else p["core_rim"]
    return c, c


def crystalf(x, y, z, face, variant, **k):
    """Many-coloured crystal: facets of pink, orange, violet and blue, lighter on their tops."""
    p = P(variant)
    i = int(_hash(math.floor(x * 0.7), math.floor(y * 0.5), math.floor(z * 0.7)) * 4) % 4
    c = p[("c_pink", "c_orange", "c_violet", "c_blue")[i]]
    if face == "up":
        c = mix(c, (255, 255, 255), 0.35)
    return tone(c, face), None


def dialf(x, y, z, face, variant, **k):
    """The dial: a translucent pink disc with rings and twelve ticks, and jagged lightning rays beyond its rim."""
    p = P(variant)
    dx, dy = x - DC[0], y - DC[1]
    r = math.hypot(dx, dy)
    a = math.degrees(math.atan2(dy, dx)) % 360
    if r <= DR:
        if abs(r - DR) < 0.6 or abs(r - DR * 0.62) < 0.35 or abs(r - DR * 0.3) < 0.3:
            return p["dial_ring"], p["dial_ring"]
        if r > DR * 0.8 and min(abs(a - t * 30) for t in range(13)) * math.pi / 180 * r < 0.45:
            return p["dial_tick"], p["dial_tick"]
        return p["dial"], None
    for ang, extra in RAYS:
        da = math.radians(ang)
        along = dx * math.cos(da) + dy * math.sin(da)
        across = -dx * math.sin(da) + dy * math.cos(da)
        if DR - 0.5 < along < DR + 5.0 + extra * 1.3:
            zig = (tri((along - DR) / 3.2) - 0.5) * 3.2
            if abs(across - zig) < 0.6:
                c = mix(p["bolt"], p["bolt_blue"], (along - DR) / (5.0 + extra * 1.3))
                return c, c
    return CLEAR


def shardf(x, y, z, face, variant, box=None, **k):
    """A crystal shard: pink, lighter along one edge (rods: x across)."""
    p = P(variant)
    if x > box.lo[0] + box.size[0] * 0.6 or face == "up":
        return p["shard_light"], None
    return tone(p["shard"], face), None


def build() -> Model:
    m = Model("ironepoch")
    mats = {"skin": pinkf, "belly": bellyf, "neck": pinkf, "head": headf, "crest": whitef, "armour": whitef,
            "plate": whitef, "leg_upper": thighf, "leg_lower": whitef, "foot": whitef, "claw": whitef,
            "tail": pinkf, "core": coref}
    a = dialga(m, mats, "ironepoch")
    bd = a["body"]
    dial = m.bone("cap", bd, (DC[0], DC[1], DZ))                                    # the dial at its back
    R = DR + 11.0
    m.box(dial, DC[0] - R, DC[1] - R + 6.0, DZ, DC[0] + R, min(DC[1] + R, 60.0), DZ, dialf)
    for i in range(10):                                                           # crystal shards from its centre
        ang = math.radians(i * 36 + 12)
        L = 9.0 + 4.0 * (i % 3)
        root = (DC[0] + math.cos(ang) * 1.5, DC[1] + math.sin(ang) * 1.5, DZ - 0.6)
        d = (math.cos(ang), math.sin(ang), -0.35)
        spike(m, dial, root, d, 2.2, L, shardf, tip=1.0)
    m.box(dial, DC[0] - 1.6, DC[1] - 1.6, DZ - 1.2, DC[0] + 1.6, DC[1] + 1.6, DZ + 0.6, coref)
    for nm, leg in a["legs"].items():                                               # crystal-sheathed lower legs
        ft = leg["foot"]
        sx = 1 if ft[0] > 0 else -1
        for j, (dx, dz, h) in enumerate(((1.0, -0.6, 7.0), (0.2, -1.2, 9.0), (-0.8, -0.4, 6.0), (0.4, 1.0, 5.0))):
            base = (ft[0] + sx * dx * 1.2, 9.0 - j * 0.6, ft[2] + dz * 1.2)
            spike(m, leg["bone"], base, (sx * dx * 0.35, -1, dz * 0.4), 2.6, h, crystalf, tip=1.2)
    hd = a["head"]
    for sx in (-1, 1):                                                            # white crest blades swept back
        spike(m, hd, (sx * 2.4, BODY_Y + 27.6, -15.0), (sx * 0.45, 0.5, 1), 1.4, 9.0, whitef, tip=0.8)
    return m
