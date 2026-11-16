"""Amphimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a magenta battle-cyborg. Heavy rounded magenta plates over grey joints, big round pauldrons and knee
caps with blue emblems, oversized armoured fists, a pale skirt of feathered fins with long green ribbons streaming
behind, and two long tendrils from its back that end in glassy jellyfish orbs marked with a plus and a minus.
35 blocks tall.

Front is -z, y is up. 68 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import dome, humanoid, shell
from _digidetail import armour, gem, local, metal, plane, solid
from _route import pal, tone

HEIGHT = 68
SCALE, HITBOX = sized(35, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a magenta battle-cyborg: rounded magenta plates over grey joints, round pauldrons and knee caps with blue "
        "emblems, big armoured fists, a feathered fin skirt with green ribbons and two tendrils ending in plus and "
        "minus jellyfish orbs")
BASE = {"pink": (214, 40, 120), "pink_dark": (120, 14, 64), "pink_light": (255, 130, 190), "grey": (130, 132, 146),
        "grey_dark": (60, 62, 72), "grey_light": (200, 204, 214), "blue": (60, 120, 230), "blue_light": (170, 210, 255),
        "fin": (246, 220, 236), "fin_dark": (210, 170, 196), "ribbon": (190, 236, 160), "ribbon_dark": (110, 170, 90),
        "orb": (230, 200, 255, 170), "orb_rim": (180, 140, 230), "plus": (255, 220, 60), "eye": (120, 230, 255)}
SHINY = {"pink": (240, 170, 30), "pink_dark": (160, 100, 10), "pink_light": (255, 230, 140), "blue": (220, 40, 60),
         "blue_light": (255, 160, 170)}


def P(v):
    return pal(BASE, SHINY, v)


PINK = armour(P, "pink", "pink_dark", light="pink_light", seams=(3.5,))
PINK_TRIM = armour(P, "pink", "pink_dark", light="pink_light", trim="grey_light")
GREY = metal(P, "grey", dark="grey_dark", light="grey_light")
GEM = gem(P, "blue", "blue_light")


def emblemf(x, y, z, face, variant, box=None, **k):
    """A round plate with a blue emblem disc in its outer face."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if math.hypot(u - W / 2, v - H / 2) < min(W, H) * 0.3 and face not in ("up", "down"):
        return tone(p["blue"], face), None
    return PINK(x, y, z, face, variant, box=box, **k)


def orbf(sign):
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        du, dv = u - W / 2, v - H / 2
        bar = abs(dv) < 0.45 and abs(du) < W * 0.32
        if sign > 0:
            bar = bar or (abs(du) < 0.45 and abs(dv) < H * 0.32)
        if bar and face in ("north", "south"):
            return p["plus"], p["plus"]
        if min(u, W - u, v, H - v) < 0.5:
            return tone(p["orb_rim"], face), None
        return p["orb"], None
    return s


def build():
    m = Model("amphimon")
    mats = {"skin": GREY, "chest": PINK_TRIM, "abs": GREY, "pelvis": PINK, "neck": GREY, "deltoid": emblemf,
            "upper_arm": GREY, "forearm": PINK, "hand": PINK, "finger": PINK, "thigh": PINK, "knee": emblemf,
            "shin": PINK, "calf": PINK, "foot": PINK, "toe": GREY}
    a = humanoid(m, mats, bulk=1.1, arm_bulk=1.35, leg_bulk=1.4, name="amphimon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.3, 2.6, 2.8, 54.6, 60.4, PINK_TRIM, cut=1)
    m.box(hd, -2.0, 56.8, -3.4, 2.0, 58.2, -2.6, solid(P, "eye", glow=True))            # visor
    rod(m, hd, (0, 60.0, -1.0), (0, 62.5, 2.5), 2, PINK, extend=0.3)
    shell(m, bd, (0, 0, 0.6), 5.6, 42.0, 51.0, -85, 85, 9, 1.2, PINK_TRIM)
    m.round_box(bd, 0, -6.0, 1.2, 0.6, 45.6, 48.2, GEM, cut=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = a[nm]["bone"]
        sh = a[nm]["shoulder"]
        ball(m, ab, (sh[0] + sx * 1.8, 49.0, 0.3), 4.6, emblemf, layers=4)
        hand = a[nm]["hand"]
        m.round_box(ab, hand[0], hand[2], 2.8, 2.8, hand[1] - 3.4, hand[1] + 2.6, PINK, cut=1)   # big fist
        for j in range(4):
            m.box(ab, hand[0] - 2.9, hand[1] - 3.2 + j * 1.4, hand[2] - 3.0, hand[0] + 2.9, hand[1] - 2.4 + j * 1.4,
                  hand[2] - 2.6, GREY)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg, kn = a[nm]["bone"], a[nm]["knee"]
        ball(m, lg, (kn[0], 18.5, kn[2] - 1.0), 3.2, emblemf, layers=3)
        m.round_box(lg, kn[0], 0.0, 3.4, 4.2, 0.0, 4.0, PINK, cut=1)                    # heavy boots
    sk = m.bone("skirt", bd, (0, 31, 0))
    for i in range(12):                                          # feathered fin skirt, longer at the back
        ang = math.radians(-180 + i * 30)
        back = 0.5 + 0.5 * math.cos(ang)
        c = (5.0 * math.sin(ang), 31.0, -4.6 * math.cos(ang))
        ln = 8.0 + 10.0 * back
        m.box(sk, c[0] - 1.8, 31.0 - ln, c[2], c[0] + 1.8, 31.0, c[2], solid(P, "fin"),
              rotation=(-22 * math.cos(ang), -math.degrees(ang), 0), pivot=c)
    for i in range(6):                                           # green ribbons streaming behind
        x = -5 + i * 2
        rod(m, sk, (x, 30.0, 3.5), (x * 2.2, 14.0, 16.0 + (i % 3) * 3), 1, solid(P, "ribbon"), extend=0.3, t2=2)
    for sx, sign in ((1, 1), (-1, -1)):                          # tendrils with jellyfish orbs
        tb = m.bone("tail" if sx > 0 else "tail_2", bd, (sx * 2.5, 48.0, 3.5))
        pts = [(sx * 2.5, 48.0, 3.5), (sx * 10.0, 58.0, 8.0), (sx * 20.0, 62.0, 6.0), (sx * 27.0, 56.0, 2.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tb, p0, p1, 1, solid(P, "grey_dark"), extend=0.3)
        e = pts[-1]
        ball(m, tb, (e[0], e[1] - 2.0, e[2]), 3.0, orbf(sign), layers=3)
        for j in range(4):
            rod(m, tb, (e[0] + (j - 1.5), e[1] - 4.5, e[2]), (e[0] + (j - 1.5) * 1.4, e[1] - 10.0, e[2] + 1), 1,
                solid(P, "ribbon"), extend=0.2)
    return m
