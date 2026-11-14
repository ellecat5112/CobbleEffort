"""Shared bits for the four pure Galar fossils (the art the user shared, names kept, artist not named): what the
Fossilized Drake, Bird, Dino and Fish really were before they were stitched into Dracozolt, Arctozolt, Dracovish and
Arctovish. Each model passes its own BASE/SHINY palettes to `palette()`."""
from __future__ import annotations

import math

from _afake import ramp_of, solid_of
from _boxmodel import spike
from _route import pal, tone


def palette(base, shiny):
    def P(v):
        return pal(base, shiny, v)
    return P, solid_of(P), ramp_of(P)


def slab_z(m, bone, cx, cy, rx, ry, z0, z1, shader, cut=None):
    """A slab running front to back, rounded in cross-section."""
    cut = max(0.5, round(min(rx, ry) * 0.35, 1)) if cut is None else cut
    m.box(bone, cx - rx, cy - ry + cut, z0, cx + rx, cy + ry - cut, z1, shader)
    m.box(bone, cx - rx + cut, cy - ry, z0 - 0.05, cx + rx - cut, cy + ry, z1 - 0.05, shader)


def body_along(m, bone, sections, shader):
    """A body built from front-to-back slabs: sections = [(z0, z1, cy, rx, ry)]."""
    for z0, z1, cy, rx, ry in sections:
        slab_z(m, bone, 0, cy, rx, ry, z0, z1, shader)


def plates(m, bone, pts, shader, w=1.6):
    """A row of dorsal plates/spikes: pts = [(x, y, z, height, lean_z)]."""
    for x, y, z, h, lean in pts:
        spike(m, bone, (x, y, z), (0, 1, lean), w, h, shader, tip=w * 0.45)


def eye_at(p, u, v, r, iris="eye", pupil="pupil", white="white"):
    """A round eye: white, iris, pupil, glint. (u, v) from its centre on the face."""
    d = math.hypot(u, v)
    if d >= r:
        return None
    if math.hypot(u - r * 0.3, v - r * 0.35) < r * 0.22:
        return p[white]
    if d < r * 0.45:
        return p[pupil]
    return p[iris]


def toned(P, key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s
