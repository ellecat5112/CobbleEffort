"""Shared builder for the eight Cardmon (CobbleEffort: Digital; hand-built after the official renders on wikimon.net):
a round floating head (coloured top, white face, two big black ringed eyes and a little "w" mouth) circled by playing
cards: green cards edged in blue with a blue ring on their face (C1, R1, R2, U1, U2), a blue grid card (C2), hollow
yellow frames with pink rings (S1), or black grid / grey cards and a blade (S2).

make(name, head, cards, card, ...): head = top colour key, cards = list of (centre, rotation, size) placements,
card = "green" | "grid" | "frame" | "black" (per-card overrides allowed in the placements' 4th item).
Shiny: the head turns pink and the green cards purple.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digibeast import ball
from _digidetail import cutout, local, mix, solid
from _route import pal, tone

BASE = {"yellow": (246, 230, 50), "yellow_dark": (200, 170, 20), "blue": (60, 150, 230), "blue_dark": (30, 90, 180),
        "black": (40, 40, 46), "black_dark": (16, 16, 20), "white": (250, 250, 252), "white_dark": (200, 204, 214),
        "eye": (16, 16, 20), "eye_ring": (250, 250, 250), "card": (50, 190, 90), "card_dark": (30, 140, 60),
        "card_edge": (40, 80, 200), "ring": (60, 90, 210), "ring_outer": (190, 196, 210), "frame": (240, 230, 140),
        "pink": (246, 170, 180), "grid": (60, 120, 220), "grid_line": (130, 180, 250), "grey": (190, 194, 204),
        "blade": (70, 72, 82)}
SHINY = {"yellow": (246, 140, 200), "yellow_dark": (200, 80, 150), "blue": (246, 140, 200), "blue_dark": (200, 80, 150),
         "black": (246, 140, 200), "black_dark": (200, 80, 150), "card": (150, 90, 210), "card_dark": (100, 50, 160),
         "grid": (150, 90, 210), "frame": (200, 160, 250)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, head, cards, card="green", r=5.0, cy=None):
    """A Cardmon: head colour key `head`, radius r, centre height cy; cards = [(centre, (rx, ry, rz), (w, h)[, kind])]."""
    # cards are placed relative to the head centre (cy); lift the head so nothing goes below the ground
    low = min([c[0][1] - max(c[2]) / 2 for c in cards if (c[3] if len(c) > 3 else card) != "blade"] + [-r])
    cy = max(r + 1.0, 1.0 - low) if cy is None else cy
    cards = [((c[0][0], c[0][1] + cy, c[0][2]),) + tuple(c[1:]) for c in cards]
    dark = head + "_dark"

    def headf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                d = math.hypot(x - sx * r * 0.42, y - cy - r * 0.12)
                if d < r * 0.3:
                    if math.hypot(x - sx * r * 0.42 + r * 0.08, y - cy - r * 0.2) < r * 0.07:
                        return tone(p["white"], face), None
                    return tone(p["eye"] if d < r * 0.24 else p["eye_ring"] if d < r * 0.28 else p["eye"], face), None
            u = x / (r * 0.12)
            if abs(u) < 2.0 and abs(y - (cy - r * 0.32) - 0.25 * abs(math.sin(u * math.pi / 2))) < 0.18:
                return tone(p["eye"], face), None                       # the little "w" mouth
        # coloured top, white face below a line that dips toward the front
        line = cy + r * 0.05 + (r * 0.35 if face in ("south", "up") else 0.0)
        if y > line or face == "up" or (face in ("east", "west") and y > cy - r * 0.2 and z > -r * 0.2):
            return tone(mix(p[head], p[dark], max(0.0, (cy + r - y) / (3 * r))), face), None
        return tone(p["white"] if face != "down" else p["white_dark"], face), None

    def cardf(kind):
        def s(x, y, z, face, variant, box=None, **k):
            p = P(variant)
            u, v, W, H = local(x, y, z, face, box)
            a, b = u / max(W, 1e-6), v / max(H, 1e-6)
            edge = min(a, 1 - a, b, 1 - b)
            d = math.hypot(a - 0.5, (b - 0.5) * H / max(W, 1e-6))
            if kind == "grid" or kind == "black":
                base = p["grid"] if kind == "grid" else p["black"]
                if edge < 0.06 or (a * 6) % 1 < 0.1 or (b * 8) % 1 < 0.1:
                    return tone(p["grid_line"] if kind == "grid" else p["grey"], face), None
                return tone(base, face), None
            if kind == "frame":
                if edge < 0.1:
                    return tone(p["frame"], face), None
                if 0.16 < d < 0.26:
                    return tone(p["pink"], face), None
                return (0, 0, 0, 0), None
            if kind == "grey":
                if 0.1 < d < 0.18 and abs(b - 0.5) < 0.2:
                    return tone(p["ring"], face), None
                return tone(p["grey"] if edge > 0.06 else p["blade"], face), None
            if edge < 0.07:
                return tone(p["card_edge"], face), None
            if d < 0.17:
                return tone(p["ring"], face), None
            if d < 0.23:
                return tone(p["ring_outer"], face), None
            return tone(p["card"] if edge > 0.14 else p["card_dark"], face), None
        return s

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, cy, 0))
        hd = m.bone("head", bd, (0, cy, 0))
        ball(m, hd, (0, cy, 0), r, headf, layers=6)
        for i, c in enumerate(cards):
            (cx, cyy, cz), rot, (w, h) = c[:3]
            kind = c[3] if len(c) > 3 else card
            cb = m.bone(f"ring_{i}", bd, (0, cy, 0))
            if kind == "blade":
                rod(m, cb, (cx, cyy, cz), (cx + rot[0], cyy + rot[1], cz + rot[2]), 1, solid(P, "blade"), extend=0,
                    t2=2)
                continue
            m.box(cb, cx - w / 2, cyy - h / 2, cz - 0.3, cx + w / 2, cyy + h / 2, cz + 0.3, cardf(kind),
                  rotation=rot, pivot=(cx, cyy, cz))
        return m
    return build
