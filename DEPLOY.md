# Deploying — one live URL for judging

The whole app ships as **one web service**: a Docker image builds the React
dashboard and runs the FastAPI backend that serves it. So the **dashboard, REST
API, and WebSocket all live on a single URL** — no CORS, and secure WebSockets
(`wss://`) work automatically.

```
                 ┌─────────── one Render web service ───────────┐
  browser ──────▶│  FastAPI  ──serves──▶ built React dashboard    │
  Discord bot ──▶│  (same process runs the asyncio simulator)     │
                 └────────────────────────────────────────────────┘
                 https://office-energy-monitor.onrender.com
```

## Deploy the backend + dashboard to Render (free)

1. **Push to GitHub** (already done for this repo).
2. Go to **[render.com](https://render.com)** → sign in with GitHub.
3. Click **New +** → **Blueprint**.
4. Pick this repository. Render reads [`render.yaml`](render.yaml) and proposes a
   free Docker web service named `office-energy-monitor`. Click **Apply**.
5. Wait for the first build (~3–5 min: it builds the dashboard, then the Python
   image). When it's **Live**, open the URL Render gives you, e.g.
   `https://office-energy-monitor.onrender.com` — that's your dashboard.

That URL is what you share with judges. `…/healthz` returns a JSON health check;
`…/api/state` is the raw data if anyone wants to see the single source of truth.

> **Free-tier note.** A free Render service **sleeps after ~15 min idle** and
> cold-starts in ~50 s on the next hit. Before you present, open the URL once to
> wake it, then it's snappy. (Upgrading to the $7 Starter plan removes the sleep
> if you want zero cold-start during judging.)

### No `render.yaml`? Configure manually instead
New + → **Web Service** → pick the repo → **Runtime: Docker** → Plan **Free** →
Health Check Path `/healthz` → add env vars `SIM_SPEED=60`,
`WATT_JITTER_PCT=0.05` → **Create**.

## Point the Discord bot at the live backend

The dashboard and the bot **must read the same backend**, or they'll show
different data (each backend instance runs its own simulator). So set the bot's
`BACKEND_URL` to your Render URL:

```bash
# bot/.env
DISCORD_TOKEN=your-bot-token
DISCORD_CHANNEL_ID=your-channel-id
GEMINI_API_KEY=your-gemini-key
BACKEND_URL=https://office-energy-monitor.onrender.com   # <-- the Render URL
```

Then run the bot during the demo:

```bash
cd bot && . .venv/bin/activate && python bot.py
```

Now `!status`, `!room`, `!usage`, `!alerts` in Discord report the **exact same
live state** judges see on the web dashboard. ✅

## Run the production image locally first (optional sanity check)

```bash
docker build -t office-energy-monitor .
docker run --rm -p 8000:8000 office-energy-monitor
# open http://localhost:8000  — dashboard, API, and WebSocket all on one port
```

## Environment variables

| Var | Where | Default | Purpose |
|---|---|---|---|
| `PORT` | backend | `8000` | Render injects this; the container binds to it. |
| `SIM_SPEED` | backend | `60` | Sim seconds per real second (accelerated day). |
| `WATT_JITTER_PCT` | backend | `0.05` | ± wattage jitter so the meter looks live. |
| `STATIC_DIR` | backend | `../dashboard/dist` | Where the built dashboard lives (set by the image). |
| `VITE_API_BASE` | dashboard build | *(same origin)* | Only needed if the backend is hosted separately. |
| `BACKEND_URL` | bot | `http://localhost:8000` | Must point at the deployed backend. |
| `DISCORD_TOKEN`, `DISCORD_CHANNEL_ID`, `GEMINI_API_KEY` | bot | — | Bot secrets — keep in `bot/.env`, never commit. |
