import os
import character, config, environment, inventoryManagement, IO

def create_character():
    print ("New Character Creation")
    IO.print_dash()

    name = input("Enter your name: ")
    IO.print_dash()
    filename = "characters/" + name + ".txt"

    if os.path.isfile(filename):
        print ("Character already exists.")
        IO.print_dash(True)
    else:
        f = open(filename, "w")
        f.write(name + "\n")
        IO.printSelectClass()

        selection = IO.getSelectionFromUser(['Wizard','Archer','Warrior','Assassin'], error="That was not a valid selection.")
        IO.print_dash(True)
        if selection == '5':
            IO.display_faction_stats()
        else:
            if selection == '1':
                faction = "Wizard"
            elif selection == '2':
                faction = "Archer"
            elif selection == '3':
                faction = "Warrior"
            elif selection == '4':
                faction = "Assassin"
            f.write("%s\n" % faction)
            f.close()
            createClass(filename, faction)
            print ("Created new character, %s!" % name)
            IO.print_dash(True)

    playerCharacter = name
    IO.charFile = filename
    inventoryFile = "inventories/" + playerCharacter + ".inv"

    f = open(inventoryFile, "w")
    f.write("Inventory\n")
    f.write("Gold Pieces:0\n")
    f.close()

def select_character():
    chars = os.listdir("characters")
    print ("Which Character would you like to play as?")
    spot = 0
    chars.remove(".gitkeep")
    for i in chars:
        chars[spot] = i[:-4]
        print ("- %s" % chars[spot])
        spot += 1
    print ("\nTo cancel            'c'")

    while True:
        choice = input("\n")
        print ("")
        if choice == 'c':
            break
        elif choice not in chars:
            print ("%s is not a valid character." % choice)
            IO.print_dash(True)
            print ("Which Character would you like to play as?")
            for i in chars:
                print ("- %s" % i)
        else:
            print ("\nNow playing as %s." % choice)
            IO.print_dash(True)

            IO.playerCharacter = choice
            IO.charFile = "characters/%s.txt" % choice
            IO.inventoryFile = "inventories/%s.inv" % choice
            IO.faction = get_faction()
            environment.set_autotake()
            environment.set_autosneak()

            break

def createClass(filename, faction):
    f = open(filename, "a")
    f.write("Level\n1\n")
    f.write("Stats (in order - SDAWSL)\n")

    if faction == "Wizard":
        f.write("2\n2\n8\n8\n5\n5\n")
    elif faction == "Archer":
        f.write("2\n6\n8\n6\n6\n7\n")
    elif faction == "Warrior":
        f.write("8\n7\n2\n3\n4\n6\n")
    elif faction == "Assassin":
        f.write("3\n4\n4\n3\n8\n8\n")

    f.write("Total XP\n0\n")
    f.write("Deaths\n0\n")
    f.write("Stage\n1\n")
    f.write("Health\n100\n100\n")
    f.write("Settings - TS\n0\n0\n")
    f.close()

def get_level():
    output = 0
    f = open(IO.charFile, "r")
    for i, line in enumerate(f):
        if i == 3:
            output = int(line[:-1])
    f.close()
    return output

def get_skill_level(skill):
    output = -1
    f = open(IO.charFile, "r")
    for i, line in enumerate(f):
        if  i ==  5 and skill == 'strength' or \
            i ==  6 and skill == 'defense'  or \
            i ==  7 and skill == 'accuracy' or \
            i ==  8 and skill == 'wisdom'   or \
            i ==  9 and skill == 'stealth'  or \
            i == 10 and skill == 'luck':
                output = int(line[:-1])
                break
        else:
            output = -1
    f.close()
    return output

def get_xp():
    output = 0
    f = open(IO.charFile, "r")
    for i, line in enumerate(f):
        if i == 12:
            output = int(line[:-1])
    f.close()
    return output

def get_faction():
    output = "none"
    f = open(IO.charFile, "r")
    for i, line in enumerate(f):
        if i == 1:
            output = "%s" % line[:-1]
    f.close()
    return output

def get_deaths():
    output = 0
    f = open(IO.charFile, "r")
    for i, line in enumerate(f):
        if i == 14:
            output = int(line[:-1])
    f.close()
    return output

def get_stage():
    output = 0
    f = open(IO.charFile, "r")
    for i, line in enumerate(f):
        if i == 16:
            output = int(line[:-1])
    f.close()
    return output

def get_health():
    output = 0
    f = open(IO.charFile, "r")
    for i, line in enumerate(f):
        if i == 18:
            output = int(line[:-1])
    f.close()
    return output

def get_max_health():
    output = 0
    f = open(IO.charFile, "r")
    for i, line in enumerate(f):
        if i == 19:
            output = int(line[:-1])
    f.close()
    return output

def add_xp(num):
    lines = open(IO.charFile, 'r').readlines()
    temp = int(lines[12])
    temp += num
    lines[12] = "%s\n" % temp
    out = open(IO.charFile, 'w')
    out.writelines(lines)
    out.close()
    update_level()

