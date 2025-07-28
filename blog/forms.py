from django import forms
from .models import Post,Comment

class commentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Write a comment...',
                'class': 'form-control',
                'style': 'height: 35px; font-size: 14px;',
            }),
        }

class searchForm(forms.ModelForm):
    class  Meta:
        modle=Post
        fields=[]


