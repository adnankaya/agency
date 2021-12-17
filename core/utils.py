from slugify import slugify
from timeit import default_timer as timer

def generate_slug(word):
    word = slugify(word)
    return word

def elapsed_timer(func):
    def wrapper(*args, **kwargs):
        start = timer()
        response = func(*args, **kwargs)
        if response.status_code == 200:
            end = timer()
            response.context_data['elapsed_time'] = round((end - start), 5)
        return response
    return wrapper