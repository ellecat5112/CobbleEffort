"""
The mod stack CobbleEffort is built to run alongside: Cobblemon plus the mods in tools/compat/mods.json.

Each mod is a Layer (a jar, or a directory of resources). Layers are ordered bottom to top like resource
packs: for the same file path the top-most layer wins. A layer either allows derivatives of its art
("derivative" layers: Cobblemon, Mega Showdown, ...) or doesn't ("foreign" layers). The generator only ever
reads textures from derivative layers; from foreign layers it reads resolver/species JSON and model UV layouts,
never their texture pixels, and it never copies their files.
"""
from __future__ import annotations

import io
import json
import re
import zipfile
from pathlib import Path

from PIL import Image

COMPAT = Path(__file__).resolve().parent / "compat"


class Layer:
    def __init__(self, index: int, meta: dict, path: Path):
        self.index = index
        self.id = meta["id"]
        self.name = meta["name"]
        self.licence = meta.get("licence", "")
        self.url = meta.get("url", "")
        self.derivatives = bool(meta.get("derivatives"))
        self.bridge = bool(meta.get("bridge"))  # a legacy-layout resource pack, used through tools/bridge.py
        self.meta = meta
        self.path = path
        self.virtual: dict[str, bytes] | None = None
        self.report: list[str] = []
        if path.is_file():
            self.zip = zipfile.ZipFile(path)
            self.files = {n for n in self.zip.namelist() if not n.endswith("/")}
        else:
            self.zip = None
            root = path.resolve()
            self.files = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
            self.path = root

    def read(self, rel: str) -> bytes:
        if self.virtual is not None:
            return self.virtual[rel]
        return self.zip.read(rel) if self.zip else (self.path / rel).read_bytes()

    def read_original(self, rel: str) -> bytes:
        return self.zip.read(rel) if self.zip else (self.path / rel).read_bytes()

    def set_virtual(self, files: dict[str, bytes]):
        """Serve these files instead of the source's own (a bridged pack: what tools/bridge.py writes)."""
        self.original_files = self.files
        self.virtual = files
        self.files = set(files)

    def json(self, rel: str):
        return json.loads(self.read(rel).decode("utf-8-sig"))

    def __repr__(self):
        return f"<{self.id}>"


# Cobblemon still reads the pre-1.5 layout (bedrock/models, bedrock/posers, bedrock/animations, bedrock/species), but
# it loads those folders BEFORE bedrock/pokemon/..., into the same name spaces (model file name, poser id, animation
# group), and the later load wins. So a resource pack in the old layout loses every name it shares with a mod's file,
# whatever the pack order, while its textures (same paths as the mods') still win: its texture on their mesh.
LEGACY_DIRS = {"models": "models", "posers": "posers", "animations": "animations", "species": "resolvers"}


def bedrock_kind(rel: str) -> tuple[str, bool] | None:
    """('models' | 'posers' | 'animations' | 'resolvers', legacy?) for a Pokémon bedrock file, else None."""
    parts = rel.split("/")
    if len(parts) < 5 or parts[0] != "assets" or parts[2] != "bedrock":
        return None
    if parts[3] == "pokemon" and len(parts) >= 6 and parts[4] in ("models", "posers", "animations", "resolvers"):
        return parts[4], False
    if parts[3] in LEGACY_DIRS:
        return LEGACY_DIRS[parts[3]], True
    return None


def _model_key(rel: str):
    """assets/<ns>/bedrock/pokemon/models/**/<name>.geo.json -> ('ns', 'name.geo')."""
    parts = rel.split("/")
    return parts[1], parts[-1][:-len(".json")]


