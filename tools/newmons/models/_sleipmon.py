"""Shared builder for Sleipmon and its forms (CobbleEffort: Digital; hand-built after the official art on wikimon.net):
the Royal Knight centaur: a six-legged horse body in crimson armour with silver-and-blue swirl shields and gold-banded
hooves, a centaur knight torso with a horned crimson horse-helm and a fiery mane, a great crossbow on its arm and a
golden halo of light behind; a long pale-blue tail. Looks: "base"; "x" (X-Antibody: sharper crimson-and-black plate
with cyan crystal edges and a great crystal bow of cyan blades); "burst" (Burst Mode: radiant silver-white armour,
golden crystal wings). Shiny: blue / gold.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, quadruped
from _digibody import humanoid
from _digidetail import armour, gem, metal, solid, strands
from _dorbickmon import mount
from _route import pal, tone


def make(name, look="base"):
    base = {"red": (190, 30, 40) if look != "burst" else (236, 238, 246),
            "red_dark": (100, 10, 16) if look != "burst" else (160, 164, 186), "silver": (210, 214, 226),
            "silver_dark": (110, 114, 130), "blue": (60, 110, 200), "gold": (236, 196, 70), "gold_dark": (150, 110, 20),
            "black": (30, 28, 34), "cyan": (110, 230, 240), "tail": (190, 220, 246), "halo": (255, 220, 120, 160),
            "eye": (90, 220, 250), "flame": (250, 140, 60)}
    shiny = {"red": (40, 70, 180), "red_dark": (14, 24, 100)} if look != "burst" else {"gold": (210, 214, 226)}

    def P(v):
        return pal(base, shiny, v)

    PLATE = armour(P, "red", "red_dark", trim="gold" if look != "x" else "cyan", trim_w=0.25)
    GOLD = metal(P, "gold", dark="gold_dark")

    def shieldf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        r = math.hypot(z, y - 18.0)
        a = math.atan2(y - 18.0, z)
        if face in ("east", "west") and abs(((r - a * 0.9) % 3.0) - 1.5) < 0.5:
            return tone(p["blue"], face), None
        return metal(P, "silver", dark="silver_dark")(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": PLATE, "head": PLATE, "paw": GOLD, "claw": GOLD, "belly": solid(P, "black")}
        a = quadruped(m, mats, name, length=32.0, body_y=20.0, body_rx=7.0, body_ry=6.4, neck=((0, 24, -16),
                      (0, 26, -17)), head_len=5.0, head_w=3.0, head_h=3.0, claws=False,
                      tail=((0, 22, 16), (0, 18, 22), (0, 12, 26)), tail_r=(2.0, 2.4, 2.0))
        m.boxes[:] = [b for b in m.boxes if b.bone not in ("head", "jaw")]
        bd = a["body"]
        for sx in (-1, 1):                                                               # middle legs + swirl shields
            lg = m.bone("leg_mid_" + ("left" if sx > 0 else "right"), a["top"], (sx * 5.0, 16.0, 0))
            rod(m, lg, (sx * 5.0, 16.0, 0), (sx * 6.0, 2.0, 0), 3, PLATE, extend=0.4)
            m.round_box(lg, sx * 6.0, 0, 2.2, 2.2, 0.0, 2.0, GOLD, cut=0)
            m.box(bd, min(sx * 7.0, sx * 7.8), 14.0, -6.0, max(sx * 7.0, sx * 7.8), 22.0, 6.0, shieldf)
        for j in range(4):
            spike(m, "tail", (0, 12.0, 26.0), ((j - 1.5) * 0.3, -0.6, 1), 1.6, 8.0, strands(P, "tail", "silver_dark"),
                  tip=0.8)
        i_box, i_bone = len(m.boxes), len(m.bones)
        r = humanoid(m, {"skin": PLATE, "hand": GOLD, "finger": GOLD}, bulk=0.9, arm_bulk=0.9, leg_bulk=0.6, name="rider")
        m.boxes[:] = m.boxes[:i_box] + [b for b in m.boxes[i_box:] if b.bone not in ("leg_left", "leg_right")]
        m.bones[:] = m.bones[:i_bone] + [b for b in m.bones[i_bone:] if b["name"] not in ("leg_left", "leg_right")]
        rb = r["body"]
        hh = m.bone("head", rb, (0, 55, 0))
        m.round_box(hh, 0, -1.6, 2.6, 4.0, 54.0, 60.0, PLATE, cut=1)                      # horse-helm
        m.box(hh, -1.8, 57.4, -4.7, 1.8, 58.2, -4.5, solid(P, "eye", glow=True))
        for sx in (-1, 1):
            spike(m, hh, (sx * 2.0, 60.0, -1.0), (sx * 0.4, 1, 0.5), 1.4, 7.0, GOLD, tip=0.8)
        for j in range(6):                                                               # fiery mane
            spike(m, hh, (0, 60.0, -1.0 + j), (0, 0.6, 1), 1.2, 6.0, strands(P, "flame", "red_dark"), tip=0.8)
        w = r["arm_left"]["wrist"]
        ab = r["arm_left"]["bone"]
        if look == "x":                                                                  # crystal bow of cyan blades
            for j in range(7):
                ang = math.radians(-90 + j * 30)
                c = (w[0] + 3.0, w[1] + 14.0 * math.sin(ang), w[2] - 4.0 - 4.0 * math.cos(ang))
                spike(m, ab, c, (0.4, math.sin(ang) * 0.5, -1), 1.2, 4.0, gem(P, "cyan", "silver"), tip=0.8)
        else:                                                                            # crossbow
            m.box(ab, w[0] - 0.6, w[1] - 1.0, w[2] - 12.0, w[0] + 0.6, w[1] + 1.0, w[2] + 2.0, GOLD)
            m.box(ab, w[0] - 8.0, w[1] - 0.5, w[2] - 10.0, w[0] + 8.0, w[1] + 0.5, w[2] - 8.0, GOLD)
        hb = m.bone("halo", rb, (0, 50, 6))                                              # halo / wings of light
        if look == "burst":
            for sx in (-1, 1):
                for j in range(4):
                    ang = math.radians(10 + j * 22)
                    spike(m, hb, (sx * 3.0, 50.0, 6.0), (sx * math.cos(ang), math.sin(ang), 0.4), 2.4, 20.0 - j * 2.0,
                          gem(P, "gold", "silver"), tip=0.8)
        else:
            for i in range(16):
                ang = 2 * math.pi * i / 16
                m.box(hb, 12.0 * math.cos(ang) - 1.0, 50.0 + 12.0 * math.sin(ang) - 1.0, 6.0, 12.0 * math.cos(ang) + 1.0,
                      50.0 + 12.0 * math.sin(ang) + 1.0, 6.6, solid(P, "halo", glow=True))
        mount(m, i_box, i_bone, -4.0, -14.0, bd)
        return m

    return build
