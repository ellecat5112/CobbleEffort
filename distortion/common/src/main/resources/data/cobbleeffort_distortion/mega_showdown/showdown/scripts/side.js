({
  chooseMove(moveText, targetLoc, event) {
    const Side = require("./sim/side").Side;
    if (typeof moveText === "string" && / distort$/.test(moveText.trim())) {
      let text = moveText.trim().replace(/ distort$/, "").trim();
      if (targetLoc === undefined && /\s(?:-|\+)?[1-3]$/.test(text)) {
        targetLoc = parseInt(text.slice(-2));
        text = text.slice(0, -2).trim();
      }
      const pokemon = this.active[this.getChoiceIndex()];
      if (!pokemon || !this.battle.actions.canToggleDistortion(pokemon)) {
        return Side.prototype.chooseMove.call(this, text, targetLoc, event);
      }
      const ok = Side.prototype.chooseMove.call(this, text, targetLoc, event);
      if (ok) this.choice.actions[this.choice.actions.length - 1].distort = true;
      return ok;
    }
    return Side.prototype.chooseMove.call(this, moveText, targetLoc, event);
  },
})
