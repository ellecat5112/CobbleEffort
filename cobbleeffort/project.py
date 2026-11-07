"""Project loading and the full build pipeline.

Project layout:

    MyAddon/
      addon.json                 <- pack name, namespace, version...
      pokemon/
        flarelope/
          flarelope.bbmodel      <- or flarelope.geo.json
          flarelope.png          <- optional if embedded in the .bbmodel
          flarelope_shiny.png    <- optional (auto-generated otherwise)
          flarelope_emissive.png <- optional glow layer
          flarelope_female.png   <- optional female texture
          *.animation.json       <- optional hand-made animations (kept as-is)
          pokemon.json           <- the friendly config
      build/                     <- output (mod jar, datapack, resourcepack, report)
"""

from __future__ import annotations

import json
import shutil
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import __version__
from .animgen import Settings, generate
from .model import Geometry, load_animation_file, load_model
from .poser import build_poser
from .rig import Rig, detect_rig
from .spawns import build_spawns
from .species import ARCHETYPES, build_species, parse_types
from .textures import RGBAImage
from .util import CobbleEffortError, as_list, load_jsonc, namespace_id, species_id, write_json

DEFAULT_ADDON = {
    "name": "My Custom Pokemon",
    "namespace": "mycustommons",
    "version": "1.0.0",
    "author": "",
    "description": "Custom Pokemon made with CobbleEffort",
    "dex_start": 2000,
    "pack_format": {"data": 48, "resource": 34},
    "max_format": 999,
    "outputs": ["jar", "datapack", "resourcepack"],
}
INHERITED_KEYS = ("types", "type", "abilities", "egg_groups", "experience_group", "gender", "male_ratio",
                  "archetype", "moves", "egg_cycles", "base_friendship", "walk_speed", "animation", "labels")
TEX_SUFFIXES = ("_shiny", "_emissive", "_glow", "_female", "_female_shiny", "_emissive_shiny", "_glow_shiny")


@dataclass
class PokemonEntry:
    folder: Path
    cfg: dict
    sid: str
    model_path: Path | None = None
    pre_evolution: str | None = None    # local sid
    stage: int = 0
    in_chain: bool = False
    dex: int = 0


@dataclass
class BuildResult:
    out_dir: Path
    files: list[Path] = field(default_factory=list)
    report: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# ================================================================== loading


def load_addon(project: Path) -> dict:
    cfg = dict(DEFAULT_ADDON)
    path = project / "addon.json"
    if path.exists():
        cfg.update(load_jsonc(path))
    cfg["namespace"] = namespace_id(cfg.get("namespace") or cfg.get("name", "custommons"))
    return cfg


def find_model(folder: Path, cfg: dict) -> Path | None:
    if cfg.get("model"):
        p = folder / cfg["model"]
        if not p.exists():
            raise CobbleEffortError(f"{folder.name}: model file '{cfg['model']}' not found")
        return p
    for pattern in ("*.bbmodel", "*.geo.json"):
        found = sorted(folder.glob(pattern))
        if found:
            return found[0]
    return None


def load_pokemon(project: Path) -> list[PokemonEntry]:
    root = project / "pokemon"
    if not root.is_dir():
        raise CobbleEffortError(f"No 'pokemon' folder in {project}. Run 'cobbleeffort add' first.")
    entries: list[PokemonEntry] = []
    for folder in sorted(p for p in root.iterdir() if p.is_dir()):
        cfg_path = folder / "pokemon.json"
        if not cfg_path.exists():
            continue
        cfg = load_jsonc(cfg_path)
        if not isinstance(cfg, dict) or not cfg.get("name"):
            raise CobbleEffortError(f"{cfg_path} needs at least a \"name\"")
        if cfg.get("enabled") is False:
            continue
        entries.append(PokemonEntry(folder=folder, cfg=cfg, sid=species_id(cfg["name"]),
                                    model_path=find_model(folder, cfg)))
    ids = [e.sid for e in entries]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise CobbleEffortError(f"Two Pokemon share the same id: {', '.join(sorted(dupes))}")
    return entries


