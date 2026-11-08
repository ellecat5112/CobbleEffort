"""
Shared helpers for turning a triangle mesh (e.g. an OBJ with vertex colours) into a Cobblemon/Bedrock model:
voxelize at one voxel per model unit, quantize the colours to a small palette, merge voxels into boxes per bone,
lay the boxes out in box UV and paint the texture so each face shows the colours of the voxels behind it.

Box-UV face layout (u, v = the cube's uv; w, h, d = size x, y, z), and which way each face's texels run. Cobblemon
builds cubes with vanilla's ModelPart (TexturedModel: x and z kept, y flipped), so this is vanilla's box UV:
    up    (+y) [u+d,     v,   w, d]  col -> x from min, row -> z from max (the bottom row meets the front)
    down  (-y) [u+d+w,   v,   w, d]  col -> x from min, row -> z from max
    east  (-x) [u,       v+d, d, h]  col -> z from max, row -> y from top
    north (-z) [u+d,     v+d, w, h]  col -> x from min, row -> y from top
    west  (+x) [u+d+w,   v+d, d, h]  col -> z from min, row -> y from top
    south (+z) [u+2d+w,  v+d, w, h]  col -> x from max, row -> y from top
"""
from __future__ import annotations

import numpy as np
from PIL import Image


def load_obj(path):
    vs, fs = [], []
    with open(path) as f:
        for line in f:
            if line.startswith("v "):
                vs.append(line[2:].split())
            elif line.startswith("f "):
                fs.append([int(p.split("/")[0]) for p in line[2:].split()])
    V = np.array(vs, dtype=np.float32)
    F = np.array(fs, dtype=np.int64) - 1
    C = V[:, 3:6] if V.shape[1] >= 6 else np.full((len(V), 3), 0.7, np.float32)
    return V[:, :3], C, F


def voxelize(P, C, F, height: float, face_negative_z: bool):
    """Points sampled on every triangle -> occupied voxels (one per model unit) with mean colours; the inside is
    filled. Returns (solid, surface, colours, lo) where voxel (i, j, k) has its min corner at lo + (i, j, k)."""
    from scipy import ndimage
    K = height / (P[:, 1].max() - P[:, 1].min())
    T, TC = P[F], C[F]
    pts = np.concatenate([P, T.mean(1), (T[:, 0] + T[:, 1]) / 2, (T[:, 1] + T[:, 2]) / 2, (T[:, 2] + T[:, 0]) / 2])
    col = np.concatenate([C, TC.mean(1), (TC[:, 0] + TC[:, 1]) / 2, (TC[:, 1] + TC[:, 2]) / 2, (TC[:, 2] + TC[:, 0]) / 2])
    q = pts.copy()
    if face_negative_z:            # Cobblemon models face -z (and the left side is +x): turn 180 degrees about y
        q[:, 0] *= -1
        q[:, 2] *= -1
    q[:, 1] -= P[:, 1].min()
    q *= K
    lo = np.floor(q.min(0)).astype(int)
    lo[1] = 0
    idx = np.clip(np.floor(q).astype(int) - lo, 0, None)
    shape = idx.max(0) + 1
    flat = np.ravel_multi_index(idx.T, shape)
    n = np.bincount(flat, minlength=int(np.prod(shape)))
    csum = np.stack([np.bincount(flat, weights=col[:, i], minlength=int(np.prod(shape))) for i in range(3)], 1)
    surf = (n > 0).reshape(shape)
    colours = (csum / np.maximum(n, 1)[:, None]).reshape(tuple(shape) + (3,))
    outside = ndimage.binary_fill_holes(np.pad(surf, 1)) == 0
    solid = ~outside[1:-1, 1:-1, 1:-1]
    return solid, surf, colours, lo


