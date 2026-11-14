{
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
