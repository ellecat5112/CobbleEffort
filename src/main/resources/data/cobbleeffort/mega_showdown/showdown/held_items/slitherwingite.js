({
  name: "Slither Wingite",
  spritenum: 0,
  megaStone: { "Slither Wing": "Slither Wing-Mega" },
  itemUser: ["Slither Wing"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9104,
  gen: 9,
  isNonstandard: "Past",
})
