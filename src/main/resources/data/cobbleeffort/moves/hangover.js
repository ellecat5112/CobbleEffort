{
num: -3044,
accuracy: 100,
basePower: 70,
category: "Special",
name: "Hangover",
pp: 10,
priority: 0,
flags: {protect: 1, mirror: 1, metronome: 1},
onBasePower(basePower, pokemon, target) {
  const last = target.lastMove;
  if (last && last.category === 'Status' && (last.boosts || (last.self && last.self.boosts))) {
    target.m.hangover = true;
    return this.chainModify(2);
  }
  target.m.hangover = false;
},
onHit(target) {
  if (target.m.hangover) {
    target.clearBoosts();
    this.add('-clearboost', target);
  }
  target.m.hangover = false;
},
secondary: null,
target: "normal",
type: "Ghost",
desc: "If the target's last move was a status move that raises stats, this move's power doubles and the target loses all its stat stages.",
shortDesc: "2x and clears boosts if the target last used a boosting move.",
contestType: "Clever"
}
