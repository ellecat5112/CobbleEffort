"""Ajatarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a warrior of the forest made of living vines: fibrous green limbs studded with thorns and tipped
with blood-red buds, baggy chartreuse trousers stitched in green, leather straps and pouches across its chest, a round
carved wooden mask with deep-set eyes under a crest of green, red and yellow leaf-spikes, a bandaged fist, a dark
curved sickle-hatchet, and thorny vines curling up from its back. 25 blocks tall.

Front is -z, y is up. 74 units tall (the vines); Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import (cutout, fabric, leather, local, metal, mix, mul, riveted, skin, solid, strands, twisted)
from _route import pal, tone

HEIGHT = 74
SCALE, HITBOX = sized(25, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = ("a vine warrior: thorny fibrous green limbs tipped with red buds, baggy chartreuse trousers, leather straps and "
        "pouches, a carved wooden mask under a crest of green, red and yellow leaf-spikes, a bandaged fist, a dark "
        "sickle-hatchet and thorny vines curling from its back")

BASE = {"vine": (70, 142, 58), "vine_dark": (30, 76, 32), "vine_light": (150, 200, 96), "bud": (176, 40, 52),
        "bud_dark": (106, 20, 34), "pants": (196, 214, 54), "pants_dark": (128, 148, 30), "stitch": (70, 120, 40),
        "leather": (150, 104, 62), "leather_dark": (90, 58, 30), "mask": (170, 134, 92), "mask_dark": (100, 74, 48), "bronze": (160, 136, 96), "bronze_dark": (90, 72, 48), "bronze_light": (230, 214, 170),
        "eye": (240, 220, 120), "pupil": (20, 16, 10), "white": (250, 250, 244), "bandage": (236, 230, 214),
        "bandage_dark": (180, 170, 150), "blade": (54, 66, 60), "blade_light": (190, 214, 200), "blade_dark": (20, 26, 24),
        "thorn": (216, 210, 170), "leaf_g": (60, 170, 70), "leaf_r": (200, 50, 50), "leaf_y": (240, 210, 60),
        "purple": (110, 80, 150)}
SHINY = {"vine": (150, 110, 60), "vine_dark": (90, 60, 30), "vine_light": (210, 180, 110), "pants": (230, 150, 60),
         "pants_dark": (170, 100, 30), "leaf_g": (220, 120, 40), "bud": (120, 60, 180), "bud_dark": (70, 30, 120)}


def P(v):
    return pal(BASE, SHINY, v)


VINE = twisted(P, "vine", "vine_dark", light="vine_light", period=2.0, angle=0.7)
PANTS = fabric(P, "pants", "pants_dark", axis="y", period=2.2)
LEATHER = leather(P, "leather", "leather_dark", stitch="bandage_dark")
BAND = fabric(P, "bandage", "bandage_dark", axis="x", period=1.2)
BLADE = metal(P, "blade", dark="blade_dark", light="blade_light", streak=5.0)
BUD = skin(P, "bud", dark="bud_dark")
LEAVES = [strands(P, k, "vine_dark") for k in ("leaf_g", "leaf_r", "leaf_y")]


def thorns(m, bone, a, b, n, size=0.9):
    """Pale thorns along a vine from a to b, pointing outward round it."""
    for i in range(n):
        t = (i + 0.5) / n
        p = tuple(a[j] + (b[j] - a[j]) * t for j in range(3))
        ang = i * 2.4
        d = (math.cos(ang), 0.25, math.sin(ang))
        spike(m, bone, (p[0] + d[0] * 1.2, p[1], p[2] + d[2] * 1.2), d, size, size * 1.8, solid(P, "thorn"), tip=0.2)


def maskf(x, y, z, face, variant, box=None, **k):
    """A round carved wooden mask: deep-set eye holes with glinting eyes, a carved mouth slit, wood grain."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.2, (y - 58.6) * 1.3)
            if d < 0.5:
                return p["eye"], p["eye"]
            if d < 1.0:
                return tone(p["pupil"], face), None
        if abs(y - 56.3) < 0.25 and abs(x) < 1.6:
            return tone(p["mask_dark"], face), None
    grain = 0.5 + 0.5 * math.sin((x * 0.5 + y * 3.0) + math.sin(y * 1.3) * 2)
    return tone(mix(p["mask_dark"], p["mask"], 0.6 + 0.4 * grain), face), None


