from sqlalchemy import URL, select, Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import os, sqlalchemy
from check_new_jobs.table_models import Base, Interested, User, Listing
from . import config


def create_engine() -> Engine:
    url_object = URL.create(
        "postgresql",
        username=os.environ['DB_APP_USERNAME'],
        password=os.environ['DB_APP_PASSWORD'],
        host=f"{os.environ['DB_SERVER_NAME']}.postgres.database.azure.com",
        database=os.environ['DB_NAME']
    )
    engine = sqlalchemy.create_engine(url_object, echo=config.echo, connect_args={'sslmode': "allow"})
    return engine

def create_tables(engine) -> None:
    Base.metadata.create_all(engine)

def create_session(engine):
    # Note: this only makes sense if I never want more than one session
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    return Session()


class UserAlreadyExists(Exception):
    pass

#TODO: this name isn't great
class SessionManager:

    def __init__(self, session):
        self.session = session

    def fetch_listings(self) -> list[Listing]:
        stmt = select(Listing)
        return self.session.scalars(stmt).all()

    def fetch_users(self) -> list[User]:
        stmt = select(User)
        return self.session.scalars(stmt).all()

    def fetch_keywords(self, user: User) -> list[str]:
        stmt = select(Interested.keyword).where(Interested.email == user.email)
        return self.session.scalars(stmt).all()

    def insert_listings(self, listings: list[Listing]) -> None:
        for listing in listings:
            self.session.add(listing)
        self.session.commit()

    def insert_user(self, user_email: str, keywords: list[str]) -> None:
        user = User(email=user_email)
        try:
            self.session.add(user)
            self.session.commit()
        except IntegrityError as ex:
            msg = f"{user} already exists in the database"
            raise UserAlreadyExists(msg) from ex
        for keyword in keywords:
            interested = Interested(email=user_email, keyword=keyword)
            self.session.add(interested)
            self.session.commit()

    def delete_user(self, user_email: str) -> None:
        stmt = select(Interested).where(Interested.email == user_email)
        user_interests = self.session.scalars(stmt)
        for interest in user_interests:
            self.session.delete(interest)

        user = self.session.get(User, user_email)
        self.session.delete(user)
        self.session.commit()