# class Summarizer:
#     def __init__(self):
#         print("""
#         Jester - Why did the chicken cross the road?
#         The King - I don't know. Why did the chicken cross the road?
#         Jester - Your Jordans are fake.
#         """)
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict
import string

class Summarizer:
    def __init__(self):
        # Download necessary NLTK data
        nltk.download("punkt_tab")
        nltk.download('punkt')
        nltk.download('stopwords')

    def summarize(self, text, num_sentences=3, max_chars=200):
        # Step 1: Sentence Tokenization
        sentences = sent_tokenize(text)
        
        # Step 2: Word Tokenization and Frequency Analysis
        stop_words = set(stopwords.words('english'))
        word_frequencies = defaultdict(int)
        for sentence in sentences:
            # Word tokenization
            words = word_tokenize(sentence.lower())
            for word in words:
                if word not in stop_words and word not in string.punctuation:
                    word_frequencies[word] += 1
        
        # Step 3: Calculate Sentence Scores
        sentence_scores = defaultdict(int)
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_frequencies:
                    sentence_scores[sentence] += word_frequencies[word]
        
        # Step 4: Select Top Sentences
        sorted_sentences = sorted(sentence_scores.items(), key=lambda item: item[1], reverse=True)
        top_sentences = [sentence for sentence, score in sorted_sentences[:num_sentences]]
        
        # Step 5: Generate Summary
        summary = ' '.join(top_sentences)
        return summary[:max_chars]
