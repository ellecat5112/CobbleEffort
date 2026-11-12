"""
Toxic Chain collection: Pokemon bound by poisonous chains and mochi (after Pecharunt's Toxic Chain).

Looks (one per line, three lines each):
  chains  dark violet bound round and round with glowing magenta chain links
  mochi   glossy lilac-pink mochi with toxic speckles and glowing magenta spots
  ooze    dark purple with toxic ooze dripping down from the top; the drips run
  sludge  bubbling green-and-purple sludge; the bubbles pop
  venom   near black threaded with glowing purple venom veins that pulse
  haze    lavender wreathed in swirling poison gas
Every look: glowing magenta eyes and an emissive animated layer (TOXIN).
Shiny: the poison turned round the colour wheel.
"""
from __future__ import annotations

import numpy as np

from ._arc import bolts, dilate
from ._cosmic import even, hue_turn_fast, noise, ramp
from ._fx import make as _make

TOXIN = {"name": "toxin", "emissive": True, "translucent": True, "frames": 4, "fps": 5}


def paint(look, c):
    rng, u = c.rng, c.u
    body = c.alpha & ~c.eye
    turn = 0.45 if c.shiny else 0.0
    col = lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], turn)[0, 0] if turn else np.array(rgb, np.float32)
    mottle = noise(c.h, c.w, 5 * u, rng, 2)
    glow_m = np.zeros_like(c.alpha)
    gcol = col((255, 60, 210))
    if look == "chains":
        rgb = ramp(even([col((14, 6, 22)), col((40, 20, 60)), col((80, 50, 110))]), c.lum * 0.5 + mottle * 0.3)
        links = np.zeros_like(c.alpha)
        for h0 in (0.3, 0.55, 0.8):
            band = np.abs(c.hm - h0) < 0.04
            L = 3 * u
            lx = (c.xx % L) - L / 2
            ly = (c.hm - h0) * 60
            even_link = ((c.xx // L) % 2) == 0
            ring = np.abs(np.hypot(lx / (L * 0.5), ly / 1.6) - 0.8) < 0.3
            links |= band & np.where(even_link, ring, np.abs(ly) < 0.5)
        links &= body
        rgb = np.where(links[..., None], col((255, 90, 220)), rgb)
        glow_m = links
    elif look == "mochi":
        rgb = ramp(even([col((150, 90, 170)), col((206, 150, 214)), col((244, 214, 244))]), c.lum * 0.5 + mottle * 0.4)
        gloss = (mottle > 0.72) & body
        rgb = np.where(gloss[..., None], rgb * 0.6 + 255 * 0.4, rgb)
        speck = (rng.random((c.h, c.w)) < 0.02) & body
        rgb = np.where(speck[..., None], col((110, 30, 130)), rgb)
        spots = dilate((rng.random((c.h, c.w)) < 0.006) & body, max(0, u // 2)) & body
        rgb = np.where(spots[..., None], col((255, 80, 220)), rgb)
        glow_m = spots
    elif look == "ooze":
        rgb = ramp(even([col((20, 6, 30)), col((56, 20, 80)), col((96, 50, 130))]), c.lum * 0.5 + mottle * 0.3)
        c.extra["drip_len"] = noise(1, c.w, max(1, u), rng, 1)[0] * 0.5 + 0.1
        m = drips(c, 0)
        rgb = np.where(m[..., None], col((180, 40, 230)) * (0.85 + 0.3 * c.lum[..., None]), rgb)
        glow_m = m
        gcol = col((200, 60, 255))
    elif look == "sludge":
        green, purple = col((80, 150, 40)), col((110, 40, 140))
        rgb = np.where((mottle > 0.5)[..., None], green, purple) * (0.7 + 0.4 * c.lum[..., None])
        c.extra["bubble_seed"] = int(rng.integers(1 << 30))
        glow_m = bubbles(c, 0)
        rgb = np.where(glow_m[..., None], rgb * 0.5 + 180, rgb)
        gcol = col((170, 255, 90))
    elif look == "venom":
        rgb = ramp(even([col((8, 4, 12)), col((26, 14, 34)), col((54, 34, 66))]), c.lum * 0.5 + mottle * 0.3)
        vein = bolts(c, rng, max(3, int(c.alpha.sum() / float(u * u) / 160)), 14, 1.4 * u, jitter=0.45, branch=0.25) & body
        vein = dilate(vein, max(0, u // 3)) & body
        rgb = np.where(vein[..., None], col((190, 60, 240)), rgb)
        glow_m = vein
        gcol = col((200, 70, 255))
    elif look == "haze":
        rgb = ramp(even([col((110, 80, 140)), col((176, 146, 206)), col((226, 210, 240))]), c.lum * 0.5 + mottle * 0.3)
        c.extra["haze"] = noise(c.h, c.w, 6 * u, rng, 3)
        swirl = (np.abs(np.sin(c.extra["haze"] * 14)) < 0.25) & body
        rgb = np.where(swirl[..., None], rgb * 0.7 + col((160, 60, 200)) * 0.3, rgb)
        glow_m = swirl
        gcol = col((210, 120, 255))
    else:
        rgb = c.a[..., :3]
    eye = col((255, 70, 220))
    rgb = np.where(c.eye[..., None], eye, rgb)
    c.shine(c.eye, eye, 1.0)
    c.extra.update(glow_m=glow_m & body, gcol=gcol, look=look)
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def drips(c, frame):
    top = 1 - c.extra["drip_len"][None, :] - frame * 0.03
    return (c.hm > top) & c.alpha & ~c.eye


def bubbles(c, frame):
    rng = np.random.default_rng(c.extra["bubble_seed"] + frame)
    m = np.zeros_like(c.alpha)
    ys, xs = np.nonzero(c.alpha & ~c.eye)
    for _ in range(max(3, int(c.alpha.sum() / float(c.u * c.u) / 80))):
        if len(xs) == 0:
            break
        k = rng.integers(len(xs))
        r = rng.uniform(0.6, 1.3) * c.u
        d = np.hypot(c.xx - xs[k], c.yy - ys[k])
        m |= np.abs(d - r) < max(0.5, 0.35 * c.u)
    return m & c.alpha & ~c.eye


def animate(glow, frame, c):
    g0, rgb0 = c.extra["static"]
    g, grgb = g0.copy(), rgb0.copy()
    look = c.extra["look"]
    if look == "ooze":
        m = drips(c, frame)
    elif look == "sludge":
        m = bubbles(c, frame)
    elif look == "haze":
        m = (np.abs(np.sin(c.extra["haze"] * 14 - frame * np.pi / 2)) < 0.25) & c.alpha & ~c.eye
    else:
        m = c.extra["glow_m"]
    s = {"venom": [1.0, 0.6, 0.35, 0.6][frame % 4], "chains": [0.9, 0.75, 0.6, 0.75][frame % 4]}.get(look, 0.7)
    g = np.where(m, np.maximum(g, s * 0.8), g)
    grgb = np.where(m[..., None], c.extra["gcol"], grgb)
    c.glow_rgb = grgb
    return g


def make(look):
    return _make(paint, look, animate, paint_layers=True)