class Stack:
    def __init__(self, cobblemon_root: Path, use_compat: bool = True):
        cob = Layer(0, {"id": "cobblemon", "name": "Cobblemon", "licence": "CC BY-NC 3.0 (assets)", "derivatives": True,
                        "url": "https://gitlab.com/cable-mc/cobblemon"}, cobblemon_root)
        self.layers = [cob]
        cfg = json.loads((COMPAT / "mods.json").read_text())
        self.painted = cfg.get("painted", {})
        if use_compat:
            missing = []
            for meta in cfg["mods"]:
                found = sorted((COMPAT / "jars").glob(meta["source"]))
                if not found:
                    missing.append(f"  {meta['name']}: tools/compat/jars/{meta['source']}  ({meta['url']})")
                    continue
                self.layers.append(Layer(len(self.layers), meta, found[-1]))
            if missing:
                raise SystemExit("Missing compat sources (put the jar, or a directory of its resources, in tools/compat/jars/;"
                                 " or pass --no-compat):\n" + "\n".join(missing))
        self.by_id = {l.id: l for l in self.layers}
        bridged = [l for l in self.layers if l.bridge]
        if bridged and self.layers[-len(bridged):] != bridged:
            raise SystemExit("mods.json: bridged packs must come last (they're used as the top resource packs)")
        # a bridged pack is seen as the bridge tools/bridge.py writes for it (computed against the layers below it)
        self._index([l for l in self.layers if not l.bridge])
        if bridged:
            from bridge import bridge
            for layer in bridged:
                layer.set_virtual(bridge(self, layer))
            self._index(self.layers)

    def _index(self, layers):
        """Model / poser / animation-group indexes: key -> [(layer, rel)] in Cobblemon's load order, so the last entry
        is the one it uses (old-layout folders first, then bedrock/pokemon/..., each bottom to top)."""
        found: dict[str, dict] = {"models": {}, "posers": {}, "animations": {}}
        for layer in layers:
            for rel in sorted(layer.files):
                kind = bedrock_kind(rel)
                if kind is None and rel.startswith("assets/") and rel.endswith(".animation.json"):
                    kind = ("animations", False)                # other entities' animation folders
                if kind is None or kind[0] == "resolvers" or not rel.endswith(".json"):
                    continue
                name = rel.split("/")[-1][:-len(".json")]
                if kind[0] == "models":
                    if not name.endswith(".geo"):
                        continue
                    key = (rel.split("/")[1], name)
                elif kind[0] == "posers":
                    key = (rel.split("/")[1], name)
                else:
                    if not name.endswith(".animation"):
                        continue
                    key = name[:-len(".animation")]
                found[kind[0]].setdefault(key, []).append((not kind[1], layer.index, layer, rel))
        sort = lambda d: {k: [(l, r) for _, _, l, r in sorted(v, key=lambda e: (e[0], e[1]))] for k, v in d.items()}
        self.models, self.posers, self.anims = sort(found["models"]), sort(found["posers"]), sort(found["animations"])

    # -----------------------------------------------------------------------------------------
    # lookups
    # -----------------------------------------------------------------------------------------

    def owner(self, rel: str, derivative_only: bool = True) -> Layer | None:
        for layer in reversed(self.layers):
            if (layer.derivatives or not derivative_only) and rel in layer.files:
                return layer
        return None

    @staticmethod
    def asset_rel(identifier: str) -> str:
        ns, path = identifier.split(":", 1)
        return f"assets/{ns}/{path}"

    def image(self, identifier: str) -> tuple[Image.Image, Layer] | None:
        """A texture from the top-most DERIVATIVE layer that has it (foreign art is never read)."""
        rel = self.asset_rel(identifier)
        layer = self.owner(rel)
        if layer is None:
            return None
        return Image.open(io.BytesIO(layer.read(rel))), layer

    @staticmethod
    def _top(entries, derivative_only):
        for layer, rel in reversed(entries or []):
            if layer.derivatives or not derivative_only:
                return layer, rel
        return None

    def model(self, model_id: str, derivative_only: bool = True):
        """(layer, rel) of the geometry Cobblemon would load for 'ns:name.geo'."""
        ns, name = model_id.split(":", 1)
        return self._top(self.models.get((ns, name)), derivative_only)

    def poser(self, poser_id: str, derivative_only: bool = True):
        ns, name = poser_id.split(":", 1)
        return self._top(self.posers.get((ns, name)), derivative_only)

    def anim(self, group: str, derivative_only: bool = True):
        return self._top(self.anims.get(group), derivative_only)

    def overwritten(self, entries) -> bool:
        """True when a foreign layer's file wins over the top-most derivative one."""
        top, deriv = self._top(entries, False), self._top(entries, True)
        return top is not None and deriv is not None and top != deriv

    def geometry(self, model_id: str, derivative_only: bool = True):
        hit = self.model(model_id, derivative_only)
        return hit[0].json(hit[1])["minecraft:geometry"][0] if hit else None

    # -----------------------------------------------------------------------------------------
    # merged data
    # -----------------------------------------------------------------------------------------

    def files(self, pattern: str, derivative_only: bool = False) -> dict[str, Layer]:
        """rel -> owning layer for every path matching the regex, top-most layer per path."""
        rx = re.compile(pattern)
        out: dict[str, Layer] = {}
        for layer in self.layers:
            if derivative_only and not layer.derivatives:
                continue
            for rel in layer.files:
                if rx.fullmatch(rel):
                    out[rel] = layer
        return dict(sorted(out.items()))


def compat_layers() -> list[Layer]:
    """The mods.json layers on their own (no Cobblemon), as their sources ship them. Fails if one is missing."""
    cfg = json.loads((COMPAT / "mods.json").read_text())
    out, missing = [], []
    for meta in cfg["mods"]:
        found = sorted((COMPAT / "jars").glob(meta["source"]))
        if not found:
            missing.append(f"  {meta['name']}: tools/compat/jars/{meta['source']}  ({meta['url']})")
            continue
        out.append(Layer(len(out) + 1, meta, found[-1]))
    if missing:
        raise SystemExit("Missing compat sources:\n" + "\n".join(missing))
    return out


def resolver_layer_names(layers: list[Layer]) -> dict[str, set[str]]:
    """species -> the names of every layer any of these layers' resolvers (either layout) gives it."""
    names: dict[str, set[str]] = {}
    for layer in layers:
        for rel in sorted(layer.files):
            kind = bedrock_kind(rel)
            if not kind or kind[0] != "resolvers" or not rel.endswith(".json"):
                continue
            try:
                data = layer.json(rel)
            except ValueError:
                continue
            sp = str(data.get("species", data.get("name", ""))).split(":")[-1]
            for v in data.get("variations", []):
                for l in v.get("layers") or []:
                    names.setdefault(sp, set()).add(l.get("name", ""))
    return names


ANIM_REF = re.compile(r"""(bedrock\w*\(\s*['"]?)([A-Za-z0-9_]+)(['"]?\s*,)""")


def poser_groups(text: str) -> set[str]:
    return {m.group(2) for m in ANIM_REF.finditer(text)}


def rename_groups(text: str, renames: dict[str, str]) -> str:
    return ANIM_REF.sub(lambda m: m.group(1) + renames.get(m.group(2), m.group(2)) + m.group(3), text)
