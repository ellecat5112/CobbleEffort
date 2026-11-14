{
num: -3043,
accuracy: true,
basePower: 0,
category: "Status",
name: "Nectar Toast",
pp: 5,
priority: 0,
flags: {heal: 1, bypasssub: 1, allyanim: 1, metronome: 1},
onHit(pokemon) {
  const healed = this.heal(this.modify(pokemon.maxhp, 0.5));
  const boosted = this.boost({atk: 1}, pokemon);
  return !!(healed || boosted);
},
secondary: null,
target: "allies",
type: "Bug",
desc: "The user and its allies on the field restore 1/2 of their maximum HP and raise their Attack by 1 stage.",
shortDesc: "User and allies: heal 50%, +1 Atk.",
contestType: "Cute"
}
