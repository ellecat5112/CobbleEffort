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
from pathlib import Path

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


def load_mesh(path, samples: int = 3_000_000, seed: int = 0):
    """Any mesh Tripo (or Blender) exports: .glb/.gltf/.obj(+.mtl+texture)/.fbx-converted/.ply, low-poly or not,
    coloured by a texture or by vertex colours. Returns (points, colours 0-1, triangles) where the points are spread
    evenly over the surface (so big low-poly triangles are covered too), as voxelize() expects with F=None.
    A zip is unpacked first (the mesh plus its .mtl and texture images)."""
    import tempfile, zipfile
    import trimesh
    path = Path(path)
    if path.suffix.lower() == ".zip":
        tmp = Path(tempfile.mkdtemp())
        with zipfile.ZipFile(path) as z:
            z.extractall(tmp)
        found = [f for ext in (".glb", ".gltf", ".obj", ".ply", ".fbx") for f in tmp.rglob(f"*{ext}")]
        if not found:
            raise SystemExit(f"no mesh (.glb/.gltf/.obj/.ply) inside {path}")
        path = found[0]
    if path.suffix.lower() == ".fbx":
        raise SystemExit("FBX can't be read here: export GLB or OBJ from Tripo instead")
    loaded = trimesh.load(path, force="scene", process=False)
    meshes = list(loaded.dump())         # every mesh instance with its node transform applied
    pts_all, col_all = [], []
    total_area = sum(m.area for m in meshes)
    rng = np.random.default_rng(seed)
    for m in meshes:
        n = max(1000, int(samples * m.area / total_area))
        pts, fidx = trimesh.sample.sample_surface(m, n, seed=int(rng.integers(1 << 31)))
        tri = m.triangles[fidx]
        bary = trimesh.triangles.points_to_barycentric(tri, pts)
        vis = m.visual
        cols = None
        if getattr(vis, "kind", None) == "texture" and getattr(vis, "uv", None) is not None:
            mat = vis.material
            img = getattr(mat, "baseColorTexture", None) or getattr(mat, "image", None)
            if img is not None:
                img = img.convert("RGB")
                uv = (vis.uv[m.faces[fidx]] * bary[:, :, None]).sum(1)
                tex = np.asarray(img, dtype=np.float32) / 255
                h, w = tex.shape[:2]
                x = np.clip((uv[:, 0] % 1.0) * (w - 1), 0, w - 1).astype(int)
                y = np.clip((1 - uv[:, 1] % 1.0) * (h - 1), 0, h - 1).astype(int)
                cols = tex[y, x]          # the texture is the art: a material tint factor is ignored
        if cols is None and getattr(vis, "vertex_colors", None) is not None and len(vis.vertex_colors):
            vc = np.asarray(vis.vertex_colors[:, :3], dtype=np.float32) / 255
            cols = (vc[m.faces[fidx]] * bary[:, :, None]).sum(1)
        if cols is None:
            mc = getattr(vis, "main_color", None)
            cols = np.tile((np.asarray(mc[:3], dtype=np.float32) / 255) if mc is not None else [0.7, 0.7, 0.7], (len(pts), 1))
        pts_all.append(pts.astype(np.float32))
        col_all.append(np.clip(cols, 0, 1).astype(np.float32))
    return np.concatenate(pts_all), np.concatenate(col_all), None


def voxelize(P, C, F, height: float, face_negative_z: bool = True, front: str | None = None):
    """Points sampled on every triangle -> occupied voxels (one per model unit) with mean colours; the inside is
    filled. Returns (solid, surface, colours, lo) where voxel (i, j, k) has its min corner at lo + (i, j, k)."""
    from scipy import ndimage
    K = height / (P[:, 1].max() - P[:, 1].min())
    if F is None:                       # already surface samples (load_mesh)
        pts, col = P, C
    else:                               # a dense mesh: its vertices, centroids and edge midpoints are enough
        T, TC = P[F], C[F]
        pts = np.concatenate([P, T.mean(1), (T[:, 0] + T[:, 1]) / 2, (T[:, 1] + T[:, 2]) / 2, (T[:, 2] + T[:, 0]) / 2])
        col = np.concatenate([C, TC.mean(1), (TC[:, 0] + TC[:, 1]) / 2, (TC[:, 1] + TC[:, 2]) / 2, (TC[:, 2] + TC[:, 0]) / 2])
    q = pts.copy()
    # Cobblemon models face -z (left side +x). `front` names the source's facing ("+z", "-z", "+x", "-x"); the old
    # face_negative_z=True means a source facing +z (turned 180 degrees about y)
    front = front or ("+z" if face_negative_z else "-z")
    x, z = q[:, 0].copy(), q[:, 2].copy()
    q[:, 0], q[:, 2] = {"+z": (-x, -z), "-z": (x, z), "-x": (-z, x), "+x": (z, -x)}[front]
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


