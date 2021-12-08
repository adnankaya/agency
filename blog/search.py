from django.contrib.postgres.search import (SearchVector,
                                            SearchQuery,
                                            SearchRank,
                                            TrigramSimilarity)

from .models import Post



def search_with_trigram_similarity(query):
    return Post.published.annotate(
        similarity=TrigramSimilarity('title', query),
    ).filter(similarity__gt=0.1).order_by('-similarity')


def search_query_weighting(query):
    s_vector = SearchVector('title', weight='A') + \
        SearchVector('body', weight='B')
    s_query = SearchQuery(query)
    return Post.published.annotate(
        rank=SearchRank(s_vector, s_query)
    ).filter(rank__gte=0.3).order_by('-rank')


def search_query(query):
    s_vector = SearchVector('title', 'body')
    s_query = SearchQuery(query)
    return Post.published.annotate(
        search=s_vector,
        rank=SearchRank(s_vector, s_query)
    ).filter(search=query).order_by('-rank')