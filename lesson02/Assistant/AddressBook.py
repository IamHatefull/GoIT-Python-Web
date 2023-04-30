import json, re
from collections import UserDict
from datetime import datetime, timedelta, date

class AddressBook(UserDict):
    
    '''Все контакты будут иметь вид:
    'имя контакта1' : { 'address' : 'адрес контакта', 'phone' : 'номер(пока что один и типа str)',
    'email' : 'електронная почта', 'birthday' : 'день рождения'},
    'имя контакта2' :{следующие данные},'''
    
    contacts = {}

    def __repr__(self):
        pass

    def serialize(self):
        with open('data.json', 'w') as file:
            json.dump(self.contacts, file)

    def deserialize(self):
        with open('data.json', 'r') as file:
            self.contacts = json.load(file)

    #Добавление контакта. Не добавив контакт через эту функ добавить другую информацию не вийдет
    def add_contact(self, name, phone_number, birthday): #Correction добавил день рождения, чтобы убрать баг с поиском n_days
        self.contacts[name] = {
            'Address' : None,
            'Phone' : phone_number,
            'Email' : None,
            'Birthday' : birthday
            }

    #Добавление адреса контакта
    #Добавить валидацию ввода   <-- Task!
    def add_address(self, name, address):
        self.contacts[name]['Address'] = address

    #Добавление електронной почты
    #Добавить валидацию ввода     <--Task
    def add_email(self, name, email):
        self.contacts[name]['Email'] = email

    #Добавление дня рождения. Только стринг. При будущих манипуляциях с датой переводим стринг в тип date
    def add_birthday(self, name, birthday):
        self.contacts[name]['Birthday'] = birthday

    # Выводит список контактов у которых день рождения через n_days от текущей даты
    def nearby_birthday(self, n_days):
        
        now = datetime.now().timetuple().tm_yday # Количество дней с начала года сегодня
        future = now + int(n_days) # Количество дней с начала года с учётом введённого числа
        new_year_future = 0
        if future > 365:
            new_year_future = future - 365
            future = 365
        fut_list = []
    
        for key, value in self.contacts.items(): # Перебираем словари по именам
            for i, j in value.items(): # Заходим у внутренний словарь чтоб найти дату дня рождения
                if i == 'Birthday':
                    s = datetime.strptime(j, '%d.%m.%Y').timetuple().tm_yday # Преобразуем др в число дней с начала года
                    if s <= future and s >= now or s >= 1 and s <= new_year_future:
                        fut_list.append(key)
                    else:
                        continue
                else:
                    continue
        if fut_list != []:
            print(f"Following users are celebrating birthdays in the next {n_days} days:")
        else:
            print(f'No contacts are celebrating their birthday in the next {n_days} days')
        result = ", ".join(fut_list)
        return result
    
    #Редакция контакта. можно разделить на отдельные функции
    def change_contact(self, name, address, phone, email, birthday):
        self.contacts[name] = {
            'Address' : address,
            'Phone' : phone,
            'Email' : email,
            'Birthday' : birthday
            }

    #Поиск по контактам. пока не знаю. будем только по имени или по всем параметрам????
    def search(self, string):
        for key, value in self.contacts.items():
            if key == string:
                return self.contacts[key]
            else:
                for val in value.values():
                    if val == string:
                        return self.contacts[key]
                    else:
                        continue

    #Удаление контакта
    def delete_contact(self, name):
        self.contacts.pop(name)

    #Правильность ввода номера телефона
    def validate_phone(self, phone: str):
        san_phone = re.sub(r'[-)( ]', '', phone)
        if re.match('^\\+380\d{9}$', san_phone):
            return True
        else:
            return False

    #Правильность ввода электронной почты
    def validate_email(self, email: str):
        if re.match('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', email):
            return True
        else:
            return False

    #правильность ввода даты
    def validate_birthday(self, date):
        if re.match('^\d{2}.\d{2}.\d{4}$', date): #Correction Исправил с чёрточек на точки
            return True
        else:
            return False
