"""Rabbrute, the Family Pokémon (Normal/Fighting), Hopple's "family" form, after the Sundor Region's art (#103, name
kept): a titanic rabbit monster made of many Hopples fused into one: a hulking, gorilla-like body of dark grey fur, a
pale lavender belly and thighs, a small head sunk between huge shoulders with two ears, a white muzzle and red eyes,
and white fluffy forearms and shins made of bunny tufts; every tuft is a little bunny face, and the fur is dotted all
over with their faintly glowing red eyes. It stands almost 80 blocks tall.

Shiny: sandy brown with blue eyes.

Front is -z, y is up. 40 units tall; baseScale 32 (about 80 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _den import dotted, palette, tone

SHINY = {"fur": (196, 160, 116), "fur_dark": (130, 98, 66), "fur_light": (222, 196, 156), "eye": (70, 130, 220),
         "dot": (80, 150, 240)}
P, solid, ramp = palette(SHINY)
SCALE = 32.0
HITBOX = [1.7, 2.5]
KIND = "biped"
K = 3
HEIGHT = 40
LOOK = ("a titanic gorilla-like rabbit monster of many fused Hopples: dark grey fur dotted with little red eyes, a pale "
        "belly, a small eared head between huge shoulders, and white bunny-tuft forearms and shins")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.3) < 0.55 and abs(y - 32.0) < 0.5:
                return p["eye"], p["eye"]                                     # red eyes
        if abs(x) < 2.0 and y < 31.0:
            return p["fluff"], None                                           # the white muzzle
    return dotted(P, "fur_dark")(x, y, z, face, variant)


def tuftf(x, y, z, face, variant, **k):
    """White bunny tufts: each lobe is a little face with two red eyes."""
    p = P(variant)
    if face in ("north", "east", "west", "south"):
        u = (x if face in ("north", "south") else z) + 40.0
        lu, lv = u % 2.6, (y + 40.0 + (1.3 if int(u // 2.6) % 2 else 0.0)) % 2.6
        if abs(lv - 1.3) < 0.3 and (abs(lu - 0.85) < 0.28 or abs(lu - 1.75) < 0.28):
            return p["dot"], p["dot"]                                         # a little face's two eyes
    return tone(p["fluff"], face), None


def bellyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and y > 12.0 and (abs(math.sin(x * 1.1) * 0.6 + 16 - y) < 0.25):
        return p["fur_light"], None                                           # abdominal ridges
    return tone(p["belly"], face), None


def tufts(m, bone, cx, cy, cz, r, n, start=0.0):
    """A ring of white bunny tufts (little ear-tipped lobes) round a point."""
    for i in range(n):
        a = start + 2 * math.pi * i / n
        spike(m, bone, (cx + math.cos(a) * r, cy, cz + math.sin(a) * r), (math.cos(a) * 0.6, 1, math.sin(a) * 0.6),
              1.4, 2.2, tuftf, tip=0.7)


def build() -> Model:
    m = Model("rabbrute")
    top = m.bone("rabbrute", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0.4, 5.2, 4.0, 10.0, 21.0, bellyf, cut=1.6)                # the pale belly
    m.round_box(bd, 0, 0.8, 9.0, 6.0, 20.0, 31.0, dotted(P, "fur_dark"), cut=2.4) # huge shoulders and chest
    m.round_box(bd, 0, -0.4, 7.4, 5.0, 19.0, 21.0, tuftf, cut=1.8)                # a band of tufts under the chest
    hd = m.bone("head", bd, (0, 30, -2))
    m.round_box(hd, 0, -2.6, 3.0, 2.8, 28.6, 34.6, headf, cut=1.0)
    for sx, side in ((-1, "left"), (1, "right")):
        ear = m.bone(f"ear_{side}", hd, (sx * 1.6, 34, -2.4))
        rod(m, ear, (sx * 1.6, 34.0, -2.4), (sx * (3.4 if sx < 0 else 2.0), 40.0, -1.6), 2.4, dotted(P, "fur", 1.2), extend=0.4)
        tufts(m, ear, sx * (3.4 if sx < 0 else 2.0), 39.0, -1.6, 0.9, 3)
        ar = m.bone(f"arm_{side}", bd, (sx * 9, 28, 0))
        rod(m, ar, (sx * 9.0, 28.0, 0.6), (sx * 11.6, 18.0, 0.0), 4.6, dotted(P, "fur"), extend=0.6)     # upper arm
        m.round_box(ar, sx * 12.0, -0.2, 3.4, 3.4, 9.0, 18.4, tuftf, cut=1.2)       # the fluffy white forearm
        tufts(m, ar, sx * 12.0, 17.6, -0.2, 3.0, 6)
        for i in range(3):                                                         # dangling bunny-foot fingers
            fx = sx * 12.0 + (i - 1) * 1.6
            rod(m, ar, (fx, 9.4, -1.6), (fx, 6.4, -2.0), 1.0, tuftf, extend=0.2)
        lb = m.bone(f"leg_{side}", top, (sx * 4, 11, 0))
        m.round_box(lb, sx * 4.4, 0.4, 3.4, 3.6, 5.0, 12.0, bellyf, cut=1.2)         # thighs
        m.round_box(lb, sx * 4.8, 0.2, 2.4, 2.6, 0.0, 6.0, dotted(P, "fur_dark"), cut=0.8)
        tufts(m, lb, sx * 4.8, 5.6, 0.2, 2.6, 5, start=0.3)
        spike(m, lb, (sx * 4.8, 0.6, -2.0), (sx * 0.3, -0.05, -1), 2.4, 4.0, tuftf, tip=1.0)   # pointed feet
    return m
