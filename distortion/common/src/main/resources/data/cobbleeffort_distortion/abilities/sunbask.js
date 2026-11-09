{
onWeather(target, source, effect) {
      if (effect.id === "sunnyday" || effect.id === "desolateland") {
        this.heal(target.baseMaxhp / 16);
      }
    },
onImmunity(type, pokemon) {
      if (type === "sunnyday") return false;
    },
"flags": {},
"name": "Sun Bask",
"rating": 1,
"num": -31109
}
