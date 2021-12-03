from slugify import slugify

def generate_slug(word):
    word = slugify(word)
    return word
