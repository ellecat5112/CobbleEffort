"""
Shared toolkit for the Cosmic Starlight collection: each line is a celestial body. Also the numpy helpers the Neon
collection uses (_neon.py).

Looks (one per line, dealt round-robin):
  nebula         deep-space violets and magentas in drifting gas clouds, teal wisps
  galaxy         midnight blue with pale spiral arms and pink dust swirling round a bright core on the chest
  sun            a burning surface (granulation), dark sunspots, a glowing corona round every edge
  moon           grey regolith with dark maria and cratered rims; shiny: a blood moon
  comet          icy blue with glowing streaks of its tail running back across the body
  black_hole     near-black with a blazing orange accretion ring round the chest and a faint purple lensing rim
  ringed_planet  pastel gas-giant bands from head to toe and a bright ring round the middle
  aurora         a night-blue body with green and pink aurora curtains that ripple
  eclipse        a black disc's body with a white-gold corona blazing round every edge
Every look: stars scattered over the dark parts, glowing eyes, and an emissive animated layer (STARLIGHT) where stars
twinkle and the look's light (corona, ring, aurora, streaks) glows in the dark.
Shiny: the look's colours turned round the colour wheel (the moon turns blood red).
"""
from __future__ import annotations

import colorsys

import numpy as np
from PIL import Image

from ._animatronic import Face
from ._festive import digest
from ._horror import find_eye_mask

STARLIGHT = {"name": "starlight", "emissive": True, "translucent": True, "frames": 4, "fps": 4}


# ---------------------------------------------------------------------------------------------
# numpy helpers (shared with _neon.py)
# ---------------------------------------------------------------------------------------------

def arrays(base, eyes_img):
    base = base.convert("RGBA")
    a = np.asarray(base).astype(np.float32)
    alpha = a[..., 3] > 0
    eye = np.array(find_eye_mask(base, eyes_img), bool) & alpha
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) / 255.0
    return base, a, alpha, eye, lum


def ramp(stops, v):
    """Colour ramp over stops [(pos, (r, g, b)), ...] for an array of values 0..1 -> (..., 3) float array."""
    v = np.clip(v, 0, 1)
    pos = np.array([p for p, _ in stops], np.float32)
    cols = np.array([c for _, c in stops], np.float32)
    out = np.empty(v.shape + (3,), np.float32)
    for ch in range(3):
        out[..., ch] = np.interp(v, pos, cols[:, ch])
    return out


def even(colours):
    return [(i / (len(colours) - 1), c) for i, c in enumerate(colours)]


