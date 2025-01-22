import contextlib
from typing import AsyncIterator

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

class Base(DeclarativeBase):
    # TODO: check this comment
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    __mapper_args__ = {"eager_defaults": True}

class DatabaseSessionManager:
    def __init__(self):
        # TODO: What does `AsyncEngine | None` mean?
        self._engine: AsyncEngine | None = None
        # TODO: Check for the type for `self.__sessionmaker`
        self._sessionmaker: AsyncSession | None = None

    @property
    def engine(self) -> AsyncEngine:
        return self.__engine

    @engine.setter
    def engine(self, engine: AsyncEngine):
        self.__engine = engine

    @property
    def sessionmaker(self) -> AsyncSession:
        return self.__sessionmaker

    @sessionmaker.setter
    def sessionmaker(self, session_manager: AsyncSession):
        self.__sessionmaker = session_manager
    
    def init(self, host: str):
        self.__engine = create_async_engine(host)
        self.__sessionmaker = async_sessionmaker(autocommit=False, bind=self.__engine)
    
    async def close(self):
        if self.__engine is None:
            raise Exception("Fail to initialize database session manager")
        
        await self.__engine.dispose()
        self.__engine = None
        self.__sessionmaker = None
    
    # TODO: What does this do?
    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.__engine is None:
            raise Exception("Fail to initialize database session manager")
        
        async with self.__engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise
    
    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.__sessionmaker is None:
            raise Exception("Fail to initialize database session manager")
        
        session = self.__sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
    
    # TODO: Read on these functions
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


sessionmanager = DatabaseSessionManager()


async def get_database_session():
    async with sessionmanager.session() as session:
        yield session