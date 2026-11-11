{
"onModifyMovePriority": -5,
onModifyMove(move) {
      if (!move.ignoreImmunity) move.ignoreImmunity = {};
      if (move.ignoreImmunity !== true) {
        move.ignoreImmunity["Rock"] = true;
        move.ignoreImmunity["Normal"] = true;
      }
    },
onTryBoost(boost, target, source, effect) {
      if (effect.name === "Intimidate" && boost.atk) {
        delete boost.atk;
        this.add(
          "-fail",
          target,
          "unboost",
          "Attack",
          "[from] ability: Rock Scrappy",
          "[of] " + target,
        );
      }
    },
"flags": {},
"name": "Rock Scrappy",
"rating": 3,
"num": -31128
}
