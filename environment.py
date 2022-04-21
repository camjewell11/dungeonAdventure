import os

def setupDirectories():
    workingDir = "Dungeon/Game/"
    if not os.path.exists(workingDir + "characters"):
        os.makedirs(workingDir + "characters")
    if not os.path.exists(workingDir + "inventories"):
        os.makedirs(workingDir + "inventories")

def toggle_autotake():
    global autotake

    lines = open(charFile, 'r').readlines()
    temp = int(lines[21])
    if temp == 1:
        temp = 0
        autotake = 0
    elif temp == 0:
        temp = 1
        autotake = 1

    lines[21] = "%s\n" % temp
    out = open(charFile, 'w')
    out.writelines(lines)
    out.close()

def get_autotake():
    output = 0
    f = open(charFile, "r")
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

    lines = open(charFile, 'r').readlines()
    temp = int(lines[22])
    if temp == 1:
        temp = 0
        autosneak = 0
    elif temp == 0:
        temp = 1
        autosneak = 1

    lines[22] = "%s\n" % temp
    out = open(charFile, 'w')
    out.writelines(lines)
    out.close()

def get_autosneak():
    output = 0
    f = open(charFile, "r")
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