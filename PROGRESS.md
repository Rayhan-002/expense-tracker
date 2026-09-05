# Expense Tracker — Progress & Roadmap

> Single source of truth for this project. Read this first in any new session to resume with full context.

## Where we left off (read this first)

**PostgreSQL switch is done and verified** (2026-08-27): installed Postgres 17 locally, created a dedicated `expense_user` role + `expense_tracker_db` database (not using the `postgres` superuser for the app), added `.env` + `python-dotenv` support so `SECRET_KEY`/`DEBUG`/DB credentials are no longer hardcoded in `settings.py`, switched `DATABASES` to the `psycopg2`/postgresql engine, ran `migrate` successfully — all 12 tables (Django built-ins + `expenses_category`/`expenses_expense`) confirmed present via `psql \dt`. SQLite is no longer used by the app (the old `db.sqlite3` file is just an unused leftover on disk).

**Work mode (decided 2026-08-27):** Claude explains and hands over small code snippets and exact terminal commands; the user types/pastes code themselves and runs all commands themselves, then reports back output. Claude does not directly edit application code files (Python/TS) or run terminal commands on this project — only this PROGRESS.md is edited directly. (One documented exception: Claude fixed a PATH/env issue directly when explicitly asked to, since it was pure environment troubleshooting, not learning content.)

**Housekeeping done (2026-08-27):** `.gitignore` fixed (added `db.sqlite3`, `.vscode/`), unused `db.sqlite3` deleted, `MAILERS` typo fixed to `EMAIL_BACKEND`, `backend/requirements.txt` generated (`pip freeze`), first real commit made (`a8f23af` — Django+DRF backend with Category/Expense models on PostgreSQL). `.vscode/` deliberately left untracked (local editor/extension state, not shared project config).

**Phase 3 core work is done and verified (2026-08-28):** `expenses/serializers.py` (CategorySerializer, ExpenseSerializer), `expenses/views.py` (generic ListCreateAPIView/RetrieveUpdateDestroyAPIView pairs for both models, `IsAuthenticated`, per-user `get_queryset()` filtering, `perform_create()` auto-assigning `user`), `expenses/urls.py` + wired into `config/urls.py` under `/api/`. Tested live via the DRF browsable API: create/list/retrieve/update all confirmed working; anonymous requests correctly get `403`; cross-user category assignment on `Expense` is blocked both by a scoped serializer field queryset and a custom `validate_category` check. Django admin also has both models registered now, and a second (staff) test user exists for cross-user testing.

**Phase 4 progress (2026-08-30):** installed `djangorestframework-simplejwt`, added `REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES` (JWT + Session fallback) in `settings.py`, wired `POST /api/auth/login/` (`TokenObtainPairView`) and `POST /api/auth/refresh/` (`TokenRefreshView`) directly in `config/urls.py`. Both tested and confirmed working via Postman — login returns access+refresh tokens, refresh returns a new access token, and `GET /api/categories/` was confirmed reachable using only a `Bearer` token (no session cookie), proving JWT auth works end-to-end.

