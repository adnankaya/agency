from unidecode import unidecode


def generate_slug(word):
    word = word.strip()
    word = unidecode(word)
    word = word.replace(' ', '-')
    return word
