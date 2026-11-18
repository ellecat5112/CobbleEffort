"""Shared builder for Meramon and Meramon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a man of living flame: a hunched figure whose body is dark red-black fire licked all over by orange and
yellow flames, tongues of fire rising from its head, shoulders and back, a jagged grin and burning eyes, and a ball of
fire in its right hand. The X-Antibody ("x"): a leaner, taller flame with an olive-gold core, long clawed fingers and
toes, a burning clenched fist and a crown of flames sweeping back from a pale blue face.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import humanoid
from _digidetail import cutout, flame_inside, fbm, local, solid
from _route import pal, tone

LOOKS = {"base": {"core": (120, 24, 14), "core_dark": (40, 8, 6), "face": (220, 110, 30)},
         "x": {"core": (150, 130, 40), "core_dark": (70, 50, 14), "face": (150, 200, 240)}}
COMMON = {"flame": (255, 150, 30, 215), "flame_core": (255, 236, 120, 235), "eye": (255, 250, 200),
          "mouth": (30, 6, 4), "claw": (250, 220, 120)}


def make(name, x=False):
    base = dict(COMMON, **LOOKS["x" if x else "base"])
    shiny = dict(base, core=(30, 40, 120), core_dark=(8, 10, 40), flame=(90, 160, 255, 215),
                 flame_core=(220, 240, 255, 235), face=(110, 140, 240))

    def P(v):
        return pal(base, shiny, v)

    def bodyf(x_, y, z, face, variant, box=None, **k):
        """Dark fire with bright flame tongues licking upward through it."""
        p = P(variant)
        n = fbm(x_ * 0.5, y * 0.35, z * 0.5, seed=3)
        t = n + 0.25 * math.sin(y * 0.9 + x_ * 0.7)
        if t > 0.62:
            return p["flame_core"][:3], p["flame_core"][:3]
        if t > 0.5:
            return p["flame"][:3], p["flame"][:3]
        return tone(p["core"] if t > 0.3 else p["core_dark"], face), None

    def firef(x_, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x_, y, z, face, box)
        c = p["flame_core"] if v / max(H, 1e-6) < 0.35 else p["flame"]
        return c, c[:3]

    FIRE = cutout(flame_inside(4, 0.1, 5), firef)

    def flame(m, bone, c, w, h, ang=0.0):
        for a in (0, 90):
            m.box(bone, c[0] - w / 2, c[1], c[2], c[0] + w / 2, c[1] + h, c[2], FIRE, rotation=(0, a + ang, 0),
                  pivot=c)

    def build():
        m = Model(name)
        mats = {"skin": bodyf, "claw": solid(P, "claw"), "talon": solid(P, "claw")}
        a = humanoid(m, mats, bulk=0.95 if not x else 0.8, arm_bulk=1.0, leg_bulk=0.95 if not x else 0.85,
                     claws=x, talons=x, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 2.8, 3.0, 53.6, 60.2, bodyf, cut=1)
        m.box(hd, -2.0, 56.4, -3.7, 2.0, 59.6, -3.5, solid(P, "face"))                   # face
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.4, sx * 1.6), 58.0, -3.8, max(sx * 0.4, sx * 1.6), 58.9, -3.7,
                  solid(P, "eye", glow=True))
        for j in range(5):                                                                # jagged grin
            m.box(hd, -1.6 + j * 0.7, 56.8 + 0.3 * (j % 2), -3.8, -1.2 + j * 0.7, 57.4 + 0.3 * (j % 2), -3.7,
                  solid(P, "mouth"))
        for j in range(5):                                                                # crown of flames
            flame(m, hd, ((j - 2) * 1.2, 59.0, 0.6 + abs(j - 2) * 0.6), 3.0, 7.0 - abs(j - 2) * 1.2 + (2 if x else 0))
        for sx in (-1, 1):                                                                # shoulder + back flames
            flame(m, bd, (sx * 6.4, 50.0, 0.4), 4.0, 7.0)
            flame(m, bd, (sx * 3.0, 40.0, 3.0), 3.4, 8.0)
        for nm in ("leg_left", "leg_right", "arm_left", "arm_right"):                     # flames off the limbs
            anc = a[nm]
            j = anc.get("knee") or anc.get("elbow")
            flame(m, anc["bone"], (j[0], j[1] - 2.0, j[2] + 0.6), 3.0, 5.0)
        ar = a["arm_right"]
        h = ar["hand"]
        if not x:                                                                          # fireball in its hand
            ball(m, ar["bone"], (h[0] - 1.0, h[1] - 3.0, h[2] - 2.0), 3.0, firef, layers=4)
            flame(m, ar["bone"], (h[0] - 1.0, h[1] - 1.0, h[2] - 2.0), 5.0, 6.0)
        else:
            al = a["arm_left"]
            hl = al["hand"]
            ball(m, al["bone"], (hl[0], hl[1] - 1.0, hl[2]), 2.2, bodyf, layers=3)          # clenched burning fist
            flame(m, al["bone"], (hl[0], hl[1], hl[2]), 4.0, 6.0)
        return m

    return build
