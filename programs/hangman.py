import random

# from data.hangman_images import images

class HangmanGame(object):

    # IMGS = {i + 1: img.split("\n") for i, img in enumerate(images)}
    TOTAL_LIVES = 5 # len(list(IMGS.keys()))

    def __init__(self, debug=False):
        # initialize word
        self.word = "goldilocks" # fix
        self.word_len = len(self.word)

        # game control vars
        self.guessed_chars = {"correct": [], "wrong": []}
        self.lives_used = 0
        self.lost = False
        self.won = False

        # user feedback vars
        self.message = ""
        self.errors = []
        # self.img = []
        self.debug = debug

    # --- helper methods --- #

    def _check_errors(self, char):
        not_alpha = not char.isalpha()
        not_single_char = len(char) > 1
        not_new_guess = char in self.guessed_chars["correct"] or \
            char in self.guessed_chars["wrong"]
        errors = {
            not_alpha: "Please enter a character from A-Z.",
            not_single_char: "Please enter one character guess at a time.",
            not_new_guess: "You've already guessed this character!"
        }
        self.errors = [msg for error, msg in errors.items() if error]

    def _check_valid_guess(self, char):
        self._check_errors(char)
        return len(self.errors) == 0

    def _check_lost(self):
        if self.lives_used >= self.TOTAL_LIVES:
            self.lost = True

    def _check_won(self):
        if len(self.guessed_chars.get("correct")) == len(set(self.word)):
            self.won = True

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
        # message resets each time
        self.message = ""
        check_char = char.lower()
        valid_guess = self._check_valid_guess(check_char)

        if valid_guess:
            if check_char in self.word:
                self.message = "Good guess!"
                self.guessed_chars["correct"].append(check_char)
            else:
                self.message = "Sorry, try again."
                self.guessed_chars["wrong"].append(check_char)
                self.lives_used += 1
            
            # self.img = self.IMGS.get(self.num_tries)
            self._check_lost()
            self._check_won()

        if self.debug:
            print("Guess:", char, check_char)
            print("Valid guess:", valid_guess)
            print("Message:", self.message)
            print("Guessed chars:", self.guessed_chars)
            print("Current guess:", self.get_current_guess())
            