from django import forms
from posts.models import Post
from typing import Any


# 🔹 Post creation / edit (ModelForms)
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["header", "description", "rate", "is_published", "image"]


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["header", "description", "rate", "is_published", "image"]


# 🔹 Comment form
class CreateCommentForm(forms.Form):
    text = forms.CharField(min_length=10)


# 🔹 Search form
class PostSearchForm(forms.Form):
    query = forms.CharField(
        label="Поиск",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control me-2",
            "placeholder": "Search"
        })
    )


# 🔹 Optional custom validation form (если реально используешь отдельно)
class CommonPostForm(forms.Form):
    header = forms.CharField(max_length=255, min_length=5, required=True)
    description = forms.CharField(max_length=255, min_length=10, required=True)
    rate = forms.IntegerField(max_value=5, min_value=1, required=True)
    is_published = forms.BooleanField(required=False)

    def clean_header(self):
        header = self.cleaned_data.get("header")
        if header == "запрещенное слово":
            raise forms.ValidationError("Вы ввели запрещенное слово!")
        return header

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        rate = cleaned_data.get("rate")

        if rate is not None and rate < 5:
            raise forms.ValidationError("Rate less then 5")

        return cleaned_data