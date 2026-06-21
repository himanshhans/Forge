# Forge

**Your portfolio, live in minutes.** AI-powered, multi-niche portfolio & contact-card generator. Describe your work → Forge designs, writes, and publishes a site that ranks.

Tagline: _Portfolios & contact cards, beautifully presented._

---

## What it does

- Pick a niche (indie hacker, freelancer, creator, coach, agency) → answer a short brief.
- Groq generates semantic HTML; Forge injects a polished baked-in theme → designed output every time.
- Publishes instantly via **wildcard-serve** (`{subdomain}.forge.app`) — no per-site deploy.
- Per-niche **showcase gallery**, SEO (meta + OG + JSON-LD), export-ready HTML.
- Free tier: 1 portfolio + 1 contact card. Pro (custom domains, more) later.

---

## Stack

| Layer | Tech |
|-------|------|
| Backend | Django 4.2 + DRF, Python 3.10 |
| Database | Neon (PostgreSQL), Django ORM, psycopg3 |
| Auth | Clerk — frontend issues JWT, Django verifies via JWKS (never issues) |
| LLM | Groq (`llama-3.3-70b-versatile`), Together.ai fallback |
| Async | Celery + Redis (optional in dev: eager + LocMem) |
| Frontend | Next.js 14 (App Router), Tailwind 3, Clerk 5, TanStack Query, Framer Motion |
| Publish | Wildcard-serve (HTML stored in DB, served on subdomain) |
| Storage | Cloudflare R2 (avatars/assets) |

Design direction: **Warm Craft Studio** — bone/ink/forest palette, Fraunces serif display + Geist body, light/dark toggle.

---

## Repo layout

```
Forge/
├── backend/        Django REST API  (see backend/README.md)
│   ├── config/         settings, urls, celery
│   ├── apps/
│   │   ├── users/      custom User (Clerk-backed) + JWT auth
│   │   ├── portfolios/ Portfolio model, generate/CRUD, niches, sites endpoint
│   │   └── gallery/    showcase (SQL view)
│   ├── services/       llm_service, portfolio_generator, theme, publisher, avatar
│   └── prompts/        per-niche generation guidance
├── web/            Next.js 14 frontend
│   └── src/app/        landing, gallery, dashboard, portfolio/new, s/[subdomain]
├── mobile/         React Native (not started)
├── shared/         shared types (planned)
└── docker-compose.yml  local Postgres + Redis (optional; Neon used instead)
```

---

## Setup

### Prerequisites
- Python 3.10, Node 20+
- Accounts/keys: [Neon](https://neon.tech), [Clerk](https://clerk.com), [Groq](https://console.groq.com)

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows  (source .venv/bin/activate on unix)
pip install -r requirements.txt
cp .env.example .env             # fill DATABASE_URL (Neon), CLERK_*, GROQ_API_KEY
python manage.py migrate
python manage.py runserver 127.0.0.1:8010
```

### Frontend
```bash
cd web
npm install
# .env.local: NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY, CLERK_SECRET_KEY,
#             NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8010/api/v1
npm run dev                      # http://localhost:3100
```

> **Ports:** backend `8010`, frontend `3100` (8000/3000 are taken by other local apps).

---

## Viewing a published portfolio (local)

After publishing, open either:
- `http://localhost:3100/s/<subdomain>` — path form, always works
- `http://<subdomain>.localhost:3100` — subdomain form (`*.localhost` resolves to 127.0.0.1)

Production serves `<subdomain>.forge.app` via wildcard DNS.

---

## Key API endpoints (`/api/v1/`)

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `niches/` | public | niche configs |
| GET/PATCH | `users/me/` | Clerk | current user |
| POST | `users/webhooks/clerk/` | Svix sig | user sync |
| GET/POST/PATCH/DELETE | `portfolios/` | Clerk | CRUD (user-scoped) |
| POST | `portfolios/generate/` | Clerk | generate (throttled, free-tier checked) |
| POST | `portfolios/{id}/regenerate/` | Clerk | re-run generation |
| GET | `portfolios/{id}/status/` | Clerk | pipeline status poll |
| GET | `gallery/` | public | showcase (filter/sort/search) |
| GET | `sites/{subdomain}/` | public | published HTML/CSS (live only) |

Docs: `http://127.0.0.1:8010/api/docs/` (Swagger).

---

## Tests

```bash
cd backend
.venv\Scripts\python.exe -m pytest      # SQLite, isolated; 16 passing
```

---

## Status

- ✅ Backend API, Neon, Clerk auth, Groq generation, baked theme, wildcard-serve, gallery, free-tier limits
- ✅ Frontend: landing, gallery, create flow, dashboard (regenerate/delete), light/dark
- ⬜ Avatars (Replicate + R2), custom domains (Pro), Stripe, mobile app, Clerk webhook (prod)
