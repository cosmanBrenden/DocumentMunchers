from database import Database
from embedding_model import Embedding_Model
from nlp_tools import POS_Enforcer
from semantic_similarity import Similarity
from summarizer import Summarizer

"""
Constructs an instance of a database
@return The database object to use
"""
def get_database():
    # pos = POS_Enforcer()
    emb = Embedding_Model()
    # sim = Similarity(checker=pos, emb_model=emb)
    # summ = Summarizer()
    db = Database(emb_model=emb)
    return db
