#!/usr/bin/env python2
import sys
import os
from random import randint
import random
from select import select

character = "none"
faction = "none"
charFile = "none"
inventoryFile = "none"
skillPoints = 0
first = True
floorMap = []
begin = []
stop = []
current = []
youDied = False
autotake = 0
autosneak = 0
enemy_table = {           # [ID,  xp,  health(min,  max) damage]
    "Cricket":              [1,   10,  randint(10,   20),  2],
    "Ant":                  [1,   10,  randint(1,     5),  1],
    "Spider":               [2,   15,  randint(10,   20),  3],
    "Rat":                  [2,  150,  randint(30,   50),  5],
    "Pigeon":               [3,  100,  randint(25,   50),  5],
    "Lizard":               [3,   50,  randint(20,   30),  6],
    "Scorpion":             [4,   50,  randint(10,   20),  8],
    "Skeleton":             [4,  200,  randint(20,   50),  9],
    "Dwarf":                [5,  300,  randint(50,  100), 10],
    "Wild Dog":             [5,  150,  randint(40,   80), 10],
    "Falcon":               [6,  125,  randint(25,   75), 11],
    "Rabid Dog":            [6,  200,  randint(40,   80), 12],
    "Drunken Dwarf":        [7,  250,  randint(50,  100), 15],
    "Hawk":                 [7,  175,  randint(30,   80), 13],
    "Ghostly Figure":       [8,  200,  randint(10,  150),  8],
    "Ghostly Creature":     [8,  250,  randint(20,  100), 10],
    "Angry Beggar":         [9,  300,  randint(60,  120), 14],
    "Wolf":                 [9,  300,  randint(50,  125), 16],
    "Skeleton Knight":      [10, 350,  randint(75,  150), 12],
    "Skeleton Warrior":     [10, 400,  randint(100, 175), 13],
    "Strange Man":          [11, 400,  randint(5,    50), 25],
    "Novice Wizard":        [11, 425,  randint(30,  100), 15],
    "Novice Warrior":       [11, 450,  randint(100, 150), 13],
    "Giant Rat":            [12, 300,  randint(100, 200),  5],
    "Massive Ant":          [12, 250,  randint(50,  100), 10],
    "Mysterious Presence":  [13, 500,  randint(10,   25), 50],
    "Novice Archer":        [13, 400,  randint(50,  125), 13],
    "Giant":                [14, 500,  randint(150, 250), 15],
    "Novice Assassin":      [14, 400,  randint(50,  100), 15],
    "Eagle":                [15, 350,  randint(75,  150), 20],
    "Bear":                 [15, 500,  randint(150, 200), 18]
}
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
item_table1 = {      # [ID, Value]
    "Gold Piece":      [1,      1],
    "Tiny Potion":     [2,      5]
}
item_table2 = {      # [ID, Value]
    "Gold Piece":      [1,      1],
    "Tiny Potion":     [2,      5],
    "Little Potion":   [3,     10]
}
item_table3 = {      # [ID, Value]
    "Gold Piece":      [1,      1],
    "Tiny Potion":     [2,      5],
    "Little Potion":   [3,     10],
    "Small Potion":    [4,     15],
    "Compass":         [5,     30]
}
item_table4 = {      # [ID, Value]
    "Gold Piece":      [1,      1],
    "Little Potion":   [3,     10],
    "Small Potion":    [4,     15],
    "Regular Potion":  [5,     25],
    "Compass":         [5,     30]
}
item_table5 = {      # [ID, Value]
    "Gold Piece":      [1,      1],
    "Small Potion":    [4,     15],
    "Regular Potion":  [5,     25],
    "Big Potion":      [6,     45],
    "Compass":         [5,     30]
}
item_table6 = {      # [ID, Value]
    "Gold Piece":      [1,      1],
    "Regular Potion":  [5,     25],
    "Big Potion":      [6,     45],
    "Large Potion":    [7,     75],
    "Compass":         [5,     30]
}
item_table7 = {      # [ID, Value]
    "Gold Piece":      [1,      1],
    "Big Potion":      [6,     45],
    "Large Potion":    [7,     75],
    "Huge Potion":     [8,    100],
    "Compass":         [5,     30]
}
item_table8 = {      # [ID, Value]
    "Gold Piece":      [1,      1],
    "Large Potion":    [7,     75],
    "Huge Potion":     [8,    100],
    "Gigantic Potion": [9,    150],
    "Compass":         [5,     30]
}
item_table9 = {      # [ID, Value]
    "Gold Piece":      [1,      1],
    "Gigantic Potion": [9,    150],
    "Epic Potion":     [10,   500],
    "Compass":         [5,     30]
}
item_table10 = {     # [ID, Value]
    "Legendary Potion": [11, 1000]
}


def print_dash(skip=False):
    if skip:
        print "------------------------------\n"
    else:
        print "------------------------------"


def start():
    while True:
        print "What would you like to do?"
        print_dash()
        print "Create Character:        1"
        print "Select Character:        2"
        print "Play Game                3"
        print "Settings:                4"
        print "Exit:                    5"

        selection = raw_input("\n")
        selection = selection.lower()
        print_dash(True)
        if selection == '1':
            create_character()
        elif selection == '2':
            select_character()
        elif selection == '3':
            play_game()
        elif selection == '4':
            settings()
        elif selection == '5' or selection == 'q':
            break
        elif selection == 'debug':
            if character == 'none':
                select_character()
            debug_menu()
    else:
        print "That was not a valid selection.\n"


