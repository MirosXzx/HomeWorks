from collections import UserDict
from datetime import datetime, timedelta
import pickle
from abc import ABC, abstractmethod


# ================= VIEW =================
class View(ABC):

    @abstractmethod
    def show_message(self, message: str):
        pass

    @abstractmethod
    def show_contact(self, contact: dict):
        pass

    @abstractmethod
    def show_all_contacts(self, contacts: list):
        pass

    @abstractmethod
    def show_help(self):
        pass


class ConsoleView(View):

    def show_message(self, message: str):
        print(message or "")

    def show_contact(self, contact: dict):
        if not contact:
            print("Contact not found")
            return

        phones = "; ".join(contact.get("phones", []))
        bday = contact.get("birthday", "No birthday")
        print(f"{contact.get('name')}: {phones} | Birthday: {bday}")

    def show_all_contacts(self, contacts: list):
        if not contacts:
            print("No contacts.")
            return

        for c in contacts:
            self.show_contact(c)

    def show_help(self):
        print("""
Commands:
add name phone
change name old new
phone name
all
add-birthday name DD.MM.YYYY
show-birthdays
help
exit / close
        """)


# ================= RESULT WRAPPER =================
def ok(data=None, message="OK"):
    return {"status": "ok", "data": data, "message": message}


def error(message):
    return {"status": "error", "message": message}


# ================= DOMAIN =================
class Phone:
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone must be 10 digits")
        self.value = value


class Birthday:
    def __init__(self, value):
        datetime.strptime(value, "%d.%m.%Y")
        self.value = value

    @property
    def date(self):
        return datetime.strptime(self.value, "%d.%m.%Y").date()


class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old, new):
        for i, p in enumerate(self.phones):
            if p.value == old:
                self.phones[i] = Phone(new)
                return
        raise ValueError("Phone not found")

    def set_birthday(self, bday):
        self.birthday = Birthday(bday)

    def to_dict(self):
        return {
            "name": self.name,
            "phones": [p.value for p in self.phones],
            "birthday": self.birthday.value if self.birthday else "No birthday"
        }


# ================= ADDRESS BOOK =================
class AddressBook(UserDict):

    def add(self, record):
        self.data[record.name] = record

    def get(self, name):
        return self.data.get(name)

    def all(self):
        return [r.to_dict() for r in self.data.values()]

    def upcoming_birthdays(self):
        today = datetime.today().date()
        result = []

        for r in self.data.values():
            if not r.birthday:
                continue

            bday = r.birthday.date

            try:
                next_bday = bday.replace(year=today.year)
            except ValueError:
                next_bday = bday.replace(year=today.year, month=3, day=1)

            if next_bday < today:
                next_bday = next_bday.replace(year=today.year + 1)

            if next_bday.weekday() == 5:
                next_bday += timedelta(days=2)
            elif next_bday.weekday() == 6:
                next_bday += timedelta(days=1)

            if 0 <= (next_bday - today).days <= 7:
                result.append({
                    "name": r.name,
                    "phones": [p.value for p in r.phones],
                    "birthday": r.birthday.value
                })

        return result


# ================= STORAGE =================
def save(book):
    with open("book.pkl", "wb") as f:
        pickle.dump(book, f)


def load():
    try:
        with open("book.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


# ================= SAFE PARSE =================
def parse_input(text):
    parts = text.strip().split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]


# ================= COMMANDS =================
def add(args, book):
    if len(args) != 2:
        return error("Usage: add name phone")

    name, phone = args
    r = book.get(name)

    if not r:
        r = Record(name)
        book.add(r)

    try:
        r.add_phone(phone)
        return ok(message="Contact added")
    except Exception as e:
        return error(str(e))


def change(args, book):
    if len(args) != 3:
        return error("Usage: change name old new")

    name, old, new = args
    r = book.get(name)

    if not r:
        return error("Contact not found")

    try:
        r.edit_phone(old, new)
        return ok(message="Updated")
    except Exception as e:
        return error(str(e))


def phone(args, book):
    if len(args) != 1:
        return error("Usage: phone name")

    r = book.get(args[0])
    if not r:
        return error("Not found")

    return ok(r.to_dict())


def all_contacts(book):
    return ok(book.all())


def add_birthday(args, book):
    if len(args) != 2:
        return error("Usage: add-birthday name date")

    name, bday = args
    r = book.get(name)

    if not r:
        return error("Contact not found")

    try:
        r.set_birthday(bday)
        return ok(message="Birthday added")
    except Exception as e:
        return error(str(e))


def birthdays(book):
    return ok(book.upcoming_birthdays())


# ================= MAIN =================
def main():
    book = load()
    view = ConsoleView()

    while True:
        cmd, args = parse_input(input("Enter command: "))

        if not cmd:
            view.show_message("Enter command")
            continue

        if cmd in ["exit", "close"]:
            save(book)
            view.show_message("Bye!")
            break

        elif cmd == "add":
            res = add(args, book)
            view.show_message(res["message"])

        elif cmd == "change":
            res = change(args, book)
            view.show_message(res["message"])

        elif cmd == "phone":
            res = phone(args, book)
            if res["status"] == "ok":
                view.show_contact(res["data"])
            else:
                view.show_message(res["message"])

        elif cmd == "all":
            res = all_contacts(book)
            view.show_all_contacts(res["data"])

        elif cmd == "add-birthday":
            res = add_birthday(args, book)
            view.show_message(res["message"])

        elif cmd == "show-birthdays":
            res = birthdays(book)
            view.show_all_contacts(res["data"])

        elif cmd == "help":
            view.show_help()

        else:
            view.show_message("Unknown command")


if __name__ == "__main__":
    main()