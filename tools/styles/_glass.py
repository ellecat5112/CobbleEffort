"""
Stained Glass collection: the Pokémon as a leaded glass window.

The texture is cut into irregular panes (Voronoi cells about six model units across, never crossing a painted
area's edge) with dark lead came between them and round every main part. Each pane is one colour of glass, taken from
the original's colour there and pushed into the look's glass palette, with a soft bevel highlight and a little
streaky texture. The glass glows as if lit from behind (an emissive translucent layer: windows shine in the dark).

Looks (one per line, three lines each):
  cathedral     deep jewel glass: sapphire, ruby, emerald, amber, amethyst
  tiffany       opalescent ambers, greens and honey (Tiffany lamp glass)
  rose_window   blues and reds with gold, as in a rose window
  art_nouveau   soft pastels of the original colours
  grisaille     grey-painted glass with touches of yellow stain
  kaleidoscope  every pane a different bright colour
Eyes: clear glowing glass. Shiny: gold came instead of lead, and the glass turned round the colour wheel.
"""
from __future__ import annotations

import colorsys

import numpy as np

from ._cosmic import hue_turn_fast, noise, outline
from ._fx import make as _make

BACKLIGHT = {"name": "backlight", "emissive": True, "translucent": True}

JEWELS = {
    "cathedral": [(20, 50, 160), (170, 20, 40), (20, 120, 60), (220, 150, 20), (110, 40, 150), (30, 120, 170)],
    "tiffany": [(210, 140, 40), (150, 170, 60), (90, 130, 50), (230, 190, 90), (170, 90, 30), (200, 210, 140)],
    "rose_window": [(30, 60, 170), (20, 30, 120), (180, 20, 40), (230, 180, 40), (60, 110, 200), (140, 20, 50)],
}


def paint(look, c):
    from scipy.spatial import cKDTree
    rng, u = c.rng, c.u
    pts_n = max(6, int(c.alpha.sum() / (36.0 * u * u)))   # panes about six model units across
    ys, xs = np.nonzero(c.alpha)
    pick = rng.choice(len(xs), size=min(pts_n, len(xs)), replace=False) if len(xs) else np.array([], int)
    pts = np.stack([xs[pick], ys[pick]], 1).astype(np.float32) + rng.random((len(pick), 2)) * 0.5
    lab = np.full((c.h, c.w), -1, int)
    if len(pts):
        _, idx = cKDTree(pts).query(np.stack([c.xx[c.alpha], c.yy[c.alpha]], 1))
        lab[c.alpha] = idx
    # lead: between panes, and round the main parts
    p = np.pad(lab, 1, constant_values=-2)
    lead = c.alpha & ((p[1:-1, 2:] != lab) | (p[2:, 1:-1] != lab))
    if u > 1:
        lead |= c.alpha & ((p[1:-1, :-2] != lab) | (p[:-2, 1:-1] != lab))
    lead |= outline(c.alpha, max(1, u // 2), 30 * u * u)
    lead &= ~c.eye
    # each pane's colour
    n = len(pts)
    flat = c.a[..., :3][c.alpha]
    sums = np.zeros((n, 3))
    cnt = np.zeros(n)
    np.add.at(sums, lab[c.alpha], flat)
    np.add.at(cnt, lab[c.alpha], 1)
    mean = sums / np.maximum(cnt, 1)[:, None]
    pane = np.zeros((n, 3), np.float32)
    jewels = np.array(JEWELS.get(look, JEWELS["cathedral"]), np.float32)
    for i, (r, g, b) in enumerate(mean / 255.0):
        hh, l, s = colorsys.rgb_to_hls(r, g, b)
        if look in JEWELS:
            # the nearest jewel by hue (greys pick by the pane's index so whites aren't all one colour)
            jh = np.array([colorsys.rgb_to_hls(*(j / 255.0))[0] for j in jewels])
            k = int(np.argmin(np.minimum(np.abs(jh - hh), 1 - np.abs(jh - hh)))) if s > 0.15 else i % len(jewels)
            col = jewels[k] * (0.8 + 0.4 * l)
        elif look == "art_nouveau":
            col = np.array(colorsys.hls_to_rgb(hh, 0.72, min(1, s * 0.8 + 0.25))) * 255
        elif look == "grisaille":
            v = 110 + 120 * l
            col = np.array([v, v, v * 0.95]) if rng.random() > 0.25 else np.array([235, 190, 70]) * (0.8 + 0.3 * l)
        else:                                             # kaleidoscope
            col = np.array(colorsys.hls_to_rgb(rng.random(), 0.5, 0.95)) * 255
        pane[i] = col
    rgb = np.zeros((c.h, c.w, 3), np.float32)
    rgb[c.alpha] = pane[lab[c.alpha]]
    # glass texture: streaks and a bevel highlight toward each pane's upper left
    streak = noise(c.h, c.w, max(1, u), rng, 1)
    rgb *= (0.88 + 0.22 * streak)[..., None]
    if len(pts):
        off = np.zeros((c.h, c.w, 2), np.float32)
        off[c.alpha] = np.stack([c.xx[c.alpha], c.yy[c.alpha]], 1) - pts[lab[c.alpha]]
        hl = np.clip(1 - np.hypot(off[..., 0] + 0.8 * u, off[..., 1] + 0.8 * u) / (1.6 * u), 0, 1)
        rgb = rgb + hl[..., None] * 60
    if c.shiny:
        rgb = hue_turn_fast(rgb, 0.4)
    came = np.array([210, 170, 60], np.float32) if c.shiny else np.array([30, 30, 34], np.float32)
    rgb = np.where(lead[..., None], came, rgb)
    rgb = np.where(c.eye[..., None], np.array([245, 250, 255], np.float32), rgb)
    glass = c.alpha & ~lead
    c.shine(glass, (0, 0, 0), 0.5)
    c.glow_rgb = np.where(glass[..., None], rgb, c.glow_rgb)
    c.shine(c.eye, (245, 250, 255), 1.0)
    return rgb


def make(look):
    return _make(paint, look, None, layer_alpha=150)
