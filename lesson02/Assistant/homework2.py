from abc import abstractclassmethod, ABC
from prettytable import PrettyTable
from pathlib import Path


try:
    from AddressBook import *
except:
    from .AddressBook import *

AB = AddressBook()

if Path('data.json').exists():
    AB.deserialize()

class BaseInterface(ABC):
    @abstractclassmethod
    def get_response(self):
        pass

class HelpInterface(BaseInterface):
    def get_response(self):
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


class AllContactsInterface(BaseInterface):
    def get_response(self):
        pretty_contacts = PrettyTable()
        pretty_contacts.field_names = [
            'Name', 'Address', 'Phone', 'Email', 'Birthday']

        for k, v in AB.contacts.items():
            pretty_contacts.add_row(
                [k, v['Address'], v['Phone'], v['Email'], v['Birthday']])
        return pretty_contacts


class AllNotesInterface(BaseInterface):
    def get_response(self):

        pretty_notes = PrettyTable()
        pretty_notes.field_names = ['Name', 'Note']
        for obj in Path('.').iterdir():
            if obj.is_dir():
                continue
            extention = obj.suffix
            if extention == '.txt':
                with open(obj,'r') as file:
                    text = file.read()
                pretty_notes.add_row([str(obj), text])
            else:
                continue
        return pretty_notes



if __name__ == "__main__":
    pass
