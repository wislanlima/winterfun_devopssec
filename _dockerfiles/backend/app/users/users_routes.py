from fastapi import APIRouter, Depends
from app.db.models import User
from app.db.base import db, engine
from sqlalchemy import Table, Column, BigInteger, String, MetaData, ForeignKey, LargeBinary
from app.auth.auth_utils import requires_auth, email_verify_token


users = APIRouter()

@users.post('/create_users_table')
async def create_users_table():
    '''
    input args : no arguments required  \n
    iniatilises the table that will contain user information
    '''
    metadata = MetaData()
    books = Table('users', metadata,
                  Column('user_id', BigInteger, primary_key=True),
                  Column('name', String),
                  Column('email', String),
                  Column('password', String),
                  Column('picture', String),
                  Column('bio', String),
                  Column('role', String),
                  )
    metadata.create_all(engine)
    print('users table created.....')



@users.get('/profile')
async def get_profile(user_id=Depends(email_verify_token)):
    '''
    input args : the user_id  \n
    returns all the data of the user
    '''

    u_dat = db.query(User).filter(User.user_id == user_id).first()

    return {
        'success': True,
        'user': u_dat.format(),

    }


@users.patch('/edit-profile')
async def edit_profile(payload: dict, user_id=Depends(email_verify_token)):
    '''
    payload = {
        name:
        bio:
        # role:
    }
    '''

    profile = db.query(User).filter(User.user_id == user_id).first()

    profile.name = payload['name']
    profile.bio = payload['bio']

    profile.update()

    return {
        'success': True,
        'profile': profile.format_short()
    }
