from django.db.models.base import Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import CharField, DateField, EmailField, SlugField, TextField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField


class Author(Model):
    first_name = CharField(max_length=20)
    last_name = CharField(max_length=20)
    email = EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tag(Model):
    caption = CharField(max_length=50)

    def __str__(self):
        return self.caption


class Post(Model):
    title = CharField(max_length=60)
    excerpt = CharField(max_length=200)
    image = ImageField(upload_to="posts", null=True)
    date = DateField(auto_now=True)
    slug = SlugField(unique=True, db_index=True)
    content = TextField()
    author = ForeignKey(Author, on_delete=SET_NULL,
                        null=True, related_name="posts")
    tags = ManyToManyField(Tag, related_name="posts", blank=True)

    def __str__(self):
        return self.title


class Comment(Model):
    user_name = CharField(max_length=50)
    user_email = EmailField()
    text = TextField(max_length=400)
    post = ForeignKey(Post, on_delete=CASCADE, related_name="comments")