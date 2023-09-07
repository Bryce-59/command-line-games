"""Command-Line Hangman

This script allows the user to play a game of Hangman.

There are four modes available: Normal Mode, Easy Mode, Hard Mode, and Two-Player.
Normal Mode represents an average game of Hangman. In Easy Mode and Hard Mode,
the game manager will choose a word based on the user's guesses to make the game
easier or harder. In Two-Player, a human will enter the secret word and the user
must guess it.

This file contains the following functions:
    * main - the main function of the script, which activates the game
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../hangman")
import agents

def main():
    print("Welcome to the Hangman Player!")

    while True:
        num_players = 0
        while True:
            try:
                num_players = int(input("How many players? (Enter 1 or 2): "))
                if num_players <= 0 or num_players > 2:
                    raise ValueError 
                break

            except ValueError:
                print("Sorry, that is not a valid number of players.")

        ai_level = 0
        if num_players == 1:
            while True:
                try:
                    ai_level = int(input("What level CPU do you want to play against? (Enter 1 for EASY, 2 for NORMAL, 3 for HARD): "))
                    if ai_level <= 0 or ai_level > 3:
                        raise ValueError
                    break 

                except ValueError:
                    print("Sorry, that is not a valid difficulty level.")

        assert num_players == 1 or num_players == 2
        assert ai_level >= 0 and ai_level <= 3

        game_agent = None
        if int(num_players) == 2:
            game_agent = agents.PlayerAgent()
        elif int(num_players) == 1:
            if ai_level == 1:
                game_agent = agents.HelpAgent()
            elif ai_level == 2:
                game_agent = agents.HangmanAgent()
            elif ai_level == 3:
                game_agent = agents.EvilAgent()

        assert game_agent is not None
        
        game_agent.start_game()
        while not game_agent.is_terminal():
            print()
            print()
            print("guesses left:",game_agent.guesses_left)
            print("guessed so far :",game_agent.guesses_made)
            print("current word :",game_agent.pattern)
            
            game_agent.make_guess()

        print()

        if game_agent.guesses_left > 0:
            print("You win!!")
        else:
            print("You lost.")

        print("The word was "+game_agent.secret_word+".")

        print()

        y = input("Would you like to play again? Type 'y' for yes, and anything else for no. ")
        if not (y[0] == 'y' or y[0] == 'Y'):
            break

if __name__ == "__main__":
    main()