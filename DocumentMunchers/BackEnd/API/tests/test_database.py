import unittest
import sys
sys.path.append("../")
from database import Database
from embedding_model import Embedding_Model

class TestEmbeddingModel(unittest.TestCase):
    def setUp(self):
        self.db = Database(emb_model=Embedding_Model())
    def test_loads(self):
        self.assertIsNotNone(self.db)
if __name__ == '__main__':
    unittest.main()