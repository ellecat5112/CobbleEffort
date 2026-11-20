"""Gnashing Night (Dark/Dragon), the ancient paradox Darkrai, built from boxes after @ArtWithAlfred's art (no name
given; our name).

A hunched beast of living shadow, ragged at every edge. Its head gapes on a red maw lined with great white fangs, a
sickly teal light glowing in its throat and its eye, under a swept-back crest of pale bone like Darkrai's plume. Long
shadowy arms end in hooked claws, and it stands on splayed, jagged feet.

Shiny: a deep blue-violet shadow with a pink glow.

Front is -z, y is up. 42 units tall (to the crest); about 3.0 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import smooth_path
from _regi import _hash, ellipsoid
from _route import mix, pal, tone

HEIGHT = 42
SCALE = round(3.0 * 16 / HEIGHT, 3)
HITBOX = [2.0, 36 / 16]
KIND = "biped"
K = 3
LOOK = ("a hunched beast of ragged living shadow with a gaping red maw of great white fangs, a teal glow in its throat, "
        "a swept-back crest of pale bone, long hooked claws and splayed jagged feet")

BASE = {"shadow": (44, 42, 52), "shadow_light": (72, 68, 84), "shadow_dark": (26, 24, 32), "bone": (204, 206, 212),
        "bone_dark": (150, 152, 162), "mouth": (176, 50, 50), "mouth_dark": (110, 30, 34), "fang": (246, 246, 240),
        "glow": (110, 236, 190), "eye": (240, 200, 70)}
SHINY = {"shadow": (40, 40, 86), "shadow_light": (70, 66, 130), "shadow_dark": (24, 22, 56), "glow": (255, 120, 200),
         "eye": (255, 160, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def shadowf(x, y, z, face, variant, **k):
    """Living shadow: near-black with lighter drifting wisps."""
    p = P(variant)
    w = math.sin(x * 0.45 + y * 0.3) * math.sin(z * 0.4 - y * 0.35)
    if w > 0.5:
        return p["shadow_light"], None
    if face == "down":
        return p["shadow_dark"], None
    return tone(p["shadow"], face), None


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(z + 13.0, y - 34.0) < 0.7:
        return p["eye"], p["eye"]
    return shadowf(x, y, z, face, variant)


def ragged(m, bone, c, r, n, seed, length=4.0, shader=None):
    """Ragged shadow spikes sticking out round a centre (the tattered edge of a shadow)."""
    for i in range(n):
        a = 2 * math.pi * i / n + _hash(seed, i) * 0.6
        b = (_hash(seed, i, 3) - 0.3) * 1.4
        d = (math.cos(a) * math.cos(b), math.sin(b), math.sin(a) * math.cos(b))
        base = tuple(cc + dd * r * 0.8 for cc, dd in zip(c, d))
        spike(m, bone, base, d, 2.2, length * (0.6 + 0.8 * _hash(seed, i, 5)), shader or shadowf, tip=1.0)


def build() -> Model:
    m = Model("gnashingnight")
    top = m.bone("gnashingnight", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20.0, 2.0))
    ellipsoid(m, bd, 0, 21.0, 2.0, 6.0, 6.6, 5.8, shadowf, step=1)                   # the hunched body
    ellipsoid(m, bd, 0, 27.0, -1.0, 7.0, 5.0, 6.0, shadowf, step=1)                  # its heaving shoulders
    ragged(m, bd, (0, 23.0, 2.0), 6.0, 14, 1, length=5.0)
    nk = m.bone("neck", bd, (0, 28.0, -4.0))
    rod(m, nk, (0, 28.0, -4.0), (0, 31.0, -9.0), 5.0, shadowf, extend=1.0)
    hd = m.bone("head", nk, (0, 32.0, -9.0))
    m.round_box(hd, 0, -13.0, 3.6, 4.4, 31.0, 36.6, headf, cut=1)                   # skull
    m.box(hd, -3.0, 31.6, -21.0, 3.0, 34.6, -15.0, headf)                          # upper jaw
    m.box(hd, -2.4, 30.8, -20.0, 2.4, 31.8, -14.0, solid("mouth"))                 # red palate
    m.box(hd, -2.0, 30.0, -15.4, 2.0, 33.6, -14.4, solid("glow", True))            # the teal glow in its throat
    for i in range(5):                                                           # great white fangs, upper
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.4, 31.6, -20.4 + i * 1.4), (sx * 0.1, -1, -0.15), 1.2, 2.6 - 0.2 * i, solid("fang"),
                  tip=0.5)
    jw = m.bone("jaw", hd, (0, 31.0, -13.0))
    m.box(jw, -2.8, 26.2, -19.6, 2.8, 28.2, -13.0, shadowf, rotation=(28, 0, 0), pivot=(0, 31.0, -13.0))
    m.box(jw, -2.2, 28.0, -19.0, 2.2, 28.6, -13.4, solid("mouth_dark"), rotation=(28, 0, 0), pivot=(0, 31.0, -13.0))
    for i in range(4):                                                           # lower fangs
        for sx in (-1, 1):
            spike(m, jw, (sx * 2.2, 27.4 - i * 0.6, -18.4 + i * 1.3), (0, 1, 0.3), 1.1, 2.2, solid("fang"), tip=0.5)
    crest = m.bone("cap", hd, (0, 36.0, -12.0))                                     # swept-back crest of bone
    pts = smooth_path([(0, 35.8, -15.0), (0, 38.6, -10.0), (1.0, 40.0, -4.0), (2.6, 39.0, 1.0), (4.0, 41.6, 4.0)], 10)
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        rod(m, crest, a, b, 1.6, solid("bone"), extend=0.6, t2=round((3.6 - 2.0 * i / (len(pts) - 2)) * 2) / 2)
        if i in (3, 6):
            spike(m, crest, b, (0.4, 1, 0.3), 1.6, 3.4, solid("bone"), tip=0.6)
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                          # long shadow arms, hooked claws
        ar = m.bone(nm, bd, (sx * 6.0, 27.0, -2.0))
        sh, el, hand = (sx * 6.0, 27.0, -2.0), (sx * 12.6, 19.0, -5.0), (sx * 15.6, 9.0, -8.0)
        rod(m, ar, sh, el, 3.6, shadowf, extend=0.8)
        rod(m, ar, el, hand, 3.0, shadowf, extend=0.6)
        ragged(m, ar, el, 2.0, 4, 10 + sx, length=3.0)
        for c in (-1.5, -0.5, 0.5, 1.5):
            pts = [hand, (hand[0] + sx * 1.0 + c * 0.8, hand[1] - 3.0, hand[2] - 2.4 + abs(c)),
                   (hand[0] + sx * 0.4 + c * 1.0, hand[1] - 6.0, hand[2] - 1.0)]
            rod(m, ar, pts[0], pts[1], 1.2, shadowf, extend=0.4)
            rod(m, ar, pts[1], pts[2], 0.9, shadowf, extend=0.4)
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):                          # splayed jagged feet
        lg = m.bone(nm, top, (sx * 4.0, 16.0, 4.0))
        hip, kn, ft = (sx * 4.0, 16.0, 4.0), (sx * 6.4, 9.0, 0.0), (sx * 8.0, 1.0, 2.0)
        rod(m, lg, hip, kn, 4.0, shadowf, extend=0.8)
        rod(m, lg, kn, ft, 3.4, shadowf, extend=0.6)
        for i in range(5):
            a = math.radians(-60 + i * 30 + (180 if sx < 0 else 0))
            spike(m, lg, ft, (math.cos(a) * sx * -1 if sx < 0 else math.cos(a), -0.15, math.sin(a) - 0.6), 1.4,
                  4.0 + 1.0 * (i % 2), shadowf, tip=0.6)
    return m
