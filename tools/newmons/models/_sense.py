"""Shared helpers for the sensing rodents (Mousense, Sensarat): eyes always closed, long whiskers to feel their way,
big round ears, buck teeth, pink noses, paws and tails. Each module passes its own palette (BASE, SHINY)."""
from __future__ import annotations

import math

from _boxmodel import mix
from _route import pal, tone


def solid(base, shiny, key):
    def s(x, y, z, face, variant, **k):
        return tone(pal(base, shiny, variant)[key], face), None
    return s


def ear_disc(base, shiny, cx, cy, r, axes="xy"):
    """A round ear plane: a dark rim round a coloured inside, cut to a circle."""
    def s(x, y, z, face, variant, **k):
        p = pal(base, shiny, variant)
        u = x if axes == "xy" else z
        d = math.hypot(u - cx, y - cy) / r
        if d > 1:
            return (0, 0, 0, 0), None
        return (p["ear_in"] if d < 0.68 else p["ear"]), None
    return s


def closed_eyes(h, v, eye_dx, eye_y, half_w, colour):
    """True on two closed eyes: short arcs (a smile-shaped line each)."""
    for sx in (-1, 1):
        dx = h - sx * eye_dx
        if abs(dx) < half_w and abs(v - eye_y - 0.25 * (dx / half_w) ** 2 * half_w) < 0.16:
            return True
    return False


def whisker(m, bone, a, b, base, shiny, key="whisker", thick=0.2):
    """A long thin whisker from a to b: a one-unit ribbon (faces front/back once aimed sideways) cut down to a line
    that tapers to its tip."""
    from _boxmodel import rod
    from _route import along

    def s(x, y, z, face, variant, box=None, **k):
        t = along(z, box)
        mid = box.lo[1] + box.size[1] / 2
        if abs(y - mid) > thick * (1.0 - 0.5 * t) or t > 0.98:
            return (0, 0, 0, 0), None
        return pal(base, shiny, variant)[key], None
    rod(m, bone, a, b, 0, s, extend=0, t2=1)
