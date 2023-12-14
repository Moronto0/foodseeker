import telebot
from telebot import types
from data import df
from searches import search_by_ingredient,search_by_category,search_by_kitchen,reset_filters

filtered_df = df.copy()
cat_list = set(filtered_df['category'])
kit_list = df['kitchen'].unique().tolist()
user_state = {}
# Инициализация словаря для отслеживания выбора пользователей
user_selections = {}

user_ingredients = {}
user_categories = {}
user_kitchens = {}

last_bot_message_id = {}

messages_to_delete = {}

# Функция для создания клавиатуры с чекбоксами
def create_category_markup(user_id):
    markup = types.InlineKeyboardMarkup()
    current_selection = user_selections.get(user_id, set())
    for category in cat_list:
        status_emoji = "✅" if category in current_selection else "❌"
        button_text = f"{status_emoji} {category}"
        callback_data = f"toggle_category|{category}"
        markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))

    # После добавления всех кнопок категорий добавляем кнопку для поиска
    markup.add(types.InlineKeyboardButton('Применить фильтр по выбранным категориям', callback_data='search_categories'))

    return markup

def send_continue_choice(chat_id):
    markup = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton('Да', callback_data='continue_yes')
    no_button = types.InlineKeyboardButton('Нет', callback_data='continue_no')
    markup.add(yes_button, no_button)
    sent_message = bot.send_message(chat_id, "Вы хотите продолжить выбор?", reply_markup=markup)
    messages_to_delete[chat_id] = {'bot_message': sent_message.message_id, 'user_message': None}



def create_continue_choice_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('По ингредиентам', callback_data='ing'))
    markup.add(types.InlineKeyboardButton('По категории', callback_data='cat'))
    markup.add(types.InlineKeyboardButton('По кухне', callback_data='kit'))
    markup.add(types.InlineKeyboardButton('Очистить фильтр поиска', callback_data='clear_filters'))
    return markup


# Функция для создания основной клавиатуры
def create_main_markup(user_id):
    markup = types.InlineKeyboardMarkup()
    # Добавление кнопок с эмодзи в зависимости от того, был ли выбор сделан
    ingredient_emoji = "✅" if user_ingredients.get(user_id) else "❌"
    category_emoji = "✅" if user_categories.get(user_id) else "❌"
    kitchen_emoji = "✅" if user_kitchens.get(user_id) else "❌"

    markup.row(types.InlineKeyboardButton(f'{ingredient_emoji} По ингредиентам', callback_data='ing'))
    markup.row(types.InlineKeyboardButton(f'{category_emoji} По категории', callback_data='cat'))
    markup.row(types.InlineKeyboardButton(f'{kitchen_emoji} По кухне', callback_data='kit'))

    # Добавление кнопки "Поиск по выбранным фильтрам", если был сделан хотя бы один выбор
    if user_ingredients.get(user_id) or user_categories.get(user_id) or user_kitchens.get(user_id):
        markup.row(types.InlineKeyboardButton('Поиск по выбранным фильтрам', callback_data='perform_search'))

    return markup


# Функция для выполнения поиска
def perform_search(user_id):
    ingredients = user_ingredients.get(user_id, [])
    categories = user_categories.get(user_id, [])
    kitchens = user_kitchens.get(user_id, [])
    search_results = []
    if ingredients:
        search_results = []
        temp = search_by_ingredient(','.join(ingredients))
        if temp is None:
            search_results = []
        else:
            search_results.extend(temp)
    if categories:
        search_results = []
        temp = search_by_category(','.join(categories))
        if temp is None:
            search_results = []
        else:
            search_results.extend(temp)
    if kitchens:
        search_results = []
        temp = search_by_kitchen(','.join(kitchens))
        if temp is None:
            search_results = []
        else:
            search_results.extend(temp)
    return search_results


# Функция обновления сообщения с кнопками
def update_main_message(chat_id, user_id):
    new_markup = create_main_markup(user_id)

    # Проверяем, есть ли запись в last_bot_message_id для этого пользователя
    if user_id in last_bot_message_id:
        last_message_id = last_bot_message_id[user_id]

        # Пытаемся получить текущее содержимое сообщения
        try:
            current_message = bot.get_message(chat_id, last_message_id)
            if current_message.reply_markup == new_markup.to_dict():
                return  # Если содержимое не изменилось, прерываем выполнение функции
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")

    # Если проверка пройдена, обновляем сообщение
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=last_bot_message_id[user_id], reply_markup=new_markup)

