CobbleEffort: Kanto @VERSION@
=============================

A Gen 1 adventure for Cobblemon: Gen 1 Bricks, a Gen 1-styled lab in villages with a glitchy PC, and the Kanto
dimension, where only Gen 1 Pokemon live, with eight gyms, an Elite Four, and Kantonian ore for armor and outfits.
NEW in 0.3.0: every other region, Johto to Paldea, each with its own dimension and a landmark holding its portal.

THE STARTER KIT (NEW in 0.12.0)
  When you first join a NEW world you get a Starter Bundle (once per player; config/cobbleeffort_kanto.json
  "give_starter_kit": false turns it off; operators: /kanto starterkit [players]). Use it to open it: 64 oak logs,
  32 cobblestone, 32 Poke Balls, 16 Exp. Candy S, 64 cooked porkchops and a Starter Base Token.
  Use the Starter Base Token on the ground and your starter base is built right in front of you, its door facing you
  (it needs a space about 34 x 27 blocks; trees and hills there are cleared, gaps underneath filled with dirt):
    - Ground floor: entrance hall with a healing machine and a PC (and a chest of Poke Balls and potions), kitchen
      (furnace, smoker, crafting table, barrel of food, water cauldron, composter), dining table, living corner.
    - First floor: three beds, wardrobes and nightstands, and an enchanting nook with bookshelves.
    - Second floor: the workshop (anvil, smithing table, grindstone, stonecutter, loom, cartography and fletching
      tables, brewing stand, lectern) and chests of materials and tools.
    - Attic under the roof, and a ladder shaft from the lowest basement all the way up.
    - Basement 1: the storage room, full of chests and barrels (building blocks, light, food, Poke Balls and
      medicine, tools, seeds, berries, apricorns, coal and ores).
    - Basement 2: the forge (furnaces, blast furnace, smoker, anvil) and a mine tunnel running out under the farm.
    - The farm beside the house: ripe wheat on watered farmland, twelve berry bushes ready to pick (Oran, Pecha,
      Cheri, Chesto, Rawst, Aspear, Persim, Lum, Sitrus, Leppa, Figy, Wiki), seven apricorn trees (one of each colour,
      apricorns ripe), a composter, a chest of seeds and a scarecrow.
  Operators can build one anywhere: /kanto starterbase <x y z> [north|south|east|west].

WHAT'S IN IT
  - Gen 1 Bricks in black, white and grey (8 stone bricks around a black, white or grey dye make 8).
  - The lab: a Gen 1-styled research lab of Gen 1 Bricks that can generate in any village (plains, desert, savanna,
    snowy, taiga), with a glitchy PC on its back wall. It's a rare building: not every village has one.
  - Essence of Olde: a rare drop (5%) from any Gen 1 Pokemon you defeat in battle.
  - Kantonian Orb: craft a Distortion Crystal (from CobbleEffort: Distortion) with Essence of Olde. 16 uses.
  - The glitchy PC: use the Kantonian Orb on it to wake it up, then use it to travel to Kanto. You arrive at the same
    spot, on a small brick pad with a PC: use it to come back to where you left. You can also craft a glitchy PC
    (grey Gen 1 Bricks, a glass pane, iron and redstone), but it still needs an orb to wake.
  - Kanto: a world of its own (bigger biomes than the overworld) where only Gen 1 Pokemon spawn: anything else that
    would spawn there becomes a Gen 1 Pokemon of the same type instead (never a legendary or mythical).

