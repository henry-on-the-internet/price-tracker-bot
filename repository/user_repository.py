from typing import List

from sqlalchemy import update
from sqlalchemy.orm import Session

from repository import auto_flush, User, UserState, UserSubGood, UserSubGoodState
from repository.database import SessionLocal


def find_one(user_id: str, session: Session = SessionLocal()) -> User:
    return session.query(User).filter(User.id == user_id).one()


def find_all_by_state(state: UserState, session: Session = SessionLocal()) -> List[User]:
    return session.query(User).filter(User.state == state).all()


@auto_flush
def save(user: User, session: Session = SessionLocal()):
    session.merge(user)


@auto_flush
def update_user_line_token(user_id: str, line_token: str, session: Session = SessionLocal()):
    statement = (
        update(User)
        .filter(User.id == user_id)
        .values(line_notify_token=line_token)
    )
    session.execute(statement=statement)


def find_all_user_by_good_id(good_id: str, session: Session = SessionLocal()):
    return (
        session.query(User)
        .join(UserSubGood)
        .filter(User.state == UserState.ENABLE)
        .filter(UserSubGood.state == UserSubGoodState.ENABLE)
        .filter(UserSubGood.good_id == good_id)
        .all()
    )
