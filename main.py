import pygame
from src.game import Game
from src.mainmenu import MainMenu
from src.continuegame import ContinueGameMenu

def main():
    pygame.init()

    running = True
    while running:
        mainmenu = MainMenu()
        menu_action = mainmenu.run()

        if menu_action == "start":  
            game = Game()
            game.run()

        elif menu_action == "continue":
            continue_game_menu = ContinueGameMenu()
            continue_game_menu.run()

        elif menu_action == "exit":
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