def debug_menu():
    while True:
        print "Secret Debug Menu"
        print_dash()
        print "For active info         'i'"
        print "To level up a skill     'u'"
        print "To add XP               'x'"
        print "To view enemy tables    'e'"
        print "To kill player          'k'"
        print "To create floorMap      'm'"
        print "To return               'q'"

        selection2 = raw_input("\n")
        selection2 = selection2.lower()
        print_dash(True)
        if selection2 == 'i':
            display_info()
        elif selection2 == 'u':
            level_up()
        elif selection2 == 'e':
            print enemy_table
        elif selection2 == 'x':
            while True:
                try:
                    num = int(raw_input("How much XP would you like to add?\n"))
                except ValueError:
                    print "That wasn't a number!"
                else:
                    break
            print ""
            add_xp(num)
            print "Total XP now:            %s\n" % get_xp()
        elif selection2 == 'k':
            died()
        elif selection2 == 'm':
            while True:
                try:
                    num = int(raw_input("Enter a Stage number.\n"))
                except ValueError:
                    print "That wasn't a number!"
                else:
                    break
            print ""
            generate_floor(num)
            print_floor()
        elif selection2 == 'q':
            break
        else:
            print "Invalid selection.\n"


def settings():
    if character == 'none':
        select_character()
    global autotake
    while True:
        print "         Settings            "
        print_dash()
        print "To Delete Character       'd'"
        print "To toggle autotake items  't'"
        print "To toggle autosneak       's'"
        print "To quit                   'q'"
        selection = raw_input("\n")
        print ""

        if selection == 'd':
            chars = os.listdir("characters")
            print "Which Character would you like to delete?"
            spot = 0
            for i in chars:
                chars[spot] = i[:-4]
                print "- %s" % chars[spot]
                spot += 1
            print "\nTo cancel                 'c'"

            while True:
                choice = raw_input("\n")
                print ""
                if choice == 'c':
                    break
                elif choice not in chars:
                    print "%s is not a valid character." % choice
                    print_dash(True)
                    print "Which Character would you like to delete?"
                    for i in chars:
                        print "- %s" % i
                    print "\nTo cancel            'c'"
                else:
                    os.remove("characters/%s.txt" % choice)
                    os.remove("inventories/%s.inv" % choice)
                    print "Removed %s.\n" % choice
                    print_dash()
        elif selection == 't':
            print "Would you like to change autotake? Currently set to %s. (y/n)" % get_autotake()
            choice = raw_input("\n")
            print ""
            if choice == 'y':
                toggle_autotake()
                print "Autotake is now %s.\n" % get_autotake()
            elif choice == 'n':
                print "Returning to menu.\n"
            else:
                print "Invalid Selection.\n"
        elif selection == 's':
            print "Would you like to change autosneak? Currently set to %s. (y/n)" % get_autosneak()
            choice = raw_input("\n")
            print ""
            if choice == 'y':
                toggle_autosneak()
                print "Autosneak is now %s.\n" % get_autosneak()
            elif choice == 'n':
                print "Returning to menu.\n"
            else:
                print "Invalid Selection.\n"
        elif selection == 'q':
            break
        else:
            print "Invalid Selection.\n"


def create_character():
    print "New Character Creation"
    print_dash()

    while True:
        name = raw_input("Enter your name: ")
        print_dash()
        filename = "characters/" + name + ".txt"
        global character
        global charFile
        global inventoryFile
        global faction

        if os.path.isfile(filename):
            print "Character already exists."
            print_dash(True)
        else:
            f = open(filename, "w")
            f.write(name + "\n")
            while True:
                print "\nSelect Faction"
                print_dash()
                print "Wizard         1"
                print "Archer         2"
                print "Warrior        3"
                print "Assassin       4"
                print_dash()
                print "View Stats     5\n"

                selection = raw_input("")
                print_dash(True)
                if selection == '1':
                    f.write("Wizard\n")
                    faction = "Wizard"
                    f.close()
                    create_wizard(filename)
                    break
                elif selection == '2':
                    f.write("Archer\n")
                    faction = "Archer"
                    f.close()
                    create_archer(filename)
                    break
                elif selection == '3':
                    f.write("Warrior\n")
                    faction = "Warrior"
                    f.close()
                    create_warrior(filename)
                    break
                elif selection == '4':
                    f.write("Assassin\n")
                    faction = "Assassin"
                    f.close()
                    create_assassin(filename)
                    break
                elif selection == '5':
                    display_faction_stats()
                else:
                    print "That was not a valid selection."
            print "Created new character, %s!" % name
            print_dash(True)

        character = name
        charFile = filename
        inventoryFile = "inventories/" + character + ".inv"

        f = open(inventoryFile, "w")
        f.write("Inventory\n")
        f.write("Gold Pieces:0\n")
        f.close()

        break


def select_character():
    chars = os.listdir("characters")
    print "Which Character would you like to play as?"
    spot = 0
    for i in chars:
        chars[spot] = i[:-4]
        print "- %s" % chars[spot]
        spot += 1
    print "\nTo cancel            'c'"

    while True:
        choice = raw_input("\n")
        print ""
        if choice == 'c':
            break
        elif choice not in chars:
            print "%s is not a valid character." % choice
            print_dash(True)
            print "Which Character would you like to play as?"
            for i in chars:
                print "- %s" % i
        else:
            print "\nNow playing as %s." % choice
            print_dash(True)

            global character
            global charFile
            global inventoryFile
            global faction

            character = choice
            charFile = "characters/%s.txt" % choice
            inventoryFile = "inventories/%s.inv" % choice
            faction = get_faction()
            set_autotake()
            set_autosneak()

            break


def display_faction_stats():
    while True:
        print "Which faction would you like to view?"
        print_dash()
        print "Wizard         1"
        print "Archer         2"
        print "Warrior        3"
        print "Assassin       4\n"

        selection = raw_input("")
        print_dash(True)

        if selection == '1':
            print "        Wizard       "
            print_dash()
            print "Strength              2/10"
            print "Defense               2/10"
            print "Range                 8/10"
            print "Wisdom                8/10"
            print "Stealth               5/10"
            print "Luck                  5/10"
            print_dash()
            break
        elif selection == '2':
            print "        Archer       "
            print_dash()
            print "Strength              2/10"
            print "Defense               6/10"
            print "Range                 8/10"
            print "Wisdom                6/10"
            print "Stealth               6/10"
            print "Luck                  7/10"
            print_dash()
            break
        elif selection == '3':
            print "        Warrior      "
            print_dash()
            print "Strength              8/10"
            print "Defense               7/10"
            print "Range                 2/10"
            print "Wisdom                3/10"
            print "Stealth               4/10"
            print "Luck                  6/10"
            print_dash()
            break
        elif selection == '4':
            print "       Assassin      "
            print_dash()
            print "Strength              3/10"
            print "Defense               4/10"
            print "Range                 4/10"
            print "Wisdom                3/10"
            print "Stealth               8/10"
            print "Luck                  8/10"
            print_dash()
            break
        else:
            print "That was not a valid selection."


