"""Tests for CobbleEffort. Run: python -m unittest discover -s tests"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "examples"))

from cobbleeffort import textures  # noqa: E402
from cobbleeffort.animgen import Settings, generate  # noqa: E402
from cobbleeffort.cli import main as cli_main  # noqa: E402
from cobbleeffort.model import _from_bbmodel, load_model  # noqa: E402
from cobbleeffort.preview import eval_molang  # noqa: E402
from cobbleeffort.project import build_project  # noqa: E402
from cobbleeffort.rig import detect_rig  # noqa: E402
from cobbleeffort.spawns import build_spawns  # noqa: E402
from cobbleeffort.species import parse_drops, parse_evolution, parse_moves, parse_stats  # noqa: E402
from cobbleeffort.util import CobbleEffortError, species_id, strip_json_comments  # noqa: E402

import make_example_models  # noqa: E402


def make_models(tmp: Path) -> Path:
    out = tmp / "models"
    make_example_models.main(out)
    return out


class UtilTests(unittest.TestCase):
    def test_jsonc(self):
        txt = '{\n // c\n "a": "http://x", /* b */ "b": [1,2,],\n}'
        self.assertEqual(json.loads(strip_json_comments(txt)), {"a": "http://x", "b": [1, 2]})

    def test_species_id(self):
        self.assertEqual(species_id("Mr. Mime-Z"), "mrmimez")


class SpeciesShorthandTests(unittest.TestCase):
    def test_stats_forms(self):
        self.assertEqual(parse_stats({"stats": [1, 2, 3, 4, 5, 6]}, 0)["speed"], 6)
        d = parse_stats({"stats": {"hp": 1, "atk": 2, "def": 3, "spa": 4, "spd": 5, "spe": 6}}, 0)
        self.assertEqual(d["special_defence"], 5)
        self.assertEqual(sum(parse_stats({"bst": 500, "spread": "physical"}, 0).values()), 500)
        self.assertEqual(parse_stats({"stats": "45/49/49/65/65/45"}, 0)["hp"], 45)
        with self.assertRaises(CobbleEffortError):
            parse_stats({"stats": [1, 2]}, 0)

    def test_evolutions(self):
        local = {"flarelord"}
        e = parse_evolution("flarelord @ level 36", "pup", "myns", local)
        self.assertEqual(e["result"], "myns:flarelord")
        self.assertEqual(e["requirements"], [{"variant": "level", "minLevel": 36}])
        e = parse_evolution("ninetales @ item fire_stone", "pup", "myns", local)
        self.assertEqual((e["variant"], e["requiredContext"], e["result"]), ("item_interact", "cobblemon:fire_stone", "ninetales"))
        e = parse_evolution("umbreon @ friendship 160 + time night", "eevee", "cobblemon", set())
        self.assertEqual([r["variant"] for r in e["requirements"]], ["friendship", "time_range"])
        e = parse_evolution("scizor @ trade holding metal_coat", "scyther", "cobblemon", set())
        self.assertEqual(e["variant"], "trade")
        self.assertTrue(e["consumeHeldItem"])
        e = parse_evolution("x @ level 20 + female + learns flamewheel", "a", "n", set())
        self.assertEqual(e["learnableMoves"], ["flamewheel"])
        self.assertEqual(e["requirements"][1], {"variant": "properties", "target": "gender=female"})
        with self.assertRaises(CobbleEffortError):
            parse_evolution("x @ dance badly", "a", "n", set())

    def test_moves(self):
        m = parse_moves({"moves": {"1": "tackle, growl", "7": "Flame Wheel", "egg": ["howl"]}}, ["fire"], 0)
        self.assertEqual(m, ["1:tackle", "1:growl", "7:flamewheel", "egg:howl"])
        auto = parse_moves({}, ["fire", "flying"], 0)
        self.assertIn("5:ember", auto)
        self.assertIn("9:gust", auto)

    def test_drops(self):
        d = parse_drops(["minecraft:bone 0-2", "cobblemon:oran_berry 5%"])
        self.assertEqual(d["entries"][0]["quantityRange"], "0-2")
        self.assertEqual(d["entries"][1]["percentage"], 5.0)

    def test_spawns(self):
        s = build_spawns({"biomes": ["forest"], "rarity": "rare", "time": "night"}, "pup", "ns:pup", "walker", 0)
        sp = s["spawns"][0]
        self.assertEqual(sp["condition"]["biomes"], ["#cobblemon:is_forest"])
        self.assertEqual(sp["bucket"], "rare")
        self.assertEqual(sp["spawnablePositionType"], "grounded")
        self.assertIsNone(build_spawns({"auto": True}, "x", "ns:x", "walker", 1))
        self.assertIsNone(build_spawns(None, "x", "ns:x", "walker", 1))
        self.assertIsNotNone(build_spawns(True, "x", "ns:x", "walker", 1))


class BBModelConversionTests(unittest.TestCase):
    def test_blockbench_export_rules(self):
        cube_box = {"uuid": "c1", "name": "c", "from": [1, 2, 3], "to": [4, 6, 8], "origin": [2, 2, 2],
                    "rotation": [10, 20, 30], "box_uv": True, "uv_offset": [5, 6], "mirror_uv": True}
        cube_face = {"uuid": "c2", "name": "f", "from": [0, 0, 0], "to": [2, 2, 2], "origin": [0, 0, 0],
                     "box_uv": False, "faces": {"north": {"uv": [0, 0, 2, 2], "texture": 0},
                                                "up": {"uv": [2, 0, 4, 2], "texture": 0},
                                                "down": {"uv": [0, 0, 0, 0], "texture": None}}}
        data = {"meta": {"model_format": "bedrock"}, "resolution": {"width": 32, "height": 32},
                "elements": [cube_box, cube_face],
                "outliner": [{"name": "root", "origin": [1, 0, 0], "rotation": [5, 6, 7], "uuid": "g1",
                              "children": ["c1", {"name": "child", "origin": [0, 1, 0], "uuid": "g2",
                                                  "children": ["c2"]}]}]}
        geo = _from_bbmodel(data)
        root, child = geo.bones
        self.assertEqual(root["pivot"], [-1, 0, 0])
        self.assertEqual(root["rotation"], [-5, -6, 7])
        c = root["cubes"][0]
        self.assertEqual(c["origin"], [-4, 2, 3])
        self.assertEqual(c["size"], [3, 4, 5])
        self.assertEqual(c["pivot"], [-2, 2, 2])
        self.assertEqual(c["rotation"], [-10, -20, 30])
        self.assertEqual(c["uv"], [5, 6])
        self.assertTrue(c["mirror"])
        f = child["cubes"][0]
        self.assertEqual(f["uv"]["north"], {"uv": [0, 0], "uv_size": [2, 2]})
        self.assertEqual(f["uv"]["up"], {"uv": [4, 2], "uv_size": [-2, -2]})
        self.assertNotIn("down", f["uv"])
        self.assertEqual(child["parent"], "root")
        self.assertEqual((geo.texture_width, geo.texture_height), (32, 32))

    def test_blockbench5_groups_array(self):
        data = {"elements": [{"uuid": "c1", "from": [0, 0, 0], "to": [1, 1, 1], "box_uv": True}],
                "groups": [{"uuid": "g1", "name": "body", "origin": [0, 0, 0]}],
                "outliner": [{"uuid": "g1", "children": ["c1"]}]}
        geo = _from_bbmodel(data)
        self.assertEqual(geo.bones[0]["name"], "body")
        self.assertEqual(len(geo.bones[0]["cubes"]), 1)

    def test_bbmodel_animation_passthrough(self):
        data = {"elements": [], "outliner": [{"name": "head", "origin": [0, 0, 0], "uuid": "g", "children": []}],
                "animations": [{"name": "animation.x.idle", "loop": "loop", "length": 2,
                                "animators": {"g": {"name": "head", "type": "bone", "keyframes": [
                                    {"channel": "rotation", "time": 0, "data_points": [{"x": "5", "y": 0, "z": 0}]},
                                    {"channel": "rotation", "time": 1, "interpolation": "catmullrom",
                                     "data_points": [{"x": "math.sin(q.anim_time*90)", "y": 0, "z": 0}]}]}}}]}
        geo = _from_bbmodel(data)
        a = geo.animations["animation.x.idle"]
        self.assertTrue(a["loop"])
        self.assertEqual(a["bones"]["head"]["rotation"]["0"], [5, 0, 0])
        self.assertEqual(a["bones"]["head"]["rotation"]["1"]["lerp_mode"], "catmullrom")


class RigAndAnimationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.models = make_models(cls.tmp)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_quadruped_rig(self):
        geo = load_model(self.models / "emberpup.bbmodel")
        rig = detect_rig(geo)
        self.assertEqual(rig.head, "head")
        self.assertEqual(rig.jaw, "jaw")
        self.assertEqual(rig.gait, "quadruped")
        self.assertEqual(sorted(rig.eyes), ["eye_left", "eye_right"])
        self.assertEqual([t.bones for t in rig.tails], [["tail", "tail2"]])
        sides = {l.root: (l.side, l.front) for l in rig.legs}
        self.assertEqual(sides["leg_front_left"], (1, True))
        self.assertEqual(sides["leg_back_right"], (-1, False))
        self.assertEqual(rig.front_sign, -1)

    def test_bird_rig(self):
        rig = detect_rig(load_model(self.models / "skylark.bbmodel"))
        self.assertEqual(len(rig.wings), 2)
        self.assertEqual({w.side for w in rig.wings}, {1, -1})
        self.assertEqual(rig.gait, "biped")

    def test_rig_overrides(self):
        geo = load_model(self.models / "emberpup.bbmodel")
        rig = detect_rig(geo, {"tails": ["flame"], "head": "neck"})
        self.assertEqual(rig.head, "neck")
        self.assertIn("flame", [b for t in rig.tails for b in t.bones])

    def test_generated_molang_is_valid(self):
        geo = load_model(self.models / "skylark.bbmodel")
        rig = detect_rig(geo)
        anims = generate(rig, "skylark", Settings(can_fly=True, can_swim=True), [0, 0, 0])
        for want in ("ground_idle", "ground_walk", "sleep", "blink", "faint", "air_fly", "water_swim"):
            self.assertIn(want, anims.animations)
        bone_names = set(geo.bone_names())
        for name, a in anims.animations.items():
            for bone, chans in a["bones"].items():
                self.assertIn(bone, bone_names, name)
                for ch, val in chans.items():
                    vals = val if isinstance(val, list) else [v for kf in val.values()
                                                              for v in (kf["post"] if isinstance(kf, dict) else kf)]
                    for v in vals:
                        if isinstance(v, str):
                            compile(v.replace("math.", "").replace("q.anim_time", "1"), "m", "eval")

    def test_molang_eval(self):
        self.assertAlmostEqual(eval_molang("math.sin(q.anim_time*90)*2", 1.0), 2.0)
        self.assertAlmostEqual(eval_molang("5+math.abs(math.sin(q.anim_time*180))", 0.5), 6.0)

    def test_supplied_animation_wins(self):
        geo = load_model(self.models / "emberpup.bbmodel")
        rig = detect_rig(geo)
        mine = {"animation.whatever.idle": {"loop": True, "bones": {}}}
        anims = generate(rig, "emberpup", Settings(), [0, 0, 0], mine)
        self.assertIs(anims.animations["ground_idle"], mine["animation.whatever.idle"])
        self.assertIn("ground_idle", anims.supplied)
        self.assertNotIn("ground_idle", anims.generated)


class TextureTests(unittest.TestCase):
    def test_pure_python_png_roundtrip_and_hue(self):
        img = textures.RGBAImage(3, 2, [(255, 0, 0, 255), (0, 255, 0, 128), (0, 0, 255, 0),
                                        (10, 20, 30, 255), (200, 100, 50, 255), (0, 0, 0, 255)])
        saved, textures.Image = textures.Image, None  # force the fallback codec
        try:
            data = img.to_png_bytes()
            back = textures.RGBAImage.from_bytes(data)
        finally:
            textures.Image = saved
        self.assertEqual(back.pixels, img.pixels)
        shifted = img.hue_shift(120)
        self.assertEqual(shifted.pixels[0][:3], (0, 255, 0))
        self.assertEqual(shifted.pixels[2], img.pixels[2])  # transparent untouched
        swapped = img.palette_swap({"#ff0000": "#00ffff"})
        self.assertEqual(swapped.pixels[0], (0, 255, 255, 255))


class FullBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        models = make_models(cls.tmp)
        cls.project = cls.tmp / "Addon"
        quiet = open(Path(tempfile.gettempdir()) / "ce_test_out.txt", "w")
        old = sys.stdout
        sys.stdout = quiet
        try:
            assert cli_main(["init", str(cls.project), "--name", "Test Addon", "--namespace", "testmons"]) == 0
            assert cli_main(["add", str(cls.project), str(models / "emberpup.bbmodel"), "--types", "fire",
                             "--evolves-to", "blazehound @ level 32"]) == 0
            assert cli_main(["add", str(cls.project), str(models / "blazehound.geo.json"), "--types", "fire/dark"]) == 0
            assert cli_main(["add", str(cls.project), str(models / "skylark.bbmodel"), "--types", "normal/flying"]) == 0
        finally:
            sys.stdout = old
            quiet.close()
        cls.result = build_project(cls.project)
        cls.out = cls.project / "build" / "unpacked"

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def read(self, rel: str) -> dict:
        return json.loads((self.out / rel).read_text())

    def test_files_and_links(self):
        res = "resourcepack/assets/testmons/"
        for sid in ("emberpup", "blazehound", "skylark"):
            species = self.read(f"datapack/data/testmons/species/custom/{sid}.json")
            self.assertEqual(species["pokedex"], [f"testmons.species.{sid}.desc"])
            resolver = self.read(f"{res}bedrock/pokemon/resolvers/{sid}/0_{sid}_base.json")
            self.assertEqual(resolver["species"], f"testmons:{sid}")
            for var in resolver["variations"]:
                tex = var["texture"].split(":", 1)[1]
                self.assertTrue((self.out / "resourcepack/assets/testmons" / tex).exists(), tex)
            poser = self.read(f"{res}bedrock/pokemon/posers/{sid}/{sid}.json")
            anims = self.read(f"{res}bedrock/pokemon/animations/{sid}/{sid}.animation.json")["animations"]
            geo = self.read(f"{res}bedrock/pokemon/models/{sid}/{sid}.geo.json")
            bones = {b["name"] for b in geo["minecraft:geometry"][0]["bones"]}
            self.assertIn(poser["rootBone"], bones)
            refs = []
            for p in poser["poses"].values():
                refs += p["animations"] + p.get("quirks", [])
            refs += list(poser["animations"].values())
            import re
            for r in refs:
                m = re.search(r"q\.bedrock\w*\('(\w+)', '(\w+)'", r)
                if m:
                    self.assertIn(f"animation.{m.group(1)}.{m.group(2)}", anims, r)
                m = re.search(r"q\.look\('(\w+)'", r)
                if m:
                    self.assertIn(m.group(1), bones)
        lang = self.read(f"{res}lang/en_us.json")
        self.assertEqual(lang["testmons.species.emberpup.name"], "Emberpup")

    def test_evolution_chain(self):
        pup = self.read("datapack/data/testmons/species/custom/emberpup.json")
        hound = self.read("datapack/data/testmons/species/custom/blazehound.json")
        self.assertEqual(pup["evolutions"][0]["result"], "testmons:blazehound")
        self.assertEqual(hound["preEvolution"], "testmons:emberpup")
        self.assertLess(pup["nationalPokedexNumber"], hound["nationalPokedexNumber"])
        self.assertGreater(sum(hound["baseStats"].values()), sum(pup["baseStats"].values()))
        self.assertFalse((self.out / "datapack/data/testmons/spawn_pool_world/blazehound.json").exists())
        self.assertTrue((self.out / "datapack/data/testmons/spawn_pool_world/emberpup.json").exists())

    def test_flier_poser(self):
        poser = self.read("resourcepack/assets/testmons/bedrock/pokemon/posers/skylark/skylark.json")
        self.assertIn("fly", poser["poses"])
        all_types = [t for p in poser["poses"].values() if not p.get("isBattle") for t in p["poseTypes"]]
        self.assertEqual(len(all_types), len(set(all_types)), "a pose type is mapped twice")
        species = self.read("datapack/data/testmons/species/custom/skylark.json")
        self.assertTrue(species["behaviour"]["moving"]["fly"]["canFly"])

    def test_packages(self):
        names = [f.name for f in self.result.files]
        jar = next(f for f in self.result.files if f.suffix == ".jar")
        self.assertIn("BUILD_REPORT.md", names)
        with zipfile.ZipFile(jar) as z:
            n = set(z.namelist())
            self.assertIn("fabric.mod.json", n)
            self.assertIn("META-INF/neoforge.mods.toml", n)
            self.assertIn("pack.mcmeta", n)
            self.assertIn("data/testmons/species/custom/emberpup.json", n)
            self.assertIn("assets/testmons/textures/pokemon/emberpup/emberpup_shiny.png", n)
            fabric = json.loads(z.read("fabric.mod.json"))
            self.assertEqual(fabric["id"], "testmons")


if __name__ == "__main__":
    unittest.main()
