{
onModifyMovePriority: -3,
onModifyMove(move) {
  if (move.category === 'Status') return;
  const before = move.onEffectiveness;
  move.onEffectiveness = function (typeMod, target, type, m) {
    if (target && target.hasType('Bug')) return type === 'Bug' ? 2 : 0;
    return before ? before.call(this, typeMod, target, type, m) : typeMod;
  };
},
onAnyNegateImmunity(pokemon, type) {
  if (pokemon && pokemon.hasType('Bug') && this.activePokemon === this.effectState.target && this.activeMove &&
      this.activeMove.category !== 'Status') return false;
},
flags: {},
name: "Insectivore",
rating: 3,
num: -3006
}
