import unittest

from config import app
from db_helper import tables, reset_db, setup_db

class TestDbHelper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ctx = app.app_context()
        cls.ctx.push()
        setup_db()

    @classmethod
    def tearDownClass(cls):
        reset_db()
        cls.ctx.pop()

    def test_tables_exist(self):
        table_list = tables()
        self.assertIn("articles", table_list)
