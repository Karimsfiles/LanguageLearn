from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.http import JsonResponse
from .models import Word, Language, FavoriteWord
import random

class WordListView(ListView):
    model = Word
    template_name = 'vocabulary/word_list.html'
    context_object_name = 'words'
    ordering = ['-date_added']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем все языки для фильтров
        context['languages'] = Language.objects.all().order_by('name')

        # Получаем параметры фильтрации из GET-запроса
        context['language_from_filter'] = self.request.GET.get('language_from', '')
        context['language_to_filter'] = self.request.GET.get('language_to', '')

        # Получаем ID избранных слов для текущего пользователя
        if self.request.user.is_authenticated:
            favorite_words_ids = FavoriteWord.objects.filter(
                user=self.request.user
            ).values_list('word_id', flat=True)
            context['favorite_words_ids'] = list(favorite_words_ids)
        else:
            context['favorite_words_ids'] = []

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Применяем фильтры
        language_from = self.request.GET.get('language_from')
        language_to = self.request.GET.get('language_to')

        if language_from:
            queryset = queryset.filter(language_from_id=language_from)

        if language_to:
            queryset = queryset.filter(language_to_id=language_to)

        return queryset


class WordDetailView(DetailView):
    model = Word
    template_name = 'vocabulary/word_detail.html'
    context_object_name = 'word'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверяем, есть ли слово в избранном у текущего пользователя
        if self.request.user.is_authenticated:
            context['is_favorite'] = FavoriteWord.objects.filter(
                user=self.request.user,
                word=self.object
            ).exists()
        else:
            context['is_favorite'] = False

        return context


def random_word_view(request):
    words = Word.objects.all()

    # Применяем фильтры, если они есть
    language_from = request.GET.get('language_from')
    language_to = request.GET.get('language_to')

    if language_from:
        words = words.filter(language_from_id=language_from)

    if language_to:
        words = words.filter(language_to_id=language_to)

    if words:
        random_word = random.choice(words)
    else:
        random_word = None

    context = {
        'word': random_word,
        'languages': Language.objects.all().order_by('name'),
        'language_from_filter': language_from,
        'language_to_filter': language_to,
    }

    # Проверяем, есть ли слово в избранном
    if request.user.is_authenticated and random_word:
        context['is_favorite'] = FavoriteWord.objects.filter(
            user=request.user,
            word=random_word
        ).exists()
    else:
        context['is_favorite'] = False

    return render(request, 'vocabulary/random_word.html', context)


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('vocabulary:word_list')
    else:
        form = UserCreationForm()

    return render(request, 'vocabulary/register.html', {'form': form})


@login_required
def custom_logout_view(request):
    logout(request)
    return redirect('vocabulary:word_list')


@login_required
@require_POST
def toggle_favorite(request, word_id):
    word = get_object_or_404(Word, id=word_id)

    try:
        # Проверяем, есть ли уже слово в избранном
        favorite = FavoriteWord.objects.get(user=request.user, word=word)
        favorite.delete()
        is_favorite = False
    except FavoriteWord.DoesNotExist:
        # Добавляем слово в избранное
        FavoriteWord.objects.create(user=request.user, word=word)
        is_favorite = True

    return JsonResponse({
        'success': True,
        'is_favorite': is_favorite
    })


@login_required
def favorite_words_view(request):
    favorite_words = FavoriteWord.objects.filter(user=request.user).select_related('word')

    # Получаем ID избранных слов
    favorite_words_ids = favorite_words.values_list('word_id', flat=True)

    # Получаем все языки для фильтров
    languages = Language.objects.all().order_by('name')

    # Получаем параметры фильтрации
    language_from = request.GET.get('language_from', '')
    language_to = request.GET.get('language_to', '')

    # Фильтруем избранные слова
    words = Word.objects.filter(id__in=favorite_words_ids)

    if language_from:
        words = words.filter(language_from_id=language_from)

    if language_to:
        words = words.filter(language_to_id=language_to)

    context = {
        'words': words,
        'languages': languages,
        'language_from_filter': language_from,
        'language_to_filter': language_to,
        'favorite_words_ids': list(favorite_words_ids),
    }

    return render(request, 'vocabulary/favorite_words.html', context)



    context = {'form': form}
    return render(request, 'language_learn/add_language.html', context)
