{
"onModifyMovePriority": -5,
onModifyMove(move) {
      if (!move.ignoreImmunity) move.ignoreImmunity = {};
      if (move.ignoreImmunity !== true) {
        move.ignoreImmunity["Psychic"] = true;
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
          "[from] ability: Scrappy Mind",
          "[of] " + target,
        );
      }
    },
"flags": {},
"name": "Scrappy Mind",
"rating": 3,
"num": -31104
}
