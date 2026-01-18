# Coding Conventions

**Analysis Date:** 2026-01-18

## Naming Patterns

**Files (Python Backend):**
- snake_case for all module names: `face_recognition.py`, `image_processing.py`
- Route files named by domain: `auth.py`
- `__init__.py` for package markers

**Files (TypeScript Frontend):**
- PascalCase for React components: `WebcamCapture.tsx`, `ErrorAlert.tsx`
- camelCase for utilities and lib: `api.ts`
- lowercase for pages (Next.js convention): `signup.tsx`, `signin.tsx`, `dashboard.tsx`
- lowercase for type files: `index.ts` in types directory

**Functions (Python):**
- snake_case for all functions: `get_embedding()`, `find_matching_user()`, `save_uploaded_image()`
- async functions prefixed when they are coroutines: `async def signup()`

**Functions (TypeScript):**
- camelCase for functions and handlers: `handleCapture`, `handleSubmit`, `validateEmail`
- Prefix event handlers with `handle`: `handleCapture`, `handleUserMedia`

**Variables (Python):**
- snake_case for all variables: `temp_image_path`, `new_embedding`, `user_data`
- UPPER_SNAKE_CASE for constants in config: `DATABASE_URL`, `UPLOAD_DIR`, `MAX_UPLOAD_SIZE`

**Variables (TypeScript):**
- camelCase for local variables and state: `capturedImage`, `isLoading`, `hasPermission`
- UPPER_SNAKE_CASE for constants: `API_URL`

**Types (TypeScript):**
- PascalCase for interfaces and types: `SignupResponse`, `SigninResponse`, `UserData`
- Props interfaces suffixed with `Props`: `WebcamCaptureProps`, `ErrorAlertProps`

**Classes (Python):**
- PascalCase for class names: `Settings`, `User`, `SignupResponse`
- SQLAlchemy models are singular nouns: `User` (not `Users`)

## Code Style

**Formatting (Python):**
- No explicit formatter configuration detected
- Use standard Python formatting (PEP 8 style)
- 4-space indentation
- Double quotes for strings observed throughout

**Formatting (TypeScript):**
- No explicit Prettier/ESLint configuration (relies on defaults)
- 2-space indentation
- Single quotes for strings
- Semicolons used
- No trailing commas observed

**Linting:**
- No ESLint configuration file in frontend
- `next lint` script available but no custom rules
- No Python linting configuration (no ruff, black, or flake8 configs)

## Import Organization

**Python Import Order:**
1. Standard library imports (`os`, `uuid`)
2. Third-party imports (`fastapi`, `sqlalchemy`, `pydantic`, `deepface`, `numpy`)
3. Local application imports (`from app.config import settings`)

**TypeScript Import Order:**
1. React and hooks (`import { useState } from 'react'`)
2. Next.js imports (`import { useRouter } from 'next/router'`)
3. Third-party packages (`import Webcam from 'react-webcam'`)
4. Local components (`import { WebcamCapture } from '../components/WebcamCapture'`)
5. Local utilities and types (`import { api } from '../lib/api'`)

**Path Aliases (TypeScript):**
- `@/*` maps to root directory (configured in `tsconfig.json`)
- Currently not used in codebase - relative imports used instead

## Error Handling

**Python (FastAPI) Patterns:**
```python
# Use HTTPException for API errors
raise HTTPException(status_code=400, detail="Email already registered")

# Re-raise HTTPException to preserve original error
except HTTPException:
    raise

# Catch all other exceptions with 500 status
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")

# Use ValueError for domain-specific validation
raise ValueError("No face detected")
```

**TypeScript Patterns:**
```typescript
// Custom ApiError class for HTTP errors
class ApiError extends Error {
  constructor(public statusCode: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

// Error message string matching for user-friendly messages
if (err.message.includes('already signed up')) {
  setError(err.message);
} else if (err.message.includes('No face detected')) {
  setError('No face detected. Please ensure your face is clearly visible and try again.');
}
```

