"""Shared builder for Stingmon and Stingmon (Black) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the insect warrior: a lean humanoid wasp in dark-green chitin armour with black-and-grey plates, a red
compound-eyed insect head with long striped antennae and a red hair tuft, four translucent wings, black pauldrons
and gauntlets with a retracting steel spike (Spiking Finish) on each arm, and big curved steel claws on its feet.
Black: charcoal-black chitin and grey plates. Shiny: purple / green.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import armour, metal, solid, strands
from _route import pal, tone


def make(name, black=False):
    base = {"green": (40, 90, 50) if not black else (40, 38, 44), "green_dark": (14, 40, 20) if not black else (12, 12, 16),
            "plate": (60, 62, 70), "plate_dark": (20, 20, 26), "red": (200, 40, 40), "steel": (200, 204, 216),
            "steel_dark": (100, 104, 120), "wing": (220, 236, 246, 150), "eye": (240, 60, 60)}
    shiny = {"green": (100, 50, 140), "green_dark": (40, 14, 70)} if not black else {"green": (40, 110, 60),
                                                                                    "green_dark": (14, 50, 20)}

    def P(v):
        return pal(base, shiny, v)

    CHITIN = armour(P, "green", "green_dark")
    PLATE = armour(P, "plate", "plate_dark")
    STEEL = metal(P, "steel", dark="steel_dark")

    def antf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        return tone(p["red"] if (y + z) % 2.4 < 1.0 else p["green"], face), None

    def build():
        m = Model(name)
        mats = {"skin": CHITIN, "deltoid": PLATE, "forearm": PLATE, "hand": PLATE, "finger": PLATE, "shin": PLATE,
                "foot": PLATE, "talon": STEEL}
        a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, talons=True, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 2.2, 2.8, 54.0, 60.0, CHITIN, cut=1)
        for sx in (-1, 1):
            m.round_box(hd, sx * 1.4, -2.6, 1.0, 1.0, 56.4, 58.6, solid(P, "eye", glow=True), cut=0)
            pts = [(sx * 1.0, 60.0, -1.0), (sx * 3.0, 66.0, -2.0), (sx * 6.0, 70.0, 2.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, hd, p0, p1, 1, antf, extend=0.2, t2=1)
        spike(m, hd, (0, 60.0, 1.0), (0, 0.6, 1), 1.4, 4.0, strands(P, "red", "red"), tip=0.8)
        for sx in (-1, 1):
            m.round_box(bd, sx * 7.6, 0, 3.0, 3.2, 46.0, 51.0, PLATE, cut=1)
            for j, ang in enumerate((25, -10)):                                          # four translucent wings
                x0, x1 = sorted((sx * 2.0, sx * 18.0))
                m.box(bd, x0, 40.0, 4.0 + j * 0.4, x1, 46.0, 4.0 + j * 0.4, solid(P, "wing"),
                      rotation=(0, -sx * 15, sx * ang), pivot=(sx * 2.0, 44.0, 4.0))
        for side in ("arm_left", "arm_right"):                                           # Spiking Finish spikes
            w = a[side]["wrist"]
            spike(m, a[side]["bone"], (w[0], w[1] + 4.0, w[2]), (0, -1, -0.3), 1.2, 10.0, STEEL, tip=0.8)
        return m

    return build
