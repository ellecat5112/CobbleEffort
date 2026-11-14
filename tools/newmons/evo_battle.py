"""The abilities and moves of the user's nicotine and alcohol evolution lines (0.80.0): Nicotiny -> Curedrake ->
Cartelord, Emberbutt -> Smolderstump -> Cigarghast, Vapulon -> Modwing -> Subohmega, Hopsprout -> Maltwort ->
Brawlerry, Stumblepup -> Kegguard -> Avalanche Hound, Copperpot -> Alembix -> Stillforge. The names and the moves'
effects are the user's; the abilities' effects (only named) are ours. Merged into build.py's CUSTOM_ABILITIES /
CUSTOM_MOVES; tested in node against Cobblemon's Showdown.
"""

EVO_ABILITIES = {
    "alkaloidsap": {
        "name": "Alkaloid Sap",
        "js": """{
onDamagingHit(damage, target, source, move) {
  if (!this.checkMoveMakesContact(move, source, target) || !this.randomChance(3, 10)) return;
  if (this.random(2)) source.trySetStatus('psn', target);
  else source.addVolatile('confusion', target);
},
flags: {},
name: "Alkaloid Sap",
rating: 2,
num: -3048
}
""",
        "lang": "Its curled leaves ooze a fermented, dizzying sap: a Pokémon that touches it has a 30% chance of being "
                "poisoned or confused.",
    },
    "secondhandhaze": {
        "name": "Secondhand Haze",
        "js": """{
onStart(pokemon) {
  let activated = false;
  for (const target of pokemon.adjacentFoes()) {
    if (!activated) {
      this.add('-ability', pokemon, 'Secondhand Haze', 'boost');
      activated = true;
    }
    if (target.volatiles['substitute']) this.add('-immune', target);
    else this.boost({accuracy: -1}, target, pokemon, null, true);
  }
},
flags: {},
name: "Secondhand Haze",
rating: 3,
num: -3049
}
""",
        "lang": "It enters battle coughing out choking clouds of soot, lowering the accuracy of every opposing Pokémon.",
    },
    "lingeringember": {
        "name": "Lingering Ember",
        "js": """{
onResidualOrder: 10,
onResidual(pokemon) {
  if (!pokemon.hp) return;
  for (const foe of pokemon.foes()) {
    if (foe.status === 'brn') this.damage(foe.baseMaxhp / 16, foe, pokemon);
  }
},
flags: {},
name: "Lingering Ember",
rating: 3,
num: -3050
}
""",
        "lang": "Its fragrant smoke keeps old embers smouldering: at the end of each turn, every burned opposing "
                "Pokémon loses another 1/16 of its maximum HP.",
    },
    "overclockedcoil": {
        "name": "Overclocked Coil",
        "js": """{
onBasePowerPriority: 23,
onBasePower(basePower, attacker, defender, move) {
  if (move.type === 'Electric') return this.chainModify(1.5);
},
onAfterMoveSecondarySelf(source, target, move) {
  if (move.type === 'Electric' && move.category !== 'Status' && source.hp) {
    this.damage(source.baseMaxhp / 10, source, source, this.dex.abilities.get('overclockedcoil'));
  }
},
flags: {},
name: "Overclocked Coil",
rating: 3.5,
num: -3051
}
""",
        "lang": "It runs its coils past their limit: its Electric-type moves are 50% stronger, but each one it uses "
                "costs it 1/10 of its maximum HP in heat.",
    },
    "fermentation": {
        "name": "Fermentation",
        "js": """{
onDamagePriority: 1,
onDamage(damage, target, source, effect) {
  if (effect && ['psn', 'tox', 'brn'].includes(effect.id)) {
    this.heal(target.baseMaxhp / 8);
    return false;
  }
},
flags: {},
name: "Fermentation",
rating: 4,
num: -3052
}
""",
        "lang": "It ferments whatever ails it into sugar: instead of losing HP to poison or a burn, it restores 1/8 of "
                "its maximum HP every turn.",
    },
    "frothyguard": {
        "name": "Frothy Guard",
        "js": """{
onSourceModifyDamage(damage, source, target, move) {
  if (move.flags['contact']) return this.chainModify(0.7);
},
flags: {breakable: 1},
name: "Frothy Guard",
rating: 3,
num: -3053
}
""",
        "lang": "The thick, pillowy foam on its shoulders cushions blows: moves that make contact deal 30% less damage "
                "to it.",
    },
    "alpinespirit": {
        "name": "Alpine Spirit",
        "js": """{
onModifySpe(spe, pokemon) {
  if (this.field.isWeather(['hail', 'snow'])) return this.chainModify(2);
},
onImmunity(type, pokemon) {
  if (type === 'hail' || type === 'sandstorm' || type === 'frz') return false;
},
flags: {},
name: "Alpine Spirit",
rating: 3,
num: -3054
}
""",
        "lang": "Born for the high passes: its Speed doubles in snow or hail, it takes no damage from hail or "
                "sandstorms, and it can't be frozen.",
    },
    "condenser": {
        "name": "Condenser",
        "js": """{
onTryHitPriority: 1,
onTryHit(target, source, move) {
  if (target !== source && move.type === 'Fire') {
    if (!this.heal(target.baseMaxhp / 4)) this.add('-immune', target, '[from] ability: Condenser');
    return null;
  }
},
flags: {breakable: 1},
name: "Condenser",
rating: 3.5,
num: -3055
}
""",
        "lang": "Its cooling coils condense heat into pure water: Fire-type moves don't harm it, they restore 1/4 of "
                "its maximum HP.",
    },
    "highproof": {
        "name": "High Proof",
        "js": """{
onBasePowerPriority: 21,
onBasePower(basePower, attacker, defender, move) {
  if (move.type === 'Fire') return this.chainModify([5325, 4096]);
},
onModifyMove(move) {
  if (move.type !== 'Fire') return;
  const own = move.onEffectiveness;
  move.onEffectiveness = function (typeMod, target, type, m) {
    if (type === 'Water') return 0;
    if (own) return own.call(this, typeMod, target, type, m);
  };
},
flags: {},
name: "High Proof",
rating: 4,
num: -3056
}
""",
        "lang": "It refines raw energy into blazing high-proof plasma: its Fire-type moves are 30% stronger and burn "
                "even Water-type Pokémon at full strength (Water no longer resists them).",
    },
}

