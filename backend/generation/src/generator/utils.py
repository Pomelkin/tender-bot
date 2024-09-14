import logging

import pymorphy3

morph = pymorphy3.MorphAnalyzer()


def genitive(word):
    word = word.strip()
    try:
        if word != "-":
            genitive_word = ""
            for subword in word.split(" "):
                parsed_word = morph.parse(subword)[0]
                genitive_word += parsed_word.inflect({"gent"}).word.capitalize() + " "
            return genitive_word.strip()
    except Exception as e:
        logging.error(f"{e}: {word}")
        return word

    return word
