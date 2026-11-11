CobbleEffort: Distortion @VERSION@
==================================

A new battle gimmick for Cobblemon. A Pokemon holding the Distortion Crystal, with its trainer wearing the
Distortion Band, distorts: its types turn into their weaknesses, its moves follow, and its colours invert.

A TEST BUILD. What's in it:
  - The Distortion Band and the Distortion Crystal (one crystal for every Pokemon), in the "Distortion" creative tab.
  - A "Distortion" accessory slot (open your Accessories screen); the band goes there.
  - Distorted forms for Giratina, Dialga, Palkia and Arceus (including the Origin forms and every Arceus plate type),
    the Gen 1 legendary and mythical Pokemon (Articuno, Zapdos, Moltres, Mewtwo, Mew), the Gen 2 ones (Raikou,
    Entei, Suicune, Lugia, Ho-Oh, Celebi), and every starter and its evolutions, Gen 1 to 9 (81 Pokemon, plus the Hisuian forms of Typhlosion, Samurott
    and Decidueye and Greninja's Bond form). Each line has its own distorted look:
      water starters -> plant-inspired, grass starters -> natural disasters, fire starters -> sea life
    (see STARTERS below).
  - NEW in 0.12.0: EVERY other Pokemon with a Cobblemon or Mega Showdown model (710 more, 884 with Gen 1), each
    with the look of its new types (see GEN 1 LOOKS: the same themes for every generation), and the Gen 2-9 STARTERS now
    get RANDOM new types (not their weakness: see STARTER TYPES). Not covered: the 45 Pokemon only other mods model
    (e.g. the Paradox Pokemon, Ultra Beasts, Gulpin, Cresselia).
  - NEW in 0.12.0: Distortion Crystal ore (see GETTING THE CRYSTAL AND THE BAND).
  - From 0.9.0: ALL 151 Gen 1 Pokemon, each with its whole evolutionary line (so also Pichu, Cleffa, Igglybuff, Crobat,
    Bellossom, Politoed, Slowking, Magnezone, Steelix, Kingdra, Scizor, Kleavor, Blissey, Happiny, Tangrowth,
    Rhyperior, Lickilicky, Mime Jr., Mr. Rime, Smoochum, Elekid, Electivire, Magby, Magmortar, Porygon2, Porygon-Z,
    Munchlax, Sirfetch'd, Perrserker, Annihilape, Tyrogue, Hitmontop and all of Eevee's evolutions): 174 more Pokemon,
    with their regional (Alolan, Galarian, Hisuian, Paldean) and Gigantamax forms. Each takes the look of its NEW
    types (see GEN 1 LOOKS below).
  - Distorting in battle, and from the interaction wheel (the radial menu) outside battle.
  - Abilities follow when they're tied to the Pokemon's type: Overgrow -> Blaze, Blaze -> Torrent, Torrent -> Overgrow,
    and NEW ones where no real ability fits: Storm Power (Solar Power, in rain), Flash Flood (Flash Fire, for Water),
    Blubber (Thick Fat, against Water and Ice), Blossom Voice (Liquid Voice, Grass) and Scrappy Mind (Scrappy,
    Psychic). NEW with Gen 1: Deluge (Drought, rain), Heat Warning (Snow Warning, sun), Sun Bask (Ice Body),
    Heat Rush (Slush Rush), Sunscreen (Overcoat), Sinkhole (Lightning Rod, draws Ground moves), Tremor Drive (Motor
    Drive), Root Absorb (Water Absorb, Grass), Quagmire (Magnet Pull, traps Ground types), Tectonize (Galvanize),
    Metallize (Pixilate, Steel), Tide Force / Silt Force (Sand Force), Earthen Spirit (Steely Spirit), Flock (Swarm,
    Flying), Jittery (Rattled), Scrappy Fists (Scrappy on a Normal type) and Insulation (Thick Fat on an Ice type).
    An ability's twin depends on the holder's types (Thick Fat: Blubber on Tepig, Insulation on Dewgong).
    Abilities that aren't tied to its type stay.
  - Wild Pokemon and NPC trainers' Pokemon holding the crystal (Arceus: a plate) distort on their first move.

THE DNA MACHINE: MAKING MEWTWO (NEW in 0.11.0)
  The cloning tank Mewtwo comes from in the first movie, two blocks tall (in the Distortion creative tab, or craft
  it: iron block, glass, iron block / glass, diamond, glass / iron block, redstone block, iron block).
  1. Get Mew DNA: every time you defeat a Pokemon in battle with a Mew in your party, 3-8 Mew DNA drop.
  2. Fill the tank: click the machine with Mew DNA (sneak-click pours the whole stack). It needs 16; the fluid
     rises as you pour.
  3. Select Mew in your party bar and click the machine with an empty hand: Mew floats into the tank.
  4. Wait five minutes. Mew becomes Mewtwo (same level, shiny if Mew was), floating in the tank.
  5. Click the machine again to take your Mewtwo (to your party, or your PC if it's full).
  The machine can't be broken while a Pokemon is inside. Only the one who put Mew in can take Mewtwo out.
  Note: Mew is used up; it becomes Mewtwo.

DISTORTING WITH THE CRYSTAL (NEW in 0.10.0)
  Give a distortable Pokemon the Distortion Crystal and it distorts at once: its distorted form, look, types, moves
  (their distorted twins) and type-bound ability, kept while it holds the crystal (it enters battle distorted). Take the crystal away and it turns back. No band needed for this;
  the band is what lets you toggle it in battle (and use the wheel).

HOW TO DISTORT IN BATTLE
  1. Wear the Distortion Band in the Distortion slot.
  2. Give the Distortion Crystal to a distortable Pokemon (Giratina, Dialga, Palkia, every Gen 1 Pokemon and its
     line, the Gen 2 legendaries and mythicals, any starter or its evolutions).
     Arceus doesn't need it: it distorts with its plate (it can only hold one item, and the plates are its power).
  3. In battle, pick "Fight": a Distort button appears next to the back button. Click it (the move tiles switch to
     the distorted moves), then pick a move.
  4. At the start of the turn, before anyone moves, the Pokemon distorts: new types, new look, every move turns into
     its distorted twin, and its ability follows if it's tied to its type.
  NEW: it's a toggle, free to use any turn: while distorted, the same button reverts it (the tiles show the normal
  moves again), and you can distort again later. At the end of the battle it's back to normal.
  NEW: distorting only needs the crystal held and the band worn, so anything that doesn't need a different held item
  still works with it, and the Pokemon stays distorted through it: Dynamax and Gigantamax (distorted Gigantamax
  Charizard, Venusaur, Blastoise, Rillaboom, Cinderace, Inteleon), Battle Bond's Ash-Greninja, move-triggered megas
  (Dragon Ascent), ability form changes. Megas that need a Mega Stone, and primals, can't (the crystal is the held
  item).
  Wild and NPC Pokemon holding the crystal distort on their own (try /pokespawn charizard
  held_item=cobbleeffort_distortion:distortion_crystal).