bot = telebot.TeleBot('6750656397:AAEfi5mFJ41YgnPR6Hz7AMzJ0EyJMTzXe7Q')
@bot.message_handler(commands=['start'])
def start(message, is_continue=False):
    user_id = message.from_user.id  # Извлечь user_id из сообщения
    if user_id not in user_ingredients:
        user_ingredients[user_id] = []
    if user_id not in user_categories:
        user_categories[user_id] = []
    if user_id not in user_kitchens:
        user_kitchens[user_id] = []

    reset_filters()
    # Сброс состояний и выборов
    user_state[user_id] = None
    user_ingredients[user_id] = []
    user_categories[user_id] = []
    user_kitchens[user_id] = []
    user_selections[user_id] = set()
    markup = create_main_markup(user_id)
    sti2 = 'CAACAgIAAxkBAAIEumVvbothiA3cPMLgh0mTaUpS31frAALFBwACeVziCYy9fb2LFU1FMwQ'
    if is_continue:
        markup.add(types.InlineKeyboardButton('Очистить фильтр поиска', callback_data='clear_filters'))
        greeting_text = 'Продолжим поиск!'
        sti2 = 'CAACAgIAAxkBAAIFnWVwXYj8stliOHcNBMdKofcmykSKAAKoBwACeVziCcv_DBHkFKLuMwQ'
    else:
        greeting_text = 'Привет как бы вы хотели начать поиск?'


    bot.send_sticker(message.chat.id,sti2)
    sent_message = bot.send_message(message.chat.id, greeting_text, reply_markup=markup)
    last_bot_message_id[user_id] = sent_message.message_id

def handle_start(message):
    start(message)


@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    print('Sticker ID:', message.sticker.file_id)


