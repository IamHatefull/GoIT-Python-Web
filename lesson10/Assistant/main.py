import os, time
from collections import Counter, OrderedDict #Correction добавил словарь
import shutil
from prettytable import PrettyTable
from pymongo import MongoClient

from redis_func import set_info, get_info, show_cache

try:
    from AddressBook import *
except:
    from .AddressBook import *


mongo_conn = 'mongodb+srv://borys26:v320@cluster0.iuejl.mongodb.net/MongoDatabase?retryWrites=true&w=majority'
    
AB = AddressBook()

wrong = lambda: 'Please retype the command correctly'


def add_contact(): #Correction добавил в добавление контакта день рождение с валидацией по дефолту
    name = input('Enter Name: ') #Correction отступ после двоеточия
    phone = input('Enter Phone number: ') #Correction отступ после двоеточия
    birthday = input('Enter Birthday in format 01.01.1990: ')
    if AB.validate_birthday(birthday) and AB.validate_phone(phone): 
        AB.add_contact(name, phone, birthday)
        return f'Contact {name} with phone number {phone} and birthday {birthday} created.'
    else:
        return f'Incorrect number. Try in format +380123456789' #Correction для наглядности с +380...


def add_email():
    name = input('Enter Name: ')#Correction отступ после двоеточия
    if not AB.contacts.get(name):
        return f'Contact {name} does not exist!'
    email = input('Enter Email: ')#Correction отступ после двоеточия
    if AB.validate_email(email):
        AB.add_email(name, email)
        return f'{name}`s email {email} has been saved'
    else:
        return f'Incorrect email'


def add_address():
    name =  input('Enter Name: ') #Correction отступ после двоеточия
    if not AB.contacts.get(name):
        return f'Contact {name} does not exist!'
    address = input('Enter Address: ') #Correction отступ после двоеточия
    AB.add_address(name, address)
    return f'{name}`s address is {address}'


def add_birthday():
    name = input('Enter Name: ') #Correction отступ после двоеточия
    if not AB.contacts.get(name):
        return f'Contact {name} does not exist!'
    birthday = input('Enter Birthday in format 01.01.1990: ') #Correction отступ после двоеточия
    print(birthday)
    if AB.validate_birthday(birthday):
        AB.add_birthday(name, birthday)
        return f'{name}`s birthday {birthday} has been saved'
    else:
        return f'Incorrect date'


def change_contact():
    name = input('Enter Name: ')#Correction отступ после двоеточия
    if not AB.contacts.get(name):
        return f'Contact {name} does not exist!'
    address = input('Enter Address: ')#Correction отступ после двоеточия
    phone = input('Enter Phone number: ')#Correction отступ после двоеточия
    email = input('Enter Email: ')#Correction отступ после двоеточия
    birthday = input('Enter Birthday: ')#Correction отступ после двоеточия
    if AB.validate_birthday(birthday) and AB.validate_email(email) and AB.validate_phone(phone):
        AB.change_contact(name, address, phone, email,birthday)
        return f'{name}`s :\n Address: {address}, Phone: {phone}, Email: {email}, Birthday: {birthday}'
    else:
        return 'Incorrect data (email, phone number or birthday)'#Correction отступ после data


def find_contact():
    return AB.search(input('Enter contact info: '))


def nearby_birthday():
    n_days = input('Enter number of days: ')
    return AB.nearby_birthday(n_days)


def delete_contact():
    name = input('Enter Name of the contact: ')
    if not AB.contacts.get(name):
        return f'Contact {name} does not exist!'
    AB.delete_contact(name)
    return f'Contact {name} was deleted!'


def show_contacts():
    pretty_contacts = PrettyTable()
    pretty_contacts.field_names = [
        'Name', 'Address', 'Phone', 'Email', 'Birthday']

    for k, v in AB.contacts.items():
        pretty_contacts.add_row(
            [k, v['Address'], v['Phone'], v['Email'], v['Birthday']])
    return pretty_contacts


def create_new_note():
    '''Create new note. Use input data as parameters for MongoDB record'''

    #Input data
    name = input('Enter name of the note: ')
    tags = input('Enter tags separated by space and starting with "#": ') 
    note = input('Enter text of your note: ') 

    #Changing str tags into tags list to input it in database
    tag_list = tags.split(' ')

    #Database connection
    client = MongoClient(mongo_conn)
    with client:
        db = client.MongoDatabase
        db.Notes.insert_one({'name': name, 'tags': tag_list, 'note': note})

    return f'You have created a note {name}' 