def display_skills():
    print "           Skills           "
    print_dash()
    print "Strength:            \t   %s" % get_skill_level('strength')
    print "Defense:             \t   %s" % get_skill_level('defense')
    print "Accuracy:            \t   %s" % get_skill_level('accuracy')
    print "Wisdom:              \t   %s" % get_skill_level('wisdom')
    print "Stealth:             \t   %s" % get_skill_level('stealth')
    print "Luck:                \t   %s" % get_skill_level('luck')
    print_dash()
    print "Level:               \t   %s" % get_level()
    print ""


def display_info():
    print "Name:               \t   %s\n" % character
    print "Faction:            \t   %s\n" % faction
    print "Character File:     \t   %s\n" % charFile
    print "Inventory File:     \t   %s\n" % inventoryFile
    display_skills()
    print "Total XP:           \t   %s/%s\n" % (get_xp(), level_table[get_level_below() + 1])
    print "Deaths:             \t   %s\n" % get_deaths()
    print "Stage:              \t   %s\n" % get_stage()
    print "Health:             \t   %s/%s\n" % (get_health(), get_max_health())


def create_wizard(filename):
    f = open(filename, "a")
    f.write("Level\n1\n")
    f.write("Stats (in order - SDAWSL)\n")
    f.write("2\n2\n8\n8\n5\n5\n")
    f.write("Total XP\n0\n")
    f.write("Deaths\n0\n")
    f.write("Stage\n1\n")
    f.write("Health\n100\n100\n")
    f.write("Settings - TS\n0\n0\n")
    f.close()


def create_archer(filename):
    f = open(filename, "a")
    f.write("Level\n1\n")
    f.write("Stats (in order - SDAWSL)\n")
    f.write("2\n6\n8\n6\n6\n7\n")
    f.write("Total XP\n0\n")
    f.write("Deaths\n0\n")
    f.write("Stage\n1\n")
    f.write("Health\n100\n100\n")
    f.write("Settings - TS\n0\n0\n")
    f.close()


def create_warrior(filename):
    f = open(filename, "a")
    f.write("Level\n1\n")
    f.write("Stats (in order - SDAWSL)\n")
    f.write("8\n7\n2\n3\n4\n6\n")
    f.write("Total XP\n0\n")
    f.write("Deaths\n0\n")
    f.write("Stage\n1\n")
    f.write("Health\n100\n100\n")
    f.write("Settings - TS\n0\n0\n")
    f.close()


def create_assassin(filename):
    f = open(filename, "a")
    f.write("Level\n1\n")
    f.write("Stats (in order - SDAWSL)\n")
    f.write("3\n4\n4\n3\n8\n8\n")
    f.write("Total XP\n0\n")
    f.write("Deaths\n0\n")
    f.write("Stage\n1\n")
    f.write("Health\n100\n100\n")
    f.write("Settings - TS\n0\n0\n")
    f.close()


def get_level():
    output = 0
    f = open(charFile, "r")
    for i, line in enumerate(f):
        if i == 3:
            output = int(line[:-1])
    f.close()
    return output


def get_skill_level(skill):
    output = -1
    f = open(charFile, "r")
    for i, line in enumerate(f):
        if i == 5 and skill == 'strength':
            output = int(line[:-1])
            break
        elif i == 6 and skill == 'defense':
            output = int(line[:-1])
            break
        elif i == 7 and skill == 'accuracy':
            output = int(line[:-1])
            break
        elif i == 8 and skill == 'wisdom':
            output = int(line[:-1])
            break
        elif i == 9 and skill == 'stealth':
            output = int(line[:-1])
            break
        elif i == 10 and skill == 'luck':
            output = int(line[:-1])
            break
        else:
            output = -1
    f.close()
    return output


def get_xp():
    output = 0
    f = open(charFile, "r")
    for i, line in enumerate(f):
        if i == 12:
            output = int(line[:-1])
    f.close()
    return output


def get_faction():
    output = "none"
    f = open(charFile, "r")
    for i, line in enumerate(f):
        if i == 1:
            output = "%s" % line[:-1]
    f.close()
    return output


def get_deaths():
    output = 0
    f = open(charFile, "r")
    for i, line in enumerate(f):
        if i == 14:
            output = int(line[:-1])
    f.close()
    return output


def get_stage():
    output = 0
    f = open(charFile, "r")
    for i, line in enumerate(f):
        if i == 16:
            output = int(line[:-1])
    f.close()
    return output


def get_health():
    output = 0
    f = open(charFile, "r")
    for i, line in enumerate(f):
        if i == 18:
            output = int(line[:-1])
    f.close()
    return output


def get_max_health():
    output = 0
    f = open(charFile, "r")
    for i, line in enumerate(f):
        if i == 19:
            output = int(line[:-1])
    f.close()
    return output


def add_xp(num):
    lines = open(charFile, 'r').readlines()
    temp = int(lines[12])
    temp += num
    lines[12] = "%s\n" % temp
    out = open(charFile, 'w')
    out.writelines(lines)
    out.close()
    update_level()


def died():
    lines = open(charFile, 'r').readlines()
    temp = int(lines[14])
    temp += 1
    lines[14] = "%s\n" % temp
    out = open(charFile, 'w')
    out.writelines(lines)
    out.close()
    add_xp((level_table[get_level_below()] - get_xp()))
    update_level()
    set_health(get_max_health())

    print "Oh no! You have died!\nYou're XP is reset to the minimum for your level.\n"


