# Reflect

## What This Is

A post-date feedback platform where users collect honest feedback from their dates through a mutual consent system. All profiles are publicly visible with aggregated stats and curated quotes. Face ID authentication prevents fake accounts and ensures authenticity.

## Core Value

Honest, actionable feedback from real dates helps people understand how they're perceived — with Face ID ensuring every account represents a real person.

## Requirements

### Validated

- ✓ User can sign up with face ID (webcam capture) — existing
- ✓ User can sign in with face ID verification — existing
- ✓ Face embeddings stored in SQLite database — existing
- ✓ FastAPI backend + Next.js frontend architecture — existing
- ✓ Docker containerization for both services — existing

### Active

**User Profiles:**
- [ ] User has public profile page visible to all authenticated users
- [ ] Profile displays aggregated feedback stats (tag counts)
- [ ] Profile displays curated quotes from feedback (basic display in v1, AI curation in v2)

**Search & Consent:**
- [ ] User can search for other users by name or email
- [ ] User can request feedback consent from another user
- [ ] User can accept/reject feedback consent requests
- [ ] User can view pending and accepted consent relationships
- [ ] Mutual consent required before feedback exchange

**Feedback Submission:**
- [ ] User can give feedback to consented connections
- [ ] Feedback form includes predefined tags (friendly, kind, funny, angry, etc.)
- [ ] Feedback form includes text field for quotes/comments
- [ ] Both positive and negative feedback tags supported

**Stats & Display:**
- [ ] System aggregates feedback tags into stats (counts per tag)
- [ ] Stats displayed on user profiles
- [ ] Feedback quotes stored and associated with profiles

**Security:**
- [ ] JWT session tokens replace URL parameter authentication
- [ ] Secure token storage and refresh mechanism
- [ ] Rate limiting on expensive face recognition endpoints
- [ ] Face embedding encryption at rest (optional for v1, security improvement)

### Out of Scope

- Mobile app — Web only for v1
- Social features — No messaging, following, or social graph beyond feedback relationships
- AI insights — Pattern detection and trend analysis deferred to v2
- AI quote curation — Algorithm to select "best/worst" quotes deferred to v2
- Real-time notifications — Email/push notifications for consent requests (can be added later)
- Account recovery — Face ID is the only auth method (no password reset needed)

## Context

- Windows development environment (use `;` for command chaining)
- Monorepo structure: face-recognition-server/ + nextjs-app/
- Face recognition: DeepFace + RetinaFace (computationally expensive, needs rate limiting)
- Existing security concerns documented in .planning/codebase/CONCERNS.md
- Zero test coverage currently (needs addressing)
- Privacy model: public reputation system (diverges from README's "no public judgment")

## Constraints

- **Tech Stack**: Keep existing FastAPI/Next.js/SQLite stack (production migration to PostgreSQL is future work)
- **Development**: Windows environment (bash via Git Bash)
- **Timeline**: No hard deadline (focus on quality over speed)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Face ID authentication | Prevents fake accounts, ensures authenticity | ✓ Good - working prototype |
| Public reputation system | Transparency helps people make informed decisions | — Pending - diverges from "no public judgment" in README |
| Mutual consent required | Prevents unsolicited feedback, maintains control | — Pending |
| Both positive/negative tags | Honest feedback requires capturing full picture | — Pending - requires abuse prevention |
| SQLite database for v1 | Fast prototyping | ⚠️ Revisit - not production-ready |
| AI quote curation (v2) | Removes bias from users hiding negative feedback | — Pending - v2 feature |

---
*Last updated: 2026-01-19 after initialization*
