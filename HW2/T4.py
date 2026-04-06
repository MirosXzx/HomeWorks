def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "User not found."
        except IndexError:
            return "Enter user name."
    return inner


contacts = {}


@input_error
def add_contact(args):
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def get_phone(args):
    name = args[0]
    return contacts[name]


@input_error
def show_all(args):
    result = ""
    for name, phone in contacts.items():
        result += f"{name}: {phone}\n"
    return result if result else "No contacts."


def main():
    while True:
        command = input("Enter a command: ").strip().lower()

        if command == "exit" or command == "close":
            print("Good bye!")
            break

        elif command.startswith("add"):
            args = command.split()[1:]
            print(add_contact(args))

        elif command.startswith("phone"):
            args = command.split()[1:]
            print(get_phone(args))

        elif command == "all":
            print(show_all([]))

        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()