EVO_MOVES = {
    "calloftheden": {
        "name": "Call of the Den",
        "js": """{
num: -3063,
accuracy: true,
basePower: 0,
category: "Status",
name: "Call of the Den",
pp: 10,
priority: 0,
flags: {snatch: 1, sound: 1, metronome: 1},
onTry(source) {
  return source.side.pokemon.some(p => p !== source && !p.fainted && /hopple|rabbrute/.test(p.species.id));
},
onHit(pokemon) {
  const family = pokemon.side.pokemon.filter(p => p !== pokemon && !p.fainted && /hopple|rabbrute/.test(p.species.id)).length;
  const n = Math.min(2, family);
  this.add('-activate', pokemon, 'move: Call of the Den');
  return this.boost({atk: n, def: n}, pokemon, pokemon) !== false;
},
secondary: null,
target: "self",
type: "Normal",
desc: "Raises the user's Attack and Defense by 1 stage for each other Hopple or Rabbrute able to battle in its party (up to 2 stages). Fails if there are none. Outside battle, a Hopple with two or more Hopples in its party can use it from the interaction wheel to fuse them all into Rabbrute.",
shortDesc: "+1 Atk/Def per other Hopple in the party (max +2).",
contestType: "Cute"
}
""",
        "lang": "The user thumps the ground and calls its family: its Attack and Defense rise by 1 stage for every "
                "other Hopple in its party (up to 2). Outside battle, with three or more Hopples in the party, it fuses "
                "them all into a towering Rabbrute (from the interaction wheel).",
        "battle": {"cobblemon.battle.activate.calloftheden": "%1$s thumped the ground and called its family!"},
    },
    "goldenleafstorm": {
        "name": "Golden Leaf Storm",
        "js": """{
num: -3057,
accuracy: 95,
basePower: 65,
category: "Special",
name: "Golden Leaf Storm",
pp: 15,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1, wind: 1},
secondaries: [{chance: 100, boosts: {spe: -1}}, {chance: 30, status: 'tox'}],
target: "normal",
type: "Grass",
desc: "Lowers the target's Speed by 1 stage. 30% chance to badly poison the target.",
shortDesc: "-1 Spe to the target. 30% chance to badly poison.",
contestType: "Beautiful"
}
""",
        "lang": "The user whips up a storm of cured golden leaves that slows the target and may badly poison it.",
    },
    "ashchoke": {
        "name": "Ash Choke",
        "js": """{
num: -3058,
accuracy: 100,
basePower: 60,
category: "Special",
name: "Ash Choke",
pp: 15,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1},
onBasePower(basePower, pokemon, target) {
  if (target.status === 'brn') return this.chainModify(2);
},
secondary: {chance: 100, boosts: {accuracy: -1}},
target: "normal",
type: "Poison",
desc: "Power doubles if the target is burned. Lowers the target's accuracy by 1 stage.",
shortDesc: "2x power if the target is burned. -1 accuracy.",
contestType: "Tough"
}
""",
        "lang": "The user coughs a choking cloud of soot at the target, lowering its accuracy. It hits twice as hard "
                "if the target is burned.",
    },
    "twincoilsurge": {
        "name": "Twin-Coil Surge",
        "js": """{
num: -3059,
accuracy: 100,
basePower: 40,
category: "Special",
name: "Twin-Coil Surge",
pp: 10,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1},
multihit: 2,
onAfterMove(source) {
  this.field.addPseudoWeather('twincoilsurge', source);
},
condition: {
  duration: 5,
  onFieldStart() {
    this.add('-fieldstart', 'move: Twin-Coil Surge');
  },
  onModifyAccuracyPriority: -1,
  onModifyAccuracy(accuracy, target, source, move) {
    if (typeof accuracy !== 'number' || !target.hasType('Flying')) return;
    return this.chainModify([3277, 4096]);
  },
  onFieldResidualOrder: 27,
  onFieldResidualSubOrder: 5,
  onFieldEnd() {
    this.add('-fieldend', 'move: Twin-Coil Surge');
  }
},
secondary: null,
target: "normal",
type: "Electric",
desc: "Hits twice. Then a thick vapour fills the field for 5 turns: moves aimed at Flying-type Pokemon are 20% less accurate.",
shortDesc: "Hits 2 times. 5 turns: Flying types are harder to hit.",
contestType: "Cool"
}
""",
        "lang": "The user fires both of its coils in turn, hitting twice, and leaves a thick vapour on the field for "
                "five turns in which Flying-type Pokémon are harder to hit.",
        "battle": {"cobblemon.battle.fieldstart.twincoilsurge": "A thick vapour cloud rolled over the field!",
                   "cobblemon.battle.fieldend.twincoilsurge": "The vapour cloud dispersed."},
    },
    "yeastbubble": {
        "name": "Yeast Bubble",
        "js": """{
num: -3060,
accuracy: 90,
basePower: 35,
category: "Special",
name: "Yeast Bubble",
pp: 15,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1},
volatileStatus: 'partiallytrapped',
onHit(target, source) {
  source.addVolatile('yeastbubble');
},
condition: {
  duration: 5,
  onStart(pokemon) {
    this.add('-start', pokemon, 'Yeast Bubble');
  },
  onResidualOrder: 6,
  onResidual(pokemon) {
    this.heal(pokemon.baseMaxhp / 16);
  },
  onEnd(pokemon) {
    this.add('-end', pokemon, 'Yeast Bubble', '[silent]');
  }
},
secondary: null,
target: "normal",
type: "Fairy",
desc: "Traps and damages the target for 4-5 turns. The user restores 1/16 of its maximum HP at the end of each turn for 5 turns.",
shortDesc: "Traps/damages for 4-5 turns; user heals 1/16 each turn.",
contestType: "Cute"
}
""",
        "lang": "The user traps the target in sticky, bubbling foam that hurts it every turn for four or five turns, "
                "while the warm fermentation restores a little of the user's HP each turn.",
        "battle": {"cobblemon.battle.activate.yeastbubble": "%1$s was trapped in sticky foam!",
                   "cobblemon.battle.damage.yeastbubble": "%1$s is hurt by the sticky foam!",
                   "cobblemon.battle.end.yeastbubble": "%1$s broke free of the foam!",
                   "cobblemon.battle.start.yeastbubble": "%1$s is fermenting happily!"},
    },
    "warmingdraught": {
        "name": "Warming Draught",
        "js": """{
num: -3061,
accuracy: true,
basePower: 0,
category: "Status",
name: "Warming Draught",
pp: 10,
priority: 0,
flags: {heal: 1, snatch: 1, bypasssub: 1, allyanim: 1, metronome: 1},
onHit(pokemon) {
  let success = false;
  if (pokemon.status === 'frz' || pokemon.status === 'brn') success = pokemon.cureStatus() || success;
  success = !!this.heal(this.modify(pokemon.maxhp, 0.35)) || success;
  return success;
},
secondary: null,
target: "allies",
type: "Normal",
desc: "The user and its allies on the field are cured of freezing and burns and restore 35% of their maximum HP.",
shortDesc: "User and allies: cure frz/brn, heal 35%.",
contestType: "Cute"
}
""",
        "lang": "The user shares warming sips of herbal tonic: it and its allies are thawed and cured of burns, and "
                "restore 35% of their HP.",
    },
    "condense": {
        "name": "Condense",
        "js": """{
num: -3062,
accuracy: true,
basePower: 0,
category: "Status",
name: "Condense",
pp: 10,
priority: 0,
flags: {snatch: 1, metronome: 1},
onHit(pokemon) {
  const cleared = this.field.clearWeather() | this.field.clearTerrain();
  return this.boost({def: 1, spd: 1}, pokemon, pokemon) !== false || !!cleared;
},
secondary: null,
target: "self",
type: "Water",
desc: "Ends the weather and the terrain, then raises the user's Defense and Special Defense by 1 stage.",
shortDesc: "Clears weather and terrain; +1 Def, +1 SpD.",
contestType: "Clever"
}
""",
        "lang": "The user condenses the air round it, clearing away the weather and the terrain, and raises its "
                "Defense and Sp. Def.",
    },
}
