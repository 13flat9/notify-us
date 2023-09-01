from sqlalchemy import create_engine, URL, select, Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import os
from check_new_jobs.table_models import Interested, Base, User
from . import config

def get_engine() -> Engine:
    url_object = URL.create(
        "postgresql",
        username=os.environ['DB_APP_USERNAME'],
        password=os.environ['DB_APP_PASSWORD'],
        host=f"{os.environ['DB_SERVER_NAME']}.postgres.database.azure.com",
        database=os.environ['DB_NAME']
    )

    engine = create_engine(url_object, echo=config.echo, connect_args={'sslmode': "allow"})
    return engine


def create_tables(engine) -> None:
    Base.metadata.create_all(engine)


def get_session(engine):
    # Note: this only makes sense if I never want more than one session
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def get_users(session) -> list[str]:
    stmt = select(User.email)
    return session.scalars(stmt).all()


def get_keywords(session, user_email: str) -> list[str]:
    stmt = select(Interested.keyword).where(Interested.email == user_email)
    return session.scalars(stmt).all()


class UserAlreadyExists(Exception):
    pass

def insert_user(session, user_email: str, keywords: list[str]) -> None:
    user = User(email=user_email)
    try:
        session.add(user)
        session.commit()
    except IntegrityError as e:
        msg = f"{user} already exists in the database"
    for keyword in keywords:
        interested = Interested(email=user_email, keyword=keyword)
        session.add(interested)
        session.commit()


def delete_user(session, user_email: str) -> None:
    stmt = select(Interested).where(Interested.email == user_email)
    user_interests = session.scalars(stmt)
    for interest in user_interests:
        session.delete(interest)

    user = session.get(User, user_email)
    session.delete(user)
    session.commit()