CobbleEffort: Distortion @VERSION@
==================================

A new battle gimmick for Cobblemon. A Pokemon holding the Distortion Crystal, with its trainer wearing the
Distortion Band, distorts: its types turn into their weaknesses, its moves follow, and its colours invert.

A TEST BUILD. What's in it:
  - The Distortion Band and the Distortion Crystal (one crystal for every Pokemon), in the "Distortion" creative tab.
  - A "Distortion" accessory slot (open your Accessories screen); the band goes there.
  - Distorted forms for Giratina, Dialga, Palkia and Arceus (including the Origin forms and every Arceus plate type),
    NEW: the Gen 1 legendary and mythical Pokemon (Articuno, Zapdos, Moltres, Mewtwo, Mew), and every starter and its evolutions, Gen 1 to 9 (81 Pokemon, plus the Hisuian forms of Typhlosion, Samurott
    and Decidueye and Greninja's Bond form). Each line has its own distorted look:
      water starters -> plant-inspired, grass starters -> natural disasters, fire starters -> sea life
    (see STARTERS below).
  - Distorting in battle, and from the interaction wheel (the radial menu) outside battle.
  - Abilities follow when they're tied to the Pokemon's type: Overgrow -> Blaze, Blaze -> Torrent, Torrent -> Overgrow,
    and NEW ones where no real ability fits: Storm Power (Solar Power, in rain), Flash Flood (Flash Fire, for Water),
    Blubber (Thick Fat, against Water and Ice), Blossom Voice (Liquid Voice, Grass) and Scrappy Mind (Scrappy,
    Psychic). Abilities that aren't tied to its type stay.
  - Wild Pokemon and NPC trainers' Pokemon holding the crystal (Arceus: a plate) distort on their first move.

HOW TO DISTORT IN BATTLE
  1. Wear the Distortion Band in the Distortion slot.
  2. Give the Distortion Crystal to a distortable Pokemon (Giratina, Dialga, Palkia, the Gen 1 legendaries and Mew,
     any starter or its evolutions).
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

You can still give a distorted-looking Pokemon with a command:   /pokegive giratina distorted

INSTALL
  Unzip and put ONE jar in your mods folder: the -fabric jar on Fabric, the -neoforge jar on NeoForge.
  Needs: Cobblemon 1.8.4+, Mega Showdown 1.3.3+, Accessories, Architectury API. Install it on the server too.

PLEASE TEST AND REPORT
  New in this build: Mew (the orb and the cord: do they sit right while it floats and animates?), Mewtwo (the arms
  and bulk), the legendary birds.
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
