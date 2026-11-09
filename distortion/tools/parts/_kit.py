"""
The part kit: builds a distorted model from a copy of Cobblemon's (same bones, so Cobblemon's poser and animations
still drive it) by hiding bones, reskinning bones and adding new boxes and planes, each painted with a material.

New cubes get their UVs in an added lower part of the texture (the texture height grows by a power of two), so they
never clash with the original layout; every texture the distorted variations use is padded to match. Materials paint
the body texture and, for glowing parts, animated layers (e.g. flames: emissive + translucent, 4 frames).

Coordinates are Bedrock's (the .geo.json's): x left/right, y up, z back (+z is behind the Pokémon, -z its face).
"""
from __future__ import annotations

import copy
import math
import random

from PIL import Image


def clamp(c):
    return tuple(max(0, min(255, int(round(v)))) for v in c)


def mix(a, b, t):
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))


def shade(c, f):
    return clamp(tuple(v * f for v in c[:3]))


def faces(uv, size):
    """The face rects of a box-UV cube, as vanilla's ModelPart lays them out: name -> (u, v, w, h)."""
    u, v = uv
    sx, sy, sz = (int(math.ceil(s - 1e-6)) for s in size)
    return {"up": (u + sz, v, sx, sz), "down": (u + sz + sx, v, sx, sz),
            "east": (u, v + sz, sz, sy), "north": (u + sz, v + sz, sx, sy),
            "west": (u + sz + sx, v + sz, sz, sy), "south": (u + 2 * sz + sx, v + sz, sx, sy)}


class Ctx:
    """What a material paints into: the body texture, the animated layers, and whether it's the shiny."""

    def __init__(self, body, layers, shiny, rng):
        self.body = body                      # PixelAccess
        self.layers = layers                  # name -> list of PixelAccess (frames)
        self.shiny = shiny
        self.rng = rng

    def put(self, x, y, c):
        self.body[x, y] = c if len(c) == 4 else tuple(c) + (255,)

    def glow(self, name, frame, x, y, c):
        self.layers[name][frame][x, y] = c if len(c) == 4 else tuple(c) + (255,)


