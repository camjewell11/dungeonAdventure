import character, config, environment, game, IO

# loop for main menu; character selection/creation, settings, and play
def start():
    while True:
        IO.printMainMenu()

        selection = input("\n")
        selection = selection.lower()
        IO.print_dash(True)
        if selection == '1':
            character.create_character()
        elif selection == '2':
            character.select_character()
        elif selection == '3':
            game.play_game()
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

# secret menu to test functionality without having to play the game
def debug_menu():
    while True:
        IO.printDebugMenu()

        selection = input("\n").lower()
        IO.print_dash(True)
        if selection == 'i':
            IO.display_info()
        elif selection == 'u':
            character.level_up()
        elif selection == 'e':
            print (config.enemy_table)
        elif selection == 'x':
            num = IO.getIntFromUser("How much XP would you like to add?\n")
            character.add_xp(num)
            print ("Total XP now:            %s\n" % character.get_xp())
        elif selection == 'k':
            character.died()
        elif selection == 'm':
            num = IO.getIntFromUser("Enter a Stage number.\n")
            environment.generate_floor(num)
            environment.print_floor()
        elif selection == 'q':
            break
        else:
            print (config.invalidResponse)

# If this is run as a script.
if __name__ == '__main__':
    environment.setupDirectories()

    print ("Welcome to Cam's Prototype game!\n")
    start()