def add_stage():
    lines = open(charFile, 'r').readlines()
    temp = int(lines[16])
    temp += 1
    lines[16] = "%s\n" % temp
    out = open(charFile, 'w')
    out.writelines(lines)
    out.close()


def add_health():
    lines = open(charFile, 'r').readlines()
    temp = int(lines[19])
    temp += 25
    lines[19] = "%s\n" % temp
    out = open(charFile, 'w')
    out.writelines(lines)
    out.close()


def set_health(num):
    lines = open(charFile, 'r').readlines()
    temp = num
    lines[18] = "%s\n" % temp
    out = open(charFile, 'w')
    out.writelines(lines)
    out.close()


def toggle_autotake():
    global autotake

    lines = open(charFile, 'r').readlines()
    temp = int(lines[21])
    if temp == 1:
        temp = 0
        autotake = 0
    elif temp == 0:
        temp = 1
        autotake = 1

    lines[21] = "%s\n" % temp
    out = open(charFile, 'w')
    out.writelines(lines)
    out.close()


def get_autotake():
    output = 0
    f = open(charFile, "r")
    for i, line in enumerate(f):
        if i == 21:
            output = int(line[:-1])
    f.close()
    return output


def set_autotake():
    global autotake

    if get_autotake() == 0:
        autotake = 0
    else:
        autotake = 1


def toggle_autosneak():
    global autosneak

    lines = open(charFile, 'r').readlines()
    temp = int(lines[22])
    if temp == 1:
        temp = 0
        autosneak = 0
    elif temp == 0:
        temp = 1
        autosneak = 1

    lines[22] = "%s\n" % temp
    out = open(charFile, 'w')
    out.writelines(lines)
    out.close()


def get_autosneak():
    output = 0
    f = open(charFile, "r")
    for i, line in enumerate(f):
        if i == 22:
            output = int(line[:-1])
    f.close()
    return output


def set_autosneak():
    global autosneak

    if get_autosneak() == 0:
        autosneak = 0
    else:
        autosneak = 1


def play_game():
    if character == 'none':
        select_character()

    global begin
    global stop
    global current
    current = begin

    global youDied

    while True:
        youDied = False
        play_stage = False
        specific = False

        print "What would you like to do?"
        print "Continue on to Labyrinth - Stage %s   \t 'c'" % get_stage()
        print "Enter a specific Labyrinth Stage      \t 'n'"
        print "Enter the general store               \t 's'"
        print "View my info/progression              \t 'i'"
        print "Quit                                  \t 'q'"

        selection = raw_input("\n")
        print ""

        if selection == 'c':
            print "What new foes may await?\n"
            stage_num = get_stage()
            play_stage = True
        elif selection == 'n':
            print "What Stage would you like to enter?"
            stage_num = int(raw_input("\n"))
            print ""
            if stage_num <= get_stage():
                play_stage = True
                specific = True
            else:
                print "You have not reached that stage yet.\n"
        elif selection == 's':
            shop()
        elif selection == 'i':
            display_info()
            print_dash()
        elif selection == 'q':
            break
        else:
            print "Invalid selection.\n"

        if play_stage:
            generate_floor(stage_num)

            print "You have entered the Labyrinth - Stage %s. Good luck...\n" % stage_num

            wisdom = get_skill_level('wisdom')
            chance = randint(0, wisdom * 3)
            direction = "none"

            if chance > stage_num:
                if current[0] > stop[0]:
                    if current[1] > stop[1]:
                        direction = "northwest"
                    elif current[1] < stop[1]:
                        direction = "northeast"
                    else:
                        direction = "north"
                elif current[0] < stop[0]:
                    if current[1] > stop[1]:
                        direction = "southwest"
                    elif current[1] < stop[1]:
                        direction = "southeast"
                    else:
                        direction = "south"
                else:
                    if current[1] > stop[1]:
                        direction = "west"
                    elif current[1] < stop[1]:
                        direction = "east"

                randy = randint(1, 3)
                if randy == 1:
                    print "You feel a force pull you to the %s...\n" % direction
                elif randy == 2:
                    print "There seems to be an inviting presence to the %s...\n" % direction
                elif randy == 3:
                    print "You feel a flow of air moving to the %s...\n" % direction

            print_dash()

            while True:
                if youDied:
                    break
                if current[0] == stop[0] and current[1] == stop[1]:
                    print "You have escaped the Labyrinth!"
                    print_dash(True)
                    if not specific:
                        add_stage()
                    if stage_num == 1:
                        print "You are awarded 50 xp for this feat!\n"
                        add_xp(50)
                    elif stage_num == 2:
                        print "You are awarded 100 xp for this feat!\n"
                        add_xp(100)
                    elif stage_num == 3:
                        print "You are awarded 150 xp for this feat!\n"
                        add_xp(150)
                    elif stage_num == 4:
                        print "You are awarded 250 xp for this feat!\n"
                        add_xp(250)
                    elif stage_num == 5:
                        print "You are awarded 500 xp for this feat!\n"
                        add_xp(500)
                    elif stage_num == 6:
                        print "You are awarded 750 xp for this feat!\n"
                        add_xp(750)
                    elif stage_num == 7:
                        print "You are awarded 1000 xp for this feat!\n"
                        add_xp(1000)
                    elif stage_num == 8:
                        print "You are awarded 1500 xp for this feat!\n"
                        add_xp(1500)
                    elif stage_num == 9:
                        print "You are awarded 2000 xp for this feat!\n"
                        add_xp(2000)
                    elif stage_num == 10:
                        print "You are awarded 2500 xp for this feat!\n"
                        add_xp(2500)
                    elif stage_num == 11:
                        print "You are awarded 3000 xp for this feat!\n"
                        add_xp(3000)
                    elif stage_num == 12:
                        print "You are awarded 3500 xp for this feat!\n"
                        add_xp(3500)
                    elif stage_num == 13:
                        print "You are awarded 4000 xp for this feat!\n"
                        add_xp(4000)
                    elif stage_num == 14:
                        print "You are awarded 4500 xp for this feat!\n"
                        add_xp(4500)
                    elif stage_num == 15:
                        print "You are awarded 5000 xp for this feat!\n"
                        add_xp(5000)
                    elif stage_num == 16:
                        print "You are awarded 6000 xp for this feat!\n"
                        add_xp(6000)
                    elif stage_num == 17:
                        print "You are awarded 7000 xp for this feat!\n"
                        add_xp(7000)
                    elif stage_num == 18:
                        print "You are awarded 8000 xp for this feat!\n"
                        add_xp(8000)
                    elif stage_num == 19:
                        print "You are awarded 9000 xp for this feat!\n"
                        add_xp(9000)
                    elif stage_num == 20:
                        print "You are awarded 10000 xp for this feat!\n"
                        add_xp(10000)
                    elif stage_num == 21:
                        print "You are awarded 12500 xp for this feat!\n"
                        add_xp(12500)
                    elif stage_num == 22:
                        print "You are awarded 15000 xp for this feat!\n"
                        add_xp(15000)
                    elif stage_num == 23:
                        print "You are awarded 17500 xp for this feat!\n"
                        add_xp(17500)
                    elif stage_num == 24:
                        print "You are awarded 20000 xp for this feat!\n"
                        add_xp(20000)
                    elif stage_num == 25:
                        print "You are awarded 22500 xp for this feat!\n"
                        add_xp(22500)
                    elif stage_num == 26:
                        print "You are awarded 25000 xp for this feat!\n"
                        add_xp(25000)
                    elif stage_num == 27:
                        print "You are awarded 30000 xp for this feat!\n"
                        add_xp(30000)
                    elif stage_num == 28:
                        print "You are awarded 35000 xp for this feat!\n"
                        add_xp(35000)
                    elif stage_num == 29:
                        print "You are awarded 40000 xp for this feat!\n"
                        add_xp(40000)
                    elif stage_num == 30:
                        print "You are awarded 50000 xp for this feat!\n"
                        add_xp(50000)
                    else:
                        pass
                    break

                print "What would you like to do?"
                print "To move             'm'"
                print "To heal             'h'"
                print "To quit             'q'"

                selection = raw_input("\n")
                print ""

                if selection == 'm':
                    moved = move()
                    if not moved:
                        pass
                    else:
                        progress(stage_num)
                elif selection == 'h':
                    heal()
                elif selection == 'q':
                    print "Exiting the Labyrinth."
                    break
                else:
                    print "Invalid Selection.\n"


