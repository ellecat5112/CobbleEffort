"""
Shared toolkit for the 80s Neon Cyberpunk collection.

Looks (one per line, dealt round-robin):
  synthwave  dark violet with a hot-pink grid and cyan neon outlines
  outrun     a retro sunset from head to toe (yellow, orange, magenta, purple) cut by sunset stripes, pink outlines
  tron       black with cyan circuit traces and nodes, cyan outlines
  vaporwave  pastel pink, teal and lavender, a black-and-white checker floor at the feet, soft pink outlines
  acid       near-black with glitched scanlines in toxic green and purple, green outlines
  chrome     80s chrome: a sky-blue to pink horizon reflection banded down the body, magenta outlines
Every look: neon outlines round every part, glowing visor eyes, and an emissive animated layer (NEON) where the neon
glows, pulses and now and then flickers.
Shiny: the neon colours turned round the colour wheel (pink <-> green, cyan <-> orange...).
"""
from __future__ import annotations

import numpy as np
from PIL import Image

from ._cosmic import arrays, edges, even, height_map, hue_turn_fast, noise, outline, ramp, to_image
from ._festive import digest

NEON = {"name": "neon", "emissive": True, "translucent": True, "frames": 4, "fps": 6}

PINK, CYAN, GREEN, PURPLE, ORANGE = (255, 40, 180), (40, 240, 255), (90, 255, 60), (190, 60, 255), (255, 140, 30)
LOOKS = {   # look -> (outline colour, eye colour, pattern colour)
    "synthwave": (CYAN, PINK, PINK),
    "outrun": (PINK, CYAN, PURPLE),
    "tron": (CYAN, CYAN, CYAN),
    "vaporwave": ((255, 150, 220), (130, 255, 240), (255, 255, 255)),
    "acid": (GREEN, GREEN, PURPLE),
    "chrome": ((255, 60, 200), CYAN, (255, 255, 255)),
}

_cache: dict = {}


