import functions

def do_help(cars):
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


def do_add(cars):
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
        functions.save_cars(cars)
        print("Машину додано")
    else:
        print("Неправильні дані (рік, ціна, пробіг - числа)")


def do_show(cars):
    if len(cars) == 0:
        print("Список машин порожній")
    else:
        for i in range(len(cars)):
            functions.print_car(i + 1, cars[i])


def do_delete(cars):
    print("Вкажіть номер машини")
    number = functions.ask_number(cars)

    if number != 0:
        cars.pop(number - 1)
        functions.save_cars(cars)
        print("Машину видалено")


def do_search(cars):
    print("Вкажіть марку")
    brand = input("> ")

    found = False
    for i in range(len(cars)):
        if cars[i]["brand"].lower() == brand.lower():
            functions.print_car(i + 1, cars[i])
            found = True

    if found == False:
        print("Машину не знайдено")


def do_edit(cars):
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
            functions.save_cars(cars)
            print("Машину змінено")
        else:
            print("Такої машини немає")
    else:
        print("Неправильні дані")


def do_sold(cars):
    print("Вкажіть номер машини")
    number = functions.ask_number(cars)

    if number != 0:
        if cars[number - 1]["sold"] == True:
            cars[number - 1]["sold"] = False
            print("Статус: в наявності")
        else:
            cars[number - 1]["sold"] = True
            print("Статус: продано")
        functions.save_cars(cars)


def do_filter(cars):
    print("Що показати? 1 - в наявності, 2 - продані")
    choice = input("> ")

    if choice == "1" or choice == "2":
        found = False
        for i in range(len(cars)):
            if choice == "1" and cars[i]["sold"] == False:
                functions.print_car(i + 1, cars[i])
                found = True
            elif choice == "2" and cars[i]["sold"] == True:
                functions.print_car(i + 1, cars[i])
                found = True

        if found == False:
            print("Нічого не знайдено")
    else:
        print("Неправильний вибір")


def do_info(cars):
    print("Вкажіть номер машини")
    number = functions.ask_number(cars)

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


def do_range(cars):
    print("Вкажіть діапазон цін: від до")
    data = input("> ").split()

    if len(data) == 2 and data[0].isdigit() and data[1].isdigit():
        low = int(data[0])
        high = int(data[1])

        found = False
        for i in range(len(cars)):
            if cars[i]["price"] >= low and cars[i]["price"] <= high:
                functions.print_car(i + 1, cars[i])
                found = True

        if found == False:
            print("Нічого не знайдено")
    else:
        print("Неправильні дані")


def do_discount(cars):
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
            functions.save_cars(cars)
            print("Ціна:", old_price, "$ ->", new_price, "$")
    else:
        print("Неправильні дані")


def do_sort(cars):
    for i in range(len(cars)):
        for j in range(len(cars) - 1 - i):
            if cars[j]["price"] > cars[j + 1]["price"]:
                cars[j], cars[j + 1] = cars[j + 1], cars[j]
    functions.save_cars(cars)
    print("Відсортовано за ціною")


def do_brands(cars):
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


def do_stats(cars):
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


def do_clear(cars):
    answer = input("Точно видалити все? (y/n) > ")
    if answer == "y":
        cars.clear()
        functions.save_cars(cars)
        print("Всі машини видалено")


COMMANDS = {
    "help": do_help,
    "add": do_add,
    "show": do_show,
    "edit": do_edit,
    "delete": do_delete,
    "search": do_search,
    "sold": do_sold,
    "filter": do_filter,
    "info": do_info,
    "range": do_range,
    "discount": do_discount,
    "sort": do_sort,
    "brands": do_brands,
    "stats": do_stats,
    "clear": do_clear,
}


def dispatch(cars, command):
    if command == "exit":
        functions.save_cars(cars)
        print("збережено")
        return False

    if command in COMMANDS:
        COMMANDS[command](cars)
    else:
        print("Невідома команда (help - список команд)")
    return True