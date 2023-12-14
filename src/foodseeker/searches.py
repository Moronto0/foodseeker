from data import df

# Инициализация DataFrame для сохранения фильтров
filtered_df = df.copy()

ingredient_filters = []
category_filters = []
kitchen_filters = []


def apply_filters():
    global filtered_df, ingredient_filters, category_filters, kitchen_filters

    # Применение сохраненных фильтров
    if ingredient_filters:
        filters = filtered_df['ingredients'].apply(lambda x: all(ingredient.lower() in x.lower() for ingredient in ingredient_filters))
        filtered_df = filtered_df[filters]

    if category_filters:
        filters = filtered_df['category'].str.lower().isin(category_filters)
        filtered_df = filtered_df[filters]

    if kitchen_filters:
        filters = filtered_df['kitchen'].str.lower().isin(kitchen_filters)
        filtered_df = filtered_df[filters]


def search_by_ingredient():
    global filtered_df, ingredient_filters, category_filters, kitchen_filters  # Используем глобальные переменные

    # Сброс данных
    filtered_df = df.copy()

    ingredients_input = input("Введите ингредиенты через запятую: ")
    ingredients_list = [ingredient.strip() for ingredient in ingredients_input.split(",")]

    # Сохранение новых фильтров по ингредиентам
    ingredient_filters = ingredients_list

    # Применение сохраненных фильтров перед выводом
    apply_filters()

    # Вывод результатов
    print_results(filtered_df)


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
            print(f"{row['food']} — {row['ingredients']} — {row['category']} — {row['kitchen']} — {row['food_url']}")
    else:
        print("Нет подходящих результатов.")

