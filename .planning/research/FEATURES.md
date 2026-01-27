# Feature Landscape: Post-Date Feedback Platform

**Domain:** Post-date feedback and public reputation system for dating
**Researched:** January 2026
**Confidence:** MEDIUM (based on dating app trends + feedback platform patterns; mutual consent feedback as explicit domain is less common, requiring interpretation)

## Table Stakes

Features users absolutely expect. Missing these = product feels incomplete or unsafe.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Mutual consent feedback form** | Core value proposition - you can't give feedback without match consent | High | Requires both parties to have matched/met and agreed to share feedback. Solves the "feedback without permission" problem |
| **Basic feedback collection** | Users need a simple way to input feedback after a date | Medium | Text input, optionally structured (ratings, tags, quotes) |
| **Consent verification before display** | Trust and safety - feedback shouldn't appear without explicit consent | High | Similar to Hinge's "We Met" feature - both parties consent to share interaction |
| **Profile visibility** | Users need a public profile showing their reputation | High | Public profiles showing aggregated feedback, reputation score/summary |
| **Ability to view your own feedback** | Users need transparency on what's being said about them | Medium | Private view of feedback given about you, with context |
| **Block/report functionality** | Safety mechanism for abusive feedback | Medium | Report false/malicious feedback; block users from giving feedback |
| **Moderation against abuse** | Platform must prevent harassment through feedback | High | Flag and remove offensive content, abusive patterns |
| **Basic search/discovery** | Users find people they've dated to give/receive feedback | Medium | Search by name, date, time period; match history integration |
| **Authentication/identity verification** | Ensures feedback is from real people who actually dated | High | Face ID (already solved in this project) plus profile verification |
| **Privacy controls on profile visibility** | Users control who sees their profile and feedback | Medium | Options: fully public, friends only, or restricted viewing |

## Differentiators

Features that set Reflect apart. Not expected by default, but create competitive advantage.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **AI-powered pattern detection** | Identify recurring behaviors across feedback (chronic lateness, ghosting patterns, love-bombing, safety red flags) | High | Analyze feedback history to surface patterns invisible in individual reviews |
| **Smart quote highlighting** | Extract and display particularly insightful or representative quotes from longer feedback | Medium | Use NLP to pull significant statements; let users curate favorite quotes |
| **Behavior trend visualizations** | Show how someone's reputation evolves over time (improving, consistent, declining) | Medium | Charts showing feedback sentiment trajectory, response patterns |
| **Compatibility insights** | Suggest what types of dates/people rate you positively (e.g., "rated highly by outdoorsy types") | High | Segment feedback by user characteristics to show compatibility patterns |
| **Proactive safety flagging** | Warn users before dates if matched person has multiple concerning feedback entries** | High | Privacy-respecting warning system; requires careful design to avoid false accusations |
| **Feedback response mechanism** | Allow users to privately or publicly respond to feedback about them | Medium | Contextual responses help clarify misunderstandings; build dialogue |
| **Detailed tagging system** | Structured tags (personality traits, interests, behavior, safety concerns) help organize feedback | Medium | Hierarchical tags: Kindness > Genuine, Respect > Listener, etc. |
| **Mutual rating symmetry** | Show how both people rated each other (without revealing specific scores until both submit) | Medium | Similar to Airbnb's simultaneous reveal - encourages honesty by reducing retaliation fear |
| **AI writing feedback** | Suggest improvements to drafted feedback before posting (tone, clarity, fairness) | Medium | Educate users on constructive feedback; reduce reactive negative posts |
| **Connection strength metrics** | Show what % of past dates agree on core traits/assessments about someone | High | Credibility through consensus - "6 out of 8 past dates mentioned trustworthiness" |
| **Demographic insights (anonymized)** | Show feedback patterns by age range, location, or date type without exposing individual identities | High | Help users understand which audiences/approaches work for them |

## Anti-Features

