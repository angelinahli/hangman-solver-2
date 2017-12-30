import re
from collections import Counter

from programs.vocabulary import sorted_words

class Solver:
    """
    Solver class: Has the ability to solve one word.
    """

    UNKNOWN = "?"

    def __init__(self, word, wrong_chars):
        """
        word is in format 'p??ho?'
        wrong_chars = list of wrong characters
        """
        self.word = word
        self.wrong_chars = wrong_chars
        self.candidate_words = self._get_candidate_words()
        self.count_chars = self._get_count_chars()

    # --- helper methods --- #

    def _all_known_chars_match(self, candidate_word):
        """
        Will return whether the known characters in self.word match the
        corresponding indices of the candidate word
        """
        for i, char in enumerate(self.word):
            if char != self.UNKNOWN and char != candidate_word[i]:
                return False
        return True

    def _contains_no_wrong_chars(self, candidate_word):
        """
        Will return whether any of the characters in the candidate_word are
        known to be wrong.
        """
        for char in self.wrong_chars:
            if char in candidate_word:
                return False
        return True

    def _get_candidate_words(self):
        """
        Returns a list of words:
        * that have the same length as self.word
        * whose characters match the known characters in self.word
        * that do not contain any characters known to be wrong
        """
        candidate_words = []
        # start with words of same length
        matching_lengths = sorted_words.get(len(self.word), [])

        for word in matching_lengths:
            if self._all_known_chars_match(word) and \
                    self._contains_no_wrong_chars(word):
                candidate_words.append(word)
        return candidate_words

    def _get_count_chars(self):
        """
        Returns a Counter object containing counts of all unguessed chars in
        candidate words.
        """
        count_chars = Counter()
        for word in self.candidate_words:
            # implicitly weights chars that show up more often in words greater
            # (i.e. a char that shows up two times will be double counted)
            unguessed_chars = filter(lambda c: c not in self.word, word)
            for char in unguessed_chars:
                count_chars[char] += 1
        return count_chars

    # --- public/user facing methods --- #

    def get_next_guess(self):
        return self.count_chars.most_common(1)[0][0] # 1st el of 1st tup

    def get_top_chars(self, n=5):
        """
        Return list of top characters to guess in order
        """
        return [char_tup[0] for char_tup in self.count_chars.most_common(n)]

    def get_possible_words(self):
        return self.candidate_words

class InteractiveSolver:
    """
    Instead of checking one word, will check words when they are given to it.
    Contains a solver
    """

    UNKNOWN = "?"
    WORD_EXAMPLE = "py?t?n"

    def __init__(self):
        self.errors = []
        self.word_errors = []
        self.solver = None

    # --- helper methods --- #

    def _check_word_errors(self, word):
        errors = []
        for char in word:
            if not char.isalpha() and char != Solver.UNKNOWN:
                msg = ("Please enter only characters from A-Z and the " + 
                    "symbol {unknown} for unknown chars. e.g. {ex}").format(
                        unknown=Solver.UNKNOWN,
                        ex=self.WORD_EXAMPLE)
                errors.append(msg)
                break
        self.word_errors = errors

    def _is_valid_word(self, word):
        self._check_word_errors(word)
        return len(self.word_errors) == 0

    def _get_check_word(self, word):
        return word.lower().strip()

    def _get_check_wrong_chars(self, wrong_chars):
        # non alpha numeric
        return list(set(re.sub("", "", wrong_chars).lower()))

    # --- public/user facing methods --- #

    def solve(self, word, wrong_chars):
        # 'resets' the solver
        self.solver = None
        check_word = self._get_check_word(word)
        check_wrong_chars = self._get_check_wrong_chars(wrong_chars)
        if self._is_valid_word(check_word):
            self.solver = Solver(check_word, check_wrong_chars)

    def get_possible_words(self):
        return self.solver.candidate_words

    def get_next_guess(self):
        try:
            return self.solver.get_next_guess()
        except IndexError:
            self.errors.append("Sorry! Couldn't solve this word :(")
            return "N/A"