{
onImmunity(type, pokemon) {
      if (type === "sandstorm" || type === "sunnyday" || type === "powder")
        return false;
    },
"onTryHitPriority": 1,
onTryHit(target, source, move) {
      if (
        move.flags["powder"] &&
        target !== source &&
        this.dex.getImmunity("powder", target)
      ) {
        this.add("-immune", target, "[from] ability: Sunscreen");
        return null;
      }
    },
"flags": {"breakable":1},
"name": "Sunscreen",
"rating": 2,
"num": -31126
}
