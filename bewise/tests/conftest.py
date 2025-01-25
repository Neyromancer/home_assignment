import asyncio

# what is `ExitStack` for?
from contextlib import ExitStack

import pytest
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

from app import init_app
from app.database import get_database_session, sessionmanager


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        # do not initialise physical DB for testing
        # DB will be mocked
        yield init_app(init_db=False)


@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client


test_db = factories.postgresql_proc(port=None, dbname="test_db")


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def database_session_connection_test(test_db, event_loop):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        user=pg_user,
        host=pg_host,
        port=pg_port,
        dbname=pg_db,
        version=test_db.version,
        password=pg_password,
    ):
        db_connection_url = f"postgresql+psycopg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        sessionmanager.init(db_connection_url)
        yield
        await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def create_tables(database_session_connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest.fixture
def test_application_data():
    return [
        {"username": "TestUser1", "description": "TestUser1 application description"},
        {"username": "TestUser2", "description": "TestUser2 application description"},
    ]


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, database_session_connection_test):
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_database_session] = get_db_override
