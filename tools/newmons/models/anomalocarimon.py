"""Anomalocarimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): an ancient crustacean. A long segmented tan body with red markings, round black stalk
eyes and a big blue eye on its head, two huge curled feeding claws ringed in segments under its head, rows of long
silver blade-fins down both sides and a fan of blades at its tail. 25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage. Anomalocarimon (X-Antibody) uses make(x=True): rainbow colours,
blue claws, scythe blades.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, slab_z
from _digidetail import armour, cutout, eye, local, metal, mix, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("an ancient crustacean: a long segmented tan body with red markings, black stalk eyes, two huge curled "
        "segmented feeding claws and rows of long silver blade-fins down its sides")
BASE = {"shell": (226, 190, 140), "shell_dark": (150, 110, 70), "shell_light": (250, 230, 190), "mark": (200, 70, 50),
        "blade": (210, 216, 230), "blade_dark": (110, 116, 134), "blade_tip": (40, 110, 130), "stalk": (30, 30, 36),
        "eye": (60, 160, 240), "pupil": (16, 16, 20), "white": (250, 250, 250),
        "c1": (230, 60, 50), "c2": (250, 160, 40), "c3": (80, 180, 80), "claw_x": (40, 90, 220), "claw_x_dark": (16, 40, 130)}
SHINY = {"shell": (150, 150, 170), "shell_dark": (80, 80, 100), "shell_light": (210, 210, 230), "mark": (60, 150, 230),
         "c1": (140, 60, 200), "c2": (60, 130, 230), "c3": (60, 200, 200), "claw_x": (220, 170, 40),
         "claw_x_dark": (150, 100, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    BLADE = metal(P, "claw_x" if x else "blade", dark="claw_x_dark" if x else "blade_dark")

    def shellf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if x:
            t = (z + 20) / 40.0                                  # rainbow from head to tail
            cols = [p["c1"], p["c2"], p["c3"], p["claw_x"]]
            i = max(0, min(2, int(t * 3)))
            base = mix(cols[i], cols[i + 1], max(0.0, min(1.0, t * 3 - i)))
        else:
            base = p["shell"]
        u, v, W, H = local(xx, y, z, face, box)
        if face == "up" and abs(xx) < 1.6 and (z % 4.0) < 1.0:
            return tone(p["mark"], face), None                   # red marks down its back
        if min(v, H - v) < 0.4 and face not in ("up", "down"):
            return tone(mix(base, (0, 0, 0), 0.35), face), None  # segment seams
        return tone(base, face), None

    def headf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("east", "west"):
            c = eye(p, z + 16.0, y - 20.0, 1.4, "eye")
            if c is not None:
                return c, None
        return shellf(xx, y, z, face, variant, box=box, **k)

    def fin_shape(xx, y, z, face, box):
        u, v, W, H = local(xx, y, z, face, box)
        t = u / max(W, 1e-6)
        return abs(v / max(H, 1e-6) - 0.5) < 0.5 * (1 - t) + 0.05

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 18, 0))
        for i in range(9):                                       # the segmented body, tapering to the tail
            z0 = -10 + i * 3.4
            r = 6.4 - max(0, i - 2) * 0.55
            slab_z(m, bd, 0, 18.0 + i * 0.4, z0, z0 + 3.6, r, r * 0.6, shellf)
            for sx in (-1, 1):                                   # a pair of blade-fins per segment
                x0, x1 = sorted((sx * r, sx * (r + 9.0 - i * 0.5)))
                m.box(bd, x0, 17.0 + i * 0.4, z0 + 1.0, x1, 21.0 + i * 0.4, z0 + 1.0, cutout(fin_shape, BLADE),
                      rotation=(-10, sx * 20, sx * (20 - i * 2)), pivot=(sx * r, 19.0 + i * 0.4, z0 + 1.0))
        tl = m.bone("tail", bd, (0, 21, 20))
        for j in range(5):                                       # tail fan of blades
            ang = math.radians(-50 + j * 25)
            rod(m, tl, (0, 21.6, 20.0), (8.0 * math.sin(ang), 24.0, 20.0 + 8.0 * math.cos(ang)), 2, BLADE, extend=0.2,
                t2=1)
        hd = m.bone("head", bd, (0, 19, -10))
        slab_z(m, hd, 0, 19.0, -17.0, -9.6, 5.2, 3.6, headf)
        for sx in (-1, 1):                                       # stalk eyes
            rod(m, hd, (sx * 2.6, 22.0, -15.0), (sx * 4.2, 25.0, -16.0), 1, solid(P, "stalk"), extend=0.2)
            ball(m, hd, (sx * 4.4, 25.6, -16.2), 1.2, solid(P, "stalk"), layers=2)
            cl = m.bone("arm_left" if sx > 0 else "arm_right", hd, (sx * 2.8, 17.0, -16.0))
            ang0 = 0.0
            p = (sx * 2.8, 17.0, -16.0)
            for j in range(9):                                   # the great curled feeding claw
                ang0 += 0.42
                q = (p[0] + sx * 0.6, p[1] - 2.4 * math.cos(ang0) * 0.9, p[2] - 2.6 * math.sin(ang0 + 0.6))
                rod(m, cl, p, q, max(1, 4 - j // 3), shellf if not x else BLADE, extend=0.5)
                if j % 2 == 0:
                    spike(m, cl, q, (0, 0.3, 1), 0.8, 1.6, BLADE)
                p = q
            if x:                                                # X: scythe blades from its head
                rod(m, hd, (sx * 3.0, 21.0, -12.0), (sx * 14.0, 30.0, -6.0), 2, BLADE, extend=0.3)
                spike(m, hd, (sx * 14.0, 30.0, -6.0), (sx * 0.6, -0.4, 1), 1.4, 6.0, BLADE)
        return m
    return build


build = make("anomalocarimon")
