# Codebase Structure

**Analysis Date:** 2026-01-18

## Directory Layout

```
Reflect/
├── .claude/                      # Claude code assistant config
├── .planning/                    # GSD planning documents
│   └── codebase/                 # Codebase analysis documents
├── face-recognition-server/      # FastAPI Python backend
│   ├── app/                      # Application source code
│   │   ├── routes/               # API route handlers
│   │   └── utils/                # Utility functions
│   ├── uploads/                  # Temporary image storage (runtime)
│   └── venv/                     # Python virtual environment
├── nextjs-app/                   # Next.js React frontend
│   ├── components/               # Reusable React components
│   ├── lib/                      # Utility functions and API client
│   ├── pages/                    # Next.js pages (file-based routing)
│   ├── public/                   # Static assets (currently empty)
│   ├── styles/                   # CSS stylesheets
│   └── types/                    # TypeScript type definitions
├── CLAUDE.md                     # Project-specific instructions
└── README.md                     # Project documentation
```

## Directory Purposes

**face-recognition-server/app/:**
- Purpose: Main Python application code
- Contains: FastAPI app, models, schemas, services
- Key files:
  - `main.py`: FastAPI app entry point and lifespan setup
  - `config.py`: Settings with env var support
  - `database.py`: SQLAlchemy engine and session factory
  - `models.py`: User ORM model
  - `schemas.py`: Pydantic response schemas
  - `face_recognition.py`: DeepFace integration for embeddings

**face-recognition-server/app/routes/:**
- Purpose: API endpoint definitions
- Contains: FastAPI router modules
- Key files:
  - `auth.py`: Signup, signin, check-email endpoints
  - `__init__.py`: Package marker

**face-recognition-server/app/utils/:**
- Purpose: Shared utility functions
- Contains: Helper modules
- Key files:
  - `image_processing.py`: Upload save/cleanup functions
  - `exceptions.py`: Custom exception classes
  - `__init__.py`: Package marker

**nextjs-app/pages/:**
- Purpose: Application pages (Next.js Pages Router)
- Contains: Page components mapped to URL routes
- Key files:
  - `_app.tsx`: App wrapper with global styles
  - `index.tsx`: Home page (redirects to signup)
  - `signup.tsx`: User registration page
  - `signin.tsx`: Login page
  - `dashboard.tsx`: Post-auth landing page

**nextjs-app/components/:**
- Purpose: Reusable UI components
- Contains: React functional components
- Key files:
  - `WebcamCapture.tsx`: Camera capture component
  - `ErrorAlert.tsx`: Error message display
  - `LoadingSpinner.tsx`: Loading indicator

**nextjs-app/lib/:**
- Purpose: Non-React utilities and API client
- Contains: Helper functions
- Key files:
  - `api.ts`: Backend API wrapper with typed responses

**nextjs-app/types/:**
- Purpose: TypeScript type definitions
- Contains: Interface/type declarations
- Key files:
  - `index.ts`: API response types mirroring backend schemas

**nextjs-app/styles/:**
- Purpose: CSS stylesheets
- Contains: Global and component styles
- Key files:
  - `globals.css`: All application styles

## Key File Locations

**Entry Points:**
- `face-recognition-server/app/main.py`: Backend FastAPI app
- `nextjs-app/pages/_app.tsx`: Frontend Next.js app wrapper
- `nextjs-app/pages/index.tsx`: Default route handler

**Configuration:**
- `face-recognition-server/app/config.py`: Backend settings class
- `face-recognition-server/.env`: Backend environment variables
- `face-recognition-server/requirements.txt`: Python dependencies
- `nextjs-app/package.json`: Node.js dependencies and scripts
- `nextjs-app/tsconfig.json`: TypeScript configuration
- `nextjs-app/next.config.js`: Next.js configuration
- `nextjs-app/.env.local`: Frontend environment variables

**Core Logic:**
- `face-recognition-server/app/face_recognition.py`: Face embedding extraction and matching
- `face-recognition-server/app/routes/auth.py`: Authentication endpoint logic
- `nextjs-app/lib/api.ts`: Frontend API client

**Database:**
- `face-recognition-server/app/database.py`: Connection setup
- `face-recognition-server/app/models.py`: ORM models
- `face-recognition-server/database.db`: SQLite database file (runtime)

**Testing:**
- No test files present

## Naming Conventions

**Files:**
- Python: `snake_case.py` (e.g., `face_recognition.py`, `image_processing.py`)
- TypeScript/TSX: `PascalCase.tsx` for components (e.g., `WebcamCapture.tsx`)
- TypeScript/TSX: `camelCase.ts` for utilities (e.g., `api.ts`)
- Next.js pages: `lowercase.tsx` (e.g., `signup.tsx`, `dashboard.tsx`)

**Directories:**
- Python: `snake_case` (e.g., `face-recognition-server`)
- JavaScript/TypeScript: `lowercase` (e.g., `components`, `lib`, `pages`)

**Functions/Variables:**
- Python: `snake_case` (e.g., `get_embedding`, `find_matching_user`)
- TypeScript: `camelCase` (e.g., `handleCapture`, `validateEmail`)

**Classes/Components:**
- Python: `PascalCase` (e.g., `User`, `Settings`)
- TypeScript: `PascalCase` (e.g., `WebcamCapture`, `ErrorAlert`)

**API Routes:**
- Pattern: `/api/{resource}/{action}` (e.g., `/api/auth/signup`)

## Where to Add New Code

**New API Endpoint:**
- Create route handler in `face-recognition-server/app/routes/auth.py` or new file in `routes/`
- Add router to `face-recognition-server/app/main.py` via `app.include_router()`
- Add frontend API method to `nextjs-app/lib/api.ts`
- Add response types to `face-recognition-server/app/schemas.py` and `nextjs-app/types/index.ts`

**New Page:**
- Create `nextjs-app/pages/{pagename}.tsx`
- Page automatically routes to `/{pagename}`

**New Component:**
- Create `nextjs-app/components/{ComponentName}.tsx`
- Use named export pattern: `export const ComponentName: React.FC`

**New Database Model:**
- Add model class to `face-recognition-server/app/models.py`
- Import and use in routes

**New Utility Function:**
- Backend: Add to appropriate file in `face-recognition-server/app/utils/` or create new file
- Frontend: Add to `nextjs-app/lib/` directory

**Styles:**
- Add CSS rules to `nextjs-app/styles/globals.css`
- Use class-based styling (no CSS modules or CSS-in-JS)

## Special Directories

**face-recognition-server/venv/:**
- Purpose: Python virtual environment with installed packages
- Generated: Yes (via `python -m venv venv`)
- Committed: No (in .gitignore)

**face-recognition-server/uploads/:**
- Purpose: Temporary storage for uploaded face images during processing
- Generated: Yes (created by `main.py` on startup)
- Committed: No (contains temporary files)

**nextjs-app/node_modules/:**
- Purpose: Installed npm packages
- Generated: Yes (via `npm install`)
- Committed: No (in .gitignore)

**nextjs-app/.next/:**
- Purpose: Next.js build output
- Generated: Yes (via `npm run build`)
- Committed: No (in .gitignore)

**face-recognition-server/database.db:**
- Purpose: SQLite database file
- Generated: Yes (on first app run)
- Committed: No (in .gitignore)

---

*Structure analysis: 2026-01-18*
