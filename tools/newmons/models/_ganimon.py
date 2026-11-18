"""Shared builder for Ganimon and Ganimon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a grey-blue crab with red blotches, a spiky shell, a little green-eyed face with fangs, thin jointed legs
and one great pincer. The X-Antibody form is broader and darker blue, with a shark-toothed maw, red-striped legs and a
huge curved claw. Shiny: sandy orange.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import armour, fbm, solid
from _route import pal, tone


def make(name, x=False):
    base = {"shell": (130, 150, 190), "shell_dark": (60, 70, 110), "shell_light": (200, 210, 240), "red": (210, 50, 60),
            "eye": (90, 200, 90), "pupil": (16, 16, 20), "tooth": (250, 250, 246), "mouth": (60, 20, 30)}
    if x:
        base.update({"shell": (80, 100, 170), "shell_dark": (30, 40, 90), "eye": (230, 40, 40)})
    shiny = {"shell": (230, 170, 90), "shell_dark": (160, 100, 40), "shell_light": (255, 220, 160)}

    def P(v):
        return pal(base, shiny, v)

    ARM = armour(P, "shell", "shell_dark", light="shell_light")

    def shellf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if fbm(xx * 0.5, y * 0.5, z * 0.5, seed=3) > (0.66 if not x else 0.8):
            return tone(p["red"], face), None
        if x and face in ("east", "west") and abs((xx * 0.8) % 3.0 - 1.5) < 0.25:
            return tone(p["red"], face), None
        return ARM(xx, y, z, face, variant, box=box, **k)

    s = 1.25 if x else 1.0

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 8, 0))
        m.round_box(bd, 0, 1.0, 6.0 * s, 5.0 * s, 6.0, 6.0 + 7.0 * s, shellf, cut=2)          # carapace
        for j in range(5 if x else 3):                                                         # shell spikes
            spike(m, bd, ((j - (2 if x else 1)) * 2.4, 6.0 + 7.0 * s, 1.0), (0, 1, 0.3), 1.6, 3.0 + j % 2,
                  shellf, tip=0.8)
        hd = m.bone("head", bd, (0, 10, -5))
        m.round_box(hd, 0, -5.0 * s, 3.4 * s, 1.6, 8.0, 8.0 + 4.0 * s, shellf, cut=1)
        for sx in (-1, 1):
            m.round_box(hd, sx * 1.6 * s, -5.0 * s - 1.8, 1.0, 0.4, 10.4, 12.0, solid(P, "eye"), cut=0)
            m.box(hd, sx * 1.6 * s - 0.3, 10.8, -5.0 * s - 2.4, sx * 1.6 * s + 0.3, 11.6, -5.0 * s - 2.2,
                  solid(P, "pupil"))
        m.box(hd, -2.0 * s, 8.6, -5.0 * s - 1.9, 2.0 * s, 9.6, -5.0 * s - 1.6, solid(P, "mouth"))
        for j in range(6 if x else 2):
            xx = -1.8 * s + j * (3.6 * s / max(1, (5 if x else 1)))
            spike(m, hd, (xx, 9.4, -5.0 * s - 1.7), (0, -1, 0), 0.6, 1.2, solid(P, "tooth"))
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                    # jointed legs
            lg = m.bone(nm, bd, (sx * 5.0, 8.0, 0))
            for j, dz in enumerate((-3.0, 0.0, 3.0)):
                knee = (sx * (10.0 * s), 12.0, dz * s)
                rod(m, lg, (sx * 5.0, 9.0, dz), knee, 1, shellf, extend=0.3, t2=1)
                rod(m, lg, knee, (sx * 13.0 * s, 0.6, dz * s * 1.3), 1, shellf, extend=0.3, t2=1)
        ab = m.bone("arm_right", bd, (-5.0, 10.0, -3.0))                                       # the great pincer
        rod(m, ab, (-5.0, 10.0, -3.0), (-10.0 * s, 14.0, -8.0), 2, shellf, extend=0.4)
        m.round_box(ab, -11.0 * s, -10.0, 2.4 * s, 3.0 * s, 12.0, 18.0, shellf, cut=1)
        for sy in (-1, 1):
            spike(m, ab, (-11.0 * s, 15.0 + sy * 2.0, -13.0), (0, -sy * 0.3, -1), 1.6, 6.0 * s, shellf, tip=0.8)
        ab2 = m.bone("arm_left", bd, (5.0, 10.0, -3.0))
        rod(m, ab2, (5.0, 10.0, -3.0), (8.0 * s, 8.0, -7.0), 1, shellf, extend=0.3, t2=1)
        spike(m, ab2, (8.0 * s, 8.0, -7.0), (0.3, -0.2, -1), 1.4, 4.0 * s, shellf, tip=0.8)
        return m

    return build
