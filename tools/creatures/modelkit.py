"""
modelkit: build Cobblemon-format Bedrock models in code.

A Model is a tree of bones with cubes. Each cube gets a Paint (base colour plus optional per-face pattern).
On export the cubes are packed into a box-UV texture atlas and painted pixel by pixel with Cobblemon-like
shading: lit tops, darker undersides and sides, a little per-pixel noise and soft edges. The result is a
`.geo.json`, a texture PNG, and helpers for writing `.animation.json` and poser files.

Coordinates are Bedrock's: 1 unit = 1/16 block, +y up, the model faces -z (its front), its right side is -x.
Face names used for painting: front (-z), back (+z), right (-x), left (+x), top (+y), bottom (-y).
Inside a face, (u, v) run left->right and top->bottom as seen from outside that face.
"""
from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from PIL import Image

Colour = tuple[int, int, int]
Pattern = Callable[[str, int, int, int, int], "Colour | None"]


def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))


def shade(c: Colour, f: float) -> Colour:
    return (clamp(c[0] * f), clamp(c[1] * f), clamp(c[2] * f))


def mix(a: Colour, b: Colour, t: float) -> Colour:
    return (clamp(a[0] + (b[0] - a[0]) * t), clamp(a[1] + (b[1] - a[1]) * t), clamp(a[2] + (b[2] - a[2]) * t))


def hexc(s: str) -> Colour:
    s = s.lstrip("#")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


FACE_LIGHT = {"top": 1.10, "front": 1.0, "back": 0.88, "right": 0.9, "left": 0.9, "bottom": 0.72}


@dataclass
class Paint:
    base: Colour
    noise: float = 0.05            # per-pixel brightness jitter
    pattern: Pattern | None = None  # (face, u, v, fw, fh) -> colour override or None
    gradient: float = 0.10         # side faces: lighter at the top, darker at the bottom
    edge: float = 0.08             # darken face borders a little
    emissive: bool = False         # also paint into the glow layer


@dataclass
class Cube:
    bone: str
    origin: tuple
    size: tuple
    paint: Paint
    rotation: tuple | None = None
    pivot: tuple | None = None
    inflate: float = 0.0
    mirror: bool = False
    uv: tuple | None = None


@dataclass
class Bone:
    name: str
    parent: str | None
    pivot: tuple
    rotation: tuple | None = None
    locators: dict = field(default_factory=dict)


