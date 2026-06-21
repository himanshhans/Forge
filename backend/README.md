# Forge Backend (Django + DRF)

AI multi-niche portfolio generator API. Auth = Clerk (verify only). DB = Neon/Postgres.
Gen = Groq. Publish = wildcard-serve. Storage = R2.

## Stack
- Python 3.10, Django 4.2, DRF
- psycopg3, Neon Postgres (local: docker-compose Postgres)
- Clerk JWT verify (JWKS, no token issuing)
- Celery + Redis (async avatar/publish)
- DRF throttling (Redis backend)

## Local setup
```bash
# 1. infra (from repo root)
docker compose up -d        # Postgres :5432 + Redis :6379

# 2. backend
cd backend
python -m venv .venv         # use Python 3.10/3.11/3.12
.venv\Scripts\activate       # win;  source .venv/bin/activate (unix)
pip install -r requirements.txt
cp .env.example .env         # fill secrets (Clerk, Groq, R2...)

python manage.py migrate
python manage.py createsuperuser   # optional, admin
python manage.py runserver
```

## Endpoints
- `GET /health/` — liveness
- `GET /api/docs/` — Swagger UI
- `GET /api/schema/` — OpenAPI
- `/api/v1/...` — users, portfolios, gallery (wiring in progress)

## Layout
```
config/        settings, urls, celery, wsgi/asgi
apps/users/    custom User (Clerk-backed) + ClerkJWTAuthentication
apps/portfolios/  Portfolio, AvatarGeneration, PortfolioAnalytics, niches.py (hardcoded)
apps/gallery/  ShowcaseEntry (managed=False, backed by SQL view)
```

## Notes
- Niche configs hardcoded in `apps/portfolios/niches.py` (5 stable niches, no DB table).
- Gallery = `showcase_index` SQL VIEW (migration `gallery/0001`), no sync logic.
- Free-tier limits (1 portfolio / 1 card) enforced in service layer — settings `FREE_PLAN_MAX_*`.
- Verify before prod: `GROQ_MODEL` live catalog, Together.ai free tier, Clerk MAU, R2/CF pricing.
