# Codebase Concerns

**Analysis Date:** 2026-01-18

## Tech Debt

**No Session/Token Management:**
- Issue: Authentication has no session persistence. After successful signin, user data is only passed via URL query parameters to the dashboard. There is no JWT, session cookie, or any token issued.
- Files: `face-recognition-server/app/routes/auth.py`, `nextjs-app/pages/signin.tsx`, `nextjs-app/pages/dashboard.tsx`
- Impact: Users can directly navigate to `/dashboard?email=any@email.com&userId=1` and gain "access" without authentication. Refreshing the page loses authentication state.
- Fix approach: Implement JWT tokens issued on successful signin, store in httpOnly cookies or secure storage, and add middleware to verify tokens on protected routes.

**No API Rate Limiting:**
- Issue: No rate limiting implemented on authentication endpoints. Face recognition is computationally expensive.
- Files: `face-recognition-server/app/main.py`, `face-recognition-server/app/routes/auth.py`
- Impact: Vulnerable to brute force attacks and denial of service. An attacker could repeatedly send images to exhaust server resources.
- Fix approach: Add rate limiting middleware (e.g., `slowapi` for FastAPI) with limits like 5 attempts per email per minute.

**Hardcoded CORS Origin:**
- Issue: CORS only allows `http://localhost:3000`, hardcoded in main.py.
- Files: `face-recognition-server/app/main.py` (lines 42-47)
- Impact: Breaks when deploying to production or using different ports. Requires code change for each environment.
- Fix approach: Move CORS origins to environment variable (e.g., `ALLOWED_ORIGINS=http://localhost:3000,https://production.com`).

**SQLite in Production:**
- Issue: SQLite is the only supported database. Configuration defaults to file-based SQLite.
- Files: `face-recognition-server/app/config.py`, `face-recognition-server/app/database.py`
- Impact: Not suitable for production with concurrent users. No connection pooling. Single-writer limitation.
- Fix approach: Add PostgreSQL support via SQLAlchemy, update DATABASE_URL pattern to support `postgresql://`.

**Custom Exception Not Used:**
- Issue: `FaceRecognitionError` exception class is defined but never used anywhere.
- Files: `face-recognition-server/app/utils/exceptions.py`
- Impact: Dead code. Inconsistent error handling throughout the codebase uses `ValueError` and `HTTPException` directly.
- Fix approach: Either remove the unused exception or refactor error handling to use it consistently.

## Security Considerations

**No Input Validation on File Upload:**
- Risk: Uploaded images are saved with their original extension without validating file type or content.
- Files: `face-recognition-server/app/utils/image_processing.py` (lines 7-19)
- Current mitigation: Only `DeepFace.represent()` processes the file, which may fail on non-images. But malicious files still get written to disk.
- Recommendations:
  - Validate MIME type from file header (magic bytes)
  - Restrict extensions to `.jpg`, `.jpeg`, `.png`
  - Validate `Content-Type` header
  - Add MAX_UPLOAD_SIZE check before saving

**Sensitive Data in URL Query Parameters:**
- Risk: User email and ID are passed in URL query params to dashboard after login.
- Files: `nextjs-app/pages/signup.tsx` (lines 46-53), `nextjs-app/pages/signin.tsx` (lines 45-51)
- Current mitigation: None
- Recommendations: Use session storage, cookies, or state management instead of URL params. URLs get logged in browser history and server logs.

**No HTTPS Enforcement:**
- Risk: No TLS/HTTPS configuration present. Face biometric data transmitted in cleartext.
- Files: All API calls in `nextjs-app/lib/api.ts`
- Current mitigation: Development only - uses localhost
- Recommendations: Add SSL certificate configuration, enforce HTTPS in production, use `Secure` flag on any future cookies.

**Face Embeddings Stored in Plain JSON:**
- Risk: Face biometric embeddings (512-dimensional vectors) stored as plain JSON in SQLite without encryption.
- Files: `face-recognition-server/app/models.py` (line 10)
- Current mitigation: None
- Recommendations: Encrypt embeddings at rest using application-level encryption or database encryption. Consider hashing approach similar to passwords.

**Information Leakage in Error Messages:**
- Risk: Error messages reveal registered email addresses to attackers.
- Files: `face-recognition-server/app/routes/auth.py` (lines 55-60, 142-146)
- Current mitigation: None. Errors like "User is already signed up with email: attacker@target.com" expose data.
- Recommendations: Use generic error messages in production. Log detailed errors server-side only.

