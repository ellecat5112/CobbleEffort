{
onEffectiveness(typeMod, target, type, move) {
  if (!move || target !== this.effectState.target) return typeMod;
  return move.type === 'Normal' ? 1 : 0;
},
onNegateImmunity(pokemon, type) {
  if (type === 'Ghost') return false;
},
onModifyMovePriority: -2,
onModifyMove(move) {
  if (move.type !== 'Normal' || move.category === 'Status') return;
  move.ignoreImmunity = Object.assign({}, typeof move.ignoreImmunity === 'object' ? move.ignoreImmunity : {}, {Normal: true});
  move.onEffectiveness = function (typeMod, target, type) {
    return type === 'Normal' ? 1 : 0;
  };
},
flags: {failroleplay: 1, noreceiver: 1, noentrain: 1, notrace: 1, failskillswap: 1, cantsuppress: 1},
name: "System Error",
rating: 4,
num: -3005
}
