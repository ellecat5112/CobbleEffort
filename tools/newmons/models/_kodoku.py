"""Shared builder for Kodokugumon Baby and Kodokugumon Child (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): the poison spider: Baby = a fuzzy black spider with a shaggy orange mane round a yellow face plate
dotted with blue eyes, a fanged maw, a black-and-yellow banded abdomen and eight furry legs tipped with red claws.
Child = a bulbous violet-striped abdomen with brass spikes, a golden horned face plate with green eyes, furry grey
legs banded red, and two big skull-marked fangs. Shiny: emerald.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import armour, fur, gem, solid
from _route import pal, tone

BASE = {"black": (40, 40, 46), "black_dark": (14, 14, 18), "orange": (230, 120, 40), "orange_dark": (160, 60, 14),
        "yellow": (240, 200, 60), "yellow_dark": (170, 130, 20), "blue": (80, 180, 230), "red": (210, 40, 40),
        "red_light": (250, 140, 120), "violet": (110, 70, 170), "violet_dark": (50, 24, 90), "grey": (110, 110, 124),
        "grey_dark": (60, 60, 70), "brass": (210, 170, 80), "green": (90, 220, 100), "white": (246, 246, 246),
        "mouth": (150, 30, 40), "tooth": (250, 250, 246)}
SHINY = {"violet": (40, 140, 90), "violet_dark": (10, 70, 40), "orange": (60, 180, 120), "orange_dark": (20, 110, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, child=False):
    LEG = fur(P, "black" if not child else "grey", "black_dark" if not child else "grey_dark")

    def abdf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if not child:
            return tone(p["yellow"] if abs(y - 8.0) < 1.0 else p["black"], face), None
        return tone(p["violet_dark"] if (math.atan2(x, z - 6.0) * 3.0) % 1.0 < 0.2 else p["violet"], face), None

    def facef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            spots = [(-1.2, 12.4), (1.2, 12.4), (-2.0, 11.0), (2.0, 11.0), (0, 13.4), (-0.8, 10.4), (0.8, 10.4)]
            for (ex, ey) in spots[: (7 if not child else 4)]:
                if math.hypot(x - ex, y - ey) < 0.5:
                    return tone(p["blue" if not child else "green"], face), p["blue" if not child else "green"]
            if not child and 7.0 < y < 9.4 and abs(x) < 2.0:
                if y > 8.8 and (x + 3.0) % 0.8 < 0.4:
                    return tone(p["tooth"], face), None
                return tone(p["mouth"], face), None
        return armour(P, "yellow" if not child else "brass", "yellow_dark")(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 6, 0))
        ball(m, bd, (0, 8.0, 6.0), 5.4 if not child else 6.4, abdf, layers=4)
        if child:
            for j in range(6):
                ang = math.radians(-60 + j * 24)
                spike(m, bd, (5.6 * math.sin(ang), 12.6, 6.0 + 2.0 * math.cos(ang)), (math.sin(ang) * 0.5, 1, 0.3), 1.2, 2.4,
                      solid(P, "brass"), tip=0.8)
        hd = m.bone("head", bd, (0, 10, -2))
        m.round_box(hd, 0, -2.0, 3.0, 2.0, 6.6, 14.0, facef, cut=1)
        if not child:
            for i in range(12):                                                    # shaggy orange mane
                ang = math.radians(-120 + i * 22)
                spike(m, hd, (3.0 * math.sin(ang), 10.4 + 3.4 * math.cos(ang), -1.0), (math.sin(ang), math.cos(ang), 0.4),
                      1.6, 3.4, fur(P, "orange", "orange_dark"), tip=0.8)
        else:
            for sx in (-1, 1):
                spike(m, hd, (sx * 2.0, 14.0, -2.0), (sx * 0.4, 1, -0.2), 1.2, 3.0, solid(P, "brass"), tip=0.8)
                m.round_box(hd, sx * 2.0, -5.0, 1.6, 1.4, 4.6, 7.4, solid(P, "red"), cut=0)          # skull fangs
                m.box(hd, sx * 2.0 - 0.6, 6.0, -6.5, sx * 2.0 + 0.6, 6.6, -6.4, solid(P, "white"))
                spike(m, hd, (sx * 2.0, 4.6, -5.0), (0, -1, -0.3), 1.0, 3.0, solid(P, "white"), tip=0.8)
        for i in range(8):                                                         # eight furry legs
            sx = 1 if i < 4 else -1
            j = i % 4
            ang = math.radians(-50 + j * 33)
            root = (sx * 2.6, 8.0, 2.0 + 3.0 * math.sin(ang))
            kn = (sx * 8.0, 12.0, 2.0 + 8.0 * math.sin(ang))
            ft = (sx * 11.0, 0.6, 2.0 + 11.0 * math.sin(ang))
            nm = "leg_%d_%s" % (j, "left" if sx > 0 else "right")
            lg = m.bone(nm, bd, root)
            rod(m, lg, root, kn, 1, LEG, extend=0.3, t2=2)
            rod(m, lg, kn, ft, 1, LEG, extend=0.3, t2=2)
            if child:
                m.round_box(lg, (kn[0] + ft[0]) / 2, (kn[2] + ft[2]) / 2, 1.2, 1.2, 5.0, 6.4, solid(P, "red"), cut=0)
            spike(m, lg, ft, (sx * 0.2, -1, -0.2), 0.9, 2.0, solid(P, "red"), tip=0.8)
        return m

    return build
