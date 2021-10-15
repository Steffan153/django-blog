from typing import Any, Dict
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import View
from django.urls.base import reverse

from .models import Post
from .forms import CommentForm


class StartingPage(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet:
        return super().get_queryset()[:3]


class AllPosts(ListView):
    template_name = 'blog/posts.html'
    model = Post
    ordering = ['-date']
    context_object_name = "posts"


class PostDetail(View):
    def get_context(self, request: HttpRequest, post: Post, form: Any) -> Dict[str, Any]:
        return {
            "post": post,
            "comments": post.comments.order_by('-id').all(),
            "comment_form": form,
            "is_saved": post.id in (request.session.get("stored_posts") or [])
        }
    
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        post = Post.objects.get(slug=slug)
        form = CommentForm()
        context = self.get_context(request, post, form)
        return render(request, 'blog/post-detail.html', context)

    def post(self, request: HttpRequest, slug: str) -> HttpResponse:
        form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
        context = self.get_context(request, post, form)
        return render(request, 'blog/post-detail.html', context)

class ReadLater(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        stored_posts = request.session.get("stored_posts")
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            context['posts'] = Post.objects.filter(id__in=stored_posts)
            context['has_posts'] = True
        return render(request, 'blog/stored-posts.html', context)

    def post(self, request: HttpRequest) -> HttpResponse:
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []
        
        id = int(request.POST['post_id'])

        if id not in stored_posts:
            stored_posts.append(id)
            request.session['stored_posts'] = stored_posts
        
        return HttpResponseRedirect(reverse("read_later"))

class RemoveReadLater(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        id = int(request.POST['post_id'])

        if id in stored_posts:
            stored_posts.remove(id)
            request.session['stored_posts'] = stored_posts

        return HttpResponseRedirect(reverse("read_later"))