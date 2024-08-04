from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Video, Course, Quiz, Webinar, LearningPath, Post, Comment
from .forms import PostForm, CommentForm, QuizForm, UserRegistrationForm
from django.http import JsonResponse
from .models import Question, Option
from .models import Stock, Portfolio, Trade


def home(request):
    return render(request, 'learning/home.html')

def video_library(request):
    videos = Video.objects.all()
    return render(request, 'learning/video_library.html', {'videos': videos})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'learning/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'learning/course_detail.html', {'course': course})


def quiz_view(request):
    questions = Question.objects.all()
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        question_id = request.POST.get('question_id')
        selected_option_id = request.POST.get('option')
        selected_option = get_object_or_404(Option, id=selected_option_id)
        if selected_option.is_correct:
            message = "Correct!"
            explanation = ""
        else:
            message = "Incorrect!"
            explanation = selected_option.question.explanation
        return JsonResponse({'message': message, 'explanation': explanation, 'question_id': question_id, 'is_correct': selected_option.is_correct})
    
    return render(request, 'learning/quiz.html', {'questions': questions})




def webinar_schedule(request):
    webinars = Webinar.objects.all()
    return render(request, 'learning/webinar_schedule.html', {'webinars': webinars})

@login_required
def personalized_dashboard(request):
    learning_paths = LearningPath.objects.filter(user=request.user)
    return render(request, 'learning/personalized_dashboard.html', {'learning_paths': learning_paths})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('personalized_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'learning/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('personalized_dashboard'))
        else:
            return render(request, 'learning/login.html', {'error': 'Invalid login'})
    else:
        return render(request, 'learning/login.html')

def logout_view(request):
    return render(request, 'learning/logout.html')

@login_required
def dashboard_view(request):
    context = {
        'data': 'Some data for the dashboard'
    }
    return render(request, 'learning/dashboard.html', context)

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'learning/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'learning/post_detail.html', {'post': post, 'comment_form': comment_form})

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'learning/post_form.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'learning/post_form.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')  # Redirect to a success page or home page
    else:
        form = UserRegistrationForm()
    return render(request, 'learning/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list')  # Redirect to a success page or home page
    else:
        form = AuthenticationForm()
    return render(request, 'learning/login.html', {'form': form})





# Using yahoo finance

import yfinance as yf
import plotly.graph_objects as go
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def get_stock_details_yahoo(symbol):
    stock = yf.Ticker(symbol)
    return {
        'current_price': stock.history(period="1d")['Close'][0]
    }

@login_required
def virtual_trading_dashboard(request):
    portfolio, created = Portfolio.objects.get_or_create(user=request.user)
    trades = Trade.objects.filter(user=request.user).order_by('-created_at')
    stocks = Stock.objects.all()
    context = {
        'portfolio': portfolio,
        'trades': trades,
        'stocks': stocks,
    }
    return render(request, 'learning/virtual_trading_dashboard.html', context)

@login_required
def execute_trade(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        trade_type = request.POST.get('trade_type')
        quantity = int(request.POST.get('quantity'))

        stock_details = get_stock_details_yahoo(symbol)
        if stock_details is None:
            messages.error(request, 'Failed to fetch stock details')
            return redirect('virtual_trading_dashboard')

        price = stock_details['current_price']  # Current price

        stock, created = Stock.objects.get_or_create(symbol=symbol, defaults={'name': symbol, 'price': price})
        if not created:
            stock.price = price
            stock.save()

        portfolio = Portfolio.objects.get(user=request.user)

        if trade_type == 'buy' and portfolio.balance < price * quantity:
            messages.error(request, 'Insufficient balance to execute the trade')
            return redirect('virtual_trading_dashboard')

        trade = Trade(
            portfolio=portfolio,
            stock=stock,
            user=request.user,
            quantity=quantity,
            price=price,
            trade_type=trade_type,
        )
        trade.save()

        if trade_type == 'buy':
            portfolio.balance -= price * quantity
        elif trade_type == 'sell':
            portfolio.balance += price * quantity
        portfolio.save()

        messages.success(request, f'Trade executed: {trade_type} {quantity} shares of {symbol} at {price}')
        return redirect('virtual_trading_dashboard')
    else:
        messages.error(request, 'Invalid request method')
        return redirect('virtual_trading_dashboard')

def fetch_stock_data_yahoo(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1mo")  # Fetching 1 month of data
    if hist.empty:
        return None
    return {
        't': hist.index.astype(str).tolist(),
        'o': hist['Open'].tolist(),
        'h': hist['High'].tolist(),
        'l': hist['Low'].tolist(),
        'c': hist['Close'].tolist()
    }

def candlestick_chart(request):
    if request.method == 'POST':
        stock_symbol = request.POST.get('stock_symbol')
        stock_data = fetch_stock_data_yahoo(stock_symbol)
        if stock_data is None:
            messages.error(request, 'No data available for the provided stock symbol.')
            return redirect('candlestick_chart')

        fig = go.Figure(data=[go.Candlestick(x=stock_data['t'],
                                             open=stock_data['o'],
                                             high=stock_data['h'],
                                             low=stock_data['l'],
                                             close=stock_data['c'])])
        fig.update_layout(title=f'Candlestick chart for {stock_symbol}', xaxis_title='Date', yaxis_title='Price')
        chart_html = fig.to_html(full_html=False)

        return render(request, 'learning/candlestick_chart.html', {'chart': chart_html, 'stock_symbol': stock_symbol})

    return render(request, 'learning/candlestick_chart.html')



