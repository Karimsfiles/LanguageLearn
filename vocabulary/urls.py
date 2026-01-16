from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import register_view, custom_logout_view, toggle_favorite, favorite_words_view, add_language

app_name = 'vocabulary'

urlpatterns = [
    path('', views.WordListView.as_view(), name='word_list'),
    path('word/<int:pk>/', views.WordDetailView.as_view(), name='word_detail'),
    path('random/', views.random_word_view, name='random_word'),
    path('favorites/', favorite_words_view, name='favorite_words'),
    path('language/add/', add_language, name='add_language'),

    # Действия с избранным
    path('word/<int:word_id>/toggle-favorite/', toggle_favorite, name='toggle_favorite'),

    # Аутентификация
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='vocabulary/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),
]

