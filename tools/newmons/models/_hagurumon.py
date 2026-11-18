"""Shared builder for Hagurumon and Hagurumon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): a living cog: a big round dark-steel face set in a golden gear, two different red eyes and a jagged
mouth-seam, flanked by two silver cogs that spin. X-Antibody: a red-and-gold gear ring, two more small black cogs above
like ears, and golden drill cones on each side. Shiny: copper and teal.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import metal, riveted, solid
from _route import pal, tone


def make(name, x=False):
    base = {"face": (80, 80, 90), "face_dark": (40, 40, 48), "gold": (240, 200, 60), "gold_dark": (160, 120, 20),
            "silver": (214, 218, 228), "silver_dark": (110, 114, 126), "red": (210, 30, 40), "white": (250, 250, 250),
            "drill": (240, 200, 70), "drill_dark": (170, 120, 20), "ring": (200, 40, 40)}
    shiny = {"gold": (200, 120, 70), "gold_dark": (130, 70, 30), "face": (40, 110, 110), "face_dark": (14, 60, 60)}

    def P(v):
        return pal(base, shiny, v)

    FACE = riveted(P, "face", "face_dark")

    def facef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx, r in ((-1, 1.6), (1, 1.8)):
                d = math.hypot(xx - sx * 2.4, y - 13.0)
                if d < 0.6:
                    return tone(p["white"], face), None
                if d < r:
                    return tone(p["red"], face), None
            if abs(y - 9.4 - 0.6 * abs(((xx + 4.0) % 2.0) - 1.0)) < 0.25 and abs(xx) < 4.0:
                return tone(p["face_dark"], face), None
            if abs(xx) < 0.2 and y > 9.0:
                return tone(p["face_dark"], face), None
        return FACE(xx, y, z, face, variant, box=box, **k)

    def disc(m, bone, c, r, shader, depth):
        n = max(3, int(r * 2 / 1.2))
        for j in range(n):
            y0 = c[1] - r + j * 2 * r / n
            dy = y0 + r / n - c[1]
            w = math.sqrt(max(0.0, r * r - dy * dy))
            m.box(bone, c[0] - w, y0, c[2] - depth / 2, c[0] + w, y0 + 2 * r / n, c[2] + depth / 2, shader)

    def cog(m, bone, c, r, teeth, shader, depth=1.6):
        disc(m, bone, c, r, shader, depth)
        for j in range(teeth):
            ang = 2 * math.pi * j / teeth
            m.box(bone, c[0] + (r + 0.6) * math.cos(ang) - 0.7, c[1] + (r + 0.6) * math.sin(ang) - 0.7, c[2] - depth / 2,
                  c[0] + (r + 0.6) * math.cos(ang) + 0.7, c[1] + (r + 0.6) * math.sin(ang) + 0.7, c[2] + depth / 2,
                  shader, rotation=(0, 0, math.degrees(ang)),
                  pivot=(c[0] + (r + 0.6) * math.cos(ang), c[1] + (r + 0.6) * math.sin(ang), c[2]))

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 12, 0))
        cog(m, bd, (0, 12.0, 0), 7.6, 8, metal(P, "ring" if x else "gold", dark="gold_dark"), depth=3.0)
        disc(m, bd, (0, 12.0, -1.6), 6.0, facef, 1.2)
        hd = m.bone("head", bd, (0, 19, 0))
        for sx, nm in ((1, "ring_left"), (-1, "ring_right")):
            rb = m.bone(nm, bd, (sx * 12.0, 12.0, 0))
            cog(m, rb, (sx * 12.0, 12.0, 0), 3.0, 8, metal(P, "silver", dark="silver_dark"), depth=1.4)
            if x:
                spike(m, bd, (sx * 7.6, 12.0, -1.0), (sx, 0, -0.1), 3.0, 7.0, metal(P, "drill", dark="drill_dark"),
                      tip=1.2)
                cog(m, hd, (sx * 5.0, 22.0, 0), 2.6, 7, metal(P, "face", dark="face_dark"), depth=1.6)
        return m

    return build