class Kit:
    def __init__(self, species, model, geo):
        self.species, self.model = species, model
        self.geo = copy.deepcopy(geo)
        g = self.geo["minecraft:geometry"][0]
        self.desc = g["description"]
        self.bones = g["bones"]
        self.W, self.H = self.desc["texture_width"], self.desc["texture_height"]
        self.cubes = []                       # (cube, material) of new cubes
        self.reskins = []                     # (rects, material, cube size) of existing cubes repainted
        self.layers = {}                      # name -> {"emissive", "translucent", "frames", "fps"}
        self.drop_layers = set()              # original layers the distorted look drops (e.g. "flame")
        self.body_ops = []                    # fn(img, shiny, src_layers) -> img, on the original area
        self._shelf = [0, 0, 0]               # packer: x, y, row height (in the added area)
        self.used = False                     # anything to do for this model
        self.geo_changed = False              # a model copy is needed (else Cobblemon's own model is used)

    # --- bones -------------------------------------------------------------------------------------------------------
    def named(self, *prefixes, contains=None):
        """Bones with cubes whose names start with any of these prefixes (or contain `contains`)."""
        return [b["name"] for b in self.bones if b.get("cubes") and (b["name"].startswith(prefixes) if prefixes else True)
                and (contains is None or contains in b["name"])]

    def op(self, fn):
        """A body op: fn(img, shiny, src_layers) -> img, on the original texture area (e.g. flames to sea life)."""
        self.used = True
        self.body_ops.append(fn)

    def has(self, name):
        return any(b["name"] == name for b in self.bones)

    def bone(self, name):
        for b in self.bones:
            if b["name"] == name:
                return b
        raise KeyError(f"{self.model}: no bone {name}")

    def find(self, *names):
        """The first of these bones the model has."""
        for n in names:
            if self.has(n):
                return n
        raise KeyError(f"{self.model}: none of {names}")

    def children(self, name):
        return [b["name"] for b in self.bones if b.get("parent") == name]

    def descendants(self, name):
        out = []
        for c in self.children(name):
            out += [c] + self.descendants(c)
        return out

    def bbox(self, *names, deep=False):
        """The box around these bones' cubes (with their descendants' if deep): (lo, hi)."""
        bs = list(names) + ([d for n in names for d in self.descendants(n)] if deep else [])
        cs = [c for n in bs for c in self.bone(n).get("cubes", [])]
        if not cs:
            raise KeyError(f"{self.model}: no cubes in {names}")
        lo = [min(c["origin"][i] - c.get("inflate", 0) for c in cs) for i in range(3)]
        hi = [max(c["origin"][i] + c["size"][i] + c.get("inflate", 0) for c in cs) for i in range(3)]
        return lo, hi

    def chain(self, name):
        out = []
        while name:
            b = self.bone(name)
            out.append(b)
            name = b.get("parent")
        return out

    def upright(self, name):
        """The nearest bone up the chain (itself included) with no rotation anywhere above it: parts added there stand
        straight (a rotated parent would tilt them)."""
        for i, b in enumerate(self.chain(name)):
            if not any(any(abs(r) > 1e-6 for r in c.get("rotation", [0, 0, 0])) for c in self.chain(b["name"])):
                return b["name"]
        return self.chain(name)[-1]["name"]

    def _rot(self, p, rot, pivot):
        x, y, z = (p[i] - pivot[i] for i in range(3))
        rx, ry, rz = (math.radians(a) for a in rot)
        x, y = x * math.cos(rz) - y * math.sin(rz), x * math.sin(rz) + y * math.cos(rz)
        x, z = x * math.cos(ry) + z * math.sin(ry), -x * math.sin(ry) + z * math.cos(ry)
        y, z = y * math.cos(rx) - z * math.sin(rx), y * math.sin(rx) + z * math.cos(rx)
        return [x + pivot[0], y + pivot[1], z + pivot[2]]

    def wbox(self, *names, deep=False):
        """Like bbox, but where the cubes really are: through every rotation of their bones (approximate)."""
        bs = list(names) + ([d for n in names for d in self.descendants(n)] if deep else [])
        pts = []
        for n in bs:
            for c in self.bone(n).get("cubes", []):
                o, sz = c["origin"], c["size"]
                for corner in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)):
                    q = [o[i] + sz[i] * corner[i] for i in range(3)]
                    if c.get("rotation"):
                        q = self._rot(q, c["rotation"], c.get("pivot", o))
                    for b in self.chain(n):
                        if b.get("rotation"):
                            q = self._rot(q, b["rotation"], b.get("pivot", [0, 0, 0]))
                    pts.append(q)
        if not pts:
            raise KeyError(f"{self.model}: no cubes in {names}")
        return [min(p[i] for p in pts) for i in range(3)], [max(p[i] for p in pts) for i in range(3)]

    def hide(self, *names, deep=False):
        self.used = self.geo_changed = True
        for n in list(names) + ([d for n in names for d in self.descendants(n)] if deep else []):
            self.bone(n).pop("cubes", None)

    def add_bone(self, name, parent, pivot):
        self.used = self.geo_changed = True
        self.bones.append({"name": name, "parent": parent, "pivot": [float(p) for p in pivot]})
        return name

    # --- new cubes ---------------------------------------------------------------------------------------------------
    def _alloc(self, w, h):
        x, y, rh = self._shelf
        if x + w > self.W:
            x, y, rh = 0, y + rh, 0
        self._shelf = [x + w, y, max(rh, h)]
        return x, self.H + y

    def box(self, bone, origin, size, material, inflate=0.0, rotation=None, pivot=None):
        """A cube in a bone (bedrock origin = its min corner), painted with a material."""
        self.used = self.geo_changed = True
        size = [float(s) for s in size]
        sx, sy, sz = (int(math.ceil(s - 1e-6)) for s in size)
        u, v = self._alloc(2 * (sx + sz), sz + sy)
        cube = {"origin": [float(o) for o in origin], "size": size, "uv": [u, v]}
        if inflate:
            cube["inflate"] = inflate
        if rotation:
            cube["rotation"] = list(rotation)
            cube["pivot"] = list(pivot if pivot else [origin[i] + size[i] / 2 for i in range(3)])
        self.bone(bone).setdefault("cubes", []).append(cube)
        self.cubes.append((cube, material))
        return cube

    def plane(self, bone, base, width, height, material, facing="z", rotation=None):
        """A vertical plane standing on `base` (its bottom centre): facing "z" spans x, facing "x" spans z."""
        x, y, z = base
        if facing == "z":
            return self.box(bone, [x - width / 2, y, z], [width, height, 0], material, rotation=rotation, pivot=[x, y, z])
        return self.box(bone, [x, y, z - width / 2], [0, height, width], material, rotation=rotation, pivot=[x, y, z])

    def cross(self, bone, base, width, height, material, turn=0.0):
        """Two vertical planes crossed (like Cobblemon's flames), standing on `base`, turned by `turn` degrees."""
        rot = [0, turn, 0] if turn else None
        self.plane(bone, base, width, height, material, "z", rotation=rot)
        self.plane(bone, base, width, height, material, "x", rotation=rot)

    def flat(self, bone, centre, width, length, material, rotation=None):
        """A horizontal plane centred on `centre`."""
        x, y, z = centre
        return self.box(bone, [x - width / 2, y, z - length / 2], [width, 0, length], material, rotation=rotation, pivot=[x, y, z])

    def reskin(self, material, *names, deep=False):
        """Repaint these bones' own cubes (their UV areas of the body texture) with a material."""
        self.used = True
        for n in list(names) + ([d for n in names for d in self.descendants(n)] if deep else []):
            for c in self.bone(n).get("cubes", []):
                if isinstance(c.get("uv"), list):
                    self.reskins.append((faces(c["uv"], c["size"]), material, c["size"]))

    def layer(self, name, emissive=True, translucent=True, frames=4, fps=8):
        self.layers[name] = {"emissive": emissive, "translucent": translucent, "frames": frames, "fps": fps}

    # --- output ------------------------------------------------------------------------------------------------------
    def height_factor(self):
        need = self._shelf[1] + self._shelf[2]
        f = 1
        while self.H * (f - 1) < need:
            f *= 2
        return f

    def finish_geo(self, identifier):
        self.desc["identifier"] = identifier
        self.desc["texture_height"] = self.H * self.height_factor()
        return self.geo

    def paint(self, img, shiny, src_layers=None):
        """The body texture (recoloured base, padded) and the animated layers' frames, with every part painted."""
        img = img.convert("RGBA")
        for op in self.body_ops:
            img = op(img, shiny, src_layers or {})
        f = self.height_factor()
        out = Image.new("RGBA", (self.W, self.H * f), (0, 0, 0, 0))
        out.paste(img, (0, 0))
        frames = {n: [Image.new("RGBA", out.size, (0, 0, 0, 0)) for _ in range(cfg["frames"])] for n, cfg in self.layers.items()}
        ctx = Ctx(out.load(), {n: [im.load() for im in fr] for n, fr in frames.items()}, shiny, random.Random(f"{self.model}{shiny}"))
        for rects, material, size in self.reskins:
            material.paint(ctx, rects, size, reskin=True)
        for cube, material in self.cubes:
            material.paint(ctx, faces(cube["uv"], cube["size"]), cube["size"], reskin=False)
        return out, frames
