"""Iron Current (Water/Fairy), the future paradox Suicune, built from boxes after the art the user shared (artist not
named, no name given; our name).

A sleek robot Suicune of glassy teal set with pale diamond facets over a grey mechanical frame, its leg joints rimmed
in glowing pink. A lavender hood of angular plates sweeps over its head and down its back, a glowing pink hexagon
crest with a cyan gem rises from its brow, and in place of Suicune's ribbons four great angular tendrils of starry
pink light arch out from its shoulders and hips like the legs of a spider.

Shiny: a lavender body with cyan tendrils.

Front is -z, y is up. 40 units tall (to the crest); about 2.2 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _pgen1 import stars
from _regi import ellipsoid
from _route import pal, tone

HEIGHT = 40
SCALE = round(2.2 * 16 / HEIGHT, 3)
HITBOX = [2.4, HEIGHT / 16]
KIND = "quadruped"
K = 3
LOOK = ("a sleek robot Suicune of glassy teal with pale diamond facets, a lavender hood of plates, a glowing pink "
        "hexagon crest and four arching tendrils of starry pink light")

BASE = {"teal": (104, 208, 214), "teal_dark": (60, 150, 162), "teal_light": (170, 236, 238), "diamond": (224, 244, 222),
        "grey": (126, 130, 140), "grey_dark": (84, 88, 98), "lav": (186, 152, 206), "lav_dark": (122, 98, 150),
        "pink": (240, 86, 120), "pink_light": (255, 190, 206), "star": (255, 255, 255), "cyan": (130, 236, 246),
        "muzzle": (208, 210, 218), "eye": (40, 20, 30)}
SHINY = {"teal": (178, 150, 214), "teal_dark": (124, 98, 166), "teal_light": (214, 196, 240), "lav": (90, 190, 200),
         "lav_dark": (54, 128, 140), "pink": (70, 220, 250), "pink_light": (200, 248, 255), "cyan": (255, 150, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def glassf(x, y, z, face, variant, **k):
    """Glassy teal with scattered pale diamond facets."""
    p = P(variant)
    a, b = {"north": (x, y), "south": (-x, y), "east": (z, y), "west": (-z, y)}.get(face, (x, z))
    cu, cv = math.floor(a / 3.0), math.floor(b / 3.0)
    h = ((cu * 73856093) ^ (cv * 19349663)) & 0xFF
    if h < 120:
        du, dv = a - (cu + 0.5) * 3.0, b - (cv + 0.5) * 3.0
        if abs(du) + abs(dv) * 0.8 < 1.1:
            return p["diamond"], None
    if face == "up":
        return p["teal_light"], None
    return tone(p["teal"], face), None


def legf(x, y, z, face, variant, box=None, **k):
    """Teal legs with glowing pink rims at the joint (rods: z runs from the joint)."""
    p = P(variant)
    d = (box.lo[2] + box.size[2] - z) / max(box.size[2], 0.01)
    if d < 0.12 or 0.86 < d:
        return p["pink"], p["pink"]
    return glassf(x, y, z, face, variant)


def headf(eye_y, eye_z):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("east", "west") and math.hypot(z - eye_z, y - eye_y) < 0.5:
            return p["eye"], None
        return glassf(x, y, z, face, variant)
    return s


def tendrilf(x, y, z, face, variant, **k):
    p = P(variant)
    if stars(x, y, z, face, cell=1.4, r=0.26, prob=0.35):
        return p["star"], p["star"]
    return p["pink"], p["pink"]


def hoodf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        return tone(p["lav"], face), None
    return tone(p["lav"] if face in ("north", "south") else p["lav_dark"], face), None


def tendril(m, bone, root, knee, tip):
    rod(m, bone, root, knee, 1.6, tendrilf, extend=0.6)
    rod(m, bone, knee, tip, 1.4, tendrilf, extend=0.6)
    spike(m, bone, tip, tuple(b - a for a, b in zip(knee, tip)), 1.2, 2.4, tendrilf, tip=0.5)


def build() -> Model:
    m = Model("ironcurrent")
    neck = ((0, 25.0, -13.0), (0, 28.5, -16.5))
    head_len, head_w, head_h = 9.0, 3.2, 4.2
    hx, hy, hz = neck[-1]
    eye_y, eye_z = hy + head_h * 0.25, hz - head_len * 0.35
    mats = {"skin": glassf, "belly": solid("grey"), "neck": glassf, "head": headf(eye_y, eye_z),
            "snout": solid("muzzle"), "jaw": solid("grey"), "mouth": solid("grey_dark"), "tooth": solid("muzzle"),
            "tongue": solid("grey_dark"), "leg_upper": glassf, "leg_lower": legf, "paw": glassf,
            "claw": solid("teal_dark"), "tail": glassf}
    a = quadruped(m, mats, "ironcurrent", length=26.0, body_y=17.0, body_rx=5.0, body_ry=5.0, chest_bulk=1.12,
                  neck=neck, head_len=head_len, head_w=head_w, head_h=head_h, snout=0.35, mouth_open=4, teeth=0,
                  leg_bulk=1.05, tail=((0, 18.5, 14.0), (0, 17.5, 16.0)), tail_r=(1.6, 1.0), toes=3, claws=False)
    bd, hd, nk = a["body"], a["head"], a["neck"]
    top = a["skull_top"]
    # the lavender hood: angular plates over the head, down the neck and along the back, with a spike at its end
    for (x0, y0, z0, x1, y1, z1) in ((-3.8, top - 1.0, hz - 3.0, 3.8, top + 3.2, hz + 4.6),
                                     (-4.4, 25.0, -15.0, 4.4, 31.0, -8.0),
                                     (-4.8, 22.0, -9.0, 4.8, 26.0, 2.0)):
        m.box(nk if z0 < -10 else bd, x0, y0, z0, x1, y1, z1, hoodf)
    m.box(bd, -4.2, 21.0, 1.6, 4.2, 23.6, 7.0, hoodf)
    spike(m, bd, (0, 22.2, 6.6), (0, 0.15, 1), 2.4, 4.4, hoodf, tip=0.9)
    # the glowing pink hexagon crest with a cyan gem, and a pink chevron on its brow
    cz, cy = hz - 2.6, top + 6.0
    hexpts = [(0, cy + 5.0), (2.6, cy + 2.6), (2.6, cy - 2.0), (0, cy - 4.2), (-2.6, cy - 2.0), (-2.6, cy + 2.6)]
    for (x0, y0), (x1, y1) in zip(hexpts, hexpts[1:] + hexpts[:1]):
        rod(m, hd, (x0, y0, cz + (y0 - cy) * 0.35), (x1, y1, cz + (y1 - cy) * 0.35), 1.0, tendrilf, extend=0.6)
    ellipsoid(m, hd, 0, top + 0.8, hz - 4.2, 0.9, 0.9, 0.6, solid("cyan", True), step=1)
    for sx in (-1, 1):
        rod(m, hd, (0, top + 0.4, hz - 4.6), (sx * 3.2, top - 0.6, hz - 2.6), 0.9, tendrilf, extend=0.3)
    # four tendrils of starry pink light arching out like spider legs
    for zz, reach, hi in ((-8.0, 14.0, 32.0), (8.0, 13.0, 29.0)):
        for sx in (-1, 1):
            root = (sx * 4.6, 21.0, zz)
            knee = (sx * 9.0, hi, zz + (-3.0 if zz < 0 else 3.0))
            tip = (sx * reach, 9.0, zz + (-7.0 if zz < 0 else 7.0))
            tendril(m, bd, root, knee, tip)
    for sx in (-1, 1):                                                              # pink rims on the hips
        x0, x1 = sorted((sx * 4.4, sx * 5.6))
        m.box(bd, x0, 13.0, 8.0, x1, 20.0, 13.0, solid("pink", True))
    return m
