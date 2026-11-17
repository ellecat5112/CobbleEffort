"""Recoloured variants of an existing Digimon module (CobbleEffort: Digital): `clone(src, name, base, shiny)` loads a
FRESH copy of models/<src>.py (its own module object, so the original keeps its colours), updates that copy's BASE /
SHINY palettes and makes its build() name the model `name`. The shaders read the palette when the texture is painted,
after build(), so the copy's palette must stay changed: never patch the shared module itself."""
from __future__ import annotations

import importlib.util
import os

_HERE = os.path.dirname(os.path.abspath(__file__))


def clone(src, name, base=None, shiny=None):
    spec = importlib.util.spec_from_file_location("_variant_%s_%s" % (src, name), os.path.join(_HERE, src + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.BASE.update(base or {})
    mod.SHINY.update(shiny or {})
    real = mod.Model
    mod.Model = lambda _n, *a, **k: real(name, *a, **k)
    return mod
