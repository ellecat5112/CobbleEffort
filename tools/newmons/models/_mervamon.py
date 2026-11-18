"""Shared builder for Mervamon and Mervamon Wide Hi-Vision Sword (CobbleEffort: Digital; hand-built after the official
art on wikimon.net): the Olympos XII war goddess: a white serpent-skull helm with red eyes and swept horns over long
green braided hair, a red-and-black armoured tunic, a ragged red scarf and cape, dark greaves with bone claws, her left
arm sheathed in the great bone-white serpent Ouroboros with a heart-marked head and a steel spike, and in her right
hand the sword Olympia, its red blade marked with a white zigzag. Wide Hi-Vision Sword ("wide"): Olympia grown into
a towering broad blade as tall as she is, held upright beside her.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import armour, fabric, local, metal, skin, solid, strands
from _route import pal, tone

BASE = {"skin": (240, 210, 190), "skin_dark": (190, 150, 130), "bone": (240, 236, 222), "bone_dark": (170, 160, 140),
        "red": (190, 30, 40), "red_dark": (100, 10, 20), "black": (40, 36, 44), "black_dark": (14, 12, 18),
        "hair": (60, 150, 130), "hair_dark": (20, 80, 70), "steel": (220, 224, 236), "steel_dark": (110, 114, 126),
        "gold": (230, 190, 80), "eye": (230, 30, 40), "heart": (60, 40, 50)}
SHINY = {"red": (40, 80, 170), "red_dark": (14, 30, 90), "hair": (230, 120, 170), "hair_dark": (160, 60, 110)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "skin", dark="skin_dark")
BONE = armour(P, "bone", "bone_dark", trim="bone_dark", trim_w=0.2)
TUNIC = armour(P, "red", "red_dark", trim="black", trim_w=0.3)
DARK = fabric(P, "black", "black_dark")
HAIR = strands(P, "hair", "hair_dark")


def bladef(x, y, z, face, variant, box=None, **k):
    """Olympia's blade: red with a white zigzag down the middle and steel edges."""
    p = P(variant)
    if box is None or face in ("up", "down"):
        return tone(p["steel"], face), None
    u, v, W, H = local(x, y, z, face, box)
    across, along = (u / max(W, 1e-6), v) if H >= W else (v / max(H, 1e-6), u)
    if across < 0.12 or across > 0.88:
        return tone(p["steel"], face), None
    if abs(across - 0.5 - 0.22 * (abs((along * 0.35) % 2.0 - 1.0) - 0.5)) < 0.06:
        return tone(p["bone"], face), None
    return tone(p["red"], face), None


