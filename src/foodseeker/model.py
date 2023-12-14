from gensim.models import Word2Vec
from data import df
from preproccessing import preprocess_text

sentences = [preprocess_text(ingredients) for ingredients in df['ingredients']]

model = Word2Vec(sentences=sentences, vector_size=300, window=5, min_count=1, workers=4, sg=1, epochs=30)

model.save("ingredients_preprocessed.model")
