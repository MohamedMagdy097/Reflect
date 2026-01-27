# Research Summary: Reflect Post-Date Feedback Platform

**Researched:** January 19, 2026  
**Status:** Research complete ✓

---

## Key Findings

### Architecture Pattern
**Consent graph model** (unidirectional) with three-layer permissions:
1. Visibility (PUBLIC/PRIVATE profile setting)
2. Consent (A→B directed edge in consent graph)
3. Publication (draft vs published feedback)

All three layers must align for feedback visibility.

### Stack Recommendations
- **Auth:** PyJWT 2.8+ (replace deprecated python-jose)
- **Forms:** React Hook Form 7.48+ + Zod 3.22+ 
- **Search:** SQLite FTS5 (outperforms Elasticsearch for <10M records)
- **Database:** Keep SQLite + SQLAlchemy 2.0 async (3-5x throughput with aiosqlite)
- **Caching:** HTTP headers Phase 1, Redis Phase 4+ (if metrics trigger)

### Feature Priorities
**v1 Table Stakes:**
- Unidirectional consent requests
- User search by name/email
- Structured feedback forms + tags
- Profile visibility controls
- Block/report functionality

**v2 Differentiators:**
- Pattern detection
- Reputation trends
- Compatibility insights
- Demographic fairness monitoring

**Anti-Features (Don't Build):**
- Anonymity, unsolicited messaging, numeric ratings, one-time consent

### Critical Pitfalls
| Pitfall | Risk | Prevention |
|---------|------|-----------|
| Consent violations | HIGH (federal liability) | Two-party consent before visibility |
| Sybil attacks | HIGH | Account maturity, rate limiting, behavior detection |
| Feedback bias | HIGH | Structured templates, rater quality weighting |
| Privacy violations | HIGH | PII filtering, content guidelines |
| System gaming | MEDIUM | Pattern detection on rating behavior |

### Recommended Phases
1. **Foundation:** Consent graph + profiles + feedback gating (4 weeks)
2. **Intelligence:** Denormalized stats + pattern detection (2 weeks)
3. **Safety:** Advanced abuse detection + appeals (2 weeks)
4. **Scale:** Caching/DB optimization (as-needed)

---

Research files: `.planning/research/STACK.md`, `FEATURES.md`, `ARCHITECTURE.md`, `PITFALLS.md`
