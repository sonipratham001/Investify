from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reputation = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    videos = models.ManyToManyField(Video)
    created_at = models.DateTimeField(auto_now_add=True)

class Quiz(models.Model):
    question = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    choices = models.JSONField()
    correct_choice = models.IntegerField()
    explanation = models.TextField(null=True, blank=True)  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    text = models.CharField(max_length=255)
    explanation = models.TextField()

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Webinar(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    scheduled_at = models.DateTimeField()
    url = models.URLField()

class LearningPath(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10)  # 'upvote' or 'downvote'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post', 'vote_type')


class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=100000.0)  # Default virtual balance

    def __str__(self):
        return f"{self.user.username}'s Portfolio"


class Trade(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Assuming user with ID 1 exists
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    trade_type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.trade_type} {self.quantity} of {self.stock.symbol} at {self.price}"















