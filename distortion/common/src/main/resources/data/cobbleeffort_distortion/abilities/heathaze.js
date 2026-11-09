{
onImmunity(type, pokemon) {
      if (type === "sunnyday") return false;
    },
"onModifyAccuracyPriority": -1,
onModifyAccuracy(accuracy) {
      if (typeof accuracy !== "number") return;
      if (this.field.isWeather(["sunnyday", "desolateland"])) {
        this.debug("Snow Cloak - decreasing accuracy");
        return this.chainModify([3277, 4096]);
      }
    },
"flags": {"breakable":1},
"name": "Heat Haze",
"rating": 1.5,
"num": -31101
}
