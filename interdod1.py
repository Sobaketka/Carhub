import json


def load_cars():
    try:
        with open("cars.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_cars(cars):
    with open("cars.json", "w", encoding="utf-8") as file:
        json.dump(cars, file, ensure_ascii=False, indent=4)


def print_car(number, car):
    if car["sold"]:
        status = "ПРОДАНО"
    else:
        status = "в наявності"
    print(number, "->", car["brand"], car["model"], "-", car["year"], "рік -",
          car["price"], "$ -", car["mileage"], "км [" + status + "]")


def ask_number(cars):
    text = input("> ")
    if not text.isdigit():
        print("Номер повинен бути числом")
        return 0
    number = int(text)
    if number < 1 or number > len(cars):
        print("Такої машини немає")
        return 0
    return number


def show_help():
    print("add      - додати машину")
    print("show     - показати всі машини")
    print("edit     - змінити машину")
    print("delete   - видалити машину")
    print("search   - пошук за маркою")
    print("sold     - змінити статус продано / не продано")
    print("filter   - показати тільки в наявності або тільки продані")
    print("info     - інформація про одну машину")
    print("range    - пошук за діапазоном цін")
    print("discount - знижка на машину у відсотках")
    print("sort     - сортувати за ціною")
    print("brands   - скільки машин кожної марки")
    print("stats    - статистика")
    print("clear    - видалити всі машини")
    print("exit     - вихід")


def repl():
    cars = load_cars()

    print("CarHub")
    print("Команди: help - список команд")

    while True:
        command = input("--> ")

        if command == "exit":
            save_cars(cars)
            print("збережено")
            break

        elif command == "help":
            show_help()

        elif command == "add":
            print("Вкажіть: марка модель рік ціна пробіг")
            data = input("> ").split()

            if len(data) == 5 and data[2].isdigit() and data[3].isdigit() and data[4].isdigit():
                car = {
                    "brand": data[0],
                    "model": data[1],
                    "year": int(data[2]),
                    "price": int(data[3]),
                    "mileage": int(data[4]),
                    "sold": False
                }
                cars.append(car)
                save_cars(cars)
                print("Машину додано")
            else:
                print("Неправильні дані (рік, ціна, пробіг - числа)")

        elif command == "show":
            if len(cars) == 0:
                print("Список машин порожній")
            else:
                for i in range(len(cars)):
                    print_car(i + 1, cars[i])

        elif command == "delete":
            print("Вкажіть номер машини")
            number = ask_number(cars)

            if number != 0:
                cars.pop(number - 1)
                save_cars(cars)
                print("Машину видалено")

        elif command == "search":
            print("Вкажіть марку")
            brand = input("> ")

            found = False
            for i in range(len(cars)):
                if cars[i]["brand"].lower() == brand.lower():
                    print_car(i + 1, cars[i])
                    found = True

            if found == False:
                print("Машину не знайдено")

        elif command == "edit":
            print("Вкажіть: номер марка модель рік ціна пробіг")
            data = input("> ").split()

            if len(data) == 6 and data[0].isdigit() and data[3].isdigit() and data[4].isdigit() and data[5].isdigit():
                number = int(data[0])

                if number >= 1 and number <= len(cars):
                    car = {
                        "brand": data[1],
                        "model": data[2],
                        "year": int(data[3]),
                        "price": int(data[4]),
                        "mileage": int(data[5]),
                        "sold": cars[number - 1]["sold"]
                    }
                    cars[number - 1] = car
                    save_cars(cars)
                    print("Машину змінено")
                else:
                    print("Такої машини немає")
            else:
                print("Неправильні дані")

        elif command == "sold":
            print("Вкажіть номер машини")
            number = ask_number(cars)

            if number != 0:
                if cars[number - 1]["sold"] == True:
                    cars[number - 1]["sold"] = False
                    print("Статус: в наявності")
                else:
                    cars[number - 1]["sold"] = True
                    print("Статус: продано")
                save_cars(cars)

        elif command == "filter":
            print("Що показати? 1 - в наявності, 2 - продані")
            choice = input("> ")

            if choice == "1" or choice == "2":
                found = False
                for i in range(len(cars)):
                    if choice == "1" and cars[i]["sold"] == False:
                        print_car(i + 1, cars[i])
                        found = True
                    elif choice == "2" and cars[i]["sold"] == True:
                        print_car(i + 1, cars[i])
                        found = True

                if found == False:
                    print("Нічого не знайдено")
            else:
                print("Неправильний вибір")

        elif command == "info":
            print("Вкажіть номер машини")
            number = ask_number(cars)

            if number != 0:
                car = cars[number - 1]
                print("Марка:", car["brand"])
                print("Модель:", car["model"])
                print("Рік:", car["year"])
                print("Ціна:", car["price"], "$")
                print("Пробіг:", car["mileage"], "км")
                if car["sold"]:
                    print("Статус: продано")
                else:
                    print("Статус: в наявності")

        elif command == "range":
            print("Вкажіть діапазон цін: від до")
            data = input("> ").split()

            if len(data) == 2 and data[0].isdigit() and data[1].isdigit():
                low = int(data[0])
                high = int(data[1])

                found = False
                for i in range(len(cars)):
                    if cars[i]["price"] >= low and cars[i]["price"] <= high:
                        print_car(i + 1, cars[i])
                        found = True

                if found == False:
                    print("Нічого не знайдено")
            else:
                print("Неправильні дані")

        elif command == "discount":
            print("Вкажіть: номер знижка(%)")
            data = input("> ").split()

            if len(data) == 2 and data[0].isdigit() and data[1].isdigit():
                number = int(data[0])
                percent = int(data[1])

                if number < 1 or number > len(cars):
                    print("Такої машини немає")
                elif percent < 1 or percent > 99:
                    print("Знижка має бути від 1 до 99")
                elif cars[number - 1]["sold"] == True:
                    print("Ця машина вже продана")
                else:
                    old_price = cars[number - 1]["price"]
                    new_price = old_price * (100 - percent) // 100
                    cars[number - 1]["price"] = new_price
                    save_cars(cars)
                    print("Ціна:", old_price, "$ ->", new_price, "$")
            else:
                print("Неправильні дані")

        elif command == "sort":
            for i in range(len(cars)):
                for j in range(len(cars) - 1 - i):
                    if cars[j]["price"] > cars[j + 1]["price"]:
                        cars[j], cars[j + 1] = cars[j + 1], cars[j]
            save_cars(cars)
            print("Відсортовано за ціною")

        elif command == "brands":
            counts = {}
            for car in cars:
                brand = car["brand"]
                if brand in counts:
                    counts[brand] = counts[brand] + 1
                else:
                    counts[brand] = 1

            if len(counts) == 0:
                print("Список машин порожній")
            else:
                for brand in counts:
                    print(brand, "-", counts[brand])

        elif command == "stats":
            if len(cars) == 0:
                print("Список машин порожній")
            else:
                sold_count = 0
                total_price = 0
                sold_sum = 0

                for car in cars:
                    total_price = total_price + car["price"]
                    if car["sold"] == True:
                        sold_count = sold_count + 1
                        sold_sum = sold_sum + car["price"]

                print("Всього машин:", len(cars))
                print("Продано:", sold_count)
                print("В наявності:", len(cars) - sold_count)
                print("Середня ціна:", total_price // len(cars), "$")
                print("Сума продажів:", sold_sum, "$")

        elif command == "clear":
            answer = input("Точно видалити все? (y/n) > ")
            if answer == "y":
                cars.clear()
                save_cars(cars)
                print("Всі машини видалено")

        else:
            print("Невідома команда (help - список команд)")


repl()