def died():
    lines = open(IO.charFile, 'r').readlines()
    temp = int(lines[14])
    temp += 1
    lines[14] = "%s\n" % temp
    out = open(IO.charFile, 'w')
    out.writelines(lines)
    out.close()
    add_xp((config.level_table[get_level_below()] - character.get_xp()))
    update_level()
    set_health(character.get_max_health())

    print ("Oh no! You have died!\nYou're XP is reset to the minimum for your level.\n")

def add_stage():
    lines = open(IO.charFile, 'r').readlines()
    temp = int(lines[16])
    temp += 1
    lines[16] = "%s\n" % temp
    out = open(IO.charFile, 'w')
    out.writelines(lines)
    out.close()

def add_health():
    lines = open(IO.charFile, 'r').readlines()
    temp = int(lines[19])
    temp += 25
    lines[19] = "%s\n" % temp
    out = open(IO.charFile, 'w')
    out.writelines(lines)
    out.close()

def set_health(num):
    lines = open(IO.charFile, 'r').readlines()
    temp = num
    lines[18] = "%s\n" % temp
    out = open(IO.charFile, 'w')
    out.writelines(lines)
    out.close()

def level_up():
    if environment.skillPoints == 1 and IO.first:
        print ("\nCongratulations! You have leveled up!\n")
        IO.first = False
    elif environment.skillPoints == 2 and IO.first:
        print ("\nCongratulations! You have leveled up twice!\n")
        IO.first = False
    elif environment.skillPoints == 3 and IO.first:
        print ("\nCongratulations! You have leveled up thrice!\n")
        IO.first = False
    elif environment.skillPoints == 4 and IO.first:
        print ("\nCongratulations! You have leveled up four times!\n")
        IO.first = False
    elif IO.first:
        print ("\nCongratulations! You have leveled up A LOT!\n")
        IO.first = False
    IO.display_skills()
    IO.printSkillUpgrade()

    skill = IO.getSelectionFromUser(['s','d','a','w','t','l']).lower()
    IO.print_dash(True)

    if skill == 's':
        skill = 1
        print ("Leveled up Strength!\n")
    elif skill == 'd':
        skill = 2
        print ("Leveled up Defense!\n")
    elif skill == 'a':
        skill = 3
        print ("Leveled up Accuracy!\n")
    elif skill == 'w':
        skill = 4
        print ("Leveled up Wisdom!\n")
    elif skill == 't':
        skill = 5
        print ("Leveled up Stealth!\n")
    elif skill == 'l':
        skill = 6
        print ("Leveled up Luck!\n")

    environment.writeLevelUp(skill)
    add_health()
    set_health(get_max_health())

def update_level():
    IO.first = True
    new_level = get_level()

    for i in config.level_table:
        if get_xp() >= config.level_table[i]:
            new_level = i

    environment.skillPoints = new_level - get_level()

    while True:
        if environment.skillPoints == 0:
            break
        else:
            lines = open(IO.charFile, 'r').readlines()
            temp = int(new_level)
            lines[3] = "%s\n" % temp
            out = open(IO.charFile, 'w')
            out.writelines(lines)
            out.close()
            level_up()
            environment.skillPoints -= 1

def get_level_below():
    level_below = 0
    for i in config.level_table:
        if get_xp() >= config.level_table[i]:
            level_below = i
    return level_below

def heal():
    if get_max_health() == get_health():
        print ("You are already at full health.\n")
    else:
        print ("What type of potion would you like to use?")
        print ("Potion   - Quantity")

        for i in range(8):
            if inventoryManagement.has_item(config.potionSizes[i]) >= 0:
                print ("%s - %s\t      '0'" % config.potionSizes[i], inventoryManagement.has_item(config.potionSizes[i]))
        print ("To cancel             'q'")

        num = buyPotion()

        if num != 0:
            lines = open(IO.charFile, 'r').readlines()
            temp = int(lines[18])
            if temp + num > get_max_health():
                temp = get_max_health()
            else:
                temp += num
            print ("You healed %s health points.\n" % num)
            lines[18] = "%s\n" % temp
            out = open(IO.charFile, 'w')
            out.writelines(lines)
            out.close()
            print ("You now have %s health.\n" % get_health())

def buyPotion():
    potion = IO.getIntFromUser()
    if potion == 0:
        num = 10
        inventoryManagement.remove_item(config.potionSizes[0])
    elif potion == 1:
        num = 25
        inventoryManagement.remove_item(config.potionSizes[1])
    elif potion == 2:
        num = 50
        inventoryManagement.remove_item(config.potionSizes[2])
    elif potion == 3:
        num = 100
        inventoryManagement.remove_item(config.potionSizes[3])
    elif potion == 4:
        num = 150
        inventoryManagement.remove_item(config.potionSizes[4])
    elif potion == 5:
        num = 200
        inventoryManagement.remove_item(config.potionSizes[5])
    elif potion == 6:
        num = 300
        inventoryManagement.remove_item(config.potionSizes[6])
    elif potion == 7:
        num = 500
        inventoryManagement.remove_item(config.potionSizes[7])
    elif potion == 8:
        num = 1000
        inventoryManagement.remove_item(config.potionSizes[8])
    return num