def _evo_targets(cfg: dict) -> list[str]:
    out = []
    for e in as_list(cfg.get("evolutions")):
        if isinstance(e, dict):
            res = str(e.get("result", "")).split()[0] if e.get("result") else ""
        else:
            res = str(e).split("@", 1)[0].strip().split()[0] if "@" in str(e) else ""
        if res:
            out.append(species_id(res.split(":")[-1]))
    return out


def link_evolutions(entries: list[PokemonEntry]) -> None:
    by_id = {e.sid: e for e in entries}
    for e in entries:
        for t in _evo_targets(e.cfg):
            if t in by_id:
                tgt = by_id[t]
                if tgt.pre_evolution and tgt.pre_evolution != e.sid:
                    continue  # first one wins
                tgt.pre_evolution = e.sid
                tgt.in_chain = True
                e.in_chain = True
    # explicit "evolves_from"
    for e in entries:
        src = e.cfg.get("evolves_from")
        if src:
            sid = species_id(str(src).split(":")[-1])
            e.pre_evolution = sid
            e.in_chain = True
            if sid in by_id:
                by_id[sid].in_chain = True
    # stages
    for e in entries:
        stage, cur, seen = 0, e, set()
        while cur.pre_evolution and cur.pre_evolution in by_id and cur.sid not in seen:
            seen.add(cur.sid)
            cur = by_id[cur.pre_evolution]
            stage += 1
        e.stage = stage
    # inheritance: walk in stage order so chains of 3 work
    for e in sorted(entries, key=lambda x: x.stage):
        if e.pre_evolution in by_id and e.cfg.get("inherit", True):
            parent = by_id[e.pre_evolution].cfg
            for k in INHERITED_KEYS:
                if k in parent and k not in e.cfg and not (k == "type" and "types" in e.cfg) \
                        and not (k == "types" and "type" in e.cfg):
                    e.cfg[k] = parent[k]
    for e in entries:
        e.cfg["_in_chain"] = e.in_chain


def assign_dex(entries: list[PokemonEntry], start: int) -> None:
    used = {int(e.cfg["dex"]) for e in entries if e.cfg.get("dex")}
    by_pre: dict[str | None, list[PokemonEntry]] = {}
    for e in entries:
        by_pre.setdefault(e.pre_evolution if e.pre_evolution in {x.sid for x in entries} else None, []).append(e)
    order: list[PokemonEntry] = []

    def visit(e: PokemonEntry) -> None:
        order.append(e)
        for child in by_pre.get(e.sid, []):
            visit(child)

    for base in by_pre.get(None, []):
        visit(base)
    nxt = start
    for e in order:
        if e.cfg.get("dex"):
            e.dex = int(e.cfg["dex"])
            continue
        while nxt in used:
            nxt += 1
        e.dex = nxt
        used.add(nxt)


# ================================================================== helpers


def pick_archetype(cfg: dict, rig: Rig, types: list[str]) -> tuple[str, str]:
    a = str(cfg.get("archetype", "auto")).lower()
    if a in ARCHETYPES:
        return a, "set in pokemon.json"
    if a != "auto":
        raise CobbleEffortError(f"archetype must be auto or one of {', '.join(ARCHETYPES)}")
    if rig.wings:
        return "flier", "has wing bones"
    if rig.fins and not rig.legs:
        return "swimmer", "has fins and no legs"
    if "water" in types and rig.fins:
        return "amphibian", "water type with fins and legs"
    if not rig.legs and ("ghost" in types or "psychic" in types):
        return "floater", "legless ghost/psychic type"
    if "water" in types:
        return "amphibian", "water type"
    return "walker", "default"


