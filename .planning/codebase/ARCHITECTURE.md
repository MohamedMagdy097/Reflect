# Architecture

**Analysis Date:** 2026-01-18

## Pattern Overview

**Overall:** Client-Server Architecture with REST API

**Key Characteristics:**
- Separate frontend (Next.js) and backend (FastAPI) applications
- Stateless REST API with form-data multipart requests
- Face embedding comparison for biometric authentication
- SQLite database for user storage with embeddings as JSON
- No session/token management - authentication per request

## Layers

**Frontend - Presentation Layer:**
- Purpose: User interface for face capture and authentication forms
- Location: `nextjs-app/`
- Contains: React pages, components, styles
- Depends on: Backend API via HTTP
- Used by: End users via browser

**Frontend - API Client Layer:**
- Purpose: HTTP communication with backend
- Location: `nextjs-app/lib/api.ts`
- Contains: Fetch wrapper functions for auth endpoints
- Depends on: Native fetch, type definitions
- Used by: Page components

**Backend - API Layer:**
- Purpose: REST endpoint routing and request handling
- Location: `face-recognition-server/app/routes/auth.py`
- Contains: FastAPI route handlers for signup/signin
- Depends on: Database, face recognition services
- Used by: Frontend API client

**Backend - Service Layer:**
- Purpose: Face recognition and embedding operations
- Location: `face-recognition-server/app/face_recognition.py`
- Contains: DeepFace model initialization, embedding extraction, similarity comparison
- Depends on: DeepFace library, numpy
- Used by: Auth routes

**Backend - Data Layer:**
- Purpose: Database models and session management
- Location: `face-recognition-server/app/database.py`, `face-recognition-server/app/models.py`
- Contains: SQLAlchemy engine, User model with embedding storage
- Depends on: SQLAlchemy, config settings
- Used by: Auth routes

**Backend - Utility Layer:**
- Purpose: Cross-cutting concerns like image handling
- Location: `face-recognition-server/app/utils/`
- Contains: Image upload/cleanup, custom exceptions
- Depends on: Config settings, OS filesystem
- Used by: Auth routes

## Data Flow

**Signup Flow:**

1. User enters email and captures face photo via webcam in `nextjs-app/pages/signup.tsx`
2. `WebcamCapture` component captures screenshot, converts to File object
3. `api.signup()` sends FormData (email + image) to `POST /api/auth/signup`
4. Backend saves image temporarily via `save_uploaded_image()`
5. `get_embedding()` extracts 512-dimensional ArcFace embedding from face
6. `find_matching_user()` compares embedding against all stored users
7. If unique, creates new User record with email and embedding JSON
8. Returns success response, frontend redirects to dashboard

**Signin Flow:**

1. User enters email and captures face photo in `nextjs-app/pages/signin.tsx`
2. `api.signin()` sends FormData to `POST /api/auth/signin`
3. Backend extracts embedding from uploaded image
4. Compares against all stored embeddings using cosine similarity
5. Verifies matched face belongs to provided email
6. Returns success with similarity score, frontend redirects to dashboard

**State Management:**
- Frontend: React useState hooks for form state, no global state
- Backend: SQLite database persists user data, no in-memory caching
- Session: None - each request is independent, user info passed via URL query params

## Key Abstractions

**User Model:**
- Purpose: Represents authenticated user with face biometrics
- Examples: `face-recognition-server/app/models.py`
- Pattern: SQLAlchemy ORM model with JSON column for embeddings

**Face Embedding:**
- Purpose: 512-dimensional vector representing facial features
- Examples: `face-recognition-server/app/face_recognition.py`
- Pattern: List[float] stored as JSON, compared via cosine similarity

**API Response Schemas:**
- Purpose: Typed response contracts between frontend and backend
- Examples: `face-recognition-server/app/schemas.py`, `nextjs-app/types/index.ts`
- Pattern: Pydantic models (backend) mirrored as TypeScript interfaces (frontend)

**WebcamCapture Component:**
- Purpose: Encapsulates camera access and image capture
- Examples: `nextjs-app/components/WebcamCapture.tsx`
- Pattern: React functional component with ref-based webcam control

## Entry Points

**Backend Entry Point:**
- Location: `face-recognition-server/app/main.py`
- Triggers: `uvicorn app.main:app` command
- Responsibilities: FastAPI app setup, CORS config, router mounting, database/model init on startup

**Frontend Entry Point:**
- Location: `nextjs-app/pages/_app.tsx`
- Triggers: `next dev` or `next start` commands
- Responsibilities: Global CSS import, App wrapper component

**Default Route:**
- Location: `nextjs-app/pages/index.tsx`
- Triggers: Browser navigation to `/`
- Responsibilities: Redirects to `/signup`

## Error Handling

**Strategy:** Exception-based with HTTP status codes

**Patterns:**
- Backend raises `HTTPException` with appropriate status codes (400, 401, 403, 404, 409, 500)
- Backend catches `ValueError` from face recognition and converts to HTTPException
- Frontend catches API errors and displays user-friendly messages based on error content
- Temporary files cleaned up in `finally` blocks

**Error Response Format:**
```python
# Backend
HTTPException(status_code=400, detail="Human-readable message")

# Frontend receives
{ "detail": "Human-readable message" }
```

**HTTP Status Code Usage:**
- 400: Invalid input (bad email, no face detected, multiple faces)
- 401: Face not recognized during signin
- 403: Face matches different email than provided
- 404: Email not registered
- 409: Face already registered with different email
- 500: Unexpected server errors

## Cross-Cutting Concerns

**Logging:** Console print statements (no structured logging framework)

**Validation:**
- Frontend: Email regex validation before submission
- Backend: Pydantic schema validation, face detection enforced by DeepFace

**Authentication:** Face recognition comparison with configurable similarity threshold (0.55 default)

**File Management:**
- Temporary images saved to `uploads/` directory
- Cleanup after each request regardless of success/failure
- Directory created on app startup

**Configuration:**
- Backend: Pydantic Settings with `.env` file support (`face-recognition-server/app/config.py`)
- Frontend: `NEXT_PUBLIC_API_URL` environment variable (`nextjs-app/.env.local`)

---

*Architecture analysis: 2026-01-18*
