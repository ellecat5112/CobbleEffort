"""Command line interface.

    cobbleeffort quick  <model>             one-shot wizard: model in, mod jar out
    cobbleeffort init   <project>           make an empty addon project
    cobbleeffort add    <project> <model>   add a Pokemon from a model (+ textures next to it)
    cobbleeffort build  <project>           build the mod jar / datapack / resourcepack
    cobbleeffort preview <project>          build + render animated GIF previews
    cobbleeffort analyze <model>            show what the auto-rigger sees
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

from . import __version__
from .model import load_model
from .project import build_project, load_addon
from .rig import detect_rig
from .species import ARCHETYPES, TYPES
from .templates import addon_json, pokemon_json
from .util import CobbleEffortError, namespace_id, species_id

MODEL_SUFFIXES = (".bbmodel", ".geo.json", ".json")


def _model_stem(path: Path) -> str:
    name = path.name
    for suf in (".geo.json", ".bbmodel", ".json"):
        if name.lower().endswith(suf):
            return name[: -len(suf)]
    return path.stem


def _pretty_name(stem: str) -> str:
    stem = re.sub(r"[_\-.]+", " ", stem).strip()
    return " ".join(w.capitalize() for w in stem.split()) or "Custommon"


def _ask(prompt: str, default: str, interactive: bool) -> str:
    if not interactive:
        return default
    try:
        val = input(f"{prompt} [{default}]: ").strip()
    except EOFError:
        return default
    return val or default


# =================================================================== init


def cmd_init(project: Path, name: str | None, namespace: str | None, author: str) -> Path:
    project.mkdir(parents=True, exist_ok=True)
    (project / "pokemon").mkdir(exist_ok=True)
    cfg = project / "addon.json"
    if not cfg.exists():
        nm = name or _pretty_name(project.name)
        cfg.write_text(addon_json(nm, namespace_id(namespace or nm), author), encoding="utf-8")
        print(f"Created project {project} (namespace '{namespace_id(namespace or nm)}')")
    else:
        print(f"Project {project} already exists - leaving addon.json alone")
    return project


def _copy_assets(model: Path, folder: Path, stem: str, sid: str, geo) -> list[str]:
    """Copy the model plus matching textures/animations next to it into the Pokemon's folder."""
    folder.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []

    def copy(src: Path, name: str) -> None:
        dst = folder / name
        if src.resolve() != dst.resolve():
            shutil.copy2(src, dst)
        copied.append(name)

    copy(model, model.name)
    for f in sorted(model.parent.iterdir()):
        low = f.name.lower()
        if f == model or not f.is_file() or not low.startswith(stem.lower()):
            continue
        if low.endswith(".png"):
            copy(f, sid + f.name[len(stem):])  # flarelope_v2_shiny.png -> flarelope_shiny.png
        elif low.endswith(".animation.json"):
            copy(f, f.name)
    # extract embedded textures so they're easy to edit later
    if geo.textures and not any(c.lower().endswith(".png") for c in copied):
        main = [t for t in geo.textures if "shiny" not in t[0].lower()] or geo.textures
        (folder / f"{sid}.png").write_bytes(main[0][1])
        copied.append(f"{sid}.png (extracted from model)")
        for tname, data in geo.textures:
            if "shiny" in tname.lower():
                (folder / f"{sid}_shiny.png").write_bytes(data)
                copied.append(f"{sid}_shiny.png (extracted from model)")
                break
    return copied


# =================================================================== add


