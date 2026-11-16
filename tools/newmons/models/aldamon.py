"""Aldamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a dragon-warrior of fire. A crimson dragon helm with a gold crest and white tusks, glowing gold eyes,
a great golden mane of flame-hair, black horns rising behind its shoulders; a black, heavily muscled body under
gold-trimmed crimson armour with a gold scale-strip down its chest; crimson gauntlets, a long gold ray-blade on its
right forearm and a tall gold kite-blade on its left; gold crescent tassets, big gold knee plates, silver talons, a
crimson tail, fire burning in its right fist and a mass of flame flaring from its back. 25 blocks tall.

Front is -z, y is up. 70 units tall (the flames); Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import (Bulge, armour, cutout, eye, flame_inside, local, metal, mix, mul, plane, skin, solid,
                         strands, torso_bulges)
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = ("a dragon-warrior of fire: a crimson dragon helm with a gold crest and white tusks, a golden flame-mane, black "
        "horns behind its shoulders, a muscled black body under gold-trimmed crimson armour, gold ray- and kite-blades, "
        "gold knee plates, silver talons, a crimson tail and flames in its fist and at its back")

BASE = {"red": (176, 28, 48), "red_dark": (104, 14, 30), "red_light": (222, 70, 80),
        "gold": (232, 182, 58), "gold_dark": (160, 112, 26), "gold_light": (255, 232, 150),
        "suit": (44, 42, 50), "suit_dark": (14, 12, 16), "suit_light": (120, 118, 134), "suit_vein": (62, 60, 72),
        "silver": (212, 214, 224), "silver_dark": (130, 134, 150), "white": (246, 242, 230),
        "horn": (34, 30, 36), "horn_light": (96, 92, 104),
        "hair": (250, 204, 62), "hair_dark": (226, 136, 34), "hair_tip": (255, 240, 160),
        "flame": (255, 150, 40, 210), "flame_core": (255, 226, 110, 230), "eye": (255, 214, 60), "pupil": (40, 20, 10)}
SHINY = {"red": (40, 70, 190), "red_dark": (20, 36, 110), "red_light": (90, 130, 230),
         "gold": (214, 218, 230), "gold_dark": (140, 146, 162), "gold_light": (250, 252, 255),
         "hair": (120, 210, 255), "hair_dark": (50, 130, 230), "hair_tip": (220, 245, 255),
         "flame": (70, 160, 255, 210), "flame_core": (180, 230, 255, 230), "eye": (120, 230, 255)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", light="red_light", trim="gold")
RED_PLAIN = armour(P, "red", "red_dark", light="red_light")
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
SILVER = metal(P, "silver", dark="silver_dark", light="white")
HORN = metal(P, "horn", light="horn_light", streak=4.0)
HAIR = strands(P, "hair", "hair_dark", tip="hair_tip")
ABS = torso_bulges(0, 44.5, 4.6, abs_rows=3)
SUIT = skin(P, "suit", dark="suit_dark", light="suit_light", bulges=ABS, var=0.04)
SUIT_ARM = skin(P, "suit", dark="suit_dark", light="suit_light", vein_key="suit_vein",
                vein_rects=(((-14, 30, 14, 46), ("north", "east", "west"), 7),), var=0.04, vein_count=2, vein_width=0.3)
SUIT_LEG = skin(P, "suit", dark="suit_dark", light="suit_light",
                bulges=[Bulge("north", sx * 3.4, 25.5, 1.8, 4.2, light=0.3, shadow=0.4) for sx in (-1, 1)], var=0.04)


def chestf(x, y, z, face, variant, box=None, **k):
    """Crimson chest armour with a gold scale-strip down the middle (overlapping dragon-belly scutes)."""
    p = P(variant)
    if face == "north" and abs(x) < 1.5:
        band = (y % 1.6) / 1.6
        c = p["gold_light"] if band > 0.78 else p["gold"] if band > 0.2 else p["gold_dark"]
        return tone(mul(c, 1 - 0.18 * abs(x) / 1.5), face), None
    return RED(x, y, z, face, variant, box=box, **k)


def helmf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):                                          # slanted glowing eyes
            du, dv = x - sx * 1.25, (y - 59.3) - 0.45 * sx * (x - sx * 1.25)
            if abs(du) < 0.9 and abs(dv) < 0.32:
                return p["eye"], p["eye"]
        if abs(x) < 0.45 and y > 59.8:
            return tone(p["gold"], face), None                      # gold crest line
    return RED(x, y, z, face, variant, box=box, **k)


def emblemf(x, y, z, face, variant, box=None, **k):
    """The belt plate with Aldamon's angular spiral crest in silver."""
    p = P(variant)
    if face == "north":
        u, v = x, y - 32.6
        if max(abs(u), abs(v)) < 1.4 and (abs(abs(u) - 1.0) < 0.22 or abs(abs(v) - 1.0) < 0.22 or
                                          (abs(u) < 0.22 and v > -0.4) or (abs(v) < 0.22 and u > -0.2)):
            return tone(p["silver"], face), None
    return RED_PLAIN(x, y, z, face, variant, box=box, **k)