## Logging

**Framework:** console (both Python and TypeScript)

**Python Patterns:**
```python
# Use print statements with emoji prefixes for visual logging
print("Starting Face Recognition Server...")
print("Database initialized")
print(f"Warning: Failed to cleanup temp file {file_path}: {e}")
```

**TypeScript Patterns:**
- No explicit logging in frontend code
- Errors displayed to users via state and UI components

## Comments

**When to Comment (Python):**
- Docstrings for public functions with multi-line descriptions
- Inline comments for non-obvious logic steps (numbered flow)
- Type hints used consistently for function signatures

**Docstring Pattern:**
```python
def find_matching_user(
    new_embedding: List[float],
    all_users: List[Tuple[int, str, List[float]]],
    threshold: float = 0.55
) -> Optional[Tuple[int, str, float]]:
    """
    Check if new embedding matches any existing user.

    Args:
        new_embedding: Embedding to check
        all_users: List of (user_id, email, embedding) tuples
        threshold: Similarity threshold (0.55 for ArcFace)

    Returns:
        (user_id, email, similarity) if match found, None otherwise
    """
```

**Flow Documentation Pattern:**
```python
"""
Signup flow:
1. Validate email format
2. Check if email already exists
3. Extract face embedding from image
4. Check if face already exists (compare against ALL users)
5. If face unique, create account
"""
```

**TypeScript/JSDoc:**
- Minimal inline comments
- No JSDoc annotations used
- Self-documenting code via descriptive variable/function names

## Function Design

**Size:** Functions are small and focused (typically under 50 lines)

**Parameters (Python):**
- Use type hints for all parameters
- Use `= Form(...)` for required form fields in FastAPI
- Use `Depends()` for dependency injection

**Parameters (TypeScript):**
- Use TypeScript interfaces for props
- Destructure props in function signature
- Default values specified in destructuring: `disabled = false`

**Return Values (Python):**
- Return Pydantic models for API responses
- Use Optional[] for functions that may return None
- Use Tuple[] for multiple return values

**Return Values (TypeScript):**
- Return JSX.Element for React components
- Async functions return typed Promises

## Module Design

**Exports (Python):**
- No explicit `__all__` declarations
- Import directly from module files

**Exports (TypeScript):**
- Named exports for components: `export const WebcamCapture`
- Named exports for api object: `export const api`
- Named exports for types: `export interface SignupResponse`
- Re-export from api.ts: `export { ApiError }`

**Barrel Files:**
- `types/index.ts` acts as barrel file for types
- Components not re-exported through barrel (imported directly)

## React Component Patterns

**Functional Components:**
- Use arrow functions with React.FC type annotation: `export const WebcamCapture: React.FC<WebcamCaptureProps>`
- Default exports for page components: `export default function SignupPage()`

**State Management:**
- Use `useState` for local component state
- Use `useEffect` for side effects and routing
- Use `useCallback` for memoized callbacks (in webcam capture)
- Use `useRef` for DOM references

**Props Pattern:**
```typescript
interface WebcamCaptureProps {
  onCapture: (file: File) => void;
  disabled?: boolean;
}

export const WebcamCapture: React.FC<WebcamCaptureProps> = ({
  onCapture,
  disabled = false
}) => {
```

## API Design Patterns

**FastAPI Route Pattern:**
```python
@router.post("/signup", response_model=schemas.SignupResponse)
async def signup(
    email: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
```

**Response Consistency:**
- Success responses include: `success: bool`, `message: str`, entity-specific fields
- Error responses use FastAPI's `HTTPException` with `detail` field

**Status Codes Used:**
- 200: Success
- 400: Bad Request (validation errors)
- 401: Unauthorized (face not recognized)
- 403: Forbidden (face matches different email)
- 404: Not Found (email not registered)
- 409: Conflict (user already exists)
- 500: Internal Server Error

---

*Convention analysis: 2026-01-18*
