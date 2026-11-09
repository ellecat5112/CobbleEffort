"""
Type themes: the distorted look of a Pokémon from its NEW types (the chart turns each type into its weakness), placed
on its own model by bone names (head, torso/body, tail*, wing*, arm*/hand*, leg*, ear*). The primary new type gets the
full motif, the secondary an accent. Used by gen1.py for every Gen 1 line (and anything else that wants it).

  fighting  a brawler: bulked-up arms and legs, a red headband with trailing ribbons
  water     sea life: a finned crest along the back, a fluke on the tail (fire turns to anemone-like sea life)
  grass     overgrown: leaves sprouting from the head, fern fronds along the back, moss on the tail
  fire      ablaze: raging animated flames on the head and the tail tip
  ground    earthen: a ridge of rocks along the back, sandstone tail and ears
  psychic   a third eye: a glowing gem on the forehead and a pulsing halo above the head
  electric  a storm: crackling lightning through wings, tail and ears (bolts on the head if it has none)
  dark      shadow: wisps of dark flame rising from the back and the tail
  flying    feathered wings spreading from the back
  fairy     blossom: a crown of petals, petals on the tail
  steel     armour: riveted steel plates on the head and the back
"""
from __future__ import annotations

import math

from _kit import clamp, mix, shade
from _materials import (ELECTRIC, LEAF_RAMP, LIGHT, MOSS_RAMP, PETAL_RAMP, Cutout, Flame, Remap, Rock, Solid, _hash,
                        _iter, _solid_alpha, fern, fin_rays, fin_shape, leaf, midrib, petal, sealife_from_layers)

SKIP_WORDS = ("eye", "pupil", "eyelid", "mouth", "ditto", "tooth", "teeth", "tongue", "brow", "whisker", "claw", "nail")

# --- palettes ----------------------------------------------------------------------------------------------------------
SHADOW = {False: [(214, 190, 255), (150, 96, 230), (84, 40, 150), (34, 18, 56)],
          True: [(255, 206, 214), (230, 90, 120), (140, 30, 70), (50, 14, 30)]}
PSYCHIC = {False: [(255, 236, 250), (255, 130, 206), (226, 64, 164), (90, 24, 74)],
           True: [(230, 255, 250), (110, 240, 220), (40, 170, 170), (20, 60, 70)]}
FIN_RAMP = ([(28, 84, 160), (70, 160, 226), (190, 240, 250)], [(100, 50, 170), (176, 120, 236), (240, 220, 255)])
WING_RAMP = ([(150, 150, 170), (226, 226, 236), (255, 255, 255)], [(150, 130, 90), (230, 206, 150), (255, 246, 220)])
FAIRY_PETALS = ([(214, 120, 180), (255, 214, 238), (255, 255, 255)], [(200, 150, 60), (255, 226, 140), (255, 252, 230)])
BAND = {False: (200, 36, 40), True: (40, 90, 210)}
STEEL = ((168, 172, 188), (196, 176, 120))
SANDSTONE = Remap([(120, 84, 48), (190, 150, 96), (236, 210, 160)], [(110, 70, 60), (180, 120, 100), (230, 190, 170)])
MOSS = Remap(*MOSS_RAMP)


# --- shapes ------------------------------------------------------------------------------------------------------------
def ring(s, t):
    r = math.hypot(s - 0.5, t - 0.5) * 2
    return None if not 0.68 < r < 1.0 else 0.4 + 0.6 * (1 - abs(r - 0.84) / 0.16)


def bolt(s, t):
    """A lightning bolt, zigzagging down."""
    y = 1 - t
    c = 0.5 + 0.28 * (1 if int(y * 4) % 2 else -1) * ((y * 4) % 1 - 0.5) * 2
    w = 0.12 + 0.1 * (1 - y)
    return None if abs(s - c) > w else 1 - abs(s - c) / w * 0.5


def ribbon(s, t):
    if t > 0.82 and abs(s - 0.5) < (t - 0.82) * 2.8:
        return None                                   # the notched end
    return 0.55 + 0.3 * (1 - abs(s - 0.5) * 2)


