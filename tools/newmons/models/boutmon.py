"""Boutmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the kickboxing beast-man. A dark-skinned muscular fighter with a spiky yellow mane, a steel mask
band over his eyes and a bushy white moustache, a string of white prayer beads with a glowing green jewel, red-and-
black fighting gloves, ragged yellow fighter's trousers belted with a black sash, bandaged shins, red clawed feet, a
yellow-to-red tail and long white streamers crackling with lightning round him. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import (Bulge, cutout, fabric, gem, leather, local, metal, mix, noise2, skin, solid, strands,
                         torso_bulges)
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a muscular kickboxing beast-man with a spiky yellow mane, a steel mask band and white moustache, prayer "
        "beads with a green jewel, red fighting gloves, ragged yellow trousers and lightning-crackling streamers")
BASE = {"skin": (60, 50, 56), "skin_dark": (26, 20, 24), "skin_light": (120, 104, 112), "mane": (250, 220, 40),
        "mane_dark": (220, 120, 20), "white": (246, 244, 236), "white_dark": (190, 186, 176), "steel": (200, 204, 216),
        "steel_dark": (100, 104, 116), "red": (220, 40, 40), "red_dark": (120, 14, 16), "yellow": (240, 220, 60),
        "yellow_dark": (170, 140, 20), "black": (30, 28, 34), "black_light": (90, 88, 100), "jewel": (60, 220, 90),
        "jewel_light": (200, 255, 210), "bolt": (255, 250, 150, 220), "vein": (90, 76, 84)}
SHINY = {"skin": (180, 120, 80), "skin_dark": (110, 66, 40), "skin_light": (230, 180, 140), "yellow": (80, 160, 230),
         "yellow_dark": (30, 90, 160), "mane": (240, 240, 250), "mane_dark": (170, 170, 190), "jewel": (230, 60, 90)}


def P(v):
    return pal(BASE, SHINY, v)


CHEST = skin(P, "skin", dark="skin_dark", light="skin_light", bulges=torso_bulges(0, 51.0, 5.8, abs_rows=4),
             vein_key="vein", vein_rects=(((-6, 36, 6, 51), ("north",), 3),), var=0.03)
ARM = skin(P, "skin", dark="skin_dark", light="skin_light", var=0.03,
           bulges=[Bulge("north", sx * 9.2, 42.0, 1.9, 3.6, light=0.35, shadow=0.45) for sx in (-1, 1)])
TROUSER = fabric(P, "yellow", "yellow_dark", axis="y", period=2.4)
GLOVE = leather(P, "red", "red_dark", stitch="black")
MANE = strands(P, "mane", "mane_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def ragged(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.25 * noise2((box.lo[0] + u) * 1.1, 2.0)


def streamerf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if (v * 1.3 + u) % 4.0 < 0.3:
        return p["bolt"], p["bolt"][:3]
    return tone(p["white"], face), None


def build():
    m = Model("boutmon")
    mats = {"skin": ARM, "chest": CHEST, "abs": CHEST, "pelvis": leather(P, "black", "black_light"),
            "hand": GLOVE, "finger": GLOVE, "thigh": TROUSER, "knee": TROUSER, "shin": solid(P, "white"),
            "calf": solid(P, "white_dark"), "foot": solid(P, "red"), "talon": solid(P, "red_dark")}
    a = humanoid(m, mats, bulk=1.2, arm_bulk=1.3, leg_bulk=1.15, digitigrade=True, talons=True, name="boutmon",
                 hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.4, 61.0, ARM, cut=1)
    m.box(hd, -3.0, 57.6, -3.4, 3.0, 59.0, 3.0, STEEL)                                    # steel mask band
    for sx in (-1, 1):
        m.box(hd, sx * 1.2 - 0.6, 58.0, -3.5, sx * 1.2 + 0.6, 58.6, -3.4, solid(P, "red", glow=True))
        rod(m, hd, (sx * 0.4, 56.0, -3.4), (sx * 3.4, 54.4, -3.0), 1, solid(P, "white"), extend=0.2, t2=2)  # moustache
    for sx in (-1, 1):                                                                    # band tails behind
        rod(m, hd, (sx * 1.0, 58.4, 3.0), (sx * 4.0, 55.0, 9.0), 1, STEEL, extend=0, t2=2)
    for i in range(14):                                                                   # spiky yellow mane
        ang = math.radians(-110 + i * 17)
        base = (2.4 * math.sin(ang), 60.4, 0.4 - 2.0 * math.cos(ang))
        spike(m, hd, base, (math.sin(ang) * 0.7, 1.0, 0.4 - 0.3 * math.cos(ang)), 1.6, 5.0 + (i % 3), MANE, tip=0.5)
    for i in range(11):                                                                   # prayer beads + jewel
        ang = math.radians(-100 + i * 20)
        c = (5.0 * math.sin(ang), 51.0 - 3.0 * math.cos(ang) ** 2, 0.2 - 4.0 * math.cos(ang))
        m.round_box(bd, c[0], c[2], 0.9, 0.9, c[1] - 0.9, c[1] + 0.9, solid(P, "white"), cut=1)
    m.box(bd, -1.4, 46.0, -5.8, 1.4, 48.8, -4.8, gem(P, "jewel", "jewel_light"))
    for nm in ("leg_left", "leg_right"):                                                  # ragged trouser hems
        lg = a[nm]
        kn = lg["knee"]
        for ang in (0, 90, 180, 270):
            m.box(lg["bone"], kn[0] - 2.8, kn[1] - 4.0, kn[2] - 2.8, kn[0] + 2.8, kn[1] + 1.0, kn[2] - 2.8,
                  cutout(ragged, TROUSER), rotation=(0, ang, 0), pivot=(kn[0], kn[1], kn[2]))
    tl = m.bone("tail", bd, (0, 31, 3))
    pts = [(0, 31, 3), (2, 24, 8), (3, 16, 10), (2, 10, 13)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 2, solid(P, "yellow" if j < 2 else "red"), extend=0.3)
    # long white streamers from his shoulders, crackling with lightning
    for sx in (-1, 1):
        sb = m.bone(f"streamer_{'left' if sx > 0 else 'right'}", bd, (sx * 6.0, 51.0, 2.0))
        pts = [(sx * 6.0, 51.0, 2.0), (sx * 14.0, 56.0, 4.0), (sx * 16.0, 42.0, 6.0), (sx * 18.0, 30.0, 4.0),
               (sx * 16.0, 20.0, 2.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, sb, p0, p1, 1, streamerf, extend=0.4, t2=2)
    return m
