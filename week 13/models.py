from sqlalchemy import Column, Integer, String
from database import Base, engine

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    status = Column(String, default="대출 가능")

Base.metadata.create_all(bind=engine)