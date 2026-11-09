({
  chooseMove(moveText, targetLoc, event) {
    const Side = require("./sim/side").Side;
    if (typeof moveText === "string" && / distort$/.test(moveText.trim())) {
      let text = moveText.trim().replace(/ distort$/, "").trim();
      if (targetLoc === undefined && /\s(?:-|\+)?[1-3]$/.test(text)) {
        targetLoc = parseInt(text.slice(-2));
        text = text.slice(0, -2).trim();
      }
      const index = this.getChoiceIndex();
      const pokemon = this.active[index];
      if (!pokemon) return this.emitChoiceError("Can't distort: no Pokemon");
      if (this.distortUsed || this.choice.distort) return this.emitChoiceError("Can't distort: you can only distort once per battle");
      if (!this.battle.actions.canDistort(pokemon)) return this.emitChoiceError(`Can't distort: ${pokemon.name} can't distort`);
      const ok = Side.prototype.chooseMove.call(this, text, targetLoc, event);
      if (ok) {
        // the queue turns this into a distort action before the move (see queue.js)
        this.choice.actions[this.choice.actions.length - 1].distort = true;
        this.choice.distort = true;
      }
      return ok;
    }
    return Side.prototype.chooseMove.call(this, moveText, targetLoc, event);
  },
})
