from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from .config import *


ENGINE = create_engine('mysql+pymysql://%s:%s@localhost/%s'%(DATABASE_USRNAME, DATABASE_PWD, DATABASE_NAME), convert_unicode=True)

db_session=scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=ENGINE))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    if not database_exists(ENGINE.url):
        create_database(ENGINE.url)
    
    from . import model
    Base.metadata.create_all(bind=ENGINE)