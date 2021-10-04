from typing import List

import graphene


class WordUnit(graphene.ObjectType):
    word = graphene.String()
    translation = graphene.String()
    number_of_repetitions = graphene.Int()
    number_of_correct_answers = graphene.Int()

    def __init__(self, word: str, translation: str, number_of_repetitions: int, number_of_correct_answers: int):
        self.word = word
        self.translation = translation
        self.number_of_repetitions = number_of_repetitions
        self.number_of_correct_answers = number_of_correct_answers


class User(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    dictionary = graphene.List(WordUnit)

    def __init__(self, id: int, name: str, words: List[WordUnit]):
        self.id = id
        self.name = name
        self.dictionary = words