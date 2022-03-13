from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .settings import DATABASE, HOST, DB_PASSWORD, DB_USER, DB_NAME

type = os.environ['TYPE']
if type=="dev":
    SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://%s:%s@%s/%s'%(DB_USER,DB_PASSWORD,HOST,DATABASE)
elif type=="PROD":
    SQLALCHEMY_DATABASE_URL = "Production DB url"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = Session()
Base = declarative_base()