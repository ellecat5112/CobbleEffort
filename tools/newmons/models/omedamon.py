"""Omedamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the holy mechanical warrior: a sleek white-and-lavender mecha knight with glowing cyan cores, a horned
crested helm, a golden shoulder cannon pack, a crystal-yellow sword in one hand wreathed in blue fire and a heavy
black cannon on the other arm blazing with orange fire. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, cutout, flame_inside, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a sleek white-and-lavender mecha knight with cyan cores, a horned helm, a golden shoulder cannon, a crystal "
        "sword in blue fire and a black arm cannon blazing orange")
BASE = {"white": (236, 238, 248), "white_dark": (150, 154, 180), "lavender": (130, 120, 210), "lav_dark": (60, 50, 130),
        "gold": (240, 200, 70), "gold_dark": (160, 120, 20), "cyan": (100, 230, 250), "cyan_light": (220, 250, 255),
        "black": (40, 40, 48), "crystal": (250, 240, 140, 210), "blue_f": (120, 200, 255, 200), "orange_f": (255, 160, 40, 210),
        "core": (255, 250, 220, 235)}
SHINY = {"white": (60, 60, 72), "white_dark": (24, 24, 30), "lavender": (200, 60, 70), "lav_dark": (120, 20, 30)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = armour(P, "white", "white_dark", trim="lavender", trim_w=0.3)
LAV = armour(P, "lavender", "lav_dark", trim="white", trim_w=0.25)
CORE = gem(P, "cyan", "cyan_light")


def firef(key):
    def f(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p["core"] if v / max(H, 1e-6) < 0.25 else p[key]
        return c, c[:3]
    return cutout(flame_inside(4, 0.1, 4), f)


def build():
    m = Model("omedamon")
    mats = {"skin": WHITE, "abs": LAV, "neck": LAV, "upper_arm": LAV, "thigh": LAV, "hand": LAV, "finger": LAV,
            "knee": LAV, "foot": LAV, "toe": LAV}
    a = humanoid(m, mats, bulk=1.1, arm_bulk=1.05, leg_bulk=1.1, name="omedamon")
    bd = a["body"]
    ball(m, bd, (0, 46.0, -4.4), 1.6, CORE, layers=2)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.0, 60.0, WHITE, cut=1)
    m.box(hd, -2.0, 57.0, -3.3, 2.0, 57.8, -3.1, solid(P, "cyan", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.6, 60.0, -0.6), (sx * 0.5, 1, 0.5), 1.4, 8.0, LAV, tip=0.8)       # horned crest
    m.round_box(bd, 8.0, 1.0, 3.0, 3.0, 50.0, 56.0, metal(P, "gold", dark="gold_dark"), cut=1)   # shoulder cannon
    rod(m, bd, (8.0, 56.0, 1.0), (10.0, 64.0, -2.0), 3, solid(P, "black"), extend=0.4)
    ar = a["arm_right"]                                                                  # crystal sword
    h = ar["hand"]
    m.box(ar["bone"], h[0] - 2.0, h[1] - 0.6, h[2] - 1.0, h[0] + 2.0, h[1] + 0.6, h[2] + 1.0, metal(P, "gold"))
    m.box(ar["bone"], h[0] - 1.4, h[1] - 24.0, h[2] - 0.4, h[0] + 1.4, h[1] - 0.6, h[2] + 0.4,
          solid(P, "crystal", glow=True), rotation=(-30, 0, -25), pivot=(h[0], h[1], h[2]))
    for ang in (0, 90):
        m.box(ar["bone"], h[0] - 3.0, h[1] - 6.0, h[2], h[0] + 3.0, h[1] + 6.0, h[2], firef("blue_f"),
              rotation=(0, ang, 0), pivot=(h[0], h[1], h[2]))
    al = a["arm_left"]                                                                   # black arm cannon
    w = al["wrist"]
    rod(m, al["bone"], (w[0], w[1] + 2.0, w[2]), (w[0] + 2.0, w[1] - 8.0, w[2] - 10.0), 5, solid(P, "black"),
        extend=0.6)
    for ang in (0, 90):
        m.box(al["bone"], w[0] - 3.0, w[1] - 10.0, w[2] - 12.0, w[0] + 7.0, w[1] - 4.0, w[2] - 12.0, firef("orange_f"),
              rotation=(0, ang, 0), pivot=(w[0] + 2.0, w[1] - 7.0, w[2] - 12.0))
    return m
