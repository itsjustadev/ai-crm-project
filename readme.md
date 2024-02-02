# Проект для прогрева лидов в Telegram боте с использованием Chat GPT и интеграцией с AMOcrm API

Этот проект предназначен для автоматизации процесса прогрева входящих лидов в Telegram боте с использованием Chat GPT и промптов, а также для отслеживания сделок и их переноса по этапам с помощью API AMOcrm.

## Основные файлы находятся в папке `src`

- `main.py`: Основной файл, содержащий основную логику и взаимодействие с Telegram ботом и AMOcrm API.
- `all_functions.py`: Файл, в котором находятся все необходимые функции для выполнения задач проекта.
- `message_handlers.py`: Файл, в котором находятся обработчики сообщений для телеграм-бота.

# Файлы папки `src/databases`

- `models_db.py`: Функции для работы с БД.
- `databases.py`: Функции для работы с БД.
- `history_db.py`: Динамические таблицы с историей сообщений для разных пользователей.

# Файлы папки `src/server`

- `server_routes.py`: Файл с эндпоинтами сервера.

## Установка и настройка

1. Установите все зависимости с помощью команды:

   ```shell
   pip install -r requirements.txt
   ```

2. Обратитесь к разработчику:

   telegram: @elpasotoro