def delete_note():
    '''Delete note by it\'s name. If such note do not exist then return error'''

    #Name to search
    note_to_open = input('Enter Note name: ')

    #Database connection
    client = MongoClient(mongo_conn)
    with client:
        db = client.MongoDatabase
        by_name = db.Notes.find({'name': note_to_open})

        #if nothing was found return error in text
        if not by_name:
            return 'Note was not found! Try again'
        #else delete note and inform user about it
        else:
            db.Notes.delete_one({'name': note_to_open})
            return 'Note {note_to_open} was deleted!'


def read_note():
    '''Search note by it\'s name and print it. If such note do not exist then return error'''

    #Name to search
    note_to_open = input('Enter Note name: ')

    #get data from cache
    cache_key = f'note_search({note_to_open})'
    if get_info(cache_key):
        res = get_info(cache_key).split('\n')
        [print(data) for data in res]
        return '\nEnd of Note!'

    #Database connection
    client = MongoClient(mongo_conn)
    with client:
        db = client.MongoDatabase
        by_name = db.Notes.find({'name': note_to_open})

        #if nothing was found return error in text
        if not by_name:
            return 'Note was not found! Try again'
        #else print note and inform user about end of it
        else:
            res = [f"{data['name']}:\n{data['note']}" for data in by_name]
            #Add data to cache
            set_info(cache_key, '\n'.join(res))
            #print search result
            [print(data) for data in res]
            return '\nEnd of Note!'
    

def show_all_tags():
    '''Show all tags in database'''

    if get_info('show all tags'):
        return get_info('show all tags')

    #result list
    res = []
    
    #Database connection
    client = MongoClient(mongo_conn)
    with client:
        db = client.MongoDatabase
        notes = db.Notes.find({})
        #extend res list by tags from each record
        [res.extend(note['tags']) for note in notes]
    #Remove any duplicates from res
    res = list(dict.fromkeys(res))

    set_info('show all tags', str(res))
            
    print('Please see the list of all available tags below:')
    return (str(res)) 


def note_search():
    '''Search notes by it\'s name or tag and print it. If such notes do not exist then return error'''

    #Search info: tag or name.
    search_info = input('Please enter name of note or some tag you are looking for: ')

    #get data from cache
    cache_key = f'note_search({search_info})'
    if get_info(cache_key):
        res = get_info(cache_key).split('\n')
        [print(data) for data in res]
        return 'Search complete'

    #Database connection
    client = MongoClient(mongo_conn)
    with client:
        db = client.MongoDatabase
        by_name = db.Notes.find({'name': search_info})
        #if nothing was found by name then search by tag
        if not by_name:
            by_tag = db.Notes.find({'tags': search_info})
            #if nothing was found by tag then return error
            if not by_tag:
                return 'Note was not found! Try again'
            res = [f"{data['name']}:\n{data['note']}" for data in by_tag]
            #Add data to cache
            set_info(cache_key, '\n'.join(res))
            #print search result
            [print(data) for data in res]          
        else:
            res = [f"{data['name']}:\n{data['note']}" for data in by_name]
            #Add data to cache
            set_info(cache_key, '\n'.join(res))
            #print search result
            [print(data) for data in res]

    return 'Search complete'


def note_update():
    '''Note update. Search note by it\'s name, then ask about new note text and update it. If such notes do not exist then return error'''

    #Search name.
    note_to_open = input('Enter Note name: ')

    #Database connection
    client = MongoClient(mongo_conn)
    with client:
        db = client.MongoDatabase
        by_name = db.Notes.find({'name': note_to_open})
        #if nothing was found return error in text
        if not by_name:
            return 'Note was not found! Try again'
        #else ask about new note text and update it, then return text about it
        else:
            note = input('Enter text of your note: ')
            db.Notes.update_one({'name': note_to_open}, {'$set':{'note': note}})
            return f'The note {note_to_open} is changed to: {note}'  


def tag_update():
    '''Update tags inside the note. Search note by it\'s name, then ask about new tags and update them. If such notes do not exist then return error'''
    #Search info: tag or name.
    note_to_open = input('Enter Note name: ')
    #Database connection
    client = MongoClient(mongo_conn)
    with client:
        db = client.MongoDatabase
        by_name = db.Notes.find({'name': note_to_open})
        #if nothing was found return error in text
        if not by_name:
            return 'Note was not found! Try again'
        #else ask about new tags and update them, then return text about it
        else:
            tags = input('Enter tags separated by space and starting with "#": ') 
            tag_list = tags.split(' ')
            db.Notes.update_one({'name': note_to_open}, {'$set':{'tags': tag_list}})
            return f'The note {note_to_open} tags were changed to: {tag_list}'


