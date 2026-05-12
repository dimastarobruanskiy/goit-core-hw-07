from classes import Record


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if "unpack" in str(e):
                return "Invalid command format. Please provide the correct arguments."
            return str(e)
        except IndexError:
            return "Enter user name."
        except KeyError:
            return "Contact not found."
        except AttributeError:
            return "Contact not found."
    return inner

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

def show_all(book):
    if not book.data:
        return "No contacts found."

    result = ""
    for record in book.data.values():
        result += str(record) + "\n"

    return result.strip()

@input_error
def delete_contact(args, book):
    name = args[0]
    book.delete(name)
    return "Deleted."

@input_error
def add_birthday(args, book):
    name, birthday = args

    record = book.find(name)

    record.add_birthday(birthday)

    return "Birthday added."

@input_error
def show_birthday(args, book):
    name = args[0]

    record = book.find(name)
    
    if record is None:
        raise KeyError  # Це коректно передасть помилку декоратору, який поверне "Contact not found."
        
    if record.birthday is None:
        return f"No birthday saved for {name}."

    return f"{record.name.value}'s birthday is {record.birthday.value}."

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No upcoming birthdays."

    result = "Upcoming birthdays:\n"
    for item in upcoming:
        result += f"{item['name']} - {item['birthday']}\n"

    return result.strip()