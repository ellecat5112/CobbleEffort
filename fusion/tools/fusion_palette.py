"""Colour designs for fusions, from Pokémon Infinite Fusion's custom sprites (as listed on the Infinite Dex).

The custom sprites are community artists' work: they're only read here, never shipped. What we keep from each one is
how the artist recoloured the two Pokémon: a palette mapping for the head's texture and one for the body's texture,
applied to Cobblemon's own textures at runtime (FusionColours on the client).

Method, per fusion:
  1. Palettes. The Cobblemon textures of head and body (opaque texels) and the fusion sprite (opaque pixels) are each
     reduced to K colour clusters in CIELAB (weighted k-means, deterministic seeding).
  2. Assignment. The head's and the body's clusters together (head share HEAD_SHARE of the mass) are matched to the
     sprite's clusters by entropic optimal transport: lightness differences cost the most, so shading order is kept,
     and hue/chroma differences cost less, so a colour that is still in the sprite keeps itself. Balanced mass means a
     big body colour has to go to a big sprite colour: that is what moves Charmander's orange body to Bulbasaur's teal
     on the Bulbasaur-headed fusion, while its flame stays orange.
  3. Each source cluster takes the Lab colour of the sprite cluster that receives most of its mass. Runtime recolours a
     texel by the soft-weighted shift (target - source) of the clusters near its colour, keeping the texture's detail.

Output entry: K source colours per species (shared, data/species.json) and K target colours each for head and body per
fusion, plus the sprite's artists for the credits.
"""
import json
import os
import sys

import numpy as np
from PIL import Image

K = 8
HEAD_SHARE = 0.4
L_WEIGHT = 1.0
AB_WEIGHT = 0.35
EPS = 60.0


# ---- colour space ----------------------------------------------------------------------------------------------------

def srgb_to_lab(rgb):
    rgb = np.asarray(rgb, dtype=np.float64) / 255.0
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
    xyz = lin @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > (6 / 29) ** 3, np.cbrt(xyz), xyz / (3 * (6 / 29) ** 2) + 4 / 29)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def lab_to_srgb(lab):
    lab = np.asarray(lab, dtype=np.float64)
    fy = (lab[..., 0] + 16) / 116
    fx = fy + lab[..., 1] / 500
    fz = fy - lab[..., 2] / 200
    f = np.stack([fx, fy, fz], -1)
    xyz = np.where(f > 6 / 29, f ** 3, 3 * (6 / 29) ** 2 * (f - 4 / 29)) * np.array([0.95047, 1.0, 1.08883])
    m = np.array([[3.2404542, -1.5371385, -0.4985314], [-0.9692660, 1.8760108, 0.0415560], [0.0556434, -0.2040259, 1.0572252]])
    lin = np.clip(xyz @ m.T, 0, 1)
    rgb = np.where(lin <= 0.0031308, lin * 12.92, 1.055 * lin ** (1 / 2.4) - 0.055)
    return np.clip(np.round(rgb * 255), 0, 255).astype(np.uint8)


# ---- palettes --------------------------------------------------------------------------------------------------------

def opaque_lab(img):
    a = np.asarray(img.convert("RGBA"))
    px = a[a[..., 3] >= 128][:, :3]
    if len(px) == 0:
        return np.zeros((0, 3)), np.zeros(0)
    cols, counts = np.unique(px, axis=0, return_counts=True)
    return srgb_to_lab(cols), counts.astype(np.float64)


def kmeans(points, weights, k=K, iters=30):
    """Weighted k-means, deterministic (farthest-point seeding from the heaviest colour)."""
    n = len(points)
    if n == 0:
        return np.zeros((0, 3)), np.zeros(0)
    k = min(k, n)
    centres = [points[np.argmax(weights)]]
    d = np.full(n, np.inf)
    for _ in range(1, k):
        d = np.minimum(d, ((points - centres[-1]) ** 2).sum(1))
        score = d * np.sqrt(weights)
        if score.max() <= 1e-9:
            break
        centres.append(points[np.argmax(score)])
    c = np.array(centres)
    for _ in range(iters):
        lab = ((points[:, None, :] - c[None]) ** 2).sum(-1).argmin(1)
        new = np.array([np.average(points[lab == j], axis=0, weights=weights[lab == j]) if (lab == j).any() else c[j]
                        for j in range(len(c))])
        if np.allclose(new, c, atol=1e-3):
            break
        c = new
    lab = ((points[:, None, :] - c[None]) ** 2).sum(-1).argmin(1)
    w = np.array([weights[lab == j].sum() for j in range(len(c))])
    keep = w > 0
    return c[keep], w[keep] / w[keep].sum()


