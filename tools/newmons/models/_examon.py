"""Shared builder for Examon, the dragon Royal Knight (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a vast crimson dragon with a long armoured neck and spined back, enormous ribbed red membrane wings edged
with silver and gold spikes, a silver-armoured dragon knight's head, and the great lance Ambitious ready under its
neck, with a long tail ending in a spike. make(x=True): Examon (X-Antibody), its knight form standing upright in
silver and gold armour studded with red jewels, wings of red membrane behind, a blade of green light, gold talons and a
glowing blue core blazing over its head. Shiny: obsidian and blue.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import bat_wing, quadruped
from _digibody import humanoid
from _digidetail import armour, cutout, gem, local, metal, scales, solid
from _route import pal, tone

BASE = {"red": (190, 50, 50), "red_dark": (90, 16, 20), "red_light": (240, 130, 120), "membrane": (200, 80, 80),
        "membrane_dark": (120, 30, 30), "silver": (220, 224, 236), "silver_dark": (110, 114, 128),
        "silver_light": (255, 255, 255), "gold": (240, 196, 60), "gold_dark": (160, 110, 20), "jewel": (220, 30, 40),
        "jewel_light": (255, 150, 150), "green": (100, 250, 130, 220), "blue": (90, 200, 255, 220),
        "blue_core": (230, 250, 255, 240), "eye": (250, 220, 60), "mouth": (120, 20, 30), "tooth": (250, 250, 246)}
SHINY = {"red": (40, 40, 60), "red_dark": (12, 12, 20), "red_light": (110, 110, 140), "membrane": (60, 90, 200),
         "membrane_dark": (20, 40, 110)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "red", "red_dark", size=1.6, light="red_light", rim_mix=0.3)
SILVER = armour(P, "silver", "silver_dark", light="silver_light", trim="gold", trim_w=0.25)
GOLD = metal(P, "gold", dark="gold_dark")


def membranef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["membrane_dark"] if (u % 3.0) < 0.5 else p["membrane"], face), None


def make(name, x=False):
    def build():
        m = Model(name)
        if not x:
            mats = {"skin": HIDE, "belly": SILVER, "neck": HIDE, "head": SILVER, "snout": SILVER, "jaw": SILVER,
                    "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": HIDE, "leg_lower": SILVER,
                    "paw": SILVER, "claw": GOLD, "tail": HIDE}
            a = quadruped(m, mats, name, length=44.0, body_y=18.0, body_rx=7.0, body_ry=6.6, chest_bulk=1.3,
                          neck=((0, 24, -20), (0, 32, -28), (0, 34, -34)), head_len=10.0, head_w=3.6, head_h=4.0,
                          snout=0.7, mouth_open=12, teeth=4, leg_bulk=1.5, toes=3,
                          tail=((0, 18, 22), (0, 16, 32), (0, 14, 42), (0, 12, 52)), tail_r=(3.0, 2.2, 1.6, 1.0))
            bd, hd = a["body"], a["head"]
            ex, ey, ez = a["eye"]
            for sx in (-1, 1):
                m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.3,
                      ez + 0.6, solid(P, "eye", glow=True))
                spike(m, hd, (sx * 2.0, ey + 1.6, ez + 2.0), (sx * 0.3, 0.6, 1), 1.4, 7.0, GOLD, tip=0.3)
            for i in range(14):                                                    # spined back
                t = i / 13
                spike(m, bd if i < 9 else a["tail"], (0, 25.0 - 10.0 * t, -16.0 + 66.0 * t), (0, 1, 0.5), 1.4,
                      4.0 - 2.0 * t, GOLD, tip=0.3)
            e = a["tail_pts"][-1]
            spike(m, a["tail"], e, (0, 0, 1), 2.0, 6.0, SILVER, tip=0.4)
            lb = m.bone("lance", bd, (0, 20, -18))                                 # lance Ambitious
            rod(m, lb, (0, 20.0, -8.0), (0, 14.0, -50.0), 2, metal(P, "silver", dark="silver_dark"), extend=0)
            spike(m, lb, (0, 14.0, -50.0), (0, -0.14, -1), 2.0, 6.0, GOLD, tip=0.5)
            span = 46.0
        else:
            mats = {"skin": SILVER, "chest": SILVER, "abs": HIDE, "pelvis": SILVER, "neck": HIDE, "deltoid": SILVER,
                    "upper_arm": HIDE, "forearm": SILVER, "hand": SILVER, "finger": SILVER, "claw": GOLD,
                    "thigh": SILVER, "knee": GOLD, "shin": SILVER, "calf": SILVER, "foot": GOLD, "talon": GOLD}
            a = humanoid(m, mats, bulk=1.15, arm_bulk=1.15, leg_bulk=1.2, claws=True, talons=True, digitigrade=True,
                         name=name)
            bd = a["body"]
            hd = m.bone("head", bd, (0, 55, 0))
            m.round_box(hd, 0, -1.4, 2.8, 4.0, 54.0, 60.0, SILVER, cut=1)
            m.box(hd, -2.0, 57.0, -5.5, 2.0, 57.8, -5.3, solid(P, "eye", glow=True))
            for sx in (-1, 1):
                spike(m, hd, (sx * 2.0, 59.6, 0), (sx * 0.4, 1, 0.5), 1.4, 7.0, GOLD, tip=0.3)
                for j in range(3):                                                 # red jewels
                    m.box(bd, sx * (2.0 + j * 1.6) - 0.6, 46.0 - j * 2.0, a["chest_front"] - 0.6, sx * (2.0 + j * 1.6)
                          + 0.6, 47.2 - j * 2.0, a["chest_front"], gem(P, "jewel", "jewel_light"))
            ar = a["arm_right"]                                                    # green light blade
            hx, hy, hz = ar["hand"]
            rod(m, ar["bone"], (hx, hy, hz), (hx - 2.0, hy + 30.0, hz - 6.0), 1, solid(P, "green", glow=True),
                extend=0, t2=2)
            cb = m.bone("core", hd, (0, 66, 0))                                    # blazing blue core
            m.round_box(cb, 0, 0, 3.0, 3.0, 63.0, 69.0, solid(P, "blue", glow=True), cut=1)
            m.round_box(cb, 0, -1.0, 1.4, 1.4, 64.6, 67.4, solid(P, "blue_core", glow=True), cut=0)
            bd = a["body"]
            span = 34.0
        for side in (1, -1):                                                       # ribbed membrane wings
            root = (side * 4.0, 26.0 if not x else 50.0, -2.0 if not x else 3.6)
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, root)
            bat_wing(m, wb, root, span, span * 0.8, 5, SILVER, cutout(lambda *a_: True, membranef), side=side, sweep=25)
        return m
    return build
