"""The parts registry: one module per distortable line (named after its first stage) with LINE (its species),
build(kit) (the parts, per model it uses), RECOLOUR (the type-colour shift: dst hue, optional src/width/sat/val/
dst_shiny; None keeps the complement recolour) and optional UNIFY (every model swap uses the base model's parts,
e.g. Torterra's trees all become one volcano)."""
from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path

from _kit import Kit  # noqa: F401  (re-exported for make_assets.py)

_BY_SPECIES = None


def module_for(species):
    global _BY_SPECIES
    if _BY_SPECIES is None:
        _BY_SPECIES = {}
        for info in pkgutil.iter_modules([str(Path(__file__).parent)]):
            if info.name.startswith("_") or info.name == "parts":
                continue
            m = importlib.import_module(info.name)
            for sp in m.LINE:
                _BY_SPECIES[sp] = m
    return _BY_SPECIES.get(species)
