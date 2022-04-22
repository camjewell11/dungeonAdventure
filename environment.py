import math, os
import character, config, IO
from random import randint

skillPoints = 0
floorMap = []
begin = []
stop = []
current = []
youDied = False

autotake = 0
autosneak = 0

def setupDirectories():
    workingDir = ""
    if not os.path.exists(workingDir + "characters"):
        os.makedirs(workingDir + "characters")
    if not os.path.exists(workingDir + "inventories"):
        os.makedirs(workingDir + "inventories")

def toggle_autotake():
    global autotake
    lines = open(IO.charFile, 'r').readlines()
    temp = int(lines[21])
    if temp == 1:
        temp = 0
        autotake = 0
    elif temp == 0:
        temp = 1
        autotake = 1

    lines[21] = "%s\n" % temp
    out = open(IO.charFile, 'w')
    out.writelines(lines)
    out.close()

def get_autotake():
    output = 0
    f = open(IO.charFile, "r")
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
    lines = open(IO.charFile, 'r').readlines()
    temp = int(lines[22])
    if temp == 1:
        temp = 0
        autosneak = 0
    elif temp == 0:
        temp = 1
        autosneak = 1

    lines[22] = "%s\n" % temp
    out = open(IO.charFile, 'w')
    out.writelines(lines)
    out.close()

def get_autosneak():
    output = 0
    f = open(IO.charFile, "r")
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

def generate_floor(num):
    global floorMap
    num = math.floor((num / 3) + 2)
    floorMap = [[0] * num for _ in range(num)]

    startX = randint(0, num - 1)
    startY = randint(0, num - 1)

    while True:
        exitX = randint(0, num - 1)
        exitY = randint(0, num - 1)
        if exitX != startX or exitY != startY:
            break

    global begin
    global current
    global stop
    begin = [startX, startY]
    current = [startX, startY]
    stop = [exitX, exitY]

def print_floor():
    print ("")
    for x in range(len(floorMap)):
        row = ""
        for y in range(len(floorMap)):
            if x == current[0] and y == current[1]:
                row += 'O '
            elif x == stop[0] and y == stop[1]:
                row += 'X '
            else:
                row += str(floorMap[x][y]) + " "
        print (row)
    IO.print_dash(True)

    print ("Current: %s" % current)
    print ("Start: %s" % begin)
    print ("Exit: %s\n" % stop)

def settings():
    if IO.playerCharacter == 'none':
        character.select_character()

    IO.printSettings()
    selection = IO.getSelectionFromUser(['d','t','s','q'], "\n")

    if selection == 'd':
        deleteCharacter()
    elif selection == 't':
        promptToggleAutotake()
    elif selection == 's':
        promptToggleAutosneak()
    elif selection == 'q':
        return

def deleteCharacter():
    chars = os.listdir("characters")
    chars.remove('.gitkeep')
    print ("Which Character would you like to delete?")
    spot = 0
    for i in chars:
        chars[spot] = i[:-4]
        print ("- %s" % chars[spot])
        spot += 1
    print ("\nTo cancel                 'c'")

    chars.append('c')
    choice = IO.getSelectionFromUser(chars, "\n", "Not a valid character.")
    if choice == 'c':
        return
    else:
        os.remove("characters/%s.txt" % choice)
        os.remove("inventories/%s.inv" % choice)
        print ("Removed %s.\n" % choice)
        IO.print_dash()

def promptToggleAutotake():
    print ("Would you like to change autotake? Currently set to %s. (y/n)" % get_autotake())
    choice = input("\n")
    print ("")
    if choice == 'y':
        toggle_autotake()
        print ("Autotake is now %s.\n" % get_autotake())
    elif choice == 'n':
        print ("Returning to menu.\n")
    else:
        print (config.invalidResponse)

def promptToggleAutosneak():
    print ("Would you like to change autosneak? Currently set to %s. (y/n)" % get_autosneak())
    choice = input("\n")
    print ("")
    if choice == 'y':
        toggle_autosneak()
        print ("Autosneak is now %s.\n" % get_autosneak())
    elif choice == 'n':
        print ("Returning to menu.\n")
    else:
        print (config.invalidResponse)

def writeLevelUp(skill):
    lines = open(IO.charFile, 'r').readlines()
    temp = int(lines[skill + 4])
    temp += 1
    temp = str(temp)
    lines[skill + 4] = "%s\n" % temp
    out = open(IO.charFile, 'w')
    out.writelines(lines)
    out.close()