def noise(h, w, cell, rng, octaves=2):
    """Smooth value noise 0..1 (bilinear upsampling of random grids), a few octaves."""
    out = np.zeros((h, w), np.float32)
    amp, total = 1.0, 0.0
    for o in range(octaves):
        c = max(1, cell >> o)
        g = rng.random((h // c + 2, w // c + 2)).astype(np.float32)
        img = Image.fromarray((g * 255).astype(np.uint8)).resize(((w // c + 2) * c, (h // c + 2) * c), Image.BILINEAR)
        out += np.asarray(img, np.float32)[:h, :w] / 255.0 * amp
        total += amp
        amp *= 0.5
    return out / total


def edges(alpha, width=1):
    """Pixels within `width` of transparency (each painted area's outline)."""
    e = np.zeros_like(alpha)
    cur = alpha.copy()
    for _ in range(width):
        p = np.pad(cur, 1)
        inner = p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
        e |= cur & ~inner
        cur = cur & inner
    return e


def outline(alpha, width=1, min_area=36):
    """Edges of the bigger painted areas only (a model's texture is made of many small faces: outlining all of
    them would cover small ones completely)."""
    from scipy import ndimage
    lab, n = ndimage.label(alpha)
    if n == 0:
        return np.zeros_like(alpha)
    sizes = ndimage.sum(alpha, lab, index=np.arange(1, n + 1))
    big = np.isin(lab, np.nonzero(sizes >= min_area)[0] + 1)
    return edges(big, width) & big


def height_map(heights, h, w):
    """The model's texel heights (0 bottom .. 1 top) at the texture's size; texture rows where unknown."""
    rows = np.repeat((1 - (np.arange(h) + 0.5) / h)[:, None], w, 1).astype(np.float32)
    if heights is None:
        return rows
    gh, gw = heights.shape
    ys = np.minimum(gh - 1, np.arange(h) * gh // h)
    xs = np.minimum(gw - 1, np.arange(w) * gw // w)
    hm = np.asarray(heights, np.float32)[ys][:, xs]
    return np.where(np.isfinite(hm), hm, rows)


def hue_turn(rgb, turn):
    """Rotate an (..., 3) float RGB array's hue by `turn` (0..1)."""
    flat = rgb.reshape(-1, 3) / 255.0
    out = np.empty_like(flat)
    for i, (r, g, b) in enumerate(flat):
        hh, l, s = colorsys.rgb_to_hls(r, g, b)
        out[i] = colorsys.hls_to_rgb((hh + turn) % 1.0, l, s)
    return (out * 255).reshape(rgb.shape)


def hue_turn_fast(rgb, turn):
    """Hue rotation by a matrix (fast; close enough for palettes)."""
    a = turn * 2 * np.pi
    c, s = np.cos(a), np.sin(a)
    k = 1 / 3.0
    sq = np.sqrt(k)
    m = np.array([[c + (1 - c) * k, k * (1 - c) - sq * s, k * (1 - c) + sq * s],
                  [k * (1 - c) + sq * s, c + k * (1 - c), k * (1 - c) - sq * s],
                  [k * (1 - c) - sq * s, k * (1 - c) + sq * s, c + k * (1 - c)]], np.float32)
    return np.clip(rgb @ m.T, 0, 255)


def centre_of(face, alpha):
    """The chest's centre (x, y, radius) in texture pixels, or the biggest area's."""
    if face.torso:
        x, y, w, h = face.torso
        return x + w / 2, y + h / 2, max(3.0, min(w, h) / 2)
    ys, xs = np.nonzero(alpha)
    if len(xs) == 0:
        return 0, 0, 4
    return xs.mean(), ys.mean(), max(4.0, np.sqrt(len(xs)) / 4)


def to_image(rgb, alpha_src):
    out = np.zeros(rgb.shape[:2] + (4,), np.uint8)
    out[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    out[..., 3] = alpha_src
    return Image.fromarray(out, "RGBA")


# ---------------------------------------------------------------------------------------------
# looks
# ---------------------------------------------------------------------------------------------

EYES = {"nebula": (255, 150, 230), "galaxy": (240, 246, 255), "sun": (255, 250, 210), "moon": (190, 220, 255),
        "comet": (150, 240, 255), "black_hole": (255, 170, 60), "ringed_planet": (255, 220, 140),
        "aurora": (140, 255, 170), "eclipse": (255, 255, 240)}

_cache: dict = {}


def plan(look, base, eyes_img, seed, shiny, hints, heights):
    key = (look, digest(base), digest(eyes_img), seed, shiny, repr(hints), None if heights is None else heights.tobytes()[:64])
    if key in _cache:
        return _cache[key]
    _cache.clear()
    rng = np.random.default_rng(seed)
    base, a, alpha, eye, lum = arrays(base, eyes_img)
    h, w = alpha.shape
    s = max(1, w // 64)
    geo_w = (hints or {}).get("tex_size", (None,))[0] if hints else None
    u = max(1, int(round(w / geo_w))) if geo_w else s          # texture pixels per model unit
    face = Face(eye.tolist(), alpha.astype(np.uint8).tolist(), w, h, hints)
    hm = height_map(heights, h, w)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    glow = np.zeros((h, w), np.float32)                     # how much a pixel glows in the layer (0..1)
    glow_rgb = np.zeros((h, w, 3), np.float32)
    edge = edges(alpha, s)
    clouds = noise(h, w, 8 * s, rng, 3)
    fine = noise(h, w, 2 * s, rng, 2)
    if look == "nebula":
        rgb = ramp(even([(8, 6, 28), (54, 16, 96), (170, 50, 160), (250, 140, 220), (255, 230, 250)]),
                   0.15 + lum * 0.45 + clouds * 0.55 - 0.15)
        teal = noise(h, w, 12 * s, rng, 2)
        rgb = np.where((teal > 0.62)[..., None], rgb * 0.5 + np.array([40, 190, 200]) * 0.5, rgb)
    elif look == "galaxy":
        rgb = ramp(even([(6, 8, 30), (22, 30, 80), (60, 70, 140)]), lum * 0.8 + clouds * 0.3)
        cx, cy, r = centre_of(face, alpha)
        dx, dy = xx - cx, yy - cy
        rad = np.sqrt(dx * dx + dy * dy) / max(r * 2.2, 1)
        th = np.arctan2(dy, dx)
        arm = np.cos(2 * (th - 2.6 * np.log(rad + 0.15))) * np.exp(-rad * 0.9)
        arms = np.clip((arm - 0.15) * 1.6, 0, 1) * (0.6 + 0.4 * fine)
        rgb = rgb * (1 - arms[..., None]) + np.array([200, 220, 255]) * arms[..., None]
        dust = np.clip((np.cos(2 * (th - 2.6 * np.log(rad + 0.15)) + 1.3) - 0.8) * 2, 0, 1) * np.exp(-rad)
        rgb = rgb * (1 - 0.5 * dust[..., None]) + np.array([230, 110, 180]) * 0.5 * dust[..., None]
        core = np.exp(-(rad * 4.5) ** 2)
        rgb = rgb * (1 - core[..., None]) + np.array([255, 245, 220]) * core[..., None]
        glow = np.maximum(glow, np.clip(arms * 0.8 + core, 0, 1))
        glow_rgb[:] = (220, 230, 255)
    elif look == "sun":
        gran = noise(h, w, 2 * s, rng, 2)
        rgb = ramp(even([(130, 30, 0), (226, 96, 10), (255, 176, 36), (255, 238, 150)]), 0.25 + lum * 0.35 + gran * 0.5)
        spots = noise(h, w, 10 * s, rng, 1) > 0.82
        rgb = np.where(spots[..., None], rgb * 0.3, rgb)
        corona = outline(alpha, u, 40 * u * u)
        rgb = np.where(corona[..., None], np.array([255, 250, 200], np.float32), rgb)
        glow = np.maximum(glow, corona * 1.0 + (gran > 0.7) * 0.35)
        glow_rgb[:] = (255, 200, 80)
    elif look == "moon":
        maria = noise(h, w, 14 * s, rng, 2)
        v = 0.35 + lum * 0.45 + fine * 0.2 - np.clip(maria - 0.55, 0, 1) * 1.2
        rgb = ramp(even([(40, 40, 46), (110, 110, 118), (178, 178, 184), (232, 232, 236)]), v)
        for _ in range(max(6, (w * h) // (180 * s * s))):            # craters: dark floor, light rim
            cx, cy = rng.integers(0, w), rng.integers(0, h)
            r = rng.integers(2, 5) * s
            d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
            rgb = np.where((d < r - s)[..., None] & alpha[..., None], rgb * 0.72, rgb)
            rim = (d >= r - s) & (d < r)
            rgb = np.where(rim[..., None] & alpha[..., None], np.minimum(rgb * 1.25 + 20, 255), rgb)
        if shiny:                                               # the blood moon
            rgb = rgb * np.array([1.15, 0.45, 0.35]) + np.array([30, 0, 0])
        glow_rgb[:] = (200, 220, 255)
    elif look == "comet":
        rgb = ramp(even([(14, 30, 70), (60, 120, 190), (170, 220, 250), (248, 252, 255)]), 0.2 + lum * 0.6 + clouds * 0.2)
        streak = ((xx + yy * 0.6 + fine * 6 * s) % (9 * s)) < 1.4 * s
        streak &= noise(h, w, 6 * s, rng, 1) > 0.45
        rgb = np.where(streak[..., None], np.array([235, 250, 255], np.float32), rgb)
        glow = np.maximum(glow, streak * 0.9)
        glow_rgb[:] = (170, 235, 255)
    elif look == "black_hole":
        rgb = ramp(even([(3, 2, 6), (20, 14, 30), (50, 38, 66)]), lum * 0.6)
        cx, cy, r = centre_of(face, alpha)
        d = np.sqrt(((xx - cx) / 1.0) ** 2 + ((yy - cy) / 0.45) ** 2) / max(r * 1.1, 1)
        ring = np.clip(1 - np.abs(d - 1.0) / 0.25, 0, 1)
        hot = ramp(even([(120, 20, 0), (255, 120, 10), (255, 220, 120), (255, 255, 230)]), ring * (0.7 + 0.3 * fine))
        rgb = rgb * (1 - ring[..., None]) + hot * ring[..., None]
        rgb = np.where((outline(alpha, u, 40 * u * u) & (ring < 0.2))[..., None], np.array([80, 40, 120], np.float32), rgb)
        glow = np.maximum(glow, ring)
        glow_rgb = hot
    elif look == "ringed_planet":
        bands = hm * 9 + (clouds - 0.5) * 1.6
        idx = np.floor(bands).astype(int) % 5
        pal = np.array([(244, 214, 160), (226, 140, 100), (250, 236, 210), (170, 160, 210), (200, 120, 80)], np.float32)
        rgb = pal[idx] * (0.75 + 0.35 * lum[..., None])
        ring = np.abs(hm - 0.5) < 0.025
        rgb = np.where(ring[..., None], np.array([250, 244, 226], np.float32), rgb)
        glow = np.maximum(glow, ring * 0.9)
        glow_rgb[:] = (255, 236, 190)
    elif look == "aurora":
        rgb = ramp(even([(4, 8, 26), (14, 26, 64), (40, 60, 110)]), lum * 0.8)
        glow_rgb = np.zeros((h, w, 3), np.float32)
        glow_rgb[..., :] = (90, 255, 150)
        glow_rgb = np.where((hm > 0.62)[..., None], np.array([240, 110, 220], np.float32), glow_rgb)
        curtain = np.clip(np.sin(xx / (2.5 * s) + clouds * 6) * 0.5 + 0.5, 0, 1) * np.clip(hm * 1.6 - 0.2, 0, 1)
        rgb = rgb * (1 - 0.65 * curtain[..., None]) + glow_rgb * 0.65 * curtain[..., None]
        glow = np.maximum(glow, curtain * 0.8)
    elif look == "eclipse":
        rgb = ramp(even([(2, 2, 4), (16, 16, 22), (36, 36, 46)]), lum * 0.6)
        corona = outline(alpha, u, 40 * u * u)
        rgb = np.where(corona[..., None], np.array([200, 170, 90], np.float32) * (0.75 + 0.25 * fine[..., None]), rgb)
        glow = np.maximum(glow, corona * 1.0)
        glow_rgb[:] = (255, 240, 190)
    else:
        rgb = a[..., :3]
    # stars over the dark parts (not the sun's surface)
    darkness = 1 - (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]) / 255
    stars = (rng.random((h, w)) < 0.018) & alpha & ~eye & (darkness > 0.55) & (look != "sun")
    star_col = np.array([(255, 255, 255), (200, 220, 255), (255, 240, 200)], np.float32)[rng.integers(0, 3, (h, w))]
    rgb = np.where(stars[..., None], star_col, rgb)
    if shiny and look != "moon":
        rgb = hue_turn_fast(rgb, 0.42)
        glow_rgb = hue_turn_fast(glow_rgb, 0.42)
    eye_col = np.array(EYES[look], np.float32)
    if shiny:
        eye_col = hue_turn_fast(eye_col[None, None], 0.42)[0, 0] if look != "moon" else np.array((255, 90, 70), np.float32)
    rgb = np.where(eye[..., None], eye_col, rgb)
    alpha8 = a[..., 3].astype(np.uint8)
    img = to_image(rgb, alpha8)
    twinkle_seed = int(rng.integers(0, 2 ** 31))
    _cache[key] = (img, glow, glow_rgb, stars, star_col, eye, eye_col, alpha, twinkle_seed, look, clouds)
    return _cache[key]


def make(look):
    def retexture(base, eyes_img, seed, shiny, frame: int = 0, layer=False, hints=None, heights=None):
        if layer:
            return base.convert("RGBA").copy()
        return plan(look, base, eyes_img, seed, shiny, hints, heights)[0].copy()

    def extra_layer(name, base, eyes_img, seed, shiny, frame, hints=None, heights=None):
        img, glow, glow_rgb, stars, star_col, eye, eye_col, alpha, tseed, lk, clouds = plan(look, base, eyes_img, seed, shiny, hints, heights)
        h, w = alpha.shape
        rng = np.random.default_rng(tseed + frame)
        pulse = 0.75 + 0.25 * np.cos(frame * np.pi / 2)
        g = glow * pulse
        if lk == "aurora":                                   # the curtains ripple
            g = glow * (0.55 + 0.45 * np.sin(np.arange(w)[None, :] / 3.0 + frame * 1.6 + clouds * 4))
        out = np.zeros((h, w, 4), np.float32)
        out[..., :3] = glow_rgb
        out[..., 3] = np.clip(g, 0, 1) * 200
        tw = stars & (rng.random((h, w)) < 0.55)              # twinkling stars
        out[tw, :3] = star_col[tw]
        out[tw, 3] = 255
        out[eye, :3] = eye_col
        out[eye, 3] = 255
        out[~alpha, 3] = 0
        if not (out[..., 3] > 0).any():
            return None
        return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")

    return retexture, extra_layer
