def total_salary(path):
    total = 0
    count = 0

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                name, salary = line.strip().split(",")
                total += int(salary)
                count += 1

        average = total / count if count > 0 else 0

        print(f"Загальна сума заробітної плати: {total}")
        print(f"Середня заробітна плата: {average}")

    except FileNotFoundError:
        print("Файл не знайдено")
    except Exception as e:
        print(f"Помилка: {e}")


# запуск
total_salary("salary.txt")