def quantize(colours, mask, k: int, seed: int = 0, iters: int = 30):
    """k-means on the masked voxel colours -> (palette [k,3] 0-255, label grid)."""
    rng = np.random.default_rng(seed)
    X = colours[mask].reshape(-1, 3) * 255
    cent = X[rng.choice(len(X), k, replace=False)]
    for _ in range(iters):
        lab = np.argmin(((X[:, None] - cent[None]) ** 2).sum(2), 1)
        for c in range(k):
            if (lab == c).any():
                cent[c] = X[lab == c].mean(0)
    labels = np.full(mask.shape, -1, int)
    labels[mask] = lab
    return cent.round().astype(int), labels


def denoise(labels, surf, passes: int = 1):
    """Majority filter over each surface voxel's 3x3x3 surface neighbours (removes speckle)."""
    lab = labels.copy()
    for _ in range(passes):
        new = lab.copy()
        for i, j, k in zip(*np.nonzero(surf)):
            nb = lab[max(0, i - 1):i + 2, max(0, j - 1):j + 2, max(0, k - 1):k + 2]
            nb = nb[nb >= 0]
            vals, cnt = np.unique(nb, return_counts=True)
            cnt[vals == lab[i, j, k]] += 1                   # a slight preference for keeping its own colour
            new[i, j, k] = vals[np.argmax(cnt)]
        lab = new
    return lab


def fill_interior_labels(labels, surf, solid):
    """Give every solid voxel the label of its nearest surface voxel (faces of merged boxes may show them)."""
    from scipy import ndimage
    _, (ii, jj, kk) = ndimage.distance_transform_edt(~surf, return_indices=True)
    out = labels[ii, jj, kk]
    out[~solid] = -1
    return out


def greedy_boxes(mask):
    """Merge a voxel mask into boxes [(i0, j0, k0, i1, j1, k1)] (exclusive ends)."""
    left = mask.copy()
    boxes = []
    X, Y, Z = mask.shape
    for j in range(Y):
        for k in range(Z):
            for i in range(X):
                if not left[i, j, k]:
                    continue
                i1 = i + 1
                while i1 < X and left[i1, j, k]:
                    i1 += 1
                k1 = k + 1
                while k1 < Z and left[i:i1, j, k1].all():
                    k1 += 1
                j1 = j + 1
                while j1 < Y and left[i:i1, j1, k:k1].all():
                    j1 += 1
                left[i:i1, j:j1, k:k1] = False
                boxes.append((i, j, k, i1, j1, k1))
    return boxes


def pack(rects, width: int):
    """Shelf-pack (w, h) rectangles into a texture `width` wide -> positions, used height."""
    order = sorted(range(len(rects)), key=lambda r: (-rects[r][1], -rects[r][0]))
    pos = [None] * len(rects)
    x = y = shelf = 0
    for r in order:
        w, h = rects[r]
        if x + w > width:
            x, y, shelf = 0, y + shelf, 0
        pos[r] = (x, y)
        x += w
        shelf = max(shelf, h)
    return pos, y + shelf


def paint_box(img, uv, box, colour_of):
    """Paint the six box-UV faces of a box (grid coords) using colour_of(i, j, k) for the voxel behind each texel."""
    i0, j0, k0, i1, j1, k1 = box
    w, h, d = i1 - i0, j1 - j0, k1 - k0
    u, v = uv
    px = img.load()
    for c in range(w):
        for r in range(d):
            px[u + d + c, v + r] = colour_of(i0 + c, j1 - 1, k1 - 1 - r)            # up
            px[u + d + w + c, v + r] = colour_of(i0 + c, j0, k1 - 1 - r)        # down
    for c in range(d):
        for r in range(h):
            px[u + c, v + d + r] = colour_of(i0, j1 - 1 - r, k1 - 1 - c)          # east (-x)
            px[u + d + w + c, v + d + r] = colour_of(i1 - 1, j1 - 1 - r, k0 + c)  # west (+x)
    for c in range(w):
        for r in range(h):
            px[u + d + c, v + d + r] = colour_of(i0 + c, j1 - 1 - r, k0)          # north (-z)
            px[u + 2 * d + w + c, v + d + r] = colour_of(i1 - 1 - c, j1 - 1 - r, k1 - 1)  # south (+z)
