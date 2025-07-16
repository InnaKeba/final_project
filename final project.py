from collections import UserDict
from datetime import datetime, timedelta
import pickle
import re


#Серелізація
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()




#опис класів

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
        if not (len(value) == 10):
            raise ValueError("Phone number must be 10 digits") 
        super().__init__(value)
class Birthday(Field):
    def __init__(self, value):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        self.value = birthday


#додала класс email та перевірку формата  його введення

class Email(Field):
    def __init__(self, value):
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            raise ValueError("Invalid email format")
        super().__init__(value)


class Address(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Address cannot be empty")
        super().__init__(value)



# обов`язкові поля для створення контакту - name та phone, інше можна додати пізніше. якщо ми хочемо щоб була
# можливість ввести їх відразу треба переробити. напевно треба спитати у ментора яка вимога тут

class Record:
    def __init__(self, name):
        self.name = Name(name)     # обов'язкове поле
        self.phones = []           # список телефонів
        self.email = None          # email можна додати пізніше
        self.address = None        # адреса — теж пізніше
        self.birthday = None       # день народження — за бажанням





    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    

    def add_phone(self, phone):
        self.phones.append(Phone(phone))   
   
    def add_birthday (self, birthday):
        self.birthday= Birthday(birthday)
    
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break
    def edit_phone(self, old_phone: str, new_phone: str):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
            break

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    def find(self, name):
        return self.data.get(name)
    
    
    
    
    
    def delete (self, name):
        if name in self.data:
            del self.data[name]
    
    # def get_upcoming_birthdays(self):
    #     today = datetime.today().date()
    #     upcoming_birthdays_this_week = []
        
    #     for user in self.data.values():
    #         name = user.name.value
    #         birthday = datetime.strptime(user.name.value, "%d.%m.%Y").date()
    #         birthday_this_year = birthday.replace(year=today.year)

    #         if birthday_this_year < today:
    #             birthday_this_year = birthday_this_year.replace(year=today.year + 1)

    #         delta_days = (birthday_this_year - today).days

    #         if 0 <= delta_days <= 7:
    #             congratulation_date = birthday_this_year

    #             if congratulation_date.weekday() == 5:
    #                 congratulation_date += timedelta(days=2)
    #             elif congratulation_date.weekday() == 6:
    #                 congratulation_date += timedelta(days=1)

    #             upcoming_birthdays_this_week.append({
    #                 "name": name,
    #                 "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
    #             })

    #     return upcoming_birthdays_this_week



def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Enter user name"
        except IndexError:
            return "Enter user name"
    return inner
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args



#вимога про контакти: add_contact - додеє контакт в книгу контактів , сhange_contact - редагує, delete  - видаляє.
#  це обовязкові функції згідно завдання. усі інші були в дз я залишила, та окремо додала функцію 
# додати имейл та адресу - це у випадку, якщо при створенні контакту ми відразу не вказали ці данні і 
# хочемо пізніше їх додати


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message
@input_error
def change_contact(args, book: AddressBook):
       name, new_phone = args
       record = book.find(name)
       if record:
           record.phones = []  
           record.add_phone(new_phone)
           return "Contact changed."
       else:
           return "Contact not found."
@input_error
def show_phone(name, book: AddressBook):
    if book.find(name):
        return ", ".join([phone.value for phone in book.find(name).phones])
    else:
        return "Contact not found"
@input_error
def show_all(book: AddressBook):
    result = ""
    for record in book.data.values():  # тут отримуємо всі записи
        phones = ", ".join(phone.value for phone in record.phones)
        result += f"{record.name.value}: {phones}\n"
    return result.strip() 

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        return f"Contact '{name}' not found."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}"
    elif record:
        return f"{name} has no birthday saved."
    else:
        return f"Contact '{name}' not found."

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays this week."

    lines = []
    for day, names in upcoming.items():
        line = f"{day}: {', '.join(names)}"
        lines.append(line)

    return "\n".join(lines)

@input_error
def delete(args, book: AddressBook):
    name = args[0]
    if book.find(name):
        book.delete(name)
        return f"Contact '{name}' deleted."
    else:
        return f"Contact '{name}' not found."
    
@input_error
def add_email(args, book: AddressBook):
    name, email = args
    record = book.find(name)
    if record:
        record.email = Email(email)
        return f"Email added for {name}."
    return "Contact not found."

@input_error
def add_address(args, book: AddressBook):
    name, address = args
    record = book.find(name)
    if record:
        record.address = Address(address)
        return f"Address added for {name}."
    return "Contact not found."


def show_help(): #додано help
    return """
📖 Доступні команди для ContactBot:

• add [ім'я] [телефон]              – додати новий контакт
• change [ім'я] [новий телефон]     – змінити номер телефону
• phone [ім'я]                      – показати номер телефону
• all                               – показати всі контакти
• add-birthday [ім'я] [дата]        – додати день народження
• show-birthday [ім'я]              – показати день народження
• birthdays                         – список хто святкує цього тижня
• add-email [ім'я] [email]          – додати email
• add-address [ім'я] [адреса]       – додати адресу
• delete [ім'я]                     – видалити контакт
• help                              – показати цей список команд
• close / exit                      – завершити роботу
"""


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")



# десь сюди команду Help (не впевнена),  спочатку зверху прописати її  функцію, а потім сюди додати 

        elif command == "help": #додала виклик команди help
            print(show_help())

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print (show_phone(args[0], book))

        elif command == "all":
            print (show_all (book))

        elif command == "add-birthday":
            print (add_birthday (args, book))

        elif command == "show-birthday":
            print (show_birthday (args, book))

        elif command == "birthdays":
            print (birthdays (args, book))

        elif command == "add-email":
            print(add_email(args, book))

        elif command == "add-address":
            print(add_address(args, book))    
        
        elif command == "delete":
            print ( delete (args, book))    

        else:
            print("Invalid command.")
        
if __name__ == "__main__":
    main()      

    