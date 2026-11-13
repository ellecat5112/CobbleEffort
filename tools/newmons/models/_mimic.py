"""Shared parts for the imitator crab line (Tyrucrab, Crabgron, Primaclaw), after the fakemon art by @dude.dude.art
that the user shared, with the user's idea: Bug crabs whose claws imitate the heads of dangerous Pokémon. A small crab
body with an angry face and thin legs, a plain pincer on one side, and a giant claw shaped like a fearsome head (the
models build those heads; this module has the crab).

Everything thinner than one unit rounds to nothing in the texture, so legs and teeth are at least a unit thick.
"""
from __future__ import annotations

import math

from _boxmodel import rod, spike
from _route import tone


def solid(colour_key, palette):
    """A flat shaded colour from a palette function."""
    def s(x, y, z, face, variant, **k):
        return tone(palette(variant)[colour_key], face), None
    return s


def crab_body(m, bone, palette, cx, cz, rx, rz, y0, y1, eye_y, eye_dx, front_z, cut=1.0):
    """The crab's round body with an angry face on its front: slanted eyes under heavy brows, a little mouth."""
    def s(x, y, z, face, variant, **k):
        p = palette(variant)
        if face == "north":
            for sx in (-1, 1):
                dx, dy = x - (cx + sx * eye_dx), y - eye_y
                if abs(dx) < 0.55 and -0.9 < dy < 0.6:
                    if dy > 0.25 - 0.5 * dx * sx:
                        return p["brow"], None                                  # the angry brow
                    return p["eye"], (p["eye"] if p.get("eye_glow") else None)
            if abs(x - cx) < 0.4 and abs(y - (eye_y - 1.6)) < 0.18:
                return p["brow"], None                                          # a little frown
        if face == "down":
            return p["belly"], None
        return tone(p["shell"], face), None
    m.round_box(bone, cx, cz, rx, rz, y0, y1, s, cut=cut)


def crab_legs(m, palette, top, pairs, cx, body_y, body_rx, reach, z_list, t=1.1, names=True):
    """Thin jointed legs, `pairs` per side at z_list, splaying out to `reach`. The first and last pair of each side get
    bones named for the rig (leg_front_* / leg_back_*); the middle ones ride on the first."""
    shader = solid("leg", palette)
    for sx, side in ((-1, "left"), (1, "right")):
        bones = {}
        for i, z in enumerate(z_list[:pairs]):
            role = "front" if i == 0 else ("back" if i == pairs - 1 else None)
            if role and names:
                bones[i] = m.bone(f"leg_{role}_{side}", top, (cx + sx * body_rx, body_y, z))
            bn = bones.get(i) or bones.get(0)
            knee = (cx + sx * (body_rx + reach * 0.55), body_y + 1.6, z * 1.15)
            foot = (cx + sx * (body_rx + reach), 0.0, z * 1.35)
            rod(m, bn, (cx + sx * body_rx, body_y, z), knee, t, shader, extend=0.2)
            rod(m, bn, knee, foot, t * 0.85, shader, extend=0.1)


def pincer(m, bone, palette, base, tip, size, key="claw"):
    """A plain crab pincer: an arm from base to tip, then two prongs."""
    sh = solid(key, palette)
    rod(m, bone, base, tip, max(1.0, size * 0.35), solid("leg", palette), extend=0.2)
    d = [b - a for a, b in zip(base, tip)]
    n = math.sqrt(sum(v * v for v in d)) or 1
    u = [v / n for v in d]
    m.round_box(bone, tip[0], tip[2], size * 0.45, size * 0.4, tip[1] - size * 0.4, tip[1] + size * 0.4, sh, cut=size * 0.15)
    for up in (1, -1):                                                          # the two prongs
        spike(m, bone, (tip[0] + u[0] * size * 0.3, tip[1] + up * size * 0.25, tip[2] + u[2] * size * 0.3),
              (u[0], up * 0.45, u[2]), max(1.0, size * 0.3), size * 0.9, sh, tip=max(1.0, size * 0.18))


def teeth(m, bone, xs, y, z, down, shader, w=1.0, h=1.2):
    """A row of pointed teeth along x at height y, pointing down (down=True) or up."""
    for x in xs:
        spike(m, bone, (x, y, z), (0, -1 if down else 1, 0), w, h, shader)
