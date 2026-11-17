"""Shared builder for Chaosmon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): the fusion of
Bancho Leomon and Darkdramon. A slender knight in white, red and silver armour with long flowing teal hair, a golden
lion-head gauntlet on its left arm and a long dragon-head lance-cannon on its right, sharp swept armour plates like
blades at its hips and back, and digitigrade armoured legs.
make(valdur=True): Chaosmon: Valdur Arm, its golden god form: a halo of rainbow light behind it, great pale feathered
wings, and the lion gauntlet blazing gold. Shiny: violet armour.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import dome, humanoid
from _digidetail import armour, cutout, feathers, gem, local, metal, solid, strands
from _route import pal, tone

BASE = {"white": (236, 240, 248), "white_dark": (160, 168, 190), "red": (200, 40, 50), "red_dark": (110, 14, 20),
        "silver": (200, 204, 216), "silver_dark": (100, 104, 116), "hair": (90, 200, 180), "hair_dark": (30, 120, 110),
        "gold": (240, 196, 70), "gold_dark": (160, 110, 20), "under": (40, 40, 52), "eye": (250, 60, 60),
        "halo": (255, 220, 120, 150), "halo2": (160, 220, 255, 150), "wing": (240, 240, 250), "wing_dark": (190, 196, 214)}
SHINY = {"white": (180, 150, 230), "white_dark": (110, 80, 170), "hair": (240, 120, 160), "hair_dark": (170, 50, 90)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = armour(P, "white", "white_dark", trim="red", trim_w=0.3)
RED = armour(P, "red", "red_dark", trim="silver", trim_w=0.25)
SILVER = metal(P, "silver", dark="silver_dark")
GOLD = metal(P, "gold", dark="gold_dark")
HAIR = strands(P, "hair", "hair_dark")


def halof(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    r = math.hypot(u / max(W, 1e-6) - 0.5, v / max(H, 1e-6) - 0.5) * 2
    c = p["halo"] if r > 0.9 else p["halo2"]
    return c, c[:3]


def halo_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    r = math.hypot(u / max(W, 1e-6) - 0.5, v / max(H, 1e-6) - 0.5) * 2
    return 0.72 < r < 1.0


def make(name, valdur=False):
    def build():
        m = Model(name)
        mats = {"skin": solid(P, "under"), "chest": WHITE, "abs": RED, "pelvis": WHITE, "deltoid": RED,
                "upper_arm": solid(P, "under"), "forearm": WHITE, "hand": SILVER, "finger": SILVER, "thigh": WHITE,
                "knee": RED, "shin": WHITE, "calf": RED, "foot": SILVER, "talon": SILVER}
        a = humanoid(m, mats, bulk=0.95, arm_bulk=1.0, leg_bulk=1.0, digitigrade=True, talons=True, name=name,
                     hand_pose="fist")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.4, 2.8, 54.4, 61.0, WHITE, cut=1)
        m.box(hd, -2.0, 57.4, -3.4, 2.0, 58.0, -3.0, solid(P, "eye", glow=True))
        spike(m, hd, (0, 60.6, -1.6), (0, 1, -0.2), 1.6, 4.0, RED)
        for i in range(10):                                                 # long flowing teal hair
            ang = math.radians(-110 + i * 24)
            rod(m, hd, (2.2 * math.sin(ang), 60.0, -1.6 * math.cos(ang) + 0.8),
                (6.0 * math.sin(ang), 40.0 + abs(math.sin(ang)) * 4, 7.0 + 2.0 * math.cos(ang)), 2, HAIR,
                extend=0.4, t2=1)
        for sx in (-1, 1):                                                  # swept blade plates
            spike(m, bd, (sx * 5.0, 34.0, 1.0), (sx * 0.8, -0.6, 0.5), 2.4, 9.0, SILVER, tip=0.5)
            spike(m, bd, (sx * 3.0, 50.0, 4.0), (sx * 0.5, 0.8, 1), 2.0, 7.0, RED, tip=0.4)
            dome(m, a["arm_left" if sx > 0 else "arm_right"]["bone"], (sx * 8.0, 49.4, 0.3), 3.8, 3.6, WHITE,
                 layers=3)
        al = a["arm_left"]                                                  # golden lion-head gauntlet
        h = al["hand"]
        m.round_box(al["bone"], h[0], h[2] - 1.0, 3.4, 4.4, h[1] - 3.0, h[1] + 4.0, GOLD, cut=2)
        for i in range(10):
            ang = math.radians(i * 36)
            spike(m, al["bone"], (h[0] + 3.4 * math.cos(ang) * 0.5, h[1] + 0.5 + 3.4 * math.sin(ang), h[2] + 0.6),
                  (math.cos(ang), math.sin(ang), 0.6), 1.6, 3.0 if valdur else 2.0, GOLD, tip=0.5)
        m.box(al["bone"], h[0] - 1.6, h[1] - 0.6, h[2] - 5.6, h[0] + 1.6, h[1] + 1.2, h[2] - 5.2,
              solid(P, "eye", glow=True))
        ar = a["arm_right"]                                                 # dragon-head lance-cannon
        h = ar["hand"]
        rod(m, ar["bone"], (h[0], h[1] + 2.0, h[2] + 3.0), (h[0], h[1] - 3.0, h[2] - 24.0), 4, RED, extend=0)
        m.box(ar["bone"], h[0] - 2.4, h[1] - 4.6, h[2] - 30.0, h[0] + 2.4, h[1] - 0.6, h[2] - 22.0, SILVER)
        spike(m, ar["bone"], (h[0], h[1] - 2.4, h[2] - 30.0), (0, 0, -1), 2.4, 4.0, SILVER, tip=0.6)
        if valdur:
            hb = m.bone("halo", bd, (0, 52, 8))
            m.box(hb, -22.0, 30.0, 8.0, 22.0, 74.0, 8.0, cutout(halo_in, halof))
            wb = m.bone("wings", bd, (0, 50, 6))
            WING = feathers(P, "wing", "wing_dark", size=(1.6, 3.4), flow=(0, 1))
            for sx in (-1, 1):
                x0, x1 = sorted((sx * 2.0, sx * 30.0))
                for j, ang in enumerate((40, 20, 0, -20)):
                    m.box(wb, x0, 46.0, 5.0 + j * 0.6, x1, 54.0, 5.0 + j * 0.6, WING,
                          rotation=(0, sx * 10, sx * ang), pivot=(sx * 2.0, 50.0, 5.0 + j * 0.6))
        return m
    return build
