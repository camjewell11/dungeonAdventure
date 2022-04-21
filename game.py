import os, random, sys
from random import randint
from select import select

import character, config, environment, inventoryManagement, IO

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
            environment.settings()
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
            character.level_up()
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
            environment.generate_floor(num)
            environment.print_floor()
        elif selection2 == 'q':
            break
        else:
            print ("Invalid selection.\n")

def play_game():
    if IO.playerCharacter == 'none':
        IO.select_character()

    environment.current = environment.begin

    while True:
        environment.youDied = False
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
            inventoryManagement.shop()
        elif selection == 'i':
            IO.display_info()
            IO.print_dash()
        elif selection == 'q':
            break
        else:
            print ("Invalid selection.\n")

        if play_stage:
            environment.generate_floor(stage_num)

            print ("You have entered the Labyrinth - Stage %s. Good luck...\n" % stage_num)

            wisdom = character.get_skill_level('wisdom')
            chance = randint(0, wisdom * 3)
            direction = "none"

            if chance > stage_num:
                if environment.current[0] > environment.stop[0]:
                    if environment.current[1] > environment.stop[1]:
                        direction = "northwest"
                    elif environment.current[1] < environment.stop[1]:
                        direction = "northeast"
                    else:
                        direction = "north"
                elif environment.current[0] < environment.stop[0]:
                    if environment.current[1] > environment.stop[1]:
                        direction = "southwest"
                    elif environment.current[1] < environment.stop[1]:
                        direction = "southeast"
                    else:
                        direction = "south"
                else:
                    if environment.current[1] > environment.stop[1]:
                        direction = "west"
                    elif environment.current[1] < environment.stop[1]:
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
                if environment.youDied:
                    break
                if environment.current[0] == environment.stop[0] and environment.current[1] == environment.stop[1]:
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
                    character.heal()
                elif selection == 'q':
                    print ("Exiting the Labyrinth.")
                    break
                else:
                    print ("Invalid Selection.\n")

def move():
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

    x = environment.current[0]
    y = environment.current[1]
    length = len(environment.floorMap)

    if num == 0 and not x == 0:  # up
        environment.current[0] = x - 1
        environment.floorMap[x][y] += 1
    elif num == 1 and not y == length - 1:  # right
        environment.current[1] = y + 1
        environment.floorMap[x][y] += 1
    elif num == 2 and not x == length - 1:  # down
        environment.current[0] = x + 1
        environment.floorMap[x][y] += 1
    elif num == 3 and not y == 0:  # left
        environment.current[1] = y - 1
        environment.floorMap[x][y] += 1
    else:
        print ("You run into the cave wall...\n")
        return False
    return True

def progress(stage_num):
    found = inventoryManagement.find_item(stage_num)

    # If item not found
    if not found:
        can_sneak = sneak(stage_num)

        while True:
            if environment.autosneak:
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
            environment.youDied = True
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
                found = inventoryManagement.find_item(stage_num)
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
                    character.heal()
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

def sneak(stage_num):
    randy = randint(1, stage_num)
    quiet = randint(1, 3)
    blind_luck = randint(0, 10)

    if (character.get_skill_level('stealth') > randy and quiet >= 2) or blind_luck > 9:
        return True
    else:
        return False

# If this is run as a script.
if __name__ == '__main__':
    environment.setupDirectories()

    print ("Welcome to Cam's Prototype game!\n")
    start()