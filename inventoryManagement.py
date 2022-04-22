import random
import character, config, environment, IO

def has_item(item):
    f = open(IO.inventoryFile, "r")
    quantity = -1
    for i, line in enumerate(f):
        if i > 0:
            spot = line.index(':')
            temp = line[:spot]
            if temp == item:
                quantity = int(line[spot + 1:-1])
    f.close()

    return quantity

def add_item(item, num):
    line_num = 0
    quantity = 0
    if has_item(item) >= 0:
        f = open(IO.inventoryFile, "r")
        for i, line in enumerate(f):
            if item in line:
                spot = line.index(':')
                quantity = int(line[spot + 1:-1])
                line_num = i
        f.close()

        lines = open(IO.inventoryFile, 'r').readlines()
        quantity += num
        lines[line_num] = item + ":" + quantity + "\n"
        out = open(IO.inventoryFile, 'w')
        out.writelines(lines)
        out.close()
    else:
        with open(IO.inventoryFile, 'a') as f:
            f.write("%s:%s\n" % (str(item), str(num)))

def remove_item(item, num=1):
    line_num = 0
    quantity = 0
    if has_item(item) > 0:
        f = open(IO.inventoryFile, "r")
        for i, line in enumerate(f):
            if item in line:
                spot = line.index(':')
                quantity = int(line[spot + 1:-1])
                line_num = i
        f.close()

        lines = open(IO.inventoryFile, 'r').readlines()
        quantity -= num
        lines[line_num] = "%s:%s\n" % (item, quantity)
        out = open(IO.inventoryFile, 'w')
        out.writelines(lines)
        out.close()

def shop():
    print ("Welcome to the General Store!")
    print ("Here you can find all sorts of goodies and unload some of your pack.\n")
    while True:
        IO.printShopPrompt()
        selection = IO.getSelectionFromUser(['s','b','q'], "\n")

        if selection == 's':
            sellItem()
        elif selection == 'b':
            print ("We have lots to offer!\n")
            while True:
                IO.printShopOffers()

                item = input("\n")
                print ("")
                cost = int(get_cost(item)*1.2)

                if item == 'q':
                    break
                elif cost <= 0:
                    print ("That is not an item for sale.\n")
                elif cost > 0:
                    print ("You bought a %s for %s gold.\n" % (item, cost))
                    add_item(item, 1)
                    remove_item(config.currencyName, cost)
                else:
                    print (config.invalidResponse)
        elif selection == 'q':
            break
        else:
            print (config.invalidResponse)

def sellItem():
    while True:
        print ("What would you like to sell?")
        f = open(IO.inventoryFile, 'r')
        for i, line in enumerate(f):
            if i > 1:
                spot = line.index(':')
                item = line[:spot]
                quantity = line[spot + 1:-1]
                cost = get_cost(item)
                print ("%s \t-\t %s      \t%s gold" % (item, quantity, cost))

        print ("\nTo quit                         'q'")
        print ("You have %s gold." % has_item(config.currencyName))
        item = input("\n")
        print ("")

        if item == 'q':
            break
        elif has_item(item) == 0:
            print ("You do not have any %s's.\n" % item)
        elif has_item(item) == 1:
            remove_item(item)
            add_item(config.currencyName, get_cost(item))
            print ("You've just sold a %s for %s gold pieces." % (item, get_cost(item)))
            IO.print_dash(True)
            break
        elif has_item(item) > 1:
            while True:
                print ("How many would you like to sell? You have %s. 'q' to quit." % has_item(item))
                num = int(input("\n")) if num != 'q' else 'q'
                print ("")

                if num > has_item(item):
                    print ("You do not have that many...\n")
                elif num < 1:
                    print ("You cannot sell less than 1...\n")
                elif num <= has_item(item):
                    print ("You sell %s %s\'s for %s gold.\n" % (num, item, num*get_cost(item)))
                    add_item(config.currencyName, get_cost(item)*num)
                    remove_item(item, num)
                    break
                elif num == 'q':
                    break
                else:
                    print (config.invalidResponse)
        else:
            print (config.invalidResponse)

