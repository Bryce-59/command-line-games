import unittest
from tictactoe import TicTacToe
from variables import PLAYER_ONE as x, PLAYER_TWO as o, EMPTY_SPACE as e
from agents import PlayerAgent, RandomAgent, FlawedAgent, UnbeatableAgent

test_game = TicTacToe()

ex0 = [[e,e,e],[e,e,e],[e,e,e]], x

ex00 = [[x,e,e],[e,e,e],[e,e,e]], o
ex01 = [[e,x,e],[e,e,e],[e,e,e]], o
ex02 = [[e,e,x],[e,e,e],[e,e,e]], o
ex03 = [[e,e,e],[x,e,e],[e,e,e]], o
ex04 = [[e,e,e],[e,x,e],[e,e,e]], o
ex05 = [[e,e,e],[e,e,x],[e,e,e]], o
ex06 = [[e,e,e],[e,e,e],[x,e,e]], o
ex07 = [[e,e,e],[e,e,e],[e,x,e]], o
ex08 = [[e,e,e],[e,e,e],[e,e,x]], o

ex000 = [[x,o,e],[e,e,e],[e,e,e]], x
ex001 = [[x,e,o],[e,e,e],[e,e,e]], x
ex002 = [[x,e,e],[o,e,e],[e,e,e]], x
ex003 = [[x,e,e],[e,o,e],[e,e,e]], x
ex004 = [[x,e,e],[e,e,o],[e,e,e]], x
ex005 = [[x,e,e],[e,e,e],[o,e,e]], x
ex006 = [[x,e,e],[e,e,e],[e,o,e]], x
ex007 = [[x,e,e],[e,e,e],[e,e,o]], x

ex1 = [[x,e,o],[e,x,o],[o,e,x]], x
ex2 = [[x,e,o],[e,x,o],[o,e,x]], x

ex1a = [[x,x,x],[o,e,o],[e,o,e]], x
ex2a = [[o,e,o],[x,x,x],[e,o,e]], x
ex3a = [[o,e,o],[e,o,e],[x,x,x]], x
ex4a = [[x,e,o],[x,o,e],[x,o,e]], x
ex5a = [[e,x,o],[o,x,e],[o,x,e]], x
ex6a = [[o,e,x],[e,o,x],[e,o,x]], x
ex7a = [[x,e,o],[e,x,o],[o,e,x]], x
ex8a = [[o,e,x],[e,x,o],[x,e,o]], x
ex1b = [[o,o,o],[x,e,x],[e,x,e]], x
ex2b = [[x,e,x],[o,o,o],[e,x,e]], x
ex3b = [[x,e,x],[e,x,e],[o,o,o]], x
ex4b = [[o,e,x],[o,x,e],[o,x,e]], x
ex5b = [[e,o,x],[x,o,e],[x,o,e]], x
ex6b = [[x,e,o],[e,x,o],[e,x,o]], x
ex7b = [[o,e,x],[e,o,x],[x,e,o]], x
ex8b = [[x,e,o],[e,o,x],[o,e,x]], x
ex9ab = [[o,x,x],[x,o,o],[o,x,x]], o

