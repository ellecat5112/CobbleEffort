{
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
