{
num: -3041,
accuracy: 100,
basePower: 70,
category: "Physical",
name: "Roast & Press",
pp: 10,
priority: 0,
flags: {contact: 1, protect: 1, mirror: 1, metronome: 1},
onBasePower(basePower, pokemon, target) {
  const last = target.getLastAttackedBy();
  if (last && this.dex.moves.get(last.move).type === 'Fire') {
    this.debug('Roast & Press: target was roasted');
    return this.chainModify(2);
  }
},
secondary: null,
target: "normal",
type: "Ground",
desc: "Power doubles if the last move to hit the target was a Fire-type move.",
shortDesc: "2x power if the target was last hit by a Fire move.",
contestType: "Tough"
}
