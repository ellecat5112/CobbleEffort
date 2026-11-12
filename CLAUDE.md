# CobbleEffort: project rules

Cobblemon sidemod (one jar for Fabric and NeoForge; all data and assets except the creative tab) adding cosmetic
forms via Cobblemon's cosmetic slot and aspects. Built against Cobblemon 1.8.4 / Minecraft 1.21.1.

## Rules that always apply

1. **Cosmetics cover whole evolutionary lines.** Never give a cosmetic to a single stage. Collection configs
   (`tools/collections/<name>.json`) list one species per line in `lines`. The generator expands each one to its
   full family (pre-evolutions, evolutions, branches) from Cobblemon's species data, and fails if any member can't be
   retextured. Don't hand-edit generated files; change the config/style and rerun the generator.
2. **Mirror every vanilla resolver variation** (shiny, female, regional, model swaps, layers) with the cosmetic aspect
   added, in Cobblemon's order, in an `order: 9000` resolver. Each style sets `EMISSIVE` ("disable" for Backrooms,
   "retexture" for Thanksgiving/Halloween). Styles may set `FRAMES`/`FPS` for animated textures (Halloween: 4 @ 5fps).
3. **Collections don't overlap**: a species is in at most one collection, and each collection has its own cosmetic
   item. New lines come from `generate.py pick` (random, fully modelled, unused), plus any lines the user asks for
   by name (put those in `lines` first, then `pick` the rest). The generator enforces no overlap.
4. **Every jar produced is delivered as a zip containing the .jar.** `./gradlew build` → `build/libs/<name>.zip`;
   the bare jar is only an intermediate in `build/tmp/jar/`. Hand users the zip, never a loose jar.
5. Generated textures are adaptations of Cobblemon assets (CC BY-NC 3.0), plus Mega Showdown's (CC BY-NC-SA 4.0,
   under `compat/mega_showdown/`): keep `CREDITS.md` accurate; non-commercial.
6. **Always build for the user's mod stack** (`tools/compat/mods.json`): Mega Showdown (+ Extra Megas, Ores),
   Cobblemon: AllTheMons x Mega Showdown, Cobblemon Baby Legends, Cobblemon Lost Lore, Legendary Monuments, Fully
   Hisuian Starters RP, Poke Costumes DP, Planeta Cobblemon free pack RP (bridged, below). The generator reads their jars from `tools/compat/jars/` (gitignored; ask the
   user for any that are missing, and never commit them). It merges species data (other mods' pre-evolutions and evolutions
   join families), retextures forms from `derivatives: true` mods, passes through forms from the others, pins
   model+poser on every copy, and vendors Cobblemon's model/poser/animations when a no-derivatives mod overwrites
   them. Members modelled only by a no-derivatives mod go under `painted` in mods.json.
   **Never name a model another mod/pack provides** in a resolver: Cobblemon loads every named model at startup and the
   game hangs on the Mojang loading screen if one is missing (data packs' and disabled resource packs' assets never
   load). Only `cobblemon:` models Cobblemon ships, or `cobbleeffort:` copies (Vendor), are allowed. Posers too (they're
   resolved at render time). The generator (`check_launch_safe`) and `validateData` enforce it. When a mod is added to the
   stack, add it to mods.json and rebuild everything.
   **Old-layout resource packs** (`bedrock/models|posers|animations|species`, e.g. Planeta Cobblemon): Cobblemon loads
   that layout first into the same names, so their meshes lose to any mod's while their textures win (scrambled).
   Mark them `"bridge": true` in mods.json (last): `tools/bridge.py` turns the user's copy into a current-layout pack
   (files at every competing path, its resolver at the lowest order, other resolvers for those species cut to forms
   with their own mesh) in `build/bridge/` (also run by `generate.py build`), never committed or shipped, and Stack
   sees that layer as its bridge so cosmetics vendor the models it replaces. Hand the user the bridge zip.

## Workflow

