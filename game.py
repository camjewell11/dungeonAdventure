import os, random, sys
from random import randint
from select import select

import character, config, environment, IO

skillPoints = 0
first = True
floorMap = []
begin = []
stop = []
current = []
youDied = False
autotake = 0
autosneak = 0

def start():
    while True:
        print ("What would you like to do?")
        IO.print_dash()
        print ("Create Character:        1")
        print ("Select Character:        2")
        print ("Play Game                3")
        print ("Settings:                4")
        print ("Exit:                    5")

        selection = input("\n")
        selection = selection.lower()
        IO.print_dash(True)
        if selection == '1':
            character.create_character()
        elif selection == '2':
            character.select_character()
        elif selection == '3':
            play_game()
        elif selection == '4':
            settings()
        elif selection == '5' or selection == 'q':
            break
        elif selection == 'debug':
            if IO.playerCharacter == 'none':
                character.select_character()
            debug_menu()
    else:
        print ("That was not a valid selection.\n")

def debug_menu():
    while True:
        print ("Secret Debug Menu")
        IO.print_dash()
        print ("For active info         'i'")
        print ("To level up a skill     'u'")
        print ("To add XP               'x'")
        print ("To view enemy tables    'e'")
        print ("To kill player          'k'")
        print ("To create floorMap      'm'")
        print ("To return               'q'")

        selection2 = input("\n")
        selection2 = selection2.lower()
        IO.print_dash(True)
        if selection2 == 'i':
            IO.display_info()
        elif selection2 == 'u':
            level_up()
        elif selection2 == 'e':
            print (config.enemy_table)
        elif selection2 == 'x':
            while True:
                try:
                    num = int(input("How much XP would you like to add?\n"))
                except ValueError:
                    print ("That wasn't a number!")
                else:
                    break
            print ("")
            character.add_xp(num)
            print ("Total XP now:            %s\n" % character.get_xp())
        elif selection2 == 'k':
            character.died()
        elif selection2 == 'm':
            while True:
                try:
                    num = int(input("Enter a Stage number.\n"))
                except ValueError:
                    print ("That wasn't a number!")
                else:
                    break
            print ("")
            generate_floor(num)
            print_floor()
        elif selection2 == 'q':
            break
        else:
            print ("Invalid selection.\n")


def settings():
    if IO.playerCharacter == 'none':
        character.select_character()
    global autotake
    while True:
        print ("         Settings            ")
        IO.print_dash()
        print ("To Delete Character       'd'")
        print ("To toggle autotake items  't'")
        print ("To toggle autosneak       's'")
        print ("To quit                   'q'")
        selection = input("\n")
        print ("")

        if selection == 'd':
            chars = os.listdir("characters")
            print ("Which Character would you like to delete?")
            spot = 0
            for i in chars:
                chars[spot] = i[:-4]
                print ("- %s" % chars[spot])
                spot += 1
            print ("\nTo cancel                 'c'")

            while True:
                choice = input("\n")
                print ("")
                if choice == 'c':
                    break
                elif choice not in chars:
                    print ("%s is not a valid character." % choice)
                    IO.print_dash(True)
                    print ("Which Character would you like to delete?")
                    for i in chars:
                        print ("- %s" % i)
                    print ("\nTo cancel            'c'")
                else:
                    os.remove("characters/%s.txt" % choice)
                    os.remove("inventories/%s.inv" % choice)
                    print ("Removed %s.\n" % choice)
                    IO.print_dash()
        elif selection == 't':
            print ("Would you like to change autotake? Currently set to %s. (y/n)" % environment.get_autotake())
            choice = input("\n")
            print ("")
            if choice == 'y':
                environment.toggle_autotake()
                print ("Autotake is now %s.\n" % environment.get_autotake())
            elif choice == 'n':
                print ("Returning to menu.\n")
            else:
                print ("Invalid Selection.\n")
        elif selection == 's':
            print ("Would you like to change autosneak? Currently set to %s. (y/n)" % environment.get_autosneak())
            choice = input("\n")
            print ("")
            if choice == 'y':
                environment.toggle_autosneak()
                print ("Autosneak is now %s.\n" % environment.get_autosneak())
            elif choice == 'n':
                print ("Returning to menu.\n")
            else:
                print ("Invalid Selection.\n")
        elif selection == 'q':
            break
        else:
            print ("Invalid Selection.\n")

