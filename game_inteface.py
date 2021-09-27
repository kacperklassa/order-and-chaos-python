from order_and_chaos import Game
import argparse
import sys


def print_main_menu():
    print("""
    Welcome to Order and Chaos!
    Please choose a game mode before playing:
    1 - play with a friend against each other
    2 - play versus a bot which moves randomly
    3 - play versus a bot which makes deliberate moves
    4 - quit
    """)

def game_mode_choice():
    choice = input("> ")
    while choice not in {'1', '2', '3', '4'}:
        print("Please choose one of the valid options")
        choice = input("> ")
    return choice

def print_end_menu():
    print("Do you want to play again or quit? (1 to play again, 2 to quit)")
    choice = input("> ")
    if choice == '1':
        start_game()
    else:
        return

def start_game():
    print_main_menu()
    mode = game_mode_choice()
    order_and_chaos = Game()
    if mode == '1':
        order_and_chaos.play_pvp()
        print_end_menu()
    elif mode == '2':
        order_and_chaos.play_npc('random')
        print_end_menu()
    elif mode == '3':
        order_and_chaos.play_npc('notrandom')
        print_end_menu()
    else:
        return

def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument('--play_pvp', action='store_true')
    parser.add_argument('--play_bot_rand', action='store_true')
    parser.add_argument('--play_bot_ai', action='store_true')

    args = parser.parse_args(arguments[1:])

    order_and_chaos = Game()
    if args.play_pvp:
        order_and_chaos.play_pvp()
        print_end_menu()
    elif args.play_bot_rand:
        order_and_chaos.play_npc('random')
        print_end_menu()
    elif args.play_bot_ai:
        order_and_chaos.play_npc('best_move')
        print_end_menu()
    else:
        start_game()




if __name__ == "__main__":
    main(sys.argv)