def wing(side):
    """A feathered wing laid flat, spreading outwards (towards s = 1 on the left wing, s = 0 on the right): a straight
    leading edge at the front, the trailing edge scalloped into feather tips."""
    def shape(s, t):
        o = s if side > 0 else 1 - s
        limit = 0.3 + 0.62 * (1 - o) ** 0.5 + 0.1 * math.sin(o * 26) * o
        if t > limit or o > 0.98:
            return None
        return 0.35 + 0.65 * (1 - t / max(limit, 1e-3)) * 0.7 + 0.25 * (1 - o)
    return shape


def feather_veins(s, t):
    return (s * 9) % 1 < 0.12


# --- materials ---------------------------------------------------------------------------------------------------------
class GlowShape:
    """A shape cut out of a plane (or a whole small box) that glows and pulses: a halo, a gem, a bolt."""

    def __init__(self, layer, palette, shape=None):
        self.layer, self.palette, self.shape = layer, palette, shape

    def paint(self, ctx, rects, size, reskin):
        frames = len(ctx.layers[self.layer])
        p = self.palette[ctx.shiny]
        for face, X, Y, s, t, x, y, w, h in _iter(rects):
            k = self.shape(s, t) if self.shape else 0.6
            if k is None:
                ctx.put(X, Y, (0, 0, 0, 0))
                continue
            ctx.put(X, Y, shade(p[2], 0.9 + 0.2 * k))
            for f in range(frames):
                pulse = 0.5 + 0.5 * math.sin(f / frames * 2 * math.pi)
                ctx.glow(self.layer, f, X, Y, p[0] if k * (0.6 + 0.4 * pulse) > 0.7 else p[1])


