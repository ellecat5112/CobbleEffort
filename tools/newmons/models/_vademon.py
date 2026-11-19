"""Shared builder for Vademon and Vademon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a space alien: an enormous wrinkled pink brain for a head with goggling yellow eyes on its brow, a wire
trailing from it, a long scrawny orange body, spindly arms, a chunky silver ray gun in one hand, and a skirt of
writhing green-tipped tentacles for legs. X-Antibody: a grey-green body in a black vest, a mottled khaki brain carved
with patterns, an ear ring, and a sickly purple-brown tentacle skirt. Shiny: blue brain, green body."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import eye, fabric, fbm, metal, plane, skin, solid
from _route import pal, tone

LOOKS = {False: {"brain": (220, 140, 190), "brain_dark": (140, 70, 120), "body": (240, 170, 120),
                 "body_dark": (190, 110, 70), "tip": (160, 220, 90), "vest": (40, 40, 44)},
         True: {"brain": (170, 170, 110), "brain_dark": (100, 100, 60), "body": (120, 130, 120),
                "body_dark": (60, 70, 60), "tip": (160, 120, 150), "vest": (34, 34, 38)}}
COMMON = {"eye": (250, 220, 40), "pupil": (20, 10, 10), "white": (255, 255, 255), "gun": (200, 204, 216),
          "gun_dark": (100, 104, 120), "wire": (40, 40, 46), "gold": (230, 190, 60)}
SHINY = {"brain": (130, 170, 240), "brain_dark": (60, 90, 170), "body": (130, 200, 130), "body_dark": (60, 130, 60)}


def make(name, x=False):
    base = dict(COMMON, **LOOKS[x])

    def P(v):
        return pal(base, SHINY, v)

    BODY = skin(P, "body", dark="body_dark")

    def brainf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        t = fbm(xx * 0.6, y * 0.6, z * 0.6, seed=7)
        if abs(math.sin(xx * 1.3 + t * 6.0) * math.cos(z * 1.1 + t * 4.0)) < 0.18:
            return tone(p["brain_dark"], face), None
        return tone(p["brain"], face), None

    def tentf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if y < 1.6:
            return tone(p["tip"], face), None
        return BODY(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 10, 0))
        for i in range(8):                                                         # tentacle skirt
            ang = i * 2 * math.pi / 8
            pts = [(1.4 * math.cos(ang), 12.0, 1.4 * math.sin(ang)), (4.0 * math.cos(ang), 6.0, 4.0 * math.sin(ang)),
                   (7.0 * math.cos(ang + 0.3), 1.0, 7.0 * math.sin(ang + 0.3)),
                   (8.4 * math.cos(ang + 0.7), 0.6, 8.4 * math.sin(ang + 0.7))]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, bd, p0, p1, 2 if j < 1 else 1, tentf, extend=0.4)
        m.round_box(bd, 0, 0, 1.8, 1.4, 12.0, 30.0, BODY, cut=0)                       # scrawny body
        if x:
            m.round_box(bd, 0, 0, 2.4, 2.0, 20.0, 30.0, fabric(P, "vest", "vest"), cut=1)
        hd = m.bone("head", bd, (0, 30, 0))
        rod(m, hd, (0, 30.0, 0), (0, 36.0, 0), 1, BODY, extend=0.3)
        for sx in (-1, 1):
            ball(m, hd, (sx * 1.6, 35.0, -1.6), 1.3, solid(P, "white"), layers=1)
            ball(m, hd, (sx * 1.6, 35.0, -2.6), 0.7, solid(P, "eye", glow=True), layers=1)
        ball(m, hd, (0, 42.0, 0), 6.4, brainf, layers=5, squash=0.9)
        pts = [(5.0, 39.0, 0), (7.0, 34.0, 0), (6.0, 30.0, -1.0)]                       # trailing wire
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "wire"), extend=0.2)
        if x:
            ball(m, hd, (-5.6, 38.6, 0), 0.8, metal(P, "gold"), layers=1)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 1.8, 28.0, 0))
            rod(m, ab, (sx * 1.8, 28.0, 0), (sx * 6.0, 22.0, -2.0), 1, BODY, extend=0.3)
            rod(m, ab, (sx * 6.0, 22.0, -2.0), (sx * 7.0, 26.0, -4.0), 1, BODY, extend=0.3)
        rb = "arm_right"                                                               # ray gun
        m.round_box(rb, -7.0, -6.0, 1.6, 2.6, 25.0, 28.2, metal(P, "gun", dark="gun_dark"), cut=1)
        rod(m, rb, (-7.0, 26.6, -8.0), (-7.0, 26.6, -11.0), 1, metal(P, "gun"), extend=0.0)
        ball(m, rb, (-7.0, 26.6, -11.6), 1.0, metal(P, "gold"), layers=1)
        return m
    return build
