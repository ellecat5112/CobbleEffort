"""
Halloween collection look: "Nightmare".

* colour drained and darkened, mottled with bruise-purple and rot-green, grime along every edge
* swollen bruised lumps, torn patches of raw flesh, some crudely stitched shut
* blood splatters with drips running down; a drop creeps further each frame
* LOTS of extra, misplaced eyes: bloodshot, with darting pupils, some blinking, some weeping blood
* the Pokémon's real eyes turn blood red, and a misplaced copy of them grows elsewhere on the body
* mouths full of jagged, yellowed, bloody teeth that open and gnash (4-frame animation)
* shiny: "pale corpse": cold grey-blue skin, so the blood stands out more
* glowing (emissive) parts turn into a sickly ghost-green glow
"""
from __future__ import annotations

import colorsys
import hashlib
import random

from PIL import Image

from . import _horror as H

EMISSIVE = "retexture"
FRAMES = len(H.GNASH)
FPS = 5

BRUISE = (74, 30, 72)
ROT = (62, 78, 34)
GRIME = (14, 8, 6)
REAL_EYE = (208, 22, 22)
REAL_EYE_EDGE = (90, 0, 4)

_cache: dict = {}


def _digest(img: Image.Image | None) -> str:
    return "" if img is None else hashlib.md5(img.convert("RGBA").tobytes()).hexdigest()


def _skin(r, g, b, shiny: bool, bruise: float, rot: float):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if shiny:   # pale corpse
        cr, cg, cb = colorsys.hls_to_rgb(h, l * 0.42 + 0.40, s * 0.16)
        c = H.mix((cr * 255, cg * 255, cb * 255), (150, 162, 176), 0.35)
    else:
        cr, cg, cb = colorsys.hls_to_rgb(h, l * 0.55 + 0.04, s * 0.42)
        c = (cr * 255, cg * 255, cb * 255)
    c = H.mix(c, BRUISE, max(0.0, bruise - 0.55) * 1.4)
    c = H.mix(c, ROT, max(0.0, rot - 0.6) * 1.5)
    return c


def _ghost_glow(base: Image.Image) -> Image.Image:
    """Only the genuinely glowing pixels survive, as a sickly green; everything else goes transparent.

    Some Pokémon (e.g. Shinx) use a full-body copy as their glow layer. Drawn on top, that would hide every
    eye and mouth on the body, so dim pixels are dropped and the body shows through.
    """
    base = base.convert("RGBA")
    out = Image.new("RGBA", base.size)
    s, o = base.load(), out.load()
    w, h = base.size
    coverage = sum(1 for y in range(h) for x in range(w) if s[x, y][3]) / (w * h)
    full_body = coverage >= 0.10      # a glow copy of the whole body: keep only its hottest spots
    for y in range(h):
        for x in range(w):
            r, g, b, a = s[x, y]
            _, l, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            v = max(r, g, b) / 255
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            keep = lum > 0.82 if full_body else v > 0.6 and (sat > 0.45 or l > 0.8)
            o[x, y] = (int(110 * v), int(255 * v), int(80 * v), 255 if full_body else a) if a and keep else (0, 0, 0, 0)
    return out


def _plan(base: Image.Image, eyes: Image.Image | None, seed: int, shiny: bool):
    rng = random.Random(seed)
    base = base.convert("RGBA")
    w, h = base.size
    src = base.load()
    scale = max(1, w // 64)
    units = max(1.0, (w * h) / (64 * 64) / (scale * scale))
    alpha = [[src[x, y][3] for x in range(w)] for y in range(h)]
    eye_mask = H.find_eye_mask(base, eyes)
    bruise = H.value_noise(w, h, max(4, 7 * scale), rng)
    rot = H.value_noise(w, h, max(4, 9 * scale), rng)

    img = Image.new("RGBA", (w, h))
    px = img.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if a == 0:
                px[x, y] = (0, 0, 0, 0)
            else:
                c = _skin(r, g, b, shiny, bruise[y][x], rot[y][x])
                px[x, y] = tuple(int(max(0, min(255, v))) for v in c) + (a,)
    cv = H.Canvas(img, alpha, eye_mask)

    # grime: edges of every painted area go dark
    for y in range(h):
        for x in range(w):
            if alpha[y][x] and not all(cv.opaque(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                cv.put(x, y, H.mix(cv.get(x, y), GRIME, 0.6))

    # real eyes turn blood red, and each one gets misplaced copies elsewhere on the body
    real = [(x, y) for y in range(h) for x in range(w) if eye_mask[y][x]]
    copies = []
    for eye in H.components(real):
        ex, ey = min(p[0] for p in eye), min(p[1] for p in eye)
        for _ in range(2):
            for _ in range(300):
                dx, dy = rng.randrange(w) - ex, rng.randrange(h) - ey
                moved = [(x + dx, y + dy) for x, y in eye]
                if all(cv.opaque(x, y) and not cv.used[y][x] and not eye_mask[y][x] for x, y in moved):
                    copies.append(moved)
                    for x, y in moved:
                        cv.used[y][x] = True
                    break

    mouths = H.plan_mouths(cv, rng, scale, int(min(8, 2 + units)))
    extra_eyes = H.plan_eyes(cv, rng, scale, int(min(26, 6 + 3 * units)))
    for _ in range(int(1 + units)):
        H.lump(cv, rng, scale, BRUISE if rng.random() < 0.6 else ROT)
    for i in range(int(1 + units)):
        H.wound(cv, rng, scale, stitched=i % 2 == 0)
    drips = H.blood_splatter(cv, rng, scale, int(4 + 2 * units))

    return img, cv, scale, real, copies, extra_eyes, mouths, drips


def retexture(base: Image.Image, eyes: Image.Image | None, seed: int, shiny: bool,
              frame: int = 0, layer=False) -> Image.Image:
    if layer == "emissive":
        return _ghost_glow(base)
    key = (_digest(base), _digest(eyes), seed, shiny)
    if key not in _cache:
        _cache.clear()
        _cache[key] = _plan(base, eyes, seed, shiny)
    img, cv0, scale, real, copies, extra_eyes, mouths, drips = _cache[key]
    if layer:   # a plain (non-glowing) layer: same diseased skin, no stamped features
        return img.copy()

    out = img.copy()
    cv = H.Canvas(out, cv0.alpha, cv0.eye)
    cv.used = cv0.used
    H.draw_drips(cv, drips, frame, scale)
    pulse = 0.25 if frame % 2 else 0.0
    for group in [real] + copies:
        for eye in H.components(group):
            cells = set(eye)
            for x, y in eye:
                edge = not all((x + dx, y + dy) in cells for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                cv.put(x, y, REAL_EYE_EDGE if edge else H.mix(REAL_EYE, (255, 90, 80), pulse))
            cx = sorted(p[0] for p in eye)[len(eye) // 2]
            cy = sorted(p[1] for p in eye)[len(eye) // 2]
            for sy in range(scale):
                for sx in range(scale):
                    if (cx + sx, cy + sy) in cells:
                        cv.put(cx + sx, cy + sy, H.PUPIL)
    for e in extra_eyes:
        H.draw_eye(cv, e, frame, scale)
    for m in mouths:
        H.draw_mouth(cv, m, frame, scale)
    return out
