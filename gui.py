import os
import FreeSimpleGUI as sg
import functions
import core


def update_list(window, cars):
    values = []

    for i in range(len(cars)):
        car = cars[i]
        if car["sold"]:
            status = "ПРОДАНО"
        else:
            status = "В наявності"

        text = str(i + 1) + ". " + car["brand"] + " " + car["model"]
        text += " | " + str(car["year"])
        text += " | " + str(car["price"]) + "$"
        text += " | " + str(car["mileage"]) + " км"
        text += " | " + status

        values.append(text)

    window["cars"].update(values=values)


def main():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(functions.FILEPATH):
        with open(functions.FILEPATH, "w", encoding="utf-8"):
            pass

    cars = functions.get_cars()

    layout = [
        [sg.Text("CarHub - Автосалон", font=("Arial", 20, "bold"))],

        [sg.Text("Марка", size=(12, 1)),
         sg.Input(key="brand", size=(25, 1))],

        [sg.Text("Модель", size=(12, 1)),
         sg.Input(key="model", size=(25, 1))],

        [sg.Text("Рік", size=(12, 1)),
         sg.Input(key="year", size=(25, 1))],

        [sg.Text("Ціна ($)", size=(12, 1)),
         sg.Input(key="price", size=(25, 1))],

        [sg.Text("Пробіг (км)", size=(12, 1)),
         sg.Input(key="mileage", size=(25, 1))],

        [sg.Button("Додати", key="add"),
         sg.Button("Редагувати", key="edit"),
         sg.Button("Видалити", key="delete")],

        [sg.Text("Пошук за маркою:"),
         sg.Input(key="search", size=(20, 1)),
         sg.Button("Знайти", key="search_button"),
         sg.Button("Показати всі", key="show")],

        [sg.Text("Фільтр:"),
         sg.Button("В наявності", key="available"),
         sg.Button("Продані", key="sold"),
         sg.Button("Усі", key="all")],

        [sg.Listbox(
            values=[],
            key="cars",
            size=(75, 12),
            enable_events=True
        )],

        [sg.Button("Інформація", key="info"),
         sg.Button("Змінити статус", key="change_sold"),
         sg.Button("Знижка", key="discount")],

        [sg.Button("Сортувати за ціною", key="sort"),
         sg.Button("Статистика", key="stats"),
         sg.Button("Марки", key="brands")],

        [sg.Button("Діапазон цін", key="range"),
         sg.Button("Очистити список", key="clear"),
         sg.Button("Вихід", key="exit")]
    ]

    window = sg.Window(
        "CarHub",
        layout,
        font=("Arial", 11)
    )

    update_list(window, cars)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "exit"):
            functions.write_cars(cars)
            break
        if event == "add":
            try:
                if not values["brand"].strip() or not values["model"].strip():
                    sg.popup_error("Введіть марку та модель")
                    continue
                if not values["year"].isdigit() or not values["price"].isdigit() or not values["mileage"].isdigit():
                    sg.popup_error("Рік, ціна та пробіг повинні бути числами")
                    continue

                car = {
                    "brand": values["brand"].strip(),
                    "model": values["model"].strip(),
                    "year": int(values["year"]),
                    "price": int(values["price"]),
                    "mileage": int(values["mileage"]),
                    "sold": False
                }

                core.add_car(cars, car)
                update_list(window, cars)
                sg.popup("Машину додано")

            except Exception as e:
                sg.popup_error(str(e))

        elif event == "cars":
            indexes = window["cars"].get_indexes()
            if indexes:
                car = cars[indexes[0]]

                window["brand"].update(car["brand"])
                window["model"].update(car["model"])
                window["year"].update(str(car["year"]))
                window["price"].update(str(car["price"]))
                window["mileage"].update(str(car["mileage"]))

        elif event == "edit":
            indexes = window["cars"].get_indexes()
            if not indexes:
                sg.popup_error("Оберіть машину")
                continue

            try:
                if not values["brand"].strip() or not values["model"].strip():
                    sg.popup_error("Введіть марку та модель")
                    continue
                if not values["year"].isdigit() or not values["price"].isdigit() or not values["mileage"].isdigit():
                    sg.popup_error("Неправильні числові дані")
                    continue

                number = indexes[0] + 1

                car = {
                    "brand": values["brand"].strip(),
                    "model": values["model"].strip(),
                    "year": int(values["year"]),
                    "price": int(values["price"]),
                    "mileage": int(values["mileage"])
                }

                core.edit_car(cars, number, car)
                update_list(window, cars)
                sg.popup("Машину змінено")

            except Exception as e:
                sg.popup_error(str(e))
        elif event == "delete":
            indexes = window["cars"].get_indexes()
            if not indexes:
                sg.popup_error("Оберіть машину")
                continue

            number = indexes[0] + 1

            if sg.popup_yes_no("Видалити цю машину?") == "Yes":
                core.delete_car(cars, number)
                update_list(window, cars)
        elif event == "show":
            update_list(window, cars)
        elif event == "search_button":
            brand = values["search"].strip().lower()
            if not brand:
                sg.popup_error("Введіть марку")
                continue

            found = []

            for i in range(len(cars)):
                if cars[i]["brand"].lower() == brand:
                    found.append(
                        str(i + 1) + ". " +
                        cars[i]["brand"] + " " +
                        cars[i]["model"] + " | " +
                        str(cars[i]["price"]) + "$"
                    )

            window["cars"].update(values=found)

            if not found:
                sg.popup("Машину не знайдено")

        elif event == "available" or event == "sold" or event == "all":
            filtered = []

            for i in range(len(cars)):
                if event == "available" and not cars[i]["sold"]:
                    filtered.append(i)
                elif event == "sold" and cars[i]["sold"]:
                    filtered.append(i)
                elif event == "all":
                    filtered.append(i)

            old_cars = []

            for i in filtered:
                old_cars.append(cars[i])

            update_list(window, old_cars)

        elif event == "change_sold":
            indexes = window["cars"].get_indexes()

            if not indexes:
                sg.popup_error("Оберіть машину")
                continue

            number = indexes[0] + 1
            core.change_sold(cars, number)
            update_list(window, cars)

        elif event == "info":
            indexes = window["cars"].get_indexes()

            if not indexes:
                sg.popup_error("Оберіть машину")
                continue

            car = cars[indexes[0]]

            if car["sold"]:
                status = "Продано"
            else:
                status = "В наявності"

            sg.popup(
                "Марка: " + car["brand"],
                "Модель: " + car["model"],
                "Рік: " + str(car["year"]),
                "Ціна: " + str(car["price"]) + "$",
                "Пробіг: " + str(car["mileage"]) + " км",
                "Статус: " + status
            )

        elif event == "sort":
            for i in range(len(cars)):
                for j in range(len(cars) - 1 - i):
                    if cars[j]["price"] > cars[j + 1]["price"]:
                        cars[j], cars[j + 1] = cars[j + 1], cars[j]

            functions.write_cars(cars)
            update_list(window, cars)

        elif event == "discount":
            indexes = window["cars"].get_indexes()
            if not indexes:
                sg.popup_error("Оберіть машину")
                continue

            percent = sg.popup_get_text("Введіть відсоток знижки")

            if percent and percent.isdigit():
                number = indexes[0]
                percent = int(percent)

                if percent < 1 or percent > 99:
                    sg.popup_error("Знижка має бути від 1 до 99")
                elif cars[number]["sold"]:
                    sg.popup_error("Машина вже продана")
                else:
                    old_price = cars[number]["price"]
                    cars[number]["price"] = old_price * (100 - percent) // 100

                    functions.write_cars(cars)
                    update_list(window, cars)
                    sg.popup("Нова ціна:", cars[number]["price"], "$")
            else:
                sg.popup_error("Неправильне значення")

        elif event == "range":
            text = sg.popup_get_text("Введіть мінімальну та максимальну ціну через пробіл")
            if text:
                data = text.split()
                if len(data) == 2 and data[0].isdigit() and data[1].isdigit():
                    low = int(data[0])
                    high = int(data[1])
                    filtered = []

                    for i in range(len(cars)):
                        if low <= cars[i]["price"] <= high:
                            filtered.append(cars[i])

                    update_list(window, filtered)

                else:
                    sg.popup_error("Неправильний діапазон")

        elif event == "brands":
            counts = {}

            for car in cars:
                brand = car["brand"]
                if brand in counts:
                    counts[brand] += 1
                else:
                    counts[brand] = 1

            result = ""

            for brand in counts:
                result += brand + " - " + str(counts[brand]) + "\n"

            sg.popup(result if result else "Список машин порожній")

        elif event == "stats":
            if len(cars) == 0:
                sg.popup("Список машин порожній")
            else:
                sold_count = 0
                total_price = 0
                sold_sum = 0

                for car in cars:
                    total_price += car["price"]
                    if car["sold"]:
                        sold_count += 1
                        sold_sum += car["price"]

                sg.popup( "Всього машин: " + str(len(cars)), "Продано: " + str(sold_count),
                    "В наявності: " + str(len(cars) - sold_count),  "Середня ціна: " + str(total_price // len(cars)) + "$",
                    "Сума продажів: " + str(sold_sum) + "$"
                )
        elif event == "clear":
            if sg.popup_yes_no("Видалити всі машини?") == "Yes":
                cars.clear()
                functions.write_cars(cars)
                update_list(window, cars)

    window.close()


if __name__ == "__main__":
    main()
