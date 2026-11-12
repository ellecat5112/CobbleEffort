"""Shaders shared by the dentistry line (Cavitot, Amalgum, Orthodread): enamel, gums, roots, steel, and the faces.

A face is drawn on one side of a tooth: `side` is the box face it sits on ("north" = front, -z; "east" = the -x side,
"west" = the +x side, as _boxmodel names them) and (cx, cz) the tooth's centre, so the face's horizontal coordinate is
measured from the middle of that side. Features are in model units, so they keep their shape on any texel density.

Shiny: minty enamel (fresh toothpaste) and gold metal (gold fillings and braces); cavities stay dark.
"""
from __future__ import annotations

import math

from _boxmodel import mix

BASE = {
    "enamel": (240, 229, 210), "enamel_dark": (214, 200, 180), "gum": (226, 148, 150), "root": (232, 200, 186),
    "root_tip": (214, 138, 132), "steel": (172, 175, 184), "steel_light": (214, 217, 226), "steel_dark": (118, 121, 132),
    "eye": (250, 206, 218), "eye_rim": (178, 60, 92), "blush": (240, 158, 170), "mouth": (206, 44, 66),
    "mouth_dark": (120, 18, 36), "angry": (224, 40, 52), "line": (150, 112, 96), "cavity": (26, 18, 20),
    "cavity_rim": (78, 50, 38), "stain": (176, 146, 104), "elastic": (232, 70, 110), "rivet": (236, 150, 170),
}
SHINY = {"enamel": (214, 242, 230), "enamel_dark": (178, 214, 200), "steel": (226, 184, 82), "steel_light": (250, 222, 140),
         "steel_dark": (168, 122, 40), "elastic": (70, 190, 230), "rivet": (120, 210, 236), "root": (210, 222, 200)}


def P(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def tri(v):
    """A triangle wave in 0..1 with period 1 (for zigzags)."""
    v = v % 1.0
    return 1 - abs(2 * v - 1)


def face_coords(x, y, z, face, side, cx, cz):
    """(h, on) for a texel: its horizontal offset from the middle of `side`, and whether it lies on that side."""
    if face != side:
        return 0.0, False
    if side == "north":
        return x - cx, True
    if side == "south":
        return cx - x, True
    if side == "west":
        return z - cz, True
    return cz - z, True


def diamond(h, v, a, b):
    """<= 1 inside a diamond of half-width a and half-height b."""
    return abs(h) / a + abs(v) / b


# --- faces --------------------------------------------------------------------------------------------------------

def sad_face(h, y, pal, ey, my, ex=2.0, a=1.25, b=1.7, mw=2.0, mh=1.1, zig=True):
    """Cavitot's and Amalgum's face: pale pink diamond eyes with a darker rim and a shine, pink blush beneath, and an
    open red frown (its corners droop) with a jagged upper lip. -> colour or None."""
    for sx in (-1, 1):
        d = diamond(h - sx * ex, y - ey, a, b)
        if d <= 1:
            if d > 0.74:
                return pal["eye_rim"]
            if diamond(h - sx * ex + 0.3 * a, y - ey - 0.3 * b, 0.28 * a, 0.28 * b) <= 1:
                return (255, 255, 255)
            return pal["eye"]
    dh = abs(h)
    if dh <= mw:
        yc = my - 0.32 * (dh / mw) ** 2 * mw              # corners droop: a frown
        t = mh * (1 - 0.55 * (dh / mw) ** 2)
        top = yc + t / 2 - (0.22 * tri(h * 1.4 + 0.5) if zig else 0)
        if yc - t / 2 <= y <= top:
            edge = min(y - (yc - t / 2), top - y, mw - dh)
            return pal["mouth_dark"] if edge < 0.16 else pal["mouth"]
    return None


def blush(h, y, ey, ex=1.9):
    """How much blush (0..1) a texel gets: soft ovals under the eyes, a little to the outside."""
    best = 0.0
    for sx in (-1, 1):
        d = ((h - sx * (ex + 0.35)) / 1.25) ** 2 + ((y - (ey - 1.75)) / 0.55) ** 2
        best = max(best, 1 - d)
    return max(0.0, best)


def angry_face(h, y, pal, ey, my, ex=1.25, a=0.95, b=0.85, mw=1.25, mh=0.75):
    """Orthodread's face: slanted red angry eyes (the inner corners cut down by a brow line) with a dark rim, and a red
    diamond frown. -> colour or None."""
    for sx in (-1, 1):
        dh = h - sx * ex
        brow = ey + 0.45 * b + 0.75 * (abs(h) - ex)        # higher at the outside, lower towards the middle
        d = diamond(dh, y - ey, a, b)
        if d <= 1 and y <= brow:
            if d > 0.62 or y > brow - 0.18:
                return (40, 16, 22)
            return (255, 214, 214) if abs(dh) < 0.13 * a else pal["angry"]
    d = diamond(h, (y - my) * (1.0 + 0.25 * abs(h)), mw, mh)
    if d <= 1:
        return pal["mouth_dark"] if d > 0.66 else pal["mouth"]
    return None


# --- materials ----------------------------------------------------------------------------------------------------

def enamel(pal, x, y, z, face, groove=None):
    """Tooth enamel: cream, a touch darker low down, a faint groove line down the middle of the sides."""
    col = pal["enamel"]
    if groove is not None and face in ("east", "west") and abs(z - groove) < 0.18:
        col = mix(col, pal["line"], 0.45)
    return col


def steel(pal, x, y, z, face, top_y=None):
    """Polished metal: a bright band near the top edge, darker underneath."""
    if face == "down":
        return pal["steel_dark"]
    if face == "up":
        return pal["steel_light"]
    if top_y is not None and y > top_y - 0.9:
        return pal["steel_light"]
    return pal["steel"]


def root(pal, y, tip_y):
    """A root: pale pink, deeper pink towards its tip."""
    return mix(pal["root"], pal["root_tip"], (tip_y - y) / max(1e-6, tip_y)) if y < tip_y else pal["root"]


def amalgam(pal, x, y, z, cx, cy, cz, r=1.6, seed=0.0):
    """True inside an irregular blob of filling round (cx, cy, cz)."""
    d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2)
    ang = math.atan2(y - cy, (x - cx) + (z - cz))
    return d < r * (1 + 0.22 * math.sin(3 * ang + seed) + 0.12 * math.sin(5 * ang + 2 * seed))
