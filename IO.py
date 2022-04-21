import character, config

playerCharacter = "none"
faction = "none"
charFile = "none"
inventoryFile = "none"
first = True

def print_dash(skip=False):
    if skip:
        print ("------------------------------\n")
    else:
        print ("------------------------------")

def display_faction_stats():
    while True:
        print ("Which faction would you like to view?")
        print_dash()
        print ("Wizard         1")
        print ("Archer         2")
        print ("Warrior        3")
        print ("Assassin       4\n")

        selection = input("")
        print_dash(True)

        if selection == '1':
            print ("        Wizard       ")
            print_dash()
            print ("Strength              2/10")
            print ("Defense               2/10")
            print ("Range                 8/10")
            print ("Wisdom                8/10")
            print ("Stealth               5/10")
            print ("Luck                  5/10")
            print_dash()
            break
        elif selection == '2':
            print ("        Archer       ")
            print_dash()
            print ("Strength              2/10")
            print ("Defense               6/10")
            print ("Range                 8/10")
            print ("Wisdom                6/10")
            print ("Stealth               6/10")
            print ("Luck                  7/10")
            print_dash()
            break
        elif selection == '3':
            print ("        Warrior      ")
            print_dash()
            print ("Strength              8/10")
            print ("Defense               7/10")
            print ("Range                 2/10")
            print ("Wisdom                3/10")
            print ("Stealth               4/10")
            print ("Luck                  6/10")
            print_dash()
            break
        elif selection == '4':
            print ("       Assassin      ")
            print_dash()
            print ("Strength              3/10")
            print ("Defense               4/10")
            print ("Range                 4/10")
            print ("Wisdom                3/10")
            print ("Stealth               8/10")
            print ("Luck                  8/10")
            print_dash()
            break
        else:
            print ("That was not a valid selection.")

def display_skills():
    print ("           Skills           ")
    print_dash()
    print ("Strength:            \t   %s" % character.get_skill_level('strength'))
    print ("Defense:             \t   %s" % character.get_skill_level('defense'))
    print ("Accuracy:            \t   %s" % character.get_skill_level('accuracy'))
    print ("Wisdom:              \t   %s" % character.get_skill_level('wisdom'))
    print ("Stealth:             \t   %s" % character.get_skill_level('stealth'))
    print ("Luck:                \t   %s" % character.get_skill_level('luck'))
    print_dash()
    print ("Level:               \t   %s" % character.get_level())
    print ("")

def display_info():
    print ("Name:               \t   %s" % playerCharacter)
    print ("Faction:            \t   %s" % faction)
    print ("Character File:     \t   %s" % charFile)
    print ("Inventory File:     \t   %s" % inventoryFile)
    display_skills()
    print ("Total XP:           \t   %s/%s" % (character.get_xp(), config.level_table[character.get_level_below() + 1]))
    print ("Deaths:             \t   %s" % character.get_deaths())
    print ("Stage:              \t   %s" % character.get_stage())
    print ("Health:             \t   %s/%s\n" % (character.get_health(), character.get_max_health()))