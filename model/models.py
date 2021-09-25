from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel


class TranslateWordRequest(BaseModel):
    word: str
    from_language: Optional[str]
    to_language: Optional[str]


class TranslateWord:
    word: str
    translated_word: str
    from_language: str
    to_language: str

    def __init__(self, word: str, translated_word: str, from_language: str, to_language: str):
        self.word = word
        self.translated_word = translated_word
        self.from_language = from_language
        self.to_language = to_language

    def return_response(self):
        return {"word": self.word, "translated_word": self.translated_word,
                "from_language": self.from_language, "to_language": self.to_language}


class Dictionary:
    def __init__(self):
        self.fake_dictionary = []

    def get_word_from_dictionary(self, word_id: int):
        if 0 <= word_id < len(self.fake_dictionary):
            return self.fake_dictionary[word_id]
        return {"word_id": "No word with this id!"}

    def get_dictionary(self):
        return self.fake_dictionary

    def add_word_to_dictionary(self, word: str, translated_word: str):
        if len(translated_word) == 0:
            raise HTTPException(status_code=500, detail="Translated word is empty")
        new_translation = {"word": word, "translated_word": translated_word}
        self.fake_dictionary.append(new_translation)
        return new_translation
