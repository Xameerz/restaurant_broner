import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Создаем директорию для логов, если её нет
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Настройка формата логов
log_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Настройка корневого логгера
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Консольный обработчик
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)
root_logger.addHandler(console_handler)

# Файловый обработчик
file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5,
    encoding="utf-8"
)
file_handler.setFormatter(log_format)
root_logger.addHandler(file_handler)

# Логгер для базы данных
db_logger = logging.getLogger("sqlalchemy.engine")
db_logger.setLevel(logging.WARNING)

# Логгер для приложения
app_logger = logging.getLogger("app")
app_logger.setLevel(logging.INFO) 