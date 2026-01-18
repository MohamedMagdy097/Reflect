# Testing Patterns

**Analysis Date:** 2026-01-18

## Test Framework

**Backend (Python):**
- Runner: Not configured
- No test files present in `face-recognition-server/` source directory
- No pytest, unittest, or test configuration detected
- No `tests/` directory exists

**Frontend (TypeScript/Next.js):**
- Runner: Not configured
- No test files present in `nextjs-app/` source directory
- No Jest, Vitest, or testing-library configuration detected
- `next lint` script available but no test script in package.json

**Run Commands:**
```bash
# Backend - Not available (no test framework)
# Would typically be: pytest

# Frontend - Not available (no test framework)
# Would typically be: npm test
```

## Test File Organization

**Location:**
- Not applicable - no tests exist

**Recommended Pattern for Future Tests:**

**Backend:**
```
face-recognition-server/
├── app/
│   └── ...
└── tests/
    ├── __init__.py
    ├── conftest.py           # Pytest fixtures
    ├── test_auth.py          # Route tests
    ├── test_face_recognition.py
    └── test_image_processing.py
```

**Frontend:**
```
nextjs-app/
├── __tests__/
│   ├── pages/
│   │   ├── signup.test.tsx
│   │   └── signin.test.tsx
│   └── components/
│       └── WebcamCapture.test.tsx
└── lib/
    └── api.test.ts
```

**Naming (Recommended):**
- Python: `test_*.py` prefix
- TypeScript: `*.test.tsx` or `*.test.ts` suffix

## Test Structure

**Recommended Python Pattern (pytest):**
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db

client = TestClient(app)

