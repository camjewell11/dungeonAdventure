# enemies and their respective xp, health, and damage
# health is randomized on encounter
enemy_table = {           # [ID,  xp,  health min/max, damage]
    "Cricket":              [1,   10,       10,    20,   2],
    "Ant":                  [1,   10,        1,     5,   1],
    "Spider":               [2,   15,       10,    20,   3],
    "Rat":                  [2,  150,       30,    50,   5],
    "Pigeon":               [3,  100,       25,    50,   5],
    "Lizard":               [3,   50,       20,    30,   6],
    "Scorpion":             [4,   50,       10,    20,   8],
    "Skeleton":             [4,  200,       20,    50,   9],
    "Dwarf":                [5,  300,       50,   100,  10],
    "Wild Dog":             [5,  150,       40,    80,  10],
    "Falcon":               [6,  125,       25,    75,  11],
    "Rabid Dog":            [6,  200,       40,    80,  12],
    "Drunken Dwarf":        [7,  250,       50,   100,  15],
    "Hawk":                 [7,  175,       30,    80,  13],
    "Ghostly Figure":       [8,  200,       10,   150,   8],
    "Ghostly Creature":     [8,  250,       20,   100,  10],
    "Angry Beggar":         [9,  300,       60,   120,  14],
    "Wolf":                 [9,  300,       50,   125,  16],
    "Skeleton Knight":      [10, 350,       75,   150,  12],
    "Skeleton Warrior":     [10, 400,       100,  175,  13],
    "Strange Man":          [11, 400,       5,     50,  25],
    "Novice Wizard":        [11, 425,       30,   100,  15],
    "Novice Warrior":       [11, 450,       100,  150,  13],
    "Giant Rat":            [12, 300,       100,  200,   5],
    "Massive Ant":          [12, 250,       50,   100,  10],
    "Mysterious Presence":  [13, 500,       10,    25,  50],
    "Novice Archer":        [13, 400,       50,   125,  13],
    "Giant":                [14, 500,       150,  250,  15],
    "Novice Assassin":      [14, 400,       50,   100,  15],
    "Eagle":                [15, 350,       75,   150,  20],
    "Bear":                 [15, 500,       150,  200,  18]
}

# xp required to reach level; max level 200
# TODO refactor to use an equation rather than static values
level_table = {
    1: 0,
    2: 50,
    3: 100,
    4: 150,
    5: 200,
    6: 300,
    7: 500,
    8: 750,
    9: 1000,
    10: 1500,
    11: 2000,
    12: 2750,
    13: 3500,
    14: 4500,
    15: 5500,
    16: 6750,
    17: 8000,
    18: 10000,
    19: 14000,
    20: 20000,
    21: 30000,
    22: 40000,
    23: 50000,
    24: 60000,
    25: 70000,
    26: 80000,
    27: 90000,
    28: 100000,
    29: 110000,
    30: 120000,
    31: 130000,
    32: 140000,
    33: 150000,
    34: 160000,
    35: 170000,
    36: 180000,
    37: 190000,
    38: 200000,
    39: 210000,
    40: 220000,
    41: 230000,
    42: 240000,
    43: 250000,
    44: 260000,
    45: 270000,
    46: 280000,
    47: 290000,
    48: 300000,
    49: 310000,
    50: 320000,
    51: 330000,
    52: 340000,
    53: 350000,
    54: 360000,
    55: 370000,
    56: 380000,
    57: 390000,
    58: 400000,
    59: 410000,
    60: 420000,
    61: 430000,
    62: 440000,
    63: 450000,
    64: 460000,
    65: 470000,
    66: 480000,
    67: 490000,
    68: 500000,
    69: 510000,
    70: 520000,
    71: 530000,
    72: 540000,
    73: 550000,
    74: 560000,
    75: 570000,
    76: 580000,
    77: 590000,
    78: 600000,
    79: 610000,
    80: 620000,
    81: 630000,
    82: 640000,
    83: 650000,
    84: 660000,
    85: 670000,
    86: 680000,
    87: 690000,
    88: 700000,
    89: 710000,
    90: 720000,
    91: 730000,
    92: 740000,
    93: 750000,
    94: 760000,
    95: 770000,
    96: 780000,
    97: 790000,
    98: 800000,
    99: 810000,
    100: 820000,
    101: 830000,
    102: 840000,
    103: 850000,
    104: 860000,
    105: 870000,
    106: 880000,
    107: 890000,
    108: 900000,
    109: 910000,
    110: 920000,
    111: 930000,
    112: 940000,
    113: 950000,
    114: 960000,
    115: 970000,
    116: 980000,
    117: 990000,
    118: 1000000,
    119: 1010000,
    120: 1020000,
    121: 1030000,
    122: 1040000,
    123: 1050000,
    124: 1060000,
    125: 1070000,
    126: 1080000,
    127: 1090000,
    128: 1100000,
    129: 1110000,
    130: 1120000,
    131: 1130000,
    132: 1140000,
    133: 1150000,
    134: 1160000,
    135: 1170000,
    136: 1180000,
    137: 1190000,
    138: 1200000,
    139: 1210000,
    140: 1220000,
    141: 1230000,
    142: 1240000,
    143: 1250000,
    144: 1260000,
    145: 1270000,
    146: 1280000,
    147: 1290000,
    148: 1300000,
    149: 1310000,
    150: 1320000,
    151: 1330000,
    152: 1340000,
    153: 1350000,
    154: 1360000,
    155: 1370000,
    156: 1380000,
    157: 1390000,
    158: 1400000,
    159: 1410000,
    160: 1420000,
    161: 1430000,
    162: 1440000,
    163: 1450000,
    164: 1460000,
    165: 1470000,
    166: 1480000,
    167: 1490000,
    168: 1500000,
    169: 1510000,
    170: 1520000,
    171: 1530000,
    172: 1540000,
    173: 1550000,
    174: 1560000,
    175: 1570000,
    176: 1580000,
    177: 1590000,
    178: 1600000,
    179: 1610000,
    180: 1620000,
    181: 1630000,
    182: 1640000,
    183: 1650000,
    184: 1660000,
    185: 1670000,
    186: 1680000,
    187: 1690000,
    188: 1700000,
    189: 1710000,
    190: 1720000,
    191: 1730000,
    192: 1740000,
    193: 1750000,
    194: 1760000,
    195: 1770000,
    196: 1780000,
    197: 1790000,
    198: 1800000,
    199: 1810000,
    200: 1820000
}