# ---------------------------------------------------------------------------------------------
# Cobblemon-style cleanup: smoother shapes, chunkier boxes, shaded faces
# ---------------------------------------------------------------------------------------------

def smooth(solid, sigma: float = 1.15, keep_thin: float = 2.0, min_part: int = 4):
    """Round off voxel stair-steps and specks: blur the signed distance field and re-threshold it. Thin parts
    (wings, tusks, spikes, strands: nowhere more than ~keep_thin voxels thick) are kept as they were, and floating
    bits smaller than min_part voxels are dropped."""
    from scipy import ndimage
    pad = 3
    s = np.pad(solid, pad)
    inside = ndimage.distance_transform_edt(s)
    outside = ndimage.distance_transform_edt(~s)
    sdf = ndimage.gaussian_filter((outside - inside).astype(np.float32), sigma)
    out = sdf < 0
    thin = s & (ndimage.maximum_filter(inside, size=5) <= keep_thin)
    out |= thin
    lab, n = ndimage.label(out)
    if n:
        sizes = ndimage.sum(out, lab, range(1, n + 1))
        for c, size in enumerate(sizes, 1):
            if size < min_part:
                out[lab == c] = False
    # smoothing must not cut a piece off: put back the original voxels on the shortest bridge between pieces
    n_orig = ndimage.label(s)[1]
    for _ in range(20):
        lab, n = ndimage.label(out)
        if n <= n_orig:
            break
        sizes = ndimage.sum(out, lab, range(1, n + 1))
        small = int(np.argmin(sizes)) + 1
        piece = lab == small
        d_piece = ndimage.distance_transform_edt(~piece)
        d_rest = ndimage.distance_transform_edt(~(out & ~piece))
        missing = s & ~out
        if not missing.any():
            break
        total = np.where(missing, d_piece + d_rest, np.inf)
        best = total.min()
        if not np.isfinite(best):
            break
        out |= missing & (total <= best + 1.0)
    return out[pad:-pad, pad:-pad, pad:-pad]


def nearest_solid(solid):
    """For every cell, the index of the nearest solid voxel (colours for the few empty cells a box may cover)."""
    from scipy import ndimage
    _, idx = ndimage.distance_transform_edt(~solid, return_indices=True)
    return idx


def fit_boxes(mask, tolerance: float = 0.12, blocked=None):
    """Like greedy_boxes, but a box may grow over a few empty cells (at most `tolerance` of the box, and each new
    slab at least 1 - tolerance full), so a part is built from fewer, larger, cleaner boxes. Cells in `blocked`
    (other parts) are never covered."""
    left = mask.copy()
    blocked = np.zeros_like(mask) if blocked is None else blocked
    X, Y, Z = mask.shape
    boxes = []

    def ok(sl, filled_needed):
        region = mask[sl]
        if blocked[sl].any():
            return False
        return region.mean() >= filled_needed

    for j in range(Y):
        for k in range(Z):
            for i in range(X):
                if not left[i, j, k]:
                    continue
                i0, j0, k0, i1, j1, k1 = i, j, k, i + 1, j + 1, k + 1
                grew = True
                while grew:
                    grew = False
                    for axis in (0, 2, 1):                       # x, then z, then y
                        lo_ = [i0, j0, k0]
                        hi_ = [i1, j1, k1]
                        if hi_[axis] >= mask.shape[axis]:
                            continue
                        slab = [slice(lo_[0], hi_[0]), slice(lo_[1], hi_[1]), slice(lo_[2], hi_[2])]
                        slab[axis] = slice(hi_[axis], hi_[axis] + 1)
                        slab = tuple(slab)
                        if not left[slab].any():
                            continue
                        new_hi = list(hi_)
                        new_hi[axis] += 1
                        whole = (slice(i0, new_hi[0]), slice(j0, new_hi[1]), slice(k0, new_hi[2]))
                        if ok(slab, 1 - tolerance) and ok(whole, 1 - tolerance) and not (mask[slab] & ~left[slab]).any():
                            i1, j1, k1 = new_hi
                            grew = True
                left[i0:i1, j0:j1, k0:k1] = False
                boxes.append((i0, j0, k0, i1, j1, k1))
    return boxes


def face_shade(face: str, r: int, h: int, edge: bool) -> float:
    """Baked Cobblemon-style shading for a texel of a box face: light from above, a soft vertical gradient on the
    sides, darker where the surface ends or turns a corner (silhouette and creases)."""
    base = {"up": 1.06, "down": 0.8}.get(face, 1.0)
    if face not in ("up", "down") and h > 1:
        base *= 1.03 - 0.13 * (r / (h - 1))
    return base * (0.86 if edge else 1.0)


_NORMALS = {"up": (0, 1, 0), "down": (0, -1, 0), "east": (-1, 0, 0), "west": (1, 0, 0), "north": (0, 0, -1), "south": (0, 0, 1)}


