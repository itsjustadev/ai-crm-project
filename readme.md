# Проект для прогрева лидов в Telegram боте с использованием Chat GPT \n и интеграцией с AMOcrm API

<img width="766" alt="Screen Shot 2024-02-25 at 20 57 58" src="https://github.com/itsjustadev/ai-crm-project/assets/86054371/74ec6437-2016-4dad-ab34-ed673067b04d">

Этот проект предназначен для автоматизации процесса прогрева входящих лидов в Telegram боте с использованием Chat GPT и промптов, а также для отслеживания сделок и их переноса по этапам с помощью API AMOcrm.

## Основные файлы находятся в папке `src`

- `main.py`: Основной файл, содержащий основную логику и взаимодействие с Telegram ботом и AMOcrm API.
- `all_functions.py`: Файл, в котором находятся все необходимые функции для выполнения задач проекта.
- `message_handlers.py`: Файл, в котором находятся обработчики сообщений для телеграм-бота.

### Файлы папки `src/databases`

- `models_db.py`: Описание моделей БД.
- `databases.py`: Функции для работы с БД.
- `history_db.py`: Динамические таблицы с историей сообщений для разных пользователей + функции для работы с ними.

### Файлы папки `src/server`

- `server_routes.py`: Файл с эндпоинтами сервера.

## Установка и настройка

1. Установите все зависимости с помощью команды:

   ```shell
   pip install -r requirements.txt
   ```

2. Обратитесь к разработчику:

   telegram: @elpasotoro
