{
onDamagePriority: -30,
onDamage(damage, target, source, effect) {
  if (!effect || effect.effectType !== 'Move' || damage < target.hp || target.m.pharaohsCurse) return damage;
  target.m.pharaohsCurse = true;
  this.add('-ability', target, "Pharaoh's Curse");
  const half = Math.max(1, Math.floor(target.maxhp / 2));
  this.boost({atk: 2, spa: 2}, target, target);
  if (target.hp > half) return target.hp - half;
  if (target.hp < half) this.heal(half - target.hp, target, target);
  return 0;
},
flags: {breakable: 1},
name: "Pharaoh's Curse",
rating: 4,
num: -3003
}
