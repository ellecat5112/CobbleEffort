"""Shared parts for the CobbleEffortian Slugma and Petroil (after @Kai_FakemonsR's art): slugs of oily sludge with
a rainbow sheen burning along their edges (it glows), drippy wavy caps, puddle bases, and Petroil's entourage of
Trubbish riding in its barrel. `trubbish(m, bone, c, s, face_dir)` builds a little Trubbish at any scale."""
from __future__ import annotations

import colorsys
import math

from _afake import ramp_of, solid_of
from _boxmodel import spike
from _route import pal, tone

BASE = {"teal": (132, 206, 214), "teal_dark": (88, 160, 176), "lime": (196, 220, 120), "lime_dark": (158, 186, 92),
        "tar": (54, 58, 50), "tar_dark": (34, 38, 32), "tar_light": (84, 90, 76), "puddle": (232, 222, 70),
        "barrel": (108, 106, 74), "barrel_dark": (78, 76, 54), "hoop": (60, 60, 46), "eye_white": (250, 248, 240),
        "pupil": (40, 30, 40), "bag": (92, 106, 84), "bag_dark": (66, 78, 62), "bag_light": (124, 138, 112),
        "trash": (190, 110, 150), "fang": (250, 250, 250), "sheen_shift": (0, 0, 0)}
SHINY = {"teal": (176, 140, 220), "teal_dark": (132, 100, 186), "lime": (240, 200, 90), "lime_dark": (206, 166, 60),
         "tar": (40, 46, 70), "tar_dark": (24, 28, 48), "tar_light": (66, 74, 104), "puddle": (120, 220, 240),
         "sheen_shift": (128, 0, 0)}


def palette():
    def P(v):
        return pal(BASE, SHINY, v)
    return P, solid_of(P), ramp_of(P)


P, solid, ramp = palette()


def sheen(p, t):
    """The burning oil-slick rainbow at position t (0..1 round the edge): it glows."""
    h = (t + p["sheen_shift"][0] / 255.0) % 1.0
    r, g, b = colorsys.hsv_to_rgb(h, 0.75, 1.0)
    c = (int(r * 255), int(g * 255), int(b * 255))
    return c, c


def angle_t(x, z, cx=0.0, cz=0.0):
    return (math.atan2(z - cz, x - cx) / (2 * math.pi)) % 1.0


def trubbish(m, bone, c, s, face_z=-1):
    """A little Trubbish (a knotted rubbish bag with an angry face, stitched patches and stubby arms) at scale s,
    its bottom centre at c, facing -z (face_z = -1) or +z."""
    cx, cy, cz = c

    def body(x, y, z, face, variant, **k):
        p = P(variant)
        front = "north" if face_z < 0 else "south"
        u, v = (x - cx) / s, (y - cy) / s
        if face == front:
            for sx in (-1, 1):
                d = math.hypot(u - sx * 1.25, v - 3.1)
                if d < 0.75:
                    return (p["pupil"] if d < 0.32 else p["eye_white"]), None
                if abs(v - 3.85 - (u * sx - 1.25) * 0.35) < 0.22 and 0.5 < u * sx < 2.1:
                    return p["pupil"], None                              # angry brows
            if 1.3 < v < 2.1 and abs(u) < 1.5:
                if v > 1.75 and int((u + 2) * 2.2) % 2 == 0:
                    return p["fang"], None                               # jagged teeth
                return p["pupil"], None
        if abs((u + v * 0.4) % 2.6 - 1.3) < 0.12 and face != front:
            return tone(p["bag_dark"], face), None                       # creases
        return tone(p["bag"] if v > 0.8 else p["bag_dark"], face), None

    m.round_box(bone, cx, cz, 2.6 * s, 2.3 * s, cy, cy + 5.0 * s, body, cut=max(0.5, round(0.9 * s, 1)))
    for sx in (-1, 1):                                                   # the knot's two "ears"
        spike(m, bone, (cx + sx * 0.9 * s, cy + 4.8 * s, cz), (sx * 0.5, 1, 0), max(1.0, 1.0 * s), 2.4 * s,
              solid("bag_light"), tip=max(0.6, 0.5 * s))
        spike(m, bone, (cx + sx * 2.4 * s, cy + 2.0 * s, cz + face_z * 0.4 * s), (sx, -0.2, face_z * 0.4),
              max(1.0, 0.9 * s), 1.6 * s, solid("bag"), tip=None)             # stubby arms
        m.box(bone, cx + sx * 3.4 * s - 0.5, cy + 1.6 * s - 0.5, cz + face_z * 1.0 * s - 0.5,
              cx + sx * 3.4 * s + 0.5, cy + 1.6 * s + 0.5, cz + face_z * 1.0 * s + 0.5, solid("trash"))   # bits of trash
