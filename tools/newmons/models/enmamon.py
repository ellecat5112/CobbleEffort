"""Enmamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the judge of the underworld. A grim armoured king in black-and-violet plate seated on a great carved
throne crowned with dark violet flame-spikes and a red eye, a tall mirror set in its back; it holds a curved wooden
judge's tablet, and the throne floats on a jagged black rock with a long scroll unrolling round it and two little
attendant spirit-masks, one red and one blue. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid
from _digidetail import armour, fabric, local, metal, skin, solid
from _dorbickmon import mount
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = ("a grim black-and-violet armoured king on a great carved throne with flame-spikes and a mirror, holding a judge's "
        "tablet, floating on a jagged black rock wrapped in an unrolling scroll")
BASE = {"black": (36, 34, 44), "black_dark": (10, 10, 14), "black_light": (110, 106, 130), "violet": (110, 80, 160),
        "violet_dark": (50, 30, 80), "violet_light": (190, 160, 230), "throne": (210, 200, 180), "throne_dark": (140, 130, 110),
        "mirror": (200, 210, 230), "mirror_light": (250, 252, 255), "red": (210, 30, 40), "rock": (40, 38, 46),
        "rock_dark": (14, 12, 18), "scroll": (40, 120, 90), "scroll_dark": (20, 60, 40), "paper": (240, 232, 214),
        "wood": (140, 90, 50), "blue": (90, 140, 230), "eye": (250, 60, 60)}
SHINY = {"violet": (190, 60, 60), "violet_dark": (90, 14, 20), "violet_light": (250, 150, 150)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "black", "black_dark", light="black_light", trim="violet", trim_w=0.3)
THRONE = armour(P, "throne", "throne_dark", trim="violet", trim_w=0.4)


def scrollf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if abs(v - H / 2) < H * 0.3:
        return tone(p["paper"] if (u % 2.0) > 0.4 else p["black"], face), None
    return tone(p["scroll"], face), None


def build():
    m = Model("enmamon")
    top = m.bone("enmamon", None, (0, 0, 0))
    rk = m.bone("rock", top, (0, 6, 0))                                           # jagged floating rock
    for i, (r, y0) in enumerate(((3.0, 0.0), (7.0, 3.0), (11.0, 6.0), (13.0, 9.0))):
        m.round_box(rk, 0, 0, r, r, y0, y0 + 3.0, skin(P, "rock", dark="rock_dark"), cut=max(1, round(r * 0.35)))
    spike(m, rk, (0, 2.0, 0), (0, -1, 0), 4.0, 2.0, skin(P, "rock", dark="rock_dark"), tip=1.0)
    th = m.bone("throne", rk, (0, 12, 4))                                         # the throne
    m.box(th, -9.0, 12.0, -6.0, 9.0, 20.0, 8.0, THRONE)
    m.box(th, -9.0, 20.0, 5.0, 9.0, 52.0, 9.0, THRONE)
    m.box(th, -6.0, 28.0, 4.6, 6.0, 48.0, 5.0, metal(P, "mirror", dark="mirror", light="mirror_light"))  # mirror
    for sx in (-1, 1):
        m.box(th, min(sx * 9.0, sx * 12.0), 12.0, -6.0, max(sx * 9.0, sx * 12.0), 30.0, 8.0, THRONE)    # armrests
        for j in range(3):                                                         # flame-spikes on the crown
            spike(m, th, (sx * (3.0 + j * 3.0), 52.0, 7.0), (sx * 0.4 * (j + 1), 1, 0), 1.6, 6.0 - j, solid(P, "violet"),
                  tip=0.4)
    spike(m, th, (0, 52.0, 7.0), (0, 1, 0), 2.0, 8.0, solid(P, "violet"), tip=0.4)
    m.round_box(th, 0, 4.4, 1.2, 0.6, 49.0, 51.0, solid(P, "eye", glow=True), cut=0)
    i_box, i_bone = len(m.boxes), len(m.bones)                                     # the seated king
    mats = {"skin": ARM, "chest": ARM, "abs": ARM, "pelvis": ARM, "neck": ARM, "deltoid": ARM, "upper_arm": ARM,
            "forearm": ARM, "hand": ARM, "finger": ARM, "claw": solid(P, "red"), "thigh": ARM, "knee": ARM, "shin": ARM,
            "calf": ARM, "foot": ARM, "talon": solid(P, "red")}
    a = humanoid(m, mats, bulk=1.2, arm_bulk=1.2, leg_bulk=1.1, claws=True, name="king")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.8, 3.0, 54.0, 60.4, ARM, cut=1)
    m.box(hd, -1.8, 57.0, -3.5, 1.8, 57.8, -3.3, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        dome(m, bd, (sx * 8.0, 49.0, 0), 3.6, 3.0, ARM)
        spike(m, hd, (sx * 2.0, 60.0, 0), (sx * 0.6, 1, 0), 1.2, 4.0, ARM, tip=0.3)
    ar = a["arm_right"]                                                            # judge's tablet
    hx, hy, hz = ar["hand"]
    rod(m, ar["bone"], (hx, hy, hz), (hx - 3.0, hy + 12.0, hz - 2.0), 1, metal(P, "wood", dark="wood"), extend=0, t2=3)
    m.boxes[i_box:] = [b for b in m.boxes[i_box:] if b.bone not in ("leg_left", "leg_right")]
    m.bones[i_bone:] = [b for b in m.bones[i_bone:] if b["name"] not in ("leg_left", "leg_right")]
    for sx in (-1, 1):                                                             # seated legs
        rod(m, bd, (sx * 3.4, 33.0, 0.0), (sx * 3.6, 33.0, -9.0), 5, ARM, extend=0.8)
        rod(m, bd, (sx * 3.6, 33.0, -9.0), (sx * 3.8, 21.0, -10.0), 4, ARM, extend=0.6)
        m.box(bd, sx * 3.8 - 2.2, 19.0, -15.0, sx * 3.8 + 2.2, 22.0, -8.0, ARM)
        for j in range(3):
            spike(m, bd, (sx * 3.8 + (j - 1) * 1.4, 20.0, -15.0), (0, -0.2, -1), 1.0, 2.4, solid(P, "red"), tip=0.25)
    mount(m, i_box, i_bone, -13.0, 0.0, "throne")
    sb = m.bone("ring_scroll", rk, (0, 10, 0))                                     # unrolling scroll
    for i in range(14):
        a0 = 2 * math.pi * i / 14
        a1 = 2 * math.pi * (i + 1) / 14
        rod(m, sb, (16.0 * math.cos(a0), 10.0 + 3.0 * math.sin(a0 * 2), 16.0 * math.sin(a0)),
            (16.0 * math.cos(a1), 10.0 + 3.0 * math.sin(a1 * 2), 16.0 * math.sin(a1)), 1, scrollf, extend=0.6, t2=3)
    for sx, key in ((-1, "red"), (1, "blue")):                                     # attendant spirit-masks
        m.round_box(sb, sx * 17.0, -2.0, 1.8, 1.4, 14.0, 17.6, solid(P, key), cut=1)
    return m
