from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone must be 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            date_obj = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        super().__init__(value)
        self.date = date_obj


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if phone not in [p.value for p in self.phones]:
            self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones)
        bday = self.birthday.value if self.birthday else "No birthday"
        return f"{self.name.value}: {phones} | Birthday: {bday}"


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bday = record.birthday.date

            # --- определяем дату в этом году ---
            try:
                next_birthday = bday.replace(year=today.year)
            except ValueError:
                next_birthday = bday.replace(year=today.year, month=3, day=1)

            if next_birthday < today:
                try:
                    next_birthday = next_birthday.replace(year=today.year + 1)
                except ValueError:
                    next_birthday = next_birthday.replace(year=today.year + 1, month=3, day=1)

            # --- перенос на рабочий день (ВАЖНО: ДО фильтра) ---
            if next_birthday.weekday() == 5:
                next_birthday += timedelta(days=2)
            elif next_birthday.weekday() == 6:
                next_birthday += timedelta(days=1)

            # --- теперь фильтр ---
            delta_days = (next_birthday - today).days

            if 0 <= delta_days <= 7:
                result.append({
                    "name": record.name.value,
                    "date": next_birthday
                })

        # сортировка по дате (правильно)
        result.sort(key=lambda x: x["date"])

        # форматирование строки
        return [
            {"name": r["name"], "birthday": r["date"].strftime("%d.%m.%Y")}
            for r in result
        ]


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Not enough arguments"
        except KeyError:
            return "Contact not found"
    return inner


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)

    record.add_phone(phone)
    return "Contact added/updated."


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)

    if record is None:
        raise KeyError

    for i, phone in enumerate(record.phones):
        if phone.value == old_phone:
            record.phones[i] = Phone(new_phone)
            return "Contact updated."

    return "Phone not found."


@input_error
def show_phone(args, book):
    record = book.find(args[0])

    if record is None:
        raise KeyError

    return ", ".join(p.value for p in record.phones)


@input_error
def show_all(args, book):
    return "\n".join(str(r) for r in book.data.values())


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)

    if record is None:
        raise KeyError

    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def birthdays(args, book):
    result = book.get_upcoming_birthdays()
    return "\n".join(f"{r['name']}: {r['birthday']}" for r in result)


def parse_input(user_input):
    return user_input.strip().split()


def main():
    book = AddressBook()

    while True:
        user_input = input("Enter command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            break

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Unknown command")


if __name__ == "__main__":
    main()