- Collections: `tools/collections/<name>.json` (aspect, feature, style, cosmetic_items, lines, optional `line_styles`)
  + `tools/styles/<style>.py` (`retexture(base, eyes, seed, shiny, frame=0, layer=False)`, `EMISSIVE`, optional
  `FRAMES`/`FPS`). `layer` is False for body textures, "emissive" or "plain" for layers. Optional
  `EXTRA_LAYERS` (list of {name, emissive, translucent, frames, fps}) + `extra_layer(name, base, eyes, seed, shiny,
  frame) -> Image | None` adds style-owned layers (named `cobbleeffort_<name>`), e.g. Christmas lights.
- Sprite collections (`"mode": "sprite"`, no style; `tools/sprites.py`, Game Boy Sprites): the model itself is
  replaced. For every union of the species' variation aspect sets, what Cobblemon resolves (model, poser, texture) is
  posed (standing pose's animations at t=0, transformedParts hidden), software-rendered front/back at 1 px/unit in
  depth slices, quantised to Game Boy tones (GBC palette from the shiny texture), and written as a layered plane model
  (`cobbleeffort:gb_<model>_<digest>.geo`) + poser (`cobbleeffort:gb_<poser>`, original portrait framing) + our
  animation group `cobbleeffort_gbsprite`; each copy pins all three and switches every layer off (no passthrough:
  their model can't be named). Preview manifests carry `retextured_model`; render.js uses it.
- Shared helpers: `styles/_horror.py` (Halloween), `styles/_festive.py` (Christmas), `styles/_spring.py` (Easter),
  `styles/_animatronic.py` (FNAF; one thin `fnaf_<look>.py` module per look).
- `WANTS_HINTS = True` on a style makes the generator pass `hints=` (from the model's `.geo.json`: `tex_size`,
  `head_front`, `head_top`, `torso_front` rects in geo UV units). Many Cobblemon models have separate eye cubes, so
  don't locate a face from the eye mask; use the hints. `WANTS_HEIGHTS = True` passes `heights=` (a float array the
  size of the model's texture in geo UV units: each texel's height on the model, 0 bottom to 1 top, NaN if unused),
  for effects that must line up across the whole body (Trans Pride's flag stripes).
- `addon_lines` in a collection config: cosmetics for Pokémon modelled by another mod (e.g. Xurkitree from ATM x MSD /
  Ultra-Beasts). Never copy or recolour another mod's art unless its licence allows it. Extract only the UV layout
  (`tools/addons/extract_layout.py`, run with `python3 -I` from outside their checkout) and paint an original texture in a
  builder (`tools/addons/<name>.py`: `build(out_tex_root, aspect, mod_id) -> (variations, manifest_entry)`).
  Disable their glow layers by name if the texture changes.
- When a requested Pokémon isn't modelled by Cobblemon, check the stack's mods first (ATM x MSD models many,
  e.g. Xurkitree), then other public mods (e.g. Cobblemon Ultra-Beasts).
- Regenerate: `python3 tools/generate.py --cobblemon <cobblemon>/common/src/main/resources build [collection]`
  (needs `assets/cobblemon` incl. posers/animations + `data/cobblemon`, the compat jars in `tools/compat/jars/`
  (Lost Lore: a directory of its `common/src/main/resources`), and Cobblemon's Kotlin sources next to the resources
  for converting Kotlin posers). The output is deterministic, so check reruns with md5.
- Release zips also contain `README.txt`, the player guide (`dist/README.txt`, written by `tools/make_readme.py` at
  the end of every `generate.py build` from each config's `readme` block and `tools/readme/<name>.json`). A new
  collection needs a `readme` block (number, title, example, summary, looks, optional specials/warning).
- New Pokémon (species Cobblemon has data for but no model): one builder per species in `tools/models/<name>.py`
  using `tools/models/_voxel.py` (OBJ/mesh -> voxels -> boxes -> box-UV texture; Cobblemon only supports box UV, laid
  out as vanilla's ModelPart; `load_mesh` reads GLB/glTF, textured OBJ zips and low-poly meshes, `pip install scipy
  trimesh`). Ask the user for Tripo exports as GLB with a reduced face count (~20k faces is plenty at this voxel
  size and fits the chat upload limit). Commit the voxels npz, not the source mesh. All ids in the cobbleeffort namespace, the
  animation group `cobbleeffort_<name>`; `species_additions` sets `implemented`; spawns in `spawn_pool_world`.
  Never copy another pack's model/art without a licence or written permission (the user's own models are fine).
  Cobblemon-style cleanup (all builders): `vx.keep_largest` drops loose bits a generated mesh carries (not for
  models made of separate pieces), `vx.smooth` (blurred SDF, keeps parts up to 2 voxels thick, never splits a
  piece), `vx.fit_bone_boxes` (fewer, chunkier boxes; or `vx.fit_budget(bone, n, MAX_CUBES, lam, weights)` for a cube
  limit: candidate boxes at several tolerances/grids, greedy non-overlapping pick, then growth) and
  `vx.paint_box_shaded` with `vx.exposure` (lit tops, side
  gradients, darker silhouette/crease edges; one-voxel stair steps don't count as edges). Keep per-voxel noise tiny.
- **CobbleEffort's own Pokémon** (original species, the user's idea and look; I write names, Pokédex entries, stats,
  moves): `tools/newmons/build.py [--showdown <cobblemon>/data/cobblemon/showdown.zip]` (the flag checks every move
  and ability). SPECIES config (dex from 3001: the stack uses none of 3000-3999; types, abilities, stats, learnset, TMs,
  egg moves, evolution, drops, spawns, entry, how-to-get), one hand-built box model per species in
  `tools/newmons/models/<name>.py` on `tools/megas/_boxmodel.py` (`K` texels per unit: `paint(..., k=K)` makes the
  image K times the geo's texture size so faces stay sharp) + the shared rig `tools/megas/_rig.py` (animations/poser
  from bone names, also used by the megas). Species `cobbleeffort:<name>` in `data/cobbleeffort/species/<line>/`,
  dex entries + the `cobbleeffort:cobbleeffort` sub-dex added to `cobblemon:national` (dex_additions), spawns in
  `spawn_pool_world`, lang `cobbleeffort.species.<name>.name|desc`, resolver order 0, README table between
  `<!-- newmons -->` markers, player guide from `tools/readme/_new_<name>.json`. Lines so far: dentistry (Cavitot ->
  Amalgum lv 24 -> Orthodread lv 42; Dark, Dark/Steel; shiny = minty enamel + gold metal; `models/_teeth.py`).
- Paradox megas: `tools/megas/build.py --cobblemon <res>` (switches off every layer the stack's resolvers give the base
  form, since Cobblemon merges layers by name into the mega; config for all 22 in MEGAS: types, ability, stats = base + 100 with Ancient
  odd / Future even, stone, recipe, dex text). One hand-built box model per mega in `tools/megas/models/<species>.py`
  on `tools/megas/_boxmodel.py` (bones + boxes placed by coordinate, front = -z; `round_box` for rounded parts;
  zero-thickness planes with cut-out shaders for feathers/moss/frills; `rod`/`chain`/`spike` aim boxes along a
  direction for tusks, horns, tails; shaders paint each texel from its model-space position, clean colours + soft
  baked shading, no noise; glow by returning (colour, glow)). Module: `build()`, SCALE, HITBOX, KIND, LOOK, optional
  ANIM; own SHINY palette. Only species with a module are built; the build writes data, stones, lang, creative tab,
  README table and readme json. Design from the official art (Fandom wiki, `pokemon.fandom.com/api.php`); never copy
  ATM x MSD's models (no derivatives). Brute Bonnet's mega is prototaxite-inspired (user's request).
- New lines: `python3 tools/generate.py --cobblemon ... pick --count 18 --seed <text>`.
- Creative tab (the only code, `src/main/java`): Minecraft has no data-driven tabs, so `CreativeTab.java` builds one by
  reflection with every Minecraft name given twice (Mojang for NeoForge, intermediary for Fabric; check new ones against
  the 1.21.1 mappings), started by `fabric/CobbleEffortFabric` (entrypoint) and `neoforge/CobbleEffortNeoForge` (`@Mod`,
  `javafml`). It compiles against the JDK plus `src/stubs/java` (loader stand-ins, never packaged), and every failure
  only logs. Its items: `cobbleeffort_creative_tab.json` from `tools/make_creative_tab.py` (run by `generate.py build`),
  so new collections' items join the tab automatically. Keep any further code
  this way (no loader-specific builds).
- **CobbleEffort: Distortion** (`distortion/`, a separate add-on jar; design in `docs/distortion_design.md`): the
  "Distortion" battle gimmick (types turn into their weaknesses, TYPE_CHART in `distortion/tools/make_assets.py`).
  Unlike CobbleEffort it's a real code mod, an Architectury build (common/fabric/neoforge, mojmap) against
  Cobblemon 1.8.4, Mega Showdown 1.3.3, Accessories and Architectury API (all required); its own `./gradlew build` in
  `distortion/` -> `build/libs/cobbleeffort-distortion-<v>.zip` (both jars + README + LICENSE, CC BY-NC-SA because its
  textures adapt Mega Showdown's). Items via Architectury registries; the accessory slot, Distorted forms (aspect
  `distorted`, appended forms so `getForm` picks `<form>-Distorted`), resolvers and recoloured textures are written by
  `tools/make_assets.py` (DISTORTABLE: Giratina, Dialga, Palkia, Arceus incl. Origin and plate forms; every other Pokémon with a Cobblemon/MSD model, whole lines (THEMED_LINES in `parts/themed_lines.json`, `parts/themed.py` + `parts/_themes.py`: looks from each form's NEW types, one motif per type placed by bone names; Gen 1 in 0.9.0, the rest in 0.12.0); the Gen 2 legendaries and mythicals; every starter line
  Gen 1-9 (STARTER_LINES), no stone megas/primals; inputs: COBBLEMON_JAR + the MSD jar in `tools/compat/jars/`). Gen 2-9 starters' TYPES are random per line since 0.12.0, Gen 1's keep the chart (CHART_STARTERS; `make_assets.starter_charts()`: seeded per line, never own/chart type; also CHART_OVERRIDES in make_battle, `distortChartBySpecies` in the engine, ability twins keyed "Species:Types"; their twins get generic names). Starter looks:
  water -> plant-inspired, grass -> natural disasters, fire -> sea life (the user's direction; Squirtle prototaxites,
  Bulbasaur raging flames, Charmander mermaid). One module per line in `tools/parts/<first stage>.py` (LINE, build(kit),
  RECOLOUR type-hue shift, optional UNIFY/GLOW_DST) on the part kit (`parts/_kit.py`: hide/reskin/box/plane/cross/flat,
  upright()/wbox() for rotated bones, UVs in an added texture area, animated layers; `parts/_materials.py`). Mirrored
  variations resolve model/texture/layers like Cobblemon (female/Hisuian model swaps pinned, per-model parts). Preview
  with `tools/preview` + `EXTRA_MODEL_ROOTS`/`CAM_UP`. One Distortion Crystal for every Pokémon (Arceus uses its plate).
  Battle (`tools/make_battle.py --showdown <dump_showdown.js output> --cobblemon-jar <jar>`): twin moves and type-bound
  ability twins (existing exact match, e.g. Blaze -> Torrent, or generated from the code: Solar Power -> Storm Power)
  as Cobblemon datapack moves/abilities (`data/<ns>/moves|abilities/*.js`), Mega Showdown scripts (`side`/`queue`/`actions`: choice `move N distort`, a queued distort
  action at Tera priority, forme change + move swap), `MoveActionResponse.isValid` mixin (band), client Distort button
  mixin on `BattleMoveSelection`, `AIDistortMixin` (wild/NPC AI actors distort on their first move; the side script
  turns a disallowed distort into the plain move so AI choices never fail). Since 0.6.0 distortion is a free toggle
  (distort/revert any turn) and the engine keeps the real species (`pokemon` script re-inverts types on setSpecies;
  `-formechange` "<species>-Distorted"/"-Reverted" drive the aspect), so item-free form changes stack (Gmax, Ash-
  Greninja, move megas); only forms needing a held item (stone megas, primals) are skipped. The add-on's resolvers may
  name Mega Showdown's models (a required dependency), e.g. its Gigantamax models. Test the engine in node against Cobblemon's Showdown + MSD's patches before a build, loading scripts and held items the way MSD does (`content.replace("\n", "")`: lines joined with no separator, so no `//` comments in generated JS; `make_battle.write` strips them).
  Distortion Crystal ore (0.12.0; stone + deepslate, coal heights, 2-4 Distortion Shards, stone pickaxe; worldgen via Architectury BiomeModifications; recipes for crystal and band): `tools/make_ore.py`.
  DNA machine (0.11.0, the user's design: Mew DNA from battles with Mew in the party + Mew -> Mewtwo in 5 min): `dna/` package + `client/DnaMachineRenderer` (display PokemonEntity in the tank) + `tools/make_dna_machine.py` (its assets/data).
  Wheel (radial menu): Cobblemon's `POKEMON_INTERACTION_GUI_CREATION` event (as Mega Showdown does; no mixin) adds
  Distort/Revert, a C2S `DistortPacket` toggles the `distorted` flag feature server-side (`DistortionWheel`); rules shared
  in `DistortionRules`. Phases 1 items/slot/forms, 2 battle gimmick, 3 radial entry: all done.
  Specialised distortions (user designs): TYPE_OVERRIDES (make_assets) + CHART_OVERRIDES (make_battle; per-species twin
  tables in the engine and move_twins.json {"default", "species"}): Mew and Mewtwo Normal/Fighting (Mew: placenta orb +
  umbilical tail; Mewtwo: translucent pink Conkeldurr arms + bulk). Parts may use RECOLOUR "keep", kit.rotate_bone,
  kit.bulk, translucent non-emissive layers (Membrane, Muscle); the kit widens the texture when a part needs it.
  RECOLOUR "negative" (Lugia). A Pokémon modelled only by a no-derivatives mod (Celebi: ATM x MSD) gets an ADDON module:
  paint(layout, shiny) on its extracted UV layout (`parts/layouts/`), texture-only resolver (names no model).
- **CobbleEffort: Kanto** (`kanto/`, a third add-on jar, the user's design; built like Distortion: Architectury,
  requires Cobblemon + Distortion for the crystal; `./gradlew build` in `kanto/` -> `build/libs/cobbleeffort-kanto-<v>.zip`).
  Stage 1 (0.1.0): Gen 1 Bricks (black/white/grey), a Gen 1-styled lab (original layout, `tools/make_assets.py` writes
  its structure NBT) joined to every village's house pool at server start (`StructureTemplatePoolAccessor`), Essence of
  Olde (5% from Gen 1 Pokémon defeated in battle), Kantonian Orb (crystal + essence, 16 uses) waking the glitchy PC,
  which teleports to the `cobbleeffort_kanto:kanto` dimension (large-biome terrain; arrival pad with a return PC;
  return position in SavedData) where non-Gen-1 spawns become a same-type Gen 1 Pokémon (ENTITY_SPAWN). Stage 2 (0.2.0):
  8 gyms + the Elite Four hall (LEADERS/ELITE in make_assets: original leaders, Gen 1 teams; templates + `kanto/sites.json`;
  Cobblemon NPC classes, dialogues, recoloured trainer.png variations), built by `KantoGyms` on first arrival (one per
  tick, foundation, doors face the centre, NPCs spawned invulnerable), badges on BATTLE_VICTORY, Elite Four gated on 8
  badges in BATTLE_STARTED_PRE, Champion Ribbon; `/kanto gyms|rebuild`. Stage 3 (0.2.0, `tools/make_kantonian.py`):
  Kantonian ore (iron's bands x1.2, Kanto only via the `cobbleeffort_kanto:in_kanto` placement filter), raw/ingot/block,
  armor (`KantoArmor`, one armor material per outfit; dye or wool in the shape's gap picks the outfit).
  0.3.0 (`tools/make_regions.py`, the user's design): Johto..Paldea, a dimension each (`Region` enum: dex ranges; spawn
  swap generalised in KantoEvents; dimension type shared with Kanto; per-region multi_noise biome lists, noise settings:
  amplified Sinnoh, large-biome Galar/Paldea, own sea levels for Hoenn/Alola) and a landmark each (jigsaw structures
  from single templates, biome tags, random_spread sets; built by Python builders on `S` shape helpers) holding the
  region's portal block (`Regions` + `RegionPortalBlock`: Plain/Facing/Tall/Parts; any block of the statue, ball or
  telescope works): pagoda bell, cave Groudon statue, manor basement boarded doorway, castle golden wardrobe
  (Magearna engraving), factory giant Poké Ball, observatory telescope, giant tree's engraved bark (300 tall from root
  tip: starts 60 below ground, terrain_adaptation none), academy PC. `KantoTravel.travel(player, region)`: home from
  inside, else arrival pad with a return portal. Previews: voxel renders (instanced three.js) of each template.
  0.4.0 (`tools/make_leagues.py` + `make_league_teams.py` -> committed `tools/league_teams.json`): every region's own
  league: 8 gyms + Elite Four (original names in NAMES, teams from that generation's dex by type and strength),
  `sites_<region>.json`, `gym/<region>_<type>.nbt`, badges `<region>_<type>_badge` + `<region>_champion_ribbon`
  (registered from `kanto/league_items.json`); KantoGyms keys roles/badges/ribbons by Region; sites build via a
  non-persistent chunk ticket (Job queue) so chunk generation never blocks a tick (the watchdog killed a synchronous
  version). `/kanto gyms [region]`, `/kanto rebuild [region]`.
  0.5.0: Region.HISUI (`allows(Species)`: Sinnoh dex + 899-905 + anything with a Hisuian form, spawned Hisuian;
  large-biome Hisui biomes), landmark `hisui_mountain` (shell mountain with a cavern core, spiral path, summit ruins,
  `arceus_statue` = portal `hisui_arceus_statue`); sites may carry `bosses` (KantoGyms: giant uncatchable wild
  Pokémon tagged `cobbleeffort_kanto_boss` = site id, glowing + particle aura, respawn 3 min after defeat when a player
  is near, rewards on BATTLE_VICTORY of the wild actor): Hisui's five frenzied Nobles (seals, Hero Ribbon) and
  Alola's eight totem trials (league_teams.json `alola_totems`, trial stamps = the alola badge ids, MSD Z-Crystals).
  Built SavedData has a per-region `layout` (layoutOf): a changed layout rebuilds that region (Alola gyms -> trials).
  `/place structure` anchors a piece at the given position (not centred) and needs every chunk it may touch loaded;
  `fill ... replace X` with X itself reports nothing changed, so count blocks by replacing them with another block.
  Copying a log's properties (`ofFullCopy(DARK_OAK_LOG)`) copies a map colour that reads `axis`: override mapColor.
  No replicas of the games' maps and no official characters or outfits: original, Kanto-inspired designs only.
  **Fabric remapping**: `fabric/build.gradle` (Kanto and Distortion) needs `modCompileOnly com.cobblemon:fabric`, or
  vanilla methods called on Cobblemon classes (`PokemonEntity.level()`, `NPCEntity.moveTo`) stay unmapped and throw
  NoSuchMethodError on Fabric only. Test on a real server: a Fabric server in the scratchpad (loader 0.17.2 launcher,
  loom's cached minecraft-server.jar, owo-lib from maven.wispforest.io) with commands piped through a fifo.
- Build and check: `./gradlew build` (runs `validateData`). Bump `mod_version` in `gradle.properties` per update.
- Preview renders: `tools/preview/` (three.js in headless Chromium; `node render.js <cobblemon-res> ../../src/main/resources out manifest_<aspect>.json`;
  `EXTRA_ROOTS=<extracted jar>:...` for other mods' forms; manifest entries with `form` are other-mod forms).
