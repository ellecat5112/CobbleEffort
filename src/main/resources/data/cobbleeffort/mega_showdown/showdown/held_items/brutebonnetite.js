({
  name: "Brute Bonnetite",
  spritenum: 0,
  megaStone: { "Brute Bonnet": "Brute Bonnet-Mega" },
  itemUser: ["Brute Bonnet"],
  onTakeItem(item, source) {
    return !item.megaStone?.[source.baseSpecies.baseSpecies];
  },
  num: 9102,
  gen: 9,
  isNonstandard: "Past",
})