def find_textures(folder: Path, sid: str, cfg: dict, geo: Geometry) -> dict[str, Any]:
    """Return dict role -> RGBAImage for base/shiny/emissive/female textures."""
    pngs = {p.stem.lower(): p for p in folder.glob("*.png")}
    out: dict[str, Any] = {}

    def by_suffix(suffix: str) -> Path | None:
        if (sid + suffix) in pngs:
            return pngs[sid + suffix]
        cands = [p for stem, p in pngs.items() if stem.endswith(suffix)
                 and not any(stem.endswith(s) for s in TEX_SUFFIXES if s != suffix and s.endswith(suffix) and len(s) > len(suffix))]
        return cands[0] if len(cands) == 1 else None

    if cfg.get("texture"):
        p = folder / cfg["texture"]
        if not p.exists():
            raise CobbleEffortError(f"{folder.name}: texture '{cfg['texture']}' not found")
        out["base"] = RGBAImage.load(p)
    elif sid in pngs:
        out["base"] = RGBAImage.load(pngs[sid])
    else:
        plain = [p for stem, p in pngs.items() if not any(stem.endswith(s) for s in TEX_SUFFIXES)]
        if len(plain) == 1:
            out["base"] = RGBAImage.load(plain[0])
        elif geo.textures:
            # embedded textures: prefer a non-shiny one
            emb = [t for t in geo.textures if "shiny" not in t[0].lower() and "emissive" not in t[0].lower()
                   and "glow" not in t[0].lower()] or geo.textures
            out["base"] = RGBAImage.from_bytes(emb[0][1])
            for name, data in geo.textures:
                low = name.lower()
                if "shiny" in low and "shiny" not in out:
                    out["shiny"] = RGBAImage.from_bytes(data)
                elif ("emissive" in low or "glow" in low) and "emissive" not in out:
                    out["emissive"] = RGBAImage.from_bytes(data)
        elif len(plain) > 1:
            raise CobbleEffortError(f"{folder.name}: several PNGs found ({', '.join(p.name for p in plain)}); "
                                    f"name the main one {sid}.png or set \"texture\" in pokemon.json")
    for role, suffix in (("shiny", "_shiny"), ("emissive", "_emissive"), ("female", "_female"),
                         ("female_shiny", "_female_shiny"), ("emissive_shiny", "_emissive_shiny")):
        p = by_suffix(suffix)
        if p is None and suffix.startswith("_emissive"):
            p = by_suffix(suffix.replace("_emissive", "_glow"))
        if p is not None:
            out[role] = RGBAImage.load(p)
    if "base" not in out:
        raise CobbleEffortError(f"{folder.name}: no texture found. Put {sid}.png next to the model "
                                "or embed the texture in the .bbmodel")
    return out


def make_shiny(img: RGBAImage, shiny_cfg: Any) -> RGBAImage:
    if isinstance(shiny_cfg, dict):
        if shiny_cfg.get("palette"):
            return img.palette_swap(shiny_cfg["palette"], int(shiny_cfg.get("tolerance", 0)))
        return img.hue_shift(float(shiny_cfg.get("hue", 160)), float(shiny_cfg.get("saturation", 1.0)),
                             float(shiny_cfg.get("brightness", 1.0)))
    if isinstance(shiny_cfg, (int, float)) and not isinstance(shiny_cfg, bool):
        return img.hue_shift(float(shiny_cfg))
    return img.hue_shift(160)


def _pack_mcmeta(addon: dict, kind: str) -> dict:
    fmt = int(addon["pack_format"][kind])
    hi = int(addon.get("max_format", 999))
    return {
        "pack": {
            "description": f"{addon['name']} ({kind}) - made with CobbleEffort",
            "pack_format": fmt,
            "supported_formats": {"min_inclusive": fmt, "max_inclusive": hi},
            "min_format": fmt,
            "max_format": hi,
        }
    }


def _mod_id(ns: str) -> str:
    return ns + "_addon" if ns in ("cobblemon", "minecraft") else ns


# ================================================================== build