class TicTacToeStateTests(unittest.TestCase):

    def test__eq(self):
        # test that equivalent states are equal
        self.assertTrue(TicTacToe._State(ex0[0], ex0[1]) == TicTacToe._State(ex0[0], ex0[1]))
        self.assertTrue(TicTacToe._State(ex1[0], ex1[1]) == TicTacToe._State(ex2[0], ex2[1]))
        test = TicTacToe._State(ex0[0], ex0[1])
        self.assertEqual(test, test)

    def test_generate_children(self):
        # test that generate_children() creates the right children
        test = TicTacToe._State(ex0[0], ex0[1])
        self.assertTrue(len(test.get_children()) == 0)
        test.generate_children()
        self.assertTrue(len(test.get_children()) == 9)
        
        expected_out = [ex00[0], ex01[0], ex02[0], ex03[0], ex04[0], ex05[0], ex06[0], ex07[0], ex08[0]]
        for child in test.get_children():
            self.assertTrue(child.copy_board() in expected_out)

        test2 = TicTacToe._State(ex00[0], ex00[1])
        test2.generate_children()
        expected_out2 = [ex000[0], ex001[0], ex002[0], ex003[0], ex004[0], ex005[0], ex006[0], ex007[0]]
        for child in test2.get_children():
            self.assertTrue(child.copy_board() in expected_out2)
        # test that generate_children does not add redundant children if re-run
        test2.generate_children()
        self.assertTrue(len(test2.get_children()) == 8)

        # test that generate_children does not generate children for terminal states
        test3 = TicTacToe._State(ex2[0], ex2[1])
        test3.generate_children()
        expected_out3 = []
        self.assertTrue(len(test3.get_children()) == 0)
        for child in test3.get_children():
            self.assertTrue(child.copy_board() in expected_out3)

    def test_is_terminal(self):
        #test that is_terminal() and get_winner() return the correct output 
        #test when x is winner
        xlist = [ex1a, ex2a, ex3a, ex4a, ex5a, ex6a, ex7a, ex8a]
        for ex in xlist:
            test = TicTacToe._State(ex[0], ex[1])
            self.assertTrue(test.is_terminal())
            self.assertTrue(test.get_winner() == x)
            
        #test when o is winner
        olist = [ex1b, ex2b, ex3b, ex4b, ex5b, ex6b, ex7b, ex8b]
        for ex in olist:
            test = TicTacToe._State(ex[0], ex[1])
            self.assertTrue(test.is_terminal())
            self.assertTrue(test.get_winner() == o)

        # test tie state
        tie = TicTacToe._State(ex9ab[0], ex9ab[1])
        self.assertTrue(tie.is_terminal())
        self.assertTrue(tie.get_winner() == None)

        # test non-terminal states
        elist = [ex000, ex001, ex002, ex003, ex004, ex005, ex006, ex007]
        for ex in elist:
            test = TicTacToe._State(ex[0], ex[1])
            self.assertFalse(test.is_terminal())
            self.assertTrue(test.get_winner() == None)

    def test_get_player(self):
        #test that get_player() works as intended
        test = TicTacToe._State(ex0[0], ex0[1])
        self.assertTrue(test.get_player() == ex0[1])
        test.generate_children()
        for child in test.get_children():
            self.assertTrue(child.get_player() == o if ex0[1] == x else x)

        self.assertTrue(TicTacToe._State(ex9ab[0], ex9ab[1]).get_player() == ex9ab[1])

    def test_copy_board(self):
        #test that copy_board() works as intended
        xlist = [ex1a, ex2a, ex3a, ex4a, ex5a, ex6a, ex7a, ex8a]
        for ex in xlist:
            test = TicTacToe._State(ex[0], ex[1])
            self.assertEqual(test.copy_board(), ex[0])

ex10 = ([[x,o,x],[e,e,e],[x,o,e]], o)
ex10a = ([[x,o,x],[o,e,e],[x,o,e]], x)
ex10aa = ([[x,o,x],[o,x,e],[x,o,e]], o)
ex10ab = ([[x,o,x],[o,e,x],[x,o,e]], o)
ex10b = ([[x,o,x],[e,o,e],[x,o,e]], x)

class UnbeatableAgentTests(unittest.TestCase):
    # the unbeatable agent should use a minmax tree to optimize its play
    def test_basic(self):
        # test 0: basic functionality
        player_1 = UnbeatableAgent("1",x)
        self.assertTrue(player_1.get_name() == "1")
        self.assertTrue(player_1.get_player() == x)

    def test_theoretical(self):
        # test 1: see that the unbeatable agents minmax operation functions
        player_1 = UnbeatableAgent("2",o)

        sub_state = TicTacToe._State(ex10a[0], ex10a[1])
        sub_state.add_child(TicTacToe._State(ex10aa[0], ex10aa[1]))
        sub_state.add_child(TicTacToe._State(ex10ab[0], ex10ab[1]))
        test_state = TicTacToe._State(ex10[0], ex10[1])
        test_state.add_child(sub_state)
        test_state.add_child(TicTacToe._State(ex10b[0], ex10b[1]))

        output = player_1.select_move(test_state)
        self.assertEqual(output.copy_board(),ex10b[0])
    
    def test_practical(self):
        # test 2: an unbeatable agent should never lose to another agent
        loss = 0

        player_1 = UnbeatableAgent("1",x)
        player_2 = UnbeatableAgent("2",o)
        for i in range(20):
            
            test_game.start_game()
            while not test_game.is_terminal():
                test_game.take_turn(player_1)
                if (test_game.is_terminal()):
                    break
                test_game.take_turn(player_2)
        
            if test_game.get_winner() is not None:
                loss += 1

        self.assertTrue(loss == 0)

if __name__ == "__main__":
    unittest.main()