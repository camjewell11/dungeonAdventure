import random
import character, config, environment, game, inventoryManagement

playerCharacter = "none"
faction = "none"
charFile = "none"
inventoryFile = "none"
first = True

# delimiter for printed instruction
def print_dash(skip=False):
    if skip:
        print ("------------------------------\n")
    else:
        print ("------------------------------")

# prints main menu
def printMainMenu():
    print (config.promptAction)
    print_dash()
    print ("Create Character:        1")
    print ("Select Character:        2")
    print ("Play Game                3")
    print ("Settings:                4")
    print ("Exit:                    5")

# prints secret menu used to validate individual functions without having to play the game
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

# print settings menu
def printSettings():
    print ("         Settings            ")
    print_dash()
    print ("To Delete Character       'd'")
    print ("To toggle autotake items  't'")
    print ("To toggle autosneak       's'")
    print ("To quit                   'q'")

# printed when creating character
def printSelectClass():
    print ("\nSelect Faction")
    print_dash()
    print ("Wizard         1")
    print ("Archer         2")
    print ("Warrior        3")
    print ("Assassin       4")
    print_dash()
    print ("View Stats     5\n")

# printed once character selected and play begins
def printPlayGameOptions():
    print (config.promptAction)
    print_dash()
    print ("Continue on to Labyrinth - Stage %s   \t 'c'" % character.get_stage())
    print ("Enter a specific Labyrinth Stage      \t 'n'")
    print ("Enter the general store               \t 's'")
    print ("View my info/progression              \t 'i'")
    print ("Quit                                  \t 'q'")

# printed when exploring a floor; directional options
def printMoveDirection():
    print ("In which direction would you like to move?")
    print_dash()
    print ("To move up           'u'")
    print ("To move right        'r'")
    print ("To move down         'd'")
    print ("To move left         'l'")
    print ("To cancel            'c'")

# prints options for shop interaction
def printShopPrompt():
    print ("You have %s gold." % inventoryManagement.has_item(config.currencyName))
    print ("")
    print (config.promptAction)
    print_dash()
    print ("To sell                's'")
    print ("To buy                 'b'")
    print ("To quit                'q'")

# prints available items in shop
def printShopOffers():
    print ("You have %s gold." % inventoryManagement.has_item(config.currencyName))
    print ("")
    print ("What would you like to buy?\n")
    print_dash()
    items = inventoryManagement.offer_items(character.get_stage())
    print ("To quit                  'q'")
    return items

# prints items in inventory to be sold
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

# prints starting attributes for each of the available factions
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
            print_dash(True)
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
            print_dash(True)
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
            print_dash(True)
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
            print_dash(True)
            break
        else:
            print ("That was not a valid selection.")

# prints the selected character's stats
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

# prints environment variables for selected character
def display_info():
    print ("Name:               \t   %s" % playerCharacter)
    print ("Faction:            \t   %s" % faction)
    print ("Character File:     \t   %s" % charFile)
    print ("Inventory File:     \t   %s" % inventoryFile)
    print ("")
    display_skills()
    print ("Total XP:           \t   %s/%s" % (character.get_xp(), config.level_table[character.get_level_below() + 1]))
    print ("Deaths:             \t   %s"    %  character.get_deaths())
    print ("Stage:              \t   %s"    %  character.get_stage())
    print ("Health:             \t   %s/%s" % (character.get_health(), character.get_max_health()))
    print_dash(True)

# prints in level options
def printLevelExplore():
    print (config.promptAction)
    print_dash()
    print ("To move             'm'")
    print ("To heal             'h'")
    print ("To quit             'q'")

# prints escape from labyrinth floor
def printEscape():
    print ("You have escaped the Labyrinth!")
    print_dash(True)

# prints prompt for user to select skill to upgrade
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

# prints directional message towards exit in floor
def printMapHint(stage_num):
    wisdom = character.get_skill_level('wisdom')
    chance = random.randint(0, wisdom * 3)

    if chance > stage_num:
        direction = getDirectionFromCurrentPosition()

        randy = random.randint(0, 2)
        print (config.directionalMessages[randy] % direction)

# helper to create hint based on current position
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

# prints results of sneak attempt
def printSneak(stage_num):
    randy = random.randint(0, 2)
    if game.sneak(stage_num):
        print (config.sneakOptions[randy])
        return True
    else:
        print (config.failedSneakOptions[randy])
        return False

# prompts user for an integer using provided prompt
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

# prompts user for a selection from the provided option with the given prompt
def getSelectionFromUser(options, prompt="", error=""):
    options.append('q')
    options.append('c')
    while True:
        selection = input(prompt).lower()
        if selection not in [x.lower() for x in options]:
            if error != "":
                print (error)
            else:
                print (config.invalidResponse)
        else:
            print ("")
            return selection