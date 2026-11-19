"""Helpers for the Xros Up forms (CobbleEffort: Digital): a Xros Up is a base Digimon wearing parts of a partner. The
module loads a FRESH copy of the base module (models/<src>.py, so the original keeps its name and palette), builds
the base model under the new name, and the caller adds the partner's parts. `hand(m, bone)` / `top(m, bone)` find
where a bone's boxes end, so parts can be fixed to the base without knowing its builder's numbers."""
from __future__ import annotations

import importlib.util
import os

_HERE = os.path.dirname(os.path.abspath(__file__))


def base(src, name, fn=None, *args, **kw):
    """Load a fresh copy of models/<src>.py; return a builder for the base model named `name`: `fn` names a factory
    in that module called as fn(name, *args, **kw) (make, small...), else the module's own build(). The root bone is
    renamed to `name` either way."""
    spec = importlib.util.spec_from_file_location("_xrosup_%s_%s" % (src, name), os.path.join(_HERE, src + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if hasattr(mod, "Model"):
        real = mod.Model
        mod.Model = lambda _n, *a, **k: real(name, *a, **k)
    inner = getattr(mod, fn)(name, *args, **kw) if fn else mod.build

    def build():
        m = inner()
        m.name = name
        old = m.bones[0]["name"]
        if old != name:
            m.bones[0]["name"] = name
            for b in m.bones[1:]:
                if b["parent"] == old:
                    b["parent"] = name
            for b in m.boxes:
                if b.bone == old:
                    b.bone = name
        return m
    return mod, build


def _boxes(m, bone):
    return [b for b in m.boxes if b.bone == bone]


def hand(m, bone):
    bs = _boxes(m, bone)
    lo = min(bs, key=lambda b: b.lo[1])
    return (lo.lo[0] + lo.size[0] / 2, lo.lo[1] + lo.size[1] / 2, lo.lo[2] + lo.size[2] / 2)


def top(m, bone):
    bs = _boxes(m, bone)
    hi = max(bs, key=lambda b: b.lo[1] + b.size[1])
    return (hi.lo[0] + hi.size[0] / 2, hi.lo[1] + hi.size[1], hi.lo[2] + hi.size[2] / 2)


def bone_of(m, *names):
    have = {b["name"] for b in m.bones}
    for n in names:
        if n in have:
            return n
    return m.bones[0]["name"]
