{
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
