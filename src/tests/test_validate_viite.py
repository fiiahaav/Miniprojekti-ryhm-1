import unittest
from unittest.mock import Mock, patch
from app import app

class TestAddArticle(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    @patch("app.psycopg2.connect")
    def test_add_article_correct_fields(self, mock_connect):
        mock_conn = Mock()
        mock_cur = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur

        article = {
            "author": "John Doe",
            "title": "Test Article",
            "journal": "Journal X",
            "year": "2024",
            "month": "1",
            "volume": "5",
            "number": "2",
            "pages": "100-120",
            "notes": "Sample notes",
        }
        response = self.client.post("/add_article", data=article, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        mock_connect.assert_called_once()
        mock_cur.execute.assert_called()
        mock_conn.commit.assert_called_once()

    @patch("app.psycopg2.connect")
    def test_add_article_incorrect_fields(self, mock_connect):
        article = {
            "author": "John Doe",
            "title": "",
            "journal": "",
        }
        response = self.client.post("/add_article", data=article, follow_redirects=False)

        self.assertEqual(response.status_code, 400)
        mock_connect.assert_not_called()
