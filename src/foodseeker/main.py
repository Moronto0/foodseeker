from searches import search_by_kitchen, search_by_category, search_by_ingredient, reset_filters


def menu():
    # Основной цикл программы
    while True:
        print("\nВыберите действие:")
        print("1. По ингредиентам")
        print("2. По категории")
        print("3. По кухне")
        print("4. Сбросить фильтры")
        print("5. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            search_by_ingredient()
        elif choice == "2":
            search_by_category()
        elif choice == "3":
            search_by_kitchen()
        elif choice == "4":
            reset_filters()
            print("Фильтры сброшены. Возвращены исходные данные.")
        elif choice == "5":
            break
        else:
            print("Некорректный ввод. Пожалуйста, введите номер действия от 1 до 5.")


if __name__ == "__main__":
    menu()
