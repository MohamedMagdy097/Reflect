# Technology Stack: Feedback/Reputation Features

**Project:** Reflect (Post-date feedback platform)
**Researched:** January 2026
**Confidence:** HIGH for backend, MEDIUM for frontend (Next.js ecosystem moving rapidly)

## Overview

This stack extends your existing FastAPI + Next.js 14 + SQLite foundation with production-grade libraries for feedback collection, reputation aggregation, and public profile caching. Emphasizes simplicity of deployment (keep single SQLite database) while adding specialized tools for the feedback domain.

---

## Recommended Stack

### Backend: Authentication & Sessions

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **PyJWT** | 2.8+ | JWT token generation & verification | Official FastAPI recommendation (replaces deprecated python-jose). Simple, lightweight, widely audited. |
| **fastapi-jwt-auth** | 0.5.0+ | FastAPI JWT extension with refresh tokens | Provides access + refresh token pattern out of the box. Handles token freshness validation and revocation. Less code than manual implementation. |
| **python-multipart** | 0.0.5+ | Form data parsing in FastAPI | Required for proper form submission handling in POST requests. |
| **email-validator** | 2.0+ | Email validation for user registration | Validates format AND checks DNS records. Critical for feedback platform where email authenticity matters. |

**Rationale:** FastAPI's native OAuth2 + JWT tutorial now recommends PyJWT over python-jose (which is abandoned). fastapi-jwt-auth provides refresh token logic that users expect (15-30 min access token, 7-day refresh token). HttpOnly cookies for refresh tokens prevent XSS compromise.

**Session Pattern:**
```python
# Access token: short-lived (15-30 min), used for API calls
# Refresh token: long-lived (7 days), stored in HttpOnly cookie, used to get new access token
# Upon feedback submission: require fresh access token to prevent CSRF
```

---

### Backend: Data Validation & Schemas

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **Pydantic** | v2.5+ | Request/response schema validation | Already bundled with FastAPI. Provides runtime validation with strong typing. Essential for reputation data consistency. |
| **Pydantic[email]** | v2.5+ | Email field validation | Stricter than standard email-validator. Use for user schemas. |

**Rationale:** Pydantic v2 (with Rust core) is faster than v1 and recommended for FastAPI. For feedback forms, Pydantic enforces schema at API boundary before database writes. Prevents malformed ratings (e.g., 6-star ratings) from entering system.

**Example schema for feedback submission:**
```python
class FeedbackCreate(BaseModel):
    recipient_id: int
    rating: int  # Pydantic validates: 1-5 range
    category: Literal["authenticity", "vibe", "safety"]
    text: str = Field(..., min_length=10, max_length=500)
```

---

### Backend: Database & ORM

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **SQLAlchemy** | 2.0+ | Async ORM for database operations | Supports async/await for non-blocking I/O. Better than sync for feedback aggregation queries under load. |
| **aiosqlite** | 0.19+ | Async driver for SQLite | Enables `sqlite+aiosqlite://` connection string. Allows FastAPI async routes to query SQLite without thread pool overhead. |
| **Alembic** | 1.13+ | Database migrations | Manage feedback table schema evolution (new rating categories, new fields). Essential as product evolves. |

**Rationale:** You're already using SQLite. Async SQLAlchemy + aiosqlite handles 3-5x more concurrent profile views without blocking. Perfect for public reputation dashboard. Alembic lets you roll out new feedback fields without manual SQL.

**Alternative considered:** PostgreSQL. NOT recommended yet—SQLite is simpler to deploy and sufficient for phase 1. Migrate to Postgres only when you exceed SQLite's write concurrency limit (~100 concurrent writers).

---

### Backend: Caching Layer

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **Redis** (optional for phase 1) | 7.0+ | Session + profile cache | Only needed if public profile views exceed 1K/sec. For early phases, skip this. |
| **SQLite FTS5** (built-in) | 3.10+ | User search indexing | Full-text search built into SQLite. Query user profiles by name/bio without external search service. Median latency: single-digit milliseconds. |

