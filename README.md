# Restaurant Booking API

API для управления бронированием столов в ресторане. Позволяет управлять столами и бронированиями через RESTful интерфейс.

## 🚀 Возможности

- Управление столами (создание, чтение, обновление, удаление)
- Бронирование столов с проверкой доступности
- Валидация времени бронирования
- Поддержка временных зон (UTC)
- Подробная документация API
- Проверка здоровья системы
- Автоматическое применение миграций при запуске
- Логирование операций
- Полное покрытие тестами

## 🛠 Технологии

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (миграции)
- Docker & Docker Compose
- Pydantic

## 📋 Требования

- Docker
- Docker Compose
- Python 3.11 (для локальной разработки)

## 🚀 Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Xameerz/restaurant_broner.git
cd restaurant_broner
```

2. Создайте файл `.env`:
```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/restaurant
```

3. Запустите проект с помощью Docker Compose:
```bash
docker-compose up --build
```

После запуска:
- API будет доступен по адресу: `http://localhost:8000`
- Миграции будут применены автоматически
- База данных будет инициализирована

## 📚 Документация API

После запуска API документация доступна по следующим URL:

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`
- OpenAPI спецификация: `http://localhost:8000/api/openapi.json`

### Основные эндпоинты

#### Столы
- `GET /api/tables` - Получить список всех столов
- `GET /api/tables/{table_id}` - Получить информацию о конкретном столе
- `POST /api/tables` - Создать новый стол
- `PUT /api/tables/{table_id}` - Обновить информацию о столе
- `DELETE /api/tables/{table_id}` - Удалить стол

#### Бронирования
- `GET /api/reservations` - Получить список всех бронирований
- `GET /api/reservations/{reservation_id}` - Получить информацию о конкретном бронировании
- `POST /api/reservations` - Создать новое бронирование
- `PUT /api/reservations/{reservation_id}` - Обновить информацию о бронировании
- `DELETE /api/reservations/{reservation_id}` - Удалить бронирование

## 🔧 Разработка

### Локальная разработка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
.\venv\Scripts\activate  # для Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите сервер разработки:
```bash
uvicorn app.main:app --reload
```

### Миграции

Для создания новой миграции:
```bash
alembic revision --autogenerate -m "описание изменений"
```

Для применения миграций вручную (если нужно):
```bash
alembic upgrade head
```

## 🧪 Тестирование

Для запуска тестов используйте следующие команды:

```bash
# Установите зависимости для тестов
pip install -r requirements.txt

# Запустите все тесты
pytest

# Запустите тесты с отчетом о покрытии в консоли
pytest --cov=app --cov-report=term-missing

# Запустите тесты с HTML отчетом о покрытии
pytest --cov=app --cov-report=html
```

После запуска тестов с HTML отчетом, вы можете открыть файл `htmlcov/index.html` в браузере для просмотра детального отчета о покрытии кода тестами.

## 📝 Структура проекта

```
restaurant-booking/
├── alembic/              # Миграции базы данных
├── app/
│   ├── models/          # SQLAlchemy модели
│   ├── schemas/         # Pydantic схемы
│   ├── routers/         # FastAPI роутеры
│   ├── services/        # Бизнес-логика
│   ├── database.py      # Настройка базы данных
│   └── main.py          # Точка входа приложения
├── tests/               # Тесты
├── .env                 # Переменные окружения
├── .gitignore
├── alembic.ini          # Конфигурация Alembic
├── docker-compose.yml   # Конфигурация Docker Compose
├── Dockerfile          # Конфигурация Docker
├── requirements.txt    # Зависимости Python
└── README.md          # Документация
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add some amazing feature'`)
4. Отправьте изменения в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

MIT

## 👥 Авторы

- [@Xameerz](https://github.com/Xameerz) 
