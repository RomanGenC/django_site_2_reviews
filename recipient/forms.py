from django import forms
from django.core.exceptions import ValidationError
from .models import Recipient, Review
from django.contrib.auth.models import User


class ReviewEditForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['modified_review', 'is_published']
        widgets = {
            'modified_review': forms.Textarea(),
        }

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class AddReview(forms.ModelForm):
    is_anonymous = forms.BooleanField(label='Анонимный отзыв', required=False)

    class Meta:
        model = Review
        fields = ['original_review', 'rate']

        widgets = {
            'original_review': forms.Textarea(attrs={'cols': 200, 'rows': 30,
                                                     'placeholder': 'Напишите ваш отзыв здесь...'}),
            'rate': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
        }

    def clean_original_review(self):
        original_review = self.cleaned_data['original_review']
        if len(original_review) < 100:
            raise ValidationError("Должно быть хотя бы 100 символов")
        return original_review


class SearchForm(forms.Form):
    query = forms.CharField()