def move():
    global current
    num = 0

    while True:
        print "In which direction would you like to move?"
        print "To move up           'u'"
        print "To move right        'r'"
        print "To move down         'd'"
        print "To move left         'l'"
        print "To cancel            'c'"

        selection = raw_input("\n")
        print ""

        if selection == 'u':
            num = 0
            break
        elif selection == 'r':
            num = 1
            break
        elif selection == 'd':
            num = 2
            break
        elif selection == 'l':
            num = 3
            break
        elif selection == 'c':
            break
        else:
            print "Invalid Selection.\n"

    x = current[0]
    y = current[1]
    length = len(floorMap)

    if num == 0 and not x == 0:  # up
        current[0] = x - 1
        floorMap[x][y] += 1
    elif num == 1 and not y == length - 1:  # right
        current[1] = y + 1
        floorMap[x][y] += 1
    elif num == 2 and not x == length - 1:  # down
        current[0] = x + 1
        floorMap[x][y] += 1
    elif num == 3 and not y == 0:  # left
        current[1] = y - 1
        floorMap[x][y] += 1
    else:
        print "You run into the cave wall...\n"
        return False
    return True


def progress(stage_num):
    found = find_item(stage_num)

    # If item not found
    if not found:
        can_sneak = sneak(stage_num)

        while True:
            if autosneak:
                randy = randint(1, 3)
                if can_sneak:
                    if randy == 1:
                        print "You managed to get by unnoticed...\n"
                    elif randy == 2:
                        print "You crawl beneath the danger in a sewage grate...\n"
                    elif randy == 3:
                        print "You sprint quietly beside the creature and sidle on...\n"
                    print_dash()
                    break
                else:
                    if randy == 1:
                        print "You couldn't sneak by!\n"
                    elif randy == 2:
                        print "The creature sees you!\n"
                    elif randy == 3:
                        print "You were unsuccessful!\n"
                    print_dash()
                    battle(stage_num)
                    print_dash()
                    break
            else:
                print "Would you like to try to sneak by? (y/n)"
                choice = raw_input("\n")
                print ""
                count = 0

                randy = randint(1, 3)
                if choice == 'y':
                    if can_sneak:
                        if randy == 1:
                            print "You managed to get by unnoticed...\n"
                        elif randy == 2:
                            print "You crawl beneath the danger in a sewage grate...\n"
                        elif randy == 3:
                            print "You sprint quietly beside the creature and sidle on...\n"
                        print_dash()
                        break
                    else:
                        if randy == 1:
                            print "You couldn't sneak by!\n"
                        elif randy == 2:
                            print "The creature sees you!\n"
                        elif randy == 3:
                            print "You were unsuccessful!\n"
                        print_dash()
                        battle(stage_num)
                        print_dash()
                        break
                elif choice == 'n':
                    if randy == 1:
                        print "You charge unwittingly into battle!\n"
                    elif randy == 2:
                        print "Prepare for battle!\n"
                    elif randy == 3:
                        print "You're in for it now!\n"
                    print_dash()
                    battle(stage_num)
                    print_dash()
                    break
                else:
                    if count > 3:
                        print "Dude. It's a yes or no question...\n"
                    else:
                        print "Invalid Selection."
                    count += 1


