# Architecture: Feedback/Reputation System

**Project:** Reflect (Post-Date Feedback Platform)
**Domain:** Consent-based feedback and reputation aggregation for user profiles
**Researched:** 2026-01-19
**Context:** Extending existing Face ID auth system with feedback, profiles, search, and public reputation display

## Executive Summary

Reflect's feedback/reputation system requires a carefully layered architecture separating:
1. **Private domain** (consents, raw feedback) - restricted access, owner-only visibility
2. **Aggregation layer** (stats, patterns, cached computations) - pre-calculated, refreshed asynchronously
3. **Public surface** (profiles, reputation display) - carefully filtered, permission-gated

The key architectural challenge is enabling "mutual consent workflows" (both parties must agree before feedback can be submitted) while maintaining queryable reputation as a public good. This requires a consent graph model where feedback flows only exist between consented pairs.

## Recommended Architecture

### System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        REFLECT SYSTEM                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Next.js Frontend (Port 3000)                                   │
│  ├── Public profiles page (anon access OK)                     │
│  ├── User discovery/search                                     │
│  ├── Consent request flow                                      │
│  └── Feedback form (consent-gated)                             │
│                                                                  │
│  ↕ HTTP REST API                                               │
│                                                                  │
│  FastAPI Backend (Port 8000)                                   │
│  ├── Auth endpoints (Face ID signin/signup) ────────┐          │
│  ├── Profile endpoints (read/write) ───────────────┤          │
│  ├── Consent endpoints (request/accept/revoke) ────┤          │
│  ├── Feedback endpoints (submit/read) ─────────────┼──────┐   │
│  ├── Stats/aggregation endpoints (read-only) ──────┤      │   │
│  └── Search endpoints (public discovery) ──────────┤      │   │
│                                                     │      │   │
│  ORM Layer: SQLAlchemy 2.0                         │      │   │
│  ├── Query builder ────────────────────────────────┼────┐ │   │
│  └── Permission filters (enforce consent) ────────┤    │ │   │
│                                                     │    │ │   │
│  SQLite Database (Port N/A)                        │    │ │   │
│  ├── users ────────────────────────────────────────┘    │ │   │
│  ├── profiles                                          │ │   │
│  ├── consents (multi-way: user_a, user_b, status)     │ │   │
│  ├── feedback (gated by consent lookup)                │ │   │
│  ├── feedback_stats (denormalized, cached)             │ │   │
│  └── uploads/temp (face images - cleaned up)           │ │   │
│                                                         │ │   │
│  Cache Layer (optional, for Phase 2+ scale)           │ │   │
│  ├── Profile stats (TTL: 1 hour) ──────────────────────┘ │   │
│  ├── Reputation summaries (TTL: 4 hours) ─────────────────┘   │
│  └── Search indexes                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Boundaries

### 1. Authentication & Identity (Existing)

**Responsibility:** Face ID registration, signin, user identity verification

**Communicates with:**
- Face Recognition service (DeepFace/ArcFace)
- User table (read/write embeddings)
- Upstream: Next.js frontend (webcam frames)
- Downstream: Profile, Consent, Feedback components (receives user_id)

**Key constraint:** One face = one account (prevents duplicate accounts)

---

### 2. Profiles Component

**Responsibility:**
- User profile data (bio, location, public display name, profile photo)
- Visibility permissions (public/private)
- Read by: anyone during discovery; self for editing; consented users for full view

**Tables involved:**
```
users (existing)
├── id (PK)
├── email (UNIQUE, indexed)
├── embedding (JSON, face data)
├── created_at, updated_at

profiles (NEW)
├── id (PK)
├── user_id (FK → users.id, UNIQUE)
├── display_name
├── bio
├── profile_photo_url (or path to uploaded image)
├── location
├── visibility (enum: PUBLIC, PRIVATE)
├── created_at, updated_at
```

