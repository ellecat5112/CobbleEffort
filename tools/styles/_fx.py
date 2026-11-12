"""
Shared plumbing for numpy-painted collections (Deep Sea, Stained Glass, Steampunk): the setup every look needs and a
generic make(): a look's painter returns the body image plus what glows (strength and colour per pixel), and the
emissive layer is drawn from that, frame by frame (an `animate(glow, frame, ctx)` hook can vary it).
"""
from __future__ import annotations

import numpy as np
from PIL import Image

from ._animatronic import Face
from ._cosmic import arrays, height_map
from ._festive import digest


class Ctx:
    """Everything a painter needs about one texture."""

    def __init__(self, base, eyes_img, seed, shiny, hints, heights, frame=0):
        self.base, self.a, self.alpha, self.eye, self.lum = arrays(base, eyes_img)
        self.h, self.w = self.alpha.shape
        self.s = max(1, self.w // 64)
        geo_w = (hints or {}).get("tex_size", (None,))[0] if hints else None
        self.u = max(1, int(round(self.w / geo_w))) if geo_w else self.s     # texture pixels per model unit
        self.rng = np.random.default_rng(seed)
        self.seed, self.shiny, self.hints, self.frame = seed, shiny, hints, frame
        self.face = Face(self.eye.tolist(), self.alpha.astype(np.uint8).tolist(), self.w, self.h, hints)
        self.hm = height_map(heights, self.h, self.w)
        self.yy, self.xx = np.mgrid[0:self.h, 0:self.w].astype(np.float32)
        self.glow = np.zeros((self.h, self.w), np.float32)                  # 0..1
        self.glow_rgb = np.zeros((self.h, self.w, 3), np.float32)
        self.extra = {}

    def shine(self, mask, colour, strength=1.0):
        """Mark pixels to glow in the emissive layer."""
        m = mask.astype(np.float32) * strength if mask.dtype == bool else np.clip(mask, 0, 1) * strength
        upd = m > self.glow
        self.glow = np.where(upd, m, self.glow)
        col = np.broadcast_to(np.asarray(colour, np.float32), self.glow_rgb.shape)
        self.glow_rgb = np.where(upd[..., None], col, self.glow_rgb)


def image(rgb, ctx):
    out = np.zeros((ctx.h, ctx.w, 4), np.uint8)
    out[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    out[..., 3] = ctx.a[..., 3].astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def make(painter, look, animate=None, layer_alpha=210):
    """painter(look, ctx) -> rgb array; sets ctx.glow / ctx.glow_rgb. Cached per texture (and frame for FRAMES)."""
    cache = {}

    def plan(base, eyes_img, seed, shiny, hints, heights, frame=0):
        key = (digest(base), digest(eyes_img), seed, shiny, repr(hints),
               None if heights is None else heights.tobytes()[:64], frame)
        if key not in cache:
            cache.clear()
            ctx = Ctx(base, eyes_img, seed, shiny, hints, heights, frame)
            rgb = painter(look, ctx)
            cache[key] = (image(rgb, ctx), ctx)
        return cache[key]

    def retexture(base, eyes_img, seed, shiny, frame: int = 0, layer=False, hints=None, heights=None):
        if layer:
            return base.convert("RGBA").copy()
        return plan(base, eyes_img, seed, shiny, hints, heights, frame)[0].copy()

    def extra_layer(name, base, eyes_img, seed, shiny, frame, hints=None, heights=None):
        img, ctx = plan(base, eyes_img, seed, shiny, hints, heights, 0)
        g = animate(ctx.glow, frame, ctx) if animate else ctx.glow
        out = np.zeros((ctx.h, ctx.w, 4), np.float32)
        out[..., :3] = ctx.glow_rgb
        out[..., 3] = np.clip(g, 0, 1) * layer_alpha
        out[~ctx.alpha, 3] = 0
        if not (out[..., 3] > 0).any():
            return None
        return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")

    return retexture, extra_layer
