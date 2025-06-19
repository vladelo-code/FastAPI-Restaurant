from fastapi import FastAPI
from app.api.api import api_router

app = FastAPI(
    title='FastAPI-Restaurant',
    description="""
**Made by Vladislav Lahtionov**

---

### Контакты

- [Telegram](https://t.me/vladelo)
- [Резюме на hh.ru](https://hh.ru/resume/cf857c35ff0e72c7610039ed1f745836647a4c)
- [Резюме на Яндекс.Диске](https://disk.yandex.ru/i/iDIPdISB0F__Tg)

---

Приятного использования API!
"""
)

app.include_router(api_router)

# Для запуска – uvicorn app.main:app --reload
