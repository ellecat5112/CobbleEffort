"""Shared builder for Icemon and Insekimon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): a
golem of stacked chunks: a big round-cornered head of stones with round ears, round yellow eyes and a wide dark grin
lined with block teeth, a stubby torso of stones and chunky stone arms and legs. make(name, colours) picks the stone:
ice blocks (Icemon) or pale green meteorite (Insekimon).
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _digidetail import local, solid
from _route import pal, tone


def make(name, colours, shiny):
    base = dict({"eye": (250, 210, 40), "pupil": (20, 20, 24), "mouth": (24, 24, 30), "tooth": (250, 250, 250),
                 "edge": (40, 44, 60)}, **colours)

    def P(v):
        return pal(base, shiny, v)

    def chunkf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        if min(u, v, W - u, H - v) < 0.3:
            return tone(p["edge"], face), None
        c = p["stone_light"] if face == "up" or (u + v) < 1.2 else p["stone"]
        if face in ("down",) or (u > W * 0.7 and v < H * 0.3):
            c = p["stone_dark"]
        return tone(c, face), None

    def facef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                d = math.hypot(x - sx * 2.6, y - 19.6)
                if d < 0.6:
                    return tone(p["pupil"], face), None
                if d < 1.5:
                    return tone(p["eye"], face), None
            if 13.6 < y < 17.0 and abs(x) < 4.4 - (17.0 - y) * 0.4:
                if y > 16.0 and (x + 5.0) % 1.8 < 1.2:
                    return tone(p["tooth"], face), None
                return tone(p["mouth"], face), None
        return chunkf(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 6, 0))
        for (cx, cy, cz, s) in ((0, 7.0, 0, 3.0), (-2.0, 9.0, 0.4, 2.2), (2.0, 8.6, -0.4, 2.2), (0, 10.4, 0, 2.6)):
            m.box(bd, cx - s, cy - s, cz - s, cx + s, cy + s, cz + s, chunkf)                # stone torso
        hd = m.bone("head", bd, (0, 12, 0))
        m.round_box(hd, 0, 0, 6.0, 4.6, 11.6, 22.6, facef, cut=2)                             # big head
        for (cx, cy, cz, s) in ((-4.6, 22.0, 0, 1.8), (4.6, 22.0, 0, 1.8), (0, 23.0, 1.0, 2.0), (-2.4, 23.4, -1.0, 1.4),
                                (2.4, 23.4, -1.0, 1.4), (-6.2, 16.0, 0, 1.4), (6.2, 16.0, 0, 1.4)):
            m.box(hd, cx - s, cy - s, cz - s, cx + s, cy + s, cz + s, chunkf)                # chunk lumps
        for sx in (-1, 1):                                                                 # round ears
            m.box(hd, sx * 5.0 - 1.8, 23.0, -1.2, sx * 5.0 + 1.8, 26.4, 1.2, chunkf)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 4.6, 10.0, 0))
            for j, (dx, dy, s) in enumerate(((4.6, 9.6, 1.4), (5.6, 7.6, 1.4), (6.2, 5.2, 1.6), (6.4, 2.6, 2.0))):
                m.box(ab, sx * dx - s, dy - s, -s, sx * dx + s, dy + s, s, chunkf)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 2.0, 4.0, 0))
            for (dy, s) in ((3.6, 1.4), (1.4, 1.6)):
                m.box(lg, sx * 2.2 - s, dy - s, -s - 0.4, sx * 2.2 + s, dy + s, s - 0.4, chunkf)
        return m

    return build
