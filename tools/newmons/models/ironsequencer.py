"""Iron Sequencer (Steel/Psychic), the future paradox Mew, built from boxes after @professorkauri's art (the art's
own name).

A seated robot Mew of glossy pink metal. Its big round head is split by fine seams, with two pale lens domes over
glowing cyan eye slits, a little round muzzle and two glowing pink crystal ears. Its chest hangs open on a dark bay
with a glowing blue screen and a tray of sample dishes and a vial; its small hands are glowing pink balls bristling
with cyan crystal needles; its long legs fade to glowing pink, and its long tail is a banded tube full of glowing pink
fluid plugged into its back. It carries its sequencer: a long glowing pink barrel through a black drum bristling with
sample vials, ending in a pink lens.

Shiny: pale blue metal with cyan glows and pink crystals.

Front is -z, y is up. 30 units tall; about 0.9 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import ribbon, smooth_path
from _regi import ellipsoid, lit
from _route import pal, tone

HEIGHT = 30
SCALE = round(0.9 * 16 / HEIGHT, 3)
HITBOX = [0.9, HEIGHT / 16]
KIND = "floater"
K = 4
LOOK = ("a seated robot Mew of pink metal with lens-dome eyes, crystal ears, an open chest bay, needle-bristling hands, "
        "glowing legs, a fluid-filled tube tail and a long glowing gene-sequencer gun")

BASE = {"metal": (252, 188, 216), "metal_dark": (226, 142, 182), "seam": (130, 70, 104), "lens": (252, 220, 234),
        "cyan": (90, 222, 252), "glow": (255, 112, 200), "glow_light": (255, 196, 232), "black": (40, 36, 46),
        "black_light": (72, 66, 80), "screen": (116, 148, 252), "dish": (190, 196, 210), "vial": (240, 240, 246)}
SHINY = {"metal": (172, 208, 246), "metal_dark": (124, 162, 222), "seam": (60, 86, 140), "lens": (222, 240, 255),
         "cyan": (255, 140, 222), "glow": (110, 236, 255), "glow_light": (196, 248, 255)}
HC = (0, 22.0, 0.0)


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def headf(x, y, z, face, variant, **k):
    """Pink metal split by a seam over the crown and one round the face; two lens domes are added as their own boxes."""
    p = P(variant)
    if face in ("up", "south") and abs(x) < 0.22:
        return p["seam"], None
    if face == "north" and abs(y - 25.8) < 0.2 and abs(x) < 4.6:
        return p["seam"], None
    return lit(p["metal"], face, y, HC[1], 6), None


def lensf(sx):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north":
            dx, dy = x - sx * 2.7, y - 22.6
            if abs(dy) < 0.4 and abs(dx) < 1.5:
                return p["cyan"], p["cyan"]                               # glowing eye slit
        return tone(p["lens"], face), None
    return s


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 1.9 and 10.4 < y < 15.4:
        if y > 13.0:
            return p["screen"], p["screen"]
        return p["black"], None                                           # the open chest bay
    return lit(p["metal"] if face != "south" else p["metal_dark"], face, y, 12.5, 4), None


def legf(x, y, z, face, variant, **k):
    return tone(P(variant)["metal"], face), None


def shinf(x, y, z, face, variant, box=None, **k):
    """The shin: pink metal at the knee fading to glowing pink at the foot (rods: z runs back from the knee)."""
    p = P(variant)
    d = (box.lo[2] + box.size[2] - z) / max(box.size[2], 0.01)
    if d > 0.38:
        c = p["glow_light"] if d > 0.8 else p["glow"]
        return c, c
    return tone(p["metal"], face), None


def tubef(x, y, z, face, variant, **k):
    """The tail: metal bands round windows of glowing pink fluid (rods: z runs along the rod)."""
    p = P(variant)
    if (z % 2.2) < 0.55:
        return tone(p["metal_dark"], face), None
    return p["glow"], p["glow"]


def barrelf(x, y, z, face, variant, **k):
    p = P(variant)
    c = p["glow_light"] if (z % 3.0) < 0.4 else p["glow"]
    return c, c


def lensringf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" or face == "south":
        return tone(p["black"], face), None
    return tone(p["black_light"], face), None


def build() -> Model:
    m = Model("ironsequencer")
    top = m.bone("ironsequencer", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0.2, 2.8, 2.4, 9.0, 16.4, bodyf, cut=1)                     # slim torso
    m.box(bd, -1.5, 10.6, -2.4, 1.5, 11.2, -1.2, solid("dish"))                      # sample tray
    for dx in (-0.9, 0.0, 0.9):
        m.box(bd, dx - 0.35, 11.2, -2.2, dx + 0.35, 11.5, -1.6, solid("lens"))       # dishes
    m.box(bd, -1.5, 11.2, -2.2, -0.9, 12.6, -1.6, solid("vial"))                       # a vial
    hd = m.bone("head", bd, (0, 16.5, 0))
    ellipsoid(m, hd, HC[0], HC[1], HC[2], 6.4, 5.8, 5.6, headf, step=1)            # the big round head
    for sx in (-1, 1):
        ellipsoid(m, hd, sx * 2.7, 22.6, -5.0, 2.3, 2.1, 1.7, lensf(sx), step=1)  # pale lens domes
        spike(m, hd, (sx * 4.0, 26.6, -0.4), (sx * 0.45, 1, 0.1), 2.4, 4.0, solid("glow", True), tip=1.2)   # crystal ears
    ellipsoid(m, hd, 0, 19.6, -5.4, 1.3, 1.1, 0.9, solid("metal"), step=1)         # little muzzle
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):
        ar = m.bone(nm, bd, (sx * 2.8, 15.0, 0))
        hand = (sx * 4.6, 13.6, -3.2)
        rod(m, ar, (sx * 2.8, 15.0, 0), hand, 1.2, solid("metal"), extend=0.3)
        ellipsoid(m, ar, hand[0], hand[1], hand[2], 1.3, 1.3, 1.3, solid("glow", True), step=1)
        for d in ((sx * 0.7, 0.9, 0.1), (sx * 0.2, 1.0, -0.4), (sx * 0.9, 0.4, -0.3)):
            spike(m, ar, (hand[0], hand[1] + 0.6, hand[2]), d, 0.5, 2.6, solid("cyan", True))   # crystal needles
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):
        lg = m.bone(nm, bd, (sx * 1.6, 9.6, 0))
        knee = (sx * 2.0, 8.6, -4.4)
        rod(m, lg, (sx * 1.6, 9.4, 0), knee, 2.4, legf, extend=0.8)
        rod(m, lg, knee, (sx * 2.2, 0.6, -5.0), 2.2, shinf, extend=0.6)
        m.box(lg, sx * 2.2 - 1.3, 4.6, -6.3, sx * 2.2 + 1.3, 5.2, -3.7, solid("metal_dark"))   # shin band
    tl = m.bone("tail", bd, (0, 9.8, 2.4))
    m.box(tl, -1.0, 9.0, 2.0, 1.0, 11.0, 3.6, solid("black"))                        # coupling
    path = smooth_path([(0, 10.0, 3.4), (3.0, 9.4, 6.2), (8.0, 9.6, 6.6), (12.0, 11.4, 3.0),
                        (12.4, 13.6, -2.0), (9.4, 15.0, -4.6), (6.6, 15.4, -3.2)], 16)
    ribbon(m, tl, path, [1.8] * len(path), tubef, extend=0.4)
    gun = m.bone("gun", bd, (-4.6, 13.0, -3.0))                                       # the sequencer
    a, b = (-4.8, 13.2, -3.4), (-13.6, 4.6, -9.6)
    rod(m, gun, a, b, 1.8, barrelf, extend=0.4)
    rod(m, gun, (-11.4, 6.8, -8.0), (-15.0, 3.4, -10.6), 4.0, solid("black"), extend=0.2)   # black drum
    rod(m, gun, (-15.0, 3.4, -10.6), (-15.6, 2.8, -11.0), 4.6, lensringf, extend=0.2)
    rod(m, gun, (-15.4, 3.0, -10.9), (-15.7, 2.7, -11.1), 2.6, solid("glow", True), extend=0.2)   # the lens
    for d in ((-0.6, 1, 0.2), (0.8, 0.2, -0.5), (-0.4, -1, 0.3), (-0.9, 0.1, 0.8)):          # sample vials
        spike(m, gun, (-13.2, 5.0, -9.3), d, 0.9, 3.4, solid("vial"))
    return m
