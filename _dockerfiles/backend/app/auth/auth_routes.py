from fastapi import APIRouter

from app.db.base import db
from app.db.models import User

from app.app_monitor import statsd_client

from datetime import datetime
from werkzeug.security import check_password_hash
import jwt
import datetime

auth = APIRouter()

# import statsd
# statsd_client = statsd.StatsClient('3.231.148.188', 8125, prefix='ncirl.pgdcloud.devsecops')


@auth.post('/signup')
def register_user(payload: dict):
    '''
    input args : email, password, name \n
    picture can be provided but is not mandatory
    '''
    if 'picture' not in payload:
        payload['picture'] = None
    user = db.query(User).filter_by(email=payload['email']).first()
    if not user:
        
        new_user = User(payload['name'], payload['email'], payload['password'])
        new_user.insert()
        
        userid = new_user.user_id
        userid = userid
        
        claims = {
            'id': userid,  
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        secret_key = 'poppushpoppushpoppop'
        auth_token = jwt.encode(claims, secret_key, algorithm='HS256')
        
        return {
            'success': True,
            'token': auth_token.decode('utf-8'),
            'userInfo': {
                'name': payload['name'],
                'email': payload['email'],
                'picture': payload['picture']
            },
            'user_id' : userid,
        }
    else:
        return {
            'message': "User Already exists"
        }

@auth.delete('/delusers')
async def del_users():
    User.delete_all()
    

    return {
        'message' : "success",
        # 'num_users' : users
    }



@auth.post('/loginemail')
def loginemail(payload: dict):
    '''
    input args : email and password
    '''
    statsd_client.incr('login.attempts')

    user = db.query(User).filter_by(email=payload["email"]).first()

    if user and check_password_hash(user.password, payload["password"]):

        claims = {
            'id': user.user_id,  
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        secret_key = 'poppushpoppushpoppop'
        auth_token = jwt.encode(claims, secret_key, algorithm='HS256')

        if auth_token:
            statsd_client.incr('login.successes')
            return {
                'success': True,
                'token': auth_token.decode('utf-8'),
                'userInfo': {
                    'name': user.name,
                    'email': user.email,
                    'picture': user.picture
                }
            }

    else:

        statsd_client.incr('login.failures')
        return {
            'message': "User doesn't exists"
        }
