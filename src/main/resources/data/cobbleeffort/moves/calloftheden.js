{
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
