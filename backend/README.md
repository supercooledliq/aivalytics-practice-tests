# AiValytics Practice Test Backend

Python + FastAPI backend for the React practice test portal.

## Stack

- Python
- FastAPI
- Pydantic
- Supabase Python client
- Uvicorn
- Docker

## Run With Docker

From the project root:

```bash
docker-compose up --build
```

Frontend:

```text
http://localhost:5173
```

Backend:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/api/health
```

## Supabase Setup

1. Create a Supabase project.
2. Run `backend/supabase/schema.sql` in the Supabase SQL editor.
3. Run `backend/supabase/seed.sql` for starter data.
4. Create `backend/.env` from `.env.example`.
5. Add:

```env
SUPABASE_URL=your-project-url
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

If Supabase credentials are not set, the backend uses in-memory/mock data so frontend work can continue.

## Main Endpoints

```text
GET    /api/health
GET    /api/practice-tests
GET    /api/practice-tests/selection-data
GET    /api/subjects
GET    /api/topics?subjectId=quant
GET    /api/subtopics?topicId=number-systems
POST   /api/test-attempts
GET    /api/test-attempts/:attemptId/questions
PATCH  /api/test-attempts/:attemptId/answers/:questionId
POST   /api/test-attempts/:attemptId/submit
GET    /api/test-attempts/:attemptId/result
GET    /api/users/:userId/recommendations
GET    /api/users/:userId/weak-areas
```

## Example Attempt Payload

```json
{
  "userId": "demo-user",
  "testId": "prime-factors",
  "subjectId": "quant",
  "topicId": "number-systems",
  "subtopicId": "prime-factors"
}
```
