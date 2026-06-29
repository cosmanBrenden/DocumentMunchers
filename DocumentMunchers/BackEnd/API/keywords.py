import spacy
import pytextrank
import Stemmer
from summarizer import Summarizer

class KeywordExtractor:
    def __init__(self):
        self._nlp = spacy.load("en_core_web_sm")
        self._nlp.add_pipe("textrank")
        self._stemmer = Stemmer.Stemmer("english")

    def get_keywords(self, text:str, phrase_depth=20, num_keywords=3) -> list[str]:
        # Process text
        doc = self._nlp(text)
        # For quickly checking if the keyword has been seen already
        kword_set = set()
        # Stores keywords as they come
        ordered_kwords = []
        # Iterates thru phrases as deep as specified
        for i in range(phrase_depth if phrase_depth < len(doc._.phrases) else len(doc._.phrases)):
            phrase = doc._.phrases[i]
            # Iterate thru chunks
            for chunk in phrase.chunks:
                # Preprocess chunk to avoid saving semantically identical chunks
                chunk = str(chunk).lower()
                chunk = self._stemmer.stemWord(chunk)
                # If the chunk hasn't been seen, save it
                if not chunk in kword_set:
                    kword_set.add(chunk)
                    ordered_kwords.append(chunk)

        # Return the "num_keywords" most relevant keywords
        return ordered_kwords[:num_keywords]