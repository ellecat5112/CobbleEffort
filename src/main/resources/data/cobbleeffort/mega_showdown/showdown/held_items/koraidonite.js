({
  name: "Koraidonite",
  spritenum: 0,
  megaStone: { "Koraidon": "Koraidon-Mega" },
  itemUser: ["Koraidon"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9107,
  gen: 9,
  isNonstandard: "Past",
})