THE GYMS AND THE ELITE FOUR (NEW in 0.2.0)
  The first time anyone arrives in Kanto, eight gyms and the Elite Four hall are built around Kanto's centre
  (x 0, z 0), about 320 blocks out, each door facing the centre. Kanto tells you where they are when you arrive, and
  /kanto gyms lists them any time. Each gym is Gen 1 Bricks with its type's colours and a leader at the back:
      Rock Gym (0, -320)      Shale       levels 12-15        Poison Gym (0, 320)     Nightshade  levels 34-38
      Water Gym (226, -226)   Brine       levels 18-21        Psychic Gym (-226, 226) Aura        levels 38-43
      Electric Gym (320, 0)   Volta       levels 21-24        Fire Gym (-320, 0)      Cinder      levels 42-47
      Grass Gym (226, 226)    Fern        levels 27-30        Ground Gym (-226, -226) Terra       levels 47-52
  Talk to a leader and pick "Battle!". Win and you get their badge (one each; the 8 badges are items you keep).
  The Elite Four hall is at Kanto's centre: Frost (Ice), Brawn (Fighting), Wisp (Ghost) and Wyrm (Dragon), levels
  54-62, one per room. They only battle trainers with all 8 badges. Beat all four for the Kanto Champion Ribbon.
  The leaders and the Elite Four are original characters (names, looks and teams), all with Gen 1 Pokemon.
  Operators: /kanto rebuild builds the gyms and their trainers again (e.g. after the world was edited).

KANTONIAN ORE AND ARMOR (NEW in 0.2.0)
  - Kantonian ore (stone and deepslate) is only found in Kanto, at iron's heights, a bit more common than iron
    (about 1.2x). Mine it with a stone pickaxe or better for Raw Kantonian; smelt that into Kantonian Ingots
    (9 make a Block of Kantonian).
  - Kantonian armor is between iron and diamond (17 armor in all, 1 toughness), enchantable and trimmable.
    Craft it from ingots in the usual shapes for the plain set.
  - OUTFITS: put a dye OR a wool block of an outfit's colour in the gap of the armor shape, and the piece comes out
    as that outfit (same stats, a different look):
        helmet      I I I       chestplate  I X I      leggings  I I I      boots   I X I
                    I X I                   I I I                I X I              I   I
                                            I I I                I   I
      red: Trainer (cap, red jacket, jeans)        blue: Ace (blue cap and coat, black trousers)
      white: Professor (lab coat, grey hair)       brown: Hiker (round hat, vest, shorts, boots)
      light blue: Swimmer (cap and goggles)        black: Biker (helmet with visor, studded jacket)
      lime: Bug Catcher (straw hat, shorts)        yellow: Engineer (hard hat, hi-vis vest, overalls)
      purple: Psychic (hood and robe)
    The outfits are original Kanto-flavoured looks for trainer classes, not copies of any game character's outfit.

