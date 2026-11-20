"""Serpent bodies for the Gen 3 paradox Rayquazas (Ancient Rogue, Iron Ascent): a tapering body along a smooth path,
each segment an octagonal-ish pair of crossed rods, with helpers to find points along it.
"""
from __future__ import annotations

import math

from _boxmodel import rod
from _pgen1 import smooth_path


def serpent(m, bones, ctrl, n, w0, w1, shader, split=None):
    """Rods along a Catmull-Rom path through ctrl (n segments), width tapering w0 -> w1. bones: one bone, or a list of
    (fraction, bone) pairs: a segment goes to the last bone whose fraction it has passed. Returns the path points."""
    pts = smooth_path(ctrl, n)
    if not isinstance(bones, list):
        bones = [(0.0, bones)]
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        f = i / max(1, len(pts) - 2)
        bone = [bn for fr, bn in bones if f >= fr][-1]
        w = max(1.0, round((w0 + (w1 - w0) * f) * 2) / 2)
        rod(m, bone, a, b, w, shader, extend=0.9)
        rod(m, bone, a, b, max(1.0, w * 0.72), shader, extend=0.7, t2=w * 1.18)
    return pts


def ring_path(c, r, a0, a1, n, plane="xy"):
    """Points round an arc of a circle (degrees), for a coiled body."""
    out = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        if plane == "xy":
            out.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2]))
        else:
            out.append((c[0], c[1] + r * math.sin(a), c[2] + r * math.cos(a)))
    return out


def at(pts, f):
    return pts[min(len(pts) - 1, max(0, int(round(f * (len(pts) - 1)))))]


def tangent(pts, f):
    i = min(len(pts) - 2, max(0, int(round(f * (len(pts) - 1)))))
    a, b = pts[i], pts[i + 1]
    d = tuple(q - p for p, q in zip(a, b))
    n = math.sqrt(sum(v * v for v in d)) or 1.0
    return tuple(v / n for v in d)
