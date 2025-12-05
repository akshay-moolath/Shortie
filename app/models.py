from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from typing import Optional
from app.db import Base



class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url= Column(String, nullable=False)
    short_code = Column(String, nullable=True)