def flame_shape(cx, cy, w, h, lean=0.0, tongues=4):
    """A flame silhouette in a plane: wide base, wavy tongues tapering up; for cutout()."""
    def inside(x, y, z, face, box):
        u, v, W, H = local(x, y, z, face, box)
        t = v / max(H, 1e-6)
        uu = u / max(W, 1e-6) - 0.5 - lean * t
        width = 0.5 * (1 - t) ** 0.7
        wave = 0.08 * math.sin(t * 9 + uu * 12)
        tongue = abs(math.sin((uu + 0.5) * math.pi * tongues)) ** 0.5
        return abs(uu) < width + wave and t < 0.55 + 0.45 * tongue
    return inside


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    core = abs(u / max(W, 1e-6) - 0.5) < 0.22 and v / max(H, 1e-6) < 0.6
    c = p["flame_core"] if core else p["flame"]
    return c, c[:3]


def build():
    m = Model("aldamon")
    mats = {"skin": SUIT_ARM, "chest": chestf, "abs": SUIT, "pelvis": RED_PLAIN, "neck": SUIT,
            "deltoid": RED, "upper_arm": SUIT_ARM, "forearm": RED, "hand": skin(P, "suit"),
            "finger": skin(P, "suit"), "thigh": SUIT_LEG, "knee": GOLD, "shin": RED, "calf": RED,
            "foot": SILVER, "talon": SILVER}
    a = humanoid(m, mats, bulk=1.12, arm_bulk=1.1, leg_bulk=1.1, digitigrade=True, talons=True, hand_pose="fist",
                 name="aldamon")
    bd = a["body"]
    # head: helm, snout, jaw, crest, tusks, mane
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.9, 3.1, 54.5, 61.8, helmf, cut=1)
    m.box(hd, -2.0, 55.4, -7.4, 2.0, 58.6, -2.8, RED, rotation=(-8, 0, 0), pivot=(0, 57, -2.8))   # the snout
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 2.4, sx * 3.4))
        m.box(hd, x0, 55.0, -4.6, x1, 59.0, -0.4, RED, rotation=(0, sx * 18, 0), pivot=(sx * 2.4, 57, -2.5))   # cheek plates
    m.box(hd, -0.6, 58.2, -7.2, 0.6, 59.6, -2.6, GOLD)                                  # gold nose ridge
    m.box(hd, -1.8, 54.0, -6.4, 1.8, 55.6, -2.8, solid(P, "suit_dark"))                # the jaw
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 56.0, -5.0), (sx * 0.35, -0.5, -1.0), 1.0, 3.2, solid(P, "white"), tip=0.25)   # tusks
        rod(m, hd, (sx * 2.6, 60.8, -1.0), (sx * 3.6, 62.6, 1.6), 1, solid(P, "white"), extend=0.2)      # white brow horns
        spike(m, hd, (sx * 3.6, 62.6, 1.6), (sx * 0.4, 0.2, 1), 1.0, 2.2, solid(P, "white"), tip=0.25)
    spike(m, hd, (0, 61.4, -3.0), (0, 1, -0.2), 1.6, 3.0, GOLD, tip=0.3)                  # gold crest
    mane = m.bone("mane", hd, (0, 60, 2))
    for i in range(16):                                                                   # flame-hair locks
        ang = math.radians(-80 + i * (160 / 15))
        base = (2.4 * math.sin(ang), 60.0 + 1.2 * math.cos(ang), 2.0)
        tip = (6.5 * math.sin(ang), 62.0 + 4.5 * math.cos(ang) - (i % 3), 8.0 + (i % 4))
        rod(m, mane, base, tip, 2, HAIR, extend=0.4, t2=3)
    for i in range(7):                                                                    # the mane falling down its back
        x = -4.5 + i * 1.5
        rod(m, mane, (x, 58.0, 3.0), (x * 1.3, 40.0 - (i % 2) * 3, 6.5), 2, HAIR, extend=0.3, t2=2)
    # shoulders: domed pauldrons with a gold-rimmed skirt plate and a gold boss, black horns rising behind them
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = a[nm]["bone"]
        sh = a[nm]["shoulder"]
        dome(m, ab, (sh[0] + sx * 1.2, 50.5, 0.2), 4.0, 4.0, RED_PLAIN, layers=4)
        a0, a1 = (25, 160) if sx > 0 else (-160, -25)
        shell(m, ab, (sh[0] + sx * 0.6, 0, 0.2), 4.3, 45.5, 51.0, a0, a1, 7, 1.0, RED, tilt=0)
        x0, x1 = sorted((sh[0] + sx * 4.6, sh[0] + sx * 5.0))
        m.box(ab, x0, 47.0, -1.3, x1, 50.0, 1.7, GOLD)
        pts = [(sx * 7.0, 53.0, 1.8), (sx * 8.4, 58.5, 2.8), (sx * 8.0, 63.0, 5.0), (sx * 6.4, 65.0, 7.5)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, ab, p0, p1, 3 - j, HORN, extend=0.3)
        wr, el = a[nm]["wrist"], a[nm]["elbow"]
        rod(m, ab, wr, (wr[0] + (el[0] - wr[0]) * 0.18, wr[1] + (el[1] - wr[1]) * 0.18, wr[2] + (el[2] - wr[2]) * 0.18),
            4, GOLD, extend=0.1)                                                       # gold wrist cuff
    # right arm: a long gold ray-blade from the forearm, fire in the fist
    ar = a["arm_right"]["bone"]
    el, wr, hand = a["arm_right"]["elbow"], a["arm_right"]["wrist"], a["arm_right"]["hand"]
    mid = tuple((e + w) / 2 for e, w in zip(el, wr))
    rod(m, ar, mid, (mid[0] - 8.5, mid[1] - 15.0, mid[2] - 8.0), 2, GOLD, extend=0.2, t2=1)
    spike(m, ar, (mid[0] - 8.5, mid[1] - 15.0, mid[2] - 8.0), (-0.45, -0.8, -0.42), 2.0, 4.0, GOLD, tip=0.3)
    rod(m, ar, mid, (mid[0] + 2.2, mid[1] + 4.0, mid[2] + 2.6), 2, GOLD, extend=0.2, t2=1)
    fl = m.bone("flame_hand", ar, hand)
    for ang in (0, 60, 120):
        m.box(fl, hand[0] - 2.8, hand[1] - 1.0, hand[2], hand[0] + 2.8, hand[1] + 9.0, hand[2],
              cutout(flame_inside(3, 0.1, 1), flamef), rotation=(0, ang, 0), pivot=hand)
    # left arm: the tall gold kite-blade along its forearm
    al = a["arm_left"]["bone"]

    def kite(x, y, z, face, box):
        u, v, W, H = local(x, y, z, face, box)
        t = v / max(H, 1e-6)
        half = (t / 0.3 if t < 0.3 else (1 - t) / 0.7) * 0.5
        return abs(u / max(W, 1e-6) - 0.5) < half

    def kitef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        if abs(u / W - 0.5) < 0.05:
            return tone(p["gold_dark"], face), None                  # its central ridge
        return GOLD(x, y, z, face, variant, box=box, **k)
    kx = a["arm_left"]["wrist"][0] + 1.4
    kz = a["arm_left"]["wrist"][2] + 1.0
    m.box(al, kx, 18.0, kz - 3.0, kx, 46.0, kz + 3.0, cutout(kite, kitef))
    m.box(al, kx - 0.4, 18.0, kz, kx + 0.4, 46.0, kz, cutout(lambda x, y, z, f, b: kite(x, y, z, "north", b), kitef))
    # waist: belt with the crest, gold crescent tassets
    m.box(bd, -4.9, 31.0, -3.9, 4.9, 34.4, 3.9, emblemf)
    for sx in (-1, 1):
        rod(m, bd, (sx * 4.6, 31.5, -2.6), (sx * 6.4, 26.0, -3.8), 3, GOLD, extend=0.3, t2=1)
        spike(m, bd, (sx * 6.4, 26.0, -3.8), (sx * 0.1, -1, -0.6), 2.4, 3.4, GOLD, tip=0.3)
    # tail
    tl = m.bone("tail", bd, (0, 31.5, 3.6))
    pts = [(0, 31.5, 3.6), (1.5, 27.0, 8.0), (3.5, 21.0, 10.5), (5.5, 14.0, 11.0), (7.0, 8.0, 9.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 4 - j * 0.7 if j < 3 else 2, RED_PLAIN, extend=0.6)
    spike(m, tl, pts[-1], (0.3, -0.6, -0.6), 1.8, 3.0, GOLD, tip=0.3)
    # the flames flaring from its back (glowing, cut-out planes)
    fw = m.bone("wing_left", bd, (3.0, 50.0, 3.6))
    for ang, dx in ((-20, 0.0), (10, 2.0), (35, 4.0)):
        m.box(fw, 2.0 + dx, 40.0, 4.2, 16.0 + dx, 70.0, 4.2, cutout(flame_inside(5, 0.2, 2), flamef),
              rotation=(0, ang, -12), pivot=(3.0, 50.0, 4.2))
    # armour pieces over the body: knee plates, shin guards, pec plates' gold collar
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = a[nm]["bone"]
        kn = a[nm]["knee"]
        shell(m, lg, kn, 2.6, 15.0, 22.5, -80, 80, 5, 1.0, GOLD)
        dome(m, lg, (kn[0], 21.5, kn[2] + 0.2), 2.8, 2.0, GOLD, layers=2)
        spike(m, lg, (kn[0], 18.5, kn[2] - 3.2), (0, 0.3, -1), 2.0, 2.6, GOLD, tip=0.3)
        shell(m, lg, (kn[0], 0, 1.2), 2.4, 3.0, 12.0, -70, 70, 5, 0.8, RED)          # shin guard
    shell(m, bd, (0, 0, 0.6), 5.0, 42.5, 50.5, -78, 78, 9, 1.0, chestf)                  # wrap-round chest plate
    m.box(bd, -1.6, 34.0, -4.6, 1.6, 50.6, -3.6, chestf)                                   # the gold scale strip
    shell(m, bd, (0, 0, 0.6), 3.4, 50.0, 52.0, -90, 90, 7, 1.0, GOLD)                      # gold collar
    return m
