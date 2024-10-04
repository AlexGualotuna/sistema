from sqlmodel import create_engine

def connect():
    engine = create_engine("mysql+pymysql://root:root123@localhost:3306/pruebaudla")
    return engine