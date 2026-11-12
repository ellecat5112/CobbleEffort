"""Hand-built Cobblemon-style models: named bones and boxes placed by hand, like a Blockbench modeller would.

A model is a list of bones (name, parent, pivot) and boxes (bone, corners, optional rotation). Planes are boxes with
zero thickness on one axis (for fins, ears, crests, whiskers: light details, cut out with transparency). Every box is
painted by a *shader*: a function of the texel's position on the model (x, y, z, in model units, front = -z, y up)
and its face, returning a colour (RGB or RGBA) and optionally a glow colour. Patterns written in model space (spots,
rings, stripes) therefore line up across neighbouring boxes and faces. Soft Cobblemon-style shading (lit tops,
gentle darkening down the sides, darker undersides) is baked in afterwards; there is no per-texel noise.

Box UV follows vanilla ModelPart / Cobblemon (the layout in _voxel.paint_box).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from PIL import Image

FACES = ("up", "down", "east", "west", "north", "south")


@dataclass
class Box:
    bone: str
    lo: tuple            # (x0, y0, z0) model units
    size: tuple          # (w, h, d) whole numbers (box UV needs whole texels)
    shader: Callable
    rotation: tuple | None = None
    pivot: tuple | None = None
    uv: tuple = (0, 0)


@dataclass
class Model:
    name: str
    bones: list = field(default_factory=list)       # dicts: name, parent, pivot
    boxes: list = field(default_factory=list)

    def bone(self, name, parent, pivot):
        self.bones.append({"name": name, "parent": parent, "pivot": [float(v) for v in pivot]})
        return name

    def box(self, bone, x0, y0, z0, x1, y1, z1, shader, rotation=None, pivot=None):
        """A box from corner (x0, y0, z0) to (x1, y1, z1); sizes are rounded to whole units."""
        size = tuple(int(round(b - a)) for a, b in ((x0, x1), (y0, y1), (z0, z1)))
        self.boxes.append(Box(bone, (x0, y0, z0), size, shader, rotation, pivot))

    def round_box(self, bone, cx, cz, rx, rz, y0, y1, shader, cut=None):
        """A rounded block (Cobblemon modellers' trick): two crossed boxes, so the corners are cut off. The second
        sits a hair lower so their shared faces don't flicker."""
        cut = max(1, round(min(rx, rz) * 0.3)) if cut is None else cut
        self.box(bone, cx - rx, y0, cz - rz + cut, cx + rx, y1, cz + rz - cut, shader)
        self.box(bone, cx - rx + cut, y0 - 0.05, cz - rz, cx + rx - cut, y1 - 0.05, cz + rz, shader)

    def mirror_x(self, bone, x0, y0, z0, x1, y1, z1, shader, rotation=None, pivot=None, bone_mirror=None):
        """The box and its copy on the other side (x -> -x), e.g. a pair of ears."""
        self.box(bone, x0, y0, z0, x1, y1, z1, shader, rotation, pivot)
        rot = None if rotation is None else (rotation[0], -rotation[1], -rotation[2])
        piv = None if pivot is None else (-pivot[0], pivot[1], pivot[2])
        self.box(bone_mirror or bone, -x1, y0, z0, -x0, y1, z1, shader, rot, piv)

    # --- texture -------------------------------------------------------------------------------------------------

    def layout(self):
        nets = [(2 * (b.size[0] + b.size[2]), b.size[2] + b.size[1]) for b in self.boxes]
        tw = 64
        while True:
            order = sorted(range(len(nets)), key=lambda r: (-nets[r][1], -nets[r][0]))
            x = y = shelf = 0
            pos = [None] * len(nets)
            for r in order:
                w, h = nets[r]
                if x + w > tw:
                    x, y, shelf = 0, y + shelf, 0
                pos[r] = (x, y)
                x += w
                shelf = max(shelf, h)
            if y + shelf <= tw:
                break
            tw *= 2
        for b, p in zip(self.boxes, pos):
            b.uv = p
        return tw, tw

    def paint(self, tw, th, variant=None, k=1):
        """-> (texture, glow texture) as RGBA images. `variant` is passed to every shader (e.g. "shiny"). `k` texels
        per model unit: the image is k times the geo's texture size (UVs are normalised, so detail like faces gets
        sharper without changing the model)."""
        img = np.zeros((th * k, tw * k, 4), np.uint8)
        glow = np.zeros((th * k, tw * k, 4), np.uint8)
        for b in self.boxes:
            x0, y0, z0 = b.lo
            w, h, d = b.size
            x1, y1, z1 = x0 + w, y0 + h, z0 + d
            u, v = b.uv
            spec = {   # face: (texture origin, cols, rows, (r, c) -> model position of the texel's centre)
                "up": ((u + d, v), w, d, lambda r, c: (x0 + c + .5, y1, z1 - r - .5)),
                "down": ((u + d + w, v), w, d, lambda r, c: (x0 + c + .5, y0, z1 - r - .5)),
                "east": ((u, v + d), d, h, lambda r, c: (x0, y1 - r - .5, z1 - c - .5)),
                "west": ((u + d + w, v + d), d, h, lambda r, c: (x1, y1 - r - .5, z0 + c + .5)),
                "north": ((u + d, v + d), w, h, lambda r, c: (x0 + c + .5, y1 - r - .5, z0)),
                "south": ((u + 2 * d + w, v + d), w, h, lambda r, c: (x1 - c - .5, y1 - r - .5, z1)),
            }
            for face, ((fu, fv), cols, rows, at) in spec.items():
                for rk in range(rows * k):
                    for ck in range(cols * k):
                        r, c = rk // k, ck // k
                        p = at((rk + .5) / k - .5, (ck + .5) / k - .5)
                        out = b.shader(*p, face=face, variant=variant, box=b, r=r, c=c, rows=rows, cols=cols)
                        col, g = (out if isinstance(out, tuple) and len(out) == 2 and isinstance(out[0], tuple) else (out, None))
                        if len(col) == 3:
                            col = tuple(col) + (255,)
                        if col[3]:
                            f = shade(face, (rk + .5) / k - .5, rows)
                            col = tuple(max(0, min(255, int(round(ch * f)))) for ch in col[:3]) + (col[3],)
                        img[fv * k + rk, fu * k + ck] = col
                        if g is not None:
                            glow[fv * k + rk, fu * k + ck] = tuple(g) + (255,) if len(g) == 3 else g
        return Image.fromarray(img, "RGBA"), Image.fromarray(glow, "RGBA")

    # --- geometry file -------------------------------------------------------------------------------------------

    def geo(self, tw, th, identifier, extra_bones=()):
        bones = [dict(bn, cubes=[]) for bn in self.bones]
        by = {bn["name"]: bn for bn in bones}
        for b in self.boxes:
            cube = {"origin": [round(v, 3) for v in b.lo], "size": list(b.size), "uv": [int(b.uv[0]), int(b.uv[1])]}
            if b.rotation:
                cube["rotation"] = [float(v) for v in b.rotation]
                cube["pivot"] = [float(v) for v in (b.pivot or b.lo)]
            by[b.bone]["cubes"].append(cube)
        for bn in bones:
            if not bn["cubes"]:
                del bn["cubes"]
        bones += list(extra_bones)
        return {"format_version": "1.12.0", "minecraft:geometry": [{
            "description": {"identifier": identifier, "texture_width": tw, "texture_height": th,
                            "visible_bounds_width": 8, "visible_bounds_height": 8, "visible_bounds_offset": [0, 3, 0]},
            "bones": bones}]}


def shade(face, r, rows):
    """Soft baked light: lit tops, a gentle gradient down the sides, darker undersides."""
    if face == "up":
        return 1.07
    if face == "down":
        return 0.8
    t = r / max(1, rows - 1)
    return 1.03 - 0.12 * t


# --- shader helpers ------------------------------------------------------------------------------------------------

def flat(colour, glow=None):
    """One colour all over."""
    def s(x, y, z, **k):
        return (tuple(colour), glow) if glow else tuple(colour)
    return s


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))


