{
"onModifySpAPriority": 5,
onModifySpA(spa, pokemon) {
      if (["raindance", "primordialsea"].includes(pokemon.effectiveWeather())) {
        return this.chainModify(1.5);
      }
    },
onWeather(target, source, effect) {
      if (target.hasItem("utilityumbrella")) return;
      if (effect.id === "raindance" || effect.id === "primordialsea") {
        this.damage(target.baseMaxhp / 8, target, target);
      }
    },
"flags": {},
"name": "Storm Power",
"rating": 2,
"num": -31101
}