def play_game():
    if IO.playerCharacter == 'none':
        IO.select_character()

    global begin
    global stop
    global current
    current = begin

    global youDied

    while True:
        youDied = False
        play_stage = False
        specific = False

        print ("What would you like to do?")
        print ("Continue on to Labyrinth - Stage %s   \t 'c'" % character.get_stage())
        print ("Enter a specific Labyrinth Stage      \t 'n'")
        print ("Enter the general store               \t 's'")
        print ("View my info/progression              \t 'i'")
        print ("Quit                                  \t 'q'")

        selection = input("\n")
        print ("")

        if selection == 'c':
            print ("What new foes may await?\n")
            stage_num = character.get_stage()
            play_stage = True
        elif selection == 'n':
            print ("What Stage would you like to enter?")
            stage_num = int(input("\n"))
            print ("")
            if stage_num <= character.get_stage():
                play_stage = True
                specific = True
            else:
                print ("You have not reached that stage yet.\n")
        elif selection == 's':
            shop()
        elif selection == 'i':
            character.display_info()
            IO.print_dash()
        elif selection == 'q':
            break
        else:
            print ("Invalid selection.\n")

        if play_stage:
            generate_floor(stage_num)

            print ("You have entered the Labyrinth - Stage %s. Good luck...\n" % stage_num)

            wisdom = character.character.get_skill_level('wisdom')
            chance = randint(0, wisdom * 3)
            direction = "none"

            if chance > stage_num:
                if current[0] > stop[0]:
                    if current[1] > stop[1]:
                        direction = "northwest"
                    elif current[1] < stop[1]:
                        direction = "northeast"
                    else:
                        direction = "north"
                elif current[0] < stop[0]:
                    if current[1] > stop[1]:
                        direction = "southwest"
                    elif current[1] < stop[1]:
                        direction = "southeast"
                    else:
                        direction = "south"
                else:
                    if current[1] > stop[1]:
                        direction = "west"
                    elif current[1] < stop[1]:
                        direction = "east"

                randy = randint(1, 3)
                if randy == 1:
                    print ("You feel a force pull you to the %s...\n" % direction)
                elif randy == 2:
                    print ("There seems to be an inviting presence to the %s...\n" % direction)
                elif randy == 3:
                    print ("You feel a flow of air moving to the %s...\n" % direction)

            IO.print_dash()

            while True:
                if youDied:
                    break
                if current[0] == stop[0] and current[1] == stop[1]:
                    print ("You have escaped the Labyrinth!")
                    IO.print_dash(True)
                    if not specific:
                        character.add_stage()
                    if stage_num == 1:
                        print ("You are awarded 50 xp for this feat!\n")
                        character.add_xp(50)
                    elif stage_num == 2:
                        print ("You are awarded 100 xp for this feat!\n")
                        character.add_xp(100)
                    elif stage_num == 3:
                        print ("You are awarded 150 xp for this feat!\n")
                        character.add_xp(150)
                    elif stage_num == 4:
                        print ("You are awarded 250 xp for this feat!\n")
                        character.add_xp(250)
                    elif stage_num == 5:
                        print ("You are awarded 500 xp for this feat!\n")
                        character.add_xp(500)
                    elif stage_num == 6:
                        print ("You are awarded 750 xp for this feat!\n")
                        character.add_xp(750)
                    elif stage_num == 7:
                        print ("You are awarded 1000 xp for this feat!\n")
                        character.add_xp(1000)
                    elif stage_num == 8:
                        print ("You are awarded 1500 xp for this feat!\n")
                        character.add_xp(1500)
                    elif stage_num == 9:
                        print ("You are awarded 2000 xp for this feat!\n")
                        character.add_xp(2000)
                    elif stage_num == 10:
                        print ("You are awarded 2500 xp for this feat!\n")
                        character.add_xp(2500)
                    elif stage_num == 11:
                        print ("You are awarded 3000 xp for this feat!\n")
                        character.add_xp(3000)
                    elif stage_num == 12:
                        print ("You are awarded 3500 xp for this feat!\n")
                        character.add_xp(3500)
                    elif stage_num == 13:
                        print ("You are awarded 4000 xp for this feat!\n")
                        character.add_xp(4000)
                    elif stage_num == 14:
                        print ("You are awarded 4500 xp for this feat!\n")
                        character.add_xp(4500)
                    elif stage_num == 15:
                        print ("You are awarded 5000 xp for this feat!\n")
                        character.add_xp(5000)
                    elif stage_num == 16:
                        print ("You are awarded 6000 xp for this feat!\n")
                        character.add_xp(6000)
                    elif stage_num == 17:
                        print ("You are awarded 7000 xp for this feat!\n")
                        character.add_xp(7000)
                    elif stage_num == 18:
                        print ("You are awarded 8000 xp for this feat!\n")
                        character.add_xp(8000)
                    elif stage_num == 19:
                        print ("You are awarded 9000 xp for this feat!\n")
                        character.add_xp(9000)
                    elif stage_num == 20:
                        print ("You are awarded 10000 xp for this feat!\n")
                        character.add_xp(10000)
                    elif stage_num == 21:
                        print ("You are awarded 12500 xp for this feat!\n")
                        character.add_xp(12500)
                    elif stage_num == 22:
                        print ("You are awarded 15000 xp for this feat!\n")
                        character.add_xp(15000)
                    elif stage_num == 23:
                        print ("You are awarded 17500 xp for this feat!\n")
                        character.add_xp(17500)
                    elif stage_num == 24:
                        print ("You are awarded 20000 xp for this feat!\n")
                        character.add_xp(20000)
                    elif stage_num == 25:
                        print ("You are awarded 22500 xp for this feat!\n")
                        character.add_xp(22500)
                    elif stage_num == 26:
                        print ("You are awarded 25000 xp for this feat!\n")
                        character.add_xp(25000)
                    elif stage_num == 27:
                        print ("You are awarded 30000 xp for this feat!\n")
                        character.add_xp(30000)
                    elif stage_num == 28:
                        print ("You are awarded 35000 xp for this feat!\n")
                        character.add_xp(35000)
                    elif stage_num == 29:
                        print ("You are awarded 40000 xp for this feat!\n")
                        character.add_xp(40000)
                    elif stage_num == 30:
                        print ("You are awarded 50000 xp for this feat!\n")
                        character.add_xp(50000)
                    break

                print ("What would you like to do?")
                print ("To move             'm'")
                print ("To heal             'h'")
                print ("To quit             'q'")

                selection = input("\n")
                print ("")

                if selection == 'm':
                    moved = move()
                    if moved:
                        progress(stage_num)
                elif selection == 'h':
                    heal()
                elif selection == 'q':
                    print ("Exiting the Labyrinth.")
                    break
                else:
                    print ("Invalid Selection.\n")

