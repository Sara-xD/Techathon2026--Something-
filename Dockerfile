# syntax=docker/dockerfile:1
# ---------------------------------------------------------------------------
# Single-service image: builds the React dashboard, then runs the FastAPI
# backend which serves that bundle from the same origin (REST + WebSocket + UI
# on one URL). This is what Render deploys.
# ---------------------------------------------------------------------------

# 1. Build the dashboard --------------------------------------------------
FROM node:20-slim AS dashboard
WORKDIR /dashboard
COPY dashboard/package.json dashboard/package-lock.json ./
RUN npm ci
COPY dashboard/ ./
# Production build -> API base resolves to same-origin at runtime (see api.js).
RUN npm run build

# 2. Python runtime -------------------------------------------------------
FROM python:3.12-slim AS runtime
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install -r backend/requirements.txt

COPY backend/ ./backend/
# Bring the built dashboard to the path backend/app/main.py looks for.
COPY --from=dashboard /dashboard/dist ./dashboard/dist

# Render provides $PORT; default to 8000 for local `docker run`.
ENV PORT=8000
EXPOSE 8000
WORKDIR /app/backend
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