class Model:
    def __init__(self, name: str, tex_width: int = 128, seed: int = 0):
        self.name = name
        self.tex_width = tex_width
        self.bones: dict[str, Bone] = {}
        self.cubes: list[Cube] = []
        self.rng = random.Random(seed)

    # ---- building -------------------------------------------------------------------------------
    def bone(self, name, parent=None, pivot=(0, 0, 0), rotation=None):
        assert name not in self.bones, name
        if parent:
            assert parent in self.bones, f"unknown parent {parent}"
        self.bones[name] = Bone(name, parent, tuple(pivot), tuple(rotation) if rotation else None)
        return name

    def locator(self, name, parent, pos):
        """Cobblemon locators are bones called locator_<name> carrying a 'locators' entry."""
        b = self.bone(f"locator_{name}", parent, pos)
        self.bones[b].locators[name] = list(pos)
        return b

    def cube(self, bone, origin, size, paint, rotation=None, pivot=None, inflate=0.0, mirror=False):
        assert bone in self.bones, bone
        size = tuple(int(round(s)) for s in size)
        p = paint if isinstance(paint, Paint) else Paint(paint)
        self.cubes.append(Cube(bone, tuple(origin), size, p, tuple(rotation) if rotation else None,
                               tuple(pivot) if pivot else None, inflate, mirror))

    def box(self, bone, center, size, paint, **kw):
        """Cube by centre instead of corner."""
        cx, cy, cz = center
        w, h, d = size
        self.cube(bone, (cx - w / 2, cy - h / 2, cz - d / 2), size, paint, **kw)

    def chain(self, name, parent, pivot, segments, paint):
        """A curving limb/blade made of connected segments, each a child bone of the previous one.

        segments: [(length, width_x, thickness_z, (rx, ry, rz)), ...]; each segment grows along +y from its
        pivot and is rotated relative to the one before, so the chain bends smoothly.
        Returns the bone names.
        """
        names = []
        px, py, pz = pivot
        prev = parent
        for i, (length, w, t, rot) in enumerate(segments):
            b = self.bone(f"{name}{i if i else ''}", prev, (px, py, pz), rotation=rot)
            self.cube(b, (px - w / 2, py, pz - t / 2), (w, length, t), paint)
            names.append(b)
            prev = b
            py += length
        return names

    def mirror_x(self, bone_map: dict[str, str]):
        """Duplicate cubes of right-side bones onto their left-side twins (x negated)."""
        for c in list(self.cubes):
            if c.bone in bone_map:
                o, s = c.origin, c.size
                rot = (c.rotation[0], -c.rotation[1], -c.rotation[2]) if c.rotation else None
                piv = (-c.pivot[0], c.pivot[1], c.pivot[2]) if c.pivot else None
                self.cubes.append(Cube(bone_map[c.bone], (-(o[0] + s[0]), o[1], o[2]), s, c.paint, rot, piv,
                                       c.inflate, False))

    # ---- export ---------------------------------------------------------------------------------
    def _pack(self):
        """Shelf-pack every cube's box-UV net into the atlas."""
        order = sorted(range(len(self.cubes)), key=lambda i: -(self.cubes[i].size[2] + self.cubes[i].size[1]))
        x = y = shelf = 0
        for i in order:
            w, h, d = self.cubes[i].size
            nw, nh = max(1, 2 * (w + d)), max(1, d + h)
            if x + nw > self.tex_width:
                x, y, shelf = 0, y + shelf, 0
            if nw > self.tex_width:
                raise ValueError(f"cube too wide for atlas: {self.cubes[i]}")
            self.cubes[i].uv = (x, y)
            x += nw
            shelf = max(shelf, nh)
        used = y + shelf
        height = 16
        while height < used:
            height *= 2
        return height

    @staticmethod
    def faces(c: Cube):
        u, v = c.uv
        w, h, d = c.size
        return {
            "top": (u + d, v, w, d),
            "bottom": (u + d + w, v, w, d),
            "right": (u, v + d, d, h),
            "front": (u + d, v + d, w, h),
            "left": (u + d + w, v + d, d, h),
            "back": (u + 2 * d + w, v + d, w, h),
        }

    def _paint(self, height):
        img = Image.new("RGBA", (self.tex_width, height), (0, 0, 0, 0))
        glow = Image.new("RGBA", (self.tex_width, height), (0, 0, 0, 0))
        px, gx = img.load(), glow.load()
        any_glow = False
        for idx, c in enumerate(self.cubes):
            rng = random.Random(idx * 7919 + 17)
            for face, (fx, fy, fw, fh) in self.faces(c).items():
                face_name = face
                if c.mirror and face in ("left", "right"):
                    face_name = "left" if face == "right" else "right"
                for j in range(fh):
                    for i in range(fw):
                        uu = (fw - 1 - i) if c.mirror else i
                        col = None
                        if c.paint.pattern:
                            col = c.paint.pattern(face_name, uu, j, fw, fh)
                        if col is None:
                            col = c.paint.base
                        f = FACE_LIGHT[face]
                        if face in ("front", "back", "left", "right") and fh > 1:
                            f *= 1 + c.paint.gradient * (0.5 - j / (fh - 1))
                        if i in (0, fw - 1) or j in (0, fh - 1):
                            f *= 1 - c.paint.edge
                        f *= 1 + rng.uniform(-c.paint.noise, c.paint.noise)
                        if len(col) == 4:   # a pattern can return RGBA to skip shading (e.g. glowing eyes)
                            out = col[:3]
                        else:
                            out = shade(col, f)
                        X, Y = fx + i, fy + j
                        if 0 <= X < self.tex_width and 0 <= Y < height:
                            px[X, Y] = out + (255,)
                            if c.paint.emissive or len(col) == 4:
                                gx[X, Y] = out + (255,)
                                any_glow = True
        return img, (glow if any_glow else None)

    def export(self, geo_path: Path, tex_path: Path, glow_path: Path | None = None):
        height = self._pack()
        img, glow = self._paint(height)
        bones_out = []
        for b in self.bones.values():
            entry = {"name": b.name}
            if b.parent:
                entry["parent"] = b.parent
            entry["pivot"] = [round(v, 3) for v in b.pivot]
            if b.rotation:
                entry["rotation"] = [round(v, 3) for v in b.rotation]
            if b.locators:
                entry["locators"] = b.locators
            cubes = []
            for c in self.cubes:
                if c.bone != b.name:
                    continue
                cd = {"origin": [round(v, 3) for v in c.origin], "size": list(c.size), "uv": list(c.uv)}
                if c.inflate:
                    cd["inflate"] = c.inflate
                if c.rotation:
                    cd["pivot"] = [round(v, 3) for v in (c.pivot or c.origin)]
                    cd["rotation"] = [round(v, 3) for v in c.rotation]
                if c.mirror:
                    cd["mirror"] = True
                cubes.append(cd)
            if cubes:
                entry["cubes"] = cubes
            bones_out.append(entry)
        ys = [c.origin[1] + c.size[1] for c in self.cubes] + [0]
        xs = [abs(c.origin[0]) + c.size[0] for c in self.cubes] + [1]
        geo = {
            "format_version": "1.12.0",
            "minecraft:geometry": [{
                "description": {
                    "identifier": f"geometry.{self.name}",
                    "texture_width": self.tex_width,
                    "texture_height": height,
                    "visible_bounds_width": round(max(xs) * 2 / 16 + 1, 2),
                    "visible_bounds_height": round(max(ys) / 16 + 1, 2),
                    "visible_bounds_offset": [0, round(max(ys) / 32, 2), 0],
                },
                "bones": bones_out,
            }],
        }
        geo_path.parent.mkdir(parents=True, exist_ok=True)
        geo_path.write_text(json.dumps(geo, indent=1) + "\n")
        tex_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(tex_path, optimize=True)
        if glow is not None and glow_path is not None:
            glow.save(glow_path, optimize=True)
        return geo, img, glow

    def height(self):
        return max(c.origin[1] + c.size[1] for c in self.cubes)