def plan(look, base, eyes_img, seed, shiny, hints, heights):
    key = (look, digest(base), digest(eyes_img), seed, shiny, None if heights is None else heights.tobytes()[:64])
    if key in _cache:
        return _cache[key]
    _cache.clear()
    rng = np.random.default_rng(seed)
    base, a, alpha, eye, lum = arrays(base, eyes_img)
    h, w = alpha.shape
    s = max(1, w // 64)
    geo_w = (hints or {}).get("tex_size", (None,))[0] if hints else None
    u = max(1, int(round(w / geo_w))) if geo_w else s          # texture pixels per model unit
    hm = height_map(heights, h, w)
    yy, xx = np.mgrid[0:h, 0:w]
    line_c, eye_c, pat_c = (np.array(c, np.float32) for c in LOOKS[look])
    pattern = np.zeros((h, w), bool)
    if look == "synthwave":
        rgb = ramp(even([(8, 2, 22), (40, 12, 70), (90, 40, 130)]), lum * 0.85)
        pattern = ((xx % (6 * s)) < s) | ((yy % (6 * s)) < s)
    elif look == "outrun":
        sun = ramp(even([(70, 10, 110), (220, 30, 140), (255, 110, 60), (255, 220, 70)]), hm * 0.9 + lum * 0.15)
        stripe_w = np.clip((0.55 - hm) * 10, 0, 4) * s                  # stripes thicken toward the feet
        stripes = (hm < 0.55) & (((yy // max(1, s)) % 5) < (stripe_w / max(1, s)))
        rgb = np.where(stripes[..., None], np.array([30, 6, 50], np.float32), sun)
        pattern = stripes & False
    elif look == "tron":
        rgb = ramp(even([(2, 4, 10), (12, 22, 40), (30, 50, 80)]), lum * 0.8)
        for _ in range(max(8, (w * h) // (90 * s * s))):            # circuit traces: right-angle walks with nodes
            x, y = int(rng.integers(0, w)), int(rng.integers(0, h))
            if not alpha[y, x]:
                continue
            for _seg in range(int(rng.integers(2, 5))):
                dx, dy = [(1, 0), (-1, 0), (0, 1), (0, -1)][int(rng.integers(0, 4))]
                for _ in range(int(rng.integers(3, 9)) * s):
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < w and 0 <= ny < h and alpha[ny, nx]):
                        break
                    x, y = nx, ny
                    pattern[y, x] = True
            pattern[max(0, y - s + 1):y + s, max(0, x - s + 1):x + s] = alpha[max(0, y - s + 1):y + s, max(0, x - s + 1):x + s]
    elif look == "vaporwave":
        rgb = ramp(even([(110, 80, 160), (255, 140, 200), (150, 240, 236), (250, 240, 255)]), lum * 0.85 + 0.1)
        checker = (hm < 0.18) & ((((xx // (2 * s)) + (yy // (2 * s))) % 2) == 0)
        rgb = np.where((hm < 0.18)[..., None], np.where(checker[..., None], np.array([20, 20, 30], np.float32),
                                                        np.array([245, 245, 250], np.float32)), rgb)
    elif look == "acid":
        rgb = ramp(even([(4, 8, 6), (18, 32, 22), (40, 64, 46)]), lum * 0.8)
        rows = rng.random(h) < 0.12
        shift = rng.integers(-3 * s, 3 * s + 1, h)
        src = a[..., :3]
        glitch = np.zeros_like(rgb)
        for y in np.nonzero(rows)[0]:
            glitch[y] = np.roll(src[y], int(shift[y]), axis=0) * 0.35 + (np.array(GREEN if y % 2 else PURPLE) * 0.65)
        pattern = rows[:, None] & alpha & (rng.random((h, w)) < 0.7)
        rgb = np.where(pattern[..., None], glitch, rgb)
    elif look == "chrome":
        sky = ramp(even([(40, 30, 90), (120, 160, 230), (230, 240, 255)]), (hm - 0.5) * 2)
        ground = ramp([(0.0, (230, 80, 160)), (0.12, (110, 36, 96)), (0.5, (40, 14, 56)), (1.0, (16, 6, 26))], (0.5 - hm) * 2)
        chrome = np.where((hm >= 0.5)[..., None], sky, ground)
        horizon = np.abs(hm - 0.5) < 0.02
        rgb = chrome * (0.75 + 0.35 * lum[..., None])
        rgb = np.where(horizon[..., None], np.array([255, 255, 255], np.float32), rgb)
        pattern = horizon
    else:
        rgb = a[..., :3].copy()
    edge = outline(alpha, u, 40 * u * u) & ~eye
    if shiny:
        turn = 0.45
        rgb = hue_turn_fast(rgb, turn)
        line_c, eye_c, pat_c = (hue_turn_fast(c[None, None], turn)[0, 0] for c in (line_c, eye_c, pat_c))
    pattern &= alpha & ~eye & ~edge
    rgb = np.where(pattern[..., None], pat_c * 0.85, rgb)
    rgb = np.where(edge[..., None], line_c * 0.8, rgb)
    rgb = np.where(eye[..., None], eye_c, rgb)
    img = to_image(rgb, a[..., 3].astype(np.uint8))
    flicker_seed = int(rng.integers(0, 2 ** 31))
    _cache[key] = (img, edge, pattern, eye, alpha, line_c, eye_c, pat_c, flicker_seed)
    return _cache[key]


def make(look):
    def retexture(base, eyes_img, seed, shiny, frame: int = 0, layer=False, hints=None, heights=None):
        if layer:
            return base.convert("RGBA").copy()
        return plan(look, base, eyes_img, seed, shiny, hints, heights)[0].copy()

    def extra_layer(name, base, eyes_img, seed, shiny, frame, hints=None, heights=None):
        img, edge, pattern, eye, alpha, line_c, eye_c, pat_c, fseed = plan(look, base, eyes_img, seed, shiny, hints, heights)
        h, w = alpha.shape
        rng = np.random.default_rng(fseed)
        tube = rng.integers(0, 6, (h, w))                     # each pixel belongs to a "tube"; one tube flickers
        pulse = [1.0, 0.85, 0.7, 0.85][frame % 4]
        out = np.zeros((h, w, 4), np.float32)
        lit = edge & ~((tube == frame % 6) & (frame == 2))     # in one frame a tube cuts out
        out[lit, :3] = line_c
        out[lit, 3] = 235 * pulse
        out[pattern, :3] = pat_c
        out[pattern, 3] = 170 * pulse
        out[eye, :3] = eye_c
        out[eye, 3] = 255
        out[~alpha, 3] = 0
        if not (out[..., 3] > 0).any():
            return None
        return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")

    return retexture, extra_layer
