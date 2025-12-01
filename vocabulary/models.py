from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название языка")
    code = models.CharField(max_length=10, verbose_name="Код языка")

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"

    def __str__(self):
        return self.name

class Word(models.Model):
    original_word = models.CharField(max_length=200, verbose_name="Слово на иностранном языке")
    translation = models.CharField(max_length=200, verbose_name="Перевод")
    language_from = models.ForeignKey(Language, on_delete=models.CASCADE,
                                    related_name='words_from', verbose_name="Исходный язык")
    language_to = models.ForeignKey(Language, on_delete=models.CASCADE,
                                  related_name='words_to', verbose_name="Язык перевода")
    example_sentence = models.TextField(blank=True, verbose_name="Пример использования")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               blank=True, verbose_name="Добавил пользователь")

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"

    def __str__(self):
        return f"{self.original_word} - {self.translation}"

class FavoriteWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    word = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name="Слово")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления в избранное")

    class Meta:
        verbose_name = "Избранное слово"
        verbose_name_plural = "Избранные слова"
        unique_together = ['user', 'word']  # Один пользователь не может добавить слово дважды

    def __str__(self):
        return f"{self.user.username} - {self.word.original_word}"