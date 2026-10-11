from http import HTTPStatus
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserDb, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get('/users', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return {'users': users}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.email == user.email)
                           | (User.username == user.username))
    )

    if db_user:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )

    db_user = User(username=user.username,
                   email=user.email, password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    try:
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password
        session.commit()
        session.refresh(db_user)

        return db_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists'
        )


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'success'}
