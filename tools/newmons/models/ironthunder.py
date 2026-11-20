"""Iron Thunder (Electric/Steel), the future paradox Raikou, built from boxes after the art the user shared (artist not
named, no name given; our name).

A robot Raikou on four lean armoured legs: yellow plates over a grey mechanical frame, glowing cyan chevrons on its
legs, a pale collar round its neck and a black helmet of a head with three cyan gems on its brow, a red pixel visor,
white jaw plates and two long yellow fangs. Where Raikou wears its storm cloud it carries five great purple missile
pods, banded with glowing cyan rings, that spit jagged cyan lightning from their ends.

Shiny: navy plates and gold lightning.

Front is -z, y is up. 38 units tall (to the top pod); about 2.3 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _pgen1 import CLEAR, stars, tri
from _regi import ellipsoid
from _rotomform import bolt_shape
from _route import pal, tone

HEIGHT = 38
SCALE = round(2.3 * 16 / HEIGHT, 3)
HITBOX = [2.4, HEIGHT / 16]
KIND = "quadruped"
K = 3
LOOK = ("a robot Raikou with yellow armour over a grey frame, glowing cyan leg chevrons, a black gem-browed helmet with "
        "a red visor and yellow fangs, and five purple missile pods spitting cyan lightning")

BASE = {"yellow": (240, 208, 64), "yellow_dark": (196, 160, 40), "olive": (176, 150, 60), "grey": (140, 140, 152),
        "grey_dark": (92, 92, 104), "pale": (222, 224, 232), "black": (32, 32, 38), "cyan": (110, 226, 236),
        "cyan_light": (214, 252, 255), "pod": (118, 60, 86), "pod_light": (156, 96, 122), "pod_dark": (84, 38, 60),
        "red": (220, 40, 50), "fang": (240, 196, 70), "claw": (234, 234, 240)}
SHINY = {"yellow": (70, 96, 176), "yellow_dark": (48, 66, 130), "olive": (56, 72, 130), "cyan": (255, 210, 80),
         "cyan_light": (255, 244, 200), "pod": (70, 70, 84), "pod_light": (104, 104, 120), "pod_dark": (44, 44, 54)}


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def armourf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and abs((z % 7.0) - 3.5) < 0.25:
        return tone(p["yellow_dark"], face), None
    return tone(p["yellow"], face), None


def bellyf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["grey_dark"] if (z % 1.6) < 0.5 else p["grey"], face), None


def legf(x, y, z, face, variant, **k):
    """Yellow armour with a glowing cyan chevron on the outer face."""
    p = P(variant)
    if face in ("east", "west"):
        u = (z % 6.0) - 3.0
        v = y % 6.0
        if abs(v - (3.0 - abs(u) * 0.7)) < 0.5 and abs(u) < 2.0:
            return p["cyan"], p["cyan"]
    return tone(p["yellow"], face), None


def headf(eye_y, eye_z):
    """A black helmet with a red pixel visor across the eyes."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("east", "west", "north") and abs(y - eye_y) < 0.7 and (face != "north" or abs(x) > 0.8):
            if ((y * 3) % 1.0 < 0.5) ^ (((z if face != "north" else x) * 3) % 1.0 < 0.5):
                return p["red"], p["red"]
            return (60, 10, 14), None
        return tone(p["black"], face), None
    return s


def podf(x, y, z, face, variant, box=None, **k):
    """A purple missile pod banded with glowing cyan rings (rods: z runs back from the pod's base)."""
    p = P(variant)
    d = box.lo[2] + box.size[2] - z
    if (d % 7.0) > 6.3:
        return p["cyan"], p["cyan"]
    if face == "up":
        return p["pod_light"], None
    return tone(p["pod"] if face != "down" else p["pod_dark"], face), None


