import os
import config, environment, IO

def create_character():
    print ("New Character Creation")
    IO.print_dash()

    while True:
        name = input("Enter your name: ")
        IO.print_dash()
        filename = "characters/" + name + ".txt"
        global playerCharacter
        global charFile
        global inventoryFile
        global faction

        if os.path.isfile(filename):
            print ("Character already exists.")
            IO.print_dash(True)
        else:
            f = open(filename, "w")
            f.write(name + "\n")
            while True:
                print ("\nSelect Faction")
                IO.print_dash()
                print ("Wizard         1")
                print ("Archer         2")
                print ("Warrior        3")
                print ("Assassin       4")
                IO.print_dash()
                print ("View Stats     5\n")

                selection = input("")
                IO.print_dash(True)
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
                    IO.display_faction_stats()
                else:
                    print ("That was not a valid selection.")
            print ("Created new character, %s!" % name)
            IO.print_dash(True)

        playerCharacter = name
        charFile = filename
        inventoryFile = "inventories/" + playerCharacter + ".inv"

        f = open(inventoryFile, "w")
        f.write("Inventory\n")
        f.write("Gold Pieces:0\n")
        f.close()

        break

def select_character():
    chars = os.listdir("characters")
    print ("Which Character would you like to play as?")
    spot = 0
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

            global playerCharacter
            global charFile
            global inventoryFile
            global faction

            playerCharacter = choice
            charFile = "characters/%s.txt" % choice
            inventoryFile = "inventories/%s.inv" % choice
            faction = get_faction()
            environment.set_autotake()
            environment.set_autosneak()

            break

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
    add_xp((config.level_table[get_level_below()] - IO.playerCharacter.get_xp()))
    update_level()
    set_health(IO.playerCharacter.get_max_health())

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
    global first
    if skillPoints == 1 and first:
        print ("\nCongratulations! You have leveled up!\n")
        first = False
    elif skillPoints == 2 and first:
        print ("\nCongratulations! You have leveled up twice!\n")
        first = False
    elif skillPoints == 3 and first:
        print ("\nCongratulations! You have leveled up thrice!\n")
        first = False
    elif skillPoints == 4 and first:
        print ("\nCongratulations! You have leveled up four times!\n")
        first = False
    elif first:
        print ("\nCongratulations! You have leveled up A LOT!\n")
        first = False
    IO.display_skills()
    while True:
        print ("Skills remaining to level: %s\n\n" % skillPoints)

        print ("Which level would you like to upgrade?")
        IO.print_dash()
        print ("For Strength           's'")
        print ("For Defense            'd'")
        print ("For Accuracy           'a'")
        print ("For Wisdom             'w'")
        print ("For Stealth            't'")
        print ("For Luck               'l'")

        skill = input("\n")
        skill = skill.lower()
        IO.print_dash(True)

        if skill == 's':
            skill = 1
            print ("Leveled up Strength!\n")
            break
        elif skill == 'd':
            skill = 2
            print ("Leveled up Defense!\n")
            break
        elif skill == 'a':
            skill = 3
            print ("Leveled up Accuracy!\n")
            break
        elif skill == 'w':
            skill = 4
            print ("Leveled up Wisdom!\n")
            break
        elif skill == 't':
            skill = 5
            print ("Leveled up Stealth!\n")
            break
        elif skill == 'l':
            skill = 6
            print ("Leveled up Luck!\n")
            break
        else:
            print ("Invalid Selection.\n")

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

    for i in config.level_table:
        if get_xp() >= config.level_table[i]:
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
    for i in config.level_table:
        if get_xp() >= config.level_table[i]:
            level_below = i
    return level_below

def heal():
    if get_max_health() == get_health():
        print ("You are already at full health.\n")
    else:
        while True:
            print ("What type of potion would you like to use?")

            print ("Potion   - Quantity")

            if has_item('Tiny Potion') >= 0:
                print ("Tiny     - %s\t      '0'" % has_item('Tiny Potion'))
            if has_item('Little Potion') >= 0:
                print ("Little   - %s\t      '1'" % has_item('Little Potion'))
            if has_item('Small Potion') >= 0:
                print ("Small    - %s\t      '2'" % has_item('Small Potion'))
            if has_item('Regular Potion') >= 0:
                print ("Regular  - %s\t      '3'" % has_item('Regular Potion'))
            if has_item('Big Potion') >= 0:
                print ("Big      - %s\t      '4'" % has_item('Big Potion'))
            if has_item('Large Potion') >= 0:
                print ("Large    - %s\t      '5'" % has_item('Large Potion'))
            if has_item('Huge Potion') >= 0:
                print ("Huge     - %s\t      '6'" % has_item('Huge Potion'))
            if has_item('Gigantic Potion') >= 0:
                print ("Gigantic - %s\t      '7'" % has_item('Gigantic Potion'))
            if has_item('Epic Potion') >= 0:
                print ("Epic     - %s\t      '8'" % has_item('Epic Potion'))

            print ("To cancel             'q'")

            potion = int(input("\n"))
            print ("")

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
                print ("Invalid Selection.")

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