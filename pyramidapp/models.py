from sqlalchemy import (Column,Integer,Text,)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session,sessionmaker,)
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    lastname = Column(Text)
    email = Column(Text)
    phone = Column(Text)
    address = Column(Text)



