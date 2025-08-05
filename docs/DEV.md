# OVRS Developer Documentation

## Setup
1. Create `.env` from `.env.example` and fill values.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run database and services with Docker:
   ```bash
   docker-compose up --build
   ```
4. Launch the app locally:
   ```bash
   uvicorn app.main:app --reload
   ```

## Architecture
The project follows a service-layered FastAPI structure:
- `models/` SQLAlchemy ORM definitions
- `schemas/` Pydantic models for request/response
- `services/` business logic used by routes
- `routes/` FastAPI routers grouped by domain
- `auth/` security utilities and role-based dependencies

## API Guide
Example invite via curl:
```bash
curl -X POST \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","team_id":1,"role":"editor"}' \
  http://localhost:8000/teams/invite
```

JavaScript fetch for export:
```js
const res = await fetch('/export?format=csv', {
  headers: { Authorization: `Bearer ${token}` }
})
const csv = await res.text()
```

## Environment Variables
| Name | Description |
|------|-------------|
| `SECRET_KEY` | JWT signing secret |
| `JWT_EXPIRATION_HOURS` | Token validity period |
| `BCRYPT_SALT_ROUNDS` | bcrypt cost factor |
| `DATABASE_URL` | Async database connection string |
| `ALLOWED_ORIGINS` | CORS whitelist |
| `REDIS_URL` | Redis instance for alerts |
| `N8N_WEBHOOK_TOKEN` | Shared token securing n8n webhooks |

## Troubleshooting
- **401 Unauthorized**: ensure the `Authorization: Bearer` header contains a valid JWT.
- **403 Forbidden**: the user lacks the required role; check role assignments.
- **Database locked**: using SQLite? ensure only one process writes at a time or switch to Postgres.

## n8n Alert Node Sample
Configure an HTTP Request node:
```json
{
  "url": "http://api:8000/integrations/n8n/alerts",
  "method": "POST",
  "headers": {"X-Webhook-Token": "${N8N_WEBHOOK_TOKEN}", "Authorization": "Bearer <TOKEN>"},
  "body": {"message": "Alert from n8n"}
}
```
