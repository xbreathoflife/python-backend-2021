from fastapi import HTTPException

from main import app
from model.models import TranslateWordRequest, TranslateWord, Dictionary
from deep_translator import GoogleTranslator

dictionary = Dictionary()


@app.get("/dictionary/{word_id}")
def get_word(word_id: int):
    return dictionary.get_word_from_dictionary(word_id)


@app.get("/dictionary/")
def get_words():
    return dictionary.get_dictionary()


def translate_word(word: str, from_language, to_language="ru"):
    translation = GoogleTranslator(source=from_language, target=to_language).translate(word)
    return translation


@app.post("/dictionary/translate/")
def post_word(request: TranslateWordRequest):
    if " " in request.word or len(request.word) > 15:
        raise HTTPException(status_code=400, detail="The word is too long or not a word")
    if request.to_language == "":
        request.to_language = "ru"
    if request.from_language == "":
        translation = translate_word(request.word, "auto", request.to_language)
    else:
        translation = translate_word(request.word, request.from_language, request.to_language)
    dictionary.add_word_to_dictionary(request.word, translation)

    response = TranslateWord(request.word, translation, request.from_language, request.to_language)
    return response