class Lightning:
    """Crackling lightning over a part (a reskin keeping its colours): thin glowing zigzags that jump between frames."""

    def __init__(self, layer, palette=ELECTRIC):
        self.layer, self.palette = layer, palette

    def paint(self, ctx, rects, size, reskin):
        frames = len(ctx.layers[self.layer])
        p = self.palette[ctx.shiny]
        for face, X, Y, s, t, x, y, w, h in _iter(rects):
            if ctx.body[X, Y][3] == 0:
                continue
            for f in range(frames):
                zig = abs(((X + f * 3) % 6) - 3 - ((Y + f) % 4 - 2) * 0.7) < 0.6 and _hash(X // 3, Y // 3, f) > 0.45
                if zig:
                    ctx.glow(self.layer, f, X, Y, p[0] if _hash(X, Y, f) > 0.5 else p[1])


class Steel(Solid):
    """Brushed steel with a bright rim and rivets at the corners."""

    def __init__(self):
        super().__init__(STEEL[0], STEEL[1], rim=1.25, noise=0.0)

    def colour(self, ctx, face, s, t, X, Y):
        c = self.c[ctx.shiny]
        f = LIGHT[face] * (1.08 - 0.2 * t if face not in ("up", "down") else 1.05) * (0.97 + 0.06 * ((X + Y) % 3 == 0))
        if (s < 0.18 or s > 0.82) and (t < 0.25 or t > 0.75):
            f *= 0.7                                          # rivets
        return shade(c, f)


class Wrap(Solid):
    """Cloth: a band with a woven texture."""

    def colour(self, ctx, face, s, t, X, Y):
        c = self.c[ctx.shiny]
        return shade(c, LIGHT[face] * (0.92 + 0.12 * ((X + Y) % 2)))


# --- bones -------------------------------------------------------------------------------------------------------------
def _with_cubes(kit):
    return [b["name"] for b in kit.bones if b.get("cubes") and not any(w in b["name"] for w in SKIP_WORDS)]


def _size(kit, name):
    lo, hi = kit.bbox(name)
    return (hi[0] - lo[0]) * (hi[1] - lo[1]) * (hi[2] - lo[2])


def pick(kit, *names):
    for n in names:
        if kit.has(n) and kit.bone(n).get("cubes"):
            return n
    return None


def largest(kit):
    bones = _with_cubes(kit) or [b["name"] for b in kit.bones if b.get("cubes")]
    return max(bones, key=lambda n: _size(kit, n))


HEAD_NOT = ("bulb", "leaf", "crest", "spike", "marking", "gem", "ring", "fur", "quill", "nail", "feather", "tuft")


def head(kit):
    """The head: 'head' itself, else the biggest bone named head_* (head_angle, head_rotation, head_ai...) that isn't
    something on the head (a crest, a gem, a leaf)."""
    if pick(kit, "head"):
        return "head"
    cands = [n for n in _with_cubes(kit) if n.startswith("head") and not any(w in n for w in HEAD_NOT)]
    if cands:
        return max(cands, key=lambda n: _size(kit, n))
    return pick(kit, "face", "skull") or torso(kit)


def torso(kit):
    return pick(kit, "torso", "body", "chest", "torso2", "abdomen", "body_segment", "shell", "upper_body") or largest(kit)


def word(kit, *words):
    """Bones whose name has a part starting with one of these words (arm -> arm_left, arm_left2; not 'charm')."""
    return [n for n in _with_cubes(kit) if any(p.startswith(words) for p in n.split("_"))]


def depth(kit, name):
    return len(kit.chain(name))


def tail_tip(kit):
    tails = [n for n in _with_cubes(kit) if n.startswith("tail")]
    return max(tails, key=lambda n: (depth(kit, n), n)) if tails else None


def box_of(kit, name):
    lo, hi = kit.bbox(name)
    c = [(lo[i] + hi[i]) / 2 for i in range(3)]
    d = [hi[i] - lo[i] for i in range(3)]
    return lo, hi, c, d


def back(kit):
    """Where things grow from the back: (bone, base point, upright?, box size). An upright body (taller than deep, a
    biped) gets them on its back face, a horizontal one along its top."""
    t = torso(kit)
    lo, hi, c, d = box_of(kit, t)
    h = head(kit)
    covered = False
    if h != t:
        hlo, hhi, hc, hd = box_of(kit, h)
        covered = lo[2] - 0.5 <= hc[2] <= hi[2] + 0.5 and hlo[1] >= c[1]   # the head sits on top of the body
    if d[1] > d[2] * 1.1 or covered:
        return t, (c[0], lo[1] + d[1] * 0.45, hi[2] - 0.1), True, d
    return t, (c[0], hi[1] - 0.2, c[2]), False, d


def model_height(kit):
    lo, hi = kit.bbox(*[b["name"] for b in kit.bones if b.get("cubes")])
    return max(1.0, hi[1] - lo[1]), max(1.0, hi[0] - lo[0], hi[2] - lo[2])


# --- motifs ------------------------------------------------------------------------------------------------------------
def fighting(kit, full):
    H, W = model_height(kit)
    if full:
        b = round(max(0.15, min(0.5, H * 0.025)), 2)
        arms = word(kit, "arm", "hand", "forearm", "fist", "shoulder", "bicep")
        legs = word(kit, "leg", "thigh")
        if arms:
            kit.bulk(b, *arms)
        if legs:
            kit.bulk(round(b * 0.6, 2), *legs)
    h = head(kit)
    lo, hi, c, d = box_of(kit, h)
    band_h = max(0.75, d[1] * 0.14)
    y = lo[1] + d[1] * 0.74
    kit.box(h, [lo[0] - 0.3, y, lo[2] - 0.3], [d[0] + 0.6, band_h, d[2] + 0.6], Wrap(BAND[False], BAND[True]))
    if full:
        rib = Cutout(ribbon, [shade(BAND[False], 0.7), BAND[False], shade(BAND[False], 1.3)],
                     [shade(BAND[True], 0.7), BAND[True], shade(BAND[True], 1.3)])
        L = max(3.0, d[1] * 0.9)
        for sx, turn in ((-1, 25), (1, -25)):
            kit.plane(h, (c[0] + sx * d[0] * 0.15, y + band_h * 0.5, hi[2] + 0.3), max(1.5, d[0] * 0.25), L, rib,
                      facing="z", rotation=[-70, turn, 0])


def water(kit, full):
    t, base, upright, d = back(kit)
    fin = Cutout(fin_shape, *FIN_RAMP, veins=fin_rays)
    w = max(2.5, (d[1] if upright else d[2]) * 0.7)
    h = max(2.0, max(d[0], min(d[1], d[2])) * 0.7 * (1 if full else 0.7))
    if upright:
        kit.plane(t, (base[0], base[1] - d[1] * 0.2, base[2] + h * 0.5), w, h, fin, facing="x", rotation=[-70, 0, 0])
    else:
        kit.plane(t, base, w, h, fin, facing="x")
    tip = tail_tip(kit)
    if full and tip:
        lo, hi, c, d = box_of(kit, tip)
        w = max(3.0, max(d[0], d[1]) * 2.2)
        kit.flat(tip, (c[0], c[1], hi[2] + w * 0.35), w, w * 0.7, Cutout(fin_shape, *FIN_RAMP, veins=fin_rays))
    if "fire" in kit.old_types:
        kit.op(sealife_from_layers())
        kit.drop_layers.update({"emissive", "flame", "fire"})


def grass(kit, full):
    h = head(kit)
    lo, hi, c, d = box_of(kit, h)
    lf = Cutout(leaf, *LEAF_RAMP, veins=midrib)
    size = max(2.0, max(d[0], d[2]) * 0.55)
    kit.cross(h, (c[0], hi[1] - 0.1, c[2]), size * 0.6, size, lf, turn=30)
    if full:
        t, base, upright, d = back(kit)
        fr = Cutout(fern, *LEAF_RAMP)
        size = max(3.0, max(d[0], d[1], d[2]) * 0.7)
        for turn in (-28, 28):
            kit.plane(t, base, size * 0.55, size, fr, facing="x", rotation=[-35 if upright else -15, turn, 0])
        tails = [n for n in _with_cubes(kit) if n.startswith("tail")]
        if tails:
            kit.reskin(MOSS, *tails)


def fire(kit, full):
    kit.layer("flames", frames=4, fps=8)
    fl = Flame("flames")
    h = head(kit)
    lo, hi, c, d = box_of(kit, h)
    s = max(2.5, max(d[0], d[2]) * 0.7)
    kit.cross(h, (c[0], hi[1] - 0.2, c[2]), s * 0.7, s * (1.1 if full else 0.8), fl)
    if full:
        tip = tail_tip(kit)
        if tip:
            lo, hi, c, d = box_of(kit, tip)
            s = max(2.5, max(d[0], d[1], d[2]) * 1.2)
            kit.cross(tip, (c[0], hi[1] - 0.2, hi[2] - min(d[2], 1.0) * 0.5), s * 0.7, s, fl)
        else:
            t = torso(kit)
            lo, hi, c, d = box_of(kit, t)
            s = max(2.5, max(d[0], d[2]) * 0.5)
            kit.cross(t, (c[0], hi[1] - 0.2, c[2] + d[2] * 0.2), s * 0.7, s, fl, turn=45)


def ground(kit, full):
    t, base, upright, d = back(kit)
    lo, hi, c, _ = box_of(kit, t)
    # a cluster of small jagged rocks breaking through the hide: (across, along, size, tilt) per rock
    spots = [(-0.22, 0.25, 1.0, 12), (0.2, 0.42, 0.8, -15), (-0.05, 0.62, 0.9, 8), (0.24, 0.8, 0.65, -10),
             (-0.26, 0.85, 0.6, 18)][:5 if full else 2]
    unit = max(1.0, max(d[0], min(d[1], d[2])) * 0.17)
    for a, b, k, tilt in spots:
        w = round(max(1.0, unit * k), 2)
        if upright:
            x, y = c[0] + a * d[0], lo[1] + d[1] * (1.0 - 0.6 * b)
            kit.box(t, [x - w / 2, y - w / 2, hi[2] - w * 0.45], [w, w * 1.3, w], Rock(), rotation=[tilt, 45, tilt])
        else:
            x, z = c[0] + a * d[0], lo[2] + d[2] * b
            kit.box(t, [x - w / 2, hi[1] - w * 0.5, z - w / 2], [w, w * 1.4, w], Rock(), rotation=[tilt, 45, -tilt])
    if full:
        rest = [n for n in _with_cubes(kit) if n.startswith("tail") or n.startswith("ear")]
        if rest:
            kit.reskin(SANDSTONE, *rest)


def psychic(kit, full):
    kit.layer("psychic", frames=4, fps=6)
    h = head(kit)
    lo, hi, c, d = box_of(kit, h)
    g = max(0.75, min(d[0], d[1]) * 0.16)
    kit.box(h, [c[0] - g / 2, lo[1] + d[1] * 0.68, lo[2] - g * 0.6], [g, g, g], GlowShape("psychic", PSYCHIC),
            rotation=[0, 0, 45])
    if full:
        r = max(3.0, max(d[0], d[2]) * 0.9)
        kit.flat(h, (c[0], hi[1] + max(1.5, d[1] * 0.25), c[2]), r, r, GlowShape("psychic", PSYCHIC, ring))


def electric(kit, full):
    kit.layer("storm", frames=4, fps=10)
    parts = word(kit, "wing") + [n for n in _with_cubes(kit) if n.startswith("tail")]
    if full:
        parts += [n for n in _with_cubes(kit) if n.startswith("ear")]
    if parts:
        kit.reskin(Lightning("storm"), *parts)
    if not parts or full:
        h = head(kit)
        lo, hi, c, d = box_of(kit, h)
        s = max(2.0, max(d[0], d[2]) * 0.45)
        kit.cross(h, (c[0], hi[1] - 0.1, c[2]), s * 0.6, s * 1.2, GlowShape("storm", ELECTRIC, bolt), turn=20)


def dark(kit, full):
    kit.layer("shadow", frames=4, fps=6)
    wisp = Flame("shadow", tongues=2.5, palette=SHADOW)
    t, base, upright, d = back(kit)
    s = max(3.0, max(d[0], min(d[1], d[2])) * (0.9 if full else 0.6))
    kit.cross(t, (base[0], base[1], base[2] + (s * 0.3 if upright else 0)), s * 0.8, s * 1.2, wisp, turn=15)
    tip = tail_tip(kit)
    if full and tip:
        lo, hi, c, d = box_of(kit, tip)
        s = max(2.5, max(d[0], d[1], d[2]) * 1.2)
        kit.cross(tip, (c[0], hi[1] - 0.2, hi[2] - min(d[2], 1.0) * 0.5), s * 0.7, s, wisp)


def flying(kit, full):
    t, base, upright, d = back(kit)
    lo, hi, c, _ = box_of(kit, t)
    span = max(3.5, max(d[0], d[1]) * (1.3 if full else 0.8))
    length = max(2.5, min(d[1], d[2]) * 0.8)
    y = lo[1] + d[1] * 0.75 if upright else hi[1] - min(1.0, d[1] * 0.2)
    z = hi[2] if upright else c[2]
    for side in (1, -1):
        x = c[0] + side * span / 2
        kit.flat(t, (x, y, z), span, length, Cutout(wing(side), *WING_RAMP, veins=feather_veins),
                 rotation=[0, 0, side * 45])


def fairy(kit, full):
    h = head(kit)
    lo, hi, c, d = box_of(kit, h)
    p = Cutout(petal, *(FAIRY_PETALS if kit.new_types[0] == "fairy" and "fairy" not in kit.old_types else PETAL_RAMP))
    s = max(3.0, max(d[0], d[2]) * 0.7)
    kit.cross(h, (c[0], hi[1] - 0.2, c[2]), s * 0.8, s, p)
    kit.cross(h, (c[0], hi[1] - 0.2, c[2]), s * 0.8, s * 0.8, p, turn=45)
    tip = tail_tip(kit)
    if full and tip:
        lo, hi, c, d = box_of(kit, tip)
        s = max(2.0, max(d[0], d[1], d[2]) * 1.0)
        kit.cross(tip, (c[0], hi[1] - 0.2, hi[2] - min(d[2], 1.0) * 0.5), s, s, p, turn=20)


def steel(kit, full):
    h = head(kit)
    lo, hi, c, d = box_of(kit, h)
    th = max(0.6, d[1] * 0.12)
    kit.box(h, [lo[0] - 0.25, hi[1] - th * 0.4, lo[2] - 0.25], [d[0] + 0.5, th, d[2] * 0.85 + 0.5], Steel())
    if full:
        t = torso(kit)
        if t != h:
            lo, hi, c, d = box_of(kit, t)
            th = max(0.6, d[1] * 0.12)
            kit.box(t, [lo[0] + d[0] * 0.15, hi[1] - th * 0.4, lo[2] + d[2] * 0.1], [d[0] * 0.7, th, d[2] * 0.8], Steel())


MOTIFS = {"fighting": fighting, "water": water, "grass": grass, "fire": fire, "ground": ground, "psychic": psychic,
          "electric": electric, "dark": dark, "flying": flying, "fairy": fairy, "steel": steel}


def apply(kit, types=None):
    """The full motif of the first new type, an accent of the second."""
    types = list(types or kit.new_types)
    for i, t in enumerate(types[:2]):
        if t in MOTIFS and not (i == 1 and t == types[0]):
            MOTIFS[t](kit, i == 0)
