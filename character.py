import os
import IO

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
            set_autotake()
            set_autosneak()

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