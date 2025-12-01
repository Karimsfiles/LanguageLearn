# 🗣️ Vocabulary Learner

Веб-приложение на Django для изучения иностранных слов.

## ✨ Возможности

- 📚 Список слов с переводами
- 🎯 Случайное слово
- 🔍 Фильтрация по языкам
- ❤️ Избранное (после регистрации)
- 👤 Регистрация/авторизация
- ⚙️ Админ-панель Django

## 🚀 Быстрый старт

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/ваш-username/vocabulary-learner.git
cd vocabulary-learner

# 2. Создайте виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows
# или source venv/bin/activate  # Linux/Mac

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Настройте базу данных
python manage.py migrate
python manage.py createsuperuser  # для админки

# 5. Запустите сервер
python manage.py runserver



## 📸 Скриншоты

![Главная страница](https://github.com/Karimsfiles/LanguageLearn/blob/main/screenshots/main.png)

![Cтраница случайных слов](https://github.com/Karimsfiles/LanguageLearn/blob/main/screenshots/randomword.png)

![Карточка слова](https://github.com/Karimsfiles/LanguageLearn/blob/main/screenshots/wordcard.png)
