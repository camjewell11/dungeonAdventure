import os
import IO
from random import randint

def setupDirectories():
    workingDir = "Dungeon/Game/"
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
    global begin
    global stop
    global current

    num = (num / 3) + 2
    floorMap = [[0] * num for _ in range(num)]

    startX = randint(0, num - 1)
    startY = randint(0, num - 1)

    while True:
        exitX = randint(0, num - 1)
        exitY = randint(0, num - 1)
        if exitX != startX or exitY != startY:
            break

    begin = [startX, startY]
    current = [startX, startY]
    stop = [exitX, exitY]

def print_floor():
    global floorMap
    print ("")
    for x in range(len(floorMap)):
        for y in range(len(floorMap)):
            if x == current[0] and y == current[1]:
                print ('O')
            elif x == stop[0] and y == stop[1]:
                print ('X')
            else:
                print ('{}'.format(floorMap[x][y]))
        print ()
    IO.print_dash(True)

    print ("Current: %s" % current)
    print ("Start: %s" % begin)
    print ("Exit: %s\n" % stop)