def move():
    global current
    num = 0

    while True:
        print ("In which direction would you like to move?")
        print ("To move up           'u'")
        print ("To move right        'r'")
        print ("To move down         'd'")
        print ("To move left         'l'")
        print ("To cancel            'c'")

        selection = input("\n")
        print ("")

        if selection == 'u':
            num = 0
            break
        elif selection == 'r':
            num = 1
            break
        elif selection == 'd':
            num = 2
            break
        elif selection == 'l':
            num = 3
            break
        elif selection == 'c':
            break
        else:
            print ("Invalid Selection.\n")

    x = current[0]
    y = current[1]
    length = len(floorMap)

    if num == 0 and not x == 0:  # up
        current[0] = x - 1
        floorMap[x][y] += 1
    elif num == 1 and not y == length - 1:  # right
        current[1] = y + 1
        floorMap[x][y] += 1
    elif num == 2 and not x == length - 1:  # down
        current[0] = x + 1
        floorMap[x][y] += 1
    elif num == 3 and not y == 0:  # left
        current[1] = y - 1
        floorMap[x][y] += 1
    else:
        print ("You run into the cave wall...\n")
        return False
    return True

def progress(stage_num):
    found = find_item(stage_num)

    # If item not found
    if not found:
        can_sneak = sneak(stage_num)

        while True:
            if autosneak:
                randy = randint(1, 3)
                if can_sneak:
                    if randy == 1:
                        print ("You managed to get by unnoticed...\n")
                    elif randy == 2:
                        print ("You crawl beneath the danger in a sewage grate...\n")
                    elif randy == 3:
                        print ("You sprint quietly beside the creature and sidle on...\n")
                    IO.print_dash()
                    break
                else:
                    if randy == 1:
                        print ("You couldn't sneak by!\n")
                    elif randy == 2:
                        print ("The creature sees you!\n")
                    elif randy == 3:
                        print ("You were unsuccessful!\n")
                    IO.print_dash()
                    battle(stage_num)
                    IO.print_dash()
                    break
            else:
                print ("Would you like to try to sneak by? (y/n)")
                choice = input("\n")
                print ("")
                count = 0

                randy = randint(1, 3)
                if choice == 'y':
                    if can_sneak:
                        if randy == 1:
                            print ("You managed to get by unnoticed...\n")
                        elif randy == 2:
                            print ("You crawl beneath the danger in a sewage grate...\n")
                        elif randy == 3:
                            print ("You sprint quietly beside the creature and sidle on...\n")
                        IO.print_dash()
                        break
                    else:
                        if randy == 1:
                            print ("You couldn't sneak by!\n")
                        elif randy == 2:
                            print ("The creature sees you!\n")
                        elif randy == 3:
                            print ("You were unsuccessful!\n")
                        IO.print_dash()
                        battle(stage_num)
                        IO.print_dash()
                        break
                elif choice == 'n':
                    if randy == 1:
                        print ("You charge unwittingly into battle!\n")
                    elif randy == 2:
                        print ("Prepare for battle!\n")
                    elif randy == 3:
                        print ("You're in for it now!\n")
                    IO.print_dash()
                    battle(stage_num)
                    IO.print_dash()
                    break
                else:
                    if count > 3:
                        print ("Dude. It's a yes or no question...\n")
                    else:
                        print ("Invalid Selection.")
                    count += 1

