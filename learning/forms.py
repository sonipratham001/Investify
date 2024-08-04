from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Trade, Stock, Question, Option

class QuizForm(forms.Form):
    quiz_id = forms.IntegerField(widget=forms.HiddenInput)
    choice = forms.ChoiceField(choices=[], widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super().__init__(*args, **kwargs)
        self.fields['choice'].choices = choices

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TradeForm(forms.ModelForm):
    stock = forms.ModelChoiceField(queryset=Stock.objects.all(), to_field_name="symbol")

    class Meta:
        model = Trade
        fields = ['stock', 'trade_type', 'quantity', 'price']


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']


