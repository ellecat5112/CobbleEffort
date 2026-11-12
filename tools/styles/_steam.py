"""
Steampunk collection: the Pokémon as a riveted, gear-driven contraption.

Every look: the body in the look's metal (or leather), cut into riveted plates, a gear on the chest, brass goggles
round the eyes with glowing amber lenses, and furnace vents low on the body that glow and flicker (an emissive layer).
Looks (one per line, three lines each):
  brass      polished brass plates, darker brass seams
  copper     copper plates gone green with verdigris in patches
  iron       dark gunmetal plates with brass rivets
  clockwork  brass with exposed gears that TURN (an animated texture)
  airship    stitched brown leather with brass straps and buckles
  boiler     black iron with pipes and many glowing furnace vents
Shiny: silver and blued steel instead of brass and copper.
"""
from __future__ import annotations

import numpy as np

from ._cosmic import centre_of, even, hue_turn_fast, noise, ramp
from ._fx import make as _make

BOILER = {"name": "boiler", "emissive": True, "translucent": True, "frames": 4, "fps": 6}

METALS = {
    "brass": even([(60, 40, 10), (150, 110, 40), (215, 175, 80), (250, 228, 150)]),
    "copper": even([(60, 24, 10), (150, 70, 36), (210, 120, 70), (245, 180, 130)]),
    "iron": even([(14, 14, 18), (46, 48, 54), (90, 94, 102), (150, 154, 162)]),
    "clockwork": even([(60, 40, 10), (150, 110, 40), (215, 175, 80), (250, 228, 150)]),
    "airship": even([(34, 18, 10), (86, 50, 28), (140, 90, 54), (190, 140, 96)]),
    "boiler": even([(8, 8, 10), (30, 30, 34), (64, 64, 70), (110, 110, 118)]),
}
BRASS = np.array([200, 160, 70], np.float32)


def gear(c, cx, cy, r, teeth, angle):
    """A gear's pixels: rim with teeth, hub, spokes."""
    dx, dy = c.xx - cx, c.yy - cy
    d = np.hypot(dx, dy)
    th = np.arctan2(dy, dx) - angle
    tooth = (np.cos(th * teeth) > 0.2) & (d <= r) & (d > r * 0.78)
    rim = (d <= r * 0.8) & (d > r * 0.62)
    hub = d <= r * 0.22
    spoke = (np.abs(np.sin(th * 3)) * d < r * 0.09) & (d <= r * 0.62)
    return (tooth | rim | hub | spoke) & c.alpha, d <= r


def paint(look, c):
    rng, u = c.rng, c.u
    grain = noise(c.h, c.w, 2 * u, rng, 2)
    rgb = ramp(METALS[look], 0.25 + c.lum * 0.55 + grain * 0.2)
    if look == "copper":
        verd = noise(c.h, c.w, 6 * u, rng, 2) > 0.62
        rgb = np.where(verd[..., None], np.array([70, 170, 140], np.float32) * (0.8 + 0.3 * grain[..., None]), rgb)
    if look == "airship":                                        # stitches and straps
        stitch = ((c.xx // u) % 4 == 0) & ((c.yy // u) % 6 < 1)
        rgb = np.where(stitch[..., None], rgb * 0.6, rgb)
        strap = (np.abs(((c.xx + c.yy) / u) % 14 - 7) < 1.2) & c.alpha
        rgb = np.where(strap[..., None], BRASS * (0.8 + 0.3 * grain[..., None]), rgb)
    # riveted plates
    pw = 6 * u
    seam = (((c.xx % pw) < max(1, u // 2)) | ((c.yy % pw) < max(1, u // 2))) & (look != "airship")
    rgb = np.where(seam[..., None], rgb * 0.55, rgb)
    rivet = (np.hypot((c.xx % pw) - 1.5 * u, (c.yy % pw) - 1.5 * u) <= 0.6 * u) & (look != "airship")
    rcol = BRASS if look in ("iron", "boiler") else np.array([250, 235, 190], np.float32)
    rgb = np.where(rivet[..., None], rcol, rgb)
    # pipes round the body (boiler: several)
    for level in ((0.3, 0.55, 0.75) if look == "boiler" else (0.3,)):
        pipe = (np.abs(c.hm - level) < 0.015) & c.alpha
        rgb = np.where(pipe[..., None], np.array([180, 100, 50], np.float32) * (0.8 + 0.3 * grain[..., None]), rgb)
    # the gear(s) on the chest; clockwork's turn with the texture's frame
    cx, cy, r = centre_of(c.face, c.alpha)
    angle = c.frame * (np.pi / 2 / 10)                            # a tenth of a turn over four frames: teeth step on
    g, disc = gear(c, cx, cy, max(3 * u, r * 0.9), 10, angle)
    gears = [(g, disc)]
    if look == "clockwork":
        for k in range(4):
            gx, gy = rng.integers(0, c.w), rng.integers(0, c.h)
            gears.append(gear(c, gx, gy, (3 + k % 2 * 2) * u, 8, -angle * 1.5 if k % 2 else angle * 1.5))
    for g, disc in gears:
        rgb = np.where((disc & c.alpha)[..., None], rgb * 0.45, rgb)          # the hollow behind
        rgb = np.where(g[..., None], BRASS * (0.85 + 0.3 * grain[..., None]), rgb)
    # goggles: a brass ring round each eye, amber lenses
    from scipy import ndimage
    ring = ndimage.binary_dilation(c.eye, iterations=max(1, u)) & ~c.eye & c.alpha
    rgb = np.where(ring[..., None], BRASS * 1.1, rgb)
    lens = np.array([255, 170, 60], np.float32)
    # furnace vents low on the body
    vents = (c.hm < 0.4) & ((c.yy // u) % 3 == 0) & ((c.xx // (4 * u)) % (2 if look == "boiler" else 5) == 0) & c.alpha
    vents &= ~c.eye & ~ring
    rgb = np.where(vents[..., None], np.array([255, 120, 30], np.float32), rgb)
    if c.shiny:
        warm = np.clip((rgb[..., 0] - rgb[..., 2]) / 120.0, 0, 1)[..., None]   # brass/copper -> silver/blued steel
        grey = rgb.mean(-1, keepdims=True)
        rgb = rgb * (1 - warm) + (grey * np.array([0.85, 0.95, 1.15])) * warm
        lens = hue_turn_fast(lens[None, None], 0.5)[0, 0]
    rgb = np.where(c.eye[..., None], lens, rgb)
    c.shine(vents, (255, 120, 30), 0.95)
    c.shine(c.eye, lens, 1.0)
    return rgb


def animate(glow, frame, c):
    rng = np.random.default_rng(c.seed + 7 * frame)
    return np.where(c.eye, glow, glow * (0.6 + 0.4 * rng.random(glow.shape)))


def make(look):
    return _make(paint, look, animate)
