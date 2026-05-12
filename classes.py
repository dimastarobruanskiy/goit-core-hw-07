from collections import UserDict
from datetime import datetime,timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)

    @staticmethod
    def validate(value):
        return isinstance(value, str) and value.isdigit() and len(value) == 10

class Birthday(Field):
    def __init__(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    def add_birthday(self, birthday_string):
        self.birthday = Birthday(birthday_string)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)

        if phone_to_edit is None:
            raise ValueError("Old phone not found")

        new_phone_obj = Phone(new_phone)

        self.phones.remove(phone_to_edit)
        self.phones.append(new_phone_obj)
        
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone):
        original_len = len(self.phones)
        self.phones = [p for p in self.phones if p.value != phone]

        if len(self.phones) == original_len:
            raise ValueError("Phone not found")

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        
        if self.birthday:
            birthday_str = f", birthday: {self.birthday.value}"
        else:
            birthday_str = ""
            
        return f"Contact name: {self.name.value}, phones: {phones}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Contact not found")
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue
            
            bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            
            try:
                bday_this_year = bday.replace(year=today.year)
            except ValueError:
                bday_this_year = bday.replace(year=today.year, day=28)
                
            if bday_this_year < today:
                try:
                    bday_this_year = bday.replace(year=today.year + 1)
                except ValueError:
                    bday_this_year = bday.replace(year=today.year + 1, day=28)
                    
            days_until_birthday = (bday_this_year - today).days
            
            if 0 <= days_until_birthday <= 7:
                congratulation_date = bday_this_year
                
                weekday = congratulation_date.weekday()
                if weekday == 5: # Субота
                    congratulation_date += timedelta(days=2)
                elif weekday == 6: # Неділя
                    congratulation_date += timedelta(days=1)
                
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "birthday": congratulation_date.strftime('%d.%m.%Y')
                })
                
        return upcoming_birthdays
        
    def __str__(self):
        if not self.data:
            return "Address book is empty"
        return "\n".join(str(record) for record in self.data.values())
    