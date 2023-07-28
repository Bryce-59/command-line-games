import random
import time
from variables import PLAYER_ONE, PLAYER_TWO, EMPTY_SPACE
from agents import PlayerAgent, RandomAgent, FlawedAgent, UnbeatableAgent 


class TicTacToe:
    class _State:

        def __init__(self, board, next_player):
            self._board = board
            self._next_player = next_player
            self._children = []

            self._generate_children()

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
            """Recursively builds the subtree of States beginning with this State.
            
            In theory, the recursion depth should never exceed 9."""

            if not self.is_terminal():

                child_player = PLAYER_ONE if self._next_player == PLAYER_TWO else PLAYER_TWO
                for r in range(3):
                    for c in range(3):
                        child_board = self.copy_board()

                        if child_board[r][c] == EMPTY_SPACE:
                            child_board[r][c] = self._next_player
                            child = TicTacToe._State(child_board, child_player)
                            self._children.append(child)

                random.shuffle(self._children)
        
        def copy_board(self):
            """Create a copy of the State board. 
            
            The original State board should never be accessed from the outside."""
            return [r[:] for r in self._board]
        
        def get_children(self):
            return self._children
        
        def get_player(self):
            return self._next_player
        
        def get_winner(self):
            return self._is_terminal()[1]
        
        def is_terminal(self):
            return self._is_terminal()[0]
            

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

    def __init__(self):
        self.root = TicTacToe._State(self._get_root(), PLAYER_ONE)
        self.start_game()

    def _get_root(self):
        board = []
        for r in range(3):
            row = []
            for c in range(3):
                row.append(EMPTY_SPACE)
            board.append(row)

        return board
    
    def _will_tie(self, state):
        ret = state.get_winner() == None

        for child in state.get_children():
            ret &= self._will_tie(child)
            
            if not ret:
                return False

        return ret
        
    def get_state(self):
        return self.state.copy_board()
    
    def get_winner(self):
        return self.state.get_winner()

    def is_terminal(self):
        ret = self.state.is_terminal()
        if ret or self._will_tie(self.state):
            return True
        return ret

    def print_board(self):
        self.state.print_board()

    def take_turn(self, player):
        nxt = player.select_move(self.state)
        assert nxt != None and nxt in self.state.get_children()
        self.state = nxt

    def start_game(self):
        self.state = self.root

def _start():
    pass

def main():
    print("Welcome to the TicTacToe Player!")
    print("Loading Game...")
    game_tree = TicTacToe()
    print("Done!")
    print()

    while True:
        game_tree.start_game()
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

        p1_name = "Human" if num_players == 1 else "Player 1"
        p2_name = "CPU" if num_players == 1 else "Player 2"

        p1_turn = PLAYER_ONE # if num_players == 2 or random.randint(1, 2) == 1 else PLAYER_TWO
        p2_turn = PLAYER_TWO if p1_turn == PLAYER_ONE else PLAYER_ONE

        assert p1_turn != p2_turn

        p1 = PlayerAgent(p1_name, p1_turn)
        p2 = None
        if int(num_players) == 2:
            p2 = PlayerAgent(p2_name, p2_turn)
        elif int(num_players) == 1:
            if ai_level == 1:
                p2 = RandomAgent(p2_name, p2_turn)
            elif ai_level == 2:
                p2 = FlawedAgent(p2_name, p2_turn)
            elif ai_level == 3:
                p2 = UnbeatableAgent(p2_name, p2_turn)

        assert p2 is not None

        player_1 = p1 if p1.get_player() == PLAYER_ONE else p2
        player_2 = p1 if p1.get_player() == PLAYER_TWO else p2

        while not game_tree.is_terminal():
            print()
            print()
            
            game_tree.print_board()
            print()
            print(player_1.get_name()+", it is your turn!")
            if not isinstance(player_1, PlayerAgent):
                time.sleep(2)

            game_tree.take_turn(player_1)

            if (game_tree.is_terminal()):
                break

            print()
            print()

            game_tree.print_board()
            print()
            print(player_2.get_name()+", it is your turn!")
            if not isinstance(player_2, PlayerAgent):
                time.sleep(2)

            game_tree.take_turn(player_2)

        print()
        print()
        game_tree.print_board()
        print()

        if game_tree.get_winner() == PLAYER_ONE:
            print(player_1.get_name()+" wins!!")
        elif game_tree.get_winner() == PLAYER_TWO:
            print(player_2.get_name()+" wins!!")
        else:
            print("It is a tie.")

        print()

        y = input("Would you like to play again? Type 'y' for yes, and anything else for no. ")
        if not (y[0] == 'y' or y[0] == 'Y'):
            break

if __name__ == "__main__":
    main()