def cmd_add(project: Path, model: Path, *, name: str | None, types: str | None, archetype: str | None,
            evolutions: list[str], dex_entry: str, interactive: bool, force: bool) -> Path:
    if not (project / "addon.json").exists():
        cmd_init(project, None, None, "")
    model = model.resolve()
    geo = load_model(model)  # validates early
    stem = _model_stem(model)
    name = name or _ask("Pokemon name", _pretty_name(stem), interactive)
    sid = species_id(name)
    types_s = types or _ask(f"Type(s), e.g. fire or fire/flying ({' '.join(TYPES)})", "normal", interactive)
    type_list = [t for t in re.split(r"[/,\s]+", types_s.lower()) if t]
    for t in type_list:
        if t not in TYPES:
            raise CobbleEffortError(f"Unknown type '{t}'")
    arch = archetype or _ask(f"Movement ({'/'.join(('auto',) + ARCHETYPES)})", "auto", interactive)
    if not evolutions and interactive:
        evo = _ask("Evolves into? e.g. 'flarelord @ level 36' (blank = none)", "", interactive)
        evolutions = [evo] if evo else []

    folder = project / "pokemon" / sid
    if folder.exists() and (folder / "pokemon.json").exists() and not force:
        raise CobbleEffortError(f"{folder} already exists (use --force to overwrite its pokemon.json)")
    copied = _copy_assets(model, folder, stem, sid, geo)

    rig = detect_rig(geo)
    (folder / "pokemon.json").write_text(
        pokemon_json(name=name, types=type_list, archetype=arch, evolutions=evolutions,
                     rig_lines=rig.summary(), dex_entry=dex_entry),
        encoding="utf-8")
    print(f"Added {name} -> {folder}")
    print("  files: " + ", ".join(copied))
    print("  detected rig:")
    for line in rig.summary():
        print("    " + line)
    for n in rig.notes + geo.warnings:
        print("  note: " + n)
    return folder


# =================================================================== build


def cmd_build(project: Path, out: Path | None, only: list[str] | None, preview: bool = False) -> int:
    res = build_project(project, out, only)
    print(f"Built {len(res.files) - 1} package(s) in {res.out_dir}:")
    for f in res.files:
        print(f"  {f}")
    if res.warnings:
        print("Warnings:")
        for w in res.warnings:
            print(f"  - {w}")
    addon = load_addon(project)
    if preview:
        cmd_preview_built(res.out_dir, addon["namespace"], only)
    print(f"\nDrop the .jar into your mods folder (next to Cobblemon), then try: /pokespawn {addon['namespace']}:<name>")
    return 0


def cmd_preview_built(out_dir: Path, ns: str, only: list[str] | None) -> None:
    from .model import load_animation_file
    from .preview import render_previews
    from .textures import RGBAImage

    bed = out_dir / "unpacked" / "resourcepack" / "assets" / ns / "bedrock" / "pokemon"
    tex_root = out_dir / "unpacked" / "resourcepack" / "assets" / ns / "textures" / "pokemon"
    wanted = {species_id(o) for o in only} if only else None
    for model_dir in sorted((bed / "models").iterdir()):
        sid = model_dir.name
        if wanted and sid not in wanted:
            continue
        geo = load_model(model_dir / f"{sid}.geo.json")
        anims = load_animation_file(bed / "animations" / sid / f"{sid}.animation.json")
        tex_path = tex_root / sid / f"{sid}.png"
        tex = RGBAImage.load(tex_path) if tex_path.exists() else None
        files = render_previews(geo, tex, anims, out_dir / "preview" / sid, sid)
        print(f"Preview for {sid}: {len(files) - 1} GIFs + contact sheet in {out_dir / 'preview' / sid}")


def cmd_analyze(model: Path) -> int:
    geo = load_model(model)
    rig = detect_rig(geo)
    print(f"Model: {model}")
    print(f"Bones ({len(geo.bones)}): {', '.join(geo.bone_names())}")
    print("Detected rig:")
    for line in rig.summary():
        print("  " + line)
    if geo.animations:
        print(f"Animations already in the model: {', '.join(geo.animations)}")
    if geo.textures:
        print(f"Embedded textures: {', '.join(t[0] for t in geo.textures)}")
    for n in rig.notes + geo.warnings:
        print("note: " + n)
    print("\nTips: name bones head / neck / jaw / eye_left / leg_front_left / arm_right / wing_left / tail / tail2 ...")
    return 0