**API boundaries:**
- `GET /api/profiles/{user_id}` → returns public data (or full if requestor has consent)
- `PATCH /api/profiles/{user_id}` → only self, requires authentication
- Visibility logic: if profile.visibility=PRIVATE, only return to owner or consented users

**Communicates with:**
- Auth (requires user_id from session)
- Consent (checks if requestor has consent to see full profile)
- Search (indexed via denormalized display_name)

---

### 3. Consent Management Component

**Responsibility:**
- Record bilateral consent relationships ("A allows B to send feedback")
- Enforce mutual opt-in before feedback submission
- Support consent revocation

**Data model (critical):**

```
consents (NEW, multi-way relationship)
├── id (PK)
├── initiator_user_id (FK → users.id, who requested)
├── recipient_user_id (FK → users.id, who is being asked)
├── status (enum: PENDING, ACCEPTED, REVOKED)
├── initiated_at
├── accepted_at (nullable, set when status→ACCEPTED)
├── revoked_at (nullable, set when status→REVOKED)
├── indexes:
│   ├── (initiator_user_id, recipient_user_id) UNIQUE
│   └── (recipient_user_id, status) for "pending requests"
```

**Key design decision:** Unidirectional consent model

- A sends consent request to B
- If B accepts: A can now submit feedback about B (one-way)
- Does NOT grant B permission to submit feedback about A
- B must separately request/obtain consent from A
- This is intentional: asymmetric feedback relationships (reviewer ≠ reviewee)

**Alternative considered (two-way):**
- Would allow both A→B and B→A feedback after one acceptance
- Simpler schema but less privacy control
- Recommend one-way for initial design; can add option later

