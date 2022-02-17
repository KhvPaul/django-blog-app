from blog.models import Blogger, Comment

from django import forms
from django.contrib.auth.forms import UserCreationForm


class BloggerCreationForm(UserCreationForm):
    class Meta:
        model = Blogger
        fields = ["username", 'email', "password1", "password2"]


class BloggerChangeForm(forms.ModelForm):
    class Meta:
        model = Blogger
        fields = ["first_name", "last_name", "email", "bio", "profile_picture"]


class BloggerUpdatePasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords didn't match")
        return cleaned_data


class ContactUsForm(forms.Form):
    email = forms.EmailField(required=True)
    text = forms.CharField(max_length=400, help_text="Describe your problem in a box", widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["blogger", 'content']