def battle(stage_num):
    global youDied
    max_damage = character.get_skill_level('strength') * 2
    max_defense = character.get_skill_level('defense') * 2
    accuracy = character.get_skill_level('accuracy') * 2
    luck = character.get_skill_level('luck')

    turn = randint(1, 2)
    fled = False

    while True:
        opponent = random.choice(config.enemy_table.keys())
        if config.enemy_table[opponent][0] <= stage_num:
            if config.enemy_table[opponent][0] > stage_num - 5:
                break

    stats = config.enemy_table[opponent]

    print ("You've entered battle with a %s.\n" % opponent)
    health = character.get_health()
    enemy_health = stats[2]
    enemy_max_damage = stats[3]

    if turn == 2:
        print ("You have %s health.             %s has %s health.\n" % (health, opponent, enemy_health))

    while True:
        if health <= 0:
            youDied = True
            character.died()
            break
        if enemy_health <= 0:
            print ("You have killed it!\n")
            character.add_xp(stats[1])

            print ("It appears the enemy dropped an item before disappearing into nothing.\n")
            if randint(0, 1) == 1:
                print ("Turns out to be nothing.\n")
            else:
                print ("You approach vicariously.\n")
                found = find_item(stage_num)
                if not found:
                    print ("Turns out it was nothing...\n")

            level = character.get_level()
            print ("Your current XP is %s of %s to level %s.\n" % (character.get_xp(), config.level_table[level + 1], level + 1))
            break
        if turn == 1:
            while True:
                print ("You have %s health.             %s has %s health.\n" % (health, opponent, enemy_health))

                print ("What would you like to do?\n")
                print ("Attack               'a'")
                print ("Heal                 'h'")
                print ("Flee                 'f'")
                choice = input("\n")
                print ("")

                if choice == 'a':
                    print ("You attack!\n")
                    hits = randint(1, accuracy * 2)
                    if hits > stats[0]:
                        if randint(0, luck) > randint(0, stage_num * 2):
                            print ("You land a critical strike!\n")
                            damage = randint(max_damage / 2, max_damage) * 2
                        else:
                            damage = randint(1, max_damage)
                        print ("You deal %s damage!\n" % damage)
                        enemy_health -= damage
                    else:
                        print ("Your attack misses!\n")

                    select([sys.stdin], [], [], 1)

                    IO.print_dash(True)
                    break
                elif choice == 'h':
                    heal()
                    break
                elif choice == 'f':
                    print ("You attempt to flee!\n")
                    if randint(character.get_skill_level('stealth') / 2, character.get_skill_level('stealth')) > randint(0, stage_num * 2):
                        print ("You get away safely...\n")
                        fled = True
                    else:
                        print ("You cannot get away!\n")
                    IO.print_dash()
                    break
                else:
                    print ("Invalid Selection.\n")
            turn = 2
        elif fled:
            break
        elif turn == 2:
            print ("The %s attacks!\n" % opponent)
            if randint(0, max_defense) > randint(0, enemy_max_damage):
                print ("You blocked the attack!\n")
            else:
                if randint(1, 5) > 4:
                    print ("On no! A critical hit!\n")
                    damage = randint(enemy_max_damage / 2, enemy_max_damage) * 2
                else:
                    damage = randint(1, enemy_max_damage)
                print ("The %s deals %s damage!\n" % (opponent, damage))
                health -= damage
                character.set_health(health)

            select([sys.stdin], [], [], 1)

            IO.print_dash()
            turn = 1

