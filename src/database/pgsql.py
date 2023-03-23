from flask import Flask, g
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config.config import ProdConfig


engine = create_engine(ProdConfig.SQLALCHEMY_DATABASE_URI,
                       pool_size=20, max_overflow=0)

Session = sessionmaker(bind=engine)
