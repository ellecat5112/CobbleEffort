"""Dullahamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the headless rider. A black ghost horse barded in black, gold and red, its mane and fetlocks
ragged black smoke shot with glowing green fire, with a glowing green eye in its masked head; on its back a headless
knight in black-and-silver armour wielding a great spiked flail on a chain and holding a huge dark crescent axe,
green ghost-fire licking round them both. 35 blocks tall.

Front is -z, y is up. 56 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digibody import humanoid
from _digidetail import armour, cutout, fabric, flame_inside, local, metal, skin, solid
from _dorbickmon import mount
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a black ghost horse barded in black, gold and red with a smoky green-fire mane, ridden by a headless black-and-"
        "silver knight with a spiked flail and a huge crescent axe")
BASE = {"black": (34, 32, 40), "black_dark": (10, 10, 14), "black_light": (100, 96, 120), "gold": (230, 180, 60),
        "red": (170, 30, 40), "red_dark": (90, 10, 16), "silver": (200, 204, 216), "silver_dark": (100, 104, 116),
        "green": (90, 250, 120, 210), "green_core": (220, 255, 220, 235), "smoke": (30, 30, 36), "eye": (90, 250, 120)}
SHINY = {"black": (230, 230, 236), "black_dark": (150, 150, 160), "green": (160, 120, 255, 210),
         "green_core": (230, 220, 255, 235), "eye": (160, 120, 255)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "black", dark="black_dark", light="black_light")
BARD = armour(P, "black", "black_dark", light="black_light", trim="gold", trim_w=0.4)
SILVER = metal(P, "silver", dark="silver_dark")


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["green_core"] if v / max(H, 1e-6) < 0.3 else p["green"]
    return c, c[:3]


def flames(m, bone, at, w, h, seed):
    for ang in (0, 90):
        m.box(bone, at[0] - w / 2, at[1], at[2], at[0] + w / 2, at[1] + h, at[2], cutout(flame_inside(4, 0.1, seed),
              firef), rotation=(0, ang, 0), pivot=at)


def build():
    m = Model("dullahamon")
    mats = {"skin": HIDE, "belly": BARD, "neck": BARD, "head": BARD, "snout": HIDE, "jaw": HIDE,
            "mouth": solid(P, "black_dark"), "tooth": solid(P, "silver"), "leg_upper": BARD, "leg_lower": HIDE,
            "paw": HIDE, "claw": solid(P, "black"), "tail": HIDE}
    a = quadruped(m, mats, "dullahamon", length=36.0, body_y=20.0, body_rx=6.4, body_ry=6.4, chest_bulk=1.2,
                  neck=((0, 26, -16), (0, 33, -20)), head_len=10.0, head_w=3.0, head_h=3.8, snout=0.8, mouth_open=6,
                  teeth=0, leg_len=14.0, leg_bulk=1.4, toes=1, claws=False,
                  tail=((0, 24, 18), (0, 20, 24), (0, 14, 26)), tail_r=(1.6, 1.4, 1.2))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    m.box(hd, -ex - 0.3, ey - 0.4, ez - 0.6, -ex, ey + 0.4, ez + 0.6, solid(P, "eye", glow=True))        # green eye
    m.round_box(bd, 0, 0, 7.0, 10.0, 16.0, 22.0, fabric(P, "red", "red_dark"), cut=2)                   # red barding
    for i in range(6):                                                                                 # fiery mane
        flames(m, a["neck"], (0, 30.0 + i * 0.6, -14.0 - i * 1.2), 3.0, 5.0, i)
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        w = a[nm]["wrist"]
        flames(m, a[nm]["bone"], (w[0], 0.0, w[2]), 3.0, 4.0, len(nm))                                 # fetlocks
    flames(m, a["tail"], a["tail_pts"][-1], 4.0, 6.0, 9)
    i_box, i_bone = len(m.boxes), len(m.bones)                                                         # the rider
    mats = {"skin": BARD, "chest": BARD, "abs": solid(P, "black"), "pelvis": BARD, "neck": BARD, "deltoid": SILVER,
            "upper_arm": BARD, "forearm": SILVER, "hand": BARD, "finger": BARD, "thigh": BARD, "knee": SILVER,
            "shin": BARD, "calf": BARD, "foot": BARD, "toe": BARD}
    r = humanoid(m, mats, bulk=0.9, arm_bulk=0.9, leg_bulk=0.9, name="rider")
    flames(m, r["body"], (0, 51.0, 0), 4.0, 6.0, 3)                                                   # fire for a head
    ar = r["arm_right"]                                                                                # spiked flail
    hx, hy, hz = ar["hand"]
    for j in range(5):
        m.box(ar["bone"], hx - 0.5, hy + 1.0 + j * 1.2, hz - 0.5 - j * 1.4, hx + 0.5, hy + 2.0 + j * 1.2,
              hz + 0.5 - j * 1.4, SILVER)
    m.round_box(ar["bone"], hx, hz - 9.0, 2.6, 2.6, hy + 7.0, hy + 12.0, BARD, cut=1)
    for ang in range(0, 360, 60):
        rr = math.radians(ang)
        spike(m, ar["bone"], (hx + 2.4 * math.cos(rr), hy + 9.5, hz - 9.0 + 2.4 * math.sin(rr)),
              (math.cos(rr), 0, math.sin(rr)), 1.0, 2.4, SILVER)
    al = r["arm_left"]                                                                                 # crescent axe
    hx, hy, hz = al["hand"]
    rod(m, al["bone"], (hx, hy - 10.0, hz), (hx, hy + 14.0, hz), 1, solid(P, "black"), extend=0)
    for j in range(5):
        ang = math.radians(-70 + j * 35)
        rod(m, al["bone"], (hx, hy + 10.0, hz), (hx + 8.0 * math.cos(ang), hy + 10.0 + 8.0 * math.sin(ang), hz), 1,
            SILVER, extend=0.3, t2=2)
    m.boxes[i_box:] = [bx for bx in m.boxes[i_box:] if bx.bone not in ("leg_left", "leg_right")]   # seated: no legs
    m.bones[i_bone:] = [bn for bn in m.bones[i_bone:] if bn["name"] not in ("leg_left", "leg_right")]
    for sx in (-1, 1):                                                                                 # thighs astride
        rod(m, r["body"], (sx * 3.0, 32.0, 0.0), (sx * 7.4, 26.0, -3.0), 4, BARD, extend=0.6)
        rod(m, r["body"], (sx * 7.4, 26.0, -3.0), (sx * 7.8, 18.0, -1.0), 3, BARD, extend=0.6)
        m.round_box(r["body"], sx * 7.8, -2.0, 1.8, 2.6, 16.0, 19.0, SILVER, cut=1)
    mount(m, i_box, i_bone, -6.0, 2.0, "body")
    return m
