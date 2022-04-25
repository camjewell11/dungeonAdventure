import random
import character, config, environment, game, inventoryManagement

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

def printMainMenu():
    print (config.promptAction)
    print_dash()
    print ("Create Character:        1")
    print ("Select Character:        2")
    print ("Play Game                3")
    print ("Settings:                4")
    print ("Exit:                    5")

def printDebugMenu():
    print ("Secret Debug Menu")
    print_dash()
    print ("For active info         'i'")
    print ("To level up a skill     'u'")
    print ("To add XP               'x'")
    print ("To view enemy tables    'e'")
    print ("To kill player          'k'")
    print ("To create floorMap      'm'")
    print ("To return               'q'")

def printSettings():
    print ("         Settings            ")
    print_dash()
    print ("To Delete Character       'd'")
    print ("To toggle autotake items  't'")
    print ("To toggle autosneak       's'")
    print ("To quit                   'q'")

def printSelectClass():
    print ("\nSelect Faction")
    print_dash()
    print ("Wizard         1")
    print ("Archer         2")
    print ("Warrior        3")
    print ("Assassin       4")
    print_dash()
    print ("View Stats     5\n")

def printPlayGameOptions():
    print (config.promptAction)
    print ("Continue on to Labyrinth - Stage %s   \t 'c'" % character.get_stage())
    print ("Enter a specific Labyrinth Stage      \t 'n'")
    print ("Enter the general store               \t 's'")
    print ("View my info/progression              \t 'i'")
    print ("Quit                                  \t 'q'")

def printMoveDirection():
    print ("In which direction would you like to move?")
    print ("To move up           'u'")
    print ("To move right        'r'")
    print ("To move down         'd'")
    print ("To move left         'l'")
    print ("To cancel            'c'")

def printShopPrompt():
    print (config.promptAction)
    print ("To sell                's'")
    print ("To buy                 'b'")
    print ("To quit                'q'")
    print ("")
    print ("You have %s gold." % character.has_item(config.currencyName))

def printShopOffers():
    print ("What would you like to buy?\n")
    inventoryManagement.offer_items(character.get_stage())
    print ("To quit                  'q'")
    print ("You have %s gold." % inventoryManagement.has_item(config.currencyName))

def printInventory():
    items = []
    f = open(inventoryFile, 'r')
    for i, line in enumerate(f):
        if i > 1:
            spot = line.index(':')
            item = line[:spot]
            quantity = line[spot + 1:-1]
            cost = inventoryManagement.get_cost(item)
            print ("%s \t-\t %s      \t%s gold" % (item, quantity, cost))
            items.append(item)
    return items

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

def printLevelExplore():
    print (config.promptAction)
    print ("To move             'm'")
    print ("To heal             'h'")
    print ("To quit             'q'")

def printEscape():
    print ("You have escaped the Labyrinth!")
    print_dash(True)

def printSkillUpgrade():
    print ("Skills remaining to level: %s\n\n" % environment.skillPoints)
    print ("Which level would you like to upgrade?")
    print_dash()
    print ("For Strength           's'")
    print ("For Defense            'd'")
    print ("For Accuracy           'a'")
    print ("For Wisdom             'w'")
    print ("For Stealth            't'")
    print ("For Luck               'l'")

def printMapHint(stage_num):
    wisdom = character.get_skill_level('wisdom')
    chance = random.randint(0, wisdom * 3)

    if chance > stage_num:
        direction = getDirectionFromCurrentPosition()

        randy = random.randint(0, 2)
        print (config.directionalMessages[randy] % direction)

def getDirectionFromCurrentPosition():
    direction = "none"
    if environment.current[0] > environment.stop[0]:
        if environment.current[1] > environment.stop[1]:
            direction = "northwest"
        elif environment.current[1] < environment.stop[1]:
            direction = "northeast"
        else:
            direction = "north"
    elif environment.current[0] < environment.stop[0]:
        if environment.current[1] > environment.stop[1]:
            direction = "southwest"
        elif environment.current[1] < environment.stop[1]:
            direction = "southeast"
        else:
            direction = "south"
    else:
        if environment.current[1] > environment.stop[1]:
            direction = "west"
        elif environment.current[1] < environment.stop[1]:
            direction = "east"
    return direction

def printSneak(stage_num):
    randy = random.randint(0, 2)
    if game.sneak(stage_num):
        print (config.sneakOptions[randy])
        return True
    else:
        print (config.failedSneakOptions[randy])
        return False

def getIntFromUser(prompt=""):
    while True:
        try:
            value = input(prompt)
            if value == 'q':
                break
            value = int(value)
        except ValueError:
            print ("That wasn't a number!")
        else:
            break
    print ("")
    return value

def getSelectionFromUser(options, prompt="", error=""):
    options.append('q')
    options.append('c')
    while True:
        selection = input(prompt).lower()
        if selection not in options:
            if error != "":
                print (error)
            else:
                print (config.invalidResponse)
        else:
            print ("")
            return selection