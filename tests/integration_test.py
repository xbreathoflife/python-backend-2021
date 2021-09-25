from typing import Optional
from unittest import TestCase

from fastapi.testclient import TestClient

import controller.endpoints
from controller.endpoints import app
from model.models import TranslateWordRequest

client = TestClient(app)


def post_word(word: str, from_language: Optional[str], to_language: Optional[str]):
    return client.post("/dictionary/translate/", json=TranslateWordRequest(
        word=word,
        from_language=from_language,
        to_language=to_language
    ).dict())


class IntegrationTestMethods(TestCase):
    def setUp(self) -> None:
        controller.endpoints.dictionary.fake_dictionary.clear()

    def test_basic(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ["Welcome to dictionary"])

    def test_empty_dictionary(self):
        response = client.get("/dictionary/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_post_word(self):
        response = post_word("Cat", "en", "ru")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"from_language": "en", "to_language": "ru", "translated_word": "Кот",
                                           "word": "Cat"})
        response = post_word("Tree", "", "ru")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"from_language": "", "to_language": "ru", "translated_word": "Дерево",
                                           "word": "Tree"})
        response = post_word("Tree house", "en", "ru")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "The word is too long or not a word"})
        response = post_word("IAMVERYLOOOOOONGWORD", "en", "ru")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "The word is too long or not a word"})
        response = post_word("auto-translate", "", "")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {"from_language": "", "to_language": "ru", "translated_word": "автоматический перевод",
                          "word": "auto-translate"})

    def test_post_and_get_dictionary(self):
        post_word("Cat", "en", "ru")
        response = client.get("/dictionary/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"translated_word": "Кот", "word": "Cat"}])
        post_word("Tree", "", "ru")
        response = client.get("/dictionary/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"translated_word": "Кот", "word": "Cat"},
                                           {"translated_word": "Дерево", "word": "Tree"}])
        post_word("Tree house", "en", "ru")
        post_word("IAMVERYLOOOOOONGWORD", "en", "ru")
        response = client.get("/dictionary/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"translated_word": "Кот", "word": "Cat"},
                                           {"translated_word": "Дерево", "word": "Tree"}])

    def test_post_and_get_word_by_id(self):
        post_word("Cat", "en", "ru")
        response = client.get("/dictionary/0")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"translated_word": "Кот", "word": "Cat"})
        post_word("Tree", "", "ru")
        response = client.get("/dictionary/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"translated_word": "Дерево", "word": "Tree"})
        post_word("Tree house", "en", "ru")
        post_word("IAMVERYLOOOOOONGWORD", "en", "ru")
        response = client.get("/dictionary/2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'word_id': 'No word with this id!'})
        response = client.get("/dictionary/-1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'word_id': 'No word with this id!'})

