from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Text, Table, ForeignKey, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.sqltypes import Integer

engine = create_engine('sqlite:///addressbook_db.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Contact(Base):
    __tablename__ = "contact"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)
    phone = Column(String)
    birthday = Column(Date)
    
    def __init__(self, name, address, email, phone, birthday):
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.birthday = birthday

    def __repr__(self):
        return f'Name:{self.name}; address: {self.address}; email {self.email}; phone: {self.phone}; birthday: {self.birthday.strftime("%Y.%m.%d")}'

