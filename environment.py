import math, os
import character, config, IO
from random import randint

skillPoints = 0
floorMap = []
begin = []
stop = []
current = []
youDied = False

autoTake = 0
autoSneak = 0

# create character and inventory directories if they don't exist
def setupDirectories():
    workingDir = ""
    if not os.path.exists(workingDir + "characters"):
        os.makedirs(workingDir + "characters")
    if not os.path.exists(workingDir + "inventories"):
        os.makedirs(workingDir + "inventories")

# swaps current value of autoTake for selected character
def toggle_autoTake():
    global autoTake
    lines = open(IO.charFile, 'r').readlines()
    temp = int(lines[21])
    if temp == 1:
        temp = 0
        autoTake = 0
    elif temp == 0:
        temp = 1
        autoTake = 1

    lines[21] = "%s\n" % temp
    out = open(IO.charFile, 'w')
    out.writelines(lines)
    out.close()

# returns value of autoTake for selected character
def get_autoTake():
    output = 0
    f = open(IO.charFile, "r")
    for i, line in enumerate(f):
        if i == 21:
            output = int(line[:-1])
    f.close()
    return output

# autoTake prevents user from having to accept the take prompt every time an item is found
def set_autoTake():
    global autoTake
    if get_autoTake() == 0:
        autoTake = 0
    else:
        autoTake = 1

# swaps current value of autoSneak for selected character
def toggle_autoSneak():
    global autoSneak
    lines = open(IO.charFile, 'r').readlines()
    temp = int(lines[22])
    if temp == 1:
        temp = 0
        autoSneak = 0
    elif temp == 0:
        temp = 1
        autoSneak = 1

    lines[22] = "%s\n" % temp
    out = open(IO.charFile, 'w')
    out.writelines(lines)
    out.close()

# returns value of autoSneak for selected character
def get_autoSneak():
    output = 0
    f = open(IO.charFile, "r")
    for i, line in enumerate(f):
        if i == 22:
            output = int(line[:-1])
    f.close()
    return output

# autoSneak prevents user from having to accept the sneak prompt every time an enemy is encountered
def set_autoSneak():
    global autoSneak
    if get_autoSneak() == 0:
        autoSneak = 0
    else:
        autoSneak = 1

# creates a num x num square floor map to be navigated (blindly) by the player
# sets the starting, current, and ending positions for the level
def generate_floor(num):
    num = round(config.floorEquation_1*num + config.floorEquation_2)
    requiredGap = math.sqrt(num)

    global floorMap
    floorMap = [[0] * num for _ in range(num)]

    gap = False
    startX = 0
    startY = 0
    exitX = 0
    exitY = 0
    while not gap:
        startX = randint(0, num - 1)
        startY = randint(0, num - 1)

        while True:
            exitX = randint(0, num - 1)
            exitY = randint(0, num - 1)
            if exitX != startX or exitY != startY:
                break

        distance = calculateDiagonalDistance(startX, startY, exitX, exitY)
        if distance >= requiredGap:
            gap = True

    global begin
    global current
    global stop
    begin = [startX, startY]
    current = [startX, startY]
    stop = [exitX, exitY]

def calculateDiagonalDistance(startX, startY, exitX, exitY):
    return ((startX - exitX)**2 + (startY - exitY)**2)**0.5

# displays the floor layout (used exclusively in debugging)
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

# presents the option to delete character or toggle autoSneak/autoTake
def settings():
    if IO.playerCharacter == 'none':
        character.select_character()

    IO.printSettings()
    selection = IO.getSelectionFromUser(['d','t','s','q'], "\n")

    if selection == 'd':
        deleteCharacter()
    elif selection == 't':
        promptToggleAutoTake()
    elif selection == 's':
        promptToggleAutoSneak()
    elif selection == 'q':
        return

# deletes selected character's inventory and character file
def deleteCharacter():
    chars = os.listdir("characters")
    if os.path.exists("character/.gitkeep"):
        chars.remove('.gitkeep')
    print ("Which Character would you like to delete?")
    spot = 0
    for i in chars:
        chars[spot] = i[:-4]
        print ("- %s" % chars[spot])
        spot += 1
    print ("\nTo cancel                 'c'")

    choice = IO.getSelectionFromUser(chars, "\n", "Not a valid character.")
    if choice == 'c':
        return
    else:
        os.remove("characters/%s.txt" % choice)
        os.remove("inventories/%s.inv" % choice)
        print ("Removed %s.\n" % choice)
        IO.print_dash()

# prompt user to change autoTake option
def promptToggleAutoTake():
    print ("Would you like to change autoTake? Currently set to %s. (y/n)" % get_autoTake())
    choice = input("\n")
    print ("")
    if choice == 'y':
        toggle_autoTake()
        print ("AutoTake is now %s.\n" % get_autoTake())
    elif choice == 'n':
        print ("Returning to menu.\n")
    else:
        print (config.invalidResponse)

# prompt user to change autoSneak option
def promptToggleAutoSneak():
    print ("Would you like to change autoSneak? Currently set to %s. (y/n)" % get_autoSneak())
    choice = input("\n")
    print ("")
    if choice == 'y':
        toggle_autoSneak()
        print ("AutoSneak is now %s.\n" % get_autoSneak())
    elif choice == 'n':
        print ("Returning to menu.\n")
    else:
        print (config.invalidResponse)
