from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column
from .config import ListingMaxLength

class Base(DeclarativeBase):
    pass

class Interested(Base):
    __tablename__ = 'interested'

    email = mapped_column(ForeignKey('user.email'), primary_key=True)
    keyword = mapped_column(String(20), primary_key=True)

    def __repr__(self):
        return f'User {self.email} is interested in keyword {self.keyword}'

class Listing(Base):
    __tablename__ = 'listing'

    #href could be shorter
    href = mapped_column(String(27), primary_key=True)
    name = mapped_column(String(ListingMaxLength))

    def __repr__(self):
        return f'Listing "{self.name}" with href {self.href}'

class User(Base):
    __tablename__= 'user'
    email = mapped_column(String(40), primary_key=True)

    def __repr__(self):
        return f'User "{self.email}"'