"""Aristograd, the Mothership Pokémon (Water/Bug), after @victorious_trainer's Pokémon Victory art (name kept):
Tardigrub grown into a great round water bear, white on top and lavender below, with purple stripes round its rear,
a pink mouth ring in a black mask, little white nubs along its back, eight stubby white legs with black claws, and four
pods in its back where it keeps Tardigrubs: two of them peek out. It launches them at its foes like darts.

Shiny: mint and cream, with a gold mouth ring.

Front is -z, y is up. 22 units tall; baseScale 1.16 (1.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _tardi import face_ring, grub, palette
from _route import tone

SHINY = {"lav": (150, 220, 190), "lav_light": (246, 240, 214), "lav_dark": (92, 170, 140), "lav_deep": (54, 120, 96),
         "pink": (240, 196, 70), "pink_dark": (150, 110, 30)}
P, solid, ramp = palette(SHINY)
SCALE = 1.16
HITBOX = [1.6, 1.4]
KIND = "quadruped"
K = 3
HEIGHT = 22
LOOK = ("a great round white-and-lavender water bear with a pink mouth ring, eight stubby clawed legs and four pods in "
        "its back with Tardigrubs peeking out")
C = (0.0, 12.0, 0.6)                                                # the ball's centre
R = 9.4


def _n(v):
    n = math.sqrt(sum(a * a for a in v))
    return tuple(a / n for a in v)


PODS = [_n((0.55, 0.72, 0.25)), _n((-0.55, 0.72, 0.25)), _n((0.62, 0.22, 0.62)), _n((-0.62, 0.22, 0.62))]
RIDERS = (0, 3)                                                     # the pods with a Tardigrub in them


def ball(x, y, z, face, variant, **k):
    p = P(variant)
    d = _n((x - C[0], y - C[1], z - C[2]))
    for i, h in enumerate(PODS):
        a = math.acos(max(-1.0, min(1.0, sum(u * v for u, v in zip(d, h)))))
        if a < 0.36:
            return (p["hole"] if a < 0.24 else p["lav_deep"]), None   # a pod: dark inside, a deep purple rim
        if a < 0.42:
            return tone(p["lav_dark"], face), None
    ly = y - C[1]
    if z > 2.5 and -7 < ly < 1.5 and (ly + 7) % 2.6 < 0.9:
        return tone(p["lav_dark"], face), None                        # stripes round its rear
    for sx, sy, sz in ((3.2, -3.0, -1), (-3.2, -3.0, -1), (5.0, 1.0, -1)):
        if face == "north" and math.hypot(x - sx, ly - sy) < 1.2:
            return tone(p["lav_dark"], face), None                    # purple spots on its front
    if ly > 1.5 - 1.2 * d[2]:
        return tone(p["lav_light"], face), None                       # white on top
    if ly < -6.0:
        return tone(p["lav_dark"], face), None
    return tone(p["lav"], face), None


def head(x, y, z, face, variant, **k):
    p = P(variant)
    hy = C[1] + 4.4
    if face == "north":
        col = face_ring(p, x, y - hy, 1.3, ring="pink", inner="pink_dark", reach=2.2)
        if col is not None:
            return col, None
        if y < hy - 0.6 and abs(x) < 3.0:
            return p["mask"], None                                    # the black mask below it
    if face in ("east", "west") and math.hypot(y - hy, z - (C[2] - R + 1.8)) < 1.2:
        return p["lav_dark"], None
    return tone(p["lav_light"], face), None


def build() -> Model:
    m = Model("aristograd")
    top = m.bone("aristograd", None, (0, 0, 0))
    bd = m.bone("body", top, (0, C[1], 0))
    for i in range(-8, 9):                                             # the great ball, in slices
        y0, y1 = C[1] + i * 1.1 - 0.55, C[1] + i * 1.1 + 0.55
        r = math.sqrt(max(0.0, R * R - (i * 1.1) ** 2))
        if r < 1.5:
            continue
        m.round_box(bd, C[0], C[2], r, r, round(y0, 2), round(y1 + 0.05, 2), ball, cut=round(r * 0.3, 1))
    hd = m.bone("head", bd, (0, C[1] + 4, C[2] - R + 2))
    m.round_box(hd, 0, C[2] - R + 0.4, 3.2, 2.2, C[1] + 1.2, C[1] + 7.6, head, cut=1.0)
    for dx in (-2.4, 0.0, 2.4):                                        # white nubs along its back
        spike(m, bd, (dx, C[1] + R - 0.6, C[2] + 1.0), (dx * 0.1, 1, 0.3), 1.6, 2.2, solid("lav_light"), tip=0.8)
    for i, lz in enumerate((-5.0, -1.7, 1.7, 5.0)):                    # eight stubby legs with black claws
        for sx, side in ((1, "left"), (-1, "right")):
            lx = sx * 6.6
            lg = m.bone(f"leg_{i + 1}_{side}", top, (lx, 4.0, lz + C[2]))
            m.round_box(lg, lx, lz + C[2], 1.8, 1.8, 1.0, 5.0, solid("lav_light"), cut=0.6)
            for dz in (-0.9, 0.9):
                m.box(lg, lx - 0.5, 0, lz + C[2] + dz - 1.4, lx + 0.5, 1.0, lz + C[2] + dz - 0.4, solid("claw"))
    for n, i in enumerate(RIDERS):                                     # Tardigrubs peeking out of two pods
        h = PODS[i]
        hx, hy, hz = (C[j] + (R + 0.6) * h[j] for j in range(3))
        pod = m.bone(f"pod_{n + 1}", bd, (hx, hy, hz))
        grub(m, pod, (hx, hy - 2.6, hz - 0.6), 0.5, P, glossy=False)
    return m