**Rationale:**
- **Caching strategy:** User profile stats (rating avg, feedback count) change infrequently. Cache with 1-hour TTL + event-based invalidation on new feedback.
- **Search:** SQLite FTS5 is sufficient for MVP. Users can search "alice" and find all users matching that name. No Elasticsearch needed.
- **When to add Redis:** Once you deploy and see cache hit ratios <80% OR profile view requests >1K/sec, add Redis in front.

**Caching pattern (no Redis yet):**
```python
# In-memory cache with TTL using fastapi-cache2 (optional)
# Or: Simple SQLite query with 1-hour browser cache headers
# When feedback posted: invalidate recipient's cache entry
```

---

### Frontend: Form Handling & Validation

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **React Hook Form** | 7.48+ | Form state management | Industry standard for React/Next.js. Minimal re-renders (critical for complex feedback forms). ~9KB gzipped. |
| **Zod** | 3.22+ | Client-side schema validation | TypeScript-first. Works seamlessly with React Hook Form. Catches validation errors before API call. |
| **@hookform/resolvers** | 3.3+ | Adapter for Zod + React Hook Form | Glue layer—lets Zod schemas validate React Hook Form. |

**Rationale:**
- React Hook Form + Zod is the 2025 gold standard for Next.js forms. Minimal bundle impact.
- Zod on frontend mirrors Pydantic on backend. Same schema logic both sides = fewer bugs.
- Server Actions (Next.js 14) handle form submission server-side, but React Hook Form manages client state.

**Form pattern:**
```typescript
// Frontend
const feedbackSchema = z.object({
  rating: z.number().min(1).max(5),
  category: z.enum(["authenticity", "vibe", "safety"]),
  text: z.string().min(10).max(500),
});

// Server Action (next/app/actions.ts)
'use server'
export async function submitFeedback(formData) {
  // Zod schema validates, then call FastAPI /feedback endpoint
}
```

---

### Frontend: UI & Styling

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **Tailwind CSS** | 3.4+ | Utility-first CSS framework | Already likely in your Next.js setup. Rapid iteration for feedback UI. ~15KB gzipped. |
| **shadcn/ui** | Latest | Accessible component library | Pre-built form components (Form, Input, Textarea, RadioGroup, Select). Copy-paste, no extra dependency. Great for rating selector UI. |
| **Radix UI** | 1.0+ | Headless UI primitives | Underlying Radix components (Dialog for confirmation modal, Tooltip for rating explanations). Accessible by default. |

**Rationale:** shadcn/ui form components integrate perfectly with React Hook Form. Use Radix Dialog for "confirm feedback submission" modal. Radix Tooltip for "What does authenticity mean?" help text.

---

### Frontend: Data Fetching & State

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **SWR** or **TanStack Query** | v3.0+ (TQ) | Stale-while-revalidate caching | For fetching public profiles, feedback history, user search results. Handles cache invalidation when feedback posted. |
| **fetch API** | Built-in | HTTP requests | Next.js 14 fetch is enhanced with auto-caching. Use for simple requests. |