Features to explicitly NOT build. Common mistakes in this domain.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| **Anonymous feedback** | Enables harassment, false accusations, and discourages accountability. Users fear retaliation with bad reason to fear lies. | Require identity verification. Feedback comes from people you've actually dated. |
| **Unsolicited messaging/contact** | Users receive unwanted messages from past dates. Creates harassment vector. | Feedback system only; no direct messaging. Control re-contact through user settings. |
| **Numeric rating gamification** | Tempts users to rate-hoard for visibility or punish perceived rejection. Creates "reputation manipulation" culture. | Focus on narrative feedback + tags. Avoid simple 5-star gamification that incentivizes gaming. |
| **Public rejection indicators** | Showing "they rejected your feedback" or "feedback denied" publicly shames users and encourages retaliation. | Keep consent/rejection private. Don't display public metrics on who denied you. |
| **Searchability by low ratings** | Users intentionally seek out people with bad feedback to harass or "punish." Enables targeted abuse. | Prevent sorting/filtering by "lowest rated." Surface feedback contextually, not by ranking. |
| **Automated "bad date" labels** | System auto-tagging users as "red flag," "liar," or "dangerous" invites lawsuits and false accusations. | Human-only curation; no automatic categorization. Require specific evidence (multiple consistent reports). |
| **Permanent record with no appeals** | Unfair feedback becomes a permanent stain with no path to correction or redemption. | Implement feedback edit/clarification windows. Allow users to dispute clearly false reports. |
| **Cross-platform reputation export** | Reputation follows users to other dating apps, creating permanent digital scarlet letters. | Keep feedback private to Reflect. No third-party integrations. |
| **Real-time alerts on feedback received** | "John just gave you 3-star feedback" notifications create anxiety loops and retaliation incentives. | Digest feedback; reveal on weekly/monthly cadence, not in real-time. |
| **Detailed location/context leakage** | Feedback reveals "we met at [specific bar]" or "[exact date/time]" enabling stalking. | Generalize context. Allow "coffee date" not "Starbucks on 5th & Main at 2pm." |
| **No content moderation infrastructure** | Believing users will self-police feedback comments. They won't. | Invest heavily in moderation, flagging systems, and abuse response. |
| **Revenge/retaliation feedback** | Allowing feedback framed as retaliation ("They gave me bad feedback so here's worse feedback") to stand. | Detect retaliation patterns. Require feedback to be constructive, not punitive. |

## Privacy Considerations

Critical for this specific domain.

### Consent Model
- **Required mutual consent** before any feedback appears publicly. Both parties must explicitly agree feedback sharing is acceptable.
- **Consent window limitation**: Feedback only accepted within 30 days of confirmed date (prevents retroactive accusations).
- **Withdrawal mechanism**: Users can request feedback removal within dispute window (e.g., 7 days after submission).

### Data Visibility Tiers
- **Private to self**: All feedback given about you visible only to you initially
- **Consent-pending**: Feedback awaiting your acceptance/rejection (stays hidden until resolved)
- **Public**: Approved feedback visible on your public profile
- **Profile audience**: Users choose if profile visible to: all, verified users only, or connections only

### Sensitive Information Protection
- **Quote redaction**: Automatically detect and blur personally identifying info in quotes (addresses, full names of others, workplace)
- **Context generalization**: Instead of "we went to the Marriott downtown," store as "hotel" or "upscale venue"
- **No location persistence**: Don't retain exact locations of dates
- **Feedback fingerprinting**: Prevent users from identifying feedback giver through writing style/details

### Abuse Prevention Gates
- **Rate limiting**: Users can give 1 feedback per person per month (prevents feedback spam)
- **Content scanning**: Automated detection of slurs, threats, personal attacks before submission
- **Flag mechanism**: Users can dispute feedback as false, malicious, or in violation of guidelines
- **Escalation path**: Repeated violations → warning → suspension of feedback ability → account review

## Feature Dependencies

```
Core Loop:
  Face ID Auth (solved) → Match/Date Confirmation → Feedback Form Request
                         → Both Consent → Feedback Visible on Profiles

Safety Net:
  Feedback Submission → Content Moderation → Approved/Flagged
                                         → Dispute/Appeal Path

Reputation Building:
  Multiple Feedback Entries → Pattern Detection → Safety Warnings/Insights
  (requires minimum 3+ feedback entries to surface patterns)
```

## MVP Recommendation

**Build in Phase 1 (Table Stakes):**
1. Mutual consent feedback form (text + tags)
2. Profile display (basic reputation summary)
3. Moderation pipeline (human review + abuse flagging)
4. Block/report functionality
5. Basic privacy controls (public/private profile toggle)

**Defer to Phase 2 (Differentiators):**
- Pattern detection (requires feedback volume)
- AI writing feedback suggestions
- Behavior trend visualizations
- Response mechanism to feedback
- Demographic insights

**Defer to Phase 3+ (Post-MVP):**
- Compatibility insights (requires significant data)
- Connection strength metrics
- Advanced tagging system
- Proactive safety flagging (legal/liability concerns)

**Rationale:**
Table stakes create the core product (feedback + reputation). Differentiators come once you have signal. Safety features (flagging, AI warnings) require legal review and can create liability, so treat as later additions with careful governance.

## Known Gotchas for This Domain

**Retaliation Problem**: Two-way feedback systems suffer from "mutual assured destruction" where users fear leaving negative feedback because the other person can retaliate. Airbnb solved this with simultaneous reveal (both submit, then both see). Consider implementing similar "sealed envelope" model.

**Consent is Dynamic**: Research from 2025 shows consent apps that treat consent as static transaction fail. Consent to share feedback may not be consent to specific uses (e.g., "you can see my feedback" ≠ "you can share it with others"). Build in ongoing opt-in, not one-time checkbox.

**Reputation Permanence**: Unlike product reviews (which fade), dating reputation is personal. A bad date 3 years ago shouldn't follow someone forever. Consider time-decay on older feedback or explicit "refresh" mechanisms.

