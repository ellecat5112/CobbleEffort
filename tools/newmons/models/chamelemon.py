"""Chamelemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Armor chameleon. A crouching green chameleon banded with red stripes, a crested casque head with
goggles pushed down over one bulging spiral eye, a toothy grin, a strap round its neck, clawed toes and a very long
red-banded tail curled into a spiral. 15 blocks tall.

Front is -z, y is up. 26 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import gem, leather, local, scales, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a crouching green chameleon banded with red stripes, a crested casque head with goggles over a spiral eye "
        "and a very long red-banded spiral tail")
BASE = {"green": (90, 170, 60), "green_dark": (40, 100, 24), "green_light": (170, 220, 120), "red": (220, 60, 50),
        "red_dark": (140, 24, 20), "eye": (230, 220, 90), "pupil": (40, 60, 20), "goggle": (180, 220, 240),
        "goggle_light": (240, 250, 255), "strap": (120, 80, 40), "strap_dark": (70, 40, 20), "claw": (240, 240, 236),
        "mouth": (120, 20, 20), "tooth": (250, 250, 246)}
SHINY = {"green": (240, 150, 50), "green_dark": (170, 80, 10), "green_light": (255, 210, 130), "red": (60, 120, 220),
         "red_dark": (20, 60, 150)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "green", "green_dark", size=1.4, light="green_light", rim_mix=0.3)


def banded(axis="x"):
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        t = {"x": z, "y": y, "t": z + y}[axis]
        if t % 4.0 < 1.4 and face not in ("down",):
            return tone(p["red"] if t % 4.0 > 0.3 else p["red_dark"], face), None
        return HIDE(x, y, z, face, variant, box=box, **k)
    return s


def eyef(x, y, z, face, variant, box=None, **k):
    """A bulging spiral eye on the side of the head."""
    p = P(variant)
    if face in ("east", "west"):
        u, v, W, H = local(x, y, z, face, box)
        a, b = u - W / 2, v - H / 2
        r, th = math.hypot(a, b), math.atan2(b, a)
        if abs(((r * 2.2 - th / math.pi) % 1.0) - 0.5) < 0.18:
            return tone(p["pupil"], face), None
        return tone(p["eye"], face), None
    return HIDE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("chamelemon")
    mats = {"skin": banded("x"), "belly": HIDE, "neck": HIDE, "head": HIDE, "snout": HIDE, "jaw": HIDE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": banded("y"), "leg_lower": banded("y"),
            "paw": HIDE, "claw": solid(P, "claw"), "tail": banded("t")}
    a = quadruped(m, mats, "chamelemon", length=22.0, body_y=11.0, body_rx=5.4, body_ry=6.0, chest_bulk=1.2,
                  neck=((0, 13, -12), (0, 14, -15)), head_len=11.0, head_w=4.4, head_h=4.4, snout=0.5, mouth_open=6,
                  teeth=5, leg_bulk=1.2, toes=3, tail=((0, 14, 14), (0, 10, 22), (2, 6, 30), (4, 3, 36)),
                  tail_r=(2.6, 2.0, 1.4, 1.0))
    hd, bd = a["head"], a["body"]
    st = a["skull_top"]
    for i in range(5):                                                       # the crested casque
        m.box(hd, -0.6, st - 0.4, -16.0 + i * 1.6, 0.6, st + 2.6 - i * 0.4, -14.6 + i * 1.6, HIDE)
    for sx in (-1, 1):                                                       # bulging spiral eyes
        m.round_box(hd, sx * 4.4, -16.6, 1.6, 2.0, 15.0, 19.0, eyef, cut=1)
    m.box(hd, 3.6, 15.4, -19.0, 6.6, 18.6, -14.2, gem(P, "goggle", "goggle_light", glow=False))   # goggles
    m.box(hd, -4.6, 17.0, -15.6, 4.6, 17.8, -11.0, leather(P, "strap", "strap_dark"))
    m.round_box(a["neck"], 0, -12.4, 4.6, 3.4, 12.0, 13.2, leather(P, "strap", "strap_dark"), cut=1)  # neck strap
    tl = a["tail"]                                                           # spiral tail curl
    e = a["tail_pts"][-1]
    prev = e
    for i in range(1, 10):
        ang = i * 0.7
        r = 4.0 * (1 - i / 12)
        p = (e[0], e[1] + r * math.sin(ang) + 0.2, e[2] + 2.0 + r * math.cos(ang) - r)
        rod(m, tl, prev, p, 1, banded("t"), extend=0.3)
        prev = p
    return m
