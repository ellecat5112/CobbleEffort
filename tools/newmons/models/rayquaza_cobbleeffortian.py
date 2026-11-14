"""The CobbleEffort Rayquaza (Flying), after Pigeon Chop's art and the user's idea: far longer than Rayquaza and
wound in coils. Its front half is white, traced with glowing red lines that link into hexagon chains, a fiery crack
across its chest; long white blades fan back from its shoulders, and two red ribbons of hexagonal links stream from the
back of its head. Its rear half is black, ringed with Rayquaza's glowing yellow circles and armoured with red-rimmed
hexagonal fins, coiled two turns and more beneath it. A long white head with a blue eye and a roaring red mouth; small
red arms with hooked claws.

Shiny: the halves swap: black front with gold chains, white coils with red rings.

Front is -z, y is up. 72 units tall (the ribbons); baseScale 1.0 (4.5 m coiled, over 14 m long).
"""
from __future__ import annotations

import math

from _afake import solid_of
from _boxmodel import Model, aim, rod, spike
from _route import pal, tone

SCALE = 1.0
HITBOX = [2.6, 4.2]
KIND = "floater"
K = 2
HEIGHT = 72
LOOK = ("a far longer Rayquaza wound in coils: a white front half traced with glowing red hexagon chains and a fiery "
        "chest crack, white blades fanning back from its shoulders, two red ribbons of hexagonal links from its head, "
        "and a black rear half ringed with glowing yellow circles and red-rimmed hexagonal fins, coiled beneath it")

BASE = {"white": (238, 238, 240), "white_dark": (198, 198, 206), "red": (214, 64, 56), "red_glow": (255, 96, 70),
        "fire": (255, 150, 70), "black": (40, 40, 44), "black_light": (64, 64, 70), "yellow": (240, 204, 64),
        "yellow_glow": (255, 226, 90), "eye": (90, 170, 240), "pupil": (20, 40, 80), "mouth": (150, 70, 90),
        "teeth": (250, 250, 250), "claw": (214, 92, 70)}
SHINY = {"white": (44, 44, 50), "white_dark": (30, 30, 36), "red": (232, 188, 70), "red_glow": (255, 216, 90),
         "fire": (255, 210, 90), "black": (232, 232, 236), "black_light": (250, 250, 252), "yellow": (214, 64, 56),
         "yellow_glow": (255, 96, 70)}


def P(variant):
    return pal(BASE, SHINY, variant)


solid = solid_of(P)


def path():
    """The spine: a rising helix of black coils (tail tip outermost, at the bottom) ending at the front, then the white
    neck rearing up in an S to the head. -> [(point, thickness, part)]"""
    pts = []
    n = 30
    for i in range(n + 1):
        t = i / n
        th = math.pi - 2 * math.pi * 2.2 * (1 - t)                      # ends facing front (theta = pi)
        r = 15 - 5 * t
        pts.append(((r * math.sin(th), 2 + 19 * t, 6 + r * math.cos(th)), 2.5 + 5.5 * t ** 0.7, "coil"))
    for p, w in (((-2.5, 29, -5), 8), ((-2.5, 36, -3), 7.5), ((-0.5, 43, -0.5), 7), ((1.5, 49, 0), 6.5),
                 ((1.5, 54, -3), 6), ((0, 57, -7), 5.5)):
        pts.append((p, w, "neck"))
    return pts


def ring_on(lx, ly, la, L, t, p):
    """A glowing yellow circle on the side of a black segment."""
    r = min(L, t) * 0.34
    d = math.hypot(la - L / 2, ly)
    return abs(d - r) < 0.42