def battle(stage_num):
    global youDied
    max_damage = get_skill_level('strength') * 2
    max_defense = get_skill_level('defense') * 2
    accuracy = get_skill_level('accuracy') * 2
    luck = get_skill_level('luck')

    turn = randint(1, 2)
    fled = False

    while True:
        opponent = random.choice(enemy_table.keys())
        if enemy_table[opponent][0] <= stage_num:
            if enemy_table[opponent][0] > stage_num - 5:
                break

    stats = enemy_table[opponent]

    print "You've entered battle with a %s.\n" % opponent
    health = get_health()
    enemy_health = stats[2]
    enemy_max_damage = stats[3]

    if turn == 2:
        print "You have %s health.             %s has %s health.\n" % (health, opponent, enemy_health)

    while True:
        if health <= 0:
            youDied = True
            died()
            break
        if enemy_health <= 0:
            print "You have killed it!\n"
            add_xp(stats[1])

            print "It appears the enemy dropped an item before disappearing into nothing.\n"
            if randint(0, 1) == 1:
                print "Turns out to be nothing.\n"
            else:
                print "You approach vicariously.\n"
                found = find_item(stage_num)
                if not found:
                    print "Turns out it was nothing...\n"

            level = get_level()
            print "Your current XP is %s of %s to level %s.\n" % (get_xp(), level_table[level + 1], level + 1)
            break
        if turn == 1:
            while True:
                print "You have %s health.             %s has %s health.\n" % (health, opponent, enemy_health)

                print "What would you like to do?\n"
                print "Attack               'a'"
                print "Heal                 'h'"
                print "Flee                 'f'"
                choice = raw_input("\n")
                print ""

                if choice == 'a':
                    print "You attack!\n"
                    hits = randint(1, accuracy * 2)
                    if hits > stats[0]:
                        if randint(0, luck) > randint(0, stage_num * 2):
                            print "You land a critical strike!\n"
                            damage = randint(max_damage / 2, max_damage) * 2
                        else:
                            damage = randint(1, max_damage)
                        print "You deal %s damage!\n" % damage
                        enemy_health -= damage
                    else:
                        print "Your attack misses!\n"

                    select([sys.stdin], [], [], 1)

                    print_dash(True)
                    break
                elif choice == 'h':
                    heal()
                    break
                elif choice == 'f':
                    print "You attempt to flee!\n"
                    if randint(get_skill_level('stealth') / 2, get_skill_level('stealth')) > randint(0, stage_num * 2):
                        print "You get away safely...\n"
                        fled = True
                    else:
                        print "You cannot get away!\n"
                    print_dash()
                    break
                else:
                    print "Invalid Selection.\n"
            turn = 2
        elif fled:
            break
        elif turn == 2:
            print "The %s attacks!\n" % opponent
            if randint(0, max_defense) > randint(0, enemy_max_damage):
                print "You blocked the attack!\n"
            else:
                if randint(1, 5) > 4:
                    print "On no! A critical hit!\n"
                    damage = randint(enemy_max_damage / 2, enemy_max_damage) * 2
                else:
                    damage = randint(1, enemy_max_damage)
                print "The %s deals %s damage!\n" % (opponent, damage)
                health -= damage
                set_health(health)

            select([sys.stdin], [], [], 1)

            print_dash()
            turn = 1


def find_item(stage_num):
    randy = randint(0, get_skill_level('luck'))
    chance = randint(1, 3)

    if chance > 2:
        if randy > 75 and stage_num > 25:
            item, values = random.choice(list(item_table9.items()))
        elif randy > 50 and stage_num > 20:
            item, values = random.choice(list(item_table8.items()))
        elif randy > 45 and stage_num > 16:
            item, values = random.choice(list(item_table7.items()))
        elif randy > 35 and stage_num > 12:
            item, values = random.choice(list(item_table6.items()))
        elif randy > 25 and stage_num > 8:
            item, values = random.choice(list(item_table5.items()))
        elif randy > 15 and stage_num > 4:
            item, values = random.choice(list(item_table4.items()))
        elif randy > 10 and stage_num > 3:
            item, values = random.choice(list(item_table3.items()))
        elif randy > 5 and stage_num > 2:
            item, values = random.choice(list(item_table2.items()))
        elif randy > 3 and stage_num > 1:
            item, values = random.choice(list(item_table1.items()))
        else:
            return False

        num = 1
        if autotake:
            if item == "Gold Piece":
                num = randint(1, stage_num ** 2)
                print "You found %s Gold Pieces. You take the gold.\n" % num
            else:
                print "You found a %s.\nYou take the %s.\n" % (item, item)
        else:
            if item == "Gold Piece":
                num = randint(1, stage_num ** 2)
                print "You found %s Gold Pieces." % num
            else:
                print "You found a %s.\n" % item

            print "Would you like to take it? (y/n)"
            choice = raw_input("\n")
            print ""
            if choice == 'y':
                if num > 1:
                    print "You take the gold.\n"
                else:
                    print "You take the %s.\n" % item
            else:
                print "You left it behind.\n"

        add_item(item, num)

    else:
        return False
    return True


def sneak(stage_num):
    randy = randint(1, stage_num)
    quiet = randint(1, 3)
    blind_luck = randint(0, 10)

    if (get_skill_level('stealth') > randy and quiet >= 2) or blind_luck > 9:
        return True
    else:
        return False


