"""Command-Line UI

This script allows the user to play a game of TicTacToe.

The user can play against three levels of rudimentary 
Artificial Intelligence or against a human player. 

This file contains the following classes:
    * TicTacToe - a class that represents the a game of TicTacToe
    and keeps track of the current game's state

This file contains the following functions:
    * main - the main function of the script, which activates the game
"""

import random
import threading
import time

import sys
import os
import tictactoe.tictactoe as tictactoe
import hangman.hangman as hangman

TITLE = """
                     _        _ _                                              
                    | |      | (_)                                             
   ___ _ __ ___   __| |______| |_ _ __   ___    __ _  __ _ _ __ ___   ___  ___ 
  / __| '_ ` _ \ / _` |______| | | '_ \ / _ \  / _` |/ _` | '_ ` _ \ / _ \/ __|
 | (__| | | | | | (_| |      | | | | | |  __/ | (_| | (_| | | | | | |  __/\__ \\
  \___|_| |_| |_|\__,_|      |_|_|_| |_|\___|  \__, |\__,_|_| |_| |_|\___||___/
                                                __/ |                          
                                               |___/                           
"""

def main():
    print(TITLE)
    print("Welcome to the Command Line Game Collection!")
    while (True):
        print("What would you like to play?")
        print("(0) Tic Tac Toe")
        print("(1) Hangman")
        print("(x) Exit Command Line Game Collection")
        user = input("Enter your choice now: ").lstrip()
        print(".")
        print(".")
        print(".")
        if user.isdecimal():
            if (int(user) == 0):
                tictactoe.main()
            elif(int(user) == 1):
                hangman.main()
            print("Welcome back!")
        elif user == 'x':
            break

if __name__ == "__main__":
    main()