# ---- animation & poser helpers ----------------------------------------------------------------------

def sine(amp, speed, phase=0.0, offset=0.0):
    """MoLang: a sine wave over animation time (degrees per second for speed)."""
    s = f"math.sin(q.anim_time * {speed} + {phase}) * {amp}"
    return f"{offset} + {s}" if offset else s


def write_animations(path: Path, group: str, anims: dict[str, dict]):
    # loops last 24 s; every sine speed used must divide into it (360/speed | 24, e.g. 15, 30, 45, 60, 90, 120, 180, 240)
    """anims: {"ground_idle": {"bone": {"rotation": [..], "position": [..]}}, ...}; all looping."""
    data = {"format_version": "1.8.0", "animations": {}}
    for name, bones in anims.items():
        data["animations"][f"animation.{group}.{name}"] = {"loop": True, "animation_length": 24.0, "bones": bones}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1) + "\n")


def write_poser(path: Path, root: str, group: str, head: str, height_px: float, head_y: float,
                walk: str | None, flies: bool, extra_idle: list[str] | None = None):
    """A Cobblemon JSON poser: standing / walking (+ hover / fly) poses using our bedrock animations."""
    look = f"q.look('{head}', 1, 1, 30, -30, 45, -45)"
    blocks = height_px / 16
    poses = {
        "standing": {"poseName": "standing", "poseTypes": ["STAND", "NONE", "PORTRAIT", "PROFILE"],
                     "animations": [look, f"q.bedrock('{group}', 'ground_idle')"] + (extra_idle or [])},
        "walk": {"poseName": "walk", "poseTypes": ["WALK"],
                 "animations": [look, f"q.bedrock('{group}', 'ground_idle')"] + ([walk] if walk else [])},
    }
    if flies:
        poses["hover"] = {"poseName": "hover", "poseTypes": ["HOVER", "FLOAT"],
                          "animations": [look, f"q.bedrock('{group}', 'air_idle')"]}
        poses["fly"] = {"poseName": "fly", "poseTypes": ["FLY", "SWIM"],
                        "animations": [look, f"q.bedrock('{group}', 'air_fly')"]}
    poser = {
        "portraitScale": round(min(2.6, 18 / max(8.0, height_px * 0.35)), 2),
        "portraitTranslation": [0, round(head_y / 16 * 1.05, 2), 0],
        "profileScale": round(min(1.0, 1.43 / max(0.8, blocks)), 2),
        "profileTranslation": [0, round(0.36 * blocks, 2), 0],
        "rootBone": root,
        "animations": {},
        "poses": poses,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(poser, indent=2) + "\n")