def build():
    m = Model("ajatarmon")
    mats = {"skin": VINE, "chest": VINE, "abs": VINE, "pelvis": PANTS, "neck": VINE, "deltoid": VINE,
            "upper_arm": VINE, "forearm": VINE, "hand": BAND, "finger": BAND, "thigh": PANTS, "knee": PANTS,
            "shin": VINE, "calf": VINE, "foot": BUD, "talon": BUD}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.15, leg_bulk=1.15, digitigrade=True, talons=True, hand_pose="fist",
                 name="ajatarmon")
    bd = a["body"]
    # baggy trousers: billowing shells round the thighs, gathered at the knee
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg, hip, kn = a[nm]["bone"], a[nm]["hip"], a[nm]["knee"]
        mid = tuple((h + k) / 2 for h, k in zip(hip, kn))
        m.round_box(lg, mid[0] + hip[0] * 0.12, mid[2] - 0.4, 3.0, 3.2, kn[1] + 1.0, hip[1] + 0.5, PANTS, cut=1)   # baggy leg
        m.round_box(lg, mid[0] + hip[0] * 0.18, mid[2] - 0.6, 3.5, 3.6, kn[1] + 3.5, hip[1] - 4.0, PANTS, cut=1)
        m.round_box(lg, kn[0], kn[2], 2.4, 2.4, 17.5, 20.0, LEATHER, cut=1)          # leather knee binding
        thorns(m, lg, (kn[0], 16.0, kn[2] + 1), a[nm]["ankle"], 4)
    m.box(bd, -4.9, 33.5, -3.8, 4.9, 35.5, 3.8, LEATHER)                              # belt
    m.round_box(bd, 3.2, -3.6, 1.6, 1.0, 30.5, 33.8, LEATHER, cut=1)                 # pouch
    # leather straps crossing the chest, pouches on the shoulders
    for sx in (-1, 1):
        m.box(bd, -0.8, 35.0, -4.6, 0.8, 52.0, -3.9, LEATHER, rotation=(0, 0, sx * 32), pivot=(0, 43, -4))
        m.round_box(bd, sx * 6.2, 0.2, 2.6, 3.0, 49.0, 53.0, LEATHER, cut=1)
    # thorns down the arms
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = a[nm]["bone"]
        thorns(m, ab, a[nm]["shoulder"], a[nm]["elbow"], 3)
        thorns(m, ab, a[nm]["elbow"], a[nm]["wrist"], 3)
        wr, el = a[nm]["wrist"], a[nm]["elbow"]
        rod(m, ab, wr, tuple(w + (e - w) * 0.35 for w, e in zip(wr, el)), 4, BAND, extend=0.2)   # bandaged wrist
    # the sickle-hatchet in its right hand: a long handle and a dark crescent blade
    ar = a["arm_right"]["bone"]
    h = a["arm_right"]["hand"]
    rod(m, ar, (h[0], h[1] + 4.0, h[2] + 3.0), (h[0], h[1] - 8.0, h[2] - 6.0), 1, LEATHER, extend=0.2)

    def crescent(x, y, z, face, box):
        u, v, W, H = local(x, y, z, face, box)
        cu, cv = W * 0.15, H * 0.5
        d1 = math.hypot(u - cu, (v - cv) * 0.8)
        d2 = math.hypot(u - cu + W * 0.18, (v - cv) * 0.8)
        return d1 < W * 0.9 and d2 > W * 0.82 and u > 0.1
    bx = h[0]
    m.box(ar, bx, h[1] - 18.0, h[2] - 14.0, bx, h[1] + 2.0, h[2] - 4.0, cutout(crescent, BLADE),
          rotation=(0, 0, 0), pivot=(bx, h[1] - 8, h[2] - 6))
    # head: the carved mask, a wooden hood, the leaf-spike crest
    hd = m.bone("head", bd, (0, 55, 0))
    BRONZE = riveted(P, "bronze", "bronze_dark", light="bronze_light", spacing=2.0)
    for i, (y0, y1, r) in enumerate(((53.6, 55.0, 2.4), (54.8, 56.6, 3.2), (56.4, 59.6, 3.6), (59.4, 61.0, 3.2),
                                      (60.8, 62.0, 2.3))):
        m.round_box(hd, 0, 0.2, r, r, y0, y1, BRONZE, cut=max(1, round(r * 0.4)))     # the round helmet
    m.box(hd, -2.4, 55.2, -3.9, 2.4, 60.2, -3.4, maskf)                                 # the carved mask face
    crest = m.bone("mane", hd, (0, 61, 0))
    for i in range(15):
        ang = math.radians(-75 + i * (150 / 14))
        base = (2.8 * math.sin(ang), 61.2, 0.8 * math.cos(ang))
        d = (math.sin(ang) * 0.9, 1.0, 0.25)
        spike(m, crest, base, d, 1.2, 5.0 + 2.0 * (i % 2), LEAVES[i % 3], tip=0.25)
    # vines curling up from its back
    for sx, nm in ((1, "vine_left"), (-1, "vine_right")):
        vb = m.bone(nm, bd, (sx * 2.5, 48.0, 3.5))
        pts = [(sx * 2.5, 48.0, 3.5), (sx * 6.0, 56.0, 7.5), (sx * 9.0, 64.0, 7.0), (sx * 8.5, 71.0, 3.0),
               (sx * 5.5, 73.5, 0.0), (sx * 3.6, 71.0, -1.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, vb, p0, p1, 2.6 - j * 0.35, VINE, extend=0.4)
            thorns(m, vb, p0, p1, 2, 0.7)
        m.round_box(vb, pts[-1][0], pts[-1][2], 1.2, 1.2, pts[-1][1] - 1.6, pts[-1][1] + 0.8, BUD, cut=0)
    return m
