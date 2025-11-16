from sentence_transformers import SentenceTransformer, util

EMBEDDING_MODEL_HF_ID = "BAAI/bge-small-en-v1.5"

class Embedding_Model:
    """
    Used for getting the similarity of two documents
    """
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL_HF_ID)
    """
    Calculates the semantic similarity between the ground truth and the actual result

    @param gt: The ground truth
    @param actual: The actual result

    @return: The semantic similarity of 'gt' and 'actual'
    """
    def embedded_similarity(self, gt:str, actual:str):
        query_embed = self.model.encode([gt])
        passage_embed = self.model.encode([actual])
        result = util.cos_sim(query_embed, passage_embed)
        return float(list(result)[0][0])



