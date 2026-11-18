"""Shared builder for Goddramon and Goddramon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): one of the Four Great Dragons, holy dragon-god of the west: a dragon-man with a lion-like mane, a
silver-and-red horned dragon helm, a golden robe with ornate armoured sleeves banded red, a long serpentine tail of
silver scales curling round clouds instead of legs, and great swept fans of white feathered wings. X-Antibody: blue
armour with white fur trim, steel-blue blade wings and a golden serpentine tail. Shiny: black and red.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing
from _digidetail import armour, fabric, feathers, metal, scales, solid, strands
from _route import pal, tone


def make(name, x=False):
    base = {"gold": (240, 200, 70), "gold_dark": (160, 120, 20), "red": (200, 30, 40), "red_dark": (120, 10, 16),
            "silver": (214, 218, 228), "silver_dark": (110, 114, 126), "white": (246, 246, 250),
            "white_dark": (190, 192, 206), "mane": (240, 236, 220), "mane_dark": (180, 170, 150),
            "eye": (60, 200, 120), "blue": (60, 90, 190), "blue_dark": (24, 40, 110), "cloud": (230, 236, 250)}
    if x:
        base.update({"gold": (60, 90, 190), "gold_dark": (24, 40, 110), "silver": (220, 190, 110),
                     "silver_dark": (150, 110, 40), "white": (150, 170, 220), "white_dark": (80, 100, 160)})
    shiny = {"gold": (50, 46, 56), "gold_dark": (20, 18, 24), "white": (60, 56, 70), "white_dark": (24, 20, 30)}

    def P(v):
        return pal(base, shiny, v)

    ROBE = armour(P, "gold", "gold_dark", trim="red", trim_w=0.4)
    SCALE_S = scales(P, "silver", "silver_dark", size=1.4)
    MANE = strands(P, "mane", "mane_dark")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 30, 0))
        m.round_box(bd, 0, 0, 7.0, 5.4, 30.0, 46.0, ROBE, cut=2)                          # robed torso
        m.round_box(bd, 0, 0.4, 9.6, 6.0, 42.0, 48.0, ROBE, cut=2)                        # shoulders
        tb = m.bone("tail", bd, (0, 30, 0))                                                 # serpentine tail, no legs
        pts = [(0, 30.0, 0), (0, 22.0, -2.0), (4.0, 15.0, 2.0), (0, 9.0, 6.0), (-5.0, 6.0, 2.0), (-2.0, 3.0, -3.0),
               (4.0, 2.0, -2.0), (8.0, 4.0, 3.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tb, p0, p1, max(2, 7 - j), SCALE_S, extend=0.6)
        for c in ((-8.0, 2.0, -4.0), (8.0, 1.0, 4.0), (-4.0, 1.0, 8.0)):                  # clouds
            m.round_box(tb, c[0], c[2], 4.0, 2.6, c[1], c[1] + 2.0, solid(P, "cloud"), cut=1)
        hd = m.bone("head", bd, (0, 50, -1))
        m.round_box(hd, 0, -1.0, 3.4, 3.8, 48.0, 56.0, metal(P, "silver", dark="silver_dark"), cut=1)   # dragon helm
        m.round_box(hd, 0, -5.0, 2.0, 2.0, 48.6, 52.0, metal(P, "silver", dark="silver_dark"), cut=1)
        m.round_box(hd, 0, -4.9, 0.8, 0.3, 53.0, 54.6, solid(P, "red"), cut=0)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.8, sx * 2.4), 52.4, -4.9, max(sx * 0.8, sx * 2.4), 53.2, -4.7, solid(P, "eye", glow=True))
            pts = [(sx * 2.6, 55.6, 0), (sx * 5.0, 60.0, 2.0), (sx * 4.0, 64.0, 4.0)]                  # horns
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, hd, p0, p1, 1, solid(P, "red"), extend=0.3, t2=2)
        for i in range(14):                                                                 # lion-like mane
            ang = math.radians(-130 + i * 20)
            spike(m, hd, (3.2 * math.sin(ang), 53.0 + 2.0 * math.cos(ang), 1.6), (math.sin(ang), 0.2, 0.8), 1.8, 6.0,
                  MANE, tip=0.8)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # ornate sleeves
            ab = m.bone(nm, bd, (sx * 9.0, 44.0, 0))
            rod(m, ab, (sx * 9.0, 44.0, 0), (sx * 13.0, 36.0, -4.0), 4, ROBE, extend=0.6)
            rod(m, ab, (sx * 13.0, 36.0, -4.0), (sx * 10.0, 32.0, -9.0), 4, ROBE, extend=0.6)
            m.round_box(ab, sx * 10.0, -10.0, 2.2, 2.2, 29.0, 33.0, solid(P, "silver"), cut=1)
        for side in (1, -1):                                                                  # fans of feathered wings
            for j in range(2):
                wb = m.bone(("wing_left" if side > 0 else "wing_right") + ("" if j == 0 else "_low"), bd,
                            (side * 5.0, 46.0 - j * 6.0, 4.0))
                feather_wing(m, wb, (side * 5.0, 46.0 - j * 6.0, 4.0), 26.0 - j * 6.0, 10.0, 3,
                             feathers(P, "white", "white_dark", size=(1.6, 2.8)), side=side, sweep=10 + j * 20,
                             droop=-8.0 + j * 10.0)
        return m

    return build
