"""
Paints an ORIGINAL base texture onto a model's UV layout, for family members modelled only by a mod whose art
can't be adapted (e.g. Cobblemon Baby Legends' Xerfawn and Latot, which are All Rights Reserved).

Only the model's cube layout (bone names, box-UV positions and sizes) is read; none of that mod's texture pixels.
The colours come from the evolved form's Cobblemon texture (CC BY-NC 3.0): its main tones are assigned to body
parts by bone name, with simple face shading, then the collection's style is applied on top as usual.
"""
from __future__ import annotations

import random

from PIL import Image


def palette(img: Image.Image, n: int = 6):
    """Main colours of a texture, most common first: [(rgb, share)]."""
    rgba = img.convert("RGBA")
    px = [p[:3] for p in rgba.getdata() if p[3] > 200]
    if not px:
        return [((128, 128, 128), 1.0)]
    strip = Image.new("RGB", (len(px), 1))
    strip.putdata(px)
    q = strip.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    counts = sorted(q.getcolors(), reverse=True)
    return [(tuple(pal[i * 3:i * 3 + 3]), c / len(px)) for c, i in counts]


def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def faces(cube):
    u, v = cube["uv"]
    w, h, d = (abs(int(round(x))) for x in cube["size"])
    return {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h),
            "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + 2 * d + w, v + d, w, h)}


def kind(chain: list[str]) -> str:
    names = " ".join(chain).lower()
    first = chain[0].lower()
    if "eye" in first:
        return "eye"
    if "mouth" in first or "tongue" in first or "teeth" in first:
        return "mouth"
    for k, words in (("accent", ("ear", "tail", "horn", "antler", "wing", "fin", "hair", "crest", "spike", "mane")),
                     ("limb", ("leg", "arm", "foot", "feet", "hand", "paw", "claw", "left", "right", "ll", "rl"))):
        if any(w in first for w in words):
            return k
    if any(w in names for w in ("leg", "arm", "foot", "feet")):
        return "limb"
    return "body"


def paint_layout(geo: dict, colours: Image.Image, seed: int):
    """-> (base texture, eye mask) at the model's texture size."""
    d = geo["description"]
    w, h = d["texture_width"], d["texture_height"]
    parent = {b["name"]: b.get("parent") for b in geo["bones"]}

    def chain(name):
        out = []
        while name:
            out.append(name)
            name = parent.get(name)
        return out

    pal = palette(colours)
    main = pal[0][0]
    others = [c for c, _ in pal[1:]] or [main]
    second = others[0]
    accent = max(others, key=lambda c: max(c) - min(c))          # the most saturated tone
    dark = min((c for c, _ in pal), key=lum)
    light = max((c for c, _ in pal), key=lum)
    tones = {"body": main, "limb": second, "accent": accent, "mouth": dark}

    rng = random.Random(seed)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    eyes = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px, ex = img.load(), eyes.load()
    shade = {"top": 1.12, "bottom": 0.78, "back": 0.9, "left": 0.95, "right": 0.95, "front": 1.0}
    for b in geo["bones"]:
        if b["name"].startswith("locator"):
            continue
        k = kind(chain(b["name"]))
        for cube in b.get("cubes", []):
            if not isinstance(cube.get("uv"), list):
                continue
            for face, (fx, fy, fw, fh) in faces(cube).items():
                for j in range(fh):
                    for i in range(fw):
                        x, y = fx + i, fy + j
                        if not (0 <= x < w and 0 <= y < h):
                            continue
                        if k == "eye" and face == "front":
                            # dark iris, a light catch-light in the upper corner
                            c = light if (i, j) == (0, 0) and fw > 1 and fh > 1 else dark
                            ex[x, y] = (255, 255, 255, 255)
                        else:
                            c = tones["body" if k == "eye" else k]
                            f = shade[face] * (1 + rng.uniform(-0.035, 0.035))
                            if j == fh - 1 and fh > 2:
                                f *= 0.9                        # a soft underside on every face
                            c = tuple(max(0, min(255, int(v * f))) for v in c)
                        px[x, y] = c + (255,)
    return img, eyes
