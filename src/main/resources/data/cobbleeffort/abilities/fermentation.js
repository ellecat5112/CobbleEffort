{
onDamagePriority: 1,
onDamage(damage, target, source, effect) {
  if (effect && ['psn', 'tox', 'brn'].includes(effect.id)) {
    this.heal(target.baseMaxhp / 8);
    return false;
  }
},
flags: {},
name: "Fermentation",
rating: 4,
num: -3052
}