HOW TO DISTORT OUTSIDE BATTLE (the interaction wheel)
  Send out your Pokemon and open its interaction wheel (the radial menu, where Mega Showdown's Mega Evolve is).
  With the band on and the crystal held (Arceus: a plate), there's a Distort option: the Pokemon distorts on the
  spot and stays distorted (it's saved). Open the wheel again and pick Revert Distortion to undo it; taking the
  crystal away also reverts it.
  One distorted Pokemon per party at a time, and not while you're battling.
  A Pokemon distorted this way enters battle distorted, with its distorted moves, and that counts as your
  distortion for the battle.

Distorted types (each type becomes its weakness):
  Giratina  Ghost/Dragon  -> Dark/Fairy        Dialga  Steel/Dragon  -> Ground/Fairy
  Palkia    Water/Dragon  -> Grass/Fairy       Arceus  its type      -> that type's weakness
  Starters: Grass -> Fire, Fire -> Water, Water -> Grass, and their second types follow the same chart
  (Charizard Fire/Flying -> Water/Electric, Venusaur Grass/Poison -> Fire/Ground, Empoleon Water/Steel -> Grass/Ground).
  Stone megas and primals don't distort (they need their own held item).

GEN 1 LEGENDARY AND MYTHICAL POKEMON
  Mew       Psychic -> Normal/Fighting (a specialised distortion): the unborn. It floats in a translucent orb, the
            placenta, veined and pulsing like a heartbeat; its tail turns to the front as the umbilical cord. Its
            Psychic moves turn Normal.
  Mewtwo    Psychic -> Normal/Fighting (a specialised distortion): the heavyweight bodybuilder. Huge translucent pink
            arms (Conkeldurr's), a bulked-up chest, waist and thighs. Its Psychic moves turn Fighting.
  Articuno  Ice/Flying -> Fire/Electric: a phoenix, its tail and crest burning. Snow Cloak -> Heat Haze (in sun).
  Zapdos    Electric/Flying -> Ground/Electric: a dust storm, ochre with a sandstone crest.
  Moltres   Fire/Flying -> Water/Electric: a tidal wave, its flames turned to water.
  (Galarian Articuno, Zapdos and Moltres distort too: Dark/Electric, Psychic/Electric, Fairy/Electric. Mega Mewtwo
  can't: it needs a Mega Stone.)

GEN 2 LEGENDARY AND MYTHICAL POKEMON
  Raikou    Electric -> Ground: a sandstorm. Desert-tan fur, a billowing dust-cloud mane, a stone tail.
  Entei     Fire -> Water: a lionfish. Sea blue, its mane striped venomous lionfish spines, a pearl crest and mask.
  Suicune   Water -> Grass: a weeping willow. Green, its ribbons willow vines, its mane wisteria, a leaf crest.
  Lugia     Psychic/Flying -> Dark/Electric: a storm at night. A photographic negative of itself (black where it was
            white), lightning crackling along its back plates.
  Ho-Oh     Fire/Flying -> Water/Electric: an aurora over the sea. Sea blue, its glowing flames aurora green-teal.
  Celebi    Psychic/Grass -> Dark/Fire: an ember sprite. Charcoal skin, an ash face with glowing ember eyes, a
            smouldering crest, ember wings, burning antenna tips. (Celebi's model comes from AllTheMons x Mega
            Showdown: with that mod installed you see this look; it's an original texture made for its model.)
  (Raikou, Entei and Suicune use Mega Showdown's models.)

GETTING THE CRYSTAL AND THE BAND (NEW in 0.12.0)
  Distortion Crystal ore (stone and deepslate) is found at the same heights as coal (y 0-192), a little rarer. Mine it
  with a stone pickaxe or better: it drops 2-4 Distortion Shards (Fortune gives more; Silk Touch keeps the ore, which
  you can smelt into a shard).
  Distortion Crystal:  4 Distortion Shards around an amethyst shard (a plus shape).
  Distortion Band:     gold ingot, shard, gold ingot / shard, Distortion Crystal, shard / gold ingot, shard, gold ingot.

STARTER TYPES (NEW in 0.12.0)
  The Gen 1 starters (Bulbasaur, Charmander, Squirtle lines) still turn into their weakness, as before (Grass ->
  Fire, Fire -> Water, Water -> Grass). Every other starter line has its own random new types, the same in every
  world (their moves and abilities follow; a pinch ability for a type without one becomes "<Type> Fervor"):
    Chikorita line   Grass -> Water
    Cyndaquil line   Fire -> Electric, Ghost -> Fairy
    Totodile line    Water -> Fairy
    Treecko line     Dragon -> Fighting, Grass -> Water
    Torchic line     Fighting -> Rock, Fire -> Fairy
    Mudkip line      Ground -> Poison, Water -> Electric
    Turtwig line     Grass -> Fighting, Ground -> Dragon
    Chimchar line    Fighting -> Steel, Fire -> Ghost
    Piplup line      Steel -> Rock, Water -> Flying
    Snivy line       Grass -> Fairy
    Tepig line       Fighting -> Grass, Fire -> Psychic
    Oshawott line    Dark -> Normal, Water -> Ground
    Chespin line     Fighting -> Ice, Grass -> Psychic
    Fennekin line    Fire -> Ice, Psychic -> Poison
    Froakie line     Dark -> Normal, Water -> Electric
    Rowlet line      Fighting -> Rock, Flying -> Normal, Ghost -> Ground, Grass -> Psychic
    Litten line      Dark -> Electric, Fire -> Psychic
    Popplio line     Fairy -> Ghost, Water -> Rock
    Grookey line     Grass -> Fairy
    Scorbunny line   Fire -> Electric
    Sobble line      Water -> Ghost
    Sprigatito line  Dark -> Normal, Grass -> Bug
    Fuecoco line     Fire -> Dark, Ghost -> Bug
    Quaxly line      Fighting -> Flying, Water -> Psychic
  Their distorted looks are the same as before:

STARTERS (the distorted looks)
  Grass starters, natural disasters:
    Bulbasaur line   a wildfire: raging flames burst from a charred stump where the bulb was; Venusaur's flower is
                     an inferno with petals of fire
    Chikorita line   a volcanic eruption: the leaf is a plume of fire, Meganium's petals cooled lava, flames erupting
    Treecko line     a firestorm: a magma tail with flames, Sceptile's seeds molten and its leaves flame
    Turtwig line     a volcano: Torterra's tree is an erupting volcano (every tree variant), Grotle's bushes lava rocks
    Snivy line       a lava flow: burning leaves, a magma collar, Serperior's tail molten rock
    Chespin line     a meteor strike: a meteorite hood and armour cracked with lava
    Rowlet line      a firestorm: burning leaves and plumes, Decidueye's cloak scorched
    Grookey line     a wildfire: burning torches for sticks, flaming hair, Rillaboom's magma drum
    Sprigatito line  an ember storm: burning fur and blossoms, smouldering cloaks
  Fire starters, sea life:
    Charmander line  a mermaid: a fish-scaled tail with a fluke instead of the flame
    Cyndaquil line   sea anemones: the flames are anemone tentacles (Hisuian Typhlosion's mane too)
    Torchic line     a coral reef: coral crest, sea-foam fluff, Blaziken's fins and kelp crest
    Chimchar line    jellyfish: the flames are jellyfish tendrils
    Tepig line       pearls and coral: a pearl tail, Emboar's coral beard
    Fennekin line    a nudibranch: frilly sea-slug ear tufts, anemone flames on the wands
    Litten line      a shark: a dorsal fin, Incineroar's coral belt
    Scorbunny line   the sea bunny (a fluffy sea slug): speckles and a gill tuft
    Fuecoco line     deep-sea bioluminescence: the flames glow cold cyan, like an anglerfish's lure
  Water starters, plant inspiration:
    Squirtle line    prototaxites: banded fungal trunks on the shell, Blastoise's cannons two towering pillars
    Totodile line    the Venus flytrap: snapping traps along the back
    Mudkip line      a lotus pond: lily-pad fins, lotus-petal gills, a lotus on Mudkip's head
    Piplup line      a pine forest: little pines, needle crests, Empoleon's bark crown with pine branches
    Oshawott line    bamboo: a bamboo-slice scalchop, Samurott's bamboo helmet, blades and back stand
    Froakie line     moss and vines: mossy frubbles, Greninja's vine scarf
    Popplio line     flowers: petal ruffs, blossoms, Primarina's golden pollen stars
    Sobble line      leaves: leafy fins and Inteleon's leaf-trail tail
    Quaxly line      fern fronds: frond hair and plumes

Distorted moves: every move becomes the same move in its new type. Where a real move is already the exact
opposite, it's that one (Blast Burn -> Hydro Cannon, Sunny Day -> Rain Dance, Trick -> Switcheroo). Otherwise it's
a new move with the same power, accuracy, PP and effects, named to match: Dragon Claw -> Fairy Claw,
Shadow Force -> Dark Force, Roar of Time -> Radiance of Time, Spacial Rend -> Fairy Rend,
Judgment -> Inverse Judgment (the weakness of Arceus's plate type), Earthquake -> Water Earthquake,
Fire Fang -> Water Fang, Air Slash -> Electric Slash, Fire Spin -> Whirlpool.

GEN 1 LOOKS
Every Gen 1 line besides the starters and legendaries looks like its NEW types: the first type gets the full look, the
second an accent, and its main colour moves to the new type's colour.
  Fighting  a brawler: bulked-up arms and legs, a red headband with trailing ribbons (Rattata, Snorlax, Eevee...)
  Water     sea life: a finned crest on the back, a fluke on the tail; flames become sea life (Vulpix, Ponyta...)
  Grass     overgrown: leaves sprouting from the head, fern fronds on the back, moss on the tail (Psyduck, Poliwag...)
  Fire      ablaze: animated flames on the head and the tail tip (Oddish, Bellsprout, Lapras, Jynx...)
  Ground    earthen: a cluster of jagged rocks on the back, sandstone tail and ears (Pikachu, Ekans, Voltorb...)
  Psychic   a third eye: a glowing gem on the forehead and a pulsing halo (Machop, Mankey, the Hitmons...)
  Electric  a storm: crackling lightning through wings and tail (Pidgey, Zubat, Butterfree...)
  Dark      shadow: wisps of dark flame on the back and tail (Abra, Gastly, Slowpoke, Drowzee...)
  Flying    feathered wings from the back (Caterpie, Weedle, Paras, Venonat, Scyther...)
  Fairy     a crown of petals (Dratini, Dragonair, Dragonite...)
  Steel     riveted steel plates on the head and back (Clefairy, Jigglypuff...)

You can still give a distorted-looking Pokemon with a command:   /pokegive giratina distorted

INSTALL
  Unzip and put ONE jar in your mods folder: the -fabric jar on Fabric, the -neoforge jar on NeoForge.
  Needs: Cobblemon 1.8.4+, Mega Showdown 1.3.3+, Accessories, Architectury API. Install it on the server too.

PLEASE TEST AND REPORT
  0.12.2 (Fabric fix): on Fabric, Mew DNA never dropped, and the radial menu's Distort/Revert sparkles and Mew's
  display in the DNA machine's tank failed (a build problem: some Minecraft calls on Cobblemon's entities weren't
  translated for Fabric). Try them again on Fabric. NeoForge was not affected.
  0.12.1: the Gen 1 starters are back to their old types (Charizard Water/Electric, Storm Power).
  0.12.0: find Distortion Crystal ore in a new chunk (y 0-192), mine it with a stone pickaxe, craft a crystal and
  a band. Try /pokegive <any Pokemon> distorted for the new ones, and a starter in battle (its random types).
  0.11.0: the DNA machine. Place it (does the upper half appear, does it face you?), win a battle with Mew in your
  party (Mew DNA drops), fill the tank, put Mew in (does Mew show inside the glass?), wait five minutes, take
  Mewtwo out. Send latest.log if anything goes wrong.
  0.10.1: give a distortable Pokemon the Distortion Crystal: it should distort straight away, with a "distorted!"
  message, its distorted moves and (if type-bound) ability in its summary. Take the crystal back: it returns to
  normal with its own moves and ability (a move it learned meanwhile stays). In battle it starts distorted; revert it
  with the band and it's back to normal, then distorted again after the battle while it still holds the crystal.
  If the message doesn't show, send latest.log (it logs "<Pokemon> distorted (holding the Distortion Crystal)").
  0.9.1: fixes the crash when creating or loading a world (Mega Showdown loads the battle scripts as one line, so a
  comment in them cut the rest off), and Magnemite's line distorting to Ground/Ground (now just Ground).
  New in this build: every Gen 1 Pokemon (try /pokegive <name> distorted, with alolan / galarian / hisuian /
  paldean for the regional forms). Do the added parts sit right while they move (headbands, wings, fins, halos,
  rocks)? Anything floating, hidden inside the body or off-theme: tell me which Pokemon. In battle: the new ability
  twins (Heat Warning should bring sun, not extreme sun).
  From 0.8.0: the Gen 2 legendaries and Celebi (with AllTheMons x Mega Showdown). From 0.7.0: Mew (the orb
  and the cord: do they sit right while it floats and animates?), Mewtwo (the arms and bulk), the legendary birds.
  New in this build: distort, then press Distort again on a later turn to revert, and again to re-distort. Dynamax
  or Gigantamax a distorted Pokemon (it should stay distorted, with the distorted look). Ash-Greninja: a distorted
  Greninja with Battle Bond (and high friendship) knocking a Pokemon out.
  New in this build: try some starters with /pokegive <name> distorted (and shiny, female for the Bulbasaur and
  Torchic lines, hisuian for Typhlosion/Samurott/Decidueye). Do the looks show (the animated flames, Torterra's
  volcano, the flytraps, the pillars)? Anything that looks broken or off-theme: tell me which Pokemon.
  From before: the mermaid tail, abilities turning when distorting, a wild Pokemon holding the crystal distorting.
  Does the Distort option show in the wheel (band on, crystal held)? Does the Pokemon change look when you pick it,
  and back with Revert Distortion, or when you take the crystal? Does it stay distorted after relogging? Does it
  enter battle distorted with the distorted moves?
  And the battle side, if you didn't get to it last time: the Distort button, the distorted moves on the tiles, the
  look and type change, back to normal after the battle, Arceus with a plate.
  If anything breaks, send the crash report or latest.log.

LICENCE
  CC BY-NC-SA 4.0 (non-commercial). The distorted textures are adaptations of Mega Showdown's (CC BY-NC-SA 4.0,
  by yajatkaul and contributors), recoloured. Code and other assets by ellecat5112 / CobbleEffort.