def coilf(x, y, z, face, variant, box=None, **k):
    """A black coil segment: a yellow ring on each side, a yellow line along its back."""
    p = P(variant)
    L, t = box.size[2], box.size[0]
    lx = x - (box.lo[0] + box.size[0] / 2)
    ly = y - (box.lo[1] + box.size[1] / 2)
    la = box.lo[2] + box.size[2] - z
    if face in ("east", "west") and L > 3 and ring_on(lx, ly, la, L, t, p):
        return p["yellow"], p["yellow_glow"]
    if face == "up" and abs(lx) < 0.4:
        return p["yellow"], p["yellow_glow"]
    return tone(p["black_light"] if face == "up" else p["black"], face), None


def neckf(fire=False):
    """A white neck segment: a red line along each side linking into hexagons; a fiery crack on the chest if fire."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        lx = x - (box.lo[0] + box.size[0] / 2)
        ly = y - (box.lo[1] + box.size[1] / 2)
        la = box.lo[2] + box.size[2] - z
        if face in ("east", "west"):
            q = la % 4.0 - 2.0
            hexd = max(abs(ly) * 1.15, abs(ly) * 0.58 + abs(q) * 1.0)
            if abs(hexd - 1.5) < 0.38 or (abs(ly) < 0.35 and abs(q) > 1.6):
                return p["red"], p["red_glow"]
        if fire and face == "down" and abs(lx + 0.6 * math.sin(la)) < 1.2 + 0.4 * math.sin(la * 2.3):
            return p["fire"], p["fire"]
        return tone(p["white_dark"] if face == "down" else p["white"], face), None
    return s


def hexfinf(x, y, z, face, variant, box=None, **k):
    """A red-rimmed black hexagonal fin (a cut-out plate)."""
    p = P(variant)
    lz = z - (box.lo[2] + box.size[2] / 2)
    ly = y - (box.lo[1] + box.size[1] / 2)
    d = max(abs(ly) * 1.15, abs(ly) * 0.58 + abs(lz) * 1.0)
    if d > 2.6:
        return (0, 0, 0, 0), None
    if d > 1.9:
        return p["red"], p["red_glow"]
    return tone(p["black"], face), None


def ribbonf(x, y, z, face, variant, box=None, **k):
    """A red ribbon of hexagonal links (cut out between them)."""
    p = P(variant)
    lx = x - (box.lo[0] + box.size[0] / 2)
    la = box.lo[2] + box.size[2] - z
    q = la % 3.2 - 1.6
    d = max(abs(lx) * 1.15, abs(lx) * 0.58 + abs(q))
    if abs(d - 1.0) < 0.38 or (abs(lx) < 0.3 and abs(q) > 1.2):
        return p["red"], p["red_glow"]
    return (0, 0, 0, 0), None


def bladef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)
    return tone(p["white"] if t < 0.85 else p["white_dark"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        if math.hypot(y - 60.4, z + 15.5) < 1.1:
            return (p["pupil"] if math.hypot(y - 60.4, z + 15.8) < 0.45 else p["eye"]), None
        if abs(y - 59.2 + 0.12 * (z + 12)) < 0.35 and z > -14:
            return p["red"], p["red_glow"]                             # a red stripe back from the eye
    if face == "down":
        return p["mouth"], None                                        # the roof of its open mouth
    if face in ("east", "west") and y < 57.8 and int(z * 1.4) % 2 == 0 and z < -10:
        return p["teeth"], None
    return tone(p["white"], face), None


def jawf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        return (p["teeth"] if abs(abs(x) - 2.0) < 0.5 and int(z * 1.4) % 2 == 0 else p["mouth"]), None
    return tone(p["white"], face), None


def build() -> Model:
    m = Model("rayquaza_cobbleeffortian")
    top = m.bone("rayquaza", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 6))
    pts = path()
    n_coil = sum(1 for _, _, part in pts if part == "coil")
    # bones: the coils in four, the neck in two, each child of the one before, so the whole body ripples
    cuts = [0, n_coil // 4, n_coil // 2, 3 * n_coil // 4, n_coil - 1, n_coil + 2]
    names = ["coil_1", "coil_2", "coil_3", "coil_4", "neck_1", "neck_2"]
    bone_of, parent = {}, bd
    for nm, c in zip(names, cuts):
        parent = m.bone(nm, parent, pts[c][0])
        bone_of[c] = parent
    cur = bone_of[0]
    for i, ((a, ta, part), (b, tb, part_b)) in enumerate(zip(pts, pts[1:])):
        cur = bone_of.get(i, cur)
        t = (ta + tb) / 2
        if part_b == "coil":
            rod(m, cur, a, b, round(t), coilf, extend=1.2)
            if i % 3 == 1 and t > 4:                                   # red-rimmed hexagonal fins on its coils
                cx, cy, cz = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + t / 2 - 0.5, (a[2] + b[2]) / 2)
                _, ry = aim((b[0] - a[0], 0, b[2] - a[2]))
                m.box(cur, cx, cy, cz - 2.6, cx, cy + 5, cz + 2.6, hexfinf, rotation=(0, ry, 0), pivot=(cx, cy, cz))
        else:
            rod(m, cur, a, b, round(t), neckf(fire=i == n_coil), extend=1.2)
    neck_2 = bone_of[n_coil + 2]
    n1 = bone_of[n_coil - 1]

    # long white blades fanning back from its shoulders
    mn = m.bone("mane", n1, (0, 44, 1))
    for j, (bx, by, dx) in enumerate(((0, 40, 0.0), (-1.5, 43, -0.35), (1.5, 43, 0.35), (-1, 47, -0.2), (1, 47, 0.2))):
        base = (bx, by, 2.5)
        d = (dx, 0.75, 1.0)
        L = 15 if j == 0 else 18
        n = math.sqrt(sum(v * v for v in d))
        mid = tuple(b + v / n * L * 0.65 for b, v in zip(base, d))
        tip = tuple(b + v / n * L for b, v in zip(base, d))
        rod(m, mn, base, mid, 1, bladef, extend=0.5, t2=3)
        rod(m, mn, mid, tip, 1, bladef, extend=0.3, t2=1.5)

    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                 # small red arms with hooked claws
        a = m.bone(nm, n1, (sx * 3, 41, -2.5))
        rod(m, a, (sx * 3, 41, -2.5), (sx * 5, 37.5, -5.5), 1.5, solid("claw"))
        for cz in (-0.6, 0.6):
            spike(m, a, (sx * 5, 37.5, -5.5 + cz), (sx * 0.2, -1, -0.6), 1, 2.5, solid("claw"))

    hd = m.bone("head", neck_2, (0, 57, -7))
    m.round_box(hd, 0, -13, 3.2, 6.5, 57.5, 62.5, headf, cut=1)           # the long head
    m.box(hd, -2.4, 58, -24, 2.4, 61.5, -18, headf)                       # the snout
    jw = m.bone("jaw", hd, (0, 57.5, -8))
    m.box(jw, -2.2, 55, -22.5, 2.2, 57.5, -8, jawf, rotation=(22, 0, 0), pivot=(0, 57.5, -8))   # roaring, jaw open
    for sx in (-1, 1):                                                    # red-trimmed white crest plates
        rod(m, hd, (sx * 2.6, 61.5, -10), (sx * 5, 64, -2), 1, solid("red", glow=True), extend=0.4, t2=2)
        spike(m, hd, (sx * 2, 62.5, -16), (sx * 0.3, 0.5, 1), 1, 5, solid("white"))   # little horns back
    # two red ribbons of hexagonal links streaming from the back of its head
    for sx, nm in ((1, "ribbon_left"), (-1, "ribbon_right")):
        rb = m.bone(nm, hd, (sx * 1.5, 62, -6))
        rp = [(sx * 1.5, 62, -6), (sx * 3, 66, -2), (sx * 5, 70, 4), (sx * 8, 70.5, 10), (sx * 11, 68, 15),
              (sx * 14, 63, 18)]
        for a, b in zip(rp, rp[1:]):
            rod(m, rb, a, b, 3, ribbonf, extend=0.3, t2=0)
    return m
