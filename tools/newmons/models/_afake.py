"""Shared helpers for the A. Fakemon starter trio (Wigwoof, Sounflame and Fangfosh and their lines), after the fakemon
art of the A. Fakemon fanpage (names kept): eyes, solid shaders from a palette, cut-out planes edged with tongues
(flame wings, capes, fin fans) and boxes given by any two corners.
"""
from __future__ import annotations

import math

from _route import along, tone


def solid_of(P):
    """-> solid(key, glow=False): a shader painting palette colour `key` (glowing if glow)."""
    def solid(key, glow=False):
        def s(x, y, z, face, variant, **k):
            c = P(variant)[key]
            return tone(c, face), (c if glow else None)
        return s
    return solid


def ramp_of(P):
    """-> ramp(key_a, key_b): a rod shader blending from key_a at its root to key_b at its tip."""
    def ramp(a, b, start=0.0):
        def s(x, y, z, face, variant, box=None, **k):
            p = P(variant)
            t = max(0.0, min(1.0, (along(z, box) - start) / max(1e-6, 1 - start)))
            c = tuple(int(round(p[a][i] * (1 - t) + p[b][i] * t)) for i in range(3))
            return tone(c, face), None
        return s
    return ramp


def bx(m, bone, a, b, shader, **kw):
    """A box between two corners given in any order."""
    (x0, x1), (y0, y1), (z0, z1) = (sorted(v) for v in zip(a, b))
    m.box(bone, x0, y0, z0, x1, y1, z1, shader, **kw)


def round_eye(dx, dy, r, p, iris, pupil="pupil", white="white", iris_frac=0.72, pupil_frac=0.36, look=(0.0, 0.0),
              ry=None):
    """A round (or, with ry, oval) eye: white, a coloured iris, a dark pupil and a shine. -> colour or None."""
    ry = ry or r
    if (dx / r) ** 2 + (dy / ry) ** 2 > 1:
        return None
    if math.hypot(dx + r * 0.3, dy - ry * 0.38) < min(r, ry) * 0.22:
        return p[white]
    di = math.hypot(dx - look[0] * r, dy - look[1] * ry)
    if di < min(r, ry) * pupil_frac:
        return p[pupil]
    if di < min(r, ry) * iris_frac:
        return p[iris]
    return p[white]


def tongues(u, peaks):
    """Depth of the tongues (flames, cape tatters, fin rays) at u: peaks = [(u0, depth, half-width)]."""
    return max((d * max(0.0, 1 - abs(u - u0) / w) for u0, d, w in peaks), default=0.0)


CUT = (0, 0, 0, 0)
