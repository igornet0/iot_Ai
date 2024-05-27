import os

class Config:
    SECRET_KEY =  "12345678Igor"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