def cmd_quick(model: Path, project: Path | None, args: argparse.Namespace) -> int:
    model = model.resolve()
    project = project or (model.parent / "CobbleEffort_Addon")
    interactive = not args.yes and sys.stdin.isatty()
    if not (project / "addon.json").exists():
        addon_name = _ask("Addon name", "My Custom Pokemon", interactive)
        author = _ask("Author", "", interactive)
        cmd_init(project, addon_name, None, author)
    stem = _model_stem(model)
    sid = species_id(args.name or _pretty_name(stem))
    folder = project / "pokemon" / sid
    if (folder / "pokemon.json").exists() and not args.reset:
        # Re-dropping an updated model: refresh files, keep the user's config.
        copied = _copy_assets(model, folder, stem, sid, load_model(model))
        print(f"Updated {sid}: {', '.join(copied)} (kept your pokemon.json; use --reset to start over)")
    else:
        cmd_add(project, model, name=args.name, types=args.types, archetype=args.archetype,
                evolutions=args.evolves_to or [], dex_entry=args.dex_entry or "", interactive=interactive,
                force=True)
    print()
    return cmd_build(project, None, None)


# =================================================================== main


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="cobbleeffort",
                                description="Plug-and-play custom Pokemon generator for Cobblemon")
    p.add_argument("--version", action="version", version=f"CobbleEffort {__version__}")
    sub = p.add_subparsers(dest="cmd")

    def pokemon_opts(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--name", help="Pokemon name (default: from the model file name)")
        sp.add_argument("--types", help="e.g. fire or fire/flying")
        sp.add_argument("--archetype", choices=("auto",) + ARCHETYPES)
        sp.add_argument("--evolves-to", action="append", metavar="'TARGET @ COND'",
                        help="e.g. 'flarelord @ level 36' (repeatable)")
        sp.add_argument("--dex-entry", help="Pokedex description text")

    q = sub.add_parser("quick", help="One-shot: model in -> mod jar out (asks a few questions)")
    q.add_argument("model", type=Path)
    q.add_argument("--project", type=Path, help="Project folder (default: CobbleEffort_Addon next to the model)")
    q.add_argument("-y", "--yes", action="store_true", help="Don't ask questions; use defaults/flags")
    q.add_argument("--reset", action="store_true", help="Rewrite pokemon.json even if it already exists")
    pokemon_opts(q)

    i = sub.add_parser("init", help="Create a new addon project")
    i.add_argument("project", type=Path)
    i.add_argument("--name")
    i.add_argument("--namespace")
    i.add_argument("--author", default="")

    a = sub.add_parser("add", help="Add a Pokemon to a project from a model file")
    a.add_argument("project", type=Path)
    a.add_argument("model", type=Path)
    a.add_argument("-i", "--interactive", action="store_true", help="Ask for missing details")
    a.add_argument("--force", action="store_true")
    pokemon_opts(a)

    b = sub.add_parser("build", help="Build the addon")
    b.add_argument("project", type=Path, nargs="?", default=Path("."))
    b.add_argument("--out", type=Path)
    b.add_argument("--only", action="append", help="Build only these Pokemon (repeatable)")
    b.add_argument("--preview", action="store_true", help="Also render animated GIF previews (needs Pillow)")

    pv = sub.add_parser("preview", help="Build, then render animated GIF previews of every animation")
    pv.add_argument("project", type=Path, nargs="?", default=Path("."))
    pv.add_argument("--only", action="append")

    an = sub.add_parser("analyze", help="Show the bones/rig the generator detects in a model")
    an.add_argument("model", type=Path)

    argv = list(sys.argv[1:] if argv is None else argv)
    # drag-and-drop: `cobbleeffort model.bbmodel` == `cobbleeffort quick model.bbmodel`
    if argv and not argv[0].startswith("-") and argv[0] not in sub.choices and \
            argv[0].lower().endswith(MODEL_SUFFIXES):
        argv = ["quick"] + argv
    args = p.parse_args(argv)
    try:
        if args.cmd == "quick":
            return cmd_quick(args.model, args.project, args)
        if args.cmd == "init":
            cmd_init(args.project, args.name, args.namespace, args.author)
            return 0
        if args.cmd == "add":
            cmd_add(args.project, args.model, name=args.name, types=args.types, archetype=args.archetype,
                    evolutions=args.evolves_to or [], dex_entry=args.dex_entry or "",
                    interactive=args.interactive, force=args.force)
            return 0
        if args.cmd == "build":
            return cmd_build(args.project, args.out, args.only, args.preview)
        if args.cmd == "preview":
            return cmd_build(args.project, None, args.only, True)
        if args.cmd == "analyze":
            return cmd_analyze(args.model)
        p.print_help()
        return 1
    except CobbleEffortError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
