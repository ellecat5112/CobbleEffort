"""Shared helper for the "Mega" giant forms (CobbleEffort: Digital): Mega Black Shoutmon X7, Mega Dark Knightmon, Mega
Darkness Bagramon, Mega Decker Greymon, Mega Gran Kuwagamon and Mega Muso Knightmon are the same Digimon swollen to
colossal size by the Digital World's energy (the game stills on wikimon.net show them unchanged but huge). make(src,
name) builds the existing module `src` and renames the model and its root bone, so the Mega module only sets the
bigger size.
"""
from __future__ import annotations

import importlib


def make(src, name):
    mod = importlib.import_module(src)

    def build():
        m = mod.build()
        old = m.name
        m.name = name
        for b in m.bones:
            if b["name"] == old:
                b["name"] = name
            if b["parent"] == old:
                b["parent"] = name
        for bx in m.boxes:
            if bx.bone == old:
                bx.bone = name
        return m

    return build, mod
