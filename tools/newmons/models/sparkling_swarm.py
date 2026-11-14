"""Sparkling's Swarm Form (Electric/Flying, battle only; the user's design): thousands of Sparklings flying as one
giant bird about 20 blocks tall. A black body and great ragged wings raised high, every edge notched with little birds
and the whole of it dotted with their glowing magenta eyes; yellow across the shoulders, neck and crest; a fanned tail,
dangling talons, white birds tumbling from its chest, and a vortex of stragglers circling round it.

Front is -z, y is up. 40 units tall; baseScale 8 (20 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _route import tone
from _starling import P, dotted, eye_on, solid

SCALE = 8.0
HITBOX = [3.0, 2.5]
KIND = "floater"
K = 2
HEIGHT = 40
LOOK = ("a giant bird made of thousands of Sparklings: ragged black wings raised high and dotted with glowing magenta "
        "eyes, a yellow neck and crest, white birds tumbling from its chest and a vortex of birds circling it")
CLEAR = ((0, 0, 0, 0), None)


def body(x, y, z, face, variant, **k):
    if z < -5.5 and y > 18.5:
        return tone(P(variant)["yellow"], face), None                 # the yellow neck and shoulders
    return dotted("black", 2.4, 0.42)(x, y, z, face, variant)


def head(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        e = eye_on(p, z + 13.2, y - 22.6, 1.4)
        if e:
            return e
    if y > 23.4 or z > -11.6:
        return tone(p["yellow"], face), None
    return tone(p["mask"], face), None


def wing(sx):
    """A great raised wing, drawn in its own plane (x out from the shoulder, y up): a band from the shoulder up and
    out, the leading edge ragged with little birds, the trailing edge notched, splitting into fingers at the tip."""
    dots = dotted("black", 2.6, 0.45, salt=sx)
    ax, ay = 0.62, 0.78                                                # the wing's axis, out and up

    def s(x, y, z, face, variant, **k):
        px, py = abs(x) - 4.0, y - 21.0
        t = px * ax + py * ay                                          # along the wing
        n = -px * ay + py * ax                                         # across it (+ = leading/upper edge)
        if t < -1 or t > 27:
            return CLEAR
        lead = 3.0 - 0.06 * t + 0.6 * abs((t * 0.8) % 2 - 1)
        trail = -(7.5 - 0.18 * t) + 1.6 * ((t * 0.45) % 1)
        if t > 19:                                                     # primary "fingers" at the tip
            trail += (t - 19) * 0.6
            if abs(((n + 30) * 0.45) % 1 - 0.5) < 0.18 and t > 21:
                return CLEAR
        if not (trail < n < lead):
            return CLEAR
        if t < 10 and n > lead - 4.0:
            return tone(P(variant)["yellow"], face), None              # yellow coverts
        return dots(x, y, z, face, variant)
    return s


def tail(x, y, z, face, variant, **k):
    t = (z - 9.0) / 13.0
    half = 2.5 + 5.0 * t
    lobe = abs(((x + 30) * 0.32) % 1 - 0.5)
    if abs(x) > half or t < 0 or t > 1.0 - 0.25 * lobe:
        return CLEAR
    return dotted("black", 2.4, 0.42, salt=7)(x, y, z, face, variant)


def little_bird(colour, eye=True):
    """A tiny bird seen from the front, wings up (a cut-out plane)."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        cx = box.lo[0] + box.size[0] / 2
        cy = box.lo[1] + box.size[1] / 2
        u, v = x - cx, y - cy
        w = box.size[0] / 2
        if abs(u) < w * 0.3 and abs(v) < w * 0.35:
            if eye and abs(u) < w * 0.12 and v > 0:
                return p["eye"], p["eye"]
            return p[colour], None
        if abs(u) < w and abs(v - abs(u) * 0.55 + w * 0.1) < w * 0.22:
            return p[colour], None                                     # the raised wings
        return CLEAR
    return s


def build() -> Model:
    m = Model("sparkling_swarm")
    top = m.bone("sparkling_swarm", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 19, 0))
    m.round_box(bd, 0, 1.0, 4.4, 9.0, 13.4, 15.2, body, cut=2.0)
    m.round_box(bd, 0, 1.0, 5.2, 10.2, 15.0, 22.6, body, cut=2.4)
    m.round_box(bd, 0, 0.6, 4.2, 8.4, 22.4, 24.4, body, cut=2.0)
    hd = m.bone("head", bd, (0, 22, -10))
    m.round_box(hd, 0, -12.6, 2.8, 3.0, 19.8, 25.6, head, cut=1.0)
    spike(m, hd, (0, 25.2, -11.4), (0, 1.0, 0.8), 2.4, 4.0, solid("yellow"), tip=1.0)      # the crest
    spike(m, hd, (0, 21.6, -15.4), (0, -0.2, -1), 1.8, 3.2, solid("beak"), tip=0.8)        # the beak
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        w = m.bone(nm, bd, (sx * 4.0, 22.0, 0))
        x0, x1 = sorted((sx * 3.0, sx * 26.0))
        m.box(w, x0, 13.0, 1.0, x1, 41.0, 1.0, wing(sx), rotation=(0, sx * 28, 0), pivot=(sx * 4.0, 22.0, 1.0))
    tl = m.bone("tail", bd, (0, 19, 9))
    m.box(tl, -8.0, 19.0, 9.0, 8.0, 19.0, 22.0, tail, rotation=(-10, 0, 0), pivot=(0, 19.0, 9.0))
    for sx in (-1, 1):                                                   # dangling talons
        rod(m, bd, (sx * 2.4, 14.0, 3.0), (sx * 2.8, 9.4, 5.4), 1.6, solid("black"))
        for dx in (-0.8, 0.0, 0.8):
            spike(m, bd, (sx * 2.8 + dx, 9.6, 5.4), (dx * 0.5, -1, 0.2), 0.8, 2.0, solid("black"))
    for i, (bx, by, bz, s) in enumerate(((-3.6, 10.6, -7.0, 3.0), (2.4, 8.4, -5.0, 2.6), (5.6, 11.2, -4.0, 2.2),
                                         (-1.0, 6.4, -3.0, 2.0))):     # white birds tumbling from its chest
        fb = m.bone(f"flock_{i + 1}", bd, (bx, by, bz))
        m.box(fb, bx - s, by - s * 0.6, bz, bx + s, by + s * 0.6, bz, little_bird("white", eye=False))
    ring = m.bone("ring_swarm", bd, (0, 20, 0))                         # a vortex of stragglers circling it
    for i in range(18):
        a = 2 * math.pi * i / 18
        r = 15.0 + 2.0 * math.sin(i * 1.7)
        cx, cy, cz = r * math.cos(a), 20 + r * math.sin(a), -4.0 + 8.0 * ((i * 0.37) % 1)
        m.box(ring, cx - 1.2, cy - 0.8, cz, cx + 1.2, cy + 0.8, cz, little_bird("black"))
    return m
