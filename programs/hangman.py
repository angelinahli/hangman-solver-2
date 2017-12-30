import os
import random

from programs.vocabulary import sorted_words

class Hangman:

    TOTAL_LIVES = 7

    def __init__(self, word):
        self.word = word
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

    IMGS = {i: os.path.join("static", "img", "hangman{}.png".format(i)) \
        for i in range(1, 8)}

    def __init__(self, debug=False):
        Hangman.__init__(self, self._choose_random_word()) # fix
        
        # initialize word
        self.word_len = len(self.word)

        # user feedback vars
        self.message = ""
        self.errors = []
        self.img = ""
        self.debug = debug

    # --- helper methods --- #

    def _choose_random_word(self):
        # should really choose with weights somehow.
        list_key = random.choice(list(sorted_words.keys()))
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

class AutomaticHangman(Hangman):
    """
    Class will, given a word, simulate an automatic game of hangman
    """
    def __init__(self, word):
        Hangman.__init__(self, word)