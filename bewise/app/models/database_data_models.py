from datetime import datetime

from sqlalchemy import Integer, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class ApplicationDBModel(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    username: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, index=True)
    creation_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
