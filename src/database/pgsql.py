from flask import Flask, g
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from config.config import ProdConfig

def get_engine(url):
    
    if not database_exists(url):
        create_database(url)
        
    engine = create_engine(url,pool_size=20, max_overflow=0)
    print("Amogh db url", engine.url)
    return engine

def get_session():
    engine = get_engine(ProdConfig.SQLALCHEMY_DATABASE_URI)
    session = sessionmaker(bind=engine)
    return session

session = get_session()
