"""Shared builder for Eosmon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): the program of
the dawn, a being of faceted blue crystal. make(name, stage):

- "adult": a floating cluster of faceted blue-white crystal plates with crystal claws, an eye-like core, translucent
  hexagon-tiled wings and a glowing golden ring at its side, with a spark of lightning above it.
- "perfect": a slender crystal figure floating at the centre of four vast translucent wings of hexagon panes, a
  crystal crown, a dangling chain of dark-blue crystal plates for a body and a pendant gem.
- "ultimate": a gold-and-blue figure in a bell of blue feathers, crowned with golden spikes, before a great fan of
  iridescent rainbow crystal blades, with a glowing violet orb hanging beneath.
Shiny: rose-gold crystal.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import feathers, gem, local, metal, solid
from _route import pal, tone

BASE = {"crystal": (130, 170, 240), "crystal_light": (230, 240, 255), "deep": (40, 60, 170), "deep_light": (140, 160, 240),
        "pane": (150, 210, 250, 140), "pane_edge": (230, 245, 255, 200), "gold": (250, 210, 60), "gold_dark": (170, 120, 20),
        "violet": (150, 70, 220), "violet_light": (230, 180, 255), "eye": (250, 230, 120), "white": (246, 246, 250),
        "rainbow0": (250, 120, 160, 170), "rainbow1": (250, 220, 100, 170), "rainbow2": (120, 230, 170, 170),
        "rainbow3": (120, 170, 250, 170), "feather": (60, 100, 220), "feather_dark": (20, 40, 120), "spark": (230, 240, 255)}
SHINY = {"crystal": (240, 170, 170), "deep": (170, 70, 90), "deep_light": (240, 150, 170), "pane": (250, 190, 200, 140),
         "feather": (200, 80, 110), "feather_dark": (110, 30, 50)}


def P(v):
    return pal(BASE, SHINY, v)


CRYSTAL = gem(P, "crystal", "crystal_light", glow=False)
DEEP = gem(P, "deep", "deep_light", glow=False)
GOLD = metal(P, "gold", dark="gold_dark")


def panef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    a, b = u * 0.6, v * 0.6
    if abs((a + (b // 1.7) * 0.85) % 1.7 - 0.85) > 0.72 or b % 1.7 < 0.14:
        return p["pane_edge"], p["pane_edge"][:3]                       # hexagon tile edges glow
    return p["pane"], None


def rainbowf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["rainbow%d" % (int((u + v * 0.5) * 0.4) % 4)]
    return c, c[:3]


def wing(m, bone, root, length, width, ang, tilt, shader):
    x0 = root[0] - width / 2
    m.box(bone, x0, root[1], root[2], x0 + width, root[1] + length, root[2], shader,
          rotation=(tilt, 0, ang), pivot=root)


def make(name, stage="adult"):
    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 20, 0))
        if stage == "adult":
            for i, (cx, cy, cz, r) in enumerate(((0, 20, 0, 4.0), (-3, 25, -1, 3.0), (3, 25, -1, 3.0), (0, 15, 1, 3.0),
                                                 (-4, 18, 1, 2.4), (4, 18, 1, 2.4))):
                m.round_box(bd, cx, cz, r, r * 0.8, cy - r, cy + r, CRYSTAL, cut=max(1, round(r * 0.4)))
            hd = m.bone("head", bd, (0, 27, 0))
            m.round_box(hd, 0, -1.0, 2.6, 2.0, 26.0, 31.0, CRYSTAL, cut=1)
            m.round_box(hd, 0, -3.0, 1.2, 0.4, 27.6, 29.4, solid(P, "eye", glow=True), cut=0)
            for sx in (-1, 1):
                spike(m, hd, (sx * 1.6, 31.0, 0), (sx * 0.5, 1, 0.2), 1.6, 5.0, CRYSTAL, tip=0.5)
                for j in range(3):                                                      # crystal claws
                    spike(m, bd, (sx * 6.0 + (j - 1) * 0.8, 13.0, -2.0), (sx * 0.2, -1, -0.3), 0.8, 4.0, DEEP, tip=0.2)
                wing(m, bd, (sx * 4.0, 22.0, 3.0), 16.0, 10.0, -sx * 55, -15, panef)
                wing(m, bd, (sx * 4.0, 18.0, 3.0), 12.0, 8.0, -sx * 110, -15, panef)
            rb = m.bone("ring_gold", bd, (8, 18, -3))
            for i in range(12):
                a0, a1 = 2 * math.pi * i / 12, 2 * math.pi * (i + 1) / 12
                rod(m, rb, (8 + 4 * math.cos(a0), 18 + 4 * math.sin(a0), -3), (8 + 4 * math.cos(a1), 18 + 4 * math.sin(a1),
                    -3), 1, solid(P, "gold", glow=True), extend=0.4, t2=2)
            for j in range(3):                                                          # spark above
                rod(m, hd, (j * 1.4, 32.0 + j * 2.4, 0), ((j + 1) * 1.4 - 2.8 * (j % 2), 34.4 + j * 2.4, 0), 1,
                    solid(P, "spark", glow=True), extend=0.2)
        elif stage == "perfect":
            m.round_box(bd, 0, 0, 2.0, 1.6, 28.0, 33.0, CRYSTAL, cut=1)
            hd = m.bone("head", bd, (0, 34, 0))
            m.round_box(hd, 0, 0, 1.6, 1.6, 33.0, 36.0, CRYSTAL, cut=0)
            for i in range(5):
                spike(m, hd, ((i - 2) * 0.8, 36.0, 0), ((i - 2) * 0.3, 1, 0), 0.8, 2.6, solid(P, "white"), tip=0.2)
            for sx in (-1, 1):                                                          # four vast pane wings
                wing(m, bd, (sx * 2.0, 32.0, 1.0), 26.0, 14.0, -sx * 40, -10, panef)
                wing(m, bd, (sx * 2.0, 30.0, 1.0), 22.0, 12.0, -sx * 95, -10, panef)
                pts = [(sx * 2.0, 31.0, 0), (sx * 8.0, 30.0, -2.0), (sx * 13.0, 27.0, -3.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, bd, p0, p1, 1, DEEP, extend=0.4)
            pts = [(0, 28.0, 0), (1.0, 23.0, 0), (-1.0, 18.0, 0), (1.0, 13.0, 1.0), (3.0, 8.0, 2.0), (6.0, 6.0, 2.0)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                            # dangling crystal chain
                rod(m, bd, p0, p1, 3 - j // 2, DEEP, extend=0.6)
            m.round_box(bd, 0, -1.0, 2.0, 1.6, 20.0, 25.0, DEEP, cut=1)                 # pendant gem
            for nm, sx in (("arm_left", 1), ("arm_right", -1)):
                m.bone(nm, bd, (sx * 2.0, 31.0, 0))
        else:
            m.round_box(bd, 0, 0, 2.4, 2.0, 22.0, 34.0, GOLD, cut=1)
            hd = m.bone("head", bd, (0, 35, 0))
            m.round_box(hd, 0, 0, 2.0, 2.0, 34.0, 38.0, GOLD, cut=1)
            for i in range(7):                                                          # crown of golden spikes
                ang = math.radians(-60 + i * 20)
                spike(m, hd, (2.0 * math.sin(ang), 38.0, 0), (math.sin(ang), 1, 0), 0.8, 4.0, GOLD, tip=0.2)
            for i in range(10):                                                         # bell of blue feathers
                ang = 2 * math.pi * i / 10
                spike(m, bd, (2.4 * math.cos(ang), 26.0, 2.0 * math.sin(ang)), (math.cos(ang), -1.2, math.sin(ang)),
                      2.4, 9.0, feathers(P, "feather", "feather_dark"), tip=1.0)
            for i in range(9):                                                          # rainbow crystal blades
                ang = -80 + i * 20
                wing(m, bd, (0, 28.0, 3.0), 26.0 - abs(i - 4) * 2.0, 6.0, ang, -10, rainbowf)
            m.round_box(bd, 0, 0, 3.0, 3.0, 6.0, 12.0, gem(P, "violet", "violet_light"), cut=1)   # violet orb
            rod(m, bd, (0, 22.0, 0), (0, 12.0, 0), 1, GOLD, extend=0)
            for nm, sx in (("arm_left", 1), ("arm_right", -1)):
                ab = m.bone(nm, bd, (sx * 2.4, 32.0, 0))
                rod(m, ab, (sx * 2.4, 32.0, 0), (sx * 6.0, 36.0, -1.0), 1, GOLD, extend=0.4)
        return m
    return build
