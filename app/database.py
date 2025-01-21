from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    # TODO: check this comment
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    __mapper_args__ = {"eager_defaults": True}

def get_db_session():
    pass