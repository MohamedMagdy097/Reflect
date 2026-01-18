# Technology Stack

**Analysis Date:** 2026-01-18

## Languages

**Primary:**
- Python 3.x - Backend face recognition server (`face-recognition-server/`)
- TypeScript 5.3.3 - Frontend Next.js application (`nextjs-app/`)

**Secondary:**
- JavaScript - Next.js configuration files (`nextjs-app/next.config.js`)
- CSS - Global styles (`nextjs-app/styles/globals.css`)

## Runtime

**Backend:**
- Python with venv virtual environment
- Activation: `face-recognition-server/venv/Scripts/activate` (Windows)

**Frontend:**
- Node.js (version not pinned, no .nvmrc)
- npm as package manager
- Lockfile: `nextjs-app/package-lock.json` (present)

## Frameworks

**Backend Core:**
- FastAPI 0.109.0 - Async Python web framework
  - Config: `face-recognition-server/app/main.py`
  - Uses lifespan context manager for startup/shutdown
- Uvicorn 0.27.0 - ASGI server with standard extras

**Frontend Core:**
- Next.js 14.1.0 - React framework (Pages Router)
  - Config: `nextjs-app/next.config.js`
  - TypeScript strict mode enabled
- React 18.2.0 - UI library
- React DOM 18.2.0 - DOM bindings

**Data Validation:**
- Pydantic 2.5.3 - Data validation for Python
- Pydantic Settings 2.1.0 - Environment configuration

**Database:**
- SQLAlchemy 2.0.25 - Python ORM
  - Uses declarative base pattern
  - Session management via dependency injection

## Key Dependencies

**Face Recognition (Critical):**
- DeepFace 0.0.88 - Face recognition framework
  - Uses ArcFace model (512-dimensional embeddings)
- RetinaFace 0.0.17 - Face detection backend
- TF-Keras 2.16.0 - TensorFlow/Keras for ML models
- OpenCV-Python 4.9.0.80 - Image processing
- Pillow 10.2.0 - Image manipulation

**Frontend:**
- react-webcam 7.2.0 - Webcam capture component

**Infrastructure:**
- python-multipart 0.0.6 - File upload handling for FastAPI
- python-dotenv 1.0.0 - Environment variable loading

**TypeScript Types (Dev):**
- @types/node 20.11.5
- @types/react 18.2.48
- @types/react-dom 18.2.18

## Configuration

**Backend Environment:**
- File: `face-recognition-server/.env`
- Variables:
  - `DATABASE_URL` - SQLite connection string (default: `sqlite:///./database.db`)
  - `UPLOAD_DIR` - Temporary image storage (default: `uploads`)
  - `SIMILARITY_THRESHOLD` - Face match threshold (default: `0.55`)
- Loaded via: pydantic-settings (`face-recognition-server/app/config.py`)

**Frontend Environment:**
- File: `nextjs-app/.env.local`
- Variables:
  - `NEXT_PUBLIC_API_URL` - Backend API URL (default: `http://localhost:8000`)

**TypeScript:**
- Config: `nextjs-app/tsconfig.json`
- Target: ES5
- Module: ESNext
- Strict mode: enabled
- Path alias: `@/*` maps to `./*`

**Build:**
- Next.js: `nextjs-app/next.config.js`
  - React strict mode enabled
  - No custom webpack configuration

## Platform Requirements

**Development:**
- Windows OS (venv activation uses `Scripts/activate`)
- Python 3.x with pip
- Node.js with npm
- Camera access for webcam capture

**Backend Server:**
- Default port: 8000
- Run: `uvicorn app.main:app --reload` (from `face-recognition-server/`)

**Frontend Dev Server:**
- Default port: 3000
- Run: `npm run dev` (from `nextjs-app/`)

**Production:**
- Backend: Uvicorn ASGI server
- Frontend: Next.js build + static export or Node.js server
- Database: SQLite (single file, filesystem storage)

## Monorepo Structure

```
Reflect/
├── face-recognition-server/   # Python FastAPI backend
│   ├── app/                   # Application code
│   ├── venv/                  # Python virtual environment
│   ├── .env                   # Backend environment config
│   └── requirements.txt       # Python dependencies
└── nextjs-app/                # TypeScript Next.js frontend
    ├── pages/                 # Next.js pages (Pages Router)
    ├── components/            # React components
    ├── lib/                   # API client
    ├── types/                 # TypeScript types
    ├── styles/                # CSS styles
    ├── .env.local             # Frontend environment config
    └── package.json           # Node dependencies
```

---

*Stack analysis: 2026-01-18*
