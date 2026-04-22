from django.forms import ModelForm 
from posts.models import Post
from django import forms
from typing import Any


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["header","description","rate","is_published", "image"]

class CommonPostForm(forms.Form):
    header = forms.CharField(max_length=255,min_length=5,required=True)
    description = forms.CharField(max_length=255,min_length=10,required=True)
    rate = forms.IntegerField(max_value=5, min_value=1, required=True)
    is_published = forms.BooleanField(disabled=False)

    
    def clean_header(self):
        header = self.cleaned_data.get("header")
        if header == "запрещенное слово":
            raise forms.ValidationError(message="Вы ввели запрещенное слово!")

        return header

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        rate = int(cleaned_data.get("rate"))

        if rate < 5:
            raise forms.ValidationError("Rate less then 5")
        
        return cleaned_data
    

class EditPostForm(forms.Form):
    header = forms.CharField(max_length=255)
    description = forms.CharField()
    image = forms.ImageField(required=False)


class CreateCommentForm(forms.Form):
    text = forms.CharField(min_length=10)


class PostSearchForm(forms.Form):
    query = forms.CharField(
    label='Поиск',
    required=False,
    widget=forms.TextInput(attrs={
        'class': 'form-control me-2',
        'placeholder': 'Search'
    })
)