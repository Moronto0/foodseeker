import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

mystem = Mystem()
russian_stopwords = stopwords.words("russian")

def preprocess_text(text):
    text = text.split(', ')
    for i, element in enumerate(text):
        tokens = mystem.lemmatize(element.lower().strip())
        tokens = [token for token in tokens if token not in russian_stopwords
                  and token != " "
                  and token.strip() not in punctuation]

        text[i] = ' '.join(tokens)

    return text