"""Shared builder for Tailmon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): a small cat
standing upright, big padded glove-paws with claws, ear tufts, a long ringed tail, in white or black (Black Tailmon),
and Black Tailmon Uver. (a green hooded cap with a cat badge, a red backpack and a sleepy expression).
Shiny: the other colour (Black Tailmon's shiny is white)."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import eye, fabric, fur, leather, plane, skin, solid
from _route import pal, tone

WHITE = {"fur": (246, 246, 248), "fur_dark": (190, 190, 200)}
BLACK = {"fur": (70, 68, 76), "fur_dark": (30, 28, 34)}
COMMON = {"glove": (150, 140, 210), "glove_dark": (90, 80, 160), "violet": (140, 110, 210), "claw": (240, 80, 120),
          "eye": (240, 200, 40), "pupil": (20, 16, 10), "white": (250, 250, 250), "pad": (50, 40, 60),
          "cap": (60, 90, 80), "cap_dark": (24, 50, 40), "red": (210, 40, 40), "red_dark": (130, 14, 20),
          "black": (30, 30, 36)}


def make(name, black=True, uver=False, colours=None, shiny_colours=None, slit=True, xab=False):
    """colours / shiny_colours override palette entries (Tailmon's yellow gloves, blue eyes); a "stripe" entry paints
    zigzag stripes on the gloves; xab = Tailmon (X-Antibody): huge gold paws with red pads, a gold collar ring."""
    base = dict(COMMON, **(BLACK if black else WHITE))
    shiny = dict(COMMON, **(WHITE if black else BLACK))
    base.update(colours or {})
    shiny.update(shiny_colours or {})

    def P(v):
        return pal(base, shiny, v)

    FUR = fur(P, "fur", "fur_dark", length=1.0)
    GLOVE0 = fur(P, "glove", "glove_dark", length=0.8)

    def GLOVE(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if "stripe" in p:
            t = y * 1.2 + 0.6 * math.sin(abs(x) * 2.2 + z * 1.7)
            if t % 2.6 < 0.7:
                return tone(p["stripe"], face), None
        if xab and "xpad" in p and face == "north" and box is not None:
            cx = box.lo[0] + box.size[0] / 2
            cy = box.lo[1] + box.size[1] / 2
            r = math.hypot(x - cx, y - cy - 0.4)
            if r < 1.3 or any(math.hypot(x - cx - j * 1.1, y - cy - 1.9) < 0.55 for j in (-1, 0, 1)):
                return tone(p["xpad"], face), None
        return GLOVE0(x, y, z, face, variant, box=box, **k)

    def headf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            a, b = plane(x, y, z, face)
            for sx in (-1, 1):
                if uver:
                    if abs(b - 21.6) < 0.35 and abs(a - sx * 2.0) < 1.4:
                        return p["black"], None                  # sleepy eyes
                else:
                    c = eye(p, a - sx * 2.0, b - 22.4, 1.2, "eye", slit=slit)
                    if c is not None:
                        return c, None
        return FUR(x, y, z, face, variant, box=box, **k)

    def ringtail(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        t = (box.lo[2] + box.size[2] - z) if box else 0
        return (tone(p["violet"], face), None) if (t % 3.0) < 0.8 else FUR(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 8, 0))
        m.round_box(bd, 0, 0, 3.4, 2.8, 7.0, 16.0, FUR, cut=1)
        hd = m.bone("head", bd, (0, 16, 0))
        ball(m, hd, (0, 21.0, 0), 4.8, headf, layers=5)
        for sx in (-1, 1):                                       # ears with violet tufts
            spike(m, hd, (sx * 2.6, 25.0, 0.0), (sx * 0.3, 1, 0.1), 2.4, 4.0, FUR, tip=1.0)
            for j in range(3):
                spike(m, hd, (sx * 3.2, 28.6, 0.0), ((j - 1) * 0.5 + sx * 0.2, 1, 0), 0.8, 2.0, solid(P, "violet"))
        if uver:                                                 # hooded cap and backpack
            m.round_box(hd, 0, 0.6, 5.2, 5.0, 23.6, 27.4, fabric(P, "cap", "cap_dark"), cut=2)
            m.box(hd, -4.4, 23.6, -8.0, 4.4, 24.4, -4.0, fabric(P, "cap", "cap_dark"))
            m.box(hd, -1.0, 24.6, -5.4, 1.0, 26.0, -5.0, solid(P, "black"))
            m.round_box(bd, 0, -0.4, 4.0, 3.4, 9.0, 16.0, fabric(P, "cap", "cap_dark"), cut=1)
            m.box(bd, -3.6, 9.0, 3.0, 3.6, 18.0, 6.6, leather(P, "red", "red_dark"))
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):     # big padded glove-paws with claws
            ab = m.bone(nm, bd, (sx * 3.4, 14.0, 0))
            h = (sx * 6.4, 13.0 if not uver else 10.0, -2.0)
            rod(m, ab, (sx * 3.4, 14.0, 0), h, 2, FUR, extend=0.3)
            if xab:
                h = (sx * 7.6, 15.0, -2.4)
                rod(m, ab, (sx * 3.4, 14.0, 0), h, 2, FUR, extend=0.3)
                ball(m, ab, h, 4.2, GLOVE, layers=4)
                for f in range(3):
                    spike(m, ab, (h[0] + sx * 2.0, h[1] + 1.2 - f * 1.4, h[2] + 1.0), (sx, 0.5 - f * 0.4, 0.6), 1.0,
                          4.0, solid(P, "claw"), tip=0.8)
            else:
                ball(m, ab, h, 2.6, GLOVE, layers=3)
                for f in range(3):
                    spike(m, ab, (h[0] + (f - 1) * 1.0, h[1] + 2.0, h[2] - 1.6), (0, 0.6, -1), 0.8, 2.0,
                          solid(P, "claw"))
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 1.8, 7.0, 0))
            rod(m, lg, (sx * 1.8, 7.0, 0), (sx * 2.0, 2.0, 0), 2, FUR, extend=0.3)
            ball(m, lg, (sx * 2.0, 1.6, -0.6), 1.8, FUR, layers=2)
        if xab:                                                  # the gold collar ring
            ring = solid(P, "gold")
            for i in range(14):
                a0 = i * 2 * math.pi / 14
                cx, cz = 4.6 * math.sin(a0), 4.0 * math.cos(a0)
                w = 2.2
                m.box(bd, cx - w / 2, 15.0, cz - w / 2, cx + w / 2, 17.4, cz + w / 2, ring)
        tl = m.bone("tail", bd, (0, 8, 2))
        pts = [(0, 8.0, 2.0), (3.0, 6.0, 7.0), (7.0, 8.0, 10.0), (10.0, 14.0, 10.0), (11.0, 20.0, 8.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tl, p0, p1, 1, ringtail, extend=0.3)
        for j in range(3):
            spike(m, tl, pts[-1], ((j - 1) * 0.6, 1, 0), 0.8, 2.0, solid(P, "violet"))
        return m
    return build
