from embedding_model import Embedding_Model
from tf_idf import TFIDF
from nlp_tools import POS_Enforcer

DELIMITERS = [".", ",", "!", "?", "(", ")", "/", ";", ":"]

class Similarity:
    """
    Used for getting the semantic similarity of a query and a file
    @param emb_model The embedding model to use on summaries
    @param check The part of speech enforcer for keyword generation from a query
    """
    def __init__(self, checker: POS_Enforcer, emb_model: Embedding_Model):
        self.emb_model = emb_model
        self.checker = checker
    
    """
    Gets the semantic similarity between the query and a file
    @param query The query to use
    @param file The file to test the query against
    @return The score
    """
    def get_similarity(self, query:str, file:dict) -> float:
        # Get the tfidf obj out of the file
        tfidf:TFIDF = file["tfidf"]
        # Remove any delimiters from the query
        for delim in DELIMITERS:
            query_no_delim = query.replace(delim, " ")
        
        # Split query into a list of works
        words = query_no_delim.split(" ")
        scores = []
        # Create a list of words that are valid parts of speech, and have a
        # valid tfidf 
        for w in words:
            if(self.checker.is_valid_pos(w)):
                score = float(tfidf.get_tfidf_for_word(w))
                if score != -1:
                    scores.append(score)
        # Get the average tfidf score
        max_tfidf = tfidf.get_tfidf_for_word(tfidf.get_keywords()[0])
        if(len(scores) > 0):
            scores = [x/max_tfidf for x in scores]
            avg_score = sum(scores)/len(scores)
        else:
            avg_score = 0

        # If there is a summary, use the embedding model on the query
        if(file["summary"] != None):
            emb_sim = self.emb_model.embedded_similarity(file["summary"], query)
            # Avg between tfidf and embedded score
            return (avg_score - emb_sim) / 2
        # Just tfidf average
        return avg_score
        
        

        
        