import random, time
import character, config, environment, inventoryManagement, IO


# recursively called to present player with continue, stage selection, info, and shop prompts
def play_game():
    if IO.playerCharacter == 'none':
        loaded = character.select_character()
    else:
        loaded = True
    if not loaded:
        return

    environment.current = environment.begin
    environment.youDied = False
    specific = False

    IO.printPlayGameOptions()
    selection = IO.getSelectionFromUser(['c', 'n', 's', 'i', 'q'])

    stage_num = 0
    if selection == 'c':
        print("What new foes may await?\n")
        stage_num = character.get_stage()
    elif selection == 'n':
        print("What Stage would you like to enter?")
        stage_num = IO.getIntFromUser("\n")
        if stage_num <= character.get_stage():
            specific = True
        else:
            print("You have not reached that stage yet.\n")
    elif selection == 's':
        inventoryManagement.shop()
        play_game()
    elif selection == 'i':
        IO.display_info()
        play_game()

    if selection == 'q':
        return
    elif selection in ['c', 'n']:
        environment.generate_floor(stage_num)
        print("You have entered the Labyrinth - Stage %s. Good luck..." % stage_num)

        IO.printMapHint(stage_num)
        IO.print_dash(True)

        exploreLevel(stage_num, specific)
        play_game()  # repeat until quit


# begins gameplay, explore a generated floor using move and heal commands
def exploreLevel(stage_num, specific):
    if environment.youDied:
        return
    elif environment.current[0] == environment.stop[0] and environment.current[1] == environment.stop[1]:
        IO.printEscape()
        if not specific:
            character.add_stage()
            print("You are awarded %d xp for this feat!\n" % config.stageXP[stage_num])
            character.add_xp(config.stageXP[stage_num])
        return

    IO.printLevelExplore()
    selection = IO.getSelectionFromUser(['m', 'h', 'q'], "\n")

    if selection == 'm':
        # able to move and item not found
        if move() and not inventoryManagement.find_item(stage_num):
            progress(stage_num)
    elif selection == 'h':
        character.heal()
    elif selection == 'q':
        print("Exiting the Labyrinth.")
        IO.print_dash(True)
        return
    exploreLevel(stage_num, specific)


# navigate the floor via up, down, left, and right commands
def move():
    IO.printMoveDirection()
    selection = IO.getSelectionFromUser(['u', 'r', 'd', 'l', 'c'], "\n")

    if selection == 'u':
        num = 0
    elif selection == 'r':
        num = 1
    elif selection == 'd':
        num = 2
    elif selection == 'l':
        num = 3
    elif selection == 'c':
        return
    else:
        num = None

    x = environment.current[0]
    y = environment.current[1]
    length = len(environment.floorMap)

    if num == 0 and x != 0:  # up
        environment.current[0] = x - 1
        environment.floorMap[x][y] += 1
    elif num == 1 and y != length - 1:  # right
        environment.current[1] = y + 1
        environment.floorMap[x][y] += 1
    elif num == 2 and x != length - 1:  # down
        environment.current[0] = x + 1
        environment.floorMap[x][y] += 1
    elif num == 3 and y != 0:  # left
        environment.current[1] = y - 1
        environment.floorMap[x][y] += 1
    else:
        print("You run into the cave wall...\n")
        return False
    return True


# prompt with sneak option; enter battle on failed sneak
def progress(stage_num):
    count = 0
    while True:
        choice = None
        if not environment.autoSneak:
            print("Would you like to try to sneak by? (y/n)")
            choice = input("\n")
            print("")
        randy = random.randint(0, 2)
        if environment.autoSneak or choice == 'y':
            print("You attempt to sneak by...")
            time.sleep(1)
            if IO.printSneak(stage_num):
                return
            break
        elif choice == 'n':
            print(config.noSneakOptions[randy])
            break
        else:
            if count > 3:
                print("Dude. It's a yes or no question...\n")
            else:
                print("Invalid Selection.")
            count += 1
    IO.print_dash(True)
    battle(stage_num)
    IO.print_dash(True)


