"""Shared builders for the DORU line's large forms (CobbleEffort: Digital; hand-built after the official art on
wikimon.net). Each takes a `look` palette key: "death" = the Death-X forms (Death-X-DORUgamon .. -goramon), others are
added for the plain forms as they come.

- gamon(name, look): a four-legged dragon with a riveted steel muzzle mask, bolts on its head, two enormous swept-back
  fin-wings, steel-banded legs with hooked claws and a long tail spitting sparking wires.
- guremon(name, look): an upright flying dragon with a beaked black helm, huge layered feather wings, hooked claws and
  a chain trailing a spiked iron ball.
- goramon(name, look): a great four-legged dragon with a saw-blade steel snout, a crest of long feather spines and
  bone blades down its back and several whip tails tipped with blades.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing, quadruped
from _digidetail import armour, cutout, feathers, gem, local, metal, riveted, scales, skin, solid
from _route import pal, tone

LOOKS = {
    "death": ({"hide": (40, 60, 110), "hide_dark": (14, 20, 46), "hide_light": (90, 120, 190), "black": (40, 36, 46),
               "black_dark": (14, 12, 18), "black_light": (100, 90, 120), "violet": (100, 60, 150),
               "feather": (190, 30, 40), "feather_dark": (60, 10, 20), "feather_tip": (30, 26, 30),
               "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "claw": (200, 30, 50),
               "claw_light": (255, 140, 150), "eye": (250, 60, 60), "mouth": (120, 20, 40), "tooth": (250, 250, 246),
               "spark": (255, 240, 120), "wire": (220, 40, 40), "ball": (150, 140, 170, 170)},
              {"hide": (120, 120, 130), "hide_dark": (50, 50, 60), "hide_light": (190, 190, 200),
               "black": (200, 200, 210), "black_dark": (120, 120, 130), "feather": (60, 120, 220),
               "feather_dark": (20, 40, 110), "claw": (240, 190, 40)}),
}


def palette(look):
    base, shiny = LOOKS[look]

    def P(v):
        return pal(base, shiny, v)
    return P


def gamon(name, look="death"):
    P = palette(look)
    HIDE = scales(P, "hide", "hide_dark", size=1.6, light="hide_light", rim_mix=0.3)
    MASK = riveted(P, "steel", "steel_dark")
    STEEL = metal(P, "steel", dark="steel_dark")
    CLAW = gem(P, "claw", "claw_light", glow=False)

    def build():
        m = Model(name)
        mats = {"skin": HIDE, "belly": HIDE, "neck": HIDE, "head": HIDE, "snout": MASK, "jaw": MASK,
                "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": HIDE, "leg_lower": HIDE,
                "paw": HIDE, "claw": CLAW, "tail": HIDE}
        a = quadruped(m, mats, name, length=30.0, body_y=16.0, body_rx=7.0, body_ry=6.6, chest_bulk=1.3,
                      neck=((0, 20, -14), (0, 23, -18)), head_len=9.0, head_w=4.4, head_h=4.4, snout=0.6,
                      mouth_open=8, teeth=4, leg_bulk=1.5, toes=3,
                      tail=((0, 18, 15), (0, 22, 22), (2, 28, 27), (4, 33, 29)), tail_r=(2.6, 2.0, 1.4, 1.0))
        bd, hd = a["body"], a["head"]
        for sx in (-1, 1):
            m.box(hd, min(sx * 4.4, sx * 4.8), 24.0, -22.0, max(sx * 4.4, sx * 4.8), 25.0, -20.6,
                  solid(P, "eye", glow=True))
            m.round_box(hd, sx * 4.6, -18.0, 1.0, 1.0, 26.0, 28.0, STEEL, cut=0)            # head bolts
        for side in (1, -1):                                                     # enormous swept fin-wings
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 22.0, -2.0))
            pts = [(side * 5.0, 22.0, 0.0), (side * 11.0, 28.0, 6.0), (side * 15.0, 34.0, 13.0),
                   (side * 17.0, 39.0, 21.0)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, wb, p0, p1, 2, HIDE, extend=0.6, t2=6 - j * 2)
            spike(m, wb, pts[-1], (0, 0.4, 1), 2.0, 4.0, HIDE, tip=0.3)
        for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
            lg = a[nm]
            w = lg["wrist"]
            for j in range(2):
                m.round_box(lg["bone"], w[0], w[2], 2.4, 2.4, 4.0 + j * 2.4, 5.2 + j * 2.4, STEEL, cut=1)
        e = a["tail_pts"][-1]
        for j in range(3):                                                       # sparking wires
            d = (math.cos(j * 2.1), 1.0, math.sin(j * 2.1))
            rod(m, a["tail"], e, (e[0] + d[0] * 3, e[1] + 4.0, e[2] + d[2] * 3), 1,
                solid(P, "wire" if j % 2 else "spark", glow=j % 2 == 0), extend=0.2)
        return m
    return build


def guremon(name, look="death"):
    P = palette(look)
    HIDE = skin(P, "black", dark="black_dark", light="black_light")
    HELM = armour(P, "black", "black_dark", light="black_light", trim="violet", trim_w=0.3)
    FEATH = feathers(P, "feather", "feather_dark", size=(1.4, 3.0), tip="feather_tip")
    CLAW = gem(P, "claw", "claw_light", glow=False)
    STEEL = metal(P, "steel", dark="steel_dark")

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 30, 0))
        m.round_box(bd, 0, 0, 5.0, 4.4, 24.0, 38.0, HIDE, cut=2)
        m.round_box(bd, 0, -2.0, 3.6, 2.6, 26.0, 36.0, HELM, cut=1)                      # chest plate
        hd = m.bone("head", bd, (0, 40, -2))
        m.round_box(hd, 0, -2.0, 3.2, 4.0, 38.0, 45.0, HELM, cut=1)
        spike(m, hd, (0, 41.0, -6.0), (0, -0.4, -1), 2.6, 6.0, HELM, tip=0.3)               # beaked helm
        for sx in (-1, 1):
            m.box(hd, min(sx * 1.8, sx * 3.3), 42.0, -6.2, max(sx * 1.8, sx * 3.3), 42.8, -5.8,
                  solid(P, "eye", glow=True))
            spike(m, hd, (sx * 2.0, 44.6, 0), (sx * 0.4, 0.6, 1), 1.6, 6.0, HELM, tip=0.25)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 5.0, 35.0, 0))
            rod(m, ab, (sx * 5.0, 35.0, 0), (sx * 8.0, 28.0, -3.0), 2, HIDE, extend=0.4)
            for j in range(3):
                spike(m, ab, (sx * 8.0 + (j - 1) * 0.8, 27.0, -3.6), (0, -1, -0.4), 0.9, 3.4, CLAW, tip=0.25)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 3.0, 24.0, 0))
            rod(m, lg, (sx * 3.0, 24.0, 0), (sx * 4.0, 14.0, -2.0), 3, HIDE, extend=0.4)
            rod(m, lg, (sx * 4.0, 14.0, -2.0), (sx * 4.0, 8.0, 1.0), 2, HIDE, extend=0.4)
            for j in range(3):
                spike(m, lg, (sx * 4.0 + (j - 1) * 1.0, 7.6, 0.0), (0, -0.6, -1), 1.0, 4.0, CLAW, tip=0.25)
        tl = m.bone("tail", bd, (0, 25, 3))
        pts = [(0, 25.0, 3.0), (0, 18.0, 8.0), (2.0, 12.0, 10.0), (3.0, 8.0, 8.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tl, p0, p1, 3 - j, HIDE, extend=0.5)
        cb = m.bone("chain", tl, (3, 8, 8))                                              # chain + iron ball
        for j in range(2):
            y = 7.0 - j * 1.2
            m.box(cb, 2.4 + (j % 2) * 0.4, y - 0.6, 7.6, 3.6 - (j % 2) * 0.4, y + 0.6, 8.4, STEEL)
        m.round_box(cb, 3.0, 8.0, 2.6, 2.6, 0.2, 5.4, solid(P, "ball"), cut=1)
        for ang in range(0, 360, 60):
            r = math.radians(ang)
            spike(m, cb, (3.0 + 2.6 * math.cos(r), 2.8, 8.0 + 2.6 * math.sin(r)), (math.cos(r), 0, math.sin(r)),
                  1.0, 1.6, STEEL)
        for side in (1, -1):                                                             # layered feather wings
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 36.0, 3.0))
            feather_wing(m, wb, (side * 3.0, 36.0, 3.0), 22.0, 14.0, 3, FEATH, side=side, sweep=30, droop=-4.0)
            feather_wing(m, wb, (side * 3.0, 32.0, 4.0), 16.0, 10.0, 2, FEATH, side=side, sweep=45, droop=2.0)
        return m
    return build


def goramon(name, look="death"):
    P = palette(look)
    HIDE = scales(P, "black", "black_dark", size=1.8, light="black_light", rim_mix=0.3)
    FEATH = feathers(P, "feather", "feather_dark", size=(1.4, 3.0), tip="feather_tip")
    STEEL = metal(P, "steel", dark="steel_dark")
    CLAW = gem(P, "claw", "claw_light", glow=False)

    def build():
        m = Model(name)
        mats = {"skin": HIDE, "belly": HIDE, "neck": HIDE, "head": HIDE, "snout": STEEL, "jaw": STEEL,
                "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": HIDE, "leg_lower": HIDE,
                "paw": HIDE, "claw": CLAW, "tail": HIDE}
        a = quadruped(m, mats, name, length=40.0, body_y=18.0, body_rx=8.0, body_ry=7.6, chest_bulk=1.2,
                      neck=((0, 24, -19), (0, 30, -25)), head_len=10.0, head_w=4.4, head_h=4.4, snout=0.5,
                      mouth_open=6, teeth=4, leg_bulk=1.8, toes=4, tail=((0, 20, 20), (0, 22, 27), (0, 26, 32)),
                      tail_r=(3.0, 2.2, 1.6))
        bd, hd = a["body"], a["head"]
        ny, sf = a["mouth_y"] + 1.0, a["snout_front"]
        for j in range(5):                                                       # saw-blade snout
            spike(m, hd, (0, ny - 1.2, sf - 1.0 - j * 2.2), (0, -1, -0.2), 1.0, 2.0, STEEL)
            spike(m, hd, (0, ny + 1.2, sf - 1.0 - j * 2.2), (0, 1, -0.2), 1.0, 2.0, STEEL)
        rod(m, hd, (0, ny, sf + 1.0), (0, ny, sf - 11.0), 2, STEEL, extend=0, t2=3)
        ex, ey, ez = a["eye"]
        for sx in (-1, 1):
            m.box(hd, min(sx * ex, sx * (ex + 0.4)), ey - 0.5, ez - 0.7, max(sx * ex, sx * (ex + 0.4)), ey + 0.5,
                  ez + 0.7, solid(P, "eye", glow=True))
        for i in range(14):                                                      # crest of feather spines + blades
            t = i / 13
            z = -18.0 + 34.0 * t
            for sx in (-1, 1):
                spike(m, bd, (sx * 2.6, 24.0 - 2.0 * t, z), (sx * 0.5, 1.0, 0.8), 2.4, 20.0 - 8.0 * t, FEATH, tip=1.2)
            if i % 2 == 0:
                spike(m, bd, (0, 25.6, z), (0, 1, 0.9), 1.2, 7.0, STEEL, tip=0.2)
        for k in range(3):                                                       # whip tails with blades
            ang = (k - 1) * 0.6
            base = a["tail_pts"][-1]
            pts = [base]
            for j in range(1, 5):
                pts.append((base[0] + math.sin(ang) * 4.0 * j, base[1] + math.sin(j * 1.1 + k) * 2.0,
                            base[2] + 3.6 * j))
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, a["tail"], p0, p1, 1, solid(P, "feather"), extend=0.4, t2=2)
            spike(m, a["tail"], pts[-1], (math.sin(ang), 0, 1), 1.6, 3.0, STEEL, tip=0.2)
        return m
    return build