def build_project(project: Path, out_dir: Path | None = None, only: list[str] | None = None) -> BuildResult:
    project = Path(project)
    addon = load_addon(project)
    ns = addon["namespace"]
    entries = load_pokemon(project)
    link_evolutions(entries)
    assign_dex(entries, int(addon.get("dex_start", 2000)))
    local_ids = {e.sid for e in entries}
    if only:
        wanted = {species_id(o) for o in only}
        unknown = wanted - local_ids
        if unknown:
            raise CobbleEffortError(f"Not in this project: {', '.join(sorted(unknown))}")
        entries = [e for e in entries if e.sid in wanted]
    if not entries:
        raise CobbleEffortError("No Pokemon to build (add one with 'cobbleeffort add')")

    out = Path(out_dir) if out_dir else project / "build"
    stage_dir = out / "unpacked"
    if stage_dir.exists():
        shutil.rmtree(stage_dir)
    data_root = stage_dir / "datapack"
    res_root = stage_dir / "resourcepack"
    result = BuildResult(out_dir=out)
    lang: dict[str, str] = {}
    report = result.report
    report.append(f"# CobbleEffort build report - {addon['name']} v{addon['version']}")
    report.append("")
    report.append(f"Namespace: `{ns}`  |  CobbleEffort {__version__}")
    report.append("")

    for e in entries:
        report.append(f"## {e.cfg['name']} (`{ns}:{e.sid}`, dex #{e.dex}, stage {e.stage})")
        warn_prefix = f"{e.cfg['name']}: "
        if e.model_path is None:
            raise CobbleEffortError(f"{e.folder.name}: no .bbmodel or .geo.json model in the folder")
        geo = load_model(e.model_path)
        root = geo.ensure_single_root(e.sid)
        rig = detect_rig(geo, e.cfg.get("rig"))
        types = parse_types(e.cfg)
        archetype, why = pick_archetype(e.cfg, rig, types)

        # ---- animations
        supplied = dict(geo.animations)
        for af in sorted(e.folder.glob("*.animation.json")):
            supplied.update(load_animation_file(af))
        acfg = e.cfg.get("animation", {}) or {}
        settings = Settings(energy=float(acfg.get("energy", 1.0)), speed=float(acfg.get("speed", 1.0)),
                            can_fly=archetype == "flier", can_swim=archetype in ("swimmer", "amphibian"),
                            floats=archetype == "floater")
        root_pivot = [float(x) for x in geo.bone(root).get("pivot", [0, 0, 0])]
        if acfg.get("regenerate"):
            supplied = {}
        anims = generate(rig, e.sid, settings, root_pivot, supplied, skip=as_list(acfg.get("skip")))
        poser = build_poser(e.sid, rig, anims, can_fly=settings.can_fly, can_swim=settings.can_swim,
                            floats=settings.floats,
                            shoulder=True,  # harmless if the species isn't shoulder-mountable
                            tweaks=e.cfg.get("poser"))

        # ---- textures
        tex = find_textures(e.folder, e.sid, e.cfg, geo)
        base = tex["base"]
        if base.width * geo.texture_height != base.height * geo.texture_width:
            result.warnings.append(warn_prefix + f"texture is {base.width}x{base.height} but the model's UVs expect "
                                   f"{geo.texture_width}x{geo.texture_height} (different aspect ratio).")
        shiny_cfg = e.cfg.get("shiny", "auto")
        shiny_note = "supplied"
        if "shiny" not in tex:
            tex["shiny"] = make_shiny(base, shiny_cfg)
            shiny_note = "auto-generated"
        if "emissive" in tex and "emissive_shiny" not in tex:
            tex["emissive_shiny"] = make_shiny(tex["emissive"], shiny_cfg)
        if "female" in tex and "female_shiny" not in tex:
            tex["female_shiny"] = make_shiny(tex["female"], shiny_cfg)

        tex_dir = res_root / "assets" / ns / "textures" / "pokemon" / e.sid
        tex_names = {"base": f"{e.sid}.png", "shiny": f"{e.sid}_shiny.png", "emissive": f"{e.sid}_emissive.png",
                     "emissive_shiny": f"{e.sid}_emissive_shiny.png", "female": f"{e.sid}_female.png",
                     "female_shiny": f"{e.sid}_female_shiny.png"}
        for role, img in tex.items():
            img.save(tex_dir / tex_names[role])

        def tex_ref(role: str) -> str:
            return f"{ns}:textures/pokemon/{e.sid}/{tex_names[role]}"

        variations: list[dict] = [{
            "aspects": [],
            "poser": f"{ns}:{e.sid}",
            "model": f"{ns}:{e.sid}.geo",
            "texture": tex_ref("base"),
            "layers": ([{"name": "emissive", "texture": tex_ref("emissive"), "emissive": True}]
                       if "emissive" in tex else []),
        }]
        shiny_var: dict[str, Any] = {"aspects": ["shiny"], "texture": tex_ref("shiny")}
        if "emissive" in tex:
            shiny_var["layers"] = [{"name": "emissive", "texture": tex_ref("emissive_shiny"), "emissive": True}]
        variations.append(shiny_var)
        if "female" in tex:
            variations.append({"aspects": ["female"], "texture": tex_ref("female")})
            variations.append({"aspects": ["female", "shiny"], "texture": tex_ref("female_shiny")})
        resolver = {"species": f"{ns}:{e.sid}", "order": 0, "variations": variations}

        # ---- resource pack files
        bed = res_root / "assets" / ns / "bedrock" / "pokemon"
        write_json(bed / "models" / e.sid / f"{e.sid}.geo.json", geo.to_geo_json(e.sid))
        write_json(bed / "animations" / e.sid / f"{e.sid}.animation.json", anims.to_file())
        write_json(bed / "posers" / e.sid / f"{e.sid}.json", poser)
        write_json(bed / "resolvers" / e.sid / f"0_{e.sid}_base.json", resolver)

        # ---- species
        lo, hi = geo.bounds()
        h_blocks = (hi[1] - lo[1]) / 16
        w_blocks = (max(hi[0] - lo[0], 0) + max(hi[2] - lo[2], 0)) / 2 / 16
        pre = None
        if e.pre_evolution:
            pre = e.pre_evolution if (e.pre_evolution not in local_ids or ns == "cobblemon") else f"{ns}:{e.pre_evolution}"
        e.cfg.setdefault("archetype", archetype)
        species = build_species(cfg=e.cfg, sid=e.sid, ns=ns, dex=e.dex, stage=e.stage, archetype=archetype,
                                model_height_blocks=h_blocks, model_width_blocks=w_blocks,
                                local_ids=local_ids, pre_evolution=pre)
        write_json(data_root / "data" / ns / "species" / "custom" / f"{e.sid}.json", species)
        species_ref = e.sid if ns == "cobblemon" else f"{ns}:{e.sid}"
        spawn = build_spawns(e.cfg.get("spawn"), e.sid, species_ref, archetype, e.stage)
        if spawn:
            write_json(data_root / "data" / ns / "spawn_pool_world" / f"{e.sid}.json", spawn)

        lang[f"{ns}.species.{e.sid}.name"] = e.cfg["name"]
        lang[f"{ns}.species.{e.sid}.desc"] = e.cfg.get("dex_entry") or f"A mysterious Pokemon known as {e.cfg['name']}."

        # ---- report
        stats = species["baseStats"]
        report += [
            f"- Types: {'/'.join(types)} | Archetype: **{archetype}** ({why}) | Gait: {rig.gait}",
            f"- Stats: {'/'.join(str(v) for v in stats.values())} (total {sum(stats.values())})",
            f"- Abilities: {', '.join(species['abilities'])}",
            f"- Evolutions: {', '.join(ev['result'] + ' via ' + ev['variant'] for ev in species['evolutions']) or 'none'}",
            f"- Pre-evolution: {pre or 'none'}",
            f"- Spawns: {'yes (' + str(len(spawn['spawns'])) + ' entries)' if spawn else 'no'}",
            f"- Shiny texture: {shiny_note}" + (" | emissive layer" if "emissive" in tex else "")
            + (" | female texture" if "female" in tex else ""),
            f"- Animations generated: {', '.join(anims.generated) or '-'}",
            f"- Animations kept from your files: {', '.join(anims.supplied) or '-'}",
            "",
            "```",
            *rig.summary(),
            "```",
            "",
        ]
        for n in rig.notes + geo.warnings:
            result.warnings.append(warn_prefix + n)

    # lang (merge with any user-supplied extra lang entries)
    extra_lang = project / "lang_extra.json"
    if extra_lang.exists():
        lang.update(load_jsonc(extra_lang))
    write_json(res_root / "assets" / ns / "lang" / "en_us.json", lang)

    write_json(data_root / "pack.mcmeta", _pack_mcmeta(addon, "data"))
    write_json(res_root / "pack.mcmeta", _pack_mcmeta(addon, "resource"))

    # ---- package
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in addon["name"]).strip("_") or ns
    version = str(addon.get("version", "1.0.0"))
    outputs = set(as_list(addon.get("outputs", DEFAULT_ADDON["outputs"])))
    out.mkdir(parents=True, exist_ok=True)
    if "datapack" in outputs:
        p = out / f"{safe_name}-datapack-{version}.zip"
        _zip_dirs(p, [(data_root, "")])
        result.files.append(p)
    if "resourcepack" in outputs:
        p = out / f"{safe_name}-resourcepack-{version}.zip"
        _zip_dirs(p, [(res_root, "")])
        result.files.append(p)
    if "jar" in outputs:
        p = out / f"{safe_name}-{version}.jar"
        _write_jar(p, addon, data_root, res_root)
        result.files.append(p)

    if result.warnings:
        report.append("## Warnings")
        report += [f"- {w}" for w in result.warnings]
        report.append("")
    report += [
        "## How to install",
        f"- **Easiest:** put `{safe_name}-{version}.jar` in your `mods` folder (Fabric or NeoForge, next to Cobblemon).",
        f"- **Or:** put the datapack zip in `saves/<world>/datapacks` and the resourcepack zip in `resourcepacks`.",
        "",
        "Test in game: `/pokespawn " + (entries[0].sid if ns == "cobblemon" else f"{ns}:{entries[0].sid}") + "`"
        + " (add `shiny=yes` to check the shiny).",
    ]
    rp = out / "BUILD_REPORT.md"
    rp.write_text("\n".join(report) + "\n", encoding="utf-8")
    result.files.append(rp)
    return result