def hue_shift(rgb, amount):
    import colorsys
    r, g, b = (v / 255 for v in rgb[:3])
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb((h + amount) % 1.0, l, s)
    return tuple(int(round(v * 255)) for v in (r, g, b)) + tuple(rgb[3:])


def shiny_aware(shader, amount):
    """Wrap a shader so the shiny variant is its colours (and glow) hue-shifted by `amount` turns."""
    def s(*a, variant=None, **k):
        out = shader(*a, variant=variant, **k)
        if variant != "shiny":
            return out
        if isinstance(out, tuple) and len(out) == 2 and isinstance(out[0], tuple):
            col, g = out
            return hue_shift(col, amount), (hue_shift(g, amount) if g else None)
        return hue_shift(out, amount)
    return s


def dist(p, q):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))


# --- aimed parts: tusks, horns, spikes -----------------------------------------------------------------------------

def aim(d):
    """(rx, ry) that turn a cube's (0, 0, -1) axis to point along d, with Cobblemon's cube rotation (Bedrock x is
    mirrored; X then Y): (0, 0, -1) -> (-sin ry cos rx, -sin rx, -cos ry cos rx)."""
    dx, dy, dz = d
    n = math.sqrt(dx * dx + dy * dy + dz * dz)
    dx, dy, dz = dx / n, dy / n, dz / n
    rx = -math.degrees(math.asin(max(-1.0, min(1.0, dy))))
    ry = math.degrees(math.atan2(-dx, -dz))
    return round(rx, 2), round(ry, 2)


def rod(m, bone, a, b, t, shader, extend=1.0, t2=None):
    """A square box of thickness t (t2 high, if given) from point a to point b, a little longer so joints overlap."""
    L = int(round(dist(a, b) + extend))
    rx, ry = aim(tuple(bb - aa for aa, bb in zip(a, b)))
    h = t if t2 is None else t2
    m.box(bone, a[0] - t / 2, a[1] - h / 2, a[2] - L, a[0] + t / 2, a[1] + h / 2, a[2], shader,
          rotation=(rx, ry, 0), pivot=tuple(a))


def chain(m, bone, pts, ts, shader):
    """Rods through a list of points (thicknesses per segment): tusks, tails, horns."""
    for a, b, t in zip(pts, pts[1:], ts):
        rod(m, bone, a, b, t, shader)


def spike(m, bone, base, d, w, h, shader, tip=None):
    """A spike standing on `base`, pointing along d: a w-wide base box and, with `tip`, a narrower tip box."""
    n = math.sqrt(sum(v * v for v in d))
    u = tuple(v / n for v in d)
    if tip is None:
        rod(m, bone, base, tuple(b + u_ * h for b, u_ in zip(base, u)), w, shader, extend=0)
        return
    h1 = max(1, round(h * 0.6))
    mid = tuple(b + u_ * (h1 - 0.5) for b, u_ in zip(base, u))
    rod(m, bone, base, tuple(b + u_ * h1 for b, u_ in zip(base, u)), w, shader, extend=0)
    rod(m, bone, mid, tuple(mm + u_ * (h - h1 + 0.5) for mm, u_ in zip(mid, u)), tip, shader, extend=0)
