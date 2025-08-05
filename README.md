# OVRS

Secure FastAPI backend skeleton demonstrating JWT authentication, bcrypt password hashing, Pydantic validation, async SQLAlchemy ORM usage with connection pooling, background tasks, structured logging and Dockerized deployment.

## Running

1. Create a `.env` based on `.env.example` and adjust values as needed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Features

- **Async database**: uses SQLAlchemy's async engine with configurable pool size and overflow.
- **Background tasks**: POST to `/tasks/log` with a `message` body to see a background logger task.
- **Structured logging**: loguru outputs JSON logs with rotation configured via env vars.
- **Dockerized**: `docker-compose up --build` launches the API along with Postgres and Redis.
- **Roles & Teams**: users belong to companies/teams with admin/editor/viewer roles enforced via RBAC middleware.
- **Export & Integrations**: admins can pull analytics exports in CSV/JSON or connect to n8n workflows through a secured webhook.
- **Admin Settings**: admins manage runtime settings via `/op/settings`, persisted in the `SystemSettings` table and surfaced in the frontend control panel.

## Analytics & Social Listening

- POST `/analytics/ingest` stores campaign metrics and returns CTR, CPA and ROI with optimization tips.
- POST `/listening/analyze` analyzes sentiment of brand mentions and triggers alerts on spikes of negative sentiment.

Example `/analytics/ingest`:

```json
[
  {"platform": "google", "impressions": 1000, "clicks": 50, "spend": 100, "revenue": 150, "conversions": 5}
]
```

Response:

```json
[
  {"platform": "google", "ctr": 0.05, "cpa": 20.0, "roi": 0.5, "tips": []}
]
```

Example `/listening/analyze`:

```json
{"text": "I love this brand"}
```

Response:

```json
{"text": "I love this brand", "sentiment": 0.5}
```

Alert trigger sample:

```python
from app.alerts.notifier import check_negative_sentiment

await check_negative_sentiment(db)
```

Example async query:

```python
result = await session.execute(select(User).where(User.username == username))
```

Sample log output:

```json
{"message": "startup complete", "level": "INFO"}
```

## Frontend

A Vite + React client lives in `frontend/` using TailwindCSS and shadcn/ui components with an Apple‑inspired dark theme.

### Dev server

```bash
cd frontend
npm install
npm run dev
```

### Sample components

`<MetricsCard />` renders KPI tiles and `<SentimentRow />` shows brand mentions with sentiment colouring.

### API usage

Requests include token auth when available:

```ts
import { fetchWithToken } from '@/services/api'

const token = localStorage.getItem('token') || ''
const funnel = await fetchWithToken(token, '/analytics/funnel')
```

## Developer Docs

Full developer documentation covering setup, environment variables, API examples and troubleshooting lives in [`docs/DEV.md`](docs/DEV.md).
