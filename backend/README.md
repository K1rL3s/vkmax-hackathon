# Бэкенд

Состоит из веб-апи fastapi, бота maxo, шедулера taskiq, очереди nats, бд psql и redis.

## Docker

### Локальный запуск

1. Всё внутри докера:
    ```bash
    docker compose -f docker-compose.local.yml up --build -d
    ```
    ```bash
    docker compose -f docker-compose.local.yml up --build -d api
    ```
2. Запуск из IDE:
    1. Поднять psql и redis:
        ```bash
        docker compose -f docker-compose.local.yml --env-file=.env run --remove-orphans -d -p 5432:5432 database
        docker compose -f docker-compose.local.yml --env-file=.env run --remove-orphans -d -p 6379:6379 redis
        ```
    2. Запускать из `MAX_task_magager/backend`:
        ```bash
        python -m maxhack.bot
        python -m maxhack.web
        python -m maxhack.scheduler
        python -m maxhack.broker
        ```

---

## Реализованные фичи

- Блэ блэ
- Блэ
  - Блю блю
  - Блю
  - Хоп
  - Буль
- Буль
- Буль
- Lingang Guli Guli Guli Watcha
- Lingang Gu Lingang Gu

---

## Технологии

- `Python` как связующее
- `Postgres` как РСУБД для хранения отчётов сканов
- `Nats` как очередь для обмена сообщениями веб-сервера с запускателями nmap'а
- `FastAPI` как веб-сервер
- `FastStream` для работы с Nats'ом
- `SQLAlchemy` как ормка
- `dishka` как DI фреймворк
- `apscheduler` как планировщик
- `black` `isort` `ruff` `mypy` как контроль качества кода

---

## Структура

```
maxhack
│
├───bot - БОТ личной персоной
│   ├───handlers - Обработчики
│   ├───middlewares - Мидлвари
│   └───widgets - Кнопочки и клавиатура
│
├───core - Получение данных из БД, обращения к infra.database
│
├───di - Дишка
│
├───infra - Всё о БД, Алхимия, sql-запросики
│   └───database - БД, контекстные менеджеры и крафт асинхронных сессий
│       ├───models - Моделки
│       └───repos - Репозитории
│
├───logger - Логирование
│   ├───bot - Логи бота
│   └───web - Логи API
│
├───scheduler - Планировщик и т.д
├───utils - всякое)
│
└───web - API и всё что с ним связано
    ├───routes - Запросы в API
    ├───schemas - Схемы веб-API, Валидация payload, очереди
    └───static - Пустая папка и одинокий __init__
migrations - Миграции
```

---

## Взаимодействия

![interaction.png](content/interaction.png)

---

## Пример .env
Смотрите в .env.example