**False Accusations Risk**: Without identity verification (which you have), false accusers can create profiles specifically to harm reputations. Require Face ID + phone verification + date confirmation before feedback allowed.

**Cross-Dating Challenges**: A person might date someone multiple times, or receive feedback from multiple people on the same person. Need clear models for: duplicate feedback, updating feedback, feedback for same person over time.

## Sources

### Consent & Dating Safety Research
- [Online Dating as Context to Design Sexual Consent Technology with Women and LGBTQ+ Stakeholders | CHI 2023](https://dl.acm.org/doi/full/10.1145/3544548.3580911) - Foundational research on consent technology design
- [Dating Apps Need to Learn How Consent Works | Electronic Frontier Foundation, 2025](https://www.eff.org/deeplinks/2025/07/dating-apps-need-learn-how-consent-works) - Legal/ethical perspective on consent models
- [Love Under Lock and Key: How Modern Dating Apps Protect User Privacy in 2025 | PG Dating Pro](https://www.datingpro.com/blog/love-under-lock-and-key-how-modern-dating-apps-protect-user-privacy-in-2025/) - Current dating app privacy practices

### Two-Way Feedback Systems
- [Reputation and Feedback Systems in Online Platform Markets | Steven Tadelis, UC Berkeley](https://faculty.haas.berkeley.edu/stadelis/Annual_Review_Tadelis.pdf) - Economics and design of bilateral feedback
- [Feedback as a two-way street: when and why rating consumers fails | ResearchGate](https://www.researchgate.net/publication/351369998_Feedback_as_a_two-way_street_when_and_why_rating_consumers_fails) - Retaliation problem in mutual rating systems
- [10 Dating App Trends Product Managers Must Know in 2025 | GetStream](https://getstream.io/blog/dating-app-trends/) - Current dating app feature landscape

### Reputation Systems
- [Reputation Systems Overview | VPN Unlimited](https://www.vpnunlimited.com/help/cybersecurity/reputation-system) - Core mechanisms for reputation systems
- [Public Reputation Profile System Features and Abuse Prevention | IPXO](https://www.ipxo.com/kb/abuse-prevention-and-reputation/) - Abuse prevention in reputation systems

### Moderation & Harassment Prevention
- [AI-Powered Moderation Tools for Enhancing Digital Safety | ResearchGate, 2024](https://www.researchgate.net/publication/387185299_AI-Powered_Moderation_Tools_for_Enhancing_Digital_Safety_and_Reducing_Online_Harassment_in_American_Communities) - AI moderation approaches
- [Tools Against Harassment: Empowering Content Creators | ADL](https://www.adl.org/resources/report/tools-against-harassment-empowering-content-creators) - Harassment prevention design patterns
- [Top 14 Content Moderation Tools for 2025 | Influencer Marketing Hub](https://influencermarketinghub.com/content-moderation-tools/) - Current moderation tool landscape

### Testimonial/Feedback Platforms
- [Do I Need Permission to Use Customer Testimonials? | Testimonial Donut, 2025](https://www.testimonialdonut.com/resources/do-i-need-permission-to-use-customer-testimonials) - Consent requirements for feedback/testimonials
- [Quote Collection and Privacy | Senja](https://senja.io/) - Testimonial platform design patterns

### Verification & Identity
- [Tinder Face Verification Starts Today as Dating Apps Battle Scambots | 9to5Mac, 2025](https://9to5mac.com/2025/10/23/mandatory-tinder-face-verification-starts-today-as-dating-apps-battle-scambots/) - Current ID verification approaches
- [Best Safe Dating Apps 2025: Safety & Verification Compared | Luxy](https://millionairedating.onluxy.com/best-dating-apps-safety-verification-2025.html) - Verification standard in 2025 dating apps

### AI & Pattern Detection
- [AI-Powered Behavioral Analysis in Cybersecurity | CrowdStrike](https://www.crowdstrike.com/en-us/cybersecurity-101/artificial-intelligence/ai-powered-behavioral-analysis/) - Behavioral anomaly detection patterns
- [Feedback Tagging and Auto-Categorization | InMoment](https://inmoment.com/blog/automatically-organize-qualitative-customer-feedback-with-auto-tagging/) - AI tagging systems for feedback

## Confidence Notes

**HIGH confidence** on:
- Table stakes (consent, feedback forms, moderation, profiles) - well-established in dating app and feedback platform research
- Anti-features (anonymity, unsolicited contact, gaming) - strong consensus in abuse prevention literature

**MEDIUM confidence** on:
- Differentiators (pattern detection, compatibility insights) - viable but requires careful implementation and testing
- Retaliation problem mitigation - Airbnb's approach is documented but untested specifically for dating feedback
- Privacy model specifics - consent models are evolving; explicit feedback timing and withdrawal windows need validation

**LOW confidence** on:
- Proactive safety flagging (warning before dates) - legal implications unclear; requires legal review
- Specific tagging hierarchy - domain-specific; needs user research in Reflect context
