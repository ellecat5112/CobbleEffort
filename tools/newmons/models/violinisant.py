"""Violinisant, the Virtuoso Pokémon (Grass/Psychic), Arpsant evolved, after the art of the A. Fakemon fanpage (the
art's own name): a tall, elegant green bird in mid-performance, a white feathered crest and ruff framing an orange
face mask, a fierce red eye and a long orange beak it plays like a violin with a twig for a bow. A cape of green wings
hangs over its orange-flamed chest, long green-and-white streamers trail from its tail, and it stands on long yellow
legs with pale claws.

Shiny: rose-pink with a lilac chest.

Front is -z, y is up. 36 units tall; baseScale 0.74 (1.65 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _route import tone
from _songbird import P, ramp, solid

SCALE = 0.74
HITBOX = [1.2, 2.25]
KIND = "biped"
K = 3
HEIGHT = 36
LOOK = ("a tall elegant green bird with a white crest and ruff, an orange face mask, a long orange beak it plays like "
        "a violin with a twig bow, an orange-flamed chest, a green wing cape and long tail streamers")


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 1.4 + 0.8 * abs(((y - 13.0) % 2.4) - 1.2):
        return tone(p["orange"], face), None                                  # flame-edged orange chest
    return tone(p["green"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        return tone(p["orange"], face), None                                  # orange face mask
    if face in ("east", "west") and ((z + 1.0) / 0.7) ** 2 + ((y - 29.6) / 0.5) ** 2 < 1:
        return p["red"], None                                                 # a fierce red eye
    return tone(p["green"], face), None


def build() -> Model:
    m = Model("violinisant")
    top = m.bone("violinisant", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    m.round_box(bd, 0, 0.6, 3.4, 4.0, 13.0, 23.0, bodyf, cut=1.4)
    pts = [(0, 14.0, 4.0), (0, 13.0, 12.0), (0, 14.0, 20.0), (0, 12.0, 28.0)]   # long tail streamers
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        rod(m, bd, a, b, 2.2, ramp("green", "white") if i == 2 else solid("green"), extend=0.6, t2=0.8)
    for z in (14.0, 22.0):
        spike(m, bd, (0, 13.4, z), (0, -1, 0.4), 1.4, 2.4, solid("white"))

    hd = m.bone("head", bd, (0, 23, -0.5))
    rod(m, hd, (0, 22.6, -0.5), (0, 27.0, -1.4), 2.4, solid("green"), extend=0.6)              # neck
    m.round_box(hd, 0, -1.2, 2.6, 2.8, 26.6, 31.6, headf, cut=0.8)
    m.round_box(hd, 0, 0.4, 3.0, 2.6, 30.2, 33.6, solid("white"), cut=1.0)       # the white crest
    rod(m, hd, (0, 33.0, 0.6), (0, 34.6, 5.2), 2.8, solid("white"), extend=0.4, t2=1.2)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.6, 27.6, 0.0), (sx * 1, -0.4, 0.2), 1.8, 2.4, solid("white"))       # white ruff
    rod(m, hd, (0, 28.8, -3.6), (0.4, 26.0, -10.4), 1.6, ramp("orange", "beak"), extend=0.4)    # long beak
    rod(m, hd, (-4.6, 24.0, -6.4), (5.4, 29.4, -8.4), 1.0, solid("stick"), extend=0.4)          # the twig bow
    spike(m, hd, (5.4, 29.4, -8.4), (1, 0.4, 0), 0.9, 1.6, solid("white"))

    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 1.6, 14, 1))
        rod(m, lb, (sx * 1.6, 14.0, 1.0), (sx * 2.2, 7.0, -1.0), 1.8, solid("leg"), extend=0.4)
        rod(m, lb, (sx * 2.2, 7.0, -1.0), (sx * 2.0, 1.0, 0.6), 1.4, solid("leg"), extend=0.4)
        for d in ((-0.4, -0.2, -1), (0.4, -0.2, -1), (0, -0.2, 1)):
            spike(m, lb, (sx * 2.0, 0.8, 0.4), d, 1.0, 2.0, solid("claw"))
        ar = m.bone(f"arm_{side}", bd, (sx * 3.2, 22, 0))                         # the cape of wings
        rod(m, ar, (sx * 3.2, 22.0, 0.0), (sx * 4.8, 11.0, 4.0), 4.2, ramp("green", "green_dark"), extend=0.4, t2=1.2)
        spike(m, ar, (sx * 4.8, 11.4, 4.0), (sx * 0.2, -1, 0.3), 2.0, 2.6, solid("white"))
    return m
