import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

nltk.download('stopwords')
mystem = Mystem()
russian_stopwords = stopwords.words("russian")

def preprocess_text(text):
    ingredients = text.split(', ') if ', ' in text else [text]

    for i, element in enumerate(ingredients):
        tokens = mystem.lemmatize(element.lower().strip())
        tokens = [token for token in tokens if token not in russian_stopwords
                  and token != " "
                  and token.strip() not in punctuation]

        ingredients[i] = ' '.join(tokens)

    return ingredients