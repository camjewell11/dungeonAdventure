import random
import character, config, environment, IO

# returns quantity of specified item or false if none
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

# adds num of item to inventory file for selected character
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
        lines[line_num] = item + ":" + str(quantity) + "\n"
        out = open(IO.inventoryFile, 'w')
        out.writelines(lines)
        out.close()
    else:
        with open(IO.inventoryFile, 'a') as f:
            f.write("%s:%s\n" % (str(item), str(num)))

# removes num of item from inventory file for selected character
# if new quantity is zero, delete the item from file entirely
def remove_item(item, numToSell=1):
    line_num = 0
    quantity = 0
    currentQuantity = has_item(item)
    newQuantity = currentQuantity - numToSell

    if currentQuantity > 0:
        f = open(IO.inventoryFile, "r")
        for i, line in enumerate(f):
            if item in line:
                spot = line.index(':')
                quantity = int(line[spot + 1:-1])
                line_num = i
        f.close()

        lines = open(IO.inventoryFile, 'r').readlines()
        quantity -= numToSell
        if newQuantity == 0 and item != config.currencyName:
            del lines[line_num]
        else:
            lines[line_num] = "%s:%s\n" % (item, quantity)
        out = open(IO.inventoryFile, 'w')
        out.writelines(lines)
        out.close()

# present buy and sell options for furthest unlocked stage
def shop():
    print ("Welcome to the General Store!")
    print ("Here you can find all sorts of goodies and unload some of your pack.\n")
    while True:
        IO.printShopPrompt()
        selection = IO.getSelectionFromUser(['s','b','q'], "\n")

        if selection == 's':
            sellItem()
        elif selection == 'b':
            buyItem()
        elif selection == 'q':
            break
        else:
            print (config.invalidResponse)

# prompt user to sell which item and how many
def sellItem():
    print ("You have %s gold." % has_item(config.currencyName))
    print ("")
    print ("What would you like to sell?")
    items = IO.printInventory()
    print ("\nTo quit                         'q'")

    item = IO.getSelectionFromUser(items, "")
    item = getItemFromItems(item, items)

    if not item:
        print (config.invalidResponse)
        sellItem()

    if item == 'q':
        return
    elif has_item(item) == 0:
        print ("You do not have any %s's.\n" % item)
    elif has_item(item) == 1:
        remove_item(item)
        add_item(config.currencyName, get_cost(item))
        print ("You've just sold a %s for %s gold pieces." % (item, get_cost(item)))
        IO.print_dash(True)
    elif has_item(item) > 1:
        print ("How many would you like to sell? You have %s. 'q' to quit." % has_item(item))
        num = IO.getIntFromUser("\n")

        if num > has_item(item):
            print ("You do not have that many...\n")
        elif num < 1:
            print ("You cannot sell less than 1...\n")
        elif num <= has_item(item):
            print ("You sell %s %s\'s for %s gold.\n" % (num, item, num*get_cost(item)))
            add_item(config.currencyName, get_cost(item)*num)
            remove_item(item, num)
        elif num == 'q':
            return

# prompt user to buy which item and how many
def buyItem():
    print ("We have lots to offer!")
    IO.print_dash(True)
    items = IO.printShopOffers()
    items.append('q')
    item = IO.getSelectionFromUser(items, "")

    if item == 'q':
        return
    elif not getItemFromItems(item, items):
        print ("That is not an item for sale.\n")
    else:
        item = getItemFromItems(item, items)
        cost = int(get_cost(item)*1.2)
        print ("You bought a %s for %s gold.\n" % (item, cost))
        add_item(item, 1)
        remove_item(config.currencyName, cost)

# returns properly capitalized item from available items
def getItemFromItems(choice, items):
    for option in items:
        if option.lower() == choice.lower():
            return option
    return False

