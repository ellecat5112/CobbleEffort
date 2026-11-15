"""Shared parts for the CobbleEffort Nidoran♂ line (Fire/Dragon; the user's "Kiruvian" regional art, artist not named):
charcoal-black hide with spiky fur, glowing magma-red patches and plates, orange-gold eyes, white claws and fangs;
Nidorino grows a translucent quartz horn, Nidoking a row of quartz crystals down its back, pale stone plates on its
limbs and cream crescent ears.

Shiny: midnight blue with azure plates and cyan-glowing patches."""
from __future__ import annotations

import math

from _afake import ramp_of, solid_of
from _boxmodel import spike
from _route import pal, tone

BASE = {"char": (52, 50, 58), "char_light": (80, 78, 88), "char_dark": (32, 30, 36), "red": (198, 46, 46),
        "red_dark": (130, 28, 34), "ember": (255, 110, 60), "eye": (244, 172, 40), "pupil": (24, 18, 18),
        "white": (248, 246, 240), "inner": (222, 150, 124), "mouth": (226, 110, 120), "crystal": (246, 226, 216, 170),
        "crystal_rim": (226, 196, 186, 220), "cream": (238, 226, 192), "stone": (204, 198, 204), "stone_dark": (168, 162, 170),
        "belly": (104, 96, 104)}
SHINY = {"char": (40, 48, 82), "char_light": (64, 74, 114), "char_dark": (26, 30, 54), "red": (60, 140, 230),
         "red_dark": (36, 90, 170), "ember": (90, 220, 255), "inner": (150, 190, 240), "crystal": (210, 240, 255, 170),
         "crystal_rim": (170, 216, 246, 220)}


def palette():
    def P(v):
        return pal(BASE, SHINY, v)
    return P, solid_of(P), ramp_of(P)


P, solid, ramp = palette()


def coords(x, y, z, face):
    return {"up": (x, z), "down": (x, z), "north": (x, y), "south": (-x, y), "east": (z, y), "west": (-z, y)}[face]


def patched(key="char", patch="red", spacing=3.2, size=0.85, glow=True, seed=0.0):
    """Hide with hexagonal magma patches on a jittered grid (glowing, like rock cooling over embers)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        a, b = coords(x, y, z, face)
        i, j = math.floor(a / spacing), math.floor(b / spacing)
        h = math.sin(i * 12.9898 + j * 78.233 + seed) * 43758.5453
        h -= math.floor(h)
        if h > 0.45:
            ca = (i + 0.3 + 0.4 * h) * spacing
            cb = (j + 0.3 + 0.4 * ((h * 7.13) % 1)) * spacing
            u, v = abs(a - ca), abs(b - cb)
            if max(u * 0.87 + v * 0.5, v) < size * (0.7 + 0.5 * h):
                c = p[patch]
                return tone(c, face), (p["ember"] if glow and patch == "red" else None)
        if face == "down":
            return tone(p["char_dark"], face), None
        return tone(p[key], face), None
    return s


def plate(key="red", dark="red_dark"):
    """A smooth plate (the rump, the chest band), darker underneath, with a few dark spots."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        a, b = coords(x, y, z, face)
        if (math.sin(a * 1.3 + 1.3) + math.sin(b * 1.5 - 0.7)) > 1.25:
            return tone(p["char"], face), None
        return tone(p[dark] if face == "down" else p[key], face), None
    return s


def earf(edge="red", inner="stone_dark", back="char"):
    """A big ear (a flat rod pointing up/out): grey inside (its local up face shows to the front), edged in red."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        lx = x - (box.lo[0] + box.size[0] / 2)
        t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)
        if abs(lx) > box.size[0] / 2 - 0.55 or t > 0.85:
            return tone(p[edge], face), None
        if face == "up":
            return tone(p[inner], face), None
        return tone(p[back], face), None
    return s


def hexplate(key="stone", line="stone_dark", cell=1.6):
    """Pale stone armour cut into hexagons (Nidoking's shoulders, elbows and knees)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        a, b = coords(x, y, z, face)
        col = math.floor(a / (cell * 1.5))
        b2 = b + (cell * 0.866 if col % 2 else 0)
        u = a - (col + 0.5) * cell * 1.5
        v = (b2 % (cell * 1.732)) - cell * 0.866
        d = max(abs(u) * 0.866 + abs(v) * 0.5, abs(v))
        if d > cell * 0.70:
            return tone(p[line], face), None
        return tone(p[key], face), None
    return s


def crystal():
    """Translucent quartz (the shell layer), its edges a little stronger."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)
        return (p["crystal_rim"] if t < 0.15 else p["crystal"]), None
    return s


def eye(p, u, v, r, side):
    """An orange-gold eye, angled (lower toward the snout), with a dark pupil and a glint."""
    if v > r * 0.5 - 0.35 * side * u or v < -r * 0.65 or abs(u) > r:
        return None
    if abs(u + side * r * 0.15) < r * 0.28 and v < r * 0.3:
        return p["pupil"]
    if u * side > r * 0.45 and v > 0:
        return p["white"]
    return p["eye"]


def claws(m, bone, x, y, z, n=3, w=1.0, length=1.6, spread=0.9):
    """White claws pointing forward from a foot at (x, y, z)."""
    for k in range(n):
        dx = (k - (n - 1) / 2) * spread
        spike(m, bone, (x + dx, y, z), (dx * 0.2, -0.3, -1), w, length, solid("white"), tip=max(0.4, w * 0.5))


def spikes(m, bone, base, dirs, w, h, shader):
    """A fan of fur spikes from `base` along each direction in dirs."""
    for d in dirs:
        spike(m, bone, base, d, w, h, shader, tip=max(0.5, w * 0.45))
