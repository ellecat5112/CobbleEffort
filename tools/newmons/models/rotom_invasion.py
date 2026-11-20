"""Invasion Rotom (Electric/Psychic), after Unknown-Dan's art (@unknown__dan; the art's own name; its "Cosmic" type is
Psychic here): Rotom inside an alien tripod walker. Its orange body has grown a tall pointed crest swept up like a
flame, an angry face with black goggle eyes and a toothy grin, black spots down its belly and a little tail; four
long silver tentacle legs arch up from it and stride down to three-pronged claw feet.

Front is -z, y is up. 36 units tall; about 1.8 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import smooth_path
from _rotomform import ball, grin, palette, solid
from _route import tone

P = palette({"aura": (120, 230, 220), "aura_light": (220, 255, 250), "silver": (184, 196, 222),
             "silver_dark": (118, 126, 150), "silver_light": (220, 226, 240)})
HEIGHT = 36
SCALE = round(1.8 * 16 / HEIGHT, 3)
HITBOX = [1.6, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("an angry orange Rotom with a tall flame-like crest, black goggle eyes and a toothy grin, riding four long "
        "arching silver tentacle legs with three-pronged claw feet")
CY = 24.0


def facef(x, y, z, face, variant, **k):
    """Angry black goggle eyes slanting down to the middle, white eyes with a dark pupil, a toothy grin, black
    spots on the lower body."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            u, v = x - sx * 1.7, y - (CY + 0.8)
            slant = v - 0.32 * (x * sx)                                     # inner corners lower: an angry frown
            if abs(u) < 1.45 and -0.95 < slant < 0.75:
                if math.hypot(u * 0.9, v + 0.05) < 0.55:
                    return (p["pupil"] if math.hypot(u, v) < 0.25 else p["white"]), p["white"]
                return p["black"], None
        g = grin(x, y - (CY - 1.6), 3.0, 1.2, p, 5)
        if g:
            return g, None
    if face in ("north", "east", "west") and y < CY - 2.6:
        a, b = (x, y) if face == "north" else (z, y)
        if math.hypot((a % 2.6) - 1.3, (b % 2.4) - 1.2) < 0.55:
            return p["black"], None
    return tone(p["orange"], face), None


def crestf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west", "north") and ((y * 0.8 + z * 0.4) % 2.0) < 0.5:
        return tone(p["orange_dark"], face), None
    return tone(p["orange"] if face != "up" else p["orange_light"], face), None


def legf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        return p["silver_light"], None
    if (z % 4.0) < 0.35:
        return tone(p["silver_dark"], face), None
    return tone(p["silver"], face), None


def leg(m, bone, root, out, peak, foot_r):
    """A tentacle leg: from the body out and up to an arch, then striding down to a claw foot on the ground."""
    ox, oz = out
    pts = smooth_path([root, (root[0] + ox * 0.35, root[1] + 3.0, root[2] + oz * 0.35),
                       (root[0] + ox * 0.65, peak, root[2] + oz * 0.65), (root[0] + ox * 0.9, peak - 6.0,
                                                                          root[2] + oz * 0.9),
                       (root[0] + ox * foot_r, 2.2, root[2] + oz * foot_r)], 14)
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        w = 1.4 - 0.5 * i / len(pts)
        rod(m, bone, a, b, max(1.0, round(w * 2) / 2), legf, extend=0.5)
    foot = pts[-1]
    d = math.hypot(ox, oz) or 1
    fx, fz = ox / d, oz / d
    for ang in (-50, 0, 50):                                                # three-pronged claw
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        dx, dz = fx * c - fz * s, fx * s + fz * c
        spike(m, bone, foot, (dx, -0.9, dz), 0.9, 2.6, solid(P, "silver_light"), tip=0.4)


def build() -> Model:
    m = Model("rotom_invasion")
    top = m.bone("rotom_invasion", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    ball(m, bd, 0, CY, 0, 4.3, facef, slices=4)                                     # the round orange body
    for i, (h, w, lean) in enumerate(((7.0, 3.2, 0.25), (5.0, 2.4, 0.45), (3.6, 1.8, 0.7))):   # the flame crest
        base = (0, CY + 2.6 + i * 0.6, 0.6 + i * 0.6)
        spike(m, bd, base, (0, 1, lean), w, h, crestf, tip=max(0.8, w * 0.35))
    for sx in (-1, 1):
        spike(m, bd, (sx * 1.6, CY + 3.0, -0.2), (sx * 0.6, 1, 0.3), 1.8, 3.6, crestf, tip=0.8)
    spike(m, bd, (0, CY - 3.4, 0.4), (0, -1, 0.5), 1.8, 3.0, solid(P, "orange"), tip=0.7)        # the little tail
    for nm, out, peak, r in (("leg_front_left", (12.0, -9.0), 33.0, 1.25), ("leg_front_right", (-12.0, -9.0), 33.0, 1.25),
                             ("leg_back_left", (11.0, 10.0), 31.0, 1.2), ("leg_back_right", (-11.0, 10.0), 31.0, 1.2)):
        lg = m.bone(nm, bd, (math.copysign(2.6, out[0]), CY - 0.6, math.copysign(1.6, out[1])))
        leg(m, lg, (math.copysign(2.6, out[0]), CY - 0.6, math.copysign(1.6, out[1])), out, peak, r)
    return m
