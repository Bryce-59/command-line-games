from abc import ABC
import random

class Node:
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.children = []

    def __copy_board__(self):
        copy = []
        for r in self.board:
            copy_r = []
            for c in r:
                copy_r.append(c)
            copy.append(copy_r)
        return copy

    def generate_children(self):
        is_terminal, _ = self.is_terminal()
        if not is_terminal:
            child = None

            child_player = 'X' if self.player == 'O' else 'O'
            for r in range(3):
                for c in range(3):
                    
                    if self.board[r][c] == ' ':
                        tmp = self.__copy_board__()
                        tmp[r][c] = child_player

                        child = Node(tmp, child_player)
                        self.children.append(child)

    def get_board(self):
        return self.__copy_board__()
    
    def get_player(self):
        return self.player

    def print_board(self):
        print("  ", end="")
        for c in range(len(self.board[0])):
            print("  "+str(c+1), end=" ")
        print()
        print()

        for r in range(len(self.board)):
            print(" "+str(r+1), end=" ")
            for c in range(len(self.board[r])):
                print(" "+self.board[r][c], end=" ")
                if (c < len(self.board[r]) - 1):
                    print("|", end="")
            print()
            if (r < len(self.board) - 1):
                print("   ---+---+---")

    def is_terminal(self):
        p_tlbr = self.board[0][0]
        p_bltr = self.board[0][-1]

        diag_tlbr = p_tlbr != ' '
        diag_bltr = p_bltr != ' '
        for i in range(3):
            row = self.board[i][0] != ' ' and self.board[i][0] == self.board[i][1] and self.board[i][1] == self.board[i][2]
            col = self.board[0][i] != ' ' and self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i]            
            if row or col:
                return (True, self.board[i][0]) if row else (True, self.board[0][i])

            diag_tlbr &= self.board[i][i] == p_tlbr
            diag_bltr &= self.board[i][-(i+1)] == p_bltr

        if diag_tlbr or diag_bltr:
            return (True, p_tlbr) if diag_tlbr else (True, p_bltr)

        for r in self.board:
            if ' ' in r:
                return (False, None)
        
        return (True, None)

class Tree:
    def __init__(self):
        self.root = Node([[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], 'O')
        self.__generate_tree__(self.root)
        self.start_game()

    def __generate_tree__(self, root):
        if not root.is_terminal()[0]:
            root.generate_children()
            for tmp in root.children:
                self.__generate_tree__(tmp)

    def __tree_successor_helper__(self, state, player, win, lose, draw):
        is_terminal, winner = state.is_terminal()
        if is_terminal:
            if winner == None:
                return state, draw
            elif winner == player:
                return state, win
            else:
                return state, lose
            
        else:
            best = lose if self.state.get_player() == state.get_player() else win
            ret = None

            for child in state.children:
                _, score = self.__tree_successor_helper__(child, player, win, lose, draw)
                if self.state.get_player() != child.get_player():
                    if score == win:
                        return child, win
                    
                    if score >= best:
                        best = score
                        ret = child
                
                else:
                    if score == lose:
                        return child, lose
                    
                    if score <= best:
                        best = score
                        ret = child

            assert ret is not None
            return ret, best

    def tree_successor(self, player, win, lose, draw):
        return self.__tree_successor_helper__(self.state, player, win, lose, draw)[0].get_board()


    def get_state(self):
        return self.state.get_board()
    
    def get_winner(self):
        return self.state.is_terminal()[1]
    
    def go_to(self, next_state):
        for c in self.state.children:
            if c.get_board() == next_state:
                self.state = c
                return True
        return False

    def is_terminal(self):
        return self.state.is_terminal()[0]

    def print_board(self):
        self.state.print_board()

    def random_successor(self):
        return self.state.children[(random.randint(0, len(self.state.children) - 1))].get_board()

    def start_game(self):
        self.state = self.root

class Agent(ABC):
    # @abstractmethod
    def __init__(self, name, player):
        self.name = name
        self.player = player

    def get_name(self):
        return self.name
    
    def get_player(self):
        return self.player

    # @abstractmethod
    def select_move(self, board):
        pass

class MistakeAgent(Agent):
    def __init__(self, name, player):
        super().__init__(name, player)

    def select_move(self, game_state):
        if random.randint(1, 10) <= 8:
            return game_state.tree_successor(self.player, 10, 0, 0)
        else:
            return game_state.random_successor()

class UnbeatableAgent(Agent):
    def __init__(self, name, player):
        super().__init__(name, player)

    def select_move(self, game_state):
        return game_state.tree_successor(self.player, 10, -10, 0)

class RandomAgent(Agent):
    def __init__(self, name, player):
        super().__init__(name, player)
    
    def select_move(self, game_state):
        return game_state.random_successor()

class PlayerAgent(Agent):
    def __init__(self, name, player):
        super().__init__(name, player)

    def select_move(self, game_state):
        tmp = game_state.get_state()

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
            
            if tmp[row-1][col-1] != ' ':
                print("Sorry, that space has already been taken!")
                print()
            else:
                tmp[row-1][col-1] = self.player
                break

        return tmp

print("Welcome to the TicTacToe Player!")
print("Loading Game...")
game_tree = Tree()
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

    p1_turn = 'X' if num_players == 2 or random.randint(1, 2) == 1 else 'O'
    p2_turn = 'O' if p1_turn == 'X' else 'X'

    assert p1_turn != p2_turn

    p1 = PlayerAgent(p1_name, p1_turn)
    p2 = None
    if int(num_players) == 2:
        p2 = PlayerAgent(p2_name, p2_turn)
    elif int(num_players) == 1:
        if ai_level == 1:
            p2 = RandomAgent(p2_name, p2_turn)
        elif ai_level == 2:
            p2 = MistakeAgent(p2_name, p2_turn)
        elif ai_level == 3:
            p2 = UnbeatableAgent(p2_name, p2_turn)

    assert p2 is not None

    player_1 = p1 if p1.get_player() == 'X' else p2
    player_2 = p1 if p1.get_player() == 'O' else p2

    while not game_tree.is_terminal():
        print()
        print()
        
        game_tree.print_board()
        print()
        print(player_1.get_name()+", it is your turn!")
        game_tree.go_to(player_1.select_move(game_tree))

        if (game_tree.is_terminal()):
            break

        print()
        print()

        game_tree.print_board()
        print()
        print(player_2.get_name()+", it is your turn!")
        game_tree.go_to(player_2.select_move(game_tree))

    print()
    print()
    game_tree.print_board()
    print()

    if game_tree.get_winner() == 'X':
        print(player_1.get_name()+" wins!!")
    elif game_tree.get_winner() == 'O':
        print(player_2.get_name()+" wins!!")
    else:
        print("It is a tie.")

    print()

    y = input("Would you like to play again? Type 'y' for yes, and anything else for no.")
    if not (y[0] == 'y' or y[0] == 'Y'):
        break


    

        

        

        