@bot.callback_query_handler(func=lambda call: call.data == 'continue_yes')
def handle_continue_yes(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    reset_filters()
    # Сброс состояний и выборов
    user_state[user_id] = None
    user_ingredients[user_id] = []
    user_categories[user_id] = []
    user_kitchens[user_id] = []
    user_selections[user_id] = set()
    if user_id in messages_to_delete:
        bot.delete_message(chat_id, messages_to_delete[user_id]['bot_message'])
        del messages_to_delete[user_id]
        # Отправка нового сообщения для продолжения выбора
    markup = create_main_markup(user_id)
    sti2 = 'CAACAgIAAxkBAAIFnWVwXYj8stliOHcNBMdKofcmykSKAAKoBwACeVziCcv_DBHkFKLuMwQ'
    bot.send_sticker(chat_id, sti2)
    sent_message = bot.send_message(chat_id, "Продолжим поиск!", reply_markup=markup)
    last_bot_message_id[user_id] = sent_message.message_id



# Функция обработчика для кнопки "Поиск по выбранным фильтрам"
@bot.callback_query_handler(func=lambda call: call.data == 'perform_search')
def perform_search_callback(call):
    user_id = call.from_user.id
    results = perform_search(user_id)
    if results:
        for result in results:
            bot.send_message(call.message.chat.id, result)
    else:
        bot.send_message(call.message.chat.id, "По вашим фильтрам ничего не найдено.")
    send_continue_choice(call.message.chat.id)



# Обработчик callback_query для всех кнопок
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    if callback.data == 'ing':
        # Установите состояние пользователя как ожидающее ингредиенты
        user_state[user_id] = 'awaiting_ingredients'
        sent_message = bot.send_message(callback.message.chat.id, 'Напишите через запятую какие ингредиенты у вас есть.\nПример :картофель, яйцо, сыр')
        # Сохраняем ID сообщения бота, чтобы удалить его позже
        messages_to_delete[user_id] = {'bot_message': sent_message.message_id, 'user_message': None}
    elif callback.data == 'cat':
        # Установите состояние пользователя как ожидающее категории
        user_state[user_id] = 'awaiting_categories'
        user_selections[user_id] = set()
        # Отправляем клавиатуру с чекбоксами
        sent_message = bot.send_message(callback.message.chat.id, "Выберите категории из представленных ниже:", reply_markup=create_category_markup(user_id))
        messages_to_delete[user_id] = {'bot_message': sent_message.message_id, 'user_message': None}
    elif callback.data == 'kit':
        # Установите состояние пользователя как ожидающее кухни
        user_state[user_id] = 'awaiting_kitchens'
        sent_message = bot.send_message(callback.message.chat.id, 'Напишите через запятую какие кухни вы хотите.\nПример :русская кухня, итальянская кухня')
        messages_to_delete[user_id] = {'bot_message': sent_message.message_id, 'user_message': None}
    elif callback.data.startswith('toggle_category|'):
        category = callback.data.split('|')[1]
        user_id = callback.from_user.id

        # Инициализируем множество для пользователя, если оно еще не создано
        if user_id not in user_selections:
            user_selections[user_id] = set()

        # Переключение выбора категории
        if category in user_selections[user_id]:
            user_selections[user_id].remove(category)
        else:
            user_selections[user_id].add(category)

        # Обновляем сообщение с чекбоксами
        bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=create_category_markup(user_id)
        )
    elif callback.data == 'continue_no':
        # Пользователь выбрал "Нет", завершаем диалог
        if user_id in user_ingredients:
            del user_ingredients[user_id]
        if user_id in user_categories:
            del user_categories[user_id]
        if user_id in user_kitchens:
            del user_kitchens[user_id]
        reset_filters()
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Спасибо за использование нашего бота!")
        sti1 = 'CAACAgIAAxkBAAIEu2VvbrjaVO2fGIy_tumoX-75qjmOAAKyBwACeVziCbixIQJYTc8KMwQ'
        bot.send_sticker(callback.message.chat.id,sti1)
    elif callback.data == 'clear_filters':
        # Очищаем все фильтры пользователя
        user_ingredients.pop(user_id, None)
        user_categories.pop(user_id, None)
        user_kitchens.pop(user_id, None)
        user_selections[user_id] = set()  # Сбрасываем выбор категорий пользователя
        reset_filters()
        # Изменяем существующее сообщение и обновляем клавиатуру
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('По ингредиентам', callback_data='ing'))
        markup.add(types.InlineKeyboardButton('По категории', callback_data='cat'))
        markup.add(types.InlineKeyboardButton('По кухне', callback_data='kit'))
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text='Продолжим поиск! (фильтр поиска очищен)',
            reply_markup=markup
        )
    elif callback.data == 'search_categories':
        user_id = callback.from_user.id
        chat_id = callback.from_user.id
        # Получаем выбранные категории
        selected_categories = user_selections.get(user_id, str())
        #
        if selected_categories:
            user_categories[user_id] = selected_categories
            user_state[user_id] = None
            update_main_message(callback.message.chat.id, user_id)
        else:
            bot.send_message(callback.message.chat.id, 'Вы не выбрали ни одной категории.')
        # Удаляем сообщения
        if user_id in messages_to_delete:
            bot.delete_message(chat_id, messages_to_delete[user_id]['bot_message'])
            del messages_to_delete[user_id]  # Удаляем информацию из словаря

@bot.message_handler(func=lambda message: user_state.get(message.from_user.id) == 'awaiting_ingredients')
def handle_ingredients(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_ingredients[user_id] = message.text.split(',')
    user_state[user_id] = None
    update_main_message(message.chat.id, user_id)
    # Удаляем сообщения
    if user_id in messages_to_delete:
        bot.delete_message(chat_id, messages_to_delete[user_id]['bot_message'])
        bot.delete_message(chat_id, message.message_id)
        del messages_to_delete[user_id]  # Удаляем информацию из словаря

@bot.message_handler(func=lambda message: user_state.get(message.from_user.id) == 'awaiting_categories')
def handle_categories(message):
    user_id = message.from_user.id
    user_categories[user_id] = message.text.split(',')
    # Получить выбранные категории из выбора пользователя
    selected_categories = ', '.join(user_selections.get(user_id, []))
    temp_row = search_by_category(selected_categories)
    if temp_row:
        for item in temp_row:
            bot.send_message(message.chat.id, item)
    # После обработки сбросить состояние пользователя
    user_state[user_id] = None

@bot.message_handler(func=lambda message: user_state.get(message.from_user.id) == 'awaiting_kitchens')
def handle_kitchens(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_kitchens[user_id] = message.text.split(',')
    user_state[user_id] = None
    update_main_message(message.chat.id, user_id)
    # Удаляем сообщения
    if user_id in messages_to_delete:
        bot.delete_message(chat_id, messages_to_delete[user_id]['bot_message'])
        bot.delete_message(chat_id, message.message_id)
        del messages_to_delete[user_id]  # Удаляем информацию из словаря


# Запуск бота
def main():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()
