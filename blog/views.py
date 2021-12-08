from django.views import View
from .forms import PostForm
from django.contrib.postgres import search
from django.shortcuts import render, get_object_or_404
from django.core.paginator import (Paginator,
                                   EmptyPage,
                                   PageNotAnInteger)
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
# internals.
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm
from .search import (search_query, search_query_weighting,
                     search_with_trigram_similarity)


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'

# =============================================================================


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'body', 'status']
    template_name = 'blog/post/new.html'

    def form_valid(self, form):
        # form.instance.author = self.request.user
        form.instance.author = User.objects.first() # NOTE temporary
        return super().form_valid(form)


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = search_query(query)
            results_w = search_query_weighting(query)
            results_trigram = search_with_trigram_similarity(query)
    context = {
        'form': form, 'query': query,
        'results': results, 'results_w': results_w,
        'results_trigram': results_trigram
    }
    return render(request, 'blog/post/search.html', context)

# =============================================================================


def post_list(request, tag_slug=None):
    allposts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        allposts = allposts.filter(tags__in=[tag])
    paginator = Paginator(allposts, per_page=2)  # 2 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(number=1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(number=paginator.num_pages)

    return render(request, 'blog/post/list.html',
                  {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, slug):
    def queryset():
        qs = Post.objects.prefetch_related('comments').annotate(
            comment_count=Count('comments'))
        return qs

    post = get_object_or_404(queryset(), slug=slug,
                             status='published',
                             published_date__year=year,
                             published_date__month=month,
                             published_date__day=day
                             )
    # list of comments for this post
    comments = post.comments.filter(is_active=True)
    context = {'post': post,
               'comments': comments,
               'similar_posts': get_similar_posts(post)
               }

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, _("Your comment has been added"))
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
        context['comment_form'] = comment_form
    return render(request, 'blog/post/detail.html', context)


def get_similar_posts(post: Post):
    # list of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')).order_by('-same_tags', '-published_date')[:4]
    return similar_posts


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'adnan@kayace.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
                  {'post': post, 'form': form, 'sent': sent})
