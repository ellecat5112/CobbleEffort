"""The CobbleEffort Tentacruel (Water/Dark), the CobbleEffort Tentacool evolved: a big deep-sea squid. Its long purple
mantle ends in a spiky tip with two broad fins, and is studded with glowing blue ring photophores; under it a yellow
head speckled blue with two great slit-pupilled eyes under heavy brows, a ring of eight arms whose blue tips glow like
a firefly squid's, and two long tentacles reaching forward with hooked clubs lined with dark hooks.

Front is -z, y is up: it hangs mantle-up in the water. 36 units tall; baseScale 0.72 (1.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _squid import P, armf, bodyf, eye, hookf, mantlef, ring_club, tentacle, tipf
from _route import tone

SCALE = 0.72
HITBOX = [1.6, 2.2]
KIND = "floater"
K = 4
HEIGHT = 36
LOOK = ("a big deep-sea squid: a long purple mantle with two fins and glowing blue ring photophores, great "
        "slit-pupilled yellow eyes, eight arms with glowing blue tips and two long tentacles with hooked clubs")

SPOTS = [(0, 19.0, -3.6, 1.2), (-1.8, 22.5, -3.4, 0.95), (1.9, 25.0, -3.1, 0.9), (-0.6, 27.6, -2.7, 0.8),
         (3.6, 18.6, 0.2, 1.1), (-3.6, 20.4, -0.6, 1.1), (3.4, 23.4, 1.5, 0.9), (-3.3, 24.6, 1.4, 0.85),
         (0.5, 18.8, 3.6, 1.1), (-1.6, 22.6, 3.4, 0.9), (1.4, 26.8, 2.8, 0.75), (0.4, 15.6, -3.7, 0.8)]


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    for sx in (-1, 1):
        c = eye(face, x, y, z, sx * 1.55, 11.6, -3.2, 1.35, variant)
        if c is not None:
            return c, None
        if face == "north" and abs(x - sx * 1.55) < 1.4 and 13.1 < y < 13.6 + 0.3 * (abs(x) - 1.55):
            return p["rim"], None                                              # heavy brows
    return bodyf(x, y, z, face, variant)


def finf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["mantle"] if face in ("north", "south") else p["mantle_dark"], face), None


def clubf(x, y, z, face, variant, **k):
    """A tentacle club: yellow, with rows of dark hooks on its inner face."""
    p = P(variant)
    if face in ("east", "west") and (y * 2.4) % 2 < 0.6:
        return p["hook"], None
    return tone(p["body"], face), None


def build() -> Model:
    m = Model("tentacruel_cobbleeffortian")
    top = m.bone("tentacruel_cobbleeffortian", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 13, 0))
    mant = mantlef(SPOTS)
    m.round_box(bd, 0, 0, 3.7, 3.7, 13.6, 24.5, mant, cut=1.4)                 # the long mantle
    m.round_box(bd, 0, 0.2, 2.9, 2.9, 24.0, 29.5, mant, cut=1.1)
    m.round_box(bd, 0, 0.3, 1.9, 1.9, 29.0, 32.0, mant, cut=0.7)
    spike(m, bd, (0, 31.8, 0.3), (0, 1, 0), 1.6, 3.6, mant, tip=0.9)            # the spiky tip
    for sx in (-1, 1):
        spike(m, bd, (sx * 1.3, 31.2, 0.3), (sx * 0.7, 1, 0), 0.9, 1.8, mant)
        x0, x1 = sorted((sx * 2.4, sx * 7.8))                                  # two broad fins near the tip
        m.box(bd, x0, 25.5, -0.3, x1, 31.0, 0.9, finf, rotation=(0, 0, -sx * 24), pivot=(sx * 2.4, 27.5, 0.3))
    hd = m.bone("head", bd, (0, 12, 0))
    m.round_box(hd, 0, 0, 3.3, 3.2, 9.0, 14.0, headf, cut=1.2)                 # the yellow head
    sk = m.bone("skirt", bd, (0, 9.5, 0))
    for i in range(8):                                                         # eight arms with glowing tips
        a = i * 2 * math.pi / 8 + math.pi / 8
        x0, z0 = 2.0 * math.sin(a), 2.0 * math.cos(a)
        rod(m, sk, (x0, 9.6, z0), (x0 * 1.9, 5.6, z0 * 1.9), 1.6, armf(), extend=0.3)
        rod(m, sk, (x0 * 1.9, 5.8, z0 * 1.9), (x0 * 2.3, 2.6, z0 * 2.3), 1.2, armf(), extend=0.2)
        rod(m, sk, (x0 * 2.3, 2.8, z0 * 2.3), (x0 * 2.4, 1.4, z0 * 2.4), 0.9, tipf(glow=True), extend=0.1)
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                        # two long tentacles with hooked clubs
        tn = m.bone(nm, bd, (sx * 1.4, 9.5, -1.4))
        tentacle(m, tn, [(sx * 1.4, 9.5, -1.4), (sx * 3.0, 6.0, -3.4), (sx * 4.0, 3.2, -5.6), (sx * 4.4, 1.6, -7.6)],
                 1.1, 0.8, armf())
        rod(m, tn, (sx * 4.4, 1.8, -7.4), (sx * 4.6, 1.2, -10.4), 1.5, clubf, extend=0.2, t2=1.0)   # the club
        for j in range(3):                                                     # its dark hooks
            spike(m, tn, (sx * 4.5, 1.2, -8.0 - j * 0.9), (0, -1, -0.4), 0.45, 0.9, hookf)
        ring_club(m, tn, sx * 4.7, 1.5, -11.2, 1.4, bodyf)
    return m
