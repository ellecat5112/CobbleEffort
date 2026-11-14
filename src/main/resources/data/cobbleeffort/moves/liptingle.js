{
num: -3026,
accuracy: true,
basePower: 0,
category: "Status",
name: "Lip Tingle",
pp: 10,
priority: 0,
flags: {snatch: 1, metronome: 1},
boosts: {spe: 2, spa: 2},
onHit(pokemon) {
  pokemon.addVolatile('liptingle');
},
condition: {
  duration: 2,
  onEnd(pokemon) {
    if (!pokemon.hp) return;
    this.add('-activate', pokemon, 'move: Lip Tingle');
    this.boost({spe: -1, spa: -1}, pokemon, pokemon);
  }
},
secondary: null,
target: "self",
type: "Fairy",
desc: "Raises the user's Speed and Sp. Atk by 2 stages; at the end of the next turn they fall by 1 stage each.",
shortDesc: "+2 Spe/SpA; -1 Spe/SpA at the end of next turn.",
contestType: "Cute"
}