Created a new `accounts` app (registered in `INSTALLED_APPS`) specifically for user-account logic, kept separate from the `expenses` domain app. Wrote `backend/accounts/serializers.py` with `RegisterSerializer` (uses `User.objects.create_user()` so passwords are hashed, `password` field is `write_only`, uses Django's `validate_password`).

**Not yet done — pick up here next:**
1. `backend/accounts/views.py` — add a `RegisterView(generics.CreateAPIView)` using `RegisterSerializer`, with `permission_classes = [permissions.AllowAny]` (registration must be open to logged-out users).
2. `backend/accounts/urls.py` (new file) — `path('register/', RegisterView.as_view(), name='register')`.
3. Wire into `backend/config/urls.py` via `path('api/auth/', include('accounts.urls'))`.
4. Test `POST /api/auth/register/` via Postman, then confirm the new user can log in via `/api/auth/login/`.
5. Once registration works, Phase 4 is essentially complete — move to Phase 5 (Next.js frontend).

**Testing setup (for reference):** using Postman, collection organized in resource-based folders (`Auth`, `Categories`, `Expenses`), an environment variable `base_url_expense_tracker` = `http://127.0.0.1:8000`, and a Tests script on the login request that auto-saves `access`/`refresh` into environment variables `access_token`/`refresh_token` for reuse in other requests.

## Project context

Learning project, built after finishing "TaskLens" (a complete full-stack project, used for interview submission). TaskLens proved the user can ship a full-stack app but left gaps in understanding the end-to-end process. This project is deliberately small, manual, and slow — the goal is understanding every stage, not just a working app.

**How we work together:**
- User implements manually. Claude Code teaches and guides, reviews what's written — it does not silently implement whole features unprompted.
- Go slow, one concept at a time, explain the *why*.
- If the user is stuck, nudge toward the answer before just doing it.
- Keep this file updated as phases complete.

**History:** Started with ChatGPT (free tier, hit usage limits) — it explained the Django CLI setup, and together they designed the schema; ChatGPT wrote the initial `models.py`. Claude Code is continuing from there.

## Tech stack

Frontend: Next.js + TypeScript + Tailwind · Backend: Django + DRF · Database: PostgreSQL (target, currently SQLite) · Auth: JWT · Deployment: Vercel + Render · Docker: added later, after the app works without it.

## Roadmap

- [~] **Phase 1 — Foundation**: Git init, Django setup, env config (.env + python-dotenv) done · Next.js setup still pending
- [x] **Phase 2 — Database**: models, migrations, relationships, constraints done · now on PostgreSQL
- [x] **Phase 3 — Backend**: DRF serializers, views, urls, CRUD APIs, validation, permissions — done and tested
- [~] **Phase 4 — Authentication**: login, JWT, protected routes, user ownership all done and tested · registration in progress (serializer written, view/urls not wired yet)
- [ ] **Phase 5 — Frontend**: Next.js structure, pages, components, forms, API client, auth UI
- [ ] **Phase 6 — Integration**: frontend ↔ API, error handling, loading states, optimistic updates
- [ ] **Phase 7 — Features**: search, filtering, sorting, pagination, dashboard, statistics
- [ ] **Phase 8 — Quality**: testing, security, code organization, error handling, API docs
- [ ] **Phase 9 — Deployment**: production DB, backend/frontend deploy, env vars, CORS, prod debugging
- [ ] **Phase 10 — Portfolio**: README, architecture diagram, screenshots, demo, CV bullets, GitHub cleanup

## Planned API surface (target for Phase 3+)

Auth: `POST /api/auth/register/`, `POST /api/auth/login/`
Categories: `GET/POST /api/categories/`, `PATCH/DELETE /api/categories/:id/`
Expenses: `GET/POST /api/expenses/`, `GET/PATCH/DELETE /api/expenses/:id/`
Dashboard: `GET /api/dashboard/`

## Current repo state

- `backend/` — Django project `config` + app `expenses`. Models done (`Category`, `Expense`, both owned by `User`, `Category→Expense` uses `PROTECT` so a category can't be deleted while expenses reference it). Everything else (`views.py`, `admin.py`, tests) is still the default empty stub — no serializers or urls exist yet.
- `frontend/` — empty directory, Next.js not initialized.
- Only one git commit exists in the repo so far; `backend/` is entirely uncommitted.

**Known rough edges to fix during housekeeping:** `MAILERS` in `settings.py` isn't a real Django setting (should be `EMAIL_BACKEND`); `db.sqlite3` isn't gitignored; no `requirements.txt` exists yet.

## Session log

- **2026-08-27** — Claude Code reviewed the existing scaffold, confirmed the gaps above, created this progress file. Switched database to PostgreSQL (local install, dedicated `expense_user`/`expense_tracker_db`, `.env` + `python-dotenv`), completed housekeeping, made the first real commit. Merged `dev` into `main` as a checkpoint.
- **2026-08-28** — Built and tested Phase 3 (DRF serializers, views, urls, CRUD, validation, permissions) for `Category`/`Expense`. Verified live via the browsable API with two test users. Committed, pushed, merged into `main`.
- **2026-08-30** — Built and tested JWT login + refresh (Phase 4). Started registration: created `accounts` app, wrote `RegisterSerializer`. Pausing here to work on another project — resume at the "Not yet done" list above (RegisterView → urls → test). Not yet committed.
