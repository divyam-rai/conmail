import os
from app import create_app
from pytest import fixture

os.environ["ENVIRONMENT"] = "test"

@fixture
def app():
    app = create_app()
    yield app

@fixture()
def client(app):
    return app.test_client()