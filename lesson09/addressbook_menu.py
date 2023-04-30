import re
from datetime import datetime
from sqlalchemy import or_

from AB_model import Contact, Session


# Function to return str respond if user enter wrong command.
wrong = lambda: 'Please retype the command correctly'


def validate_phone(phone: str):
    '''Function to check if phone number is valid.
    Example: phone = +380778092314'''
    san_phone = re.sub(r'[-)( ]', '', phone)
    if re.match('^\\+380\d{9}$', san_phone):
        return True
    else:
        return False


def validate_email( email: str):
    ''' Function to check if email is valid'''
    if re.match('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', email):
        return True
    else:
        return False


def validate_birthday(date):
    ''' Function to check if birthday date is valid.
    Proper format is 2002.01.01'''
    if re.match('^\d{4}.\d{2}.\d{2}$', date): 
        return True
    else:
        return False



def add_contact(): 
    ''' Function to add contact to database.
    All contact information are taken from console input and after validation added to database.'''

    session = Session()
    name = input('Enter Name: ') 
    address = input('Enter Address: ')
    email = input('Enter Email: ')
    phone = input('Enter Phone number in format +380123456789: ') 
    birthday = input('Enter Birthday in format 1990.01.01: ')


    if validate_birthday(birthday) and validate_phone(phone) and validate_email(email): 
        
        contact = Contact(name,address, email, phone, datetime.strptime(birthday, "%Y.%m.%d").date())
        session.add(contact)

        session.commit()
        session.close()
        
        return f'Contact {name} with phone number {phone} and birthday {birthday} created.'
    else:
        return f'Incorrect data. Try again'


def change_contact():
    ''' Function to change contact parameters in database.
    Contact name can NOT be changed. Variable name used to find contact in database and after that input data become new contact info'''

    name = input('Enter Name: ')
    address = input('Enter Address: ')
    phone = input('Enter Phone number: ')
    email = input('Enter Email: ')
    birthday = input('Enter Birthday: ')

    if validate_birthday(birthday) and validate_email(email) and validate_phone(phone):
        session = Session()

        contact = session.query(Contact).filter(Contact.name == name).first()
        contact.address = address
        contact.phone = phone
        contact.email = email
        contact.birthday = datetime.strptime(birthday, "%Y.%m.%d").date()

        session.commit()
        session.close()

        return f'{name}`s :\n Address: {address}, Phone: {phone}, Email: {email}, Birthday: {birthday}'
    else:
        return 'Incorrect data (email, phone number or birthday)'


def find_contact():
    ''' Function to find contact by any information. Return contact info or error massage'''

    session = Session()
    info = input('Enter contact info: ')
    contacts = session.query(Contact).filter(or_(Contact.name == info, Contact.address == info, Contact.email == info, Contact.phone == info, Contact.birthday == info)).all()
    session.close()
    
    if contacts:
        return str(contacts)
    else:
        return 'Wrong info! Try again.'


def nearby_birthday():
    ''' Function to show contacts, who have birthday in n number of days'''

    n_days = input('Enter number of days')
    now = datetime.now().timetuple().tm_yday 
    future = now + int(n_days) 
    new_year_future = 0
    
    if future > 365:
        new_year_future = future - 365
        future = 365
    fut_list = []
    
    session = Session()
    contacts = session.query(Contact).all()

    for contact in contacts:
        s = datetime.strptime(contact.birthday , '%d.%m.%Y').timetuple().tm_yday
        if s <= future and s >= now or s >= 1 and s <= new_year_future:
            fut_list.append(contact.name)
        else:
            continue

    if fut_list != []:
        print(f"Following users are celebrating birthdays in the next {n_days} days:")
    else:
        print(f'No contacts are celebrating their birthday in the next {n_days} days')
    result = ", ".join(fut_list)
    return result


def delete_contact():
    ''' Function to delete contact. Use any information to find contact and then delete it.'''

    session = Session()
    info = input('Enter contact info to delete: ')
    session.query(Contact).filter(or_(Contact.name == info, Contact.address == info, Contact.email == info, Contact.phone == info, Contact.birthday == info)).delete(synchronize_session = "fetch")
    session.commit()
    session.close()
    return 'Contact was deleted!'


def show_contacts():
    ''' Function to show all contacts from database'''

    session = Session()
    all_contacts = session.query(Contact).all()
    for contact in all_contacts:
        print(contact)
    session.close()
    return '__End of contact list__'


OPERATIONS = {
    'add contact' : add_contact,
    'change contact' : change_contact,
    'find contact' : find_contact,
    'near birthday' : nearby_birthday,
    'delete contact' : delete_contact,
    'show contacts' : show_contacts
    }

def get_handler(operator):
    if not OPERATIONS.get(operator):
        return wrong
    return OPERATIONS[operator]

    
def main():
    #Start of the cli
    print('Hello, User! Welcome to our CLI-bot. Enter "help" in case you need to see the commands again') 

    while True:
        command = input('Enter your command: ')
        if command == '.' or command == 'exit' or command == 'close':
            print('Goodbye, User!')
            break
        handler = get_handler(command)
        answer = handler()
        print (answer)


if __name__ == '__main__':
    main()