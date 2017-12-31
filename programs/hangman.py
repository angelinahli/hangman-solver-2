import os
import random

from programs.solver import Solver
from programs.vocabulary import sorted_words

class Hangman:

    TOTAL_LIVES = 6

    def __init__(self, word):
        self.word = word.lower()
        self.len_word_set = len(set(self.word))
        self.guessed_chars = {"correct": [], "wrong": []}
        self.lives_used = 0
        self.lost = False
        self.won = False

    # --- helper methods --- #

    def _has_lost(self):
        return self.lives_used >= self.TOTAL_LIVES

    def _check_lost(self):
        if self._has_lost():
            self.lost = True

    def _has_won(self):
        return len(self.guessed_chars.get("correct")) == self.len_word_set

    def _check_won(self):
        if self._has_won():
            self.won = True

    # --- main methods --- #

    def guess_char(self, char):
        # message resets each time

        if char in self.word:
            self.guessed_chars["correct"].append(char)
        else:
            self.guessed_chars["wrong"].append(char)
            self.lives_used += 1

        self._check_lost()
        self._check_won()

class InteractiveHangman(Hangman):

    IMGS = {i: os.path.join("static", "img", "hangman{}.png".format(i + 1)) \
        for i in range(1, Hangman.TOTAL_LIVES + 1)}

    def __init__(self, user, debug=False):
        Hangman.__init__(self, self._choose_random_word()) # fix
        
        # user = user's ip address.
        self.user = user

        # initialize word
        self.word_len = len(self.word)

        # user feedback vars
        self.message = ""
        self.errors = []
        self.img = os.path.join("static", "img", "hangman1.png")
        self.debug = debug

    # --- helper methods --- #

    def _choose_random_word(self):
        list_key = random.choices(
            list(sorted_words.keys()), 
            weights=[len(val) for val in sorted_words.values()],
            k=1)[0]
        return random.choice(sorted_words[list_key])

    def _check_errors(self, char):
        errors = []
        if not char.isalpha():
            errors.append("Please enter a character from A-Z.")
        if len(char) > 1:
            errors.append("Please enter one character guess at a time.")
        if char in self.guessed_chars["correct"] or \
                char in self.guessed_chars["wrong"]:
            errors.append("You've already guessed this character!")

        self.errors = errors

    def _check_valid_guess(self, char):
        self._check_errors(char)
        return len(self.errors) == 0

    def _get_check_char(self, char):
        """return a char to use to test validity and to play the game"""
        return char.lower().strip()

    # --- public methods --- #

    def get_current_guess(self):
        current_word = []
        for c in self.word:
            if c in self.guessed_chars["correct"]:
                current_word.append(c)
            else:
                current_word.append("_")
        return "".join(current_word)

    def get_lives_left(self):
        return self.TOTAL_LIVES - self.lives_used

    def get_correct_guesses(self):
        return ", ".join(sorted(self.guessed_chars["correct"]))

    def get_wrong_guesses(self):
        return ", ".join(sorted(self.guessed_chars["wrong"]))

    def guess_char(self, char):
        # message and errors reset each time
        self.errors = []
        self.message = ""
        check_char = self._get_check_char(char)
        valid_guess = self._check_valid_guess(check_char)

        if valid_guess:
            if check_char in self.word:
                self.guessed_chars["correct"].append(check_char)
                self.message = "Good guess!"
            else:
                self.guessed_chars["wrong"].append(check_char)
                self.message = "Sorry, try again."
                self.lives_used += 1
                self.img = self.IMGS.get(self.lives_used)

            self._check_lost()
            self._check_won()

        if self.debug:
            print("Guess:", char, check_char)
            print("Valid guess:", valid_guess)
            print("Message:", self.message)
            print("Guessed chars:", self.guessed_chars)
            print("Current guess:", self.get_current_guess())

class SimulateHangman:
    """
    Represents an object that will, given a word,
    simulate an automatic game of hangman against the Solver algorithm
    """
    def __init__(self):
        self.errors = []
        self.game = None

    # --- helper methods --- #

    def _get_current_guess(self):
        current_word = []
        for c in self.game.word:
            if c in self.game.guessed_chars["correct"]:
                current_word.append(c)
            else:
                current_word.append(Solver.UNKNOWN)
        return "".join(current_word)

    def _simulate_one_step(self):
        solver = Solver(self._get_current_guess(), self.game.guessed_chars["wrong"])
        next_char = solver.get_next_guess()
        if next_char != "N/A":
            self.game.guess_char(next_char)
        return next_char

    def _simulate_game(self):
        invalid_next_char = False
        # to prevent infinite loop in the case where the word is not in our corpus
        while(not self.game.won and not invalid_next_char):
            next_char = self._simulate_one_step()
            if next_char == "N/A":
                invalid_next_char = True
        if invalid_next_char:
            self.errors.append("I don't recognize this word. Sorry!")

    # --- main methods --- #

    def simulate(self, word):
        # re initialize errors
        self.errors = []
        self.game = Hangman(word)
        self._simulate_game()

    def get_wrong_tries(self):
        return len(self.game.guessed_chars.get("wrong"))

class StatsHangman(SimulateHangman):
    """
    Represents an object that will, given a word,
    generate summary statistics about an automatic game of hangman played using
    that word and the Solver algorithm
    """

    # unusual characters are defined as characters in the last quartile of 
    # frequency usage, taken from:
    # https://en.oxforddictionaries.com/explore/which-letters-are-used-most
    UNUSUAL_CHARS = "wkvxzjq"

    def __init__(self):
        SimulateHangman.__init()

    # --- helper methods --- #

    def _contain_unusual_chars(self, word):
        for char in self.UNUSUAL_CHARS:
            if char in word:
                return True
        return False

    # --- main methods --- #

    def get_summary_statistics(self, word):
        self.simulate(word)
        return {
            "word": word,
            "num_wrong": self.get_wrong_tries(),
            "word_length": len(word),
            "contain_unusual_chars": self._contain_unusual_chars(word)
        }