EVERY REGION: JOHTO TO PALDEA (NEW in 0.3.0)
  Each region has its own dimension (its own mix of biomes and terrain) where only that generation's Pokemon live:
  anything else that would spawn there becomes one of that generation's Pokemon of the same type (never a legendary,
  mythical, Ultra Beast or Paradox). Each region's portal is in a landmark that generates in the overworld (and in any
  dimension with the right biomes, so you can also find them in the regions). Use the portal block to go to that
  region; you arrive at the same spot on a little pad with a portal back. Use it to come home (to where you left).
    Johto   (Gen 2)  Johto Pagoda: a three-storey wooden pagoda with a pillar and ladder up the middle.
                     The PORTAL is the bell in the belfry at the top. Forests, cherry groves, plains, meadows.
    Hoenn   (Gen 3)  Hoenn Granite Cave: a grassy hill with a tunnel into a cavern. The PORTAL is the giant stone
                     Groudon statue inside (touch any part of it). Badlands, savanna, deserts, shores, windswept hills.
    Sinnoh  (Gen 4)  Sinnoh Old Manor: a gloomy two-storey manor. The PORTAL is the boarded-up doorway hidden in the
                     basement's back wall (stairs down on the left inside the door). Dark forests, taigas, swamps.
    Unova   (Gen 5)  Unova Castle: white and gold, four towers, a keep. The PORTAL is the golden wardrobe engraved with
                     Magearna, next to the throne at the end of the throne room. Plains, meadows, savanna.
    Kalos   (Gen 6)  Kalos Ball Factory: a factory beside a MASSIVE Poke Ball (25 blocks across). The PORTAL is the
                     ball (touch any part of it). Plains, flower forests, meadows.
    Alola   (Gen 7)  Alola Observatory: a domed observatory. The PORTAL is the telescope pointing out of the dome.
                     Mountains, meadows, groves, cherry groves.
    Galar   (Gen 8)  Galar Giant Tree: a snowy shrine (gate, lanterns, pavilion) before a giant Dynamax tree, 300
                     blocks from its deepest root to the top of its crown (about 240 above ground: Minecraft can't
                     build above y 320). The PORTAL is the bark block engraved with a Poke Ball at the base of the
                     trunk, at the end of the shrine path. Snowy plains, snowy taiga, ice spikes, groves.
    Paldea  (Gen 9)  Paldea Academy: a grand academy with a clock tower up a flight of steps. The PORTAL is the PC on
                     the front desk in the entrance hall. Plains, savanna, meadows, deserts, cherry groves.
  /locate structure cobbleeffort_kanto:johto_pagoda (hoenn_granite_cave, sinnoh_old_manor, unova_castle,
  kalos_ball_factory, alola_observatory, galar_giant_tree, paldea_academy) finds the nearest one.
  The landmarks are original builds inspired by those places, not copies of the games' maps.
  The regions' worlds: Johto forests and peaks; Hoenn tropical with more sea; Sinnoh snowy and towering (amplified
  terrain); Unova plains, deserts and dark forests; Kalos flowers and meadows; Alola an archipelago in warm seas;
  Galar wide (large biomes), green to snowy; Paldea wide and varied. Landmarks only appear in NEW chunks.

