"""Dracarabo, the Dragon Beetle Pokémon (Bug/Dragon), Ovarupa evolved, after the art by @artworks218_ (the art's own
name, used with the creator's permission): a beetle whose great horn has grown into the orange skull of a dragon, a
long jagged upper jaw and a lower jaw ending in a curved tusk, a swirl on each cheek and two yellow-tipped horns on
top. Under it sits the beetle's own small brown face (a yellow beak, green eyes with dark slits) and a dark thorax with
a spike, then a big rounded abdomen: yellow wing cases licked by orange flames, an orange ribbed underside. Six spiky
dark brown legs end in yellow claws.

Shiny: a teal dragon skull and flames, navy legs and thorax, pink eyes.

Front is -z, y is up. 31 units tall to its horn tips; baseScale 0.93 (1.8 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix, rod, spike
from _route import tone
from _scarab import P, horn, slab_xy, solid

SCALE = 0.93
HITBOX = [1.9, 1.95]
KIND = "quadruped"
K = 3
HEIGHT = 31
LOOK = ("a beetle whose great horn is an orange dragon's skull with jagged jaws, a small brown face with a yellow beak "
        "and green eyes, a yellow flame-striped abdomen and six spiky dark legs with yellow claws")

ABDOMEN = [(4, 4.6, 4.4), (6, 5.6, 5.2), (8, 6.2, 5.8), (10, 6.4, 6.0), (12, 6.2, 5.8), (14, 5.4, 5.0), (16, 4.0, 3.6)]
ABD_Y = 12.5


def flame(z):
    """Height of the orange flame tongues rising up the wing cases at z (a sawtooth of three points)."""
    t = ((z - 3.0) / 4.2) % 1.0
    return 3.6 * (1 - abs(2 * t - 1)) * (1 - max(0.0, z - 13) / 5)


def abdf(x, y, z, face, variant, **k):
    p = P(variant)
    edge = ABD_Y - 1.0
    if face == "down" or (face != "up" and y < edge):
        if abs(((z - 3.0) % 2.6) - 1.3) < 0.22:
            return p["orange_dark"], None                                     # ribs of the underside
        return tone(p["orange_dark"] if face == "down" else p["orange"], face), None
    if face == "up" and abs(x) < 0.3:
        return p["yellow_dark"], None                                         # the split between the wing cases
    if face != "up" and y - edge < flame(z):
        return tone(p["orange"], face), None                                  # flames licking up the wing cases
    if face != "up" and y - edge < 0.5:
        return p["brown_dark"], None                                          # the rim of the wing cases
    return tone(mix(p["yellow"], p["yellow_light"], 0.5) if face == "up" else p["yellow"], face), None


def skullf(x, y, z, face, variant, **k):
    """The orange dragon skull: lighter on top, a swirl on each cheek."""
    p = P(variant)
    if face in ("east", "west") and abs(x) > 4.6:
        dz, dy = z + 6.2, y - 18.4
        r, th = math.hypot(dz, dy), math.atan2(dy, dz) % (2 * math.pi)
        if r < 3.2:
            for turn in range(3):
                if abs(r - (0.35 + 0.42 * (th + 2 * math.pi * turn))) < 0.3:
                    return p["orange_dark"], None
    return tone(p["orange_light"] if face == "up" else p["orange"], face), None


def facef(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and abs(x) > 2.4:
        dz, dy = z + 6.0, y - 9.8
        if (dz / 1.4) ** 2 + (dy / 1.0) ** 2 < 1:
            if abs(dz + 0.3) < 0.18 or abs(dz - 0.25) < 0.18:
                return p["eye_dark"], None                                    # two dark slits
            return (p["eye_light"] if dy > 0.45 else p["eye"]), None
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.6, y - 9.8) < 0.7:
                return p["eye"], None
    return tone(p["brown"], face), None


def build() -> Model:
    m = Model("dracarabo")
    top = m.bone("dracarabo", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, -0.5, 4.6, 4.0, 7.0, 15.0, solid("brown"), cut=1.6)    # the dark thorax
    m.box(bd, -4.0, 13.4, 1.0, 4.0, 15.6, 6.4, solid("brown"))                 # its plate over the abdomen
    spike(m, bd, (0, 15.0, 0.4), (0, 1, 0.55), 2.6, 4.6, solid("brown_dark"), tip=1.4)
    for zc, rx, ry in ABDOMEN:                                                 # the big rounded abdomen
        slab_xy(m, bd, 0, ABD_Y, rx, ry, zc - 1.05, zc + 1.05, abdf, cut=max(1, round(min(rx, ry) * 0.32)))

    hd = m.bone("head", bd, (0, 12, -4))
    m.box(hd, -2.6, 6.6, -8.0, 2.6, 11.6, -3.6, facef)                         # its own small face
    spike(m, hd, (0, 8.0, -7.8), (0, -0.8, -0.6), 2.2, 3.4, solid("yellow"), tip=1.2)   # yellow beak
    # the dragon skull its horn has become
    m.round_box(hd, 0, -6.0, 5.0, 4.4, 12.6, 24.0, skullf, cut=1.8)
    m.box(hd, -3.0, 14.0, -11.0, 3.0, 20.0, -10.0, solid("inner"))              # the back of its open mouth
    a, b = (0, 20.5, -8.5), (0, 28.0, -26.0)
    rod(m, hd, a, b, 8.0, skullf, extend=0.5, t2=7.0)                          # the long upper jaw
    for f in (0.28, 0.46, 0.64, 0.82):                                         # jagged teeth along its edge
        p = tuple(aa + (bb - aa) * f for aa, bb in zip(a, b))
        spike(m, hd, (p[0], p[1] - 3.4, p[2]), (0, -1, 0.15), 2.0, 3.0, solid("orange_dark"))
    spike(m, hd, (0, 26.0, -24.8), (0, -1, -0.45), 5.0, 6.0, skullf, tip=2.6)  # the hooked tip of the jaw
    for sx in (-1, 1):
        horn(m, hd, (sx * 2.6, 23.0, -4.0), (sx * 3.6, 28.0, -2.6), (sx * 4.2, 31.6, -1.6), 2.4, 1.8)

    jw = m.bone("jaw", hd, (0, 15, -9))
    c, d = (0, 14.5, -9.0), (0, 13.0, -24.0)
    rod(m, jw, c, d, 5.0, skullf, extend=0.5, t2=3.6)                          # the lower jaw
    spike(m, jw, (0, 14.0, -23.4), (0, 1, -0.35), 3.0, 7.0, skullf, tip=1.6)   # its curved tusk
    for f in (0.35, 0.6):
        p = tuple(aa + (bb - aa) * f for aa, bb in zip(c, d))
        spike(m, jw, (p[0], p[1] + 1.6, p[2]), (0, 1, 0.1), 1.8, 2.6, solid("orange_dark"))

    for sx, side in ((-1, "left"), (1, "right")):                              # six spiky legs with yellow claws
        for role, z in (("front", -3.0), ("mid", 1.6), ("back", 6.0)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 4.0, 9.0, z))
            knee = (sx * 8.6, 12.0, z * 1.1)
            foot = (sx * 11.0, 2.6, z * 1.3)
            rod(m, lb, (sx * 4.0, 9.0, z), knee, 2.2, solid("brown"), extend=0.4)
            rod(m, lb, knee, foot, 2.0, solid("brown"), extend=0.3)
            spike(m, lb, knee, (sx * 0.5, 1, 0), 1.4, 2.0, solid("brown_dark"))          # a spike at each knee
            spike(m, lb, foot, (sx * 0.3, -1, 0), 1.6, 2.8, solid("yellow"), tip=1.0)    # the claw
    return m