**API boundaries:**
- `POST /api/consents/{target_user_id}/request` → create consent with status=PENDING
- `GET /api/consents/pending` → list pending requests (recipient's view)
- `POST /api/consents/{consent_id}/accept` → update status=ACCEPTED
- `POST /api/consents/{consent_id}/revoke` → update status=REVOKED
- `GET /api/consents/check?source={me}&target={user}` → check if I can send feedback (status=ACCEPTED)

**Communicates with:**
- Auth (requires user_id, target_user_id validation)
- Feedback (before submit, must validate consent exists with status=ACCEPTED)
- Notifications (optional: notify user of pending request)

---

### 4. Feedback Component

**Responsibility:**
- Store feedback/review submissions
- Validate consent before accepting feedback
- Support feedback versioning (user can edit before published stats aggregation)

**Tables involved:**

```
feedback (NEW)
├── id (PK)
├── from_user_id (FK → users.id, who gave feedback)
├── to_user_id (FK → users.id, who receives feedback)
├── consent_id (FK → consents.id, proof of consent)
├── text (string, the review/feedback)
├── rating (integer, 1-5, or enum: POSITIVE/NEUTRAL/NEGATIVE)
├── category (enum: COMMUNICATION, RELIABILITY, RESPECT, etc.)
├── is_published (boolean, draft vs published)
├── created_at
├── updated_at
├── published_at (nullable, when stats were last computed from this)
├── indexes:
│   ├── (to_user_id, is_published) for stats queries
│   ├── (from_user_id, to_user_id, created_at) for "my feedback"
│   └── (consent_id) for auditing consent violations
```

**Pre-submit validation:**

```python
def submit_feedback(from_user_id, to_user_id, text, rating):
    # 1. Verify consent exists and is ACCEPTED
    consent = db.query(Consent).filter(
        Consent.initiator_user_id == from_user_id,
        Consent.recipient_user_id == to_user_id,
        Consent.status == "ACCEPTED"
    ).first()

    if not consent:
        raise PermissionError("No accepted consent exists")

    # 2. Create feedback (is_published=False initially)
    feedback = Feedback(
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        consent_id=consent.id,
        text=text,
        rating=rating,
        is_published=False
    )
    db.add(feedback)
    db.commit()
    return feedback
```

**API boundaries:**
- `POST /api/feedback` → submit (validates consent)
- `PATCH /api/feedback/{id}` → edit own draft feedback
- `DELETE /api/feedback/{id}` → delete own feedback (revoke)
- `GET /api/feedback?about_user={user_id}` → list published feedback (public, no auth)

**Communicates with:**
- Auth (requires user_id)
- Consent (validates before storing)
- Stats (notifies aggregator when feedback published)

---

### 5. Stats/Aggregation Component

**Responsibility:**
- Pre-calculate and cache reputation metrics
- Generate summaries for profile display (avg rating, themes, quotes)
- Support background refresh without blocking API requests

**Denormalized tables (for performance):**

```
feedback_stats (NEW, materialized view or periodic refresh)
├── id (PK)
├── user_id (FK → users.id, who is being rated)
├── total_feedback_count (int)
├── avg_rating (float, e.g., 3.7 out of 5)
├── positive_percentage (float, % of POSITIVE ratings)
├── category_breakdown (JSON: {COMMUNICATION: 0.6, RELIABILITY: 0.4})
├── recent_themes (JSON array of 5 most common words from feedback text)
├── best_quote (string, longest or most recent positive feedback)
├── worst_quote (string, longest or most recent negative feedback)
├── last_updated (timestamp, when stats were computed)
├── update_version (int, increments on each refresh for cache invalidation)
```

**Refresh strategy:**

```
Option A: Scheduled job (RECOMMENDED for MVP)
├── Runs every 30 minutes
├── Query: SELECT * FROM feedback WHERE to_user_id={uid} AND is_published=true AND published_at > last_update
├── Recalculate stats
├── Update feedback_stats row
├── Increment update_version to invalidate cache

Option B: Event-driven (post-Phase 2)
├── On feedback.published_at change, trigger async job
├── Better for real-time but adds complexity
├── Requires message queue (e.g., Redis pubsub)
```

**Quote selection logic:**

```python
def select_best_worst_quotes(user_id):
    # Best: highest rated, or most recent if tied
    best = db.query(Feedback)
        .filter(Feedback.to_user_id == user_id)
        .filter(Feedback.rating == "POSITIVE")
        .order_by(Feedback.created_at.desc())
        .first()

    # Worst: lowest rated, or most recent if tied
    worst = db.query(Feedback)
        .filter(Feedback.to_user_id == user_id)
        .filter(Feedback.rating == "NEGATIVE")
        .order_by(Feedback.created_at.desc())
        .first()

    return best, worst
```

**API boundaries:**
- `GET /api/stats/{user_id}` → returns denormalized stats (public, no auth)
- `GET /api/stats/{user_id}/feedback` → list individual feedback items (public)
- Internal: refresh job calls `POST /api/stats/{user_id}/refresh` (admin-only, cron)

**Communicates with:**
- Feedback (reads published feedback)
- Cache layer (writes stats, sets TTL)
- Monitoring/metrics (logs aggregation timing)

---

### 6. Search/Discovery Component

**Responsibility:**
- Enable finding users by display_name, location, etc.
- Return only profiles with visibility=PUBLIC or consented users
- No auth required (public discovery)

**Index strategy:**

```
profiles (enhanced indexing)
├── (visibility, display_name) compound index
├── (visibility, location) for location-based search
└── (visibility, created_at) for "newest members"
```

**Query logic (permission-aware):**

```python
def search_profiles(query_string, current_user_id=None):
    base_query = db.query(Profile).filter(Profile.visibility == "PUBLIC")

    # If authenticated, also include PRIVATE profiles we have consent for
    if current_user_id:
        consented_ids = db.query(Consent.recipient_user_id)
            .filter(Consent.initiator_user_id == current_user_id)
            .filter(Consent.status == "ACCEPTED")
            .subquery()

        base_query = base_query.union(
            db.query(Profile).filter(
                Profile.visibility == "PRIVATE",
                Profile.user_id.in_(consented_ids)
            )
        )

    # Filter by search term
    results = base_query.filter(
        Profile.display_name.ilike(f"%{query_string}%")
    ).limit(20)

    return results
```

**API boundaries:**
- `GET /api/search?q=alice&type=user` → public search, no auth
- `GET /api/search?q=alice&type=user` (authenticated) → includes private profiles with consent

**Communicates with:**
- Auth (optional user_id for authenticated searches)
- Consent (checks acceptance status)
- Profiles (reads display_name, location, visibility)

---

## Data Flow

### Flow 1: Feedback Submission (Happy Path)

```
1. User A discovers User B via search/discovery
   GET /api/search?q=bob → returns B's public profile

2. A clicks "Request Consent"
   POST /api/consents/{B.id}/request
   → creates row: (initiator=A.id, recipient=B.id, status=PENDING)
   → notification sent to B (optional)

3. User B views pending requests
   GET /api/consents/pending
   → returns rows where recipient_user_id=B.id AND status=PENDING

4. B clicks "Accept" on A's request
   POST /api/consents/{consent_id}/accept
   → updates: status=ACCEPTED, accepted_at=now()

5. User A can now submit feedback
   POST /api/feedback
   {
       "to_user_id": B.id,
       "text": "Great conversation!",
       "rating": "POSITIVE",
       "category": "COMMUNICATION"
   }
   → Pre-submit validation:
      1. Query: SELECT * FROM consents WHERE initiator=A.id AND recipient=B.id AND status=ACCEPTED
      2. If found: create feedback row with is_published=false
      3. If not found: return 403 Forbidden

6. Feedback submitted, stats stale
   feedback_stats[B.id].last_updated = 5 minutes ago

7. Background job runs (every 30 min)
   → SELECT * FROM feedback WHERE to_user_id=B.id AND is_published=true
   → Recalculate avg_rating, category_breakdown, quotes
   → UPDATE feedback_stats[B.id]
   → increment update_version

8. Next time B's profile is viewed
   GET /api/profiles/{B.id}
   → includes: stats (avg_rating, positive_pct, quote)
   → client caches based on update_version
```

### Flow 2: Consent Revocation

```
1. User B decides to revoke consent from User A
   POST /api/consents/{consent_id}/revoke
   → updates: status=REVOKED, revoked_at=now()

   NOTE: Existing feedback from A about B is NOT deleted
   (audit trail preserved; user chose to revoke ongoing feedback, not past)

2. User A attempts new feedback submission
   POST /api/feedback (from_user_id=A, to_user_id=B, ...)
   → Consent check fails (status=REVOKED, not ACCEPTED)
   → Error: "Consent has been revoked"

3. A can still view existing feedback if it was published
   GET /api/feedback?about_user=B
   → Shows historical feedback (immutable)
   → But A cannot submit new feedback
```

### Flow 3: Profile Visibility Control

```
1. User A has private profile
   PATCH /api/profiles/{A.id}
   { "visibility": "PRIVATE" }
   → Profile hidden in public search

2. User B (non-consented) searches for A
   GET /api/search?q=alice
   → Returns empty (A is PRIVATE and B has no consent)

3. User B requests consent
   POST /api/consents/{A.id}/request
   → Consent request created, B cannot yet see A's profile

4. User A accepts B's consent request
   POST /api/consents/{consent_id}/accept

5. User B now searches for A
   GET /api/search?q=alice (as user B)
   → Returns A's profile (B has ACCEPTED consent)

   Alternative: GET /api/profiles/{A.id}
   → Returns full profile if B has ACCEPTED consent
   → Returns error "Profile is private" if no consent
```

## Build Order Implications

### Phase 1: Foundation (Users + Consent)

**Build first:**
1. Extend `users` table with Face ID auth (already done)
2. Create `consents` table
3. Implement consent request/accept/revoke endpoints
4. Add consent validation middleware for downstream components

**Why first:**
- Consent is a gating requirement for all feedback
- Allows testing consent workflows independently
- Provides permission infrastructure for later phases

**Risk:** If consent schema is wrong, all feedback APIs will be built on broken foundation

---

### Phase 2: Profiles + Feedback

**Build after Phase 1:**
1. Create `profiles` table
2. Implement profile endpoints (CRUD)
3. Create `feedback` table
4. Implement feedback endpoints with consent validation
5. Add search/discovery endpoints

**Dependencies on Phase 1:**
- Feedback submission queries consents table
- Search includes consent checks
- Profile visibility gated by consent

**Risk:** Feedback validation will fail if consent middleware not working

---

### Phase 3: Stats + Caching

**Build after Phases 1-2:**
1. Create `feedback_stats` table
2. Implement stats calculation job (scheduled)
3. Add stats endpoints (read-only)
4. Implement cache invalidation strategy

**Dependencies on Phase 1-2:**
- Stats reads from `feedback` and `consents` tables
- No feedback = no stats to aggregate
- Consent tracking helps audit stat accuracy

**Can defer to Phase 2+:** Stats are read-only and non-blocking; profiles still work without them (just slower)

---

### Phase 4: Scale (Caching Layer)

**Build after Phase 3, if needed:**
1. Add Redis (or in-process cache)
2. Cache profile stats with TTL
3. Cache search results
4. Implement cache invalidation on feedback changes

**No new database changes required**

**Optional optimization:** Only add if bottleneck appears (hitting db every request)

---

## Database Schema (Full)

```sql
-- Existing (from auth phase)
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    embedding JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_email ON users(email);

-- NEW: Profile data
CREATE TABLE profiles (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    display_name VARCHAR,
    bio TEXT,
    profile_photo_url VARCHAR,
    location VARCHAR,
    visibility VARCHAR CHECK(visibility IN ('PUBLIC', 'PRIVATE')) DEFAULT 'PUBLIC',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX idx_visibility_display ON profiles(visibility, display_name);
CREATE INDEX idx_visibility_location ON profiles(visibility, location);

-- NEW: Consent relationships
CREATE TABLE consents (
    id INTEGER PRIMARY KEY,
    initiator_user_id INTEGER NOT NULL,
    recipient_user_id INTEGER NOT NULL,
    status VARCHAR CHECK(status IN ('PENDING', 'ACCEPTED', 'REVOKED')) DEFAULT 'PENDING',
    initiated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accepted_at TIMESTAMP,
    revoked_at TIMESTAMP,
    FOREIGN KEY (initiator_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (initiator_user_id, recipient_user_id)
);
CREATE INDEX idx_recipient_status ON consents(recipient_user_id, status);
CREATE INDEX idx_initiator_recipient ON consents(initiator_user_id, recipient_user_id, status);

-- NEW: Feedback submissions
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    from_user_id INTEGER NOT NULL,
    to_user_id INTEGER NOT NULL,
    consent_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    rating VARCHAR CHECK(rating IN ('POSITIVE', 'NEUTRAL', 'NEGATIVE')),
    category VARCHAR CHECK(category IN ('COMMUNICATION', 'RELIABILITY', 'RESPECT', 'OTHER')),
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP,
    FOREIGN KEY (from_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (to_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (consent_id) REFERENCES consents(id) ON DELETE RESTRICT
);
CREATE INDEX idx_to_user_published ON feedback(to_user_id, is_published);
CREATE INDEX idx_from_to_created ON feedback(from_user_id, to_user_id, created_at);
CREATE INDEX idx_consent_id ON feedback(consent_id);

-- NEW: Aggregated stats (denormalized, refreshed periodically)
CREATE TABLE feedback_stats (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    total_feedback_count INTEGER DEFAULT 0,
    avg_rating FLOAT DEFAULT 0.0,
    positive_percentage FLOAT DEFAULT 0.0,
    category_breakdown JSON,  -- {"COMMUNICATION": 0.6, "RELIABILITY": 0.4}
    recent_themes JSON,       -- ["trust", "responsive", "kind"]
    best_quote TEXT,
    worst_quote TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_version INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX idx_user_id ON feedback_stats(user_id);
```

## Caching Considerations

### What to Cache

1. **Profile stats** (low write, high read)
   - Key: `stats:{user_id}:{version}`
   - TTL: 1-4 hours
   - Invalidated: when `feedback_stats.update_version` increments

2. **Profile data** (medium write, high read in discovery)
   - Key: `profile:{user_id}:{version}`
   - TTL: 1 hour
   - Invalidated: when user updates profile

3. **Search results** (high write potential due to profile changes, low read)
   - Don't cache initially; add if bottleneck appears
   - If cached: Key: `search:{query_hash}`; TTL: 15 minutes

### Cache Invalidation Strategy

```python
def invalidate_profile_cache(user_id):
    """Called when profile is updated"""
    redis.delete(f"profile:{user_id}:*")

def invalidate_stats_cache(user_id):
    """Called when feedback_stats.update_version changes"""
    redis.delete(f"stats:{user_id}:*")

def refresh_stats(user_id):
    """Scheduled job: recalculate and invalidate cache"""
    stats = calculate_feedback_stats(user_id)
    db.update(feedback_stats, stats)
    invalidate_stats_cache(user_id)
```

## Performance & Scalability

### At <1K users (MVP)
- No caching needed
- Direct database queries
- Full table scans acceptable (users table tiny)
- Consent lookups: O(1) via unique index
- Stats refresh: run every 30 min, completes in <1s

### At 10K users
- Add caching for profile stats
- Consider indexing search terms (display_name, location)
- Consent lookups still O(1)
- Stats refresh: run more frequently, parallel across shards

### At 100K+ users
- Redis caching required
- Elasticsearch for full-text search
- Partition consent table by recipient_user_id
- Partition feedback table by to_user_id
- Stats aggregation via MapReduce or Spark batch jobs

## Key Architectural Decisions

| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| **Unidirectional consent** | Privacy: A→B feedback doesn't auto-grant B→A | More schema complexity than bidirectional |
| **Denormalized stats table** | Fast profile display; no expensive aggregates on read | Stats slightly stale (30min delay); need refresh job |
| **Scheduled refresh vs event-driven** | Simpler for MVP; no message queue; predictable load | Delayed stats (30min); not real-time |
| **JSON for category_breakdown & themes** | Flexible schema; no migration per new category | Query-unfriendly for filtering; need app-level parsing |
| **Quote selection: max recent not longest** | Recency signals active engagement; avoids gaming | May miss nuance of verbose feedback |
| **No permanent feedback deletion** | Audit trail; prevents consent abuse evidence erasure | User cannot fully delete past feedback |
| **Consent.status=REVOKED not deleted** | Audit trail; prevents replay of old consents | Revocation history visible |

## Anti-Patterns to Avoid

### 1. Bidirectional consent without opt-out
**What goes wrong:** A requests consent to give feedback about B. B accepts. Now A thinks they can give feedback, but system auto-grants B→A consent. A is surprised when B gives unsolicited feedback about A.

**Prevention:** Use unidirectional model. Each party explicitly requests consent when needed.

---

### 2. Stats without versioning
**What goes wrong:** Client caches profile stats. Backend recalculates stats. Client doesn't know stats changed. Shows stale reputation for hours.

**Prevention:** Include `update_version` in stats response. Client re-fetches if version increments.

---

### 3. Feedback deletion instead of revocation
**What goes wrong:** User A gives negative feedback about B. B complains. A deletes feedback. Now there's no audit trail that feedback existed. Later, A gives same negative feedback again; B has no proof of prior feedback.

**Prevention:** Mark feedback as `deleted_by_user=true` instead of cascading delete. Keep audit trail.

---

### 4. Consent validation only at submit time
**What goes wrong:** A requests consent, B accepts, A submits 10 feedback items. B revokes consent. All 10 feedback items remain published. A could argue "I submitted when consent existed."

**Prevention:** Add `submitted_with_consent=true` flag to feedback. During revocation, optionally unpublish feedback (or keep published but flag "consent later revoked").

---

### 5. Stats aggregation in request path
**What goes wrong:** User views profile. System recalculates stats from 1000 feedback items. Blocks request for 5s. User sees timeout.

**Prevention:** Pre-calculate stats in background job. On read, serve cached stats. Never aggregate in request path.

---

### 6. No distinction between draft and published feedback
**What goes wrong:** User submits feedback with typos. Edits feedback. But stats already include original version. Profile shows wrong reputation.

**Prevention:** Keep `is_published=false` until background job includes feedback in stats. Allow user edits pre-publication. Treat published feedback as immutable.

---

### 7. Profile visibility not considered in consent logic
**What goes wrong:** User A has PRIVATE profile. User B requests consent to give feedback. A accepts. B now has "consent" but still can't see A's profile in discovery. Confusing UX.

**Prevention:** Visibility and consent are separate concerns. Consent = "can give feedback"; Visibility = "can be discovered." Both must be satisfied for full access.

---

## Migration Path from Auth-Only to Full System

### Step 1: Add consent table (zero-downtime)
- New table, no changes to existing data
- Consent endpoints live but optional
- Feedback endpoints not yet added

### Step 2: Add profiles table (zero-downtime)
- New table, auto-populate from users.email on first profile read
- Visibility defaults to PUBLIC (opt-in to PRIVATE later)

### Step 3: Add feedback table + endpoints (zero-downtime)
- New table, consent validation active
- Only new feedback uses consent checks
- Backwards compatible with feedback-less profiles

### Step 4: Add stats table + refresh job (zero-downtime)
- New table, initially empty
- Refresh job runs, populates stats asynchronously
- Endpoints serve stats if available, else empty stats

## Testing Strategy by Component

| Component | Test Coverage | Risk Level |
|-----------|---------------|-----------|
| **Consent validation** | Unit: test matrix of all status combos; E2E: request→accept→feedback | CRITICAL - wrong consent breaks security |
| **Profile visibility** | Unit: permission checks; E2E: public search, private without consent | HIGH - data leakage risk |
| **Feedback submission** | Unit: consent lookup; E2E: consent→submit→view | HIGH - feedback should never bypass consent |
| **Stats refresh** | Unit: aggregation logic; Integration: full feedback→stats pipeline | MEDIUM - stats wrong doesn't break functionality, just accuracy |
| **Search** | Unit: query construction; E2E: public/private profile visibility | MEDIUM - search should respect visibility but not security-critical |

## Sources

- [Graph Theory for Consent Management](https://dl.acm.org/doi/10.1145/3665252.3665265) - ACM SIGMOD
- [Consent Management in Data Workflows: A Graph Problem](https://openproceedings.org/2023/conf/edbt/3-paper-121.pdf) - EDBT 2023
- [Customer Reviews and Ratings Platform Design](https://www.geeksforgeeks.org/sql/how-to-design-a-relational-database-for-customer-reviews-and-ratings-platform/) - GeeksforGeeks
- [Database Schema Design Best Practices](https://www.bytebase.com/blog/top-database-schema-design-best-practices/) - Bytebase
- [Denormalization and Materialized Views](https://www.datacamp.com/tutorial/denormalization) - DataCamp
- [Caching Best Practices](https://aws.amazon.com/caching/best-practices/) - AWS
- [Role-Based Access Control](https://memgraph.com/docs/database-management/authentication-and-authorization/role-based-access-control) - Memgraph
- [Reputation, Feedback, and Trust in Online Platforms](https://www.cambridge.org/core/books/reengineering-the-sharing-economy/reputation-feedback-and-trust-in-online-platforms/6C1EB222CAE385076434293D2680EC13) - Cambridge University Press
