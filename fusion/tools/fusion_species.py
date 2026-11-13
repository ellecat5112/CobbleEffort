"""Infinite Fusion's Pokémon (Infinite Dex ids) -> Cobblemon species/forms and their base textures.

A key is "<species>" or "<species>:<form aspect>" (Cobblemon's species id path and the aspect that selects the form).
Pokémon Cobblemon doesn't model (e.g. Oricorio, Meloetta, Castform in 1.8.4) are left out: their fusions keep the
plain head-on-body look.
"""
import glob
import json
import os
import re

FORMS = {  # Infinite Dex name -> form aspect ("" = Cobblemon's default form)
    "Lycanroc (Midday)": "", "Lycanroc (Midnight)": "midnight-form",
    "Minior (Meteor)": "meteor-form", "Minior (Core)": "",
    "Shellos (East Sea)": "east-sea", "Shellos (West Sea)": "",
    "Gastrodon (East Sea)": "east-sea", "Gastrodon (West Sea)": "",
}


def resolver_variations(res_root, folder):
    out = []
    for path in sorted(glob.glob(os.path.join(res_root, "assets/cobblemon/bedrock/pokemon/resolvers", folder, "*.json"))):
        d = json.load(open(path))
        for v in d.get("variations", []):
            out.append((d.get("order", 0), v))
    out.sort(key=lambda t: t[0])
    return [v for _, v in out]


def base_texture(res_root, folder, form):
    """The texture Cobblemon draws for the plain (not shiny, not female) form."""
    tex = None
    for v in resolver_variations(res_root, folder):
        aspects = set(v.get("aspects", []))
        want = {form} if form else set()
        t = v.get("texture")
        if isinstance(t, dict):
            t = (t.get("frames") or [None])[0]
        if t and aspects <= want | {"male"} and (not form or form in aspects):
            tex = t
    if tex is None:
        return None
    ns, path = tex.split(":", 1)
    return os.path.join(res_root, "assets", ns, path)


def species_name(res_root, nat):
    for path in glob.glob(os.path.join(res_root, "data/cobblemon/species/*/*.json")):
        d = json.load(open(path))
        if d.get("nationalPokedexNumber") == nat and d.get("implemented", False):
            return os.path.splitext(os.path.basename(path))[0]
    return None


def mapping(res_root, dropdown):
    """{if_id: {"key", "species", "form", "texture"}} for every Infinite Dex Pokémon Cobblemon models."""
    folders = {}
    for p in glob.glob(os.path.join(res_root, "assets/cobblemon/bedrock/pokemon/resolvers/*")):
        m = re.match(r"(\d+)_", os.path.basename(p))
        if m:
            folders.setdefault(int(m.group(1)), os.path.basename(p))
    names = {}
    for path in glob.glob(os.path.join(res_root, "data/cobblemon/species/*/*.json")):
        d = json.load(open(path))
        names.setdefault(d.get("nationalPokedexNumber"), os.path.splitext(os.path.basename(path))[0])
    out = {}
    for p in dropdown["pokemon"]:
        nat, name = p["nat_id"], p["real_name"]
        if "(" in name and name not in FORMS:
            continue
        form = FORMS.get(name, "")
        folder = folders.get(nat)
        sp = names.get(nat)
        if folder is None or sp is None:
            continue
        tex = base_texture(res_root, folder, form)
        if tex is None or not os.path.exists(tex):
            continue
        out[p["pokemon_id"]] = {"key": sp + (":" + form if form else ""), "species": sp, "form": form, "texture": tex}
    return out


if __name__ == "__main__":
    import sys
    res, dd, out = sys.argv[1:4]
    m = mapping(res, json.load(open(dd)))
    json.dump({str(k): v for k, v in sorted(m.items())}, open(out, "w"), indent=0)
    print(len(m), "of", len(json.load(open(dd))["pokemon"]))
