#Configuration file for the application
#class Config:
#    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/delicias_sorley"
#    SQLALCHEMY_TRACK_MODIFICATIONS = False
#    SECRET_KEY = "fritos123"

# Configuration file for the application
import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('MYSQL_USER')}:"
        f"{os.getenv('MYSQL_PASSWORD')}@"
        f"{os.getenv('MYSQL_HOST')}:"
        f"{os.getenv('MYSQL_PORT')}/"
        f"{os.getenv('MYSQL_DB')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "fritos123"