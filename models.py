from sqlalchemy import Column, Integer, String, Text

from database import Base


class Title(Base):
    __tablename__ = "title"

    title = Column(Text, nullable=False, primary_key=True)
    vector = Column(Text, nullable=False)
