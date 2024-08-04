from django.urls import path
from . import views
from .views import quiz_view

urlpatterns = [
    path('', views.home, name='home'),
    path('videos/', views.video_library, name='video_library'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('quizzes/', views.quiz_view, name='quiz_view'),
    path('webinars/', views.webinar_schedule, name='webinar_schedule'),
    path('dashboard/', views.personalized_dashboard, name='personalized_dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('register/', views.register, name='register'),
    path('virtual-trading/', views.virtual_trading_dashboard, name='virtual_trading_dashboard'),
    path('execute-trade/', views.execute_trade, name='execute_trade'),
    path('candlestick-chart/', views.candlestick_chart, name='candlestick_chart'),
]