def palette(img, k=K):
    pts, w = opaque_lab(img)
    return kmeans(pts, w, k)


def sprite_hist(img):
    """A sprite's colours: [[0xRRGGBB, pixels, outline pixels]] at its native size (Infinite Fusion draws 96 px art 3x).
    Outline pixels touch the outside; Cobblemon textures have no outlines, so they count less."""
    a = np.asarray(img.convert("RGBA"))
    if a.shape[0] == 288 and a.shape[1] == 288:
        a = a[1::3, 1::3]
    op = a[..., 3] >= 128
    pad = np.pad(op, 1)
    edge = op & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    key = (a[..., 0].astype(np.int64) << 16) | (a[..., 1].astype(np.int64) << 8) | a[..., 2]
    cols, inv = np.unique(key[op], return_inverse=True)
    n = np.bincount(inv, minlength=len(cols))
    e = np.bincount(inv, weights=edge[op], minlength=len(cols)).astype(int)
    return [[int(c), int(k), int(x)] for c, k, x in zip(cols, n, e)]


LINE_L = 22.0        # darker, greyish colours are mostly line art
LINE_WEIGHT = 0.25


def sprite_palette(hist, k=K):
    h = np.array(hist, dtype=np.float64).reshape(-1, 3)
    rgb = np.stack([(h[:, 0] // 65536) % 256, (h[:, 0] // 256) % 256, h[:, 0] % 256], -1)
    lab = srgb_to_lab(rgb)
    w = np.maximum(h[:, 1] - h[:, 2], 0) + 0.15 * h[:, 2]
    line = (lab[:, 0] < LINE_L) & (np.hypot(lab[:, 1], lab[:, 2]) < 14)
    w = np.where(line, w * LINE_WEIGHT, w)
    keep = w > 0
    return kmeans(lab[keep], w[keep], k)


# ---- assignment ------------------------------------------------------------------------------------------------------
# Infinite Fusion artists mostly either keep a part's own colours or repaint it in the fusion's scheme. So each part
# (head texture, body texture) is either kept, or repainted by lightness rank: its colours, darkest to lightest by
# share, take the sprite's colours at the same place in the sprite's darkest-to-lightest order (big to big, dark to
# dark, so shading survives). The body repaints into what the head doesn't already explain. The pair whose colours
# best reproduce the sprite wins (a small cost on change keeps a part as it is when that fits as well); small colours
# that are already in the sprite (eyes, flames, whites) always stay.

KEEP = 12.0          # ΔE within which a small source colour is already in the sprite
KEEP_MASS = 0.10     # "small"
NEAR = 22.0          # ΔE within which a sprite colour counts as the head's own
CHANGE_COST = 0.12   # per unit of ΔE moved, against reproducing the sprite
USE_REST = os.environ.get("FUSION_REST", "0") == "1"


def rank_map(src, sw, tgt, tw):
    """Each source colour -> the target colour at its middle place in lightness order, by mass."""
    so, to = np.argsort(src[:, 0]), np.argsort(tgt[:, 0])
    tcum = np.cumsum(tw[to]) / tw.sum()
    scum = np.cumsum(sw[so]) / sw.sum()
    mids = scum - sw[so] / sw.sum() / 2
    out = np.empty_like(src)
    for i, q in zip(so, mids):
        out[i] = tgt[to[min(np.searchsorted(tcum, q), len(to) - 1)]]
    return out


def _de(x, y):
    return np.sqrt(((x[:, None, :] - y[None]) ** 2).sum(-1))


def _keep_small(src, w, tgt, sc):
    d0 = _de(src, sc).min(-1)
    keep = (w < KEEP_MASS) & (d0 < KEEP)
    out = tgt.copy()
    out[keep] = src[keep]
    return out


def assign(head_pal, body_pal, sprite_pal):
    """Targets (Lab) for the head's and the body's clusters."""
    (hc, hw), (bc, bw), (sc, sw) = head_pal, body_pal, sprite_pal
    heads = {"keep": hc.copy(), "repaint": rank_map(hc, hw, sc, sw)}
    best = None
    for hn, ht in heads.items():
        # what the head explains of the sprite, at its share
        dh = _de(sc, ht)
        own = np.minimum(sw, HEAD_SHARE * np.array([hw[dh[j].argmin()] if dh[j].min() < NEAR else 0 for j in range(len(sc))]) * 2)
        rest = np.maximum(sw - own, 0)
        bodies = {"keep": bc.copy(), "repaint": rank_map(bc, bw, sc, sw)}
        if USE_REST and rest.sum() > 0.15:
            bodies["rest"] = rank_map(bc, bw, sc, rest)
        for bn, bt in bodies.items():
            mix_c = np.concatenate([ht, bt])
            mix_w = np.concatenate([hw * HEAD_SHARE, bw * (1 - HEAD_SHARE)])
            d = _de(sc, mix_c)
            fit = (d.min(1) * sw).sum() + (d.min(0) * mix_w).sum()
            change = (np.sqrt(((ht - hc) ** 2).sum(-1)) * hw).sum() * HEAD_SHARE + \
                     (np.sqrt(((bt - bc) ** 2).sum(-1)) * bw).sum() * (1 - HEAD_SHARE)
            score = fit + CHANGE_COST * change
            if best is None or score < best[0]:
                best = (score, ht, bt, hn, bn)
    _, ht, bt, _, _ = best
    return _keep_small(hc, hw, ht, sc), _keep_small(bc, bw, bt, sc)


# ---- recolouring (the same maths FusionColours.java runs) ------------------------------------------------------------

SIGMA = 14.0


def recolour(img, src_lab, tgt_lab):
    a = np.asarray(img.convert("RGBA")).copy()
    lab = srgb_to_lab(a[..., :3])
    d2 = ((lab[..., None, :] - src_lab) ** 2).sum(-1)
    w = np.exp(-(d2 - d2.min(-1, keepdims=True)) / (2 * SIGMA ** 2))
    w /= w.sum(-1, keepdims=True)
    shift = (w[..., None] * (tgt_lab - src_lab)).sum(-2)
    a[..., :3] = lab_to_srgb(lab + shift)
    return Image.fromarray(a)


if __name__ == "__main__":
    head, body, sprite, out = sys.argv[1:5]
    h, b, s = Image.open(head), Image.open(body), Image.open(sprite)
    hp, bp, sp = palette(h), palette(b), sprite_palette(sprite_hist(s))
    ht, bt = assign(hp, bp, sp)
    hr, br = recolour(h, hp[0], ht), recolour(b, bp[0], bt)
    for name, pal, tgt in (("head", hp, ht), ("body", bp, bt)):
        print(name, [(tuple(lab_to_srgb(c)), round(float(w), 2), tuple(lab_to_srgb(t))) for c, w, t in zip(pal[0], pal[1], tgt)])
    print("sprite", [(tuple(lab_to_srgb(c)), round(float(w), 2)) for c, w in zip(*sp)])
    sc = 3
    tiles = [im.convert("RGBA").resize((im.width * sc, im.height * sc), Image.NEAREST) for im in (h, hr, b, br)]
    sheet = Image.new("RGBA", (sum(t.width for t in tiles) + 300, max(max(t.height for t in tiles), 288)), (40, 40, 40, 255))
    x = 0
    for t in tiles:
        sheet.alpha_composite(t, (x, 0))
        x += t.width
    sheet.alpha_composite(s.convert("RGBA"), (x + 6, 0))
    sheet.save(out)
