"""Throh's Gi form (Fighting/Fire), after @magikdex's Cornera region art: Throh ablaze. A hulking red judoka in a
round black gi: white lapels crossing in a V over its red chest, a white belt with hanging tails, wide black trousers
ending in jagged white hems, big red open hands raised to grapple, a black brow band with a ridge down its nose over
cold blue eyes, and flames everywhere: a blazing mane round its head, tufts on its shoulders and fire roaring from its
hips.

Shiny: orange skin and blue fire.

Front is -z, y is up. 32 units tall; baseScale 0.72 (1.4 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _gi import fan, near_seg, palette, seamed
from _route import tone

SHINY = {"red": (236, 140, 64), "red_dark": (190, 100, 40), "flame": (80, 150, 255), "flame_hot": (196, 234, 255)}
P, solid, ramp = palette(SHINY)
SCALE = 0.72
HITBOX = [1.6, 2.0]
KIND = "biped"
K = 4
HEIGHT = 32
LOOK = ("a hulking red judoka in a round black gi with white lapels and belt, jagged white trouser hems, big open red "
        "hands, a black brow band and flames blazing round its head, shoulders and hips")
HY = 25.0


def flame(x, y, z, face, variant, box=None, **k):
    """Fire: golden at the root, orange-red further out; it glows."""
    p = P(variant)
    t = 0.0
    if box is not None:
        t = max(0.0, min(1.0, (box.lo[2] + box.size[2] - z) / max(1e-6, box.size[2])))
    c = p["flame_hot"] if t < 0.35 else p["flame"]
    return c, c


def gi(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and y > 15.0:
        w = (y - 15.0) * 0.62
        if abs(x) < w - 1.0:
            return tone(p["red"], face), None                              # the chest in the open V
        if abs(x) < w + 0.8:
            return tone(p["white"], face), None                            # the lapels
    return tone(p["black"], face), None


def trousers(x, y, z, face, variant, **k):
    p = P(variant)
    edge = 4.2 + 0.9 * abs(((x + z) * 0.9) % 2 - 1)                     # a jagged white hem
    if y < edge and face not in ("up", "down"):
        return tone(p["white"], face), None
    return tone(p["black"], face), None


def head(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        if HY + 0.4 < y < HY + 1.6 and abs(x) < 3.4:
            return tone(p["black"], face), None                            # the brow band
        if abs(x) < 0.55 and HY - 2.0 < y <= HY + 0.4:
            return tone(p["black"], face), None                            # its ridge down the nose
        for sx in (-1, 1):
            d = math.hypot((x - sx * 1.6) / 0.95, (y - HY - 0.1) / 0.62)
            if d < 1:
                return (p["pupil"] if d < 0.32 else p["blue_eye"] if d < 0.75 else p["eye_white"]), None
        if near_seg(x, y, (-1.2, HY - 2.7), (1.2, HY - 2.7), 0.2):
            return tone(p["red_dark"], face), None                         # a set mouth
    return tone(p["red"], face), None


def build() -> Model:
    m = Model("throh_gi")
    top = m.bone("throh_gi", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 13, 0))
    m.round_box(bd, 0, 0.3, 6.4, 5.0, 8.6, 13.6, solid("black"), cut=2.0)          # the round gi body
    m.round_box(bd, 0, 0.3, 6.8, 5.2, 13.4, 15.0, solid("white"), cut=2.0)          # the white belt
    m.round_box(bd, 0, 0.3, 6.6, 5.0, 14.8, 21.6, gi, cut=2.0)
    m.round_box(bd, 0, 0.3, 5.2, 4.0, 21.4, 22.6, gi, cut=1.5)

    def tails(x, y, z, face, variant, **k):
        return tone(P(variant)["white"], face), None
    m.box(bd, -2.4, 8.0, -5.4, -0.4, 14.4, -4.4, tails, rotation=(0, 0, -8), pivot=(-1.4, 14.4, -4.9))
    m.box(bd, 0.4, 8.6, -5.4, 2.4, 14.4, -4.4, tails, rotation=(0, 0, 8), pivot=(1.4, 14.4, -4.9))
    for sx in (-1, 1):                                                  # fire roaring from the hips
        fan(m, bd, (sx * 6.4, 13.2, 1.0), 3, 6.4, 2.2, flame, spread=0.5, up=(sx * 1.6, 0.8, 0.4))
    hd = m.bone("head", bd, (0, 21.5, 0))
    m.round_box(hd, 0, -1.0, 3.6, 3.4, HY - 4.0, HY + 2.8, head, cut=1.2)
    m.round_box(hd, 0, -1.0, 2.8, 2.6, HY + 2.7, HY + 3.4, head, cut=0.9)
    m.box(hd, -3.8, HY + 0.4, -4.8, 3.8, HY + 1.6, -4.2, solid("black"))          # the brow band juts out
    mane = m.bone("mane", hd, (0, HY, 1))                                # the blazing mane
    fan(m, mane, (0, HY + 1.0, 1.2), 7, 7.4, 2.6, flame, spread=0.42, up=(0, 1.0, 0.5))
    for sx in (-1, 1):
        fan(m, mane, (sx * 3.2, HY - 1.4, -1.0), 2, 4.4, 2.0, flame, spread=0.5, up=(sx * 1.4, 0.6, 0.1))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 6.4, 19.0, 0))
        m.round_box(a, sx * 7.0, 0.3, 2.6, 2.6, 17.0, 21.6, solid("black"), cut=1.0)   # big round shoulders
        fan(m, a, (sx * 7.4, 21.4, 0.6), 2, 4.6, 2.0, flame, spread=0.6, up=(sx * 0.6, 1.0, 0.2))
        rod(m, a, (sx * 7.6, 18.6, 0.2), (sx * 10.6, 17.6, -1.0), 4.0, solid("black"))   # sleeves
        rod(m, a, (sx * 10.6, 17.6, -1.0), (sx * 11.0, 22.6, -2.6), 3.0, seamed(P, "red", [("y", 19.6)], dark="red_dark"))
        m.round_box(a, sx * 11.0, -2.8, 2.0, 1.2, 22.4, 25.6, solid("red"), cut=0.5)      # big open hands
        for i, dx in enumerate((-1.3, -0.1, 1.1)):
            spike(m, a, (sx * 11.0 + dx, 25.2, -2.8), (dx * 0.2, 1, -0.3), 1.0, 2.6 - 0.3 * abs(i - 1), solid("red"))
        spike(m, a, (sx * 11.0 - sx * 2.0, 23.4, -2.8), (-sx, 0.6, -0.4), 1.0, 1.8, solid("red"))   # thumbs
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.4, 10.0, 0))
        rod(m, lg, (sx * 3.4, 10.6, 0.2), (sx * 5.4, 5.6, -0.4), 4.6, trousers)
        rod(m, lg, (sx * 5.4, 5.6, -0.4), (sx * 5.8, 2.2, -0.2), 4.4, trousers)
        m.round_box(lg, sx * 5.8, -1.2, 2.2, 2.6, 0, 2.2, seamed(P, "red", [("z", -2.0)], dark="red_dark"), cut=0.8)
    return m
