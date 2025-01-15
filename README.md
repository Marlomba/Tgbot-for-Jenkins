# bottapi

Этот проект представляет собой Telegram-бота, который взаимодействует с Jenkins для получения информации о сборках.

## Структура проекта

Структура проекта BotAPI
```bash

botapi/
├── .venv/ # Виртуальное окружение проекта │ 
├── Lib/ │ │ └── … # Библиотеки Python для проекта │
│ └── Scripts/ │ └── … # Скрипты виртуального окружения
├── .gitignore # Файл для игнорирования файлов в Git (например, .venv)
├── pyvenv.cfg # Файл конфигурации виртуального окружения
├── bottapi.py # Основной файл Python с кодом бота
└── README.md # Этот файл с описанием проекта
 ```

## Как использовать

1.  Установите необходимые библиотеки:
    ```bash
    pip install pyTelegramBotAPI requests
    ```
2.  Запустите бота:
    ```bash
    python bottapi.py
    ```
3.  Отправьте команду `/jenkins` боту, чтобы увидеть информацию из Jenkins.

## Настройки

*   Замените токен бота в файле `bottapi.py`:
    ```python
    bot = telebot.TeleBot("ВАШ_ТОКЕН_БОТА")
    ```
*   Настройте параметры доступа к Jenkins в файле `bottapi.py`:
    ```python
    JENKINS_URL = "http://<адрес_jenkins>/api/python?tree=..."
    JENKINS_USERNAME = "<имя_пользователя_jenkins>"
    JENKINS_PASSWORD = "<пароль_пользователя_jenkins>"
    ```