def pretty_commands():
    table = PrettyTable()
    table.title = 'Use these commands bellow or "exit" to stop work'
    table.field_names = ['ADD INFO', 'CHANGE INFO',
                         'Notes&Tags', 'Additionally']

    table.add_rows(
        [
            ['add contact', 'change contact', 'create note', 'near birthday'],
            ['add address', 'find contact', 'change note', 'search by tags'], #Correction shortened search by tags
            ['add email', 'show contacts', 'change tag', 'search by text'], #Correction shortened search by text
            ['add birthday', 'delete contact', 'delete note', 'sorting files'],
            ['','','read note','show all tags']
        ]
    )
    return table


def sorting_files ():
    
    p = input('Enter to the path to the directory: ')
    
    print(f'Started in {p}')
    
    images_list = list()
    video_list = list()
    documents_list = list()
    music_list = list()
    archives_list =  list()

    suffix_imeges = ".jpeg", ".png", ".jpg"
    suffix_videos = ".avi", ".mp4", ".mov"
    suffix_documents = ".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"
    suffix_music = ".mp3", ".ogg", ".wav", ".amr"
    suffix_archiv = ".zip", ".tar", ".gztar", ".bztar", ".xztar"

    ignor = "archives", "images", "music", "videos", "documents"

    def serch(p):

        for i in os.listdir(p):
            if i not in ignor:
                if os.path.isdir(p +"\\" + i):
                    serch(p + "\\" + i)
 
        for root, dirs, files in os.walk(p):
            for file in files:
                i = os.path.join(root, file)
                sort_file(i, file)
                unpuck_archives(i, file)
                
            for folder in dirs:
                f = os.path.join(root, folder)
                remove_folder(f)
    
    def creat_folder():

        if len(images_list) != 0:
            if not os.path.exists(p +"\\images"):
                os.mkdir(p + "\\images")
        if len(video_list) != 0:
            if not os.path.exists(p + "\\videos"):
                os.mkdir(p + "\\videos")
        if len(documents_list) != 0:
            if not os.path.exists(p + "\\documents"):
                os.mkdir(p + "\\documents")
        if len(music_list) != 0:
            if not os.path.exists(p + "\\music"):
                os.mkdir(p + "\\music")
        if len(archives_list) !=0:
            if not os.path.exists(p + "\\archives"):
                os.mkdir(p + "\\archives")


    def sort_file(i, file):

        if file.endswith(suffix_imeges):
            if file not in images_list:
                images_list.append(file)
            creat_folder()
            if  i != p + "\\images" + "\\" + file:
                os.replace(i, p + "\\images" + "\\" + file)
        elif file.endswith(suffix_videos):
            if file not in video_list:
                video_list.append(file)
            creat_folder()
            if i != p + "\\videos" + "\\" + file:
                os.replace(i , p + "\\videos" + "\\" + file)
        elif file.endswith(suffix_documents):
            if file not in documents_list:
                documents_list.append(file)
            creat_folder()
            if i != p + "\\documents" + "\\" + file:
                os.replace(i, p + "\\documents" + "\\" + file)
        elif file.endswith(suffix_music):
            if file not in music_list:
                music_list.append(file)
            creat_folder()
            if i != p + "\\music" + "\\" + file:
                os.replace(i, p + "\\music" + "\\" + file)

    def remove_folder(f):
        if not os.listdir(f):
            os.removedirs(f)

    def unpuck_archives(i, file):

        if file.endswith(suffix_archiv):
            if file not in archives_list:
                archives_list.append(file)
            creat_folder()
            name_folder_archive = file.split(".")
            shutil.unpack_archive(i, p + "\\archives"+ "\\" + name_folder_archive[0])
    
    serch(p)
    return (f"Sorting files by the specified path {p} completed succesfully!")


OPERATIONS = {
    'add contact' : add_contact,
    'add address' : add_address,
    'add email' : add_email,
    'add birthday' : add_birthday,
    'change contact' : change_contact,
    'find contact' : find_contact,
    'near birthday' : nearby_birthday,
    'delete contact' : delete_contact,
    'show contacts' : show_contacts,
    'create note' : create_new_note,
    'delete note' : delete_note,
    'change note' : note_update,
    'change tag' : tag_update, 
    'search by text' : note_search, 
    'sorting files' : sorting_files,
    'help': pretty_commands,
    'show all tags':show_all_tags,
    'read note': read_note,
    'show cache': show_cache
    }

def get_handler(operator):
    if not OPERATIONS.get(operator):
        return wrong
    return OPERATIONS[operator]

    
def main():
    #Start of the cli
    if os.path.exists('data.json'):
        AB.deserialize()
    print('Hello, User! Welcome to our CLI-bot. Enter "help" in case you need to see the commands again') #Correction добавил выход
    print(pretty_commands())

    while True:
        command = input('Enter your command: ')
        if command == '.' or command == 'exit' or command == 'close':
            AB.serialize()
            print('Goodbye, User!')
            break
        handler = get_handler(command)
        answer = handler()
        print (answer)


if __name__ == '__main__':
    main()
