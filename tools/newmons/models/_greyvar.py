"""Recoloured variants of the Agumon line's Greymon body (CobbleEffort: Digital): `make(name, base, shiny, metal)`
loads FRESH copies of _digi (the shared palette) and _greymon, updates that _digi copy's BASE / SHINY and rebinds the
_greymon copy to it, so the variant paints with its own colours while Greymon and MetalGreymon keep theirs (the same
rule as _variant.clone: never patch a shared palette)."""
from __future__ import annotations

import importlib.util
import os

_HERE = os.path.dirname(os.path.abspath(__file__))


def _fresh(src, tag):
    spec = importlib.util.spec_from_file_location("_greyvar_%s_%s" % (src, tag), os.path.join(_HERE, src + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make(name, base=None, shiny=None, metal=False):
    d = _fresh("_digi", name)
    d.BASE.update(base or {})
    d.SHINY.update(shiny or {})
    g = _fresh("_greymon", name)
    for k in ("P", "claw_fan", "eye", "solid", "striped", "teeth_row"):
        setattr(g, k, getattr(d, k))

    def build():
        return g.build_body(name, metal)

    return build
