"""Shared builder for Mega Seadramon and Mega Seadramon (X-Antibody) (CobbleEffort: Digital; hand-built after the
official art on wikimon.net): a great sea serpent coiled in an S, its long white body chevroned with blue scales and
edged with rows of red fin-blades, a red underside, a black tail tip with a green finned tuft, and a golden armoured
helm on its long-jawed head with a lightning-bolt horn and a green mane. The X-Antibody ("x"): a pale yellow body with
red-orange leopard spots and orange fins, a brown bone-skull helm with a great curved tusk-blade, swept horns and
green fins on its back, and a violet finned tail tip.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import jaws
from _digidetail import armour, metal, scales, solid
from _route import pal, tone

LOOKS = {
    "base": {"body": (236, 240, 248), "body_dark": (150, 170, 200), "chev": (60, 110, 200), "fin": (220, 40, 50),
             "fin_dark": (130, 14, 24), "belly": (210, 50, 60), "helm": (230, 190, 90), "helm_dark": (150, 110, 40),
             "horn": (220, 224, 236), "horn_dark": (120, 124, 140), "mane": (90, 160, 70), "tail": (30, 30, 36),
             "tuft": (110, 170, 60)},
    "x": {"body": (240, 220, 140), "body_dark": (190, 160, 70), "chev": (200, 80, 30), "fin": (230, 110, 40),
          "fin_dark": (150, 50, 14), "belly": (250, 240, 200), "helm": (170, 130, 80), "helm_dark": (100, 70, 40),
          "horn": (210, 214, 220), "horn_dark": (110, 114, 124), "mane": (60, 140, 160), "tail": (200, 70, 30),
          "tuft": (110, 80, 200)}}
COMMON = {"eye": (90, 200, 250), "mouth": (200, 70, 110), "tooth": (250, 250, 240), "green": (60, 160, 60)}


def make(name, look="base"):
    base = dict(COMMON, **LOOKS[look])
    shiny = dict(base, body=(60, 64, 80), body_dark=(24, 26, 36), chev=(200, 190, 60), belly=(230, 200, 60)) \
        if look == "base" else dict(base, body=(170, 230, 210), body_dark=(90, 160, 140), chev=(40, 90, 160))
    x = look == "x"

    def P(v):
        return pal(base, shiny, v)

    HELM = armour(P, "helm", "helm_dark", trim="helm_dark", trim_w=0.3)
    HORN = metal(P, "horn", dark="horn_dark")
    FIN = scales(P, "fin", "fin_dark", size=1.2)
    SC = scales(P, "body", "body_dark", size=1.4)

    def bodyf(x_, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "down":
            return tone(p["belly"], face), None
        if x:
            if (math.sin(x_ * 0.9 + z * 0.7) * math.sin(y * 0.8 - z * 0.5)) > 0.55:
                return tone(p["chev"], face), None
        elif abs(((y * 0.6 + abs(x_) * 0.6 + z * 0.3) % 2.6) - 1.3) < 0.28:
            return tone(p["chev"], face), None
        return SC(x_, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 20, 0))
        pts = []
        for i in range(26):                                                           # S-coiled serpent body
            t = i / 25
            pts.append((9.0 * math.sin(t * 2.2 * math.pi) * (1 - 0.3 * t), 38.0 - 34.0 * t + 3.0 * math.sin(t * 6.0),
                        2.0 + 6.0 * math.cos(t * 2.2 * math.pi)))
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            r = 6 if j < 6 else 5 if j < 14 else 4 if j < 19 else 3 if j < 22 else 2
            rod(m, bd, p0, p1, r, bodyf if j < 22 else solid(P, "tail"), extend=0.8)
            if j % 2 == 0 and j < 22:                                                 # rows of red fin-blades
                for sx in (-1, 1):
                    spike(m, bd, (p0[0] + sx * r * 0.4, p0[1] + r * 0.3, p0[2]), (sx * 0.9, 0.5, 0.6), 1.6,
                          5.0 - j * 0.12, FIN, tip=0.8)
        e = pts[-1]
        for j in range(5):                                                            # finned tail tuft
            ang = math.radians(-60 + j * 30)
            spike(m, bd, e, (math.sin(ang), -0.4, math.cos(ang)), 1.2, 6.0, solid(P, "tuft"), tip=0.8)
        h = pts[0]
        hd = m.bone("head", bd, h)
        hx, hy, hz = h[0], h[1] + 2.0, h[2] - 2.0
        m.round_box(hd, hx, hz - 3.0, 4.6, 5.0, hy - 2.0, hy + 5.0, HELM, cut=1)       # golden/bone helm
        m.round_box(hd, hx, hz - 11.0, 3.2, 5.0, hy + 0.6, hy + 3.6, HELM, cut=1)     # long upper jaw
        jb = m.bone("jaw", hd, (hx, hy, hz - 6.0))
        m.round_box(jb, hx, hz - 10.0, 2.8, 4.6, hy - 1.6, hy + 0.2, SC, cut=1)       # lower jaw
        m.box(jb, hx - 2.2, hy + 0.2, hz - 14.0, hx + 2.2, hy + 0.5, hz - 7.0, solid(P, "mouth"))
        m.box(jb, hx - 0.8, hy + 0.5, hz - 15.0, hx + 0.8, hy + 1.0, hz - 9.0, solid(P, "mouth"))   # tongue
        for j in range(6):
            for sx in (-1, 1):
                spike(m, hd, (hx + sx * 2.6, hy + 0.6, hz - 7.0 - j * 1.4), (0, -1, 0), 0.8, 1.6, solid(P, "tooth"),
                      tip=0.8)
        for sx in (-1, 1):
            m.box(hd, hx + min(sx * 4.6, sx * 4.9), hy + 3.0, hz - 6.0, hx + max(sx * 4.6, sx * 4.9), hy + 4.2,
                  hz - 4.0, solid(P, "eye", glow=True))
            for j in range(4):                                                        # mane fins behind the helm
                spike(m, hd, (hx + sx * 3.0, hy + 3.0 - j * 1.6, hz + 2.0), (sx * 0.5, 0.3, 1), 1.4, 9.0 - j,
                      solid(P, "mane"), tip=0.8)
        if not x:
            pts_b = [(hx, hy + 5.0, hz - 2.0), (hx, hy + 9.0, hz + 1.0), (hx, hy + 8.0, hz + 4.0), (hx, hy + 12.0,
                                                                                                  hz + 9.0)]
            for p0, p1 in zip(pts_b, pts_b[1:]):                                      # lightning-bolt horn
                rod(m, hd, p0, p1, 2, HORN, extend=0.4)
            spike(m, hd, pts_b[-1], (0, 0.5, 1), 1.6, 5.0, HORN, tip=0.8)
            for j in range(4):
                spike(m, hd, (hx, hy + 5.0, hz + 1.0 + j), (0, 0.7, 1), 1.2, 7.0 - j, solid(P, "green"), tip=0.8)
        else:
            rod(m, hd, (hx, hy + 2.0, hz - 1.0), (hx - 9.0, hy + 9.0, hz + 2.0), 2, HORN, extend=0.4)   # tusk-blade
            m.box(hd, hx - 15.0, hy + 4.0, hz + 1.6, hx - 6.0, hy + 14.0, hz + 2.4, HORN,
                  rotation=(0, 0, -30), pivot=(hx - 9.0, hy + 9.0, hz + 2.0))
            for sx in (-1, 1):
                spike(m, hd, (hx + sx * 3.0, hy + 5.0, hz), (sx * 0.4, 0.5, 1), 1.6, 9.0, HELM, tip=0.8)
            for j in range(4):                                                        # green back fins
                spike(m, bd, pts[3 + j * 2], (0.2, 1, 0.5), 1.6, 8.0 - j, solid(P, "green"), tip=0.8)
        return m

    return build
