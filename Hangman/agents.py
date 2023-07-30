import pwinput
from variables import SECRET, SPACE_IN, SPACE_OUT
import random

class HangmanAgent():
    """
    A class used to play a game of Hangman

    ...

    Attributes
    ----------
    
    guesses_made : int
    
    num_guesses : int

    pattern : str

    secret_word : str


    Methods
    -------

    make_guess()

    is_terminal()

    start_game()

    """

    @property
    def pattern(self):
        return self._get_pattern(self.secret_word)
    
    @property
    def secret_word(self):
        return self._secret_word

    @property
    def guesses_made(self):
        return self._guesses_made.copy()

    @property
    def guesses_left(self):
        return self._guesses_left
    

    def __init__(self):
        pass

    def start_game(self):
        self._reset()
        f = open("dictionary.txt", "r", encoding="utf8")
        self._secret_word = self._choose_from_dict(f.read().splitlines())

    def _reset(self):
        self._guesses_left = 7
        self._guesses_made = []

    def _choose_from_dict(self, dict):
        return random.choice(dict)
    

    def _get_pattern(self, word):
        ret = ""
        for letter in word:
            if letter.lower() in self._guesses_made:
                ret += letter
            elif letter == SPACE_IN:
                ret += SPACE_OUT
            elif self._is_valid_guess(letter):
                ret += SECRET
            else:
                ret += letter

        return ret

    def _is_valid_guess(self, guess):
        return guess.isalpha()

    def _is_valid_letter(self, guess):
        return self._is_valid_guess(guess) or guess == SPACE_IN


    def make_guess(self):
        guess = self._input_guess()
        self._guesses_made.append(guess)
        self._guesses_made.sort()
        return self._test_guess(guess)

    def _input_guess(self):
        guess = None
        while True:
            try:
                guess = input("What is your next guess? ")
                guess = guess.lstrip().lower()
                if len(guess) != 1 or not self._is_valid_guess(guess):
                    raise ValueError
                
                if guess in self._guesses_made:
                    print("You already guessed that!")
                else:
                    break

            except Exception:
                print("Sorry, that is not a valid input")
        return guess
    
    def _test_guess(self, guess):
        if guess not in self.pattern:
            self._guesses_left -= 1
            return False
        return True
    
    
    def is_terminal(self):
        if self._guesses_left == 0:
            return True

        word = self.secret_word
        for w in word:
            if w != SPACE_IN and (self._is_valid_guess(w) and w.lower() not in self._guesses_made):
                return False

        return True



class EvilAgent(HangmanAgent):
    @property
    def pattern(self):
        return self._pattern

    @property
    def secret_word(self):
        return random.choice(self._secret_word)
    
    def __init__(self):
        pass

    def _reset(self):
        self._guesses_left = 14
        self._guesses_made = []
        self._pattern = ""
        self._secret_word = []
    
    def _choose_from_dict(self, dict):
        ret = []
        tmp = random.choice(dict)
        size = len(tmp)
        for word in dict:
            if len(word) == size:
                ret.append(word)
        
        self._pattern = self._get_pattern(tmp)
        return ret


    def _test_guess(self, guess):
        patterns = {}
        
        for word in self._secret_word:
            tmp = self._get_pattern(word).lower()
            if tmp not in patterns:
                patterns[tmp] = (0, set()) 

            freq, letc = patterns[tmp] 
            freq += 1

            for let in word:
                if let not in self._guesses_made:
                    letc.add(let)

            patterns[tmp] = freq, letc

        self._pattern = self._get_best_pattern(patterns, guess)
        new_dict = []
        for word in self._secret_word:
            if self.pattern == self._get_pattern(word):
                new_dict.append(word)
        self._secret_word = new_dict

        return super()._test_guess(guess)

    def _get_best_pattern(self, patterns, guess):
        maxkey = None
        maxfreq = -1
        for key in patterns:
            freq, _ = patterns[key]
            if freq > maxfreq:
                maxfreq = freq
                maxkey = key
            elif freq == maxfreq:
                if guess not in key:
                    maxfreq = freq
                    maxkey = key    

        return maxkey

class HelpAgent(EvilAgent):
    def __init__(self):
        super().__init__()

    def _reset(self):
        super()._reset()
        self._guesses_left = 4
    
    def _get_best_pattern(self, patterns, guess):
        maxlet = -1
        maxfreq = -1
        maxeasy = -1
        maxkey = None

        opt0 = False
        for key in patterns:
            freq, letc = patterns[key]

            easy = 0
            for k in key:
                if k == guess:
                    easy += 1

            opt1 = len(letc) > maxlet
            opt2 = len(letc) == maxlet and easy > maxeasy
            opt3 = len(letc) == maxlet and easy == maxeasy and freq > maxfreq 
            opt4 = SECRET not in key
            
            if opt4:
                return key

            if opt0 or opt1 or opt2 or opt3 or opt4:
                if opt0 or maxkey is None or guess in key:
                    # print("Winner!",opt0,opt1,opt2,opt3)
                    # print(key, freq, len(letc))

                    maxlet = len(letc)
                    maxfreq = freq
                    maxkey = key
                    maxeasy = easy

                    opt0 = easy == 0

        return maxkey
    
class PlayerAgent(HangmanAgent):
    def __init__(self):
        super().__init__()
    
    def _is_valid_guess(self, guess):
        if self._numeric:
            return guess.isalnum()
        else:
            return guess.isalpha()

    def _is_valid_letter(self, letter):
        return letter != SECRET and letter != SPACE_OUT 

    def start_game(self):
        self._reset()
        while True:
            tmp = pwinput.pwinput(prompt="Please enter the secret word: ",mask="*")
            valid = True
            numeric = False
            for c in tmp:
                valid &= self._is_valid_letter(c)
                numeric |= c.isalnum() and not c.isalpha()
            
            if not valid:
                print("Sorry, that secret word contained an illegal character.")
            else:
                self._secret_word = tmp
                if numeric:
                    y = input("Your secret word contained some numbers. Would you like these to be hidden? Type 'y' for yes, and anything else for no. ")
                    if y[0] == 'y' or y[0] == 'Y':
                        self._numeric = True
                break
        
        while True:
                try:
                    tmp = int(input("How many wrong guesses are allowed? "))
                    if tmp <= 0 or (tmp > 26 and not self._numeric) or (tmp > 36 and self._numeric):
                        raise ValueError
                    self._guesses_left = tmp
                    break 

                except ValueError:
                    print("Sorry, that is not a valid number of guesses.")

    def _reset(self):
        self._guesses_left = 0
        self._guesses_made = []
        self._numeric = False