class TestSignup:
    """Tests for signup endpoint"""

    def test_signup_success(self, db_session, mock_face_image):
        """Test successful user signup with valid email and face"""
        response = client.post(
            "/api/auth/signup",
            data={"email": "test@example.com"},
            files={"image": mock_face_image}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_signup_duplicate_email(self, existing_user, mock_face_image):
        """Test signup fails for duplicate email"""
        response = client.post(
            "/api/auth/signup",
            data={"email": existing_user.email},
            files={"image": mock_face_image}
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
```

**Recommended TypeScript Pattern (Jest + React Testing Library):**
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { useRouter } from 'next/router';
import SignupPage from '@/pages/signup';
import { api } from '@/lib/api';

jest.mock('next/router', () => ({
  useRouter: jest.fn()
}));

jest.mock('@/lib/api');

describe('SignupPage', () => {
  const mockPush = jest.fn();

  beforeEach(() => {
    (useRouter as jest.Mock).mockReturnValue({ push: mockPush });
    jest.clearAllMocks();
  });

  it('displays error when email is invalid', async () => {
    render(<SignupPage />);

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'invalid-email' }
    });
    fireEvent.click(screen.getByRole('button', { name: /create account/i }));

    expect(screen.getByText(/valid email address/i)).toBeInTheDocument();
  });
});
```

## Mocking

**Framework (Recommended):**
- Python: pytest-mock, unittest.mock
- TypeScript: Jest mocks

**Python Mocking Pattern (Recommended):**
```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_deepface():
    """Mock DeepFace model responses"""
    with patch('app.face_recognition.DeepFace') as mock:
        mock.represent.return_value = [{
            "embedding": [0.1] * 512  # 512-dim ArcFace embedding
        }]
        yield mock

def test_get_embedding(mock_deepface):
    from app.face_recognition import get_embedding
    result = get_embedding("test.jpg")
    assert len(result) == 512
```

**TypeScript Mocking Pattern (Recommended):**
```typescript
// Mock API module
jest.mock('@/lib/api', () => ({
  api: {
    signup: jest.fn(),
    signin: jest.fn(),
    checkEmail: jest.fn()
  }
}));

// Mock webcam component
jest.mock('react-webcam', () => {
  return function MockWebcam({ onUserMedia }: any) {
    onUserMedia?.();
    return <div data-testid="mock-webcam" />;
  };
});
```

**What to Mock:**
- External APIs (DeepFace, fetch calls)
- Database sessions (use test database or mock)
- File system operations
- Browser APIs (webcam, file blobs)
- Next.js router

**What NOT to Mock:**
- Pydantic validation
- React component rendering
- Form validation logic
- Pure utility functions

## Fixtures and Factories

**Python Test Data (Recommended):**
```python
@pytest.fixture
def db_session():
    """Create test database session"""
    from app.database import SessionLocal, Base, engine
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def mock_face_image():
    """Create a mock face image file"""
    from io import BytesIO
    # Create minimal JPEG bytes
    image_bytes = BytesIO(b'\xff\xd8\xff\xe0...')
    image_bytes.name = 'face.jpg'
    return ('face.jpg', image_bytes, 'image/jpeg')

@pytest.fixture
def sample_embedding():
    """Return a valid 512-dimensional embedding"""
    return [0.1] * 512
```

**TypeScript Test Data (Recommended):**
```typescript
// __tests__/fixtures/responses.ts
export const mockSignupResponse = {
  success: true,
  message: 'Account created successfully',
  user_id: 1,
  email: 'test@example.com'
};

export const mockSigninResponse = {
  success: true,
  message: 'Authentication successful',
  user_id: 1,
  email: 'test@example.com',
  similarity_score: 0.87
};

// Factory function
export const createMockFile = (name = 'face-capture.jpg') => {
  return new File(['mock-image-data'], name, { type: 'image/jpeg' });
};
```

**Location:**
- Python: `tests/conftest.py` for pytest fixtures
- TypeScript: `__tests__/fixtures/` or `__mocks__/` directories

## Coverage

**Requirements:** None enforced

**Recommended Setup (Python):**
```bash
# Install pytest-cov
pip install pytest-cov

# Run with coverage
pytest --cov=app --cov-report=html tests/

# Add to requirements-dev.txt
pytest>=7.0.0
pytest-cov>=4.0.0
httpx>=0.24.0  # For async test client
```

**Recommended Setup (TypeScript):**
```json
// package.json scripts
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

**Recommended Coverage Targets:**
- Minimum: 70%
- Routes/Pages: 80%
- Utility functions: 90%

## Test Types

**Unit Tests (Not Present):**
- Scope: Individual functions and components
- Files to test:
  - `face-recognition-server/app/face_recognition.py` - `get_embedding()`, `cosine_similarity()`, `find_matching_user()`
  - `face-recognition-server/app/utils/image_processing.py` - `save_uploaded_image()`, `cleanup_temp_image()`
  - `nextjs-app/lib/api.ts` - API client methods
  - `nextjs-app/components/*.tsx` - Component rendering

**Integration Tests (Not Present):**
- Scope: API endpoint testing with database
- Files to test:
  - `face-recognition-server/app/routes/auth.py` - Full signup/signin flow
  - Database operations through routes

**E2E Tests (Not Present):**
- Framework recommendation: Playwright or Cypress
- Scope: Full user flows (signup, signin, dashboard navigation)

## Common Patterns

**Async Testing (Python - Recommended):**
```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/auth/signup", ...)
        assert response.status_code == 200
```

**Async Testing (TypeScript - Recommended):**
```typescript
it('submits form successfully', async () => {
  (api.signup as jest.Mock).mockResolvedValue(mockSignupResponse);

  render(<SignupPage />);

  // Fill form and submit
  fireEvent.click(screen.getByRole('button', { name: /create account/i }));

  await waitFor(() => {
    expect(mockPush).toHaveBeenCalledWith(expect.objectContaining({
      pathname: '/dashboard'
    }));
  });
});
```

**Error Testing (Python - Recommended):**
```python
def test_signup_no_face_detected(db_session, mock_deepface_no_face):
    """Test error when no face is detected in image"""
    response = client.post(
        "/api/auth/signup",
        data={"email": "test@example.com"},
        files={"image": ("test.jpg", b"invalid-image", "image/jpeg")}
    )
    assert response.status_code == 400
    assert "No face detected" in response.json()["detail"]
```

**Error Testing (TypeScript - Recommended):**
```typescript
it('displays error when signup fails', async () => {
  (api.signup as jest.Mock).mockRejectedValue(
    new Error('Email already registered')
  );

  render(<SignupPage />);
  // Trigger form submit

  await waitFor(() => {
    expect(screen.getByText(/already registered/i)).toBeInTheDocument();
  });
});
```

## Testing Gaps and Recommendations

**Critical Missing Tests:**
1. No unit tests for `face_recognition.py` core functions
2. No API endpoint tests for auth routes
3. No React component tests
4. No form validation tests

**Recommended Test Setup (Python):**
```bash
# Create requirements-dev.txt
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-cov>=4.0.0
httpx>=0.24.0

# Create pytest.ini
[pytest]
testpaths = tests
asyncio_mode = auto
```

**Recommended Test Setup (TypeScript):**
```bash
npm install -D jest @types/jest ts-jest @testing-library/react @testing-library/jest-dom jest-environment-jsdom
```

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1'
  },
  testPathIgnorePatterns: ['<rootDir>/node_modules/']
};
```

---

*Testing analysis: 2026-01-18*
