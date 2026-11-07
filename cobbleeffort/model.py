"""Load Blockbench (.bbmodel) or Bedrock (.geo.json) models into one structure.

The .bbmodel conversion mirrors Blockbench's own "Export Bedrock Geometry"
so the user never has to open Blockbench's export dialogs: cubes, pivots,
rotations, box/per-face UVs, mirroring, locators, embedded textures and any
animations already made in Blockbench are all carried over.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .textures import decode_data_uri
from .util import CobbleEffortError, num

AXES = ("x", "y", "z")


@dataclass
class Geometry:
    bones: list[dict]
    texture_width: int = 64
    texture_height: int = 64
    textures: list[tuple[str, bytes]] = field(default_factory=list)  # embedded textures (name, png bytes)
    animations: dict[str, dict] = field(default_factory=dict)  # bedrock animation name -> json
    warnings: list[str] = field(default_factory=list)
    source: str = ""

    # ------------------------------------------------------------ queries
    def bone(self, name: str) -> dict | None:
        for b in self.bones:
            if b["name"] == name:
                return b
        return None

    def bone_names(self) -> list[str]:
        return [b["name"] for b in self.bones]

    def children(self) -> dict[str | None, list[str]]:
        ch: dict[str | None, list[str]] = {}
        for b in self.bones:
            ch.setdefault(b.get("parent"), []).append(b["name"])
        return ch

    def roots(self) -> list[str]:
        names = set(self.bone_names())
        return [b["name"] for b in self.bones if not b.get("parent") or b.get("parent") not in names]

    def depth(self, name: str) -> int:
        d = 0
        b = self.bone(name)
        seen = set()
        while b and b.get("parent") and b["parent"] not in seen:
            seen.add(b["parent"])
            b = self.bone(b["parent"])
            d += 1
        return d

    def ancestors(self, name: str) -> list[str]:
        out = []
        b = self.bone(name)
        while b and b.get("parent"):
            out.append(b["parent"])
            b = self.bone(b["parent"])
            if len(out) > 256:
                break
        return out

    def descendants(self, name: str) -> list[str]:
        ch = self.children()
        out: list[str] = []
        stack = list(ch.get(name, []))
        while stack:
            n = stack.pop(0)
            out.append(n)
            stack.extend(ch.get(n, []))
        return out

    def bounds(self) -> tuple[list[float], list[float]]:
        """Axis-aligned bounds of all cubes in model pixels (ignores rotations)."""
        lo = [float("inf")] * 3
        hi = [float("-inf")] * 3
        for b in self.bones:
            for c in b.get("cubes", []):
                inf = float(c.get("inflate", b.get("inflate", 0)) or 0)
                o = c.get("origin", [0, 0, 0])
                s = c.get("size", [0, 0, 0])
                for i in range(3):
                    lo[i] = min(lo[i], o[i] - inf)
                    hi[i] = max(hi[i], o[i] + s[i] + inf)
        if lo[0] == float("inf"):
            return [0.0, 0.0, 0.0], [16.0, 16.0, 16.0]
        return lo, hi

    def bone_bounds(self, name: str, include_children: bool = True) -> tuple[list[float], list[float]] | None:
        names = [name] + (self.descendants(name) if include_children else [])
        sub = Geometry([self.bone(n) for n in names if self.bone(n)])
        if not any(b.get("cubes") for b in sub.bones):
            return None
        return sub.bounds()

    # ------------------------------------------------------------ editing
    def ensure_single_root(self, root_name: str) -> str:
        """Cobblemon posers need a single root bone; wrap multiple roots if needed."""
        roots = self.roots()
        if len(roots) == 1:
            return roots[0]
        if self.bone(root_name):
            root_name = root_name + "_root"
        for b in self.bones:
            if b["name"] in roots:
                b["parent"] = root_name
        self.bones.insert(0, {"name": root_name, "pivot": [0, 0, 0]})
        self.warnings.append(f"Model had {len(roots)} top-level bones; wrapped them in a new root bone '{root_name}'.")
        return root_name

    def to_geo_json(self, identifier: str) -> dict:
        lo, hi = self.bounds()
        width = max(hi[0] - lo[0], hi[2] - lo[2]) / 16
        height = (hi[1] - lo[1]) / 16
        bones = []
        for b in self.bones:
            nb = {k: v for k, v in b.items() if v not in (None, [], {})}
            bones.append(nb)
        return {
            "format_version": "1.12.0",
            "minecraft:geometry": [
                {
                    "description": {
                        "identifier": f"geometry.{identifier}",
                        "texture_width": self.texture_width,
                        "texture_height": self.texture_height,
                        "visible_bounds_width": num(max(2.0, width * 2 + 1), 2),
                        "visible_bounds_height": num(max(2.0, height + 1), 2),
                        "visible_bounds_offset": [0, num(max(0.5, height / 2), 2), 0],
                    },
                    "bones": bones,
                }
            ],
        }


# ====================================================================== load


def load_model(path: Path) -> Geometry:
    path = Path(path)
    if not path.exists():
        raise CobbleEffortError(f"Model file not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as e:
        raise CobbleEffortError(f"Model {path} is not readable JSON: {e}") from e
    name = path.name.lower()
    if name.endswith(".bbmodel") or ("elements" in data and "outliner" in data):
        geo = _from_bbmodel(data)
    else:
        geo = _from_geo_json(data)
    geo.source = str(path)
    if not geo.bones:
        raise CobbleEffortError(f"{path} contains no bones")
    _dedupe_bone_names(geo)
    _order_bones(geo)
    return geo


def load_animation_file(path: Path) -> dict[str, dict]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except Exception as e:
        raise CobbleEffortError(f"Animation file {path} is not readable JSON: {e}") from e
    return dict(data.get("animations", {}))


# ------------------------------------------------------------------ geo.json


def _from_geo_json(data: dict) -> Geometry:
    warnings: list[str] = []
    if "minecraft:geometry" in data:
        geos = data["minecraft:geometry"]
        if not geos:
            raise CobbleEffortError("geo.json has an empty minecraft:geometry list")
        if len(geos) > 1:
            warnings.append(f"geo.json has {len(geos)} geometries; using the first one.")
        g = geos[0]
        desc = g.get("description", {})
        tw, th = desc.get("texture_width", 64), desc.get("texture_height", 64)
        bones = copy.deepcopy(g.get("bones", []))
    else:  # legacy 1.8.0 format {"geometry.name": {...}}
        keys = [k for k in data if k.startswith("geometry.")]
        if not keys:
            raise CobbleEffortError("Unrecognised model format (expected .bbmodel or Bedrock .geo.json)")
        g = data[keys[0]]
        tw, th = g.get("texturewidth", 64), g.get("textureheight", 64)
        bones = copy.deepcopy(g.get("bones", []))
    for b in bones:
        b.setdefault("pivot", [0, 0, 0])
    return Geometry(bones=bones, texture_width=int(tw), texture_height=int(th), warnings=warnings)


# ------------------------------------------------------------------- bbmodel


def _neg_x(v: list) -> list:
    return [num(-float(v[0])), num(float(v[1])), num(float(v[2]))]


def _bb_rot(r: list | None) -> list | None:
    if not r or all(float(x) == 0 for x in r):
        return None
    return [num(-float(r[0])), num(-float(r[1])), num(float(r[2]))]


def _from_bbmodel(data: dict) -> Geometry:
    warnings: list[str] = []
    meta = data.get("meta", {})
    fmt = meta.get("model_format", "")
    if fmt and fmt not in ("bedrock", "bedrock_old", "free", "modded_entity", "generic", "cobblemon"):
        warnings.append(f"Blockbench project format is '{fmt}'; Cobblemon expects 'Bedrock Entity'. Converting anyway.")
    global_box_uv = bool(meta.get("box_uv", False))
    res = data.get("resolution", {})
    tw, th = int(res.get("width", 64)), int(res.get("height", 64))

    elements = {e["uuid"]: e for e in data.get("elements", []) if "uuid" in e}
    groups_by_uuid = {g["uuid"]: g for g in data.get("groups", []) if isinstance(g, dict) and "uuid" in g}

    bones: list[dict] = []
    loose_cubes: list[dict] = []
    skipped_meshes = 0

    def compile_cube(e: dict, bone_mirror: bool) -> dict | None:
        nonlocal skipped_meshes
        etype = e.get("type", "cube")
        if etype != "cube":
            if etype == "mesh":
                skipped_meshes += 1
            return None
        if e.get("export") is False:
            return None
        f = [float(x) for x in e.get("from", [0, 0, 0])]
        t = [float(x) for x in e.get("to", [0, 0, 0])]
        size = [num(t[i] - f[i]) for i in range(3)]
        cube: dict[str, Any] = {"origin": [num(-(f[0] + (t[0] - f[0]))), num(f[1]), num(f[2])], "size": size}
        inflate = float(e.get("inflate", 0) or 0)
        if inflate:
            cube["inflate"] = num(inflate)
        rot = _bb_rot(e.get("rotation"))
        if rot:
            cube["pivot"] = _neg_x(e.get("origin", [0, 0, 0]))
            cube["rotation"] = rot
        box_uv = e.get("box_uv", global_box_uv)
        if box_uv:
            cube["uv"] = [num(x) for x in e.get("uv_offset", [0, 0])]
            mirror = bool(e.get("mirror_uv", False))
            if mirror != bone_mirror:
                cube["mirror"] = mirror
        else:
            uv: dict[str, Any] = {}
            for face_name, face in (e.get("faces") or {}).items():
                if not isinstance(face, dict):
                    continue
                if "texture" in face and face["texture"] is None:
                    continue
                fu = [float(x) for x in face.get("uv", [0, 0, 0, 0])]
                fuv = [fu[0], fu[1]]
                fsize = [fu[2] - fu[0], fu[3] - fu[1]]
                if face_name in ("up", "down"):
                    fuv = [fuv[0] + fsize[0], fuv[1] + fsize[1]]
                    fsize = [-fsize[0], -fsize[1]]
                entry: dict[str, Any] = {"uv": [num(fuv[0]), num(fuv[1])], "uv_size": [num(fsize[0]), num(fsize[1])]}
                if face.get("rotation"):
                    entry["uv_rotation"] = face["rotation"]
                uv[face_name] = entry
            cube["uv"] = uv
        return cube

    def locator_of(e: dict) -> tuple[str, list] | None:
        if e.get("type") != "locator":
            return None
        pos = e.get("position") or e.get("from") or [0, 0, 0]
        return e.get("name", "locator"), _neg_x(pos)

    def resolve_group(node: Any) -> dict | None:
        if isinstance(node, str):
            return groups_by_uuid.get(node)
        if isinstance(node, dict):
            if "name" in node:
                return node
            g = groups_by_uuid.get(node.get("uuid"))
            if g is not None:
                merged = dict(g)
                if "children" in node:
                    merged["children"] = node["children"]
                return merged
        return None

    def walk(node: Any, parent: str | None) -> None:
        g = resolve_group(node)
        if g is None:
            # an element directly in the outliner (or a child element of a group handled by caller)
            if isinstance(node, str) and node in elements and parent is None:
                c = compile_cube(elements[node], False)
                if c:
                    loose_cubes.append(c)
            return
        if g.get("export") is False:
            return
        bone: dict[str, Any] = {"name": g.get("name", "bone")}
        if parent:
            bone["parent"] = parent
        bone["pivot"] = _neg_x(g.get("origin", [0, 0, 0]))
        rot = _bb_rot(g.get("rotation"))
        if rot:
            bone["rotation"] = rot
        mirror = bool(g.get("mirror_uv", False))
        if mirror:
            bone["mirror"] = True
        cubes: list[dict] = []
        locators: dict[str, list] = {}
        child_groups: list[Any] = []
        for ch in g.get("children", []):
            if isinstance(ch, str) and ch in elements:
                e = elements[ch]
                loc = locator_of(e)
                if loc:
                    locators[loc[0]] = loc[1]
                    continue
                c = compile_cube(e, mirror)
                if c:
                    cubes.append(c)
            else:
                child_groups.append(ch)
        if cubes:
            bone["cubes"] = cubes
        if locators:
            bone["locators"] = locators
        bones.append(bone)
        for ch in child_groups:
            walk(ch, bone["name"])

    for node in data.get("outliner", []):
        walk(node, None)

    if loose_cubes:
        bones.append({"name": "bb_main", "pivot": [0, 0, 0], "cubes": loose_cubes})
        warnings.append("Some cubes were not inside any group; they were put in a bone named 'bb_main'.")
    if skipped_meshes:
        warnings.append(f"Skipped {skipped_meshes} mesh element(s): Cobblemon models only support cubes.")

    # embedded textures
    textures: list[tuple[str, bytes]] = []
    for i, tex in enumerate(data.get("textures", [])):
        raw = decode_data_uri(tex.get("source", ""))
        if raw is None and tex.get("path"):
            p = Path(tex["path"])
            if p.exists():
                raw = p.read_bytes()
        if raw:
            textures.append((tex.get("name") or f"texture_{i}.png", raw))
        if tex.get("width") and i == 0 and not res:
            tw, th = int(tex.get("uv_width", tex["width"])), int(tex.get("uv_height", tex["height"]))
    if len(textures) > 1:
        names = [t[0] for t in textures]
        warnings.append(f"Model has {len(textures)} textures {names}; Cobblemon uses one texture per model (others are used for shiny/emissive if named so).")

    geo = Geometry(bones=bones, texture_width=tw, texture_height=th, textures=textures, warnings=warnings)
    geo.animations = _bb_animations(data, {b["name"] for b in bones}, warnings)
    return geo


def _parse_val(v: Any) -> Any:
    if isinstance(v, (int, float)):
        return num(v, 4)
    if isinstance(v, str):
        s = v.strip()
        if s == "":
            return 0
        try:
            return num(float(s), 4)
        except ValueError:
            return s
    return 0


def _bb_animations(data: dict, bone_names: set[str], warnings: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for anim in data.get("animations", []) or []:
        name = anim.get("name", "animation")
        entry: dict[str, Any] = {}
        loop = anim.get("loop", "once")
        if loop == "loop":
            entry["loop"] = True
        elif loop == "hold":
            entry["loop"] = "hold_on_last_frame"
        if anim.get("length"):
            entry["animation_length"] = num(anim["length"], 4)
        bones: dict[str, dict] = {}
        for animator in (anim.get("animators") or {}).values():
            if animator.get("type", "bone") != "bone":
                continue
            bname = animator.get("name")
            if bname not in bone_names:
                continue
            for kf in animator.get("keyframes", []):
                ch = kf.get("channel")
                if ch not in ("rotation", "position", "scale"):
                    continue
                dps = kf.get("data_points") or [{}]
                vals = [[_parse_val(dp.get(a, 0 if ch != "scale" else 1)) for a in AXES] for dp in dps]
                t = str(num(kf.get("time", 0), 4))
                interp = kf.get("interpolation", "linear")
                if len(vals) > 1:
                    v: Any = {"pre": vals[0], "post": vals[1]}
                elif interp == "catmullrom":
                    v = {"post": vals[0]}
                else:
                    v = vals[0]
                if interp == "catmullrom":
                    v["lerp_mode"] = "catmullrom"
                elif interp == "step" and isinstance(v, list):
                    v = {"pre": v, "post": v}
                if interp == "bezier":
                    warnings.append(f"Animation '{name}' uses bezier keyframes; exported as linear.")
                bones.setdefault(bname, {}).setdefault(ch, {})[t] = v
        for bdata in bones.values():
            for ch, frames in list(bdata.items()):
                bdata[ch] = dict(sorted(frames.items(), key=lambda kv: float(kv[0])))
        entry["bones"] = bones
        if bones:
            out[name] = entry
    return out


# ------------------------------------------------------------------ cleanup


def _dedupe_bone_names(geo: Geometry) -> None:
    seen: dict[str, int] = {}
    for b in geo.bones:
        n = b["name"]
        if n in seen:
            seen[n] += 1
            new = f"{n}_{seen[n]}"
            geo.warnings.append(f"Duplicate bone name '{n}' renamed to '{new}'.")
            # children of the duplicate refer by name; re-point those that come after it
            idx = geo.bones.index(b)
            for c in geo.bones[idx + 1 :]:
                if c.get("parent") == n:
                    c["parent"] = new
            b["name"] = new
        else:
            seen[n] = 0


def _order_bones(geo: Geometry) -> None:
    """Make sure parents are listed before their children."""
    by_name = {b["name"]: b for b in geo.bones}
    ordered: list[dict] = []
    placed: set[str] = set()

    def place(b: dict, guard: int = 0) -> None:
        if b["name"] in placed or guard > 256:
            return
        p = b.get("parent")
        if p and p in by_name and p not in placed:
            place(by_name[p], guard + 1)
        if b["name"] not in placed:
            placed.add(b["name"])
            ordered.append(b)

    for b in geo.bones:
        place(b)
    geo.bones = ordered
