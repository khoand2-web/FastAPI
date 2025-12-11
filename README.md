# Web Bán Hàng - FastAPI

## Setup (local)
1. Copy `.env.example` to `.env` and adjust values.
2. python -m venv .venv
3. .venv\Scripts\activate (Windows) or source .venv/bin/activate (Unix)
4. pip install -r requirements.txt
5. uvicorn app.main:app --reload

## Notes
- DB defaults to sqlite; set DATABASE_URL for Postgres in .env for production.
- JWT secret: generate securely.
