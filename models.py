# from sqlalchemy import Column, Integer, String, ForeignKeyConstraint,ForeignKey
# from database import Base
# from sqlalchemy.orm import relationship


# class Blog(Base):
#     __tablename__ = 'blogs'

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     body = Column(String)
#     #about = Column(String)
#     #relationship!!!
#     #user_id = Column(Integer, Foreignkey('users.id'))

#     user_id = Column(Integer, ForeignKey('users.id'))
#     creator = relationship("User", back_populates="blogs1")
    
# class User(Base):
#     __tablename__ = 'users'

#     id= Column(Integer, primary_key=True, index=True)
#     name=Column(String)
#     email=Column(String)
#     password=Column(String)
    
#     blogs1 = relationship('Blog', back_populates="creator")
#     #back_populates: reverse

from sqlite3 import sqlite_version
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    #blogs = relationship('Blog', back_populates="creator")
    
class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    #user_id = Column(Integer, ForeignKey('users.id'))
    #creator = relationship("User", back_populates="blogs")