def make(name, wide=False):
    def build():
        m = Model(name)
        mats = {"skin": SKIN, "chest": TUNIC, "abs": DARK, "pelvis": TUNIC, "neck": SKIN, "deltoid": TUNIC,
                "upper_arm": SKIN, "forearm": DARK, "hand": DARK, "finger": DARK, "claw": solid(P, "bone"),
                "thigh": DARK, "knee": BONE, "shin": DARK, "calf": DARK, "foot": BONE, "talon": solid(P, "bone")}
        a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.95, talons=True, name=name)
        bd = a["body"]
        for j in range(3):                                                             # tunic skirt
            r = 5.0 + j * 0.8
            m.round_box(bd, 0, 0.4, r, r * 0.8, 30.0 - (j + 1) * 3.4, 30.4 - j * 3.4, TUNIC, cut=1)
        for j in range(5):                                                             # ragged red scarf
            ang = math.radians(-60 + j * 30)
            m.box(bd, 4.0 * math.sin(ang) - 1.4, 47.0, -3.8 * math.cos(ang) - 0.2, 4.0 * math.sin(ang) + 1.4, 53.0,
                  -3.8 * math.cos(ang) + 0.2, fabric(P, "red", "red_dark"), rotation=(0, -math.degrees(ang), 0),
                  pivot=(4.0 * math.sin(ang), 50.0, -3.8 * math.cos(ang)))
        cape(m, bd, 51.0, 13.0, 38.0, fabric(P, "red", "red_dark"), z=4.0, flare=0.8, panels=5, seed=4)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 59.4, SKIN, cut=1)
        m.round_box(hd, 0, -0.6, 3.0, 3.2, 57.8, 61.6, BONE, cut=1)                    # serpent-skull helm
        m.round_box(hd, 0, -4.6, 1.8, 1.6, 58.4, 61.0, BONE, cut=1)                    # helm snout over the brow
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.8, sx * 1.8), 59.6, -6.25, max(sx * 0.8, sx * 1.8), 60.4, -6.1,
                  solid(P, "eye", glow=True))
            m.box(hd, min(sx * 0.6, sx * 1.6), 56.6, -2.9, max(sx * 0.6, sx * 1.6), 57.3, -2.8, solid(P, "black"))
            for j in range(3):                                                          # swept horns
                spike(m, hd, (sx * 2.4, 61.0 - j * 1.4, 0.0 + j), (sx * 0.6, 0.7, 0.4), 1.4, 6.0 - j, BONE, tip=0.8)
            pts = [(sx * 2.4, 57.0, 1.6), (sx * 3.4, 48.0, 3.4), (sx * 3.8, 38.0, 4.0), (sx * 3.4, 30.0, 4.0)]
            for p0, p1 in zip(pts, pts[1:]):                                            # long green braids
                rod(m, hd, p0, p1, 2, HAIR, extend=0.4)
        al = a["arm_left"]                                                             # Ouroboros, the serpent arm
        el, wr = al["elbow"], al["wrist"]
        rod(m, al["bone"], al["shoulder"], el, 5, BONE, extend=0.6)
        rod(m, al["bone"], el, wr, 6, BONE, extend=0.6)
        for j in range(4):
            t = j / 4
            p = (el[0] + (wr[0] - el[0]) * t, el[1] + (wr[1] - el[1]) * t, el[2] + (wr[2] - el[2]) * t)
            m.round_box(al["bone"], p[0], p[2], 3.6, 3.6, p[1] - 0.6, p[1] + 0.6, BONE, cut=1)
        sh = (wr[0] + 1.0, wr[1] - 5.0, wr[2] - 1.0)
        ball(m, al["bone"], sh, 4.6, BONE, layers=4, ry=5.0)                           # serpent head fist
        m.box(al["bone"], sh[0] - 1.6, sh[1] - 2.0, sh[2] - 4.7, sh[0] + 1.6, sh[1] + 1.4, sh[2] - 4.5,
              solid(P, "heart"))
        spike(m, al["bone"], (sh[0] + 3.6, sh[1] + 2.0, sh[2]), (1, 0.4, 0), 2.0, 7.0, metal(P, "steel"), tip=0.8)
        ar = a["arm_right"]                                                            # Olympia
        h = ar["hand"]
        m.box(ar["bone"], h[0] - 0.8, h[1] - 1.6, h[2] - 0.8, h[0] + 0.8, h[1] + 1.6, h[2] + 0.8, solid(P, "black"))
        if not wide:
            m.box(ar["bone"], h[0] - 3.0, h[1] - 2.2, h[2] - 1.0, h[0] + 3.0, h[1] - 1.4, h[2] + 1.0, metal(P, "gold"))
            m.box(ar["bone"], h[0] - 1.8, h[1] - 24.0, h[2] - 0.5, h[0] + 1.8, h[1] - 2.2, h[2] + 0.5, bladef,
                  rotation=(-30, 0, -20), pivot=(h[0], h[1] - 2.0, h[2]))
        else:
            bx, bz = h[0] - 7.0, h[2] - 3.0                                              # towering broad blade,
            for j in range(9):                                                          # tip down beside her
                w = 5.6 - max(0, 1 - j) * 2.4
                m.box(ar["bone"], bx - w, 4.0 + j * 6.0, bz - 0.8, bx + w, 10.0 + j * 6.0, bz + 0.8, bladef)
            spike(m, ar["bone"], (bx, 4.4, bz), (0, -1, 0), 2.4, 4.4, metal(P, "steel"), tip=0.8)
            m.box(ar["bone"], bx - 7.0, 58.0, bz - 1.4, bx + 7.0, 59.6, bz + 1.4, metal(P, "gold"))      # guard
            rod(m, ar["bone"], (bx, 59.6, bz), (bx, 68.0, bz), 2, solid(P, "black"), extend=0.4)          # grip
            for sx in (-1, 1):                                                          # grip horns
                spike(m, ar["bone"], (bx + sx * 1.0, 67.0, bz), (sx * 0.8, 1, 0), 1.2, 5.0, BONE, tip=0.8)
            rod(m, ar["bone"], (h[0], h[1], h[2]), (bx + 1.0, h[1] + 2.0, bz), 1, solid(P, "black"), extend=0.3)
        return m

    return build
