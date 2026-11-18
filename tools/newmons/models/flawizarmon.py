"""Fla Wizarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the flame wizard. A slim wizard in a long red coat with gold buttons and a high collar, a broad
red wizard's hat crowned with welding goggles and sprouting a crest of flames, a scarf over the lower face so only
two sharp eyes show, black gloves (the left hand wreathed in blue fire), red boots and a long staff topped with a
golden sun ring. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import cutout, fabric, flame_inside, leather, local, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a slim wizard in a long red coat with gold buttons, a broad red hat with goggles and a crest of flames, a face "
        "scarf, black gloves with blue fire in one hand and a staff topped with a gold sun ring")
BASE = {"red": (200, 40, 40), "red_dark": (110, 14, 18), "gold": (240, 200, 70), "gold_dark": (160, 120, 20),
        "black": (34, 32, 40), "black_dark": (14, 14, 20), "scarf": (230, 220, 200), "scarf_dark": (170, 160, 140),
        "eye": (250, 220, 60), "lens": (120, 200, 230), "staff": (110, 70, 40), "fire": (255, 170, 40, 210),
        "fire_core": (255, 245, 180, 235), "blue": (90, 170, 255, 210), "blue_core": (220, 245, 255, 235)}
SHINY = {"red": (60, 50, 140), "red_dark": (24, 18, 70), "fire": (180, 90, 255, 210), "fire_core": (240, 210, 255, 235)}


def P(v):
    return pal(BASE, SHINY, v)


COAT = fabric(P, "red", "red_dark", axis="y")
GLOVE = leather(P, "black", "black_dark")


def coatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 0.5 and (y * 0.5) % 2.0 < 0.6:
        return tone(p["gold"], face), None
    return COAT(x, y, z, face, variant, box=box, **k)


def firef(key, core):
    def f(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p[core] if v / max(H, 1e-6) < 0.3 else p[key]
        return c, c[:3]
    return f


def flame(m, bone, at, w, h, seed, key="fire", core="fire_core"):
    for ang in (0, 90):
        m.box(bone, at[0] - w / 2, at[1], at[2], at[0] + w / 2, at[1] + h, at[2],
              cutout(flame_inside(4, 0.1, seed), firef(key, core)), rotation=(0, ang, 0), pivot=at)


def build():
    m = Model("flawizarmon")
    mats = {"skin": COAT, "chest": coatf, "abs": coatf, "pelvis": COAT, "neck": solid(P, "scarf"), "deltoid": COAT,
            "upper_arm": COAT, "forearm": COAT, "hand": GLOVE, "finger": GLOVE, "thigh": COAT, "knee": COAT,
            "shin": leather(P, "red", "red_dark"), "calf": leather(P, "red", "red_dark"), "foot": GLOVE, "toe": GLOVE}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.9, leg_bulk=0.9, name="flawizarmon")
    bd = a["body"]
    for sx in (-1, 1):                                                                 # long coat tails
        x0, x1 = sorted((sx * 0.6, sx * 5.0))
        m.box(bd, x0, 16.0, 2.6, x1, 32.0, 3.6, COAT, rotation=(-6, 0, sx * 6), pivot=(sx * 2.0, 32.0, 3.0))
    m.round_box(bd, 0, 0.0, 4.4, 3.4, 49.6, 53.0, COAT, cut=1)                          # high collar
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.6, 2.6, 53.0, 59.0, solid(P, "scarf"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 57.0, -2.8, max(sx * 0.6, sx * 1.8), 57.6, -2.6, solid(P, "eye", glow=True))
    m.round_box(hd, 0, 0, 7.0, 7.0, 58.8, 60.0, COAT, cut=3)                            # broad brim
    m.round_box(hd, 0, 0.4, 3.4, 3.4, 59.6, 63.6, COAT, cut=1)                          # crown
    m.round_box(hd, 0, 0.4, 3.6, 3.6, 61.6, 62.6, solid(P, "black"), cut=1)             # goggle strap
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.4, -3.2, 1.0, 0.4, 61.0, 63.2, solid(P, "lens"), cut=0)
    for j in range(3):
        flame(m, hd, ((j - 1) * 1.6, 63.4, 0.4 + abs(j - 1) * 0.6), 3.0, 6.0 - abs(j - 1) * 1.4, j + 2)
    hl = a["arm_left"]["hand"]                                                           # blue fire in the left hand
    flame(m, a["arm_left"]["bone"], (hl[0], hl[1] + 1.0, hl[2] - 1.0), 3.0, 5.0, 8, "blue", "blue_core")
    hr = a["arm_right"]["hand"]                                                          # the staff
    ar = a["arm_right"]["bone"]
    rod(m, ar, (hr[0], 4.0, hr[2] - 1.0), (hr[0], 60.0, hr[2] - 1.0), 1, solid(P, "staff"), extend=0)
    for i in range(10):
        a0, a1 = 2 * math.pi * i / 10, 2 * math.pi * (i + 1) / 10
        rod(m, ar, (hr[0] + 3.0 * math.cos(a0), 63.0 + 3.0 * math.sin(a0), hr[2] - 1.0),
            (hr[0] + 3.0 * math.cos(a1), 63.0 + 3.0 * math.sin(a1), hr[2] - 1.0), 1,
            metal(P, "gold", dark="gold_dark"), extend=0.3)
    return m