def offer_items(stage_num):
    costPrompt = "%s \t-\t %s gold"
    print (    costPrompt % config.potionSizes[0], int(get_cost(config.potionSizes[0])*1.2))
    if stage_num > 1:
        print (costPrompt % config.potionSizes[1], int(get_cost(config.potionSizes[1])*1.2))
    if stage_num > 3:
        print (costPrompt % config.potionSizes[2], int(get_cost(config.potionSizes[2])*1.2))
    if stage_num > 6:
        print (costPrompt % config.potionSizes[3], int(get_cost(config.potionSizes[3])*1.2))
    if stage_num > 8:
        print ("Compass \t\t-\t %s gold" % int(get_cost('Compass')*1.2))
    if stage_num > 10:
        print (costPrompt % config.potionSizes[4], int(get_cost(config.potionSizes[4])*1.2))
    if stage_num > 14:
        print (costPrompt % config.potionSizes[5], int(get_cost(config.potionSizes[5])*1.2))
    if stage_num > 18:
        print (costPrompt % config.potionSizes[6], int(get_cost(config.potionSizes[6])*1.2))
    if stage_num > 22:
        print (costPrompt % config.potionSizes[7], int(get_cost(config.potionSizes[7])*1.2))
    if stage_num > 26:
        print (costPrompt % config.potionSizes[8], int(get_cost(config.potionSizes[8])*1.2))
    if stage_num >= 30:
        print (costPrompt % config.potionSizes[9], int(get_cost(config.potionSizes[9], )*1.2))
    print ("")

def find_item(stage_num):
    chance = random.randint(0, 2)
    if chance == 2:
        amountGold = 1
        item = getItemFromStage(stage_num)
        if item == config.currencyName:
            amountGold = random.randint(1, stage_num ** 2)
            print ("You found %s Gold Pieces." % amountGold)
        else:
            print ("You found a %s.\n" % item)

        if not environment.autotake:
            print ("Would you like to take it? (y/n)")
            choice = input("\n")
            print ("")
        if environment.autotake or choice == 'y':
            if amountGold > 1:
                print ("You take the gold.\n")
            else:
                print ("You take the %s.\n" % item)
        else:
            print ("You left it behind.\n")

        add_item(item, amountGold)
    else:
        return False
    return True

def getItemFromStage(stage_num):
    randy = random.randint(0, character.get_skill_level('luck'))
    if randy > 75 and stage_num > 25:
        item, values = random.choice(list(config.item_table9.items()))
    elif randy > 50 and stage_num > 20:
        item, values = random.choice(list(config.item_table8.items()))
    elif randy > 45 and stage_num > 16:
        item, values = random.choice(list(config.item_table7.items()))
    elif randy > 35 and stage_num > 12:
        item, values = random.choice(list(config.item_table6.items()))
    elif randy > 25 and stage_num > 8:
        item, values = random.choice(list(config.item_table5.items()))
    elif randy > 15 and stage_num > 4:
        item, values = random.choice(list(config.item_table4.items()))
    elif randy > 10 and stage_num > 3:
        item, values = random.choice(list(config.item_table3.items()))
    elif randy > 5 and stage_num > 2:
        item, values = random.choice(list(config.item_table2.items()))
    elif randy > 3 and stage_num > 1:
        item, values = random.choice(list(config.item_table1.items()))
    else:
        return False
    return item

def get_cost(item):
    if item in config.item_table1:
        return config.item_table1[item][1]
    elif item in config.item_table2:
        return config.item_table2[item][1]
    elif item in config.item_table3:
        return config.item_table3[item][1]
    elif item in config.item_table4:
        return config.item_table4[item][1]
    elif item in config.item_table5:
        return config.item_table5[item][1]
    elif item in config.item_table6:
        return config.item_table6[item][1]
    elif item in config.item_table7:
        return config.item_table7[item][1]
    elif item in config.item_table8:
        return config.item_table8[item][1]
    elif item in config.item_table9:
        return config.item_table9[item][1]
    else:
        return False