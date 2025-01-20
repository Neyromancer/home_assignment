from datetime import datetime

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class ApplicationDBModel(Base):
    __tablename__ = "application"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(index=True) 
    description: Mapped[str] = mapped_column(index=True)
    created_at: datetime
