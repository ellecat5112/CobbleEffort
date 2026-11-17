"""Blastmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the crystal emperor. A hulking, hunched giant in black-and-silver plate whose shoulders, back and
chest bristle with a great mane of pale blue crystals, a small grim face sunk between them, a skull-faced pauldron
with yellow lenses on its left shoulder, a tattered crimson cape, and a huge right gauntlet set with red, green and
yellow jewels. 35 blocks tall.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, dome, humanoid
from _digidetail import armour, eye, fabric, gem, metal, skin, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hulking crystal emperor in black-and-silver plate, a mane of pale blue crystals over its shoulders and "
        "chest, a skull-faced pauldron, a tattered crimson cape and a huge jewelled gauntlet")
BASE = {"black": (56, 58, 70), "black_dark": (22, 22, 30), "black_light": (120, 124, 140), "silver": (206, 210, 222),
        "silver_dark": (110, 114, 128), "crystal": (150, 196, 240), "crystal_light": (236, 248, 255),
        "crystal_dark": (70, 110, 170), "cape": (150, 20, 34), "cape_dark": (70, 6, 14), "face": (150, 150, 160),
        "face_dark": (80, 80, 92), "lens": (240, 220, 90), "gem_r": (230, 40, 50), "gem_g": (60, 200, 90),
        "gem_y": (250, 220, 60), "white": (250, 250, 250), "pupil": (30, 10, 10), "eye": (250, 80, 60)}
SHINY = {"crystal": (240, 150, 200), "crystal_light": (255, 236, 248), "crystal_dark": (170, 70, 130),
         "cape": (30, 60, 140), "cape_dark": (10, 24, 70), "black": (210, 200, 180), "black_dark": (130, 120, 100)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "black", "black_dark", light="black_light", trim="silver")
SILVER = metal(P, "silver", dark="silver_dark")
CRYSTAL = gem(P, "crystal", "crystal_light", glow=False)
CRYSTAL_D = gem(P, "crystal_dark", "crystal", glow=False)
CAPE = fabric(P, "cape", "cape_dark", axis="y", period=3.4)
FACE = skin(P, "face", dark="face_dark", var=0.04)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = eye(p, x - sx * 1.1, y - 54.6, 0.6, "eye")
            if c is not None:
                return c, (c[:3] if c == p["eye"] else None)
        if abs(x) < 1.4 and 52.0 < y < 52.5:
            return tone(p["face_dark"], face), None
    return FACE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("blastmon")
    mats = {"skin": PLATE, "chest": CRYSTAL, "abs": PLATE, "pelvis": SILVER, "neck": PLATE, "deltoid": PLATE,
            "upper_arm": PLATE, "forearm": SILVER, "hand": PLATE, "finger": SILVER, "claw": SILVER, "thigh": PLATE,
            "knee": SILVER, "shin": PLATE, "calf": PLATE, "foot": SILVER, "talon": SILVER}
    a = humanoid(m, mats, bulk=1.5, arm_bulk=1.4, leg_bulk=1.35, digitigrade=True, claws=True, talons=True,
                 name="blastmon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 52, -2))
    m.round_box(hd, 0, -3.0, 2.4, 2.4, 50.5, 56.5, facef, cut=1)                    # the small grim face, sunk low
    m.box(hd, -2.6, 56.0, -5.4, 2.6, 57.4, -1.0, SILVER)                              # brow band
    # the crystal mane: rings of crystals round the shoulders and back, longest over the spine
    for ring, (rad, yb, n) in enumerate(((8.6, 50.0, 18), (7.0, 54.0, 14), (4.6, 57.5, 9))):
        for i in range(n):
            deg = -160 + i * 320 / max(n - 1, 1)
            if ring and abs(deg) < 45:
                continue                                                         # leave the face clear
            ang = math.radians(deg)
            base = (rad * math.sin(ang), yb, 1.0 - rad * 0.8 * math.cos(ang))
            d = (math.sin(ang) * 1.3, 0.8 + 0.3 * ring, 0.9 - 0.4 * math.cos(ang))
            spike(m, bd, base, d, 2.6 - 0.4 * ring, 6.5 + 1.5 * ring + (i % 3), CRYSTAL if (i + ring) % 3 else CRYSTAL_D,
                  tip=1.0)
    for row in range(4):                                                             # crystal scales down the chest
        for j in range(5 - row % 2):
            x = (j - (4 - row % 2) / 2) * 2.2
            spike(m, bd, (x, 49.0 - row * 3.0, -6.4), (x * 0.06, -0.5, -1), 2.2, 2.8, CRYSTAL, tip=0.8)
    # the skull-faced pauldron on its left shoulder with two yellow lenses
    al = a["arm_left"]
    sh = al["shoulder"]
    dome(m, al["bone"], (sh[0] + 1.6, 49.0, 0.0), 5.0, 4.6, PLATE, layers=4)
    for dz in (-1.6, 1.6):
        m.box(al["bone"], sh[0] + 1.0, 50.8, -5.4 + dz * 0.3, sh[0] + 3.2, 52.6, -5.0 + dz * 0.3,
              solid(P, "lens", glow=True))
    for i in range(4):
        spike(m, al["bone"], (sh[0] + 1.6 + (i - 1.5) * 1.6, 52.6, 0), (0.2 * (i - 1.5), 1, 0.3), 1.4, 3.0, SILVER)
    # the huge right gauntlet with its three jewels
    ar = a["arm_right"]
    w, h = ar["wrist"], ar["hand"]
    rod(m, ar["bone"], ar["elbow"], (h[0], h[1] - 1.0, h[2]), 7, SILVER, extend=0.6)
    m.round_box(ar["bone"], h[0], h[2], 4.4, 4.2, h[1] - 6.0, h[1] + 1.4, PLATE, cut=2)
    for j, key in enumerate(("gem_r", "gem_g", "gem_y")):
        y = w[1] - 0.5 - j * 3.0
        m.box(ar["bone"], h[0] - 1.2, y - 1.0, h[2] - 4.8, h[0] + 1.2, y + 1.0, h[2] - 4.0,
              gem(P, key, "white"))
    for i in range(5):
        spike(m, ar["bone"], (h[0] - 4.0, h[1] - 5.0 + i * 1.6, h[2]), (-1, 0.1, 0), 1.2, 2.6, SILVER)
    # the tattered crimson cape
    cb = m.bone("cap", bd, (0, 52, 4))
    cape(m, cb, 52.0, 26.0, 46.0, CAPE, z=6.0, flare=1.0, panels=9, sweep=(0, 6), seed=4)
    return m