# display items available depending on which stage has been reached
def offer_items(stage_num):
    costPrompt = "%s \t-\t %d gold"
    items = []
    print (costPrompt % (config.potionSizes[0], int(get_cost(config.potionSizes[0])*1.2)))
    items.append(config.potionSizes[0])
    if stage_num > 1:
        print (costPrompt % (config.potionSizes[1], int(get_cost(config.potionSizes[1])*1.2)))
        items.append(config.potionSizes[1])
    if stage_num > 3:
        print (costPrompt % (config.potionSizes[2], int(get_cost(config.potionSizes[2])*1.2)))
        items.append(config.potionSizes[2])
    if stage_num > 6:
        print (costPrompt % (config.potionSizes[3], int(get_cost(config.potionSizes[3])*1.2)))
        items.append(config.potionSizes[3])
    if stage_num > 8:
        print ("Compass \t\t-\t %s gold" % int(get_cost('Compass')*1.2))
        items.append("Compass")
    if stage_num > 10:
        print (costPrompt % (config.potionSizes[4], int(get_cost(config.potionSizes[4])*1.2)))
        items.append(config.potionSizes[4])
    if stage_num > 14:
        print (costPrompt % (config.potionSizes[5], int(get_cost(config.potionSizes[5])*1.2)))
        items.append(config.potionSizes[5])
    if stage_num > 18:
        print (costPrompt % (config.potionSizes[6], int(get_cost(config.potionSizes[6])*1.2)))
        items.append(config.potionSizes[6])
    if stage_num > 22:
        print (costPrompt % (config.potionSizes[7], int(get_cost(config.potionSizes[7])*1.2)))
        items.append(config.potionSizes[7])
    if stage_num > 26:
        print (costPrompt % (config.potionSizes[8], int(get_cost(config.potionSizes[8])*1.2)))
        items.append(config.potionSizes[8])
    if stage_num >= 30:
        print (costPrompt % (config.potionSizes[9], int(get_cost(config.potionSizes[9], )*1.2)))
        items.append(config.potionSizes[9])
    print ("")

    return items

# random chance at finding item based on current floor
def find_item(stage_num):
    chance = random.randint(0, 2)
    if chance == 2:
        amountGold = 1
        item = getItemFromStage(stage_num)
        if item == config.currencyName:
            amountGold = random.randint(1, stage_num ** 2)
            print ("You found %s Gold Pieces." % amountGold)
        elif item:
            print ("You found a %s.\n" % item)
        elif not item:
            return

        promptTakeItem(amountGold, item)
        add_item(item, amountGold)
    else:
        return False
    return True

# display to user to take item; take automatically if setting enabled
def promptTakeItem(amountGold, item):
    choice = None
    if not environment.autoTake:
        print ("Would you like to take it? (y/n)")
        choice = input("\n")
        print ("")
    if environment.autoTake or choice == 'y':
        if amountGold > 1:
            print ("You take the gold.\n")
        else:
            print ("You take the %s.\n" % item)
    else:
        print ("You left it behind.\n")

# returns random item from possible items for stage
def getItemFromStage(stage_num):
    randy = random.randint(0, character.get_skill_level('luck'))
    if randy > 75 and stage_num > 25:
        item, _ = random.choice(list(config.item_table9.items()))
    elif randy > 50 and stage_num > 20:
        item, _ = random.choice(list(config.item_table8.items()))
    elif randy > 45 and stage_num > 16:
        item, _ = random.choice(list(config.item_table7.items()))
    elif randy > 35 and stage_num > 12:
        item, _ = random.choice(list(config.item_table6.items()))
    elif randy > 25 and stage_num > 8:
        item, _ = random.choice(list(config.item_table5.items()))
    elif randy > 15 and stage_num > 4:
        item, _ = random.choice(list(config.item_table4.items()))
    elif randy > 10 and stage_num > 3:
        item, _ = random.choice(list(config.item_table3.items()))
    elif randy > 5 and stage_num > 2:
        item, _ = random.choice(list(config.item_table2.items()))
    elif randy > 3 and stage_num > 1:
        item, _ = random.choice(list(config.item_table1.items()))
    else:
        return False
    return item

# returns value of item
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
