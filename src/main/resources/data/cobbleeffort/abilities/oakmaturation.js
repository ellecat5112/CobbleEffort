{
onTryHeal(damage, target, source, effect) {
  if (effect && effect.isBerry) return this.chainModify(2);
},
onChangeBoost(boost, target, source, effect) {
  if (effect && effect.isBerry) {
    let b;
    for (b in boost) boost[b] *= 2;
  }
},
onSourceModifyDamagePriority: -1,
onSourceModifyDamage(damage, source, target, move) {
  if (target.abilityState.berryWeaken) {
    target.abilityState.berryWeaken = false;
    return this.chainModify(0.5);
  }
},
onTryEatItemPriority: -1,
onTryEatItem(item, pokemon) {
  this.add('-activate', pokemon, 'ability: Oak Maturation');
},
onEatItem(item, pokemon) {
  pokemon.abilityState.berryWeaken = !!item.onSourceModifyDamage;
  pokemon.abilityState.oakBerry = item.id;
  pokemon.abilityState.oakTurns = 0;
},
onResidualOrder: 28,
onResidualSubOrder: 3,
onResidual(pokemon) {
  const berry = pokemon.abilityState.oakBerry;
  if (!berry || pokemon.item) return;
  if (++pokemon.abilityState.oakTurns < 2) return;
  pokemon.abilityState.oakBerry = '';
  if (pokemon.setItem(berry)) {
    this.add('-item', pokemon, this.dex.items.get(berry), '[from] ability: Oak Maturation');
  }
},
flags: {},
name: "Oak Maturation",
rating: 3.5,
num: -3035
}