def find_item(stage_num):
    randy = randint(0, character.get_skill_level('luck'))
    chance = randint(1, 3)

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
        if autotake:
            if item == "Gold Piece":
                num = randint(1, stage_num ** 2)
                print ("You found %s Gold Pieces. You take the gold.\n" % num)
            else:
                print ("You found a %s.\nYou take the %s.\n" % (item, item))
        else:
            if item == "Gold Piece":
                num = randint(1, stage_num ** 2)
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

def sneak(stage_num):
    randy = randint(1, stage_num)
    quiet = randint(1, 3)
    blind_luck = randint(0, 10)

    if (character.get_skill_level('stealth') > randy and quiet >= 2) or blind_luck > 9:
        return True
    else:
        return False

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
            if temp + num > character.get_max_health():
                temp = character.get_max_health()
            else:
                temp += num
            print ("You healed %s health points.\n" % num)
            lines[18] = "%s\n" % temp
            out = open(IO.charFile, 'w')
            out.writelines(lines)
            out.close()
            print ("You now have %s health.\n" % character.get_health())


def shop():
    print ("Welcome to the General Store!")
    print ("Here you can find all sorts of goodies and unload some of your pack.\n")
    while True:
        print ("What would you like to do?")
        print ("To sell                's'")
        print ("To buy                 'b'")
        print ("To quit                'q'")
        print ("")
        print ("You have %s gold." % has_item('Gold Piece'))

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
                print ("You have %s gold." % has_item('Gold Piece'))
                item = input("\n")
                print ("")

                if item == 'q':
                    break
                elif has_item(item) == 0:
                    print ("You do not have any %s's.\n" % item)
                elif has_item(item) == 1:
                    remove_item(item)
                    add_item('Gold Piece', get_cost(item))
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
                            add_item('Gold Piece', get_cost(item)*num)
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
                print ("You have %s gold." % has_item('Gold Piece'))

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
                    remove_item('Gold Piece', cost)
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

def generate_floor(num):
    global floorMap
    global begin
    global stop
    global current

    num = (num / 3) + 2
    floorMap = [[0] * num for _ in xrange(num)]

    startx = randint(0, num - 1)
    starty = randint(0, num - 1)

    while True:
        exitx = randint(0, num - 1)
        exity = randint(0, num - 1)
        if exitx == startx and exity == starty:
            pass
        else:
            break

    begin = [startx, starty]
    current = [startx, starty]
    stop = [exitx, exity]

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


def has_item(item):
    f = open(inventoryFile, "r")
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
        f = open(inventoryFile, "r")
        for i, line in enumerate(f):
            if item in line:
                spot = line.index(':')
                quantity = int(line[spot + 1:-1])
                line_num = i
        f.close()

        lines = open(inventoryFile, 'r').readlines()
        quantity += num
        lines[line_num] = "%s:%s\n" % (item, quantity)
        out = open(inventoryFile, 'w')
        out.writelines(lines)
        out.close()
    else:
        with open(inventoryFile, 'a') as f:
            f.write("%s:%s\n" % (str(item), str(num)))

def remove_item(item, num=1):
    line_num = 0
    quantity = 0
    if has_item(item) > 0:
        f = open(inventoryFile, "r")
        for i, line in enumerate(f):
            if item in line:
                spot = line.index(':')
                quantity = int(line[spot + 1:-1])
                line_num = i
        f.close()

        lines = open(inventoryFile, 'r').readlines()
        quantity -= num
        lines[line_num] = "%s:%s\n" % (item, quantity)
        out = open(inventoryFile, 'w')
        out.writelines(lines)
        out.close()

def get_cost(item):
    if item in item_table1:
        return item_table1[item][1]
    elif item in item_table2:
        return item_table2[item][1]
    elif item in item_table3:
        return item_table3[item][1]
    elif item in item_table4:
        return item_table4[item][1]
    elif item in item_table5:
        return item_table5[item][1]
    elif item in item_table6:
        return item_table6[item][1]
    elif item in item_table7:
        return item_table7[item][1]
    elif item in item_table8:
        return item_table8[item][1]
    elif item in item_table9:
        return item_table9[item][1]
    else:
        return False

# If this is run as a script.
if __name__ == '__main__':
    main()
    environment.setupDirectories()

    print ("Welcome to Cam's Prototype game!\n")
    start()