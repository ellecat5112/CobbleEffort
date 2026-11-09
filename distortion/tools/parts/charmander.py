"""Charmander line (Fire -> Water): sea life. The flame on the tail becomes a mermaid tail: the flame planes go (and the
flame layer), a fluke grows from the tail tip and the tail gets fish scales."""
from __future__ import annotations

import math

from _kit import clamp, mix

LINE = ["charmander", "charmeleon", "charizard"]
RECOLOUR = None          # the complement (orange -> blue), as shipped in 0.4.0

# the last tail bone (the fluke's parent), the flame bones (emptied), the scaled tail bones, the fluke (width, length)
TAILS = {
    "charmander": ("tail3", ["fire", "fire2"], ["tail2", "tail3"], (11, 7)),
    "charmeleon": ("tail4", ["fire"], ["tail2", "tail3", "tail4"], (13, 8)),
    "charizard": ("tail5", ["fire", "fire2"], ["tail3", "tail4", "tail5"], (18, 12)),
}
FIN = {False: ((80, 214, 226), (28, 104, 168), (170, 244, 250)),
       True: ((206, 156, 255), (110, 70, 186), (240, 214, 255))}
SCALE = {False: ((40, 120, 190), (120, 210, 240)), True: ((120, 80, 200), (220, 190, 255))}


class Fluke:
    """The fluke: two lobes spreading from the tail tip, rays fanning out, a darker rim. t = 0 is the far end."""

    def paint(self, ctx, rects, size, reskin):
        centre, edge, ray = FIN[ctx.shiny]
        for face in ("up", "down"):
            u, v, w, l = rects[face]
            inside = [[self.inside((x + 0.5) / w, (y + 0.5) / l) for x in range(w)] for y in range(l)]
            for y in range(l):
                for x in range(w):
                    if not inside[y][x]:
                        ctx.put(u + x, v + y, (0, 0, 0, 0))
                        continue
                    inner = 0 < x < w - 1 and 0 < y < l - 1 and inside[y][x - 1] and inside[y][x + 1] and inside[y - 1][x] and inside[y + 1][x]
                    xn = (x + 0.5) / w * 2 - 1
                    s = 1 - (y + 0.5) / l
                    if not inner:
                        c = edge
                    elif abs(math.atan2(xn, s + 0.25) * 4.2) % 1 < 0.22:
                        c = ray
                    else:
                        c = clamp(mix(centre, edge, min(1.0, (abs(xn) + s) / 1.4) * 0.35))
                    ctx.put(u + x, v + y, c)

    @staticmethod
    def inside(sx, t):
        s = 1 - t                                              # 0 at the tail, 1 at the far end
        half = 0.22 + 0.78 * s ** 0.55
        notch = 0.0 if s < 0.7 else 0.3 * (s - 0.7) / 0.3
        return notch <= abs(sx * 2 - 1) <= half


class Scales:
    """Fish scales over the tail, the body colour kept underneath (a reskin)."""

    def paint(self, ctx, rects, size, reskin):
        dark, light = SCALE[ctx.shiny]
        for face, (u, v, w, h) in rects.items():
            for y in range(h):
                for x in range(w):
                    r, g, b, a = ctx.body[u + x, v + y]
                    if a == 0:
                        continue
                    row = y // 2
                    cx = (x + (row % 2)) % 3
                    outline = (y % 2 == 1 and cx != 1) or (y % 2 == 0 and cx == 0)
                    c, k = (dark, 0.55) if outline else (light, 0.35)
                    ctx.put(u + x, v + y, (int(r * (1 - k) + c[0] * k), int(g * (1 - k) + c[1] * k), int(b * (1 - k) + c[2] * k), a))


def build(kit):
    tip, flame, scaled, (w, l) = TAILS[kit.model]
    kit.reskin(Scales(), *scaled)
    kit.hide(*flame)
    kit.drop_layers.add("flame")
    lo, hi = kit.bbox(tip)
    y, z_end = (lo[1] + hi[1]) / 2, hi[2]
    kit.add_bone("distorted_fluke", tip, [0, y, z_end])
    kit.box("distorted_fluke", [-w / 2, y, z_end - 1], [w, 0, l], Fluke())
