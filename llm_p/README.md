# Построение защищенного API для работы с большой языковой моделью

# Описание проекта:
Проект представляет собой защищенное серверное приложение на **FastAPI**, предоставляющее API для взаимодействия с большой языковой моделью (LLM) через сервис **OpenRouter**.

В рамках проекта реализовано аутентификация и авторизация пользователей с использованием JWT, хранение данных в базе SQLite, а также разделение ответственности между слоями приложения (API, бизнес-логика, доступ к данным):
-	работа с FastAPI и асинхронным backend;
-	проектирование серверной архитектуры с разделением слоёв;
-	использование JWT для аутентификации;
-	интеграция внешних API (LLM);
-	работа с базой данных через SQLAlchemy;
-	управление зависимостями проекта через uv.

# Структура проекта:
Была создана корневая папка проекат "llm_p" в корой созданы следующие папки и реализован функционал:

1) Параметры инициализации проекта (pyproject.toml) и переменные окружения (.env.example - пример и .env - основной файл, помещенный в .gitignore);

2) Папка "app" с файлами __init__.py и main.py (точка входа в приложение), а также содержащая папки:
- папка "core" с файлами: __init__.py,config.py,security.py и errors.py - ядро приложения;
- папка "db" с файлами: __init__.py,base.py,session.py и models.py - база данных; 
- папка "schemas" с файлами: __init__.py,auth.py,user.py и chat.py - pydantic схемы (DTO);
- папка "repositories" с файлами: __init__.py,users.py и chat_messages.py - слой доступа к данным;
- папка "services" с файлами: __init__.py и openrouter_client.py - внешние сервисы;
- папка "usecases" с файлами: __init__.py,auth.py и chat.py - бизнес-логика;
- папка "api" с файлами: __init__.py,deps.py,routes_auth.py,routes_chat.py - HTTP эндпоинты.

3) app.db - SQLite база (создаётся при запуске).

# Запуск приложения:
- Перейдите в папку проекта: cd llm_p;
- Создайте виртуальное окружение: uv venv;
- Активируйте виртуальное окружение: source .venv/bin/activate;
- Создайте файл «.env» из примера файла «.env.example» (необходима индивидуальная настройка для JWT_SECRET и OPENROUTER_API_KEY);
- Установите зависимости: uv pip install -r <(uv pip compile pyproject.toml);
- Запустите приложение: uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000;
- Остановка работы приложения: Ctrl+C.

# Интерфейс Swagger: документация и тестирование реализованных эндпоинтов:
**1. Переход по ссылке в браузере после запуска приложения: https://ideal-barnacle-wrq7vqp94g992g7xg-8000.app.github.dev/docs:**
![alt text](image.png)

**2. Процедура регистрации пользователя:** <br>
**2.1.:**
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-4.png)

_Справочно:_
{
  "email": "polina_polyakova@email.com",
  "password": "123456"
}

**2.2.:**
![alt text](image-5.png)
![alt text](image-6.png)
![alt text](image-7.png)

_Справочно:_
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6InVzZXIiLCJleHAiOjE3NzQ0Mzc4MDYsImlhdCI6MTc3NDQzNDIwNn0.bKsFi8BH7xB23qTtHXTINoqnESmMQXqMKVMIaWIq7Eg",
  "token_type": "bearer"
}

**3. Кнопка «Authorize» в правом верхнем угулу:**
![alt text](image-8.png)
![alt text](image-9.png)

**4. Отправка запроса к LLM:**
![alt text](image-10.png)

**4.1. Вопрос: Привет, какие цвета есть во флаге России?**
![alt text](image-11.png)

**4.2. Ответ: Привет! На государственном флаге Российской Федерации три равные горизонтальные полосы: Белая (сверху), Синяя (в середине), Красная (снизу). Этот дизайн был утверждён в 1991 году и восходит к историческому флагу Российской империи.**
![alt text](image-12.png)

**5. Сохранение истории диалогов:**
![alt text](image-13.png)
![alt text](image-14.png)

**6. Удаление истории диалогов:**

**6.1. Удаление истории диалогов:**
![alt text](image-15.png)
![alt text](image-16.png)

**6.2. Проверка удаления:**
![alt text](image-17.png)
![alt text](image-18.png)
