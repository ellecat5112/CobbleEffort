"""Shared builder for the Dot Digimon (CobbleEffort: Digital; after the pixel-sprite art and the voxel figures on
wikimon.net): each one is its pixel sprite turned into a little block figure. make(name, rows, palette, ...) takes the
front view as text rows (one character a pixel, "." empty), merges runs of one colour along each row into a single box,
and gives each pixel `px` model units; rows from the top down to `head_rows` go on the head bone, the bottom
`leg_rows` rows split down the middle into the two leg bones, and `deep` maps a character to a depth in pixels
(default `depth`) and `front` to a forward offset in pixels, so faces sit proud and limbs stay slim.
"""
from __future__ import annotations

from _boxmodel import Model
from _digidetail import solid
from _route import pal


def make(name, rows, base, shiny, px=2.0, depth=4, head_rows=0, leg_rows=0, deep=None, front=None):
    deep = deep or {}
    front = front or {}

    def P(v):
        return pal(base, shiny, v)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        H = len(rows)
        W = max(len(r) for r in rows)
        bd = m.bone("body", top, (0, (leg_rows) * px, 0))
        hd = m.bone("head", bd, (0, (H - head_rows) * px, 0)) if head_rows else bd
        legs = {}
        if leg_rows:
            legs[1] = m.bone("leg_left", top, (px * W / 4, leg_rows * px, 0))
            legs[-1] = m.bone("leg_right", top, (-px * W / 4, leg_rows * px, 0))
        for r, row in enumerate(rows):
            y1 = (H - r) * px
            y0 = y1 - px
            c = 0
            while c < len(row):
                ch = row[c]
                if ch == ".":
                    c += 1
                    continue
                e = c
                while e + 1 < len(row) and row[e + 1] == ch and (not leg_rows or r < H - leg_rows or
                                                                  (e + 1 < W / 2) == (c < W / 2)):
                    e += 1
                x0 = (c - W / 2) * px
                x1 = (e + 1 - W / 2) * px
                d = deep.get(ch, depth) * px / 2
                f = front.get(ch, 0.0) * px
                if r < head_rows:
                    bone = hd
                elif leg_rows and r >= H - leg_rows:
                    bone = legs[1 if (x0 + x1) / 2 > 0 else -1]
                else:
                    bone = bd
                m.box(bone, x0, y0, -d - f, x1, y1, d - f, solid(P, ch))
                c = e + 1
        return m
    return build
