import lftk
import spacy

VALID_POS = ["n_adj", "n_noun", "n_propn", "n_verb", "n_adv"]

class POS_Enforcer:
    """
    For determining if a word is a valid part of speech, used for keywords
    """
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    """
    Checks if the passed word is a valid part of speech for keywords,
    this is define in the static variable 'VALID_POS'
    @param word The word to check
    @param nlp The tokenizer for checking pos
    @return True if valid, False else.
    """
    def is_valid_pos(self, word):
        # Tokenize
        word = self.nlp(word)
        # Init POS extractor on word
        extr = lftk.Extractor(docs=[word])
        # Extract features
        fts = extr.extract(features=VALID_POS)
        # Check if one of the features returned a 1, return on the first 1
        for k in fts.keys():
            curr = fts[k]
            if(curr == 1):
                return True
        # The word is not a valid part of speech, reject
        return False