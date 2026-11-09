"""Mega Flutter Mane, hand-built from boxes in Cobblemon's style.

Flutter Mane (official art: an ancient Misdreavus, a dark teal ghost with a mane of big feathered "wings" (teal with
lavender feather tips and a pale teal patch), a crest of red spikes, glaring red-and-yellow eyes, a red bead
necklace and a jagged skirt) as a mega: two tiers of mane-wings with glowing pink feather tips, a crown of red
spikes, two glowing bead necklaces and a long tattered skirt. It floats.

Front is -z, y is up. ~34 units tall; baseScale 1.0 (about 2.1 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, mix, spike

SCALE = 1.0
HITBOX = [2.0, 2.2]
LOOK = "two tiers of feathered mane-wings with glowing pink tips, a crown of red spikes, glaring red-and-yellow eyes, a glowing bead necklace and a long tattered skirt"
KIND = "floater"

BASE = {
    "teal": (40, 84, 96), "teal_light": (62, 112, 124), "teal_dark": (26, 58, 70), "patch": (110, 170, 160),
    "feather": (150, 128, 200), "feather_tip": (240, 120, 190), "crest": (214, 40, 54), "crest_light": (240, 90, 90),
    "eye": (250, 214, 60), "iris": (220, 30, 40), "pupil": (30, 10, 20), "mouth": (20, 20, 30), "fang": (250, 250, 250),
    "bead": (220, 40, 60), "bead_light": (255, 120, 120),
}
SHINY = {"teal": (110, 120, 60), "teal_light": (140, 150, 80), "teal_dark": (80, 88, 40), "patch": (200, 210, 120),
         "feather": (230, 170, 90), "feather_tip": (255, 220, 120), "crest": (230, 120, 40), "bead": (240, 140, 50),
         "bead_light": (255, 200, 120)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def body(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "down":
        return P["teal_dark"]
    return P["teal_light"] if face == "up" else P["teal"]


def face(x, y, z, face, variant, **k):
    """Glaring eyes (yellow, red iris, slanted) and a little fanged smirk."""
    P = palette(variant)
    if face == "north":
        for side in (-1, 1):
            dx = (x - side * 3.4) * side
            top = 18.2 - 0.7 * (2.8 - dx)
            if -2.8 <= dx <= 2.8 and 14.0 <= y <= top:
                if -1.2 <= dx <= 1.0 and y <= 16.4:
                    return (P["pupil"] if -0.6 <= dx <= 0.4 and y <= 15.6 else P["iris"]), P["iris"]
                return P["eye"], P["eye"]
        if 11.6 <= y <= 12.6 and abs(x) < 3.0 and not (abs(x) > 2.0 and y > 12.1):
            return P["mouth"]                         # a wide smirk
        if 10.8 <= y < 11.6 and (0.8 < x < 1.8 or -2.2 < x < -1.2):
            return P["fang"]
    return body(x, y, z, face, variant)


def wing(x, y, z, face, variant, r=0, c=0, rows=1, cols=1, box=None, **k):
    """A mane-wing panel: teal, lavender feathers near the edge with glowing pink tips, feathered (cut) edge."""
    P = palette(variant)
    t = (abs(x) - 6) / box.size[0]                     # 0 at the root, 1 at the tip (either side)
    edge = rows - 1 - int(2.5 * abs(math.sin(abs(x) * 0.9)))   # a scalloped lower edge
    if r > edge:
        return (0, 0, 0, 0)
    if t > 0.78:
        return P["feather_tip"], P["feather_tip"]
    if t > 0.55:
        return P["feather"]
    if 0.2 < t < 0.45 and 1 <= r <= rows - 3:
        return P["patch"]
    return P["teal"]


def crest(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["crest_light"] if face in ("up", "north") else P["crest"]


def bead(x, y, z, face, variant, **k):
    P = palette(variant)
    return (P["bead_light"] if face in ("up", "north") else P["bead"]), P["bead"]


def skirt(x, y, z, face, variant, r=0, c=0, rows=1, **k):
    P = palette(variant)
    if face not in ("up", "down") and r >= rows - 2 and (c % 3 != 1 or r == rows - 1):
        return (0, 0, 0, 0)                           # long tattered points
    return P["teal_dark"] if face == "down" else P["teal"]


def build() -> Model:
    m = Model("fluttermane_mega")
    root = m.bone("fluttermane_mega", None, (0, 0, 0))
    bodyb = m.bone("body", root, (0, 14, 0))
    # head-body: one rounded ghostly bulb with the face
    m.round_box(bodyb, 0, 0, 7, 6, 10, 22, face, cut=2)
    m.round_box(bodyb, 0, 0, 6, 5, 22, 24, body, cut=2)
    # bead necklaces: two strands of glowing red beads
    for ring_y, rad, n in ((9, 7.6, 9),):
        for i in range(n):
            a = 2 * math.pi * i / n
            bx, bz = rad * math.sin(a), -rad * 0.85 * math.cos(a)
            if bz > 2:
                continue                              # only round the front and sides
            m.box(bodyb, bx - 1, ring_y - 1, bz - 1, bx + 1, ring_y + 1, bz + 1, bead)
    # the skirt: long and tattered
    skirtb = m.bone("skirt", bodyb, (0, 10, 0))
    m.round_box(skirtb, 0, 0, 6, 5, 2, 10, skirt, cut=2)
    m.round_box(skirtb, 0, 0, 4, 4, -3, 2, skirt, cut=1)

    head = m.bone("head", bodyb, (0, 22, 0))
    # a crown of red spikes
    for ang, h in ((0, 9), (-28, 7), (28, 7), (-52, 5), (52, 5)):
        a = math.radians(ang)
        spike(m, head, (5 * math.sin(a), 23.5, -2 * math.cos(a)), (math.sin(a) * 0.5, 1, 0.3), 3, h, crest, tip=1)

    # the mane: two tiers of feathered wings each side (planes), lower tier smaller
    mane = m.bone("mane", bodyb, (0, 18, 2))
    for sgn in (1, -1):
        for tier, (y0, h, length, tilt) in enumerate(((16, 12, 20, 18), (11, 9, 14, -8))):
            x0 = sgn * 6
            m.box(mane, x0 if sgn > 0 else x0 - length, y0, 2, x0 + length if sgn > 0 else x0, y0 + h, 2, wing,
                  rotation=(0, sgn * -15, sgn * tilt), pivot=(x0, y0 + h / 2, 2))
            # a thick root where each wing meets the body
            m.box(mane, (x0 - 1) if sgn > 0 else (x0 - 3), y0 + 2, 0, (x0 + 3) if sgn > 0 else (x0 + 1), y0 + h - 2, 4, body)
    return m
