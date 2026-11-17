"""Shared builder for Diablomon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): the rogue
program. Its head is a wide, flat, swept purple shield with a tiny orange-and-black face and green eyes in the
middle, from which hang long ragged olive-brown ribbon limbs: two arms ending in huge violet hands with long red
claws and two legs ending in violet feet with red talons. make(x=True): Diablomon (X-Antibody), slender armoured
limbs of translucent pink crystal with magenta clawed gauntlets, a head of jagged magenta blades, long flowing mint-
green hair and a curved silver blade at one foot. Shiny: crimson shield, grey ribbons.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import armour, gem, metal, solid, strands
from _route import pal, tone

BASE = {"purple": (60, 50, 130), "purple_dark": (20, 16, 60), "purple_light": (130, 120, 210), "ribbon": (130, 120, 80),
        "ribbon_dark": (70, 60, 36), "violet": (80, 50, 140), "violet_dark": (30, 16, 60), "red": (170, 50, 40),
        "orange": (250, 140, 40), "black": (30, 26, 30), "eye": (90, 240, 120), "pink": (240, 180, 230, 200),
        "pink_light": (255, 230, 250, 220), "magenta": (200, 40, 120), "magenta_dark": (110, 10, 60), "mint": (150, 240, 210),
        "mint_dark": (80, 170, 150), "silver": (220, 224, 236), "silver_dark": (110, 114, 128), "gold": (240, 200, 70)}
SHINY = {"purple": (160, 30, 40), "purple_dark": (70, 10, 14), "purple_light": (230, 110, 110), "ribbon": (130, 130, 140),
         "ribbon_dark": (60, 60, 70), "pink": (180, 220, 250, 200), "mint": (250, 200, 120)}


def P(v):
    return pal(BASE, SHINY, v)


SHIELD = armour(P, "purple", "purple_dark", light="purple_light")
RIBBON = strands(P, "ribbon", "ribbon_dark", lines=4)
CRYSTAL = gem(P, "pink", "pink_light", glow=False)
MAGENTA = armour(P, "magenta", "magenta_dark", trim="gold", trim_w=0.25)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 0.8) < 0.45 and abs(y - 47.4) < 0.4:
                return p["eye"], p["eye"]
        if y > 48.4:
            return tone(p["orange"], face), None
        return tone(p["black"], face), None
    return tone(p["black"], face), None


def limb(m, bone, pts, shader, t):
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bone, p0, p1, t, shader, extend=0.6, t2=max(1, t - 1))


def make(name, x=False):
    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 40, 0))
        hd = m.bone("head", bd, (0, 47, 0))
        if not x:
            for sx in (-1, 1):                                                 # the swept shield head
                for j in range(4):
                    x0, x1 = sorted((sx * 2.0, sx * (21.0 - j * 3.4)))
                    m.box(hd, x0, 43.6 + j * 2.0, -1.0 + j * 0.6, x1, 46.4 + j * 2.0, 3.0 - j * 0.4, SHIELD,
                          rotation=(0, 0, sx * (12 + j * 4)), pivot=(sx * 2.0, 46.0, 1.0))
                spike(m, hd, (sx * 19.0, 51.0, 1.0), (sx, 0.6, 0.2), 2.0, 6.0, SHIELD, tip=0.5)
            m.round_box(hd, 0, 0, 2.6, 3.0, 44.0, 52.0, SHIELD, cut=1)
            spike(m, hd, (0, 51.0, 1.0), (0, 1, 0.3), 1.6, 6.0, SHIELD, tip=0.4)  # central horn
            m.box(hd, -1.8, 45.6, -3.2, 1.8, 49.6, -2.6, facef)                # the little face
        else:
            m.round_box(hd, 0, 0, 2.4, 2.6, 44.0, 50.0, MAGENTA, cut=1)
            m.box(hd, -1.4, 46.0, -2.8, 1.4, 48.6, -2.4, facef)
            for i in range(9):                                                 # jagged magenta blades
                ang = math.radians(-80 + i * 20)
                spike(m, hd, (2.0 * math.sin(ang), 49.0, 0.0), (math.sin(ang), 0.8, 0.2), 1.6, 8.0 + (i % 2) * 4.0,
                      MAGENTA, tip=0.4)
            for i in range(10):                                                # flowing mint hair
                ang = math.radians(-90 + i * 20)
                pts = [(1.6 * math.sin(ang), 49.0, 1.6), (5.0 * math.sin(ang) + 2.0, 40.0, 7.0),
                       (8.0 * math.sin(ang) + 6.0, 28.0, 10.0)]
                limb(m, hd, pts, strands(P, "mint", "mint_dark"), 2)
        mat = RIBBON if not x else CRYSTAL
        hand = solid(P, "violet") if not x else MAGENTA
        claw = solid(P, "red") if not x else MAGENTA
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                   # ribbon arms
            ab = m.bone(nm, bd, (sx * 3.0, 44.0, 0))
            pts = [(sx * 3.0, 44.0, 0), (sx * 10.0, 38.0, -2.0), (sx * 12.0, 28.0, -3.0), (sx * 14.0, 20.0, -4.0)]
            limb(m, ab, pts, mat, 3)
            m.round_box(ab, sx * 14.0, -4.0, 2.4, 2.4, 17.0, 21.0, hand, cut=1)
            for j in range(4):
                spike(m, ab, (sx * 14.0 + (j - 1.5) * 1.2, 17.0, -4.6), (sx * 0.2 * (j - 1.5), -1, -0.3), 0.9, 7.0,
                      claw, tip=0.25)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                   # ribbon legs
            lg = m.bone(nm, top, (sx * 2.0, 40.0, 0))
            pts = [(sx * 1.0, 42.0, 0), (sx * 4.0, 30.0, 1.0), (sx * 3.0, 18.0, 0.0), (sx * 6.0, 6.0, -2.0)]
            limb(m, lg, pts, mat, 3)
            m.round_box(lg, sx * 6.0, -2.0, 2.6, 3.0, 2.0, 6.0, hand, cut=1)
            for j in range(4):
                spike(m, lg, (sx * 6.0 + (j - 1.5) * 1.3, 2.0, -4.6), (0, -0.4, -1), 1.0, 5.0, claw, tip=0.25)
            if x and sx > 0:                                                   # curved silver foot blade
                bl = [(sx * 6.0, 2.0, 2.0), (sx * 8.0, 0.0, 8.0), (sx * 7.0, 1.0, 14.0)]
                for p0, p1 in zip(bl, bl[1:]):
                    rod(m, lg, p0, p1, 1, metal(P, "silver", dark="silver_dark"), extend=0.4, t2=3)
        return m
    return build
