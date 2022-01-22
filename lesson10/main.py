import os, time
from collections import Counter, OrderedDict #Correction добавил словарь
from prettytable import PrettyTable


def create_new_note():
    tags = input('Enter tags separated by space and starting with "#": ') 
    note = input('Enter text of your note: ') 

    data = f'{tags}\n\n{note}'
    t = str(time.time()).split('.')[0]
    filename = t+".txt"   
    try:
        with open(filename, "w") as file:
            file.write(data)            
    except IOError:
        print("File not accessible")
    return f'You have created a note {filename}' 

def delete_note():
    filename = input("Enter FileName: ")
    path = os.getcwd()
    if os.path.isfile(filename):
        os.remove(os.path.join(path, filename))
        return f'{filename} deleted'
    else:
        return 'wrong FileName'


def read_note():
    file_to_open = input('Enter FileName: ')
    try:
        with open(file_to_open, encoding='utf8') as file:
            data = file.read()
        return(data) #Correction changed to return
    except:
        return('File not found') #Correction changed to return

def show_all_tags():
    search_path = '.'
    file_type = '.txt'
    taglist = []
    if not (search_path.endswith("/") or search_path.endswith("\\") ): 
        search_path = search_path + "/"

    for fname in os.listdir(path = search_path):
        if fname.endswith(file_type):
            fo = open(search_path + fname)
            line = fo.readline()
            temp = (line.lower()).split(' ')
            for i in temp:
                if i.startswith('#'):
                    taglist.append(i.strip())  
    result = sorted(list(set(taglist)))
    resstr = " ".join(result) #Correction убрал лишнюю строку
    print('Please see the list of all available tags below:')
    return(resstr) #Correction change from print to return

def note_search():
    search_path = '.'
    file_type = '.txt'
    search_str = input('Please enter the text/word you are looking for: ')

    if not (search_path.endswith("/") or search_path.endswith("\\") ): 
            search_path = search_path + "/"

    for fname in os.listdir(path = search_path):
        if fname.endswith(file_type):
            fo = open(search_path + fname)
            line = fo.readline()
            line = fo.readline()
            line = fo.readline()
            index = line.find(search_str)
            if (index != -1) :
                    print(fname, line, sep=" ")
            fo.close()
    return 'Search complete'

def note_update():
    file_to_open = input('Enter the full name of the note you want to update: ') #Correction full name
    try:
        with open(file_to_open, 'r') as file:            
            data = file.readlines()

        print('Current note is: ') #Correction отступ после двоеточия
        print(data[1][:-1])
        note = input("Update a note: ") + '\n' #note input
        data[-1] = note

        with open(file_to_open, 'w') as file:
            file.writelines(data)
    except IOError:
        print("File not accessible")
    return f'The note {file_to_open} is changed to: {note}'

def tag_search_helper(tag: str, flist: list, filename: str, text: str):
    # Tags we're looking for in the first line, lowercase
    if tag != '%%%%%%%%%%' and ((tag.lower() + ' ') in text.lower()):
        flist.append(filename)
    return flist

def tag_search(): #Correction поисправлял регистр функций tag_search и tag_search_helper
    deftags = ['%%%%%%%%%%', '%%%%%%%%%%', '%%%%%%%%%%', '%%%%%%%%%%', '%%%%%%%%%%', '%%%%%%%%%%']
    tags = input('Enter up to six tags separated by space: ') #Correction Separated by space
    tags = tags.split(' ')
    tags.extend(deftags)
    tags = tags[:6]
    search_path = '.'
    file_type = '.txt'
    flist = []

    if not (search_path.endswith("/") or search_path.endswith("\\") ): 
        search_path = search_path + "/"

    for fname in os.listdir(path = search_path):
        if fname.endswith(file_type):
            fo = open(search_path + fname)
            line = fo.readline()
            flist = tag_search_helper(tags[0], flist, fname, line)
            flist = tag_search_helper(tags[1], flist, fname, line)
            flist = tag_search_helper(tags[2], flist, fname, line)
            flist = tag_search_helper(tags[3], flist, fname, line)
            flist = tag_search_helper(tags[4], flist, fname, line)
            flist = tag_search_helper(tags[5], flist, fname, line)
            fo.close()

    result = Counter(flist)
    result = OrderedDict(result.most_common()) #Correction Добавил сортировку через OrderedDict
    if not result:
        return 'No match!'
    else:
        print("Matches in Files:")
        for key, value in result.items():
            print(f'{value} : {key}')
    return 'Sorted in descending order'


def tag_update():
    #file_to_open = 'data.txt' #filename input.
    file_to_open = input('Enter FileName: ')
    try:
        with open(file_to_open, 'r') as file:
            data = file.readlines()           
        
        print('Current tags are: ') #Correction отступ после двоеточия
        print(data[0][:-1])
        tags = input('Write tags: ') + '\n' #tags input
        data[0] = tags
        
        with open(file_to_open, 'w') as file:
            file.writelines(data)

    except IOError:
        print("File not accessible")
    return f'New tags of the note {file_to_open} are as follows: {tags}'



OPERATIONS = {
    'create note' : create_new_note,
    'delete note' : delete_note,
    'change note' : note_update,
    'change tag' : tag_update,
    'search by tags' : tag_search, 
    'search by text' : note_search, 
    'show all tags':show_all_tags,
    'read note': read_note
    }

def get_handler(operator):
    if not OPERATIONS.get(operator):
        return wrong
    return OPERATIONS[operator]

    
def main():
    #Start of the cli
    
    print('Hello, User! Welcome to our CLI-bot. Enter "help" in case you need to see the commands again') #Correction добавил выход

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
