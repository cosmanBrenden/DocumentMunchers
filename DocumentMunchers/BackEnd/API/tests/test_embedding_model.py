import unittest
import sys
sys.path.append("../")
from embedding_model import Embedding_Model

class TestEmbeddingModel(unittest.TestCase):
    def test_loads(self):
        try:
            model = Embedding_Model()
        except:
            self.fail()
    def test_runs(self):
        model = Embedding_Model()
        self.assertNotEqual(model.embedded_similarity("king", "queen"), 1)
        self.assertEqual(int(model.embedded_similarity("king", "king")), 1)
        self.assertEqual(model.embedded_similarity("king", "queen"), model.embedded_similarity("queen", "king"))
if __name__ == '__main__':
    unittest.main()