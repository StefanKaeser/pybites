from typing import List


def common_words(sentence1: List[str], sentence2: List[str]) -> List[str]:
    """
    Input:  Two sentences - each is a  list of words in case insensitive ways.
    Output: those common words appearing in both sentences. Capital and lowercase 
            words are treated as the same word. 

            If there are duplicate words in the results, just choose one word. 
            Returned words should be sorted by word's length.
    """
    #common_words = set()
    #for word1 in sentence1:
    #    word1 = word1.lower()
    #    for word2 in sentence2:
    #        word2 = word2.lower()
    #        if word1 == word2:
    #            common_words.add(word1)
    sentence1 = set([word.lower() for word in sentence1])
    sentence2 = set([word.lower() for word in sentence2])
    common_words = sentence1 & sentence2

    return list(common_words)



