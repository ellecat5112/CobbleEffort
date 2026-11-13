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
3. **Each collection has its own cosmetic item** (unique across collections; the generator enforces it). Until #23
   collections never shared species; the unused lines then ran out, so since #24 they may overlap (the user's call):
   `generate.py pick` (random, fully modelled) takes never-used lines first, then the least-used. Lines the user asks
   for by name go in `lines` first, then `pick` the rest.
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
  Numpy-painted collections share `styles/_fx.py` (`make(painter, look, animate, paint_layers)`; paint_layers also
  paints plain layers and emissive layers covering >15% of the texture): Deep Sea `_abyss.py`, Arc Light `_arc.py`
  (`bolts()` = branching arcs, re-struck per frame in `animate`), Abyss `_void.py` (`void_*`; the void, not the sea),
  Ancient Ruins `_ruins.py` (`courses()`, `glyphs()`; not Stone Statues), Gilded `_gilded.py` (shiny = platinum).
  Glacial `_glacial.py` (not Ice Sculptures), Kitsune `_kitsune.py` (`face_marks()` from face hints; foxfire = top of
  the height map). Cosmetic items must be unique across collections (incl. multi-item ones; generate.py checks), and
  not one Cobblemon itself uses as a cosmetic for one of the species (e.g. its dyes: Gengar takes pink dye). #24-28:
  Super Mario `_mario.py` (eyes keep their colours; shiny = the other power-ups), Nimbus `_nimbus.py` (`clouds()`),
  Pajama `_pajama.py`, Pinkan Island `_pinkan.py`, Prismatic `_prism.py` (shiny = black opal).
  #29-33: Sakura `_sakura.py` (blossoms at least 2.2 px), Shadow `_shadow.py` (Colosseum/XD), Slayer `_slayer.py`
  (Demon Slayer-inspired haori + breathing), Sunburst `_sunburst.py` (`sun_*`), Toxic Chain `_toxic.py`.
  #34-38: Undertale `_undertale.py` (`soul_*`; `heart()` shared), Pokemon Unite `_unite.py` (purple team, shiny
  orange), Zelda `_hyrule.py`, Valentine's Day `_valentine.py`, St. Patrick's Day `_patrick.py`.
  #39-41: April Fools' Day `_fools.py`, Star Wars `_galaxy.py`, LGBTQIA+ Pride `_pride.py` (flags by height, like
  Trans Pride #10).
  Patterns must read at u = 1 (one texel per model unit): test the small textures, not just the big ones.
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
  `<!-- newmons -->` markers, player guide from `tools/readme/_new_<name>.json`. Layers come from the shaders: a glow
  colour -> emissive `cobbleeffort_glow` layer (3 flicker frames); an alpha between 0 and 255 -> translucent
  `cobbleeffort_shell` layer (cut out of the base texture; listed after the glow so the shell doesn't hide it). Rig:
  `spin*` bones turn round z in battle idle and fast in physical moves (gun drums). CUSTOM_MOVES -> Cobblemon datapack
  moves `data/cobbleeffort/moves/<id>.js` (`Object.assign({}, Dex.data.Moves[base], {...})`, lang `cobblemon.move.<id>`);
  test them in node against Cobblemon's Showdown, sending the species as Cobblemon does (id `cobbleeffort<name>`,
  name `cobbleeffort:<Name>`). Starters: data-pack categories in `data/cobbleeffort/starters/`; Cobblemon shows ONLY
  data-pack categories once any exist (default `useConfigStarters=false`), so STARTER_CATEGORIES ships its built-in
  regions (copied from its default config) plus ours (OUR_STARTERS). Lines so far: dentistry (Cavitot -> Amalgum lv 24
  -> Orthodread lv 42; Dark, Dark/Steel; shiny = minty enamel + gold metal; `models/_teeth.py`); coal butterfly, the
  starter (Coalarva -> Cinderoon lv 16 -> Gatterfly lv 36; Fire/Bug; Blaze / Skill Link; translucent ash cocoon with
  the larva inside; Gatling arms; Machine Gun Stinger; shiny = blue fire; `models/_coal.py`); mantis (Prayling ->
  Mawntis lv 22 -> Mantasma lv 40 at night; Grass/Bug, Grass/Ghost; eyeless; ability Blindsight = its own moves always
  hit, incl. semi-invulnerable targets; shiny = orchid pink; `models/_mantis.py`). CUSTOM_ABILITIES -> Cobblemon
  datapack abilities `data/cobbleeffort/abilities/<id>.js` (raw Showdown ability object, lang `cobblemon.ability.<id>`);
  an `evolve` tuple may carry a 4th item: extra requirements (e.g. `time_range` night). The mantis reference is a
  free-to-use picture found online (untagged; its labels Blygentom/Briartom/Xygenthorn are the fakemon's names, not an
  artist tag); the user's description led, and our names and models are our own.
  Mummy line, the water starter (Mumpillar -> Sarcoon lv 16 -> Pharantis lv 36; Water/Bug; ability Pharaoh's Curse:
  once per battle (`target.m.pharaohsCurse`) a KO hit leaves it at half HP, healing up to half if lower, +2 Atk/SpA;
  hidden Torrent; shiny = turquoise + rose gold; `models/_pharaoh.py`); OUR_STARTERS holds Coalarva and Mumpillar.
  Route one (#3013-3023, line "route_one", `models/_route.py` helpers + `_knife.py`, `_cardinal.py`, `_radish.py`):
  Pipider -> Blanketula (Bug/Grass, 14), Shivnymph -> Sheathalis -> Cutlassfly (Bug/Steel, 7/10, floater with blade
  wings), Cardling -> Rubraptor (Fairy/Flying, 22), Squeakling -> Elastigoose (Water/Flying, 25, "swims": surface
  spawns), Raddent -> Rattlebunch (Grass/Normal, 20). Plane parts (leaves, blades, feathers) are edge-on from the
  side: tilt them (rotation) so their faces show. Rod boxes run along -z before rotating (`along()`).
  Fossils (#3024-3027, line "fossil", `tools/newmons/fossils.py`, data only): fossil items are echo shards with
  custom_data `{cobbleeffort_fossil: <key>}` + name/lore/custom_model_data icon (overrides in
  `assets/minecraft/models/item/echo_shard.json`); Cobblemon fossil entries match them with the legacy predicate
  `{"item", "nbt"}`. Found by brushing suspicious gravel (archaeology loot tables) in our structures: `tar_pit`
  (underground y -34, tar pool by lava) and `spire_stump` (forests/swamps); templates via the Kanto NBT writer.
  Fossil items join the creative tab via `tools/newmons/creative_items.json`. Petroleodd -> Petroleossil (Rock ->
  Rock/Dragon, lv 45 holding a King's Rock, `consume`; design by @aalacer398, with permission, names kept); Mycolith ->
  Taxitower (Rock/Poison, lv 38; Gemini's Prototaxites idea; ability Paleomycelium = Grass forceSTAB + immune to
  powder/Leech Seed; move Devonian Drift = a foeSide condition, raw JS move with its own `condition` and battle lang
  `cobblemon.battle.sidestart|sideend.ally|opponent.<id>`, `cobblemon.battle.damage.<id>`). A CUSTOM_MOVES entry
  with "js" is a whole move; without, it's Object.assign on "base". Real bucket pickup (a tar fluid) would need code.
  Jerboa mice (#3028-3029, `models/_jerboa.py`; design by NyonTox, with permission): Jerbolt -> Mesmerboa
  (Electric/Psychic, `evolve_stone` = item_interact with a Thunder Stone), floaters whose tail is a `ring` bone: a
  circle of rod segments banded yellow/violet (violet glows) + a bolt plane; the rig turns `ring*` bones round z in
  idle (slow), walk and battle (faster).
  Land sharks, the pseudo-legendary (#3030-3032, `models/_landshark.py`: polygon fins, flame-tongue planes, translucent
  smoke): Sharkindle -> Forgnash (40) -> Magmalodon (60), Steel/Fire, `growth: slow`, 300/420/600.
  Jormbuoy -> Jorminous (#3033-3034, `models/_jorm.py`; Zorneo x Norden region series, creators' permission, names
  kept): Water -> Water/Ghost by Dusk Stone at level 45+ (`evolve_stone` with a 4th item: extra requirements),
  `aquatic` (swims, breathes underwater), surface spawns on oceans; oars are `oar_*` bones (they sway).
  Type: Error (#3035, `models/typeerror.py`): species type Normal, ability System Error makes it the "Error" type in
  battle (onEffectiveness: neutral except Normal = 2x; onNegateImmunity for Ghost; its Normal moves get
  ignoreImmunity + their own onEffectiveness: 2x on Normal, else neutral). Genderless (`male: -1`), catch 3.
  Tanhyll (#3036, `models/tanhyll.py`; the art's own name): Normal/Fighting anteater, ability Insectivore (its
  attacks' onEffectiveness = 4x on any Bug-type target, plus onAnyNegateImmunity for Bug targets of its own attacks);
  Cobblemon's Showdown reports 4x hits as `-extremelyeffective`.
  Tikimp -> Tikilla (#3037-3038, `models/_tiki.py`): Normal/Fighting kickboxing apes (skull face, tiki-mask fists), lv 32.
  Mousense -> Sensarat (#3039-3040, `models/_sense.py`; the art's names): Normal rodents with eyes always closed, lv 22;
  `_sense.whisker` = thin whisker ribbons (a 0 x 1 rod cut to a tapering line; plain rods under 1 unit round to nothing).
  Gigantler (#3041, `models/gigantler.py`; art by @rontoregion, name kept): Normal moose, three palmate crown antlers
  (palms = wide flat rods aimed along the palm, `t2` = palm height; lobed `tine`s); LIFT raises all non-leg boxes for long legs.
  Assoulsect (#3042, `models/assoulsect.py`; art by @mazenta_inku, name kept; the user's idea: fallen Bug Pokémon
  bound into a hive mind by Ophiocordyceps): Bug/Ghost, genderless, undiscovered, single stage; ability Hive Mind
  (`onTryHit`: a Bug-type foe's move on it is cancelled with `-activate`; a damaging one hits a random active member
  of the attacker's own side via `this.actions.getDamage(source, victim, move)`; battle lang via the ability's
  "battle" dict); hidden Effect Spore. Fog = `clump()` stacks, translucent soul wisps (shell layer), `cordyceps()`
  stalks with glowing tips; extra head bones `head_top`/`head_mask`/`head_green` sway.
  Capybrute (#3043, `models/capybrute.py`; art by @Kai_FakemonsR, name kept; capybara/marmot): Ground/Fighting,
  Guts / Thick Fat / Unaware; a domed back built as front-to-back slices under a dome curve (smoother than stacked
  tiers), `slash()` markings, low head with buck teeth.
  **Regional forms** (`tools/newmons/regional.py --cobblemon <res>`, standalone): aspect `cobbleeffortian` (flag
  species feature + assignment), form "CobbleEffort" appended via species_additions (Cobblemon appends `forms` and
  `evolutions`; getForm picks the last form whose aspects all match), types/abilities/moves/pokedex/evolutions per form
  (evolution results "<next> cobbleeffortian"), texture-only resolvers at order 5 in `resolvers/regional/` (Cobblemon's
  models stay; female/regional model swaps below still apply; cosmetics at 9000 win), textures recoloured from
  Cobblemon's by HSV rules + warning `spots()`, spawns in `spawn_pool_world/regional_<line>.json`, README section by
  hand. Lines: Caterpie/Metapod/Butterfree (Bug/Poison, art by @MerphISC for Caterpie; shiny electric blue + orange).
  Writhing Rot (#3044, `models/writhingrot.py`; the user's art, artist not named, also "Infestower"): Bug/Dragon
  ancient paradox of Sudowoodo, Protosynthesis, genderless, labels ["paradox"]; hollow log body (`hollowf` ringed
  front), grub neck/feelers/tail from `segment_chain()` (per-rod `segf(az)` seams every 2.2 units), head bone under a
  `neck` bone so it follows the neck. Cobblemon 1.8.4 has no Booster Energy item (don't use it in drops).
  Wrapiglet -> Croissoar (#3045-3046, line "blanket", `models/_blanket.py`; r/fakemon art, artist not named; our
  names): Normal -> Normal/Flying at 26, pigs in a blanket; Croissoar is a floater whose paraglider (`cap` bone) is
  one continuous arch of slabs placed round a circle (each rotated by its angle about its own centre), ears = wings.
  Minnolith -> Placofin (#3047-3048, line "minnow", `models/_minnow.py`; art by Fionn Keeley, our names): Rock/Water
  fossils, level 38, aquatic; Minnow Fossil (fossils.py key "minnow", cmd 3) from the `riverbed` structure: a 2-layer
  bed (only its own blocks set, so the water stays) at OCEAN_FLOOR_WG with start_height -1 in rivers and swamps.
  Engine tests for our moves/abilities: node scripts against Cobblemon's Showdown (team string field 4 = current HP).
  Egg groups are Cobblemon's ids (`water_1`, not `water1`): a wrong one stops the server at startup; build.py checks them.
  **Reference pictures for new Pokémon** (user's rule): unless the user says a picture is paid for or licensed, treat
  it as shared in good faith from a free source (fakemon art posted as free to use) and use it as the design
  reference without questioning it. Credit the artist in CREDITS.md when the user names one. Models are still built
  by hand from the description and picture; no pixels are copied.
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
- **CobbleEffort: Fusion** (`fusion/`, a fourth add-on jar; Infinite Fusion's DNA Splicers and head/body rules, the
  user's request; built like Kanto: Architectury, requires Cobblemon + Architectury API, recommends CobbleEffort;
  `./gradlew build` in `fusion/` -> `build/libs/cobbleeffort-fusion-<v>.zip`; `tools/make_assets.py` writes item
  textures/models, lang, recipes). Items (`SplicerItem`): DNA Splicers (average level, used up), Super Splicers (higher
  level), Infinite Splicers (never used up), DNA Reversers (swap head/body); picking a fusion with splicers unfuses it.
  Party picks via `PartySelectCallbacks`; not in battle. The fusion is the BODY's Pokemon object; the head is forced
  aspects `fusion_head=<species id>` + `fusion_head_aspect=<aspect>` (saved + synced), and the whole head NBT plus the
  body's ability/nickname sit in `persistentData["cobbleeffort_fusion"]` (`Fusing`: fuse/unfuse/reverse, overloads
  taking party/PC/registry access so `/fusion selftest` (ops) runs them in a scratch party). Rules (`FusionRules`): HP,
  SpA, SpD = (2 head + body)/3, Atk, Def, Spe = (2 body + head)/3; types = head's primary (Flying for Normal/Flying
  heads) + body's secondary or only type, a duplicate becomes the body's primary; name = head's first half + body's
  last half; ability = body's, clickable choice of the head's (`/fusion ability <uuid> head|body`); the head's moves
  become benched moves. Stats/types outside battle: mixins on `CobblemonStatProvider.getStatForPokemon` and
  `Pokemon.getTypes/getPrimaryType/getSecondaryType` (aspects can be null while a Pokemon is constructed: guard).
  Battle: `FusionEngine` evals JS into the Graal Showdown context by reflection (wraps `Pokemon.prototype.setSpecies`,
  table `__ceFusion[uuid] = {base, types}`; composes with Distortion's instance script), registered on fuse and in a
  static HEAD mixin on `BattleRegistry.startBattle`; tested in node (`fusion_sim`-style: Water Gun not super effective
  on a Bulbasaur-head Charmander). Look (client, `FusionRender` + `PosableModelMixin` on `PosableModel.render`): the
  body model's `head` bone is hidden and the head species' `head` ModelPart drawn on the body's head joint (bone chain
  transforms), scaled to the replaced head's size (0.5-2.5x), with the head's own texture/aspects; models without a
  `head` bone show the plain body. Custom per-pair forms: later (the user's plan).
  **Fusion designs (0.2.0, the user's call: "use the Infinite Dex to decide the designs")**: colours, names and credits
  from Pokémon Infinite Fusion's custom sprites via infinitefusiondex.com (hosts allowed in the environment: the site +
  `ifd-spaces.sfo2.cdn.digitaloceanspaces.com`; the user OK'd reading the sprites). Its API: `/api/filter?page=N&base=0&
  triple=0&head=<id>` (50 per page; default lists custom art only; `real_id` "head.body", main sprite = `alts` entry
  with `default_extension`, `/custom/<real_id><ext>.png`, 288 px = 96 px art x3), `/api/initial/dropdown-data` (its
  576 Pokémon, nat ids). Data goes to a gitignored dex dir in the scratchpad (heads/<id>.json, hist.jsonl = each
  sprite's colour histogram with outline counts; sprites are never stored or shipped). `fusion/tools/`:
  `fusion_species.py` (dex id -> Cobblemon key `species[:form]` + base texture; 543 of 576 modelled),
  `fusion_palette.py` (CIELAB k-means K=8; sprite palette down-weights outline/line-art pixels; assign = per part
  keep or repaint by lightness rank into the sprite's palette, best fit to the sprite + small change cost; small
  colours already in the sprite stay; recolour = soft-weighted Lab shift, same maths as `client/FusionColours.java`),
  `make_designs.py <cobblemon res> <dex dir> [--preview N]` -> gzip `designs.bin` (species palettes + IF name parts,
  credit strings, per pair 3-byte Lab targets with a changed-mask), CREDITS.txt (all artists) and designs_count.txt
  (README @DESIGNS@), `preview_fusions.py <res> <dex> out.png Head/Body ...` (3D: `tools/preview/fusion.html` +
  `render_fusion.js` mimic FusionRender). Runtime: `FusionDesigns` (both sides: `/fusion info` + fuse message credit
  the artist, `Fusing.fusionName` uses IF's name parts), `TextureMixin` (RETURN of `VaryingModelRepository.getTexture`:
  fused body -> recoloured DynamicTexture, also remembers body species per render state for the head), head recoloured
  in `FusionRender.prepare`; shiny parts = designed colours turned by a per-pair hue angle (IF's shiny style).
- Build and check: `./gradlew build` (runs `validateData`). Bump `mod_version` in `gradle.properties` per update.
- Shareable packages (the user's ask: all mods in zips under 20 MB, e.g. for Discord): `tools/make_share.py --out <dir>
  --base build/tmp/jar/cobbleeffort-<v>+1.21.1.jar --distortion/--kanto/--fusion <loader jars from their release zips>
  --readme "<Mod>=<file>" ... [--limit 19.5] [--loader Fabric]`. Repacks every jar (oxipng, >256-colour textures to
  their best 256, minified JSON; cached by hash), splits CobbleEffort into a core jar + texture-only jars
  (`cobbleeffort_textures_N`, whole `textures/pokemon/<folder>`s, fabric.mod.json + lowcodefml mods.toml, depend on
  the exact core version) sized to fill each zip's leftover room, and writes as few zips as fit, each with INSTALL.txt.
  Boot-test the unzipped jars on the Fabric test server. The Planeta bridge pack is the user's own, never shared.
- Preview renders: `tools/preview/` (three.js in headless Chromium; `node render.js <cobblemon-res> ../../src/main/resources out manifest_<aspect>.json`;
  `EXTRA_ROOTS=<extracted jar>:...` for other mods' forms; manifest entries with `form` are other-mod forms).
