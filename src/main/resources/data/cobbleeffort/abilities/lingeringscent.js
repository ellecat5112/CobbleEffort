{
onFaint(pokemon) {
  this.field.addPseudoWeather('lingeringscent', pokemon);
},
condition: {
  duration: 4,
  onFieldStart() {
    this.add('-fieldstart', 'ability: Lingering Scent');
  },
  onFieldResidualOrder: 26,
  onFieldResidualSubOrder: 2,
  onFieldResidual() {
    for (const p of this.getAllActive()) {
      if (p.fainted || !p.hp || p.hasType('Ghost')) continue;
      this.damage(p.baseMaxhp / 16, p, null, this.dex.conditions.get('lingeringscent'));
    }
  },
  onFieldEnd() {
    this.add('-fieldend', 'ability: Lingering Scent');
  }
},
flags: {},
name: "Lingering Scent",
rating: 2,
num: -3016
}
