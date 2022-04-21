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
    print ("Strength:            \t   %s" % get_skill_level('strength'))
    print ("Defense:             \t   %s" % get_skill_level('defense'))
    print ("Accuracy:            \t   %s" % get_skill_level('accuracy'))
    print ("Wisdom:              \t   %s" % get_skill_level('wisdom'))
    print ("Stealth:             \t   %s" % get_skill_level('stealth'))
    print ("Luck:                \t   %s" % get_skill_level('luck'))
    print_dash()
    print ("Level:               \t   %s" % get_level())
    print ("")

def display_info():
    print ("Name:               \t   %s\n" % playerCharacter)
    print ("Faction:            \t   %s\n" % faction)
    print ("Character File:     \t   %s\n" % charFile)
    print ("Inventory File:     \t   %s\n" % inventoryFile)
    display_skills()
    print ("Total XP:           \t   %s/%s\n" % (get_xp(), level_table[get_level_below() + 1]))
    print ("Deaths:             \t   %s\n" % get_deaths())
    print ("Stage:              \t   %s\n" % get_stage())
    print ("Health:             \t   %s/%s\n" % (get_health(), get_max_health()))