LANDMARKS OF GENERATIONS 1-3 (0.14.0)
  Fourteen new overworld structures, original builds inspired by famous places (not copies of the games' maps),
  each with its own chests and its own Pokemon living in and around it. Find them with /locate structure.
  Generation 1
  - Bill's Sea Cottage (beaches): Bill's PC and the Cell Separation System; the console between the pods gives
    every visitor an Eevee (once each).
  - S.S. Anne (oceans): a liner afloat with a dining hall, cabins, the bridge and an engine room.
  - Lavender Town Tower (plains, meadows, taigas): seven floors of graves, Ghost Pokemon and Cubone.
  - Celadon Rocket Hideout (plains, savannas, forests): a game corner; a hatch behind the prize counter leads down
    three basement floors with spinner tiles, a lab and the boss's office.
  - Cinnabar Pokemon Lab (beaches, savannas, deserts, badlands): nearly every machine of Cobblemon, Mega Showdown
    and CobbleEffort: Distortion in one place: healing machines, PCs, fossil restoration stations, TM machines,
    display cases, a disc shelf, a lectern, campfire pots, gilded chests and a pasture; the five Rotom appliance
    units, a reassembly unit, pedestals and a power spot; the DNA machine, analyzer and purifier; and the glitchy PC.
  Generation 2
  - Ruins of Alph (plains, savannas, meadows): four chambers of glyphs and puzzle panels spelling A-L-P-H; Unown.
  - Lake of Rage (forests, taigas): Magikarp and Gyarados in the lake; the shrine at the end of the dock calls the
    red Gyarados (shiny, level 30).
  - Mahogany Rocket HQ (taigas, snowy plains): a souvenir shop over a two-floor base with the radio transmitter.
  Generation 3
  - Meteor Falls (windswept hills, meadows): a cavern with a waterfall, meteorite chunks and a dragon's den; Bagon,
    Solrock, Lunatone, Absol.
  - Mt. Chimney (badlands, savanna plateaus): a volcano with a lava crater, a stair up its face and a lookout.
  - Mt. Pyre (meadows, windswept hills, taigas): a hall of graves inside the mountain and a stair to the summit
    shrine, which gives each trainer the Red Orb and the Blue Orb (Mega Showdown's, for Primal Groudon/Kyogre).
  - Sky Pillar (beaches, stony shores): a ruined tower; at the top the shrine calls Rayquaza (level 70).
  - Temple of Jirachi (cherry groves, flower forests, meadows): at night the shrine on the dais wakes Jirachi (50).
  - Deoxys Meteorite (plains, deserts, savannas, snowy plains, badlands): a crater round a meteorite; its four
    Deoxys meteorites (Mega Showdown's) change your Deoxys's forme, and the shrine calls Deoxys (level 50).
  Shrines: the legendary and mythical encounters can be called again (after five minutes) until you catch the
  Pokemon; gifts are once per trainer. Operators: /kanto shrines reset <player> [key].

GAME RULES AND COMMANDS (0.13.0)
  Game rules (/gamerule <name> <value>, per world; /kanto rules lists them):
  kantoRegionSpawns (true): each region's dimension keeps only its own generation (off: anything can spawn there).
  kantoOverworldGeneration (0): 1-9 makes the overworld that generation only, the way the regions are (every other
    wild Pokemon becomes one of that generation sharing its type); 0 = off.
  kantoEssenceDropChance (5): percent chance a defeated Gen 1 Pokemon leaves Essence of Olde.
  kantoBossRespawnMinutes (3): minutes before a beaten Noble or totem comes back.
  kantoEliteFourNeedsBadges (true): the Elite Four want all of their region's badges first.
  Commands (operators unless noted):
  /kanto travel <region> [players]: straight into a region (Kanto, Johto, ... Paldea, Hisui).
  /kanto home [players]: back from a region to where they came from.
  /kanto badges (anyone): your badges and Elite Four progress in every region; /kanto badges <player> for anyone's.
  /kanto badges <player> give|clear <region>: give all of a region's badges (with the badge items) or clear them
    (and its Elite Four progress).
  /kanto rules (anyone). Also /kanto gyms, /kanto rebuild, /kanto forcebiome, /kanto drops, /kanto dna,
  /kanto starterkit, /kanto starterbase.

INSTALL
  Unzip and put ONE jar in your mods folder: the -fabric jar on Fabric, the -neoforge jar on NeoForge.
  Needs: Cobblemon 1.8.4+, CobbleEffort: Distortion 0.12.0+ (for the Distortion Crystal), Architectury API.
  Install it on the server too. Kanto is a new dimension: it's there in new and existing worlds.

EVERY REGION'S LEAGUE (NEW in 0.4.0)
  Every region has its own league, like Kanto's: the first time anyone arrives in a region, its eight gyms and its
  Elite Four hall are built round that region's centre (the same places as in Kanto: about 320 blocks out, the hall at
  0, 0). Kanto tells you where they are when you arrive, and /kanto gyms lists the region you're in (or
  /kanto gyms johto, hoenn...). Every leader and Elite Four member is an original character with a team from that
  region's own generation, getting stronger from the first gym (levels 14+) to the Elite Four (levels 54-62).
  Each gym gives its own badge (e.g. the Johto Flying Badge); a region's Elite Four only battle trainers holding all
  eight of THAT region's badges, and beating all four gives that region's Champion Ribbon.
    Johto   gyms: Flying (Wren), Bug (Sable), Normal (Corin), Fighting (Hollis), Steel (Brannock), Ice (Ferris), Psychic (Aster), Poison (Draven)
            Elite Four: Mireille (Dark), Thorne (Fire), Kestrel (Water), Vesper (Grass)
    Hoenn   gyms: Rock (Marisol), Fighting (Cobalt), Electric (Rhea), Fire (Pell), Normal (Tasman), Flying (Cirrus), Psychic (Lumen), Water (Halia)
            Elite Four: Sorrel (Dark), Nerine (Ghost), Basalt (Ice), Corvina (Dragon)
    Sinnoh  gyms: Rock (Linnea), Grass (Gerd), Fighting (Holm), Water (Frida), Ghost (Torvald), Steel (Isak), Ice (Saga), Electric (Embla)
            Elite Four: Runa (Bug), Valdis (Ground), Eir (Fire), Brage (Psychic)
    Unova   gyms: Grass (Jett), Normal (Marlow), Bug (Ceci), Electric (Dorian), Ground (Tamsin), Flying (Rook), Ice (Indigo), Dragon (Halcyon)
            Elite Four: Vale (Ghost), Odessa (Dark), Cyprus (Psychic), Nyx (Fighting)
    Kalos   gyms: Bug (Amelie), Rock (Bastien), Fighting (Coralie), Grass (Fleur), Electric (Gaspard), Fairy (Lucien), Psychic (Margaux), Ice (Sylvain)
            Elite Four: Odile (Fire), Thibault (Water), Celeste (Steel), Aurelien (Dragon)
    Alola   gyms: Normal (Kalani), Water (Makoa), Fire (Leilani), Grass (Nalu), Electric (Keoni), Ghost (Mahina), Fairy (Ikaika), Ground (Pua)
            Elite Four: Kaimana (Rock), Nohea (Flying), Lani (Bug), Akoni (Fighting)
    Galar   gyms: Grass (Bryony), Water (Rowan), Fire (Imogen), Fighting (Ewan), Ghost (Morwenna), Fairy (Callum), Rock (Heddwyn), Ice (Fenella)
            Elite Four: Gareth (Dark), Isolde (Dragon), Lachlan (Psychic), Rhiannon (Steel)
    Paldea  gyms: Bug (Ines), Grass (Mateo), Electric (Lucia), Water (Rafael), Normal (Carmen), Ghost (Joaquin), Psychic (Pilar), Rock (Tomas)
            Elite Four: Alba (Steel), Ignacio (Fairy), Rocio (Dragon), Esteban (Flying)
  Operators: /kanto rebuild (the region you're in) or /kanto rebuild <region> builds the gyms and trainers again.
  Building waits for the area to load in the background, so arriving in a new region doesn't freeze the server.

HISUI, NOBLES AND TOTEM TRIALS (NEW in 0.5.0)
  - Hisui: a new region dimension (fieldlands, mirelands, coastlands, highlands, icelands). Its Pokemon are Sinnoh's
    Pokedex, Hisui's own new Pokemon (Wyrdeer, Kleavor, Ursaluna, Basculegion, Sneasler, Overqwil, Enamorus) and
    everything that has a Hisuian form, which always appears IN its Hisuian form there.
  - The way in: the Hisui Great Mountain, a huge snow-capped mountain (about 150 blocks high, nearly 200 across) with
    a path spiralling up to ruined white pillars at the summit, a great cavern inside (tunnel at the south foot), and
    on the summit a stone sculpture of Arceus with a golden cross-wheel. Touch any part of the sculpture to go to
    Hisui (and back). It generates in plains, meadows, taiga and snowy lands: /locate structure
    cobbleeffort_kanto:hisui_great_mountain
  - Instead of gyms, Hisui has five FRENZIED NOBLE arenas round its centre (/kanto gyms): giant glowing Nobles
    wreathed in fire and gold sparks: Kleavor (60), Hisuian Lilligant (63), Hisuian Arcanine (66), Hisuian Electrode
    (69), Hisuian Avalugg (72). They can't be caught: beat one to calm it and earn its Noble Seal; calm all five for
    the Hisui Hero Ribbon. A calmed Noble returns a few minutes later.
  - Alola now has TOTEM TRIALS instead of gyms: eight trial grounds (totem poles, a trial gate, a ring of flowers),
    each guarded by a giant glowing Totem Pokemon of the trial's type: Bewear, Golisopod, Turtonator, Dhelmise,
    Vikavolt, Palossand, Comfey and Mudsdale (levels 16-51). Beat the totem to clear the trial: you get its Trial
    Stamp and the type's Z-Crystal from Mega Showdown. Alola's Elite Four still wants all eight stamps.
    (In a world from 0.4.0, Alola's gyms are replaced by the trials the next time someone arrives in Alola.)

TAR (NEW in 0.6.0)
  - Tar: a slow, sticky black fluid of the overworld. It pools in tar lakes on the surface of badlands, deserts,
    savannas and swamps, in tar lakes underground (like lava lakes), and in tar pits: caverns deep underground
    (around y -30) with a tar pool beside pockets of lava (/locate structure cobbleeffort_kanto:tar_pit). Wading
    through it slows you right down. It spreads like lava but is cold and never makes new source blocks.
  - Scoop it up with an empty bucket: a Bucket of Tar is the fossil CobbleEffort's Petroleodd is revived from. Put it
    in Cobblemon's Fossil Analyzer like any fossil (the bucket goes in with it). It's in the Kanto creative tab.

THE ASHTRAY WASTES (NEW in 0.7.0)
  - A new overworld biome, nicotine-blighted: its ground is ash, its water is tar, no trees grow there (only the odd
    dead bush), and giant cigarettes stick out of the ground at odd angles, filters buried, gold-ringed, their tips
    smouldering (glowing, smoking and hot to stand on) or stubbed out in ash. Cigarette butts litter the ground between
    them, and tar pools fill the hollows. Grey skies, a haze of drifting ash.
  - It takes over patches of plains, savannas, deserts and badlands in new chunks (existing land doesn't change):
    /locate biome cobbleeffort_kanto:ashtray
  - New blocks: Ash (falls like sand), Cigarette Paper, Cigarette Filter and Cigarette Ember (glows, smokes, burns).
  - Its Pokemon: the Nicodex, 19 Pokemon (one per type) in CobbleEffort 0.78.0 and later, which spawn only here
    (spawn tag #cobbleeffort_kanto:is_ashtray).

THE LIQUOR MEADOWS (NEW in 0.8.0)
  - A new overworld biome, cheerfully tipsy: extra-vibrant green grass and flowers under clear skies (it never rains
    there), ponds and lakes of water the colour of whisky, and no trees. Instead, giant bottles stick out of the
    ground at odd angles: wine (green glass, red wine, cork), champagne (gold foil), beer (brown glass, gold cap),
    whisky (clear glass, black-and-gold label), vodka (clear, silver cap) and ceramic sake bottles, each with its
    label band and its drink filled level inside however it leans. Little empties lie about in the grass.
  - It takes over patches of forests, flower and birch forests, plains and meadows in new chunks (existing land
    doesn't change): /locate biome cobbleeffort_kanto:liquor_meadows
  - New blocks: Cork, Bottle Cap and Bottle Label.
  - Its Pokemon: 20 Pokemon (one per type) in CobbleEffort 0.79.0 and later, which spawn only here
    (spawn tag #cobbleeffort_kanto:is_liquor).

BIOME FREQUENCY (NEW in 0.9.0)
  - The Ashtray Wastes and the Liquor Meadows are now much more common (they used to take about 15% of their host
    biomes in big, far-apart patches; now 35% in smaller, closer patches).
  - Server owners can set both in config/cobbleeffort_kanto.json (written on the first start):
      "frequency": share of the host biomes taken over, 0 (never) to 1 (all of them)
      "patch_size": roughly how wide a patch is, in blocks
    Changes apply to chunks generated after the next server start.

TESTING TOOLS (NEW in 0.9.0, creative mode + operator only; in the Kanto creative tab)
  - Biome Wand: use it to locate the nearest Ashtray Wastes or Liquor Meadows (click the coordinates to teleport);
    use it on a block to turn the 65 x 65 area round that block into the biome, with its giant cigarettes or bottles
    and ponds; sneak + use to switch biome. The same as a command (for command blocks too):
      /kanto forcebiome <ashtray|liquor_meadows> [x y z]
  - Drop testing (NEW in 0.11.0, operators; for testing rare drops like CobbleEffort's Garbage Bag):
      /kanto drops <pokemon>                rolls the Pokemon's drop table as if you'd defeated it 100 times and
                                            lists what came up; nothing is given
      /kanto drops roll <rolls> <pokemon>   the same, for any number of defeats
      /kanto drops give <rolls> <pokemon>   rolls like real defeats and you really get the items
      /kanto drops force <pokemon>          gives you one of every item it can drop, chance or no chance
      /kanto dna [battles]                  simulates winning battles with Mew in your party and gives you the
                                            Mew DNA they'd drop (CobbleEffort: Distortion's DNA machine)
    <pokemon> is any Cobblemon properties (the rest of the line): /kanto drops force garbodor,
    /kanto drops roll 1000 slugma cobbleeffortian
  - Structure Wand: use it to locate the nearest CobbleEffort or Kanto structure of the chosen kind; use it on a block
    to place that structure there; sneak + use to switch structure.
  - Pokemon Spawner and Trainer Spawner: blocks set up like command blocks. Right-click one to open its settings;
    every time it receives a redstone signal it spawns what you set:
      Pokemon Spawner: any Cobblemon properties (e.g. "mewtwo level=70 shiny=yes moves=psychic,recover,aurasphere
      ability=pressure nature=modest"), a name tag, a default level, a size (2 = twice as big), and switches for
      Uncatchable, Glowing, Battle nearest player (starts the battle at once) and One at a time (no new spawn while
      the last one is still around). Perfect for scripted legendary encounters.
      Trainer Spawner: a name, an optional player name for the skin, a team (one Pokemon per line or separated by
      ";", in the same properties format; members without level= get the Level box), skill 0-5, and switches for
      Battle nearest player, Double battle, Leave after losing and One at a time. Players can also talk to the
      trainer to battle it.

CALL OF THE DEN (NEW in 0.10.0, for CobbleEffort's Hopple)
  - With three or more Hopples in your party, open the interaction wheel on a Hopple that knows Call of the Den and
    choose Call of the Den: every Hopple in the party fuses into that one, which evolves for good into Rabbrute, a
    titanic rabbit monster almost 80 blocks tall. The other Hopples' held items go back to you. Needs CobbleEffort
    0.81.0 or later (where Hopple lives).

PLEASE TEST AND REPORT
  0.12.0: make a new world: do you get the Starter Bundle? Open it, then use the token on open ground: is the base
  built facing you, in one piece? Pick the berries and apricorns, check the chests, climb the ladder to the attic.
  0.10.0: gather three Hopples and use Call of the Den from the wheel: do they fuse into Rabbrute?
  0.9.0: set up a Pokemon Spawner and a Trainer Spawner with a button: do they spawn, battle you, and stay uncatchable
  / leave after losing when set to? Try both wands. Are the new biomes easy enough to find now?
  0.8.0: find the Liquor Meadows (/locate biome cobbleeffort_kanto:liquor_meadows): bright grass, whisky ponds, giant
  bottles. Do the bottles and their drinks look right, and does anything look wrong at its edges?
  0.7.0: find the Ashtray Wastes (/locate biome cobbleeffort_kanto:ashtray) and look around: ash ground, tar pools,
  giant cigarettes. Does anything look wrong at its edges?
  0.6.0: find a tar lake or tar pit, fill a bucket, pour it out again, and revive Petroleodd from the bucket.
  0.5.0: find the great mountain and climb to the sculpture; in Hisui, do Pokemon appear in their Hisuian forms,
  and can you battle and calm the Nobles? In Alola, do the totems appear, and do you get the stamp and Z-Crystal?
  0.4.0: travel to another region: do its gyms appear (/kanto gyms), can you battle its leaders, do you get its
  badges, and does its Elite Four ask for that region's eight badges?
  0.3.0: /locate each landmark, use its portal (and the pad's portal to come back). Do the right Pokemon spawn in
  each region? Does the Galar tree look right, and is its engraved bark reachable at the end of the path?
  0.2.0: battle a gym leader (do you get the badge?), try the Elite Four without and with 8 badges, find Kantonian
  ore in Kanto, craft an outfit and wear it. (/give @s cobbleeffort_kanto:rock_badge etc. to skip ahead.)
  Find a village with the lab (or /place template cobbleeffort_kanto:village/gen1_lab), craft or find a Kantonian
  Orb (/give @s cobbleeffort_kanto:kantonian_orb), wake the PC, travel to Kanto and back. Does only Gen 1 spawn
  there? Does Essence of Olde drop now and then? Send latest.log if anything goes wrong.

LICENCE
  CC BY-NC-SA 4.0 (non-commercial). All textures and buildings are original, by ellecat5112 / CobbleEffort, except
  the trainers' skins, which are recoloured from Cobblemon's trainer texture (Cobblemon's assets: CC BY-NC).

CHANGES
  0.14.0: fourteen landmarks of Generations 1-3 with their own loot and Pokemon, and shrines for Rayquaza,
         Jirachi, Deoxys, the red Gyarados, the Red and Blue Orbs and Bill's Eevee.
  0.13.0: game rules (region spawns, a one-generation overworld, Essence chance, boss respawns, the Elite Four's
         badge gate) and /kanto travel, home, badges, rules.
  0.12.0: the starter kit: the Starter Bundle on joining a new world, and the Starter Base Token that builds a
         stocked starter base with a farm.
  0.11.0: /kanto drops and /kanto dna, to force and simulate Pokemon drops and Mew DNA (testing tools).
  0.10.0: Call of the Den (fuse your party's Hopples into Rabbrute from the interaction wheel).
  0.9.0: the Ashtray Wastes and Liquor Meadows are more common (config/cobbleeffort_kanto.json); Biome and
         Structure Wands, Pokemon and Trainer Spawners, /kanto forcebiome (testing tools for creative operators).
  0.8.0: the Liquor Meadows biome (vibrant grass, whisky-coloured water, giant bottles) and its three blocks.
  0.7.0: the Ashtray Wastes biome (ash ground, tar for water, giant cigarettes) and its four blocks.
  0.6.0: tar (fluid, Bucket of Tar, tar lakes, tar pits moved here from CobbleEffort); a Bucket of Tar revives
         CobbleEffort's Petroleodd at the Fossil Analyzer.
  0.5.0: Hisui (dimension, great mountain with the Arceus sculpture, Hisuian forms, five frenzied Noble boss arenas,
         Noble Seals, Hisui Hero Ribbon); Alola's gyms became totem trials (totem bosses, trial stamps, Z-Crystals).
  0.4.0: every region (Johto to Paldea) has its own eight gyms, Elite Four, badges and Champion Ribbon; gym building
         loads its chunks in the background (no server freeze).
  0.3.0: Johto, Hoenn, Sinnoh, Unova, Kalos, Alola, Galar and Paldea: a dimension each (only that generation's
         Pokemon), a landmark each with its portal block, arrival pads with a way home.
  0.2.0: the gyms, the Elite Four, badges and the Champion Ribbon; Kantonian ore, ingots and armor with 9 outfits;
         /kanto gyms and /kanto rebuild. Fabric fix: Kanto's Gen 1-only spawns and Essence of Olde drops failed on
         Fabric (a build problem); they work now.
  0.1.0: Gen 1 Bricks, the lab, Essence of Olde, the Kantonian Orb, the glitchy PC and Kanto.
