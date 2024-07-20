from collections import UserDict

# Базовий клас для полів запису
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для зберігання імені контакту. Ім'я не може бути порожнім
class Name(Field):
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

# Клас для зберігання номера телефону. Має валідацію формату (10 цифр)
class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

# Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    # Метод для додавання телефону
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Метод для видалення телефону
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    # Метод для редагування телефону
    def edit_phone(self, old_phone, new_phone):
        if not new_phone.isdigit() or len(new_phone) != 10:
            raise ValueError("Phone number must be 10 digits.")
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError("Old phone number not found.")

    # Метод для пошуку телефону
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    # Метод для виведення інформації про запис у вигляді рядка
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

# Клас для зберігання та управління записами. Наслідується від UserDict
class AddressBook(UserDict):
    # Метод для додавання запису
    def add_record(self, record):
        self.data[record.name.value] = record

    # Метод для пошуку запису за ім'ям
    def find(self, name):
        return self.data.get(name, None)

    # Метод для видалення запису за ім'ям
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    # Метод для виведення всіх записів у вигляді рядка
    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

# Тестування функціональності

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
print(book)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

# Виведення запису John після редагування телефону
print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name.value}: {found_phone.value}")  # Виведення: John: 5555555555

# Видалення запису Jane
book.delete("Jane")

# Виведення всіх записів після видалення Jane
print(book)