def boltf(w, h, x0, y0, z0):
    """A jagged cyan lightning exhaust on a zy plane (seen from the side), streaming back along +z."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u, v = (z - z0) / w, (y - y0) / h
        if not (0 <= u <= 1 and 0 <= v <= 1) or not bolt_shape(v, u):
            return CLEAR
        c = p["cyan_light"] if stars(x, y, z, face, cell=1.4, r=0.3, prob=0.3) else p["cyan"]
        return c, c
    return s


def build() -> Model:
    m = Model("ironthunder")
    neck = ((0, 23.0, -13.5), (0, 25.0, -17.0))
    head_len, head_w, head_h = 9.0, 3.6, 4.4
    hx, hy, hz = neck[-1]
    eye_y = hy + head_h * 0.25
    mats = {"skin": armourf, "belly": bellyf, "neck": solid("pale"), "head": headf(eye_y, hz - head_len * 0.35),
            "snout": solid("pale"), "jaw": solid("pale"), "mouth": solid("black"), "tooth": solid("fang"),
            "tongue": solid("grey_dark"), "leg_upper": legf, "leg_lower": legf, "paw": solid("grey"),
            "claw": solid("claw"), "tail": solid("grey")}
    a = quadruped(m, mats, "ironthunder", length=28.0, body_y=17.0, body_rx=5.2, body_ry=5.0, chest_bulk=1.1,
                  neck=neck, head_len=head_len, head_w=head_w, head_h=head_h, snout=0.55, mouth_open=6, teeth=0,
                  leg_bulk=1.0, tail=((0, 19.0, 15.0), (0, 18.0, 18.0)), tail_r=(1.6, 1.0), toes=3)
    bd, hd = a["body"], a["head"]
    for sx in (-1, 1):                                                              # grey hip/shoulder joints
        for zz in (-9.6, 9.6):
            x0, x1 = sorted((sx * 5.0, sx * 6.2))
            m.box(bd, x0, 14.6, zz - 1.8, x1, 18.2, zz + 1.8, solid("grey"))
    for i, (yy, rr) in enumerate(((21.0, 4.6), (22.6, 4.2))):                       # the pale collar
        m.round_box(bd, 0, -11.2 - i * 1.2, rr, 3.0, yy - 1.2, yy + 1.2, solid("pale"), cut=1)
    # the helmet: a black brow crest, three cyan gems, white cheek plates and long yellow fangs
    top = a["skull_top"]
    spike(m, hd, (0, top - 0.4, hz - 2.0), (0, 0.8, 1), 2.2, 6.0, solid("black"), tip=0.9)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.6, top - 0.6, hz - 1.0), (sx * 0.5, 0.7, 1), 1.6, 4.0, solid("black"), tip=0.7)
        x0, x1 = sorted((sx * 2.8, sx * 4.4))
        m.box(hd, x0, hy - 2.0, hz - 4.6, x1, hy + 1.4, hz + 0.8, solid("pale"))           # cheek plates
        spike(m, hd, (sx * 1.6, a["mouth_y"] - 0.4, a["snout_front"] + 2.0), (sx * 0.1, -1, -0.15), 1.0, 4.4,
              solid("fang"), tip=0.4)                                                     # long fangs
    for gx, gy in ((-1.2, 0.0), (1.2, 0.0), (0.0, 0.9)):
        ellipsoid(m, hd, gx, top + gy - 0.6, hz - 3.4, 0.7, 0.7, 0.5, solid("cyan", True), step=1)
    # five purple missile pods fanned over its back, spitting cyan lightning
    pods = m.bone("cap", bd, (0, 22.0, -6.0))
    for x, y0, z0, rise, length, w in ((0.0, 23.5, -7.0, 0.42, 26.0, 5.0), (3.6, 22.4, -5.0, 0.30, 24.0, 4.6),
                                       (-3.6, 22.4, -5.0, 0.30, 24.0, 4.6), (6.4, 20.6, -2.0, 0.16, 20.0, 4.2),
                                       (-6.4, 20.6, -2.0, 0.16, 20.0, 4.2)):
        d = (x * 0.05, rise, 1.0)
        n = math.sqrt(sum(v * v for v in d))
        u = tuple(v / n for v in d)
        a0 = (x, y0, z0)
        b0 = tuple(p + q * length for p, q in zip(a0, u))
        rod(m, pods, a0, b0, w, podf, extend=0.2, t2=w * 0.72)
        rod(m, pods, a0, b0, w * 0.72, podf, extend=0.0, t2=w)
        tip = tuple(p + q * 2.0 for p, q in zip(b0, u))
        rod(m, pods, b0, tip, w * 0.5, solid("cyan_light", True), extend=0.2)
        bw, bh = 14.0, 8.0
        m.box(pods, x, tip[1] - bh / 2, tip[2], x, tip[1] + bh / 2, tip[2] + bw, boltf(bw, bh, x, tip[1] - bh / 2,
                                                                                        tip[2]))
    return m
