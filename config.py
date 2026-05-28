#Configuration file for the application
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/delicias_sorley"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "fritos123"
