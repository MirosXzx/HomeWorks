import pickle
import os


class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name, phone):
        self.contacts.append({"name": name, "phone": phone})

    def show_contacts(self):
        if not self.contacts:
            print("Адресная книга пуста")
            return

        for contact in self.contacts:
            print(f"{contact['name']} - {contact['phone']}")


def save_data(book, filename="addressbook.pkl"):
    try:
        with open(filename, "wb") as f:
            pickle.dump(book, f)
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")


def load_data(filename="addressbook.pkl"):
    if not os.path.exists(filename):
        return AddressBook()

    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception:
        print("Файл повреждён. Создаётся новая книга.")
        return AddressBook()


def main():
    book = load_data()

    while True:
        print("\n1 - добавить контакт")
        print("2 - показать контакты")
        print("0 - выход")

        choice = input("Выбор: ")

        if choice == "1":
            name = input("Имя: ").strip()
            phone = input("Телефон: ").strip()
            if name and phone:
                book.add_contact(name, phone)
            else:
                print("Пустые данные не допускаются")

        elif choice == "2":
            book.show_contacts()

        elif choice == "0":
            save_data(book)
            print("Данные сохранены. Выход...")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()