# dictionary of available potions
potionSizes = [
    "Tiny Potion", "Little Potion", "Small Potion", "Regular Potion", "Big Potion",
    "Large Potion", "Huge Potion", "Gigantic Potion", "Epic Potion", "Legendary Potion"
]
currencyName = "Gold Pieces"

# item table # for which floor you can find which items
# also specific what can be bought in the shop once you have unlocked a stage
item_table1 = {      # [ID, Value]
    currencyName:      [1,      1],
    potionSizes[0]:    [2,      5]
}
item_table2 = {      # [ID, Value]
    currencyName:      [1,      1],
    potionSizes[0]:    [2,      5],
    potionSizes[1]:    [3,     10]
}
item_table3 = {      # [ID, Value]
    currencyName:      [1,      1],
    potionSizes[0]:    [2,      5],
    potionSizes[1]:    [3,     10],
    potionSizes[2]:    [4,     15],
    "Compass":         [5,     30]
}
item_table4 = {      # [ID, Value]
    currencyName:      [1,      1],
    potionSizes[1]:    [3,     10],
    potionSizes[2]:    [4,     15],
    potionSizes[3]:    [5,     25],
    "Compass":         [5,     30]
}
item_table5 = {      # [ID, Value]
    currencyName:      [1,      1],
    potionSizes[2]:    [4,     15],
    potionSizes[3]:    [5,     25],
    potionSizes[4]:    [6,     45],
    "Compass":         [5,     30]
}
item_table6 = {      # [ID, Value]
    currencyName:      [1,      1],
    potionSizes[3]:    [5,     25],
    potionSizes[4]:    [6,     45],
    potionSizes[5]:    [7,     75],
    "Compass":         [5,     30]
}
item_table7 = {      # [ID, Value]
    currencyName:      [1,      1],
    potionSizes[4]:    [6,     45],
    potionSizes[5]:    [7,     75],
    potionSizes[6]:    [8,    100],
    "Compass":         [5,     30]
}
item_table8 = {      # [ID, Value]
    currencyName:      [1,      1],
    potionSizes[5]:    [7,     75],
    potionSizes[6]:    [8,    100],
    potionSizes[7]:    [9,    150],
    "Compass":         [5,     30]
}
item_table9 = {      # [ID, Value]
    currencyName:      [1,      1],
    potionSizes[7]:    [9,    150],
    potionSizes[8]:    [10,   500],
    "Compass":         [5,     30]
}
item_table10 = {     # [ID, Value]
    potionSizes[9]: [11, 1000]
}

# static text; reused in multiple functions (IO)
promptAction = "What would you like to do?"
invalidResponse = "Invalid selection.\n"

directionalMessages = [
    "You feel a force pull you to the %s...",
    "There seems to be an inviting presence to the %s...",
    "You feel a flow of air moving to the %s..."
]

sneakOptions = [
    "You managed to get by unnoticed...\n",
    "You crawl beneath the danger in a sewage grate...\n",
    "You sprint quietly beside the creature and sidle on...\n"
]
failedSneakOptions = [
    "You couldn't sneak by!\n",
    "The creature sees you!\n",
    "You were unsuccessful!\n"
]
noSneakOptions = [
    "You charge unwittingly into battle!\n",
    "Prepare for battle!\n",
    "You're in for it now!\n"
]

# xp awarded for each stage; 30 stages currently
stageXP = [
    50, 100, 150, 250, 500, 750, 1000, 1500, 2000, 2500, 3000,
    3500, 4000, 4500, 5000, 6000, 7000, 8000, 9000, 10000,
    12500, 15000, 17500, 20000, 22500, 25000, 30000, 35000, 40000
]