**Rationale:**
- For MVP: Just use `fetch` + Next.js caching headers. Simpler.
- For post-MVP: Add TanStack Query when you need smart cache invalidation (e.g., after posting feedback, refresh recipient's profile automatically).

---

### Frontend: State Management

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **React Context** | Built-in | Authenticated user state (current user ID, token) | Sufficient for small app. Pass user token to API requests. |
| **Zustand** | 4.4+ | (Optional) Global feedback state | Only if you need complex multi-step feedback forms or feedback list filtering. Skip for MVP. |

**Rationale:** Feedback submission is mostly form → API → done. Context is enough. Avoid Redux—too much boilerplate for this domain.

---

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| **JWT library** | PyJWT + fastapi-jwt-auth | python-jose | python-jose abandoned. PyJWT is actively maintained. |
| **User search** | SQLite FTS5 | Elasticsearch | Elasticsearch adds deployment complexity (separate container). FTS5 is built-in. Only migrate if you hit 10K+ users and need fuzzy matching. |
| **Form library** | React Hook Form + Zod | Formik | RHF is lighter weight (9KB vs 26KB). Better TypeScript support. |
| **Caching** | (None for MVP) | Redis | Redis adds operational overhead. SQLite with HTTP caching headers works for MVP. Add Redis when needed. |
| **ORM** | SQLAlchemy 2.0 async | Tortoise ORM | SQLAlchemy is more mature. Tortoise is newer, less battle-tested. |

---

## Installation & Setup

### Backend Dependencies

```bash
# Core FastAPI stack
pip install fastapi==0.109.0 uvicorn==0.27.0

# Authentication
pip install PyJWT==2.8.0 fastapi-jwt-auth==0.5.0

# Database
pip install sqlalchemy==2.0.23 aiosqlite==0.19.0 alembic==1.13.0

# Validation
pip install pydantic==2.5.0 email-validator==2.0.0

# Form parsing
pip install python-multipart==0.0.6

# Development
pip install pytest==7.4.0 pytest-asyncio==0.21.0 httpx==0.25.0
```

### Frontend Dependencies

```bash
# Already in Next.js 14 app
npm install react==18.2.0 next==14.0.0

# Form handling
npm install react-hook-form==7.48.0 zod==3.22.0 @hookform/resolvers==3.3.0

# UI
npm install tailwindcss==3.4.0
npm install -D shadcn-ui  # Copy component files, don't npm install

# Data fetching
npm install swr  # or add TanStack Query later
```

---

## Configuration Patterns

### Authentication Middleware (FastAPI)

```python
# app/security.py
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings

class Settings(BaseSettings):
    authjwt_secret_key: str = "secret-key-for-dev"  # Use env var in prod
    authjwt_algorithm: str = "HS256"
    authjwt_access_token_expires: int = 900  # 15 minutes
    authjwt_refresh_token_expires: int = 604800  # 7 days

@app.post("/feedback", status_code=201)
async def submit_feedback(
    feedback: FeedbackCreate,
    authorize: AuthJWT = Depends(),
):
    """Only fresh access tokens accepted."""
    authorize.fresh_jwt_required()
    user_id = authorize.get_jwt_subject()
    # ... submit feedback
```

### Reputation Aggregation (FastAPI)

```python
@app.get("/users/{user_id}/reputation")
async def get_reputation(user_id: int):
    """Aggregate feedback stats. Cache for 1 hour."""
    cache_key = f"reputation:{user_id}"

    # Check cache (or skip for MVP)

    # Query aggregates
    result = await db.execute(
        select([
            func.avg(Feedback.rating).label("avg_rating"),
            func.count(Feedback.id).label("feedback_count"),
            func.count(distinct(Feedback.author_id)).label("unique_raters"),
        ]).where(Feedback.recipient_id == user_id)
    )

    # Cache for 1 hour
    return ReputationSchema(**result)
```

### Form Validation (Next.js)

```typescript
// app/actions.ts
'use server'
import { z } from 'zod'

const feedbackSchema = z.object({
  recipientId: z.number(),
  rating: z.number().min(1).max(5),
  text: z.string().min(10).max(500),
})

export async function submitFeedback(formData: FormData) {
  const parsed = feedbackSchema.safeParse({
    recipientId: parseInt(formData.get('recipientId')),
    rating: parseInt(formData.get('rating')),
    text: formData.get('text'),
  })

  if (!parsed.success) {
    return { error: parsed.error.flatten() }
  }

  const res = await fetch(`${API_URL}/feedback`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(parsed.data),
  })

  return res.json()
}
```

---

## Performance Targets

| Metric | Target | How to Achieve |
|--------|--------|----------------|
| **API latency (POST /feedback)** | <200ms p99 | Async SQLAlchemy, indexed recipient_id |
| **Profile view latency (GET /users/:id/reputation)** | <100ms p99 | SQLite FTS5 + HTTP cache headers (1 hour) |
| **JWT validation overhead** | <5ms | PyJWT is simple crypto, no DB lookup needed |
| **Form validation (client)** | <10ms | Zod compiles schema once, reuses |
| **Search query (GET /users?q=alice)** | <50ms | SQLite FTS5 on user names/bios |

**Scaling path:**
1. **Phase 1 (MVP):** All in-memory with SQLite. No Redis. Monitor metrics.
2. **Phase 2 (1K users):** Add HTTP cache headers for public profiles. Keep SQLite.
3. **Phase 3 (10K users):** Add Redis for reputation aggregates. Consider Postgres if write contention spikes.

---

## Deployment Considerations

### Docker (Production)

```dockerfile
# Dockerfile for FastAPI
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Database persistence:** Mount SQLite file as volume:
```yaml
# docker-compose.yml (simplified)
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data  # SQLite file here
    environment:
      DATABASE_URL: sqlite+aiosqlite:///./data/reflect.db
```

### Frontend (Vercel/Self-hosted)

```bash
# Build and deploy Next.js 14
npm run build
npm run start

# Or: vercel deploy (automatic)
```

Vercel handles caching of static assets. Use `revalidate` in Next.js server functions to control ISR (Incremental Static Regeneration).

---

## Security Checklist

- [ ] **Refresh tokens in HttpOnly cookies.** Don't expose in localStorage.
- [ ] **Access tokens short-lived (15-30 min).** Limits damage if leaked.
- [ ] **CORS configured:** Only allow your frontend origin.
- [ ] **Rate limiting:** Use slowapi on feedback endpoint (max 10 feedback/hour per user).
- [ ] **Input validation:** Pydantic + Zod catch injection attacks.
- [ ] **SQL injection:** SQLAlchemy parameterized queries prevent this.
- [ ] **CSRF protection:** Feedback form requires fresh JWT (recent login).

---

## Sources

### Backend Authentication & JWT
- [FastAPI Security/OAuth2 Tutorial](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- [fastapi-jwt-auth GitHub](https://github.com/IndominusByte/fastapi-jwt-auth)
- [FastAPI JWT Auth Discussion](https://github.com/fastapi/fastapi/discussions/9587)
- [Access vs Refresh Tokens](https://testdriven.io/blog/fastapi-jwt-auth/)

### Database & ORM
- [SQLAlchemy 2.0 with FastAPI](https://testdriven.io/blog/fastapi-sqlmodel/)
- [Async SQLAlchemy in FastAPI](https://dev.to/akarshan/asynchronous-database-sessions-in-fastapi-with-sqlalchemy-1o7e)
- [aiosqlite on PyPI](https://pypi.org/project/aiosqlite/)
- [SQLAlchemy Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)

### Frontend Form & Validation
- [React Hook Form Documentation](https://react-hook-form.com/)
- [Zod Documentation](https://zod.dev/)
- [Next.js Forms Guide (2025)](https://www.deepintodev.com/blog/form-handling-in-nextjs)
- [Next.js 14 Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)

### Search & Caching
- [SQLite FTS5 Performance](https://medium.com/@build_break_learn/replaced-elasticsearch-with-sqlite-fts5-100x-faster-5343a4458dd4)
- [Cache Invalidation Strategies (2025)](https://www.designgurus.io/blog/cache-invalidation-strategies)
- [Redis vs SQLite](https://airbyte.com/data-engineering-resources/sqlite-vs-redis)

### Deployment
- [FastAPI Docker Deployment (2025 Edition)](https://blog.greeden.me/en/2025/09/02/the-definitive-guide-to-fastapi-production-deployment-with-dockeryour-one-stop-reference-for-uvicorn-gunicorn-nginx-https-health-checks-and-observability-2025-edition/)
- [FastAPI in Containers](https://fastapi.tiangolo.com/deployment/docker/)

---

## Next Steps

1. **Phase 1 implementation:**
   - Install listed backend + frontend dependencies
   - Set up PyJWT + fastapi-jwt-auth for user sessions
   - Build FeedbackCreate schema (Pydantic) + feedback form (React Hook Form + Zod)
   - Configure SQLAlchemy async for feedback + user reputation tables

2. **Before phase 2:**
   - Profile feedback form UX (load testing)
   - Monitor SQLite query latency
   - If any endpoint >500ms, re-evaluate caching strategy

3. **Phase 2 (if scaling needed):**
   - Add Redis for reputation aggregates
   - Implement event-based cache invalidation
   - Consider PostgreSQL migration (when SQLite write contention matters)
