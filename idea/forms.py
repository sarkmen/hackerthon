from django import forms
from django.forms.widgets import FileInput
from .models import Idea, Comment, Vote

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'contents', 'image', ]
        labels = {
            'title': '제목',
            'contents': '내용',
            'image': '이미지',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '제목'}),
            'contents': forms.Textarea(attrs={'placeholder': '컨텐츠'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['contents', ]
        widgets = {
            'contents': forms.Textarea(attrs={'placeholder': '내용 입력', 'rows': 2}),
        }