def heal():
    if get_max_health() == get_health():
        print "You are already at full health.\n"
    else:
        while True:
            print "What type of potion would you like to use?"

            print "Potion   - Quantity"

            if has_item('Tiny Potion') >= 0:
                print "Tiny     - %s\t      '0'" % has_item('Tiny Potion')
            if has_item('Little Potion') >= 0:
                print "Little   - %s\t      '1'" % has_item('Little Potion')
            if has_item('Small Potion') >= 0:
                print "Small    - %s\t      '2'" % has_item('Small Potion')
            if has_item('Ragular Potion') >= 0:
                print "Regular  - %s\t      '3'" % has_item('Regular Potion')
            if has_item('Big Potion') >= 0:
                print "Big      - %s\t      '4'" % has_item('Big Potion')
            if has_item('Large Potion') >= 0:
                print "Large    - %s\t      '5'" % has_item('Large Potion')
            if has_item('Huge Potion') >= 0:
                print "Huge     - %s\t      '6'" % has_item('Huge Potion')
            if has_item('Gigantic Potion') >= 0:
                print "Gigantic - %s\t      '7'" % has_item('Gigantic Potion')
            if has_item('Epic Potion') >= 0:
                print "Epic     - %s\t      '8'" % has_item('Epic Potion')

            print "To cancel             'q'"

            potion = int(raw_input("\n"))
            print ""

            if potion == 0:
                num = 10
                remove_item('Tiny Potion')
                break
            elif potion == 1:
                num = 25
                remove_item('Little Potion')
                break
            elif potion == 2:
                num = 50
                remove_item('Small Potion')
                break
            elif potion == 3:
                num = 100
                remove_item('Regular Potion')
                break
            elif potion == 4:
                num = 150
                remove_item('Big Potion')
                break
            elif potion == 5:
                num = 200
                remove_item('Large Potion')
                break
            elif potion == 6:
                num = 300
                remove_item('Huge Potion')
                break
            elif potion == 7:
                num = 500
                remove_item('Gigantic Potion')
                break
            elif potion == 8:
                num = 1000
                remove_item('Epic Potion')
                break
            else:
                print "Invalid Selection."

        if num == 0:
            pass
        else:
            lines = open(charFile, 'r').readlines()
            temp = int(lines[18])
            if temp + num > get_max_health():
                temp = get_max_health()
            else:
                temp += num
            print "You healed %s health points.\n" % num
            lines[18] = "%s\n" % temp
            out = open(charFile, 'w')
            out.writelines(lines)
            out.close()
            print "You now have %s health.\n" % get_health()


def shop():
    print "Welcome to the General Store!"
    print "Here you can find all sorts of goodies and unload some of your pack.\n"
    while True:
        print "What would you like to do?"
        print "To sell                's'"
        print "To buy                 'b'"
        print "To quit                'q'"
        print ""
        print "You have %s gold." % has_item('Gold Piece')

        selection = raw_input("\n")
        print ""

        if selection == 's':
            while True:
                print "What would you like to sell?"
                f = open(inventoryFile, 'r')
                for i, line in enumerate(f):
                    if i > 1:
                        spot = line.index(':')
                        item = line[:spot]
                        quantity = line[spot + 1:-1]
                        cost = get_cost(item)
                        print "%s \t-\t %s      \t%s gold" % (item, quantity, cost)

                print "\nTo quit                         'q'"
                print "You have %s gold." % has_item('Gold Piece')
                item = raw_input("\n")
                print ""

                if item == 'q':
                    break
                elif has_item(item) == 0:
                    print "You do not have any %s's.\n" % item
                elif has_item(item) == 1:
                    remove_item(item)
                    add_item('Gold Piece', get_cost(item))
                    print "You've just sold a %s for %s gold pieces." % (item, get_cost(item))
                    print_dash(True)
                    break
                elif has_item(item) > 1:
                    while True:
                        print "How many would you like to sell? You have %s. 'q' to quit." % has_item(item)
                        num = int(raw_input("\n"))
                        print ""

                        if num > has_item(item):
                            print "You do not have that many...\n"
                        elif num < 1:
                            print "You cannot sell less than 1...\n"
                        elif num <= has_item(item):
                            print "You sell %s %s\'s for %s gold.\n" % (num, item, num*get_cost(item))
                            add_item('Gold Piece', get_cost(item)*num)
                            remove_item(item, num)
                            break
                        elif num == 'q':
                            break
                        else:
                            print "Invalid selection.\n"
                else:
                    print "Invalid selection.\n"

        elif selection == 'b':
            print "We have lots to offer!\n"
            while True:
                print "What would you like to buy?\n"
                offer_items(get_stage())

                print "To quit                  'q'"
                print "You have %s gold." % has_item('Gold Piece')

                item = raw_input("\n")
                print ""

                cost = int(get_cost(item)*1.2)

                if item == 'q':
                    break
                elif not cost > 0:
                    print "That is not an item for sale.\n"
                elif cost > 0:
                    print "You bought a %s for %s gold.\n" % (item, cost)
                    add_item(item, 1)
                    remove_item('Gold Piece', cost)
                else:
                    print "Invalid selection.\n"

        elif selection == 'q':
            break
        else:
            print "Invalid selection.\n"


def offer_items(stage_num):
    print "Tiny Potion \t-\t %s gold" % int(get_cost('Tiny Potion')*1.2)
    if stage_num > 1:
        print "Little Potion \t-\t %s gold" % int(get_cost('Little Potion')*1.2)
    if stage_num > 3:
        print "Small Potion \t-\t %s gold" % int(get_cost('Small Potion')*1.2)
    if stage_num > 6:
        print "Regular Potion \t-\t %s gold" % int(get_cost('Regular Potion')*1.2)
    if stage_num > 8:
        print "Compass \t\t-\t %s gold" % int(get_cost('Compass')*1.2)
    if stage_num > 10:
        print "Big Potion \t-\t %s gold" % int(get_cost('Big Potion')*1.2)
    if stage_num > 14:
        print "Large Potion \t-\t %s gold" % int(get_cost('Large Potion')*1.2)
    if stage_num > 18:
        print "Huge Potion \t-\t %s gold" % int(get_cost('Huge Potion')*1.2)
    if stage_num > 22:
        print "Gigantic Potion \t-\t %s gold" % int(get_cost('Gigantic Potion')*1.2)
    if stage_num > 26:
        print "Epic Potion \t-\t %s gold" % int(get_cost('Epic Potion')*1.2)
    if stage_num >= 30:
        print "Legendary Potion \t-\t %s gold" % int(get_cost('Legendary Potion')*1.2)
    print ""


