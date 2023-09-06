"""Command-Line TicTacToe

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

from agents import PlayerAgent, RandomAgent, FlawedAgent, UnbeatableAgent 
from variables import PLAYER_ONE, PLAYER_TWO, EMPTY_SPACE

class TicTacToe:
    """
    A class used to represent a game of TicTacToe.
    ...

    Attributes
    ----------
    
    board : list
        a representation of the game board as a 2D-list of symbols 

    Methods
    -------
    get_winner()
        Return the winner if the game is in a terminal state, else None.
    is_terminal()
        Return whether the game has reached a terminal state.
    print_board()
        Print a representation of the current game board to the output. 
    take_turn(player)
        Take in a player agent and progress to the state that  the player agent chooses.
    start_game()
        Reset the internal state. Must be called before a game can be played.
    """
    class _State:
        """
        A private inner class used to represent a single state of a TicTacToe game.
        ...

        Attributes
        ----------
        
        board : list
            a representation of the game board as a 2D-list of symbols 
        children : list
            the list of states that the current state can progress to
        is_terminal : bool
            whether the current state is a terminal state
        player : str
            the symbol that represents the player that should take the next turn
        winner : str or None
            the symbol that represents the player that won, if one exists
        Methods
        -------
        print_board()
            Print a representation of the current game board to the output. 
        """

        @property
        def board(self):
            """a representation of the game board as a 2D-list of symbols"""
            return [r[:] for r in self._board]
        
        @property
        def children(self):
            """the list of states that the current state can progress to"""
            ret = self._children.copy()
            random.shuffle(ret)
            return ret 
        
        @property
        def is_terminal(self):
            """whether the current state is a terminal state"""
            return self._win_state[0]

        @property
        def player(self):
            """the symbol that represents the player that should take the next turn"""
            return self._next_player

        @property
        def winner(self):
            """the symbol that represents the player that won, if one exists"""
            return self._win_state[1]

        def __init__(self, board, next_player):
            """
            Parameters
            ----------
            board : list
                The representation of the game board as a 2D-list of symbols
            next_player : str
                The symbol that represents the player that should take the next turn
            """
            self._board = board
            self._next_player = next_player
            self._children = []
            self._win_state = self._is_terminal()

        def __eq__(self, other):
            try:
                return self._board == other._board
            except:
                return False

        def _is_terminal(self):
            """Return whether the State represents the end of a game and the winner if True."""

            # Initialize values related to diagonals.
            p_neg = self._board[0][0]
            p_pos = self._board[0][-1]
            diag_neg = p_neg != EMPTY_SPACE
            diag_pos = p_pos != EMPTY_SPACE


            for i in range(3):
                # Initialize values related to the row and columns.
                p_row = self._board[i][0]
                p_col = self._board[0][i]
                row = p_row != EMPTY_SPACE
                col = p_col != EMPTY_SPACE

                # Test the row and column cases.
                for j in range(3):
                    row &= self._board[i][j] == p_row
                    col &= self._board[j][i] == p_col 
                if row or col:
                    return (True, p_row) if row else (True, p_col)

                # Test the diagonal cases.
                diag_neg &= self._board[i][i] == p_neg
                diag_pos &= self._board[i][-(i+1)] == p_pos
            if diag_neg or diag_pos:
                return (True, p_neg) if diag_neg else (True, p_pos)
            
            # Test whether a tie or a non-terminal State.
            return (not any(EMPTY_SPACE in r for r in self._board), None)

        def _generate_children(self):
            """Creates the list of game states that this State can progress to and adds them to self.children.
            
            Should only be run once.
            """
            if not self.is_terminal:

                child_player = PLAYER_ONE if self._next_player == PLAYER_TWO else PLAYER_TWO
                for r in range(3):
                    for c in range(3):
                        child_board = self.board

                        if child_board[r][c] == EMPTY_SPACE:
                            child_board[r][c] = self._next_player
                            child = TicTacToe._State(child_board, child_player)
                            if child not in self._children:
                                self._children.append(child)
            

        def print_board(self):
            """Print an ASCII portrayal of the TicTacToe State."""
            print("  ", end="")
            for c in range(len(self._board[0])):
                print("  "+str(c+1), end=" ")
            print()
            print()

            for r in range(len(self._board)):
                print(" "+str(r+1), end=" ")
                for c in range(len(self._board[r])):
                    print(" "+self._board[r][c], end=" ")
                    if (c < len(self._board[r]) - 1):
                        print("|", end="")
                print()
                if (r < len(self._board) - 1):
                    print("   ---+---+---")

    @property
    def board(self):
        """a representation of the game board as a 2D-list of symbols"""
        return self.state.board

    def __init__(self):
        self.root = TicTacToe._State(self._get_root(), PLAYER_ONE)
        self.start_game()
        self._generate_tree(self.root)

    def _generate_tree(self, node):
        """Recursively builds the subtree of States beginning with this State (node).
            
        In theory, the recursion depth should never exceed 9."""
        node._generate_children()
        for child in node._children:
            self._generate_tree(child)

    def _get_root(self):
        """Generates the root node as an entirely empty 3x3 board."""
        board = []
        for r in range(3):
            row = []
            for c in range(3):
                row.append(EMPTY_SPACE)
            board.append(row)

        return board
    
    def _will_tie(self, state):
        """Takes in a state and looks ahead to see if it is guaranteed to result in a tie."""
        ret = state.winner == None

        for child in state._children:
            ret &= self._will_tie(child)
            
            if not ret:
                return False

        return ret
    
    def get_winner(self):
        """If the current State (self.state) has a winner, return it. Else None."""
        return self.state.winner

    def is_terminal(self):
        """Return whether the current State (self.state) is a terminal state."""
        ret = self.state.is_terminal
        if ret or self._will_tie(self.state):
            return True
        return ret

    def print_board(self):
        """Print an ASCII portrayal of the TicTacToe State."""
        self.state.print_board()

    def take_turn(self, player):
        """take_turn(player)
        Take in a player agent and progress to the state that  the player agent chooses.
        """
        nxt = player.select_move(self.state)
        assert nxt != None and nxt in self.state._children
        self.state = nxt

    def start_game(self):
        """start_game()
        Reset the internal state. Must be called before a game can be played.
        """
        self.state = self.root

def _choose_ai(difficulty, name, turn):
    """Given a difficulty level (difficulty), return the appropriate Agent"""
    assert(difficulty > 0 and difficulty <= 3)

    ret = None
    if difficulty == 1:
        ret = RandomAgent(name, turn)
    elif difficulty == 2:
        ret = FlawedAgent(name, turn)
    elif difficulty == 3:
        ret = UnbeatableAgent(name, turn)
    return ret

def _ask_difficulty(message):
    """Receive the difficulty as a user input and return it"""
    ret = None
    while True:
        try:
            ret = int(input(message + " (Enter 1 for EASY, 2 for NORMAL, 3 for HARD): "))
            if ret <= 0 or ret > 3:
                raise ValueError
            break 
        except ValueError:
            print("Sorry, that is not a valid difficulty level.")

    return ret

global_tree = None
def create_tree():
    global global_tree
    global_tree = TicTacToe()

def main():
    print("Welcome to the TicTacToe Player!")
    print()

    game_tree = None
    t1 = threading.Thread(target=create_tree)
    t1.start()

    while True:
        num_players = 0
        while True:
            try:
                num_players = int(input("How many players? (Enter 1 or 2): "))
                if num_players < 0 or num_players > 2:
                    raise ValueError 
                break

            except ValueError:
                print("Sorry, that is not a valid number of players.")

        ai_level_bonus = 0
        ai_level = 0
        if num_players == 0: 
            print()
            print("You found the secret 0-player mode!")
            ai_level_bonus = _ask_difficulty("What level should the first CPU be?")
            ai_level = _ask_difficulty("What level should the second CPU be?")

        if num_players == 1:
            ai_level = _ask_difficulty("What level CPU do you want to play against?")

        assert num_players == 0 or num_players == 1 or num_players == 2
        assert ai_level >= 0 and ai_level <= 3

        p1_name = "Human" if num_players == 1 else "Player 1"
        p2_name = "CPU" if num_players == 1 else "Player 2"

        p1_name = "CPU_1" if num_players == 0 else p1_name
        p2_name = "CPU_2" if num_players == 0 else p2_name

        p1_turn = PLAYER_ONE # if num_players == 2 or random.randint(1, 2) == 1 else PLAYER_TWO
        p2_turn = PLAYER_TWO if p1_turn == PLAYER_ONE else PLAYER_ONE

        assert p1_turn != p2_turn

        p1 = PlayerAgent(p1_name, p1_turn)
        if num_players == 0:
            p1 = _choose_ai(ai_level_bonus, p1_name, p1_turn)

        p2 = None
        if num_players == 2:
            p2 = PlayerAgent(p2_name, p2_turn)
        else:
            p2 = _choose_ai(ai_level, p2_name, p2_turn)

        assert p2 is not None

        player_1 = p1 if p1.player == PLAYER_ONE else p2
        player_2 = p1 if p1.player == PLAYER_TWO else p2

        print("Loading Game...")
        if t1 is not None:
            if t1.is_alive():
                t1.join()
            
            game_tree = global_tree
            t1 = None
        game_tree.start_game()
        print("Done!")

        while not game_tree.is_terminal():
            print()
            print()
            
            game_tree.print_board()
            print()
            print(player_1.name+", it is your turn!")
            if not isinstance(player_1, PlayerAgent):
                time.sleep(2)

            game_tree.take_turn(player_1)

            if (game_tree.is_terminal()):
                break

            print()
            print()

            game_tree.print_board()
            print()
            print(player_2.name+", it is your turn!")
            if not isinstance(player_2, PlayerAgent):
                time.sleep(2)

            game_tree.take_turn(player_2)

        print()
        print()
        game_tree.print_board()
        print()

        if game_tree.get_winner() == PLAYER_ONE:
            print(player_1.name+" wins!!")
        elif game_tree.get_winner() == PLAYER_TWO:
            print(player_2.name+" wins!!")
        else:
            print("It is a tie.")

        print()

        y = input("Would you like to play again? Type 'y' for yes, and anything else for no. ")
        if not (y[0] == 'y' or y[0] == 'Y'):
            break

if __name__ == "__main__":
    main()