## Технологии

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-000000?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-F80000?style=for-the-badge&logo=alembic&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-FFD43B?style=for-the-badge&logo=pytest&logoColor=black)
![Uvicorn](https://img.shields.io/badge/Uvicorn-FF1C68?style=for-the-badge&logo=uvicorn&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-00B2FF?style=for-the-badge&logo=pydantic&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Logging](https://img.shields.io/badge/Logging-5C5C5C?style=for-the-badge&logo=logstash&logoColor=white)

# 🍽️ FastAPI-Restaurant

Проект REST API для управления рестораном — блюдами и заказами — с использованием **FastAPI**, **SQLAlchemy**, **PostgreSQL** и **Alembic**.

**Автор:** Владислав Лахтионов

- [Telegram](https://t.me/vladelo)
- [Резюме на hh.ru](https://hh.ru/resume/cf857c35ff0e72c7610039ed1f745836647a4c)
- [Резюме на Яндекс.Диске](https://disk.yandex.ru/i/iDIPdISB0F__Tg)

---

## 🚀 Технологии

- Python 3.11+
- FastAPI
- SQLAlchemy (sync)
- Alembic
- PostgreSQL
- Pydantic
- Pytest
- Uvicorn
- Docker
- logging

---

## 📁 Структура проекта

```
FastAPI-Restaurant/
├── app/
│   ├── api/                # Маршруты (эндпоинты FastAPI)
│   ├── core/               # Настройки, логирование, зависимости
│   ├── models/             # SQLAlchemy модели
│   ├── schemas/            # Pydantic-схемы
│   ├── services/           # Бизнес-логика
│   └── main.py             # Точка входа в приложение
│
├── tests/
│   ├── test_dish.py        # Тесты для блюд
│   └── test_order.py       # Тесты для заказов
│
├── alembic/                # Миграции базы данных
│   ├── versions/           # Файлы миграций
│   └── env.py              # Конфигурация Alembic
│
├── docker-compose.yml      # Конфигурация docker-compose для запуска сервисов
├── Dockerfile              # Dockerfile для сборки образа приложения
├── README.md               # Документация проекта
├── alembic.ini             # Настройки Alembic
├── .env.example            # Пример .env
├── requirements.txt        # Зависимости проекта
```

---

## ⚙️ Установка и запуск

1. Клонируй репозиторий:

```bash
git clone https://github.com/vladelo777/FastAPI-Restaurant.git
cd FastAPI-Restaurant
```

2. Установи зависимости:

```bash
pip install -r requirements.txt
```

3. Настрой переменные окружения в `.env`, используя `.env.template`.


4. Примени миграции:

```bash
alembic upgrade head
```

5. Запусти сервер:

```bash
uvicorn app.main:app --reload
```

---

## 🧪 Тестирование

```bash
pytest
```

Тесты используют `httpx` и `TestClient` FastAPI, чтобы покрыть основные сценарии запросов/ответов.

---

## 📘 Методы API

- `GET /dishes/` — список всех блюд
- `POST /dishes/` — добавить новое блюдо
- `DELETE /dishes/{id}` — удалить блюдо


- `GET /orders/` — список всех заказов
- `POST /orders/` — создать новый заказ
- `DELETE /orders/{id}` — отменить заказ
- `PATCH /orders/{id}/status` — изменить статус заказа

Документация Swagger доступна по адресу:

```
http://localhost:8000/docs
```

---

## 📄 Логгирование

Проект использует встроенный логгер (`app/core/logger.py`) для отладки и отслеживания операций, включая:

- создание/удаление блюд,
- создание заказов,
- обновление статуса и ошибки.

---

## 📬 **Контакты**

Автор: Владислав Лахтионов  
GitHub: [vladelo777](https://github.com/vladelo777)  
Telegram: [@vladelo](https://t.me/vladelo)

💌 Не забудьте поставить звезду ⭐ на GitHub, если вам понравился проект! 😉