from collections import Counter


def is_anagram(word1, word2):
    """Receives two words and returns True/False (boolean) if word2 is
       an anagram of word1, ignore case and spacing.
       About anagrams: https://en.wikipedia.org/wiki/Anagram"""

    def _normalize_str(s):
        return s.replace(" ", "").lower()

    word1, word2 = _normalize_str(word1), _normalize_str(word2)

    return Counter(word1) == Counter(word2)
