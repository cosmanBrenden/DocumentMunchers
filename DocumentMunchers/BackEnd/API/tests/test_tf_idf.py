import unittest
import sys
sys.path.append("../")
from tf_idf import TFIDF

DOCUMENT = """
The On Psychic Pneuma survives in about thirty-five manuscripts dating to
between the fourteenth and sixteenth centuries.198 It was first printed in Greek
in the sixteenth century.199 Two further Greek editions were published in the
late eighteenth century and early nineteenth century respectively.200 It was
written at the request of John’s contemporary, the intellectual monk Joseph
Rhakendytes, with the aim of helping the latter to keep his psychic pneuma in
a purified state. In the text there is no evidence that John had been a student of
Joseph Rhakendytes, as has previously been suggested.201 The latter arrived in
Constantinople around 1308202 when John, as is confirmed in his correspond-
ence with Lakapenos, was already a practising physician. John sometimes uses
the term ‘father’ (pateras) when addressing Joseph, which should be seen in
the light of Joseph’s status as a member of the clergy and probably reflects a
spiritual relationship.203 In the text we are informed about meetings between
John and Joseph in which they used to discuss philosophical matters. Joseph
was also able to get involved in discussions about medicine with John and
could perform venesection.204
The work is divided into two books as follows: theoretical aspects on the
formation and roles of various kinds of pneumata (book one) and therapeutic
agents (book two) with considerable attention given to diet. Throughout the
treatise the psychic pneuma, which is dispersed through the body via the
nerves and is responsible for sensory and motor activities, is the subject of
significant attention. John introduces a new theory in which each of the four
pneumata is correlated with two primary qualities (unnamed, ‘gastric’
pneuma: cold and moist; natural pneuma: warm and moist; vital pneuma:
warm and dry; psychic pneuma: cold and dry). Any disturbance in the quality,
for example, of the psychic pneuma may affect its flow and consequently it can
be a cause of impairment. Ultimately, John made a direct connection between
the quality of pneuma and someone’s daily regimen, thus introducing a
systematic classification of qualitative change in pneuma as an object of
treatment.
"""


class TestTFIDF(unittest.TestCase):

    def test_fit(self):
        try:
            tfidf = TFIDF(document=DOCUMENT)   
        except:
            self.fail()
        print(tfidf.get_keywords(num_w=20))
        self.assertNotEqual(tfidf.get_keywords(num_w=20), None)
        self.assertGreater(tfidf.get_tfidf_for_word("confirmed"), -1)
        self.assertNotEqual(list(tfidf.export().keys()), None)
    
    def test_load(self):
        tfidf = TFIDF(document=DOCUMENT)
        dat = tfidf.export()

        try:
            tfidf2 = TFIDF(vectorizer_data=dat)   
        except:
            self.fail()
        self.assertEqual(tfidf.get_keywords(num_w=20), tfidf2.get_keywords(num_w=20))
        self.assertEqual(tfidf.get_tfidf_for_word("confirmed"), tfidf2.get_tfidf_for_word("confirmed"))

if __name__ == '__main__':
    unittest.main()