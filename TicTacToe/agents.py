from abc import ABC, abstractmethod
import random
from variables import EMPTY_SPACE

class Agent(ABC):
    @abstractmethod
    def __init__(self, name, player):
        self._name = name
        self._player = player
    
    def _choose_successor(self, game_state, win=None, lose=None, draw=None):
        if win == lose and lose == draw:
            return random.choice(game_state.children)
        
        assert win is not None and lose is not None and draw is not None
        return self._run_min_max(game_state, win, lose, draw)[0]
        
    def _run_min_max(self, game_state, win, lose, draw):
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

            for child in children:
                _, score = self._run_min_max(child, win, lose, draw)
                if self.player != child.player:
                    # MAX
                    if score == win:
                        return child, win
                    
                    if score >= best:
                        best = score
                        ret = child
                
                else:
                    # MIN
                    if score == lose:
                        return child, lose
                    
                    if score <= best:
                        best = score
                        ret = child

            assert ret is not None
            return ret, best


    @property
    def name(self):
        return self._name
    
    @property
    def player(self):
        return self._player

    @abstractmethod
    def select_move(self, board):
        pass

class UnbeatableAgent(Agent):
    def __init__(self, name, player):
        super().__init__(name, player)

    def select_move(self, game_state):
        return super()._choose_successor(game_state, 1, -1, 0)
    
class FlawedAgent(Agent):
    def __init__(self, name, player):
        super().__init__(name, player)

    def select_move(self, game_state):
        if random.randint(1, 10) <= 8:
            return super()._choose_successor(game_state, 1, 0, 0)
        else:
            return super()._choose_successor(game_state)

class RandomAgent(Agent):
    def __init__(self, name, player):
        super().__init__(name, player)
    
    def select_move(self, game_state):
        return super()._choose_successor(game_state)

class PlayerAgent(Agent):
    def __init__(self, name, player):
        super().__init__(name, player)

    def select_move(self, game_state):
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
                    row = int(input("Select a row: "))
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