"""Shared builder for the Justimon arms and Justimon (X-Antibody) (CobbleEffort: Digital; hand-built at the detail
standard after the official art on wikimon.net): the masked hero: a lean cyborg in a blue-and-white bodysuit with
silver armour plates, a silver helm with two short horns and a dark visor, a long red scarf streaming in the wind,
white boots, a blue left fist, and a cybernetic right arm: Accel Arm = a huge piston arm with a red triangle and a
clawed fist; Blitz Arm = a thick armoured arm with a short blade; Critical Arm = a long cannon blade with a jet flare.
X-Antibody: red armour with cyan lights, a white scarf and a giant red X-marked arm cannon blazing blue.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import armour, cutout, fabric, flame_inside, gem, local, metal, solid
from _route import pal, tone


def make(name, arm="accel", x=False):
    base = {"blue": (50, 60, 160), "blue_dark": (16, 20, 80), "white": (246, 246, 250), "white_dark": (170, 176, 200),
            "silver": (210, 214, 226), "silver_dark": (100, 104, 120), "red": (220, 40, 40), "red_dark": (130, 10, 18),
            "red_light": (250, 140, 130), "black": (30, 30, 38), "eye": (240, 60, 40), "scarf": (220, 40, 40),
            "scarf_dark": (130, 10, 18), "cyan": (90, 230, 250), "cyan_light": (220, 255, 255),
            "jet": (255, 140, 120, 210), "jet_core": (255, 240, 230, 240)}
    if x:
        base.update({"blue": (200, 40, 50), "blue_dark": (110, 10, 20), "silver": (220, 60, 60), "silver_dark": (120, 20, 24),
                     "scarf": (246, 246, 250), "scarf_dark": (170, 180, 210), "jet": (120, 200, 255, 210)})
    shiny = {"blue": (40, 120, 60), "blue_dark": (14, 60, 24), "scarf": (60, 90, 220), "scarf_dark": (20, 40, 140)}

    def P(v):
        return pal(base, shiny, v)

    SUIT = fabric(P, "blue", "blue_dark")
    WHITE = armour(P, "white", "white_dark", trim="blue", trim_w=0.2)
    SILVER = armour(P, "silver", "silver_dark", trim="black", trim_w=0.2, rivets=True)
    STEEL = metal(P, "silver", dark="silver_dark")

    def jetf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(xx, y, z, face, box)
        c = p["jet_core"] if v / max(H, 1e-6) < 0.3 else p["jet"]
        return c, c[:3]

    def build():
        m = Model(name)
        mats = {"skin": SUIT, "chest": SILVER, "abs": SUIT, "pelvis": SUIT, "neck": SUIT, "deltoid": SILVER,
                "upper_arm": WHITE, "forearm": WHITE, "hand": SUIT, "finger": SUIT, "thigh": SUIT, "knee": SILVER,
                "shin": SUIT, "calf": SUIT, "foot": WHITE, "toe": WHITE}
        a = humanoid(m, mats, bulk=0.9, arm_bulk=0.9, leg_bulk=0.92, name=name)
        bd = a["body"]
        if x:
            m.round_box(bd, 0, -3.8, 1.4, 0.4, 44.0, 47.0, gem(P, "cyan", "cyan_light"), cut=0)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.2, 2.4, 2.8, 54.0, 60.4, SILVER, cut=1)
        m.round_box(hd, 0, -3.0, 2.0, 0.4, 56.0, 58.6, solid(P, "black"), cut=0)
        m.box(hd, -1.6, 57.0, -3.5, 1.6, 57.6, -3.4, solid(P, "eye", glow=True))
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.6, 60.2, -1.0), (sx * 0.5, 1, 0.3), 1.0, 3.0, STEEL, tip=0.8)
        sb = m.bone("scarf", bd, (0, 53, 0))                                         # streaming scarf
        m.round_box(sb, 0, 0.4, 2.8, 2.8, 51.0, 54.0, fabric(P, "scarf", "scarf_dark"), cut=1)
        pts = [(1.0, 53.0, 2.6), (8.0, 54.0, 8.0), (16.0, 52.0, 12.0), (24.0, 55.0, 14.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, sb, p0, p1, 1, fabric(P, "scarf", "scarf_dark"), extend=0.4, t2=4)
        hr = a["arm_right"]
        el = hr["elbow"]
        hx, hy, hz = hr["hand"]
        if arm == "accel":                                                          # huge piston arm
            rod(m, hr["bone"], el, (hx - 2.0, hy - 6.0, hz - 6.0), 5, SILVER, extend=1.0)
            m.round_box(hr["bone"], hx - 2.6, hz - 8.0, 3.6, 3.6, hy - 14.0, hy - 6.0, STEEL, cut=2)
            m.round_box(hr["bone"], hx - 2.6, hz - 11.8, 2.0, 0.4, hy - 12.0, hy - 8.0, solid(P, "red"), cut=0)
            for j in range(3):
                spike(m, hr["bone"], (hx - 2.6 + (j - 1) * 1.6, hy - 14.0, hz - 8.0), (0, -1, -0.2), 1.2, 3.6, STEEL,
                      tip=0.8)
        elif arm == "blitz":                                                        # thick armoured arm + blade
            rod(m, hr["bone"], el, (hx, hy, hz), 4, SILVER, extend=0.8)
            m.round_box(hr["bone"], hx, hz, 2.6, 2.6, hy - 4.0, hy + 1.0, STEEL, cut=1)
            spike(m, hr["bone"], (hx - 2.6, hy, hz), (-0.2, 1, -0.2), 1.6, 8.0, STEEL, tip=0.8)
        elif arm == "critical":                                                     # long cannon blade + jet flare
            rod(m, hr["bone"], el, (hx, hy, hz), 3, SILVER, extend=0.6)
            m.round_box(hr["bone"], hx - 10.0, hz - 2.0, 14.0, 3.0, hy - 2.0, hy + 3.6, STEEL, cut=1)
            m.round_box(hr["bone"], hx - 22.0, hz - 2.0, 2.0, 3.2, hy - 1.6, hy + 3.2, solid(P, "red"), cut=1)
            for ang in (0, 90):
                m.box(hr["bone"], hx + 4.0, hy - 1.0, hz - 2.0, hx + 14.0, hy + 3.0, hz - 2.0,
                      cutout(flame_inside(3, 0.0, 1, 0.3), jetf), rotation=(ang, 0, 0), pivot=(hx + 4.0, hy + 1.0, hz - 2.0))
        if x:                                                                       # giant X-marked arm cannon
            hl = a["arm_left"]
            lx, ly, lz = hl["hand"]
            m.round_box(hl["bone"], lx + 2.0, lz, 3.6, 3.6, ly - 2.0, ly + 22.0, SILVER, cut=2)
            for j in range(2):
                rod(m, hl["bone"], (lx - 1.4 + j * 6.8, ly + 4.0, lz - 3.8), (lx + 5.4 - j * 6.8, ly + 14.0, lz - 3.8), 1,
                    solid(P, "black"), extend=0, t2=1)
            m.round_box(hl["bone"], lx + 2.0, lz, 2.4, 2.4, ly + 22.0, ly + 25.0, gem(P, "cyan", "cyan_light"), cut=1)
        return m

    return build
