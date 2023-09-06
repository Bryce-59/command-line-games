"""Command-Line TicTacToe Agents

This file includes the agents which manage each game of TicTacToe.

There are four agents which can be imported to other files: 
    -UnbeatableAgent, which plays optimally for all states;
    -FlawedAgent, which plays sub-optimally and may occassionally play randomly;
    -RandomAgent, which plays randomly for all states;
    -PlayerAgent, which is controlled by a user.
"""

from abc import ABC, abstractmethod
import random
from variables import EMPTY_SPACE

class Agent(ABC):
    """
    An abstract method used to implement a TicTacToe Agent

    ...

    Attributes
    ----------
    
    name : str
        the string associated with this agent's ID 

    player : str
        the symbol that represents this agent on the board


    Methods
    -------

    select_move(board)
        Takes in a game state (board) and returns the child state that the game should progress to.

    """
        
    @property
    def name(self):
        """the string associated with this agent's ID"""
        return self._name
    
    @property
    def player(self):
        """the symbol that represents this agent on the board"""
        return self._player

    @abstractmethod
    def __init__(self, name, player):
        """
        Parameters
        ----------
        name : str
            The string associated with this agent's ID
        player : str
            The symbol that represents this agent on the board
        """
        self._name = name
        self._player = player
    
    def _choose_successor(self, game_state, win=0, lose=0, draw=0):
        """
        Take in a game state (game_state) and the most optimal child. 
        
        Take a win value, lose value, and draw value, and return a child state that
        is optimal according to these values. Makes the assumption that both agents
        use the same values.
        """
        if win == lose and lose == draw:
            return random.choice(game_state.children)
        
        assert win is not None and lose is not None and draw is not None
        return self._run_min_max(game_state, win, lose, draw)[0]
        
    def _run_min_max(self, game_state, win, lose, draw):
        """
        Run the min-max algorithm.
         
        Takes in a game state (game_state) and returns an optimal child
        according to the values of (win), (lose), and (draw).
        """
        is_terminal = game_state.is_terminal
        winner = game_state.winner
        children = game_state.children
        if is_terminal or len(children) == 0:
            if winner == None:
                return game_state, draw
            elif winner == self.player:
                return game_state, win
            else:
                return game_state, lose
            
        else:
            best = lose if self.player == game_state.player else win
            ret = None

            max_score = max(win, max(lose, draw))
            min_score = min(win, min(lose, draw))

            for child in children:
                _, score = self._run_min_max(child, win, lose, draw)
                if self.player != child.player:
                    # MAX
                    if score == max_score:
                        return child, max_score
                    
                    if score >= best:
                        best = score
                        ret = child
                
                else:
                    # MIN
                    if score == min_score:
                        return child, min_score
                    
                    if score <= best:
                        best = score
                        ret = child

            assert ret is not None
            return ret, best

    @abstractmethod
    def select_move(self, board):
        """Takes in a game state (board) and returns the child state that the game should progress to."""
        pass

class UnbeatableAgent(Agent):
    def __init__(self, name, player):
        super().__init__(name, player)

    def select_move(self, game_state):
        """Takes in a game state (board) and returns the child state that the game should progress to.
        
        Plays optimally.
        """
        return super()._choose_successor(game_state, 1, -1, 0)
    
class FlawedAgent(Agent):
    def __init__(self, name, player):
        super().__init__(name, player)

    def select_move(self, game_state):
        """Takes in a game state (board) and returns the child state that the game should progress to.

        Plays sub-optimally 80% of the time (sub-optimal is defined as being unable to distinguish between
        a loss and a tie), and randomly 20% of the time.
        """
        if random.randint(1, 10) <= 8:
            return super()._choose_successor(game_state, 1, 0, 0)
        else:
            return super()._choose_successor(game_state)

class RandomAgent(Agent):
    def __init__(self, name, player):
        super().__init__(name, player)
    
    def select_move(self, game_state):
        """Takes in a game state (board) and returns the child state that the game should progress to.

        Plays randomly.
        """
        return super()._choose_successor(game_state)

class PlayerAgent(Agent):
    def __init__(self, name, player):
        super().__init__(name, player)

    def select_move(self, game_state):
        """Takes in a game state (board) and returns the child state that the game should progress to.

        Choices are dictated by user input.
        """
        tmp = game_state.board

        while True:
            col = 0
            while True:
                try:
                    col = int(input("Select a column: "))
                    if col <= 0 or col > len(tmp[0]):
                        raise ValueError
                    break
                except ValueError:
                    print("Sorry, "+str(col)+" is not a valid column")
                    print()

            row = 0
            while True:
                try:
                    tmp_row = input("Select a row: ")
                    row = int(tmp_row)
                    if row <= 0 or row > len(tmp):
                        raise ValueError
                    break
                except ValueError:
                    print("Sorry, "+str(row)+" is not a valid row")
                    print()
            
            if tmp[row-1][col-1] != EMPTY_SPACE:
                print("Sorry, that space has already been taken!")
                print()
            else:
                tmp[row-1][col-1] = self.player
                break

        for child in game_state.children:
            if tmp == child.board:
                return child
        
        print("Sorry, there was a problem")
        return None