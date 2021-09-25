import unittest

from fastapi import HTTPException

from controller import endpoints
from controller.endpoints import translate_word
from model.models import Dictionary


class UnitTestMethods(unittest.TestCase):
    def test_empty_dict(self):
        dictionary = Dictionary()
        self.assertEqual(len(dictionary.get_dictionary()), 0)

    def test_add_to_dict(self):
        dictionary = Dictionary()
        dictionary.add_word_to_dictionary("cat", "кот")
        self.assertEqual(len(dictionary.get_dictionary()), 1)
        dictionary.add_word_to_dictionary("dog", "собака")
        self.assertEqual(len(dictionary.get_dictionary()), 2)

    def test_get_word_from_dict(self):
        dictionary = Dictionary()
        dictionary.add_word_to_dictionary("cat", "кот")
        dictionary.add_word_to_dictionary("dog", "собака")
        self.assertEqual(dictionary.get_word_from_dictionary(0), {"word": "cat", "translated_word": "кот"})
        self.assertEqual(dictionary.get_word_from_dictionary(1), {"word": "dog", "translated_word": "собака"})

    def test_get_word_from_dict_wrong_index(self):
        dictionary = Dictionary()
        dictionary.add_word_to_dictionary("cat", "кот")
        self.assertEqual(dictionary.get_word_from_dictionary(1), {"word_id": "No word with this id!"})
        self.assertEqual(dictionary.get_word_from_dictionary(-1), {"word_id": "No word with this id!"})

    def test_empty_translation(self):
        dictionary = Dictionary()
        self.assertRaises(HTTPException, dictionary.add_word_to_dictionary, "empty", "")

    def test_empty_word(self):
        dictionary = Dictionary()
        dictionary.add_word_to_dictionary("", "кот")
        self.assertEqual(dictionary.get_word_from_dictionary(0), {"word": "", "translated_word": "кот"})

    def test_translate_from_en_to_ru(self):
        self.assertEqual(translate_word("cat", "en", "ru").lower(), "кот")

    def test_translate_to_ru(self):
        self.assertEqual(translate_word("cat", from_language="auto", to_language="ru").lower(), "кот")

    def test_translate(self):
        self.assertEqual(translate_word("cat", from_language="auto").lower(), "кот")

    def test_translate_wrong_languages(self):
        self.assertEqual(translate_word("cat", from_language="ru", to_language="en").lower(), "cat")
