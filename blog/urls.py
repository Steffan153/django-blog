from django.urls.conf import path
from . import views

urlpatterns = [
    path("", views.StartingPage.as_view(), name="starting_page"),
    path("posts", views.AllPosts.as_view(), name="posts"),
    path("posts/<slug:slug>", views.PostDetail.as_view(), name="post_detail"),
    path("read-later", views.ReadLater.as_view(), name="read_later"),
    path("remove-read-later", views.RemoveReadLater.as_view(), name="remove_read_later"),
]
