"""Komondomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
dust-storm dog: a big shaggy white-and-brown corded-fur dog crouched low, wearing a rust-red riveted aviator helmet with
a glowing lamp eye, side horns and an ear flap, a pair of blue goggles over its muzzle, a pink tongue, white paws and a
plumed tail. 15 blocks long.

Front is -z, y is up. 30 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, fur, gem, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "quadruped"
K = 3
LOOK = "a big shaggy white corded-fur dog in a rust-red riveted helmet with a lamp eye and side horns, blue goggles and a plumed tail"
BASE = {"white": (240, 236, 226), "white_dark": (170, 150, 130), "brown": (120, 80, 50), "rust": (160, 60, 40),
        "rust_dark": (90, 24, 14), "rust_light": (210, 120, 90), "lamp": (250, 240, 150), "lamp_light": (255, 255, 230),
        "glass": (120, 200, 230), "glass_light": (230, 250, 255), "pink": (240, 140, 160), "steel": (180, 184, 196)}
SHINY = {"white": (200, 190, 230), "white_dark": (130, 110, 170), "rust": (60, 110, 160), "rust_dark": (20, 50, 90)}


def P(v):
    return pal(BASE, SHINY, v)


CORD = fur(P, "white", "white_dark", tip="brown", length=2.4, density=1.6)
HELM = armour(P, "rust", "rust_dark", light="rust_light", rivets=True, trim="steel", trim_w=0.2)


def build():
    m = Model("komondomon")
    top = m.bone("komondomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 12.0, 4.0), 11.0, CORD, layers=6, squash=0.8)
    hd = m.bone("head", bd, (0, 14, -8))
    m.round_box(hd, 0, -9.0, 6.0, 5.0, 12.0, 20.0, CORD, cut=2)
    m.round_box(hd, 0, -9.0, 6.4, 5.4, 18.0, 23.0, HELM, cut=2)                       # aviator helmet
    m.round_box(hd, 0, -14.6, 1.6, 0.4, 19.0, 21.6, gem(P, "lamp", "lamp_light"), cut=0)
    for sx in (-1, 1):
        spike(m, hd, (sx * 6.0, 21.0, -8.0), (sx, 0.3, 0), 1.6, 6.0, HELM, tip=0.8)          # side horns
    m.round_box(hd, 0, -14.4, 5.0, 0.8, 14.0, 16.4, gem(P, "glass", "glass_light"), cut=0)      # goggles
    m.round_box(hd, 0, -14.6, 1.0, 0.6, 11.0, 13.0, solid(P, "pink"), cut=0)                    # tongue
    tb = m.bone("tail", bd, (0, 16, 14))
    for j in range(5):
        spike(m, tb, (0, 16.0, 14.0), ((j - 2) * 0.3, 1, 0.6), 2.0, 8.0, CORD, tip=0.8)
    for sx, sz, nm in ((1, -1, "leg_front_left"), (-1, -1, "leg_front_right"), (1, 1, "leg_back_left"),
                       (-1, 1, "leg_back_right")):
        lg = m.bone(nm, top, (sx * 6.0, 6.0, sz * 7.0 + 3.0))
        m.round_box(lg, sx * 6.0, sz * 7.0 + 2.0, 2.4, 3.0, 0.0, 4.0, solid(P, "white"), cut=1)
    return m
