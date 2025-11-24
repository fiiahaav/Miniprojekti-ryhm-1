import pytest
from src.db_helper import tables, reset_db, setup_db
from src.config import db, app

@pytest.fixture(scope="module")
def test_app():
    with app.app_context():
        setup_db()  # luo taulut testikantaa varten
        yield app
        reset_db()  # tyhjennä lopuksi

def test_tables_exist(test_app):
    table_list = tables()
    assert "todos" in table_list 