**No CSRF Protection:**
- Risk: Form submissions vulnerable to cross-site request forgery.
- Files: `nextjs-app/pages/signup.tsx`, `nextjs-app/pages/signin.tsx`
- Current mitigation: None
- Recommendations: Implement CSRF tokens in forms, validate `Origin`/`Referer` headers on backend.

## Performance Bottlenecks

**Linear User Scan for Face Matching:**
- Problem: `find_matching_user()` loads ALL users from database and iterates through each one for comparison.
- Files: `face-recognition-server/app/face_recognition.py` (lines 64-85), `face-recognition-server/app/routes/auth.py` (lines 50-51, 128-129)
- Cause: No indexing structure for face embeddings. O(n) complexity where n is total users.
- Improvement path:
  - Implement approximate nearest neighbor (ANN) search using FAISS or Annoy
  - Add embedding index that persists in memory
  - Consider batched comparison with numpy vectorization for moderate user counts

**Model Initialization on Every Request:**
- Problem: While `init_model()` pre-loads ArcFace at startup, `DeepFace.represent()` may still have overhead.
- Files: `face-recognition-server/app/face_recognition.py`
- Cause: DeepFace may reload detector model (retinaface) per request.
- Improvement path: Cache detector model instance, use model singleton pattern.

**Full Image Saved to Disk:**
- Problem: Every authentication attempt writes image to disk, processes it, then deletes it.
- Files: `face-recognition-server/app/utils/image_processing.py`, `face-recognition-server/app/routes/auth.py`
- Cause: DeepFace API requires file path, not bytes.
- Improvement path: Consider in-memory processing if DeepFace supports numpy arrays, or use tmpfs/RAM disk.

## Fragile Areas

**Dashboard Page Session Handling:**
- Files: `nextjs-app/pages/dashboard.tsx`
- Why fragile: Completely depends on URL query parameters. Any navigation away loses state. Direct URL access bypasses auth.
- Safe modification: Must implement proper session management before adding any protected functionality.
- Test coverage: None

**Similarity Threshold Configuration:**
- Files: `face-recognition-server/app/config.py` (line 8), `face-recognition-server/.env`
- Why fragile: Threshold of 0.55 affects security/usability tradeoff. Too low = false accepts (security breach), too high = false rejects (poor UX).
- Safe modification: Requires testing with diverse face dataset. Consider making it user-configurable or adding confidence tiers.
- Test coverage: None

**Temp File Cleanup:**
- Files: `face-recognition-server/app/utils/image_processing.py` (lines 22-28)
- Why fragile: `cleanup_temp_image()` silently catches exceptions and only prints warning. If cleanup fails, temp files accumulate.
- Safe modification: Add monitoring for uploads directory size, implement scheduled cleanup job.
- Test coverage: None

## Test Coverage Gaps

**No Tests Exist:**
- What's not tested: Entire codebase has zero test files
- Files: All files in `face-recognition-server/app/` and `nextjs-app/`
- Risk: Any change could break functionality without detection. Face recognition edge cases untested.
- Priority: High

**Critical Untested Scenarios:**
- Face detection with poor lighting
- Multiple face detection edge cases
- Embedding comparison accuracy
- Database transaction rollbacks
- File upload size limits
- Concurrent authentication attempts
- Invalid image formats

## Missing Critical Features

**No Password/Backup Auth:**
- Problem: Face-only authentication with no fallback method.
- Blocks: Users cannot authenticate if camera fails, lighting changes significantly, or physical appearance changes (aging, injury, glasses).

**No Account Recovery:**
- Problem: No way to recover account if face no longer matches.
- Blocks: Users permanently locked out if face recognition fails consistently.

**No Audit Logging:**
- Problem: No logging of authentication attempts (successful or failed).
- Blocks: Cannot detect attack patterns, investigate security incidents, or meet compliance requirements.

**No User Management:**
- Problem: No ability to delete accounts, update email, or re-enroll face.
- Blocks: GDPR compliance, user self-service.

## Dependencies at Risk

**deepface==0.0.88:**
- Risk: Bundles multiple ML frameworks (TensorFlow, Keras). Heavy dependency chain. Version pinning may cause conflicts.
- Impact: Installation issues, potential CVEs in transitive dependencies
- Migration plan: Monitor for updates, consider lighter alternatives like `face_recognition` library.

**SQLite for Face Embeddings:**
- Risk: JSON column type in SQLite has no native vector operations.
- Impact: Cannot use database-level similarity search, limits scalability
- Migration plan: Consider pgvector for PostgreSQL or dedicated vector database (Pinecone, Milvus).

---

*Concerns audit: 2026-01-18*
