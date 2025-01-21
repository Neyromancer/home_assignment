import asyncio
# what is `ExitStack` for?
from contextlib import ExitStack

import pytest
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy.testing.entities import ComparableEntity

from app import init_app
from app.models.application import ApplicationDBModel
from app.database import get_db_session, sessionmanager


# what does `autouse` mean?
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


# Is `request` required as a parameter?
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def db_session_connection_test(test_db, event_loop):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor (pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password):
        db_connection_url = f"postgresql+psycopg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        sessionmanager.init(db_connection_url)
        yield
        await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def create_tables(db_session_connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)

@pytest.fixture
def test_application_data():
    return {
        "username": "TestUser1",
        "description": "TestUser1 application description"
    }

# TODO: check if this scope level has to be excplicitly mentioned
@pytest.fixture(scope="function", autouse=True)
async def session_override(app, db_session_connection_test):
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db_session] = get_db_override