# External Integrations

**Analysis Date:** 2026-01-18

## APIs & External Services

**Internal REST API:**
- Backend exposes REST API at `/api/auth/*`
- Frontend consumes via fetch in `nextjs-app/lib/api.ts`
- CORS configured for `http://localhost:3000`

**ML Model Downloads (DeepFace):**
- ArcFace model weights downloaded on first run
  - Source: DeepFace package default sources
  - Stored: User's home directory (DeepFace default cache)
- RetinaFace detector weights similarly downloaded
- No API key required - pre-trained models

## Data Storage

**Database:**
- SQLite (file-based)
  - Connection: `DATABASE_URL` env var
  - Default: `sqlite:///./database.db`
  - Location: `face-recognition-server/database.db`
  - Client: SQLAlchemy ORM
  - Config: `face-recognition-server/app/database.py`

**Tables:**
- `users` table (`face-recognition-server/app/models.py`)
  - `id` - Integer primary key
  - `email` - Unique string, indexed
  - `embedding` - JSON array (512 floats for ArcFace)
  - `created_at` - Timestamp
  - `updated_at` - Timestamp

**File Storage:**
- Local filesystem only
  - Temporary images: `face-recognition-server/uploads/`
  - Images deleted after embedding extraction
  - No persistent image storage

**Caching:**
- None configured
- DeepFace models cached in memory after initialization

## Authentication & Identity

**Auth Provider:**
- Custom face recognition authentication (no third-party auth)
  - Implementation: `face-recognition-server/app/face_recognition.py`

**Auth Flow:**
1. User captures face via webcam (`nextjs-app/components/WebcamCapture.tsx`)
2. Image sent as FormData to backend
3. Backend extracts 512-dim ArcFace embedding
4. Cosine similarity compared against stored embeddings
5. Threshold: 0.55 (configurable via `SIMILARITY_THRESHOLD`)

**Endpoints:**
- `POST /api/auth/signup` - Register new user with face
- `POST /api/auth/signin` - Authenticate existing user
- `GET /api/auth/check-email` - Check if email exists

**No Session Management:**
- No JWT tokens
- No session cookies
- Stateless authentication per request

## Monitoring & Observability

**Error Tracking:**
- None configured (no Sentry, Datadog, etc.)

**Logs:**
- Console output only
- FastAPI prints startup messages to stdout
- No structured logging framework

## CI/CD & Deployment

**Hosting:**
- Not configured (local development only)

**CI Pipeline:**
- None configured (no GitHub Actions, etc.)

**Docker:**
- Not configured (no Dockerfile)

## Environment Configuration

**Required Environment Variables:**

Backend (`face-recognition-server/.env`):
```
DATABASE_URL=sqlite:///./database.db
UPLOAD_DIR=uploads
SIMILARITY_THRESHOLD=0.55
```

Frontend (`nextjs-app/.env.local`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Secrets Location:**
- No secrets required
- No API keys needed
- All configuration in `.env` files (not committed to git)

## Webhooks & Callbacks

**Incoming:**
- None

**Outgoing:**
- None

## Frontend-Backend Communication

**API Client:**
- Location: `nextjs-app/lib/api.ts`
- Pattern: Fetch-based with FormData for image upload

**Request Format:**
```typescript
// Signup/Signin requests
const formData = new FormData();
formData.append('email', email);
formData.append('image', file);

fetch(`${API_URL}/api/auth/signup`, {
  method: 'POST',
  body: formData,
});
```

**Response Types:**
- Defined in `nextjs-app/types/index.ts`
- Mirrored in `face-recognition-server/app/schemas.py`

```typescript
interface SignupResponse {
  success: boolean;
  message: string;
  user_id: number;
  email: string;
}

interface SigninResponse {
  success: boolean;
  message: string;
  user_id: number;
  email: string;
  similarity_score?: number;
}
```

**Error Handling:**
- Backend: HTTPException with `detail` field
- Frontend: Custom `ApiError` class wrapping status code and message

## Browser APIs

**Webcam Access:**
- Uses MediaDevices API via react-webcam
- Component: `nextjs-app/components/WebcamCapture.tsx`
- Constraints: 640x480, front-facing camera ("user")
- Output: JPEG screenshot as File object

---

*Integration audit: 2026-01-18*
