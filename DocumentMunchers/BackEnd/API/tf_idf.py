from nlp_tools import POS_Enforcer
import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer


TFIDF_PERCENTILE = 90
VALID_POS = ["n_adj", "n_noun", "n_propn", "n_verb", "n_adv"]

class TFIDF:
    """
    TF*IDF class, manages table for one document, pass either vectorizer data or a document, but not both.
    @param vectorizer_data Data loaded from a json of a previously saved tfidf obj, default=None
    @param document The document to fit the tfidf to if nothing should be loaded, default=None
    """
    def __init__(self, vectorizer_data=None, document=None):
        # If nothing has been given to build the TFIDF model, raise an exception
        if(not vectorizer_data and not document):
            raise Exception("Nothing to load!")
        
        self.vectorizer = None

        # If somehow both args are not none, prefer refitting in case of potential
        # changes to the file content
        if(document != None):
            self.__fit(document)
        elif(vectorizer_data != None):
            self.__load(vectorizer_data)
        
    
    """
    Private method for getting keywords, a bit costly, this runs when constructing, so that
    future access can be constant.

    @return The list of keywords sorted in descending order of tfidf
    """
    def __get_keywords(self):
        # Used for checking if a word is a valid part of speech
        checker = POS_Enforcer()

        # Extract all valid feature names based on above parts of speech
        valid_words = []
        invalid_words = ['cid']
        for word in self.feature_names:
            if(checker.is_valid_pos(word) and word not in invalid_words):
                valid_words.append(word)
        # Get the tfidf of all valid words
        tfidfs = []
        for word in valid_words:
            tfidfs.append(self.get_tfidf_for_word(word))
        
        # Find the value for the upper percentile (90th)
        upper_val = np.percentile(np.array(tfidfs), TFIDF_PERCENTILE)
        # Get all words that are within the 90th percentile
        upper_percentile_words_tuples = []
        for i in range(len(tfidfs)):
            val = tfidfs[i]
            word = valid_words[i]
            if val >= upper_val:
                upper_percentile_words_tuples.append((word, val))

        # Sort keywords in descending order of tfidf, so that the first keyword
        # is the most relevant, and the second one the second most relevant, and
        # so on...
        sorted_tuples = sorted(upper_percentile_words_tuples, key=lambda x : x[1])
        upper_percentile_words = [x[0] for x in sorted_tuples]
        upper_percentile_words.reverse()
        
        return upper_percentile_words

    """
    Private method, handles filling the fields when a document needs to be fitted
    @param document The document to fit
    """
    def __fit(self, document):
        print("Fitting TFIDF")
        # Fit document
        self.vectorizer = TfidfVectorizer()
        # Get the matrix out so we don't have to convert it again
        self.fit = self.vectorizer.fit_transform([document])
        
        # Get the feature names out for similar reasons
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        # Get the list of keywords
        self.keywords = self.__get_keywords()

    """
    Private method, for when the table was saved, just need to reload
    @param vectorizer_data The data to load
    """
    def __load(self, vectorizer_data):
        print("Loading TFIDF table")
        # From Deepseek, this info would have been stored in a json, and loaded
        # into vectorizer_data
        self.vectorizer = TfidfVectorizer(**vectorizer_data['vectorizer_params'])
        self.vectorizer.vocabulary_ = vectorizer_data['vocabulary_']
        self.vectorizer.idf_ = np.array(vectorizer_data['idf_'])
        self.vectorizer.fixed_vocabulary_ = vectorizer_data['fixed_vocabulary_'] == "True"
        self.keywords = vectorizer_data["keywords"]
        # Get the matrix out so we don't have to convert it again
        self.fit = sparse.csr_matrix(np.matrix(vectorizer_data["fit"]))
        # Get the feature names out for similar reasons
        self.feature_names = self.vectorizer.get_feature_names_out()


    """
    Returns the tfidf of a word, or -1 if the word doesn't exist in the fit
    @return The tfidf value if its a word in the matrix, -1 if not
    """
    def get_tfidf_for_word(self, word, doc_index=0):
        try:
            # Find the column index of the word
            word_index = np.where(self.feature_names == word)[0][0]
            # Get the TF-IDF value
            tfidf_value = self.fit[doc_index, word_index]
            return tfidf_value
        except IndexError:
            return -1  # Word not in vocabulary
    
    """
    Get n keywords, default 3
    @param num_w The number of keywords to return
    @return The keywords, default=3
    """
    def get_keywords(self, num_w=3):
        return self.keywords[:num_w]
    
        
    """
    Creates a dictionary of the vectorizer and fit for saving to a file
    @return The dictionary for writing
    """
    def export(self):
        # From deepseek, extract all pertinent data
        vectorizer_data = {
            'vectorizer_params': self.vectorizer.get_params(),
            'vocabulary_': self.vectorizer.vocabulary_,
            'idf_': self.vectorizer.idf_.tolist(),
            'fixed_vocabulary_': str(self.vectorizer.fixed_vocabulary_),
            "keywords": list(self.keywords),
            # Will throw warnings, still works
            "fit": self.fit.todense().tolist()
        }
        return vectorizer_data
        

