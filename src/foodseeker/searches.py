import pandas as pd
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
from preproccessing import preprocess_text
from grammar import correct_text
from data import df
import numpy as np

# Инициализация DataFrame для сохранения фильтров
filtered_df = df.copy()

# Импорт модели
model = Word2Vec.load(r"..\..\ingredients.model")

ingredient_filters = []
category_filters = []
kitchen_filters = []

def apply_filters():
    global filtered_df, ingredient_filters, category_filters, kitchen_filters

    # Применение сохраненных фильтров
    if ingredient_filters:
        filters = filtered_df['ingredients'].apply(lambda x: all(ingredient in x for ingredient in ingredient_filters))
        filtered_df = filtered_df[filters]

    if category_filters:
        filters = filtered_df['category'].str.lower().isin(category_filters)
        filtered_df = filtered_df[filters]

    if kitchen_filters:
        filters = filtered_df['kitchen'].str.lower().isin(kitchen_filters)
        filtered_df = filtered_df[filters]

def search_by_ingredient():
    global filtered_df, model

    ingredients_input = correct_text(input("Введите список ингредиентов через запятую: "))

    # Препроцессинг введенных ингредиентов
    ingredients_list = preprocess_text(ingredients_input)

    # Векторизация
    ingredients_vector = sum([model.wv[token] for token in ingredients_list if token in model.wv]) / len(
        ingredients_list)

    print(ingredients_vector, type(ingredients_vector))

    # Вычисление степени схожести введенного текста с моделью
    model_vectors = [
        sum([model.wv[token] for token in ingredients.split(', ') if token in model.wv]) / len(ingredients.split(', '))
        for ingredients in filtered_df['ingredients']
    ]

    # Вычисление степени схожести
    similarities = [np.dot(ingredients_vector, model_vector) / (np.linalg.norm(ingredients_vector) * np.linalg.norm(model_vector))
                    for model_vector in model_vectors]

    # Сортировка результата по схожести
    sorted_indices = np.argsort(similarities)[::-1]

    seen_recipes = set()
    count = 0

    search_results_df = pd.DataFrame(columns=filtered_df.columns)

    for idx in sorted_indices:
        if filtered_df['food'].iloc[idx] not in seen_recipes:
            new_row = filtered_df.iloc[idx:idx + 1]  # Extract the row as a DataFrame
            search_results_df = pd.concat([search_results_df, new_row], ignore_index=True)

            seen_recipes.add(filtered_df['food'].iloc[idx])
            count += 1

    # Применение сохраненных фильтров перед выводом
    apply_filters()

    # Вывод результатов
    print_results(search_results_df)


def search_by_category():
    global filtered_df, ingredient_filters, category_filters, kitchen_filters

    # Сброс данных
    filtered_df = df.copy()

    category_input = input("Введите категории через запятую: ")
    categories_list = [category.strip().lower() for category in category_input.split(",")]

    # Сохранение новых фильтров по категориям
    category_filters = categories_list

    # Применение сохраненных фильтров перед выводом
    apply_filters()

    # Вывод результатов
    print_results(filtered_df)

def search_by_kitchen():
    global filtered_df, ingredient_filters, category_filters, kitchen_filters

    # Сброс данных
    filtered_df = df.copy()

    kitchen_input = input("Введите кухни через запятую: ")
    kitchens_list = [kitchen.strip().lower() for kitchen in kitchen_input.split(",")]

    # Сохранение новых фильтров по кухням
    kitchen_filters = kitchens_list

    # Применение сохраненных фильтров перед выводом
    apply_filters()

    # Вывод результатов
    print_results(filtered_df)


def reset_filters():
    global filtered_df, ingredient_filters, category_filters, kitchen_filters

    # Сброс всех фильтров
    filtered_df = df.copy()
    ingredient_filters = []
    category_filters = []
    kitchen_filters = []

    return filtered_df


def print_results(result_df):
    if not result_df.empty:
        # Сортировка по количеству ингредиентов
        sorted_df = result_df.sort_values(by='ingredients', key=lambda x: x.str.len())
        # Удаление дубликатов
        unique_df = sorted_df.drop_duplicates(subset=['food', 'ingredients', 'category', 'kitchen', 'food_url'])
        # Ограничение вывода до 30 строк
        limited_df = unique_df.head(30)
        for _, row in limited_df.iterrows():
            print(f"{row['food'].capitalize()} — {row['ingredients'].capitalize()} — {row['category'].capitalize()} — {row['kitchen'].capitalize()} — {row['food_url'].capitalize()}")
    else:
        print("Нет подходящих результатов.")

