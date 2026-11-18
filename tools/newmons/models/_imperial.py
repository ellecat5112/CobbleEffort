"""Shared builder for the Imperialdramon modes (CobbleEffort: Digital; hand-built at the detail standard after the
official art on wikimon.net): the ancient emperor dragon. Dragon Mode: a great four-legged dragon in black armour with
gold trim and gold talons on every foot, a white dragon helm with a blue face and gold crest, red-and-orange dragon
wings, a Positron Laser cannon on its back and a blue tail. Fighter Mode: the same armour standing upright, the
cannon on its right arm, a red chest gem, gold knee spikes and wings spread behind. Paladin Mode: white-and-silver
holy knight armour with gold trim, white wings, a red cape and the long Omega Blade. Black: darker armour, a silver
helm, red eyes and crimson wings.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import bat_wing, quadruped
from _digibody import cape, humanoid
from _digidetail import armour, cutout, fabric, gem, local, metal, noise2, scales, skin, solid
from _route import pal, tone


def make(name, mode="dragon", black=False):
    paladin = mode == "paladin"
    base = {"armour": (40, 40, 50), "armour_dark": (12, 12, 18), "armour_light": (110, 110, 130),
            "gold": (240, 200, 70), "gold_dark": (160, 120, 20), "gold_light": (255, 240, 170),
            "helm": (240, 240, 246), "helm_dark": (170, 172, 190), "face": (60, 110, 210), "face_dark": (24, 50, 130),
            "wing": (220, 50, 30), "wing_dark": (240, 150, 40), "red": (220, 40, 40), "red_light": (255, 160, 140),
            "eye": (250, 220, 60), "steel": (200, 204, 216), "steel_dark": (90, 94, 106), "blade": (230, 236, 246)}
    if paladin:
        base.update({"armour": (236, 238, 246), "armour_dark": (150, 156, 180), "armour_light": (255, 255, 255),
                     "wing": (246, 246, 252), "wing_dark": (190, 196, 220)})
    if black:
        base.update({"armour": (30, 30, 36), "armour_dark": (6, 6, 10), "armour_light": (90, 90, 100),
                     "helm": (170, 172, 184), "helm_dark": (90, 92, 104), "face": (40, 40, 60),
                     "wing": (150, 20, 30), "wing_dark": (60, 6, 14), "eye": (240, 40, 40)})
    shiny = {"armour": (40, 60, 120), "armour_dark": (14, 24, 60), "armour_light": (110, 140, 220)} if not paladin else \
        {"armour": (250, 236, 200), "armour_dark": (190, 160, 110), "wing": (250, 240, 210)}

    def P(v):
        return pal(base, shiny, v)

    ARM = armour(P, "armour", "armour_dark", light="armour_light", trim="gold", trim_w=0.3, rivets=True)
    GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
    HELM = armour(P, "helm", "helm_dark", trim="gold", trim_w=0.25)
    FACE = skin(P, "face", dark="face_dark")

    def tatter(x, y, z, face, box):
        if not black:
            return True
        u, v, W, H = local(x, y, z, face, box)
        return v / max(H, 1e-6) > 0.12 * abs(math.sin(u * 0.8)) + 0.06 * noise2(u, 0.0, 9)

    def wingf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        return tone(p["wing_dark"] if v / max(H, 1e-6) < 0.4 else p["wing"], face), None

    def helm(m, hd, c, s=1.0):
        x, y, z = c
        m.round_box(hd, x, z, 2.8 * s, 3.2 * s, y - 3.0 * s, y + 3.4 * s, HELM, cut=1)
        m.round_box(hd, x, z - 3.4 * s, 1.8 * s, 1.8 * s, y - 2.6 * s, y + 0.4 * s, FACE, cut=1)       # blue snout
        for sx in (-1, 1):
            m.box(hd, min(x + sx * 0.8 * s, x + sx * 2.2 * s), y + 0.8 * s, z - 3.4 * s, max(x + sx * 0.8 * s,
                  x + sx * 2.2 * s), y + 1.6 * s, z - 3.1 * s, solid(P, "eye", glow=True))
            spike(m, hd, (x + sx * 2.4 * s, y + 2.4 * s, z), (sx * 0.6, 0.8, 0.6), 1.2, 5.0 * s, GOLD, tip=0.8)
        spike(m, hd, (x, y + 3.2 * s, z - 1.4 * s), (0, 1, -0.3), 1.6, 5.0 * s, GOLD, tip=0.8)        # gold crest

    def cannon(m, bone, a, b, r):
        rod(m, bone, a, b, r, ARM, extend=0.6)
        d = [b[i] - a[i] for i in range(3)]
        n = math.sqrt(sum(t * t for t in d)) or 1.0
        tip = tuple(b[i] + d[i] / n * 3.0 for i in range(3))
        rod(m, bone, b, tip, max(1, r - 1), GOLD, extend=0)

    def build():
        m = Model(name)
        if mode == "dragon":
            mats = {"skin": ARM, "belly": GOLD, "neck": ARM, "head": HELM, "snout": FACE, "jaw": FACE,
                    "mouth": solid(P, "red"), "tooth": solid(P, "helm"), "leg_upper": ARM, "leg_lower": ARM,
                    "paw": GOLD, "claw": GOLD, "tail": skin(P, "face", dark="face_dark")}
            a = quadruped(m, mats, name, length=34.0, body_y=16.0, body_rx=7.0, body_ry=6.6, chest_bulk=1.3,
                          neck=((0, 22, -15), (0, 25, -21)), head_len=10.0, head_w=3.6, head_h=4.0, snout=0.7,
                          mouth_open=14, teeth=5, leg_bulk=1.5, toes=4,
                          tail=((0, 18, 17), (0, 16, 24), (0, 12, 30)), tail_r=(2.6, 2.0, 1.2))
            bd, hd = a["body"], a["head"]
            ex, ey, ez = a["eye"]
            for sx in (-1, 1):
                m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.4,
                      ez + 0.8, solid(P, "eye", glow=True))
                spike(m, hd, (sx * 2.0, ey + 2.0, ez + 1.0), (sx * 0.4, 0.8, 0.8), 1.4, 6.0, GOLD, tip=0.8)
            for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
                w = a[nm]["wrist"]
                for j in range(4):                                                  # long gold talons
                    spike(m, a[nm]["bone"], (w[0] + (j - 1.5) * 1.2, 1.2, w[2] - 2.0), (0, -0.2, -1), 1.0, 6.0, GOLD,
                          tip=0.8)
            cannon(m, bd, (5.0, 24.0, 4.0), (7.0, 28.0, -10.0), 3)                  # Positron Laser on the back
            for side in (1, -1):
                wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 23.0, 0.0))
                bat_wing(m, wb, (side * 4.0, 23.0, 0.0), 26.0, 18.0, 4, ARM, cutout(tatter, wingf), side=side, sweep=30)
            for i in range(7):
                spike(m, bd, (0, 23.0, -10.0 + i * 3.6), (0, 1, 0.6), 1.4, 3.0, GOLD, tip=0.8)
            return m
        mats = {"skin": ARM, "chest": ARM, "abs": ARM, "pelvis": ARM, "neck": ARM, "deltoid": ARM,
                "upper_arm": ARM, "forearm": ARM, "hand": ARM, "finger": GOLD, "thigh": ARM, "knee": GOLD,
                "shin": ARM, "calf": ARM, "foot": GOLD, "toe": GOLD}
        a = humanoid(m, mats, bulk=1.3, arm_bulk=1.2, leg_bulk=1.25, digitigrade=True, talons=True, name=name)
        bd = a["body"]
        m.round_box(bd, 0, -4.6, 2.2, 0.6, 44.0, 48.0, gem(P, "red", "red_light"), cut=0)          # chest gem
        for sx in (-1, 1):                                                      # shoulder spikes
            m.round_box(bd, sx * 8.6, 0.0, 3.6, 3.6, 47.0, 53.0, ARM, cut=2)
            spike(m, bd, (sx * 9.6, 52.0, 0), (sx * 0.6, 1, 0), 1.6, 6.0, GOLD, tip=0.8)
        hd = m.bone("head", bd, (0, 55, 0))
        helm(m, hd, (0, 57.4, -0.4), 1.0)
        for nm in ("leg_left", "leg_right"):
            kn = a[nm]["knee"]
            sx = 1 if kn[0] > 0 else -1
            spike(m, a[nm]["bone"], kn, (sx * 0.2, 0.4, -1), 1.4, 4.0, GOLD, tip=0.8)
            ank = a[nm]["ankle"]
            for j in range(3):
                spike(m, a[nm]["bone"], (ank[0] + (j - 1) * 1.4, 1.0, ank[2] - 2.0), (0, -0.2, -1), 1.2, 6.0, GOLD,
                      tip=0.8)
        rod(m, bd, (0, 32.0, 3.0), (0, 22.0, 12.0), 2, skin(P, "face", dark="face_dark"), extend=0.4, t2=1)  # tail
        hr = a["arm_right"]
        hx, hy, hz = hr["hand"]
        if paladin:                                                              # Omega Blade + red cape
            hl = a["arm_left"]
            lx, ly, lz = hl["hand"]
            m.round_box(hl["bone"], lx, lz, 0.8, 0.8, ly - 2.0, ly + 2.0, GOLD, cut=0)
            m.round_box(hl["bone"], lx, lz - 1.0, 1.4, 0.5, ly + 2.4, ly + 34.0, metal(P, "blade", dark="steel_dark"),
                        cut=0)
            spike(m, hl["bone"], (lx, ly + 34.0, lz - 1.0), (0, 1, 0), 2.6, 4.0, metal(P, "blade", dark="steel_dark"),
                  tip=0.8)
            m.round_box(hl["bone"], lx, lz, 3.0, 0.8, ly + 1.4, ly + 2.4, GOLD, cut=0)
            cape(m, bd, 52.0, 12.0, 34.0, fabric(P, "red", "red"), z=4.0, flare=0.6, panels=6)
        else:                                                                    # Positron Laser on the right arm
            cannon(m, hr["bone"], (hx - 1.0, hy + 4.0, hz + 4.0), (hx - 1.0, hy - 1.0, hz - 10.0), 3)
        for side in (1, -1):
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 50.0, 4.0))
            bat_wing(m, wb, (side * 4.0, 50.0, 4.0), 28.0, 26.0, 4, ARM, cutout(tatter, wingf), side=side, sweep=20)
        return m

    return build
