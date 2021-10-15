from django.forms.models import ModelForm

from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']
        labels = {
            "user_name": "Your Name",
            "user_email": "Your Email",
            "text": "Your Comment",
        }