# battle script; repeats until fled or one member is killed
def battle(stage_num):
    max_damage = character.get_skill_level('strength') * 2
    max_defense = character.get_skill_level('defense') * 2
    accuracy = character.get_skill_level('accuracy') * 2
    luck = character.get_skill_level('luck')

    # pick opponent based on floor
    while True:
        opponent = random.choice(list(config.enemy_table.keys()))
        if config.enemy_table[opponent][0] <= stage_num:
            if config.enemy_table[opponent][0] > stage_num - 5:
                break

    print("You've entered battle with a %s.\n" % opponent)
    stats = config.enemy_table[opponent]
    health = character.get_health()
    enemy_health = random.randint(stats[2], stats[3])
    enemy_max_damage = stats[4]

    # either you or the opponent begins
    turn = random.randint(1, 2)
    if turn == 2:
        print("You have %s health.             %s has %s health.\n" % (health, opponent, enemy_health))

    # main battle loop
    fled = False
    while True:
        if health <= 0:
            environment.youDied = True
            character.died()
            break
        if enemy_health <= 0:
            print("You have killed it!\n")
            character.add_xp(stats[1])
            itemDrop(stage_num)

            level = character.get_level()
            print("Your current XP is %s of %s to level %s."
                  % (character.get_xp(), config.level_table[level + 1], level + 1))
            break
        if turn == 1:  # your turn
            print("You have %s health.             %s has %s health.\n" % (health, opponent, enemy_health))
            enemy_health, fled = makeYourMove(stage_num, accuracy, luck, max_damage, stats, enemy_health)
            turn = 2
        elif turn == 2:  # opponent turn
            health = enemyMove(health, opponent, max_defense, enemy_max_damage)
            IO.print_dash(True)
            turn = 1
        if fled:
            break


# choose from action options; attack, heal, or flea
def makeYourMove(stage_num, accuracy, luck, max_damage, stats, enemy_health):
    print("What would you like to do?\n")
    print("Attack               'a'")
    print("Heal                 'h'")
    print("Flee                 'f'")
    choice = IO.getSelectionFromUser(['a', 'h', 'f'], "\n")

    fled = False
    if choice == 'a':
        print("You attack!\n")
        time.sleep(1)
        hits = random.randint(1, accuracy * 2)
        if hits > stats[0]:
            if random.randint(0, luck) > random.randint(0, stage_num * 2):
                print("You land a critical strike!\n")
                damage = random.randint(max_damage / 2, max_damage) * 2
            else:
                damage = random.randint(1, max_damage)
            print("You deal %s damage!\n" % damage)
            enemy_health -= damage
        else:
            print("Your attack misses!\n")

        IO.print_dash(True)
        time.sleep(1)
    elif choice == 'h':
        character.heal()
    elif choice == 'f':
        print("You attempt to flee!\n")
        time.sleep(1)
        if random.randint(character.get_skill_level('stealth') / 2,
                          character.get_skill_level('stealth')) > random.randint(0, stage_num * 2):
            print("You get away safely...\n")
            fled = True
        else:
            print("You cannot get away!\n")
        IO.print_dash()

    return enemy_health, fled


# opponent attacks
def enemyMove(health, opponent, max_defense, enemy_max_damage):
    print("The %s attacks!\n" % opponent)
    time.sleep(1)
    if random.randint(0, max_defense) > random.randint(0, enemy_max_damage):
        print("You blocked the attack!\n")
    else:
        if random.randint(1, 5) > 4:
            print("On no! A critical hit!\n")
            damage = random.randint(int(enemy_max_damage / 2), enemy_max_damage) * 2
        else:
            damage = random.randint(1, enemy_max_damage)
        print("The %s deals %s damage!\n" % (opponent, damage))
        health -= damage
        character.set_health(health)
    return health


# generate sneak success randomly based on stealth skill and chance
def sneak(stage_num):
    randy = random.randint(1, stage_num)
    quiet = random.randint(0, 2)
    blind_luck = random.randint(0, 10)

    if (character.get_skill_level('stealth') > randy and quiet >= 2) or blind_luck > 9:
        return True
    else:
        return False


# generate item; 50-50 chance, followed by 1 in 3 chance
def itemDrop(stage_num):
    print("It appears the enemy dropped an item before disappearing into nothing.\n")
    time.sleep(0.5)
    if random.randint(0, 1) == 1:
        print("Turns out to be nothing.\n")
    else:
        print("You approach vicariously.\n")
        time.sleep(0.5)
        found = inventoryManagement.find_item(stage_num)
        if not found:
            print("Turns out it was nothing...\n")
