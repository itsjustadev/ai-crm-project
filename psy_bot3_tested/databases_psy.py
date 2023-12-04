from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from library_tables import Base

# Создаем соединение с базой данных
engine = create_engine('sqlite:///psy_bot.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


session.close()
