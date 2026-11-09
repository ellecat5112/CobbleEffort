"""
Distorted parts: new body parts for distorted looks, where they fit (make_assets.py's looks() uses them).

The Charmander line: Fire turns Water, so the flame on the tail becomes a mermaid tail: the flame planes go (and the
flame layer), a flat fluke grows from the tail tip and the tail gets fish scales. The model is a copy of Cobblemon's
(CC BY-NC; the add-on's own namespace, so Cobblemon's poser and animations still drive every bone) with the texture
height doubled: the fin is painted in the new lower half, so it never clashes with the original UV layout, and every
texture the distorted variations use is padded to match.

Each part: {"model": geo id, "geo": the geo JSON, "height": the texture height factor, "drop_layers": layer names,
"paint": fn(img, shiny) -> img for the body texture}.
"""
from __future__ import annotations

import copy
import json
import math

import numpy as np
from PIL import Image

MOD = "cobbleeffort_distortion"

# per species: the last tail bone (the fluke's parent), the flame bones (emptied), the tail bones that get scales,
# and the fluke's size (width across, length back) in model units
TAILS = {
    "charmander": {"folder": "0004_charmander", "tip": "tail3", "flame": ["fire", "fire2"], "scaled": ["tail2", "tail3"],
                   "fluke": (11, 7)},
    "charmeleon": {"folder": "0005_charmeleon", "tip": "tail4", "flame": ["fire"], "scaled": ["tail2", "tail3", "tail4"],
                   "fluke": (13, 8)},
    "charizard": {"folder": "0006_charizard", "tip": "tail5", "flame": ["fire", "fire2"], "scaled": ["tail3", "tail4", "tail5"],
                  "fluke": (18, 12)},
}
# fin colours: centre, edge, rays (the normal look's water blue; the shiny's violet)
FIN = {False: ((80, 214, 226), (28, 104, 168), (170, 244, 250)),
       True: ((206, 156, 255), (110, 70, 186), (240, 214, 255))}
SCALE = {False: ((40, 120, 190), (120, 210, 240)), True: ((120, 80, 200), (220, 190, 255))}


def _bone(bones, name):
    for b in bones:
        if b["name"] == name:
            return b
    raise SystemExit(f"bone {name} missing")


def _fluke_mask(w, l):
    """The fluke's shape on its w x l face: row 0 is the far end (the lobes), the last row meets the tail."""
    m = np.zeros((l, w), bool)
    for row in range(l):
        s = (l - row - 0.5) / l                                  # 0 at the tail, 1 at the far end
        half = 0.22 + 0.78 * s ** 0.55                            # spreading towards the lobes
        notch = 0.0 if s < 0.7 else 0.3 * (s - 0.7) / 0.3        # the V between the two lobes
        for x in range(w):
            xn = abs((x + 0.5) / w * 2 - 1)
            m[row, x] = notch <= xn <= half
    return m


def _paint_fluke(px, u, v, w, l, shiny):
    centre, edge, ray = FIN[shiny]
    mask = _fluke_mask(w, l)
    for slot in (0, 1):                                          # the top face, then the bottom face (same layout)
        ou = u + l + slot * w
        for row in range(l):
            for x in range(w):
                if not mask[row, x]:
                    continue
                inner = (0 < x < w - 1 and 0 < row < l - 1 and mask[row, x - 1] and mask[row, x + 1]
                         and mask[row - 1, x] and mask[row + 1, x])
                xn = (x + 0.5) / w * 2 - 1
                s = (l - row - 0.5) / l
                if not inner:
                    c = edge
                elif abs(math.atan2(xn, s + 0.25) * 4.2) % 1 < 0.22:  # rays fanning out from the tail
                    c = ray
                else:
                    t = min(1.0, (abs(xn) + s) / 1.4)
                    c = tuple(int(centre[i] * (1 - t * 0.35) + edge[i] * t * 0.35) for i in range(3))
                px[ou + x, v + row] = c + (255,)


def _box_regions(cube):
    """Every face rect of a box-UV cube: (u, v, w, h)."""
    u, v = cube["uv"]
    sx, sy, sz = (int(math.ceil(c)) for c in cube["size"])
    return [(u + sz, v, sx, sz), (u + sz + sx, v, sx, sz), (u, v + sz, sz, sy), (u + sz, v + sz, sx, sy),
            (u + sz + sx, v + sz, sz, sy), (u + 2 * sz + sx, v + sz, sx, sy)]


def _paint_scales(px, size, regions, shiny):
    """Fish scales over the tail: a scalloped pattern, each scale lighter in its middle, the body colour kept underneath."""
    dark, light = SCALE[shiny]
    W, H = size
    for (u, v, w, h) in regions:
        for y in range(v, min(H, v + h)):
            for x in range(u, min(W, u + w)):
                r, g, b, a = px[x, y]
                if a == 0:
                    continue
                lx, ly = x - u, y - v
                row = ly // 2
                cx = (lx + (row % 2)) % 3
                outline = (ly % 2 == 1 and cx != 1) or (ly % 2 == 0 and cx == 0)
                c = dark if outline else light
                k = 0.55 if outline else 0.35
                px[x, y] = (int(r * (1 - k) + c[0] * k), int(g * (1 - k) + c[1] * k), int(b * (1 - k) + c[2] * k), a)


def build(sp, cobblemon_zip):
    t = TAILS[sp]
    folder = t["folder"]
    geo = json.loads(cobblemon_zip.read(f"assets/cobblemon/bedrock/pokemon/models/{folder}/{sp}.geo.json"))
    geo = copy.deepcopy(geo)
    g = geo["minecraft:geometry"][0]
    desc = g["description"]
    W, H = desc["texture_width"], desc["texture_height"]
    desc["identifier"] = f"geometry.{sp}_distorted"
    desc["texture_height"] = H * 2
    bones = g["bones"]
    scaled = [c for name in t["scaled"] for c in _bone(bones, name).get("cubes", [])]
    for name in t["flame"]:
        _bone(bones, name).pop("cubes", None)                     # no flame
    tip = _bone(bones, t["tip"])
    tc = tip["cubes"][0]
    y = tc["origin"][1] + tc["size"][1] / 2
    z_end = tc["origin"][2] + tc["size"][2]
    w, l = t["fluke"]
    uv = (0, H)
    bones.append({"name": "distorted_fluke", "parent": t["tip"], "pivot": [0, y, z_end],
                  "cubes": [{"origin": [-w / 2, y, z_end - 1], "size": [w, 0, l], "uv": list(uv)}]})

    def paint(img, shiny):
        img = img.convert("RGBA")
        assert img.size == (W, H), (sp, img.size)
        out = Image.new("RGBA", (W, H * 2), (0, 0, 0, 0))
        out.paste(img, (0, 0))
        px = out.load()
        _paint_scales(px, (W, H), [r for c in scaled for r in _box_regions(c)], shiny)
        _paint_fluke(px, uv[0], uv[1], w, l, shiny)
        return out

    return {"model": f"{MOD}:{sp}_distorted.geo", "file": f"{folder}/{sp}_distorted.geo.json", "geo": geo,
            "height": 2, "drop_layers": ["flame"], "paint": paint}


def pad(img, factor):
    """A layer texture padded to the part model's texture height."""
    img = img.convert("RGBA")
    out = Image.new("RGBA", (img.width, img.height * factor), (0, 0, 0, 0))
    out.paste(img, (0, 0))
    return out
