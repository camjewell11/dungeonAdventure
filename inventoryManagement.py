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
        print ("What would you like to do?")
        print ("To sell                's'")
        print ("To buy                 'b'")
        print ("To quit                'q'")
        print ("")
        print ("You have %s gold." % has_item('Gold Pieces'))

        selection = input("\n")
        print ("")

        if selection == 's':
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
                print ("You have %s gold." % has_item('Gold Pieces'))
                item = input("\n")
                print ("")

                if item == 'q':
                    break
                elif has_item(item) == 0:
                    print ("You do not have any %s's.\n" % item)
                elif has_item(item) == 1:
                    remove_item(item)
                    add_item('Gold Pieces', get_cost(item))
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
                            add_item('Gold Pieces', get_cost(item)*num)
                            remove_item(item, num)
                            break
                        elif num == 'q':
                            break
                        else:
                            print ("Invalid selection.\n")
                else:
                    print ("Invalid selection.\n")

        elif selection == 'b':
            print ("We have lots to offer!\n")
            while True:
                print ("What would you like to buy?\n")
                offer_items(character.get_stage())

                print ("To quit                  'q'")
                print ("You have %s gold." % has_item('Gold Pieces'))

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
                    remove_item('Gold Pieces', cost)
                else:
                    print ("Invalid selection.\n")

        elif selection == 'q':
            break
        else:
            print ("Invalid selection.\n")

def offer_items(stage_num):
    print ("Tiny Potion \t-\t %s gold" % int(get_cost('Tiny Potion')*1.2))
    if stage_num > 1:
        print ("Little Potion \t-\t %s gold" % int(get_cost('Little Potion')*1.2))
    if stage_num > 3:
        print ("Small Potion \t-\t %s gold" % int(get_cost('Small Potion')*1.2))
    if stage_num > 6:
        print ("Regular Potion \t-\t %s gold" % int(get_cost('Regular Potion')*1.2))
    if stage_num > 8:
        print ("Compass \t\t-\t %s gold" % int(get_cost('Compass')*1.2))
    if stage_num > 10:
        print ("Big Potion \t-\t %s gold" % int(get_cost('Big Potion')*1.2))
    if stage_num > 14:
        print ("Large Potion \t-\t %s gold" % int(get_cost('Large Potion')*1.2))
    if stage_num > 18:
        print ("Huge Potion \t-\t %s gold" % int(get_cost('Huge Potion')*1.2))
    if stage_num > 22:
        print ("Gigantic Potion \t-\t %s gold" % int(get_cost('Gigantic Potion')*1.2))
    if stage_num > 26:
        print ("Epic Potion \t-\t %s gold" % int(get_cost('Epic Potion')*1.2))
    if stage_num >= 30:
        print ("Legendary Potion \t-\t %s gold" % int(get_cost('Legendary Potion')*1.2))
    print ("")

def find_item(stage_num):
    randy = random.randint(0, character.get_skill_level('luck'))
    chance = random.randint(0, 2)

    if chance > 2:
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

        num = 1
        if environment.autotake:
            if item == "Gold Piece":
                num = random.randint(1, stage_num ** 2)
                print ("You found %s Gold Pieces. You take the gold.\n" % num)
            else:
                print ("You found a %s.\nYou take the %s.\n" % (item, item))
        else:
            if item == "Gold Piece":
                num = random.randint(1, stage_num ** 2)
                print ("You found %s Gold Pieces." % num)
            else:
                print ("You found a %s.\n" % item)

            print ("Would you like to take it? (y/n)")
            choice = input("\n")
            print ("")
            if choice == 'y':
                if num > 1:
                    print ("You take the gold.\n")
                else:
                    print ("You take the %s.\n" % item)
            else:
                print ("You left it behind.\n")

        add_item(item, num)

    else:
        return False
    return True

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