def _zip_dirs(path: Path, roots: list[tuple[Path, str]], extra: dict[str, bytes] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in (extra or {}).items():
            z.writestr(name, data)
        seen = set(extra or {})
        for root, prefix in roots:
            for f in sorted(root.rglob("*")):
                if f.is_file():
                    arc = prefix + f.relative_to(root).as_posix()
                    if arc in seen:
                        continue
                    seen.add(arc)
                    z.write(f, arc)


def _write_jar(path: Path, addon: dict, data_root: Path, res_root: Path) -> None:
    ns = addon["namespace"]
    mod_id = _mod_id(ns)
    version = str(addon.get("version", "1.0.0"))
    desc = addon.get("description", "")
    authors = [a for a in as_list(addon.get("author")) if a]
    fabric = {
        "schemaVersion": 1,
        "id": mod_id,
        "version": version,
        "name": addon["name"],
        "description": desc,
        "authors": authors,
        "license": addon.get("license", "All-Rights-Reserved"),
        "environment": "*",
        "depends": {"fabricloader": ">=0.15.0", "cobblemon": "*"},
    }
    toml_desc = desc.replace("'''", "'")
    neoforge = f"""modLoader="lowcodefml"
loaderVersion="[1,)"
license="{addon.get('license', 'All-Rights-Reserved')}"

[[mods]]
modId="{mod_id}"
version="{version}"
displayName="{addon['name'].replace('"', "'")}"
authors="{', '.join(authors)}"
description='''{toml_desc}'''

[[dependencies.{mod_id}]]
modId="cobblemon"
type="required"
versionRange="[1.6,)"
ordering="AFTER"
side="BOTH"
"""
    combined_meta = _pack_mcmeta(addon, "data")
    combined_meta["pack"]["description"] = f"{addon['name']} - made with CobbleEffort"
    extra = {
        "META-INF/MANIFEST.MF": b"Manifest-Version: 1.0\r\nCreated-By: CobbleEffort\r\n\r\n",
        "fabric.mod.json": json.dumps(fabric, indent=2).encode(),
        "META-INF/neoforge.mods.toml": neoforge.encode(),
        "pack.mcmeta": json.dumps(combined_meta, indent=2).encode(),
    }
    _zip_dirs(path, [(data_root, ""), (res_root, "")], extra)