def exposure(solid):
    """{face: voxels whose face in that direction is open air}."""
    out = {}
    p = np.pad(solid, 1)
    for face, (dx, dy, dz) in _NORMALS.items():
        nb = p[1 + dx:p.shape[0] - 1 + dx, 1 + dy:p.shape[1] - 1 + dy, 1 + dz:p.shape[2] - 1 + dz]
        out[face] = solid & ~nb
    return out


def paint_box_shaded(img, uv, box, colour_of, exposed=None):
    """paint_box with face_shade applied (use for body textures, not glow layers). With `exposed` (from exposure()),
    a texel is an edge when the visible surface doesn't continue into a neighbouring voxel in the face's plane."""
    i0, j0, k0, i1, j1, k1 = box
    w, h, d = i1 - i0, j1 - j0, k1 - k0
    u, v = uv
    px = img.load()
    X = Y = Z = None
    if exposed is not None:
        X, Y, Z = exposed["up"].shape

    def edge(face, i, j, k):
        if exposed is None:
            return False
        ex = exposed[face]
        n = _NORMALS[face]
        for t in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            if t[0] * n[0] + t[1] * n[1] + t[2] * n[2]:
                continue                                         # only directions in the face's plane
            # the surface continues if the neighbour, or the voxel one step up or down from it (a stair step),
            # shows the same face
            cont = False
            for off in (0, 1, -1):
                a, b, c = i + t[0] + off * n[0], j + t[1] + off * n[1], k + t[2] + off * n[2]
                if 0 <= a < X and 0 <= b < Y and 0 <= c < Z and ex[a, b, c]:
                    cont = True
                    break
            if not cont:
                return True
        return False

    def put(x, y, ijk, face, r, hh):
        col = colour_of(*ijk)
        if col[3]:
            f = face_shade(face, r, hh, edge(face, *ijk))
            px[x, y] = tuple(max(0, min(255, int(ch * f))) for ch in col[:3]) + (col[3],)
        else:
            px[x, y] = col
    for c in range(w):
        for r in range(d):
            put(u + d + c, v + r, (i0 + c, j1 - 1, k1 - 1 - r), "up", r, d)
            put(u + d + w + c, v + r, (i0 + c, j0, k1 - 1 - r), "down", r, d)
    for c in range(d):
        for r in range(h):
            put(u + c, v + d + r, (i0, j1 - 1 - r, k1 - 1 - c), "east", r, h)
            put(u + d + w + c, v + d + r, (i1 - 1, j1 - 1 - r, k0 + c), "west", r, h)
    for c in range(w):
        for r in range(h):
            put(u + d + c, v + d + r, (i0 + c, j1 - 1 - r, k0), "north", r, h)
            put(u + 2 * d + w + c, v + d + r, (i1 - 1 - c, j1 - 1 - r, k1 - 1), "south", r, h)


def fit_bone_boxes(bone, n_bones: int, tolerance: float = 0.12):
    """[(bone index, box)] for every bone, boxes fitted with fit_boxes and never covering another bone's voxels."""
    out = []
    for b in range(n_bones):
        mask = bone == b
        out += [(b, box) for box in fit_boxes(mask, tolerance, blocked=(bone >= 0) & ~mask)]
    return out


def at_nearest(nearest, fn):
    """Wrap colour_of(i, j, k) so an empty cell a box covers takes the colour of the nearest solid voxel."""
    def f(i, j, k):
        return fn(int(nearest[0, i, j, k]), int(nearest[1, i, j, k]), int(nearest[2, i, j, k]))
    return f


def keep_largest(solid):
    """Only the biggest connected piece (drops loose bits a generated mesh may carry, e.g. a stray ball or bar)."""
    from scipy import ndimage
    lab, n = ndimage.label(solid)
    if n <= 1:
        return solid
    sizes = ndimage.sum(solid, lab, range(1, n + 1))
    return lab == (int(np.argmax(sizes)) + 1)


def strip_base(solid, drop: float = 0.45):
    """Cut off a display stand under the feet (a generated figurine's plinth): the lowest rows while their filled area
    is a big slab, until it drops below `drop` of that slab; then keep the largest piece and drop the model to y = 0."""
    area = solid.sum(axis=(0, 2)).astype(float)
    if not area.any():
        return solid
    base = area[: max(1, len(area) // 10)].max()
    top = 0
    while top < len(area) - 1 and area[top] >= drop * base:
        top += 1
    out = solid.copy()
    out[:, :top, :] = False
    out = keep_largest(out)
    ys = np.nonzero(out.any(axis=(0, 2)))[0]
    if len(ys) and ys[0] > 0:
        out = np.concatenate([out[:, ys[0]:, :], np.zeros_like(out[:, : ys[0], :])], axis=1)
    return out
