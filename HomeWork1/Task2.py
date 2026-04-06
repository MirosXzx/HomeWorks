def get_cats_info(path):
    try:
        cats = []

        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                cat_id, name, age = line.strip().split(",")

                cats.append({
                    "id": cat_id,
                    "name": name,
                    "age": age
                })

        print(cats)

    except FileNotFoundError:
        print("Файл не знайдено")
    except Exception as e:
        print(f"Помилка: {e}")


# запуск
get_cats_info("cats.txt")