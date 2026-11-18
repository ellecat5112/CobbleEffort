"""Shared builder for Impmon and Impmon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the little devil: a purple imp with a white face and green eyes, a cocky fanged grin, pointed purple
hood-ears, a red bandana knotted at the neck, a yellow smiley badge on the belly, big red gloves with claw points,
white toe claws and a pointed devil tail. X-Antibody: a long-limbed imp in a tall pointed wizard hat with an X visor,
a tattered red cape-wing, a belt with a gem buckle, blue fire in one hand and red fire in the other.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import cutout, fabric, flame_inside, gem, leather, local, noise2, skin, solid
from _route import pal, tone

BASE = {"purple": (70, 50, 140), "purple_dark": (30, 20, 70), "purple_light": (130, 110, 200), "white": (246, 246, 250),
        "eye": (60, 190, 90), "pupil": (16, 16, 20), "red": (220, 40, 40), "red_dark": (130, 14, 18),
        "yellow": (250, 220, 60), "mouth": (24, 20, 30), "tooth": (250, 250, 250), "claw": (240, 240, 230),
        "blue_fire": (90, 180, 255, 220), "red_fire": (255, 120, 40, 220), "fire_core": (255, 250, 220, 240),
        "steel": (180, 184, 196), "gem": (240, 120, 40), "gem_light": (255, 220, 160)}
SHINY = {"purple": (40, 40, 46), "purple_dark": (12, 12, 16), "purple_light": (110, 110, 124)}


def P(v):
    return pal(BASE, SHINY, v)


PUR = skin(P, "purple", dark="purple_dark", light="purple_light")


def make(name, x=False):
    def facef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        hy = 17.0 if not x else 31.0
        if face == "north":
            for sx in (-1, 1):
                d = math.hypot(xx - sx * 1.4, y - (hy + 1.0))
                if x and abs(y - (hy + 1.2)) < 0.4 and abs(abs(xx) - abs(y - (hy + 1.2)) * 0.0 - 1.4) < 1.2:
                    return tone(p["red"], face), p["red"]
                if not x and d < 0.4:
                    return tone(p["pupil"], face), None
                if not x and d < 1.0:
                    return tone(p["eye"], face), None
            if abs(y - (hy - 1.4)) < 0.35 and abs(xx) < 1.8:
                return tone(p["mouth"], face), None
            if abs(y - (hy - 1.0)) < 0.3 and abs(abs(xx) - 1.2) < 0.3:
                return tone(p["tooth"], face), None
        return skin(P, "white", dark="purple_light")(xx, y, z, face, variant, box=box, **k)

    def bellyf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and math.hypot(xx, y - 10.6) < 1.2:
            return tone(p["yellow"], face), None
        return PUR(xx, y, z, face, variant, box=box, **k)

    def firef(key):
        def f(xx, y, z, face, variant, box=None, **k):
            p = P(variant)
            u, v, W, H = local(xx, y, z, face, box)
            c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p[key]
            return c, c[:3]
        return cutout(flame_inside(3, 0.1, 5), f)

    def tatter(xx, y, z, face, box):
        u, v, W, H = local(xx, y, z, face, box)
        return v / max(H, 1e-6) > 0.15 * abs(math.sin(u * 1.1)) + 0.08 * noise2(u, 0.0, 4)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        if not x:                                                              # little round imp
            bd = m.bone("body", top, (0, 6, 0))
            m.round_box(bd, 0, 0, 3.0, 2.6, 6.0, 13.6, bellyf, cut=1)
            m.round_box(bd, 0, -0.4, 2.4, 2.0, 13.0, 14.4, fabric(P, "red", "red_dark"), cut=1)
            spike(m, bd, (0.6, 13.4, -2.4), (0.4, -1, -0.3), 1.2, 2.4, fabric(P, "red", "red_dark"), tip=0.8)
            hd = m.bone("head", bd, (0, 14, 0))
            m.round_box(hd, 0, 0, 3.4, 3.0, 14.2, 20.4, PUR, cut=1)
            m.round_box(hd, 0, -0.6, 2.8, 2.6, 14.4, 19.4, facef, cut=1)
            for sx in (-1, 1):
                spike(m, hd, (sx * 2.6, 19.6, 0.2), (sx, 0.6, 0.2), 1.8, 3.6, PUR, tip=0.8)        # hood ears
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
                ab = m.bone(nm, bd, (sx * 3.0, 12.6, 0))
                rod(m, ab, (sx * 3.0, 12.6, 0), (sx * 5.4, 10.4, -0.6), 1, PUR, extend=0.3, t2=1)
                m.round_box(ab, sx * 6.4, -0.6, 1.8, 1.8, 9.0, 12.0, leather(P, "red", "red_dark"), cut=1)
                for j in range(3):
                    spike(m, ab, (sx * 7.6, 10.4, -0.6 + (j - 1) * 1.0), (sx, 0.3, 0), 0.8, 1.8, leather(P, "red", "red_dark"),
                          tip=0.8)
            for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
                lg = m.bone(nm, top, (sx * 1.6, 6.0, 0))
                rod(m, lg, (sx * 1.6, 6.4, 0), (sx * 1.8, 1.4, 0), 1, PUR, extend=0.3, t2=2)
                m.round_box(lg, sx * 1.8, -0.6, 1.4, 1.8, 0.0, 1.6, PUR, cut=0)
                for j in range(2):
                    spike(m, lg, (sx * 1.8 + (j - 0.5) * 1.0, 0.6, -2.4), (0, 0, -1), 0.8, 1.2, solid(P, "claw"), tip=0.8)
            tb = m.bone("tail", bd, (0, 7, 2))
            pts = [(0, 7.0, 2.4), (1.0, 6.0, 5.0), (2.0, 8.0, 7.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, tb, p0, p1, 1, PUR, extend=0.2, t2=1)
            spike(m, tb, pts[-1], (0.4, 1, 0.4), 1.4, 1.8, PUR, tip=0.8)
        else:                                                                   # long-limbed X imp
            bd = m.bone("body", top, (0, 14, 0))
            m.round_box(bd, 0, 0, 3.0, 2.4, 14.0, 26.0, PUR, cut=1)
            m.round_box(bd, 0, 0, 3.2, 2.6, 16.0, 17.4, leather(P, "steel", "purple_dark"), cut=1)
            m.round_box(bd, 0, -2.6, 0.8, 0.4, 16.0, 17.4, gem(P, "gem", "gem_light"), cut=0)
            hd = m.bone("head", bd, (0, 26, 0))
            m.round_box(hd, 0, 0, 2.8, 2.6, 27.0, 33.4, facef, cut=1)
            m.round_box(hd, 0, 0.4, 4.4, 4.0, 33.0, 34.4, PUR, cut=2)                            # hat brim
            spike(m, hd, (0, 34.0, 0.6), (0.3, 1, 0.5), 3.4, 11.0, PUR, tip=0.8)                    # tall hat
            for sx in (-1, 1):
                spike(m, hd, (sx * 3.0, 32.6, 0), (sx, 0.4, 0), 1.2, 3.0, PUR, tip=0.8)
            for sx, nm, key in ((1, "arm_left", "blue_fire"), (-1, "arm_right", "red_fire")):
                ab = m.bone(nm, bd, (sx * 3.0, 25.0, 0))
                rod(m, ab, (sx * 3.0, 25.0, 0), (sx * 8.0, 20.0, -2.0), 1, PUR, extend=0.3, t2=1)
                rod(m, ab, (sx * 8.0, 20.0, -2.0), (sx * 11.0, 24.0, -3.0), 1, PUR, extend=0.3, t2=1)
                m.round_box(ab, sx * 11.6, -3.0, 1.8, 1.8, 23.0, 26.0, leather(P, "red", "red_dark"), cut=1)
                for ang in (0, 90):
                    m.box(ab, sx * 11.6 - 2.0, 26.0, -3.0, sx * 11.6 + 2.0, 32.0, -3.0, firef(key),
                          rotation=(0, ang, 0), pivot=(sx * 11.6, 26.0, -3.0))
            for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
                lg = m.bone(nm, top, (sx * 1.8, 14.0, 0))
                rod(m, lg, (sx * 1.8, 14.0, 0), (sx * 2.6, 7.0, -1.0), 1, PUR, extend=0.3, t2=2)
                rod(m, lg, (sx * 2.6, 7.0, -1.0), (sx * 2.6, 1.0, 0.6), 1, PUR, extend=0.3, t2=2)
                spike(m, lg, (sx * 2.6, 0.8, -0.4), (0, 0, -1), 1.4, 4.0, solid(P, "claw"), tip=0.8)
            for side in (1, -1):                                                 # tattered red cape-wings
                wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 1.6, 25.0, 2.6))
                x0, x1 = sorted((side * 1.6, side * 16.0))
                m.box(wb, x0, 10.0, 2.8, x1, 30.0, 2.8, cutout(tatter, fabric(P, "red", "red_dark")),
                      rotation=(0, side * -25, 0), pivot=(side * 1.6, 25.0, 2.8))
        return m

    return build
