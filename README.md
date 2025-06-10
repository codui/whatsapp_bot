<!-- Documentation of project -->
whatsapp_bot_project/
│
├── main.py                       # Точка входа — запуск логики бота
├── bot/
│   ├── __init__.py
│   ├── bot_controller.py        # Основной контроллер логики бота
│   ├── message_handler.py       # Обработка входящих сообщений
│   └── media_downloader.py      # Скачивание фото/медиа
│
├── utils/
│   ├── __init__.py
│   ├── selenium_setup.py        # Инициализация Selenium WebDriver
│   └── helpers.py               # Утилиты: парсинг, логирование и др.
│
├── data/
│   └── downloads/               # Сюда будут сохраняться скачанные фото
│
├── config/
│   └── settings.py              # Конфигурация: пути, селекторы, таймауты
│
├── requirements.txt             # Зависимости (Selenium и др.)
└── README.md                    # Документация проекта
