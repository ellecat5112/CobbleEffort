{
onDamagePriority: -30,
onDamage(damage, target, source, effect) {
  if (!effect || effect.effectType !== 'Move' || damage < target.hp || target.hp <= 1 || target.m.cryptobiosis) return damage;
  target.m.cryptobiosis = true;
  this.add('-ability', target, 'Cryptobiosis');
  return target.hp - 1;
},
flags: {breakable: 1},
name: "Cryptobiosis",
rating: 3,
num: -3020
}
