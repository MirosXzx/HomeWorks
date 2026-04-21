from collections import UserDict
from datetime import datetime, timedelta
import pickle


# ================= ДЕКОРАТОР =================
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
        except AttributeError:
            return "Contact not found"
    return inner


# ================= ПОЛЯ =================
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


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
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

    @property
    def date(self):
        return datetime.strptime(self.value, "%d.%m.%Y").date()


# ================= RECORD =================
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Old phone not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        bday = self.birthday.value if self.birthday else "No birthday"
        return f"{self.name.value}: {phones} | Birthday: {bday}"


# ================= ADDRESS BOOK =================
class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bday = record.birthday.date

            try:
                next_birthday = bday.replace(year=today.year)
            except ValueError:
                next_birthday = bday.replace(year=today.year, month=3, day=1)

            if next_birthday < today:
                try:
                    next_birthday = next_birthday.replace(year=today.year + 1)
                except ValueError:
                    next_birthday = next_birthday.replace(year=today.year + 1, month=3, day=1)

            if next_birthday.weekday() == 5:
                next_birthday += timedelta(days=2)
            elif next_birthday.weekday() == 6:
                next_birthday += timedelta(days=1)

            delta = (next_birthday - today).days

            if 0 <= delta <= 7:
                result.append({
                    "name": record.name.value,
                    "date": next_birthday
                })

        result.sort(key=lambda x: x["date"])

        return [
            f"{r['name']}: {r['date'].strftime('%d.%m.%Y')}"
            for r in result
        ]


# ================= PICKLE =================
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


# ================= HANDLERS =================
@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)

    record.add_phone(phone)
    return "Contact added."


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)

    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)

    return "; ".join(p.value for p in record.phones)


@input_error
def show_all(args, book):
    if not book.data:
        return "No contacts."
    return "\n".join(str(r) for r in book.data.values())


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)

    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthdays(args, book):
    result = book.get_upcoming_birthdays()
    return "\n".join(result) if result else "No upcoming birthdays."


# ================= MAIN =================
def parse_input(user_input):
    return user_input.split()


def main():
    book = load_data()

    while True:
        user_input = input("Enter command: ").strip()

        if not user_input:
            print("Enter command")
            continue

        command, *args = parse_input(user_input)
        command = command.lower()

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
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

        elif command == "show-birthdays":
            print(show_birthdays(args, book))

        else:
            print("Unknown command")


if __name__ == "__main__":
    main()