def level_up():
    global first
    if skillPoints == 1 and first:
        print "\nCongratulations! You have leveled up!\n"
        first = False
    elif skillPoints == 2 and first:
        print "\nCongratulations! You have leveled up twice!\n"
        first = False
    elif skillPoints == 3 and first:
        print "\nCongratulations! You have leveled up thrice!\n"
        first = False
    elif skillPoints == 4 and first:
        print "\nCongratulations! You have leveled up four times!\n"
        first = False
    elif first:
        print "\nCongratulations! You have leveled up A LOT!\n"
        first = False
    display_skills()
    while True:
        print "Skills remaining to level: %s\n\n" % skillPoints

        print "Which level would you like to upgrade?"
        print_dash()
        print "For Strength           's'"
        print "For Defense            'd'"
        print "For Accuracy           'a'"
        print "For Widsom             'w'"
        print "For Stealth            't'"
        print "For Luck               'l'"

        skill = raw_input("\n")
        skill = skill.lower()
        print_dash(True)

        if skill == 's':
            skill = 1
            print "Leveled up Strength!\n"
            break
        elif skill == 'd':
            skill = 2
            print "Leveled up Defense!\n"
            break
        elif skill == 'a':
            skill = 3
            print "Leveled up Accuracy!\n"
            break
        elif skill == 'w':
            skill = 4
            print "Leveled up Wisdom!\n"
            break
        elif skill == 't':
            skill = 5
            print "Leveled up Stealth!\n"
            break
        elif skill == 'l':
            skill = 6
            print "Leveled up Luck!\n"
            break
        else:
            print "Invalid Selection.\n"

    lines = open(charFile, 'r').readlines()
    temp = int(lines[skill + 4])
    temp += 1
    temp = str(temp)
    lines[skill + 4] = "%s\n" % temp
    out = open(charFile, 'w')
    out.writelines(lines)
    out.close()

    add_health()
    set_health(get_max_health())


def update_level():
    global skillPoints
    global first
    first = True
    new_level = get_level()

    for i in level_table:
        if get_xp() >= level_table[i]:
            new_level = i

    skillPoints = new_level - get_level()

    while True:
        if skillPoints == 0:
            break
        else:
            lines = open(charFile, 'r').readlines()
            temp = int(new_level)
            lines[3] = "%s\n" % temp
            out = open(charFile, 'w')
            out.writelines(lines)
            out.close()
            level_up()
            skillPoints -= 1


def get_level_below():
    level_below = 0
    for i in level_table:
        if get_xp() >= level_table[i]:
            level_below = i
    return level_below


def generate_floor(num):
    global floorMap
    global begin
    global stop
    global current

    num = (num / 3) + 2
    floorMap = [[0] * num for _ in xrange(num)]

    startx = randint(0, num - 1)
    starty = randint(0, num - 1)

    while True:
        exitx = randint(0, num - 1)
        exity = randint(0, num - 1)
        if exitx == startx and exity == starty:
            pass
        else:
            break

    begin = [startx, starty]
    current = [startx, starty]
    stop = [exitx, exity]


def print_floor():
    global floorMap
    print ""
    for x in range(len(floorMap)):
        for y in range(len(floorMap)):
            if x == current[0] and y == current[1]:
                print 'O',
            elif x == stop[0] and y == stop[1]:
                print 'X',
            else:
                print '{}'.format(floorMap[x][y]),
        print
    print_dash(True)

    print "Current: %s" % current
    print "Start: %s" % begin
    print "Exit: %s\n" % stop


def has_item(item):
    f = open(inventoryFile, "r")
    quantity = -1
    for i, line in enumerate(f):
        if i > 0:
            spot = line.index(':')
            temp = line[:spot]
            if temp == item:
                quantity = int(line[spot + 1:-1])
    f.close()

    return quantity


def add_item(item, num):
    line_num = 0
    quantity = 0
    if has_item(item) >= 0:
        f = open(inventoryFile, "r")
        for i, line in enumerate(f):
            if item in line:
                spot = line.index(':')
                quantity = int(line[spot + 1:-1])
                line_num = i
        f.close()

        lines = open(inventoryFile, 'r').readlines()
        quantity += num
        lines[line_num] = "%s:%s\n" % (item, quantity)
        out = open(inventoryFile, 'w')
        out.writelines(lines)
        out.close()
    else:
        with open(inventoryFile, 'a') as f:
            f.write("%s:%s\n" % (str(item), str(num)))


def remove_item(item, num=1):
    line_num = 0
    quantity = 0
    if has_item(item) > 0:
        f = open(inventoryFile, "r")
        for i, line in enumerate(f):
            if item in line:
                spot = line.index(':')
                quantity = int(line[spot + 1:-1])
                line_num = i
        f.close()

        lines = open(inventoryFile, 'r').readlines()
        quantity -= num
        lines[line_num] = "%s:%s\n" % (item, quantity)
        out = open(inventoryFile, 'w')
        out.writelines(lines)
        out.close()


def get_cost(item):
    if item in item_table1:
        return item_table1[item][1]
    elif item in item_table2:
        return item_table2[item][1]
    elif item in item_table3:
        return item_table3[item][1]
    elif item in item_table4:
        return item_table4[item][1]
    elif item in item_table5:
        return item_table5[item][1]
    elif item in item_table6:
        return item_table6[item][1]
    elif item in item_table7:
        return item_table7[item][1]
    elif item in item_table8:
        return item_table8[item][1]
    elif item in item_table9:
        return item_table9[item][1]
    else:
        return False


def main():
    if not os.path.exists("characters"):
        os.makedirs("characters")
    if not os.path.exists("inventories"):
        os.makedirs("inventories")

    print "Welcome to Cam's Prototype game!\n"
    start()


# If this is run as a script.
if __name__ == '__main__':
    main()
