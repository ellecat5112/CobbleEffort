"""Shared builder for Fenriloogamon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): the
god-wolf of Digimon Ghost Game. A huge prowling wolf in silver-and-navy plate armour edged with sky-blue, a long
armoured muzzle with red eyes, a great mane and tail of blazing blue spirit-fire streaming back, a thick knotted rope
round its neck, and heavy armoured paws with black hooked claws. make(take=True): Fenriloogamon: Takemikazuchi,
the same wolf wreathed in green lightning, carrying a long green-bladed sword in its jaws, with four silver thruster
pods on its back trailing blue flame. Shiny: crimson fire on black plate.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _digidetail import armour, cutout, flame_inside, local, metal, solid, twisted
from _route import pal, tone

BASE = {"silver": (210, 214, 230), "silver_dark": (110, 114, 132), "silver_light": (255, 255, 255),
        "navy": (40, 54, 110), "navy_dark": (14, 20, 50), "navy_light": (100, 120, 190), "sky": (110, 200, 250),
        "fire": (90, 170, 255, 210), "fire_core": (220, 240, 255, 235), "claw": (30, 30, 40), "rope": (170, 140, 90),
        "rope_dark": (100, 76, 40), "eye": (250, 50, 50), "mouth": (110, 20, 40), "tooth": (250, 250, 246),
        "green": (150, 250, 90, 220), "green_core": (240, 255, 220, 240), "blade": (190, 250, 140, 220)}
SHINY = {"navy": (30, 30, 36), "navy_dark": (8, 8, 12), "navy_light": (90, 90, 110), "sky": (250, 90, 70),
         "fire": (255, 90, 60, 210), "fire_core": (255, 220, 200, 235)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "silver", "silver_dark", light="silver_light", trim="sky", trim_w=0.3)
NAVY = armour(P, "navy", "navy_dark", light="navy_light", trim="sky", trim_w=0.3)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def boltf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return p["green"], p["green"][:3]


def flame(m, bone, at, w, h, seed, lean=0.0, tilt=-50):
    """A tongue of spirit-fire streaming back (crossed planes leaning toward +z)."""
    for ang in (0, 90):
        m.box(bone, at[0] - w / 2, at[1], at[2], at[0] + w / 2, at[1] + h, at[2],
              cutout(flame_inside(4, lean, seed), firef), rotation=(tilt, ang, 0), pivot=at)


def make(name, take=False):
    def build():
        m = Model(name)
        mats = {"skin": NAVY, "belly": PLATE, "neck": PLATE, "head": PLATE, "snout": PLATE, "jaw": PLATE,
                "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": NAVY, "leg_lower": PLATE,
                "paw": PLATE, "claw": solid(P, "claw"), "tail": NAVY}
        a = quadruped(m, mats, name, length=40.0, body_y=16.0, body_rx=7.4, body_ry=7.0, chest_bulk=1.4,
                      neck=((0, 20, -19), (0, 22, -25)), head_len=12.0, head_w=4.0, head_h=4.4, snout=0.8,
                      mouth_open=14, teeth=5, leg_bulk=1.9, toes=4,
                      tail=((0, 20, 21), (0, 24, 28), (0, 26, 34)), tail_r=(3.0, 2.4, 1.8))
        bd, hd = a["body"], a["head"]
        ex, ey, ez = a["eye"]
        for sx in (-1, 1):
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.3,
                  ez + 0.8, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 2.6, ey + 1.6, ez + 3.0), (sx * 0.3, 1, 0.7), 1.6, 5.0, PLATE, tip=0.5)     # ears
            for j in range(3):                                                      # shoulder plates
                spike(m, bd, (sx * 7.0, 22.0, -12.0 + j * 4.0), (sx * 0.8, 0.6, 0.4), 2.0, 4.0, PLATE, tip=0.4)
        for i in range(10):                                                         # blazing blue spirit mane
            t = i / 9
            flame(m, bd, ((i % 3 - 1) * 2.4, 22.0 + 2.0 * (1 - t), -16.0 + 24.0 * t), 5.0, 10.0 - 3.0 * t, i,
                  lean=0.2 * ((i % 2) * 2 - 1))
        e = a["tail_pts"][-1]
        for j in range(3):                                                          # flaming tail
            flame(m, a["tail"], (e[0] + (j - 1) * 2.0, e[1] - 1.0, e[2]), 5.0, 12.0, 20 + j, tilt=-70)
        for j in range(8):                                                          # knotted rope round the neck
            ang = 2 * math.pi * j / 8
            m.round_box(a["neck"], 4.6 * math.cos(ang), -21.0 + 4.0 * math.sin(ang), 1.2, 1.2, 20.4, 22.0,
                        twisted(P, "rope", "rope_dark"), cut=0)
        rod(m, a["neck"], (0, 20.0, -24.0), (2.0, 14.0, -26.0), 1, twisted(P, "rope", "rope_dark"), extend=0.3)
        if take:
            for sx in (-1, 1):                                                      # silver thruster pods
                for j in range(2):
                    base = (sx * 4.0, 24.0, -2.0 + j * 9.0)
                    rod(m, bd, base, (sx * 7.0, 34.0, 4.0 + j * 9.0), 4, metal(P, "silver", dark="silver_dark"),
                        extend=0.5)
                    flame(m, bd, (sx * 7.0, 34.0, 4.0 + j * 9.0), 4.0, 9.0, 40 + j, tilt=-30)
            sw = m.bone("sword", hd, (0, a["mouth_y"], a["snout_front"] + 4.0))     # green-bladed sword in its jaws
            y, z = a["mouth_y"], a["snout_front"] + 4.0
            rod(m, sw, (-14.0, y, z), (14.0, y + 6.0, z), 1, solid(P, "blade", glow=True), extend=0, t2=3)
            m.round_box(sw, 10.0, z, 1.4, 1.4, y + 4.0, y + 6.0, metal(P, "silver", dark="silver_dark"), cut=0)
            for j in range(6):                                                      # green lightning
                rod(m, sw, (-12.0 + j * 4.0, y + 2.0 + (j % 2) * 4.0, z), (-8.0 + j * 4.0, y + 2.0 + ((j + 1) % 2) * 4.0,
                    z), 1, boltf, extend=0.2)
        return m
    return build
