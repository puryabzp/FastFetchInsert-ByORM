from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


# you can customize it as you want
class TableName(Base):
    __tablename__ = 'tableName'
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String)
    lastName = Column(String)
