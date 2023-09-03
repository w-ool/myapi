from sqlalchemy import Column, Integer, String, Text

from database import Base


class Question(Base):
    __tablename__ = "title"

    title = Column(String, nullable=False, primary_key=True)
    vector = Column(String, nullable=False)
