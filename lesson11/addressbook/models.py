'''from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Text, Table, ForeignKey, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.sqltypes import Integer'''

from addressbook import db
#engine = create_engine('sqlite:///addressbook_db.db')
#Session = sessionmaker(bind=engine)
#Base = declarative_base()


class Contact(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    address = db.Column(db.String(60))
    email = db.Column(db.String(60))
    phone = db.Column(db.String(60))
    birthday = db.Column(db.Date)
    
    '''def __init__(self, name, address, email, phone, birthday):
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.birthday = birthday'''

    def __repr__(self):
        return f'Name:{self.name}; address: {self.address}; email {self.email}; phone: {self.phone}; birthday: {self.birthday.strftime("%Y.%m.%d")}'

#Base.metadata.create_all(engine)