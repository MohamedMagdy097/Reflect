# Domain Pitfalls: Post-Date Feedback & Reputation Systems

**Project:** Reflect (public reputation system with Face ID)
**Domain:** Post-date feedback and reputation platforms
**Researched:** 2026-01-19
**Confidence:** MEDIUM to HIGH (verified with 2025 regulatory changes, platform research, and behavioral studies)

---

## CRITICAL PITFALLS

These mistakes cause rewrites, legal liability, user exodus, or system collapse.

### Pitfall 1: Consent Violation Through Unverified Feedback

**What goes wrong:**
System publishes feedback about someone without their awareness or agreement that it would be published. Or worse: intimate images, videos, or non-consensual depictions are shared via feedback mechanism.

**Why it happens:**
- Assuming "mutual match" = automatic consent to feedback
- Treating feedback as private conversation but then making it public
- Not explicitly asking "will you publish this?" when collecting feedback
- Allowing images/videos in feedback without explicit consent protocols
- Gap between "feedback collected" and "feedback displayed" creates ambiguity

**Consequences:**
- Federal liability (TAKE IT DOWN Act 2025: platforms must remove non-consensual intimate imagery within 48 hours or face penalties)
- Class action lawsuits from users whose reputations were damaged
- User exodus when community discovers consent violations
- Regulatory investigation and possible platform shutdown

**Prevention:**
1. **Explicit consent flow** (Address in Phase 1):
   - When feedback is given: "This will be visible to [person's] profile. Agree?"
   - When feedback is published: Notify both parties in advance of what will appear
   - Allow feedback giver to withdraw consent before publication

2. **Two-party verification**:
   - Require BOTH parties to agree feedback enters public system
   - Consider "draft feedback" → "person reviews" → "agreement to publish" → "published" flow
   - For sensitive feedback types, require active confirmation

3. **Image/video scanning** (Phase 2-3):
   - Scan all images/videos in feedback against PhotoDNA or similar (StopNCII.org)
   - Reject intimate imagery automatically
   - Educate users: "Intimate images forbidden in feedback"

4. **Documentation**:
   - Log consent with timestamps (prove later if needed)
   - Store explicit agreements ("User X agreed to publish feedback about User Y on [date]")

**Detection:**
- Spike in reports: "I didn't agree to this feedback being public"
- Users receiving feedback they had no context for
- Intimate images appearing in feedback before you detect them
- Legal takedown notice or government inquiry

**Phase responsibility:** Phase 1 (consent architecture is foundational)

---

### Pitfall 2: Sybil Attacks & Coordinated Reputation Destruction

**What goes wrong:**
Bad actor creates 10+ fake accounts (each passes Face ID) and systematically attacks one person's reputation with negative feedback. Or coordinated group attacks someone with false negative feedback to tank their rating.

**Why it happens:**
- Face ID prevents *casual* fake accounts but not determined attackers with multiple real faces
- No cooldown between feedback submissions
- No detection of coordinated behavior (same IP, same geolocation, similar feedback patterns)
- Reputation algorithm weights all feedback equally regardless of account age or behavior history
- No minimum "relationship history" required to give feedback (e.g., "give feedback 30 days after match")

**Consequences:**
- Innocent user's reputation collapses overnight from coordinated attack
- User loses trust in system, leaves platform
- Legal liability if person can prove coordinated harassment
- Platform reputation: "anyone can destroy someone else's reputation"

**Prevention:**
1. **Account maturity requirements** (Phase 1):
   - Can't give feedback until 48+ hours after match
   - Can't give feedback until you've exchanged some messages
   - First-time accounts have limited feedback weight

2. **Coordinated behavior detection** (Phase 2):
   - Flag: 3+ new accounts giving negative feedback to same person within 24 hours
   - Flag: Multiple accounts from same IP/geolocation targeting one person
   - Flag: Feedback text is similar across accounts (copy-paste attacks)
   - Response: Hold feedback for review before publishing

3. **Reputation algorithm resistance** (Phase 2):
   - Weight feedback by account age/history (new account feedback worth 20%, established account worth 100%)
   - Require minimum feedback history from giver before their feedback counts (10+ previous honest reviews)
   - Discount feedback from accounts that only target one person

4. **Rate limiting** (Phase 1):
   - One person can give at most 1 feedback per match
   - Same person can't give feedback twice to same target in 30 days
   - Account can't give more than 3 feedbacks per week

5. **Manual review workflow** (Phase 2):
   - Rapid reputation swings trigger review queue
   - Community moderators can reject obviously coordinated attacks

**Detection:**
- Reputation graph suddenly becomes highly negative in short time
- Multiple new accounts all target one user with similar feedback
- Feedback metrics: "20 new feedbacks in 6 hours" (anomaly)
- User reports: "I'm being attacked"

**Phase responsibility:** Phase 1 (rate limiting, account maturity) + Phase 2 (detection, moderation)

---

### Pitfall 3: Feedback Bias & Unfair Representation

**What goes wrong:**
System amplifies existing biases (racial, gender, appearance-based, age-based) through feedback. Examples:
- Women receive "too selective" feedback while men receive "approaches too many people" (same behavior, gendered language)
- Racial minorities' profiles get systematically lower feedback
- Older users' feedback is interpreted as "boring" while younger users with identical behavior get "fun"

**Why it happens:**
- Feedback text is unstructured and captures human biases directly
- System doesn't surface that similar behaviors get opposite feedback
- Algorithmic recommendation learning from biased feedback (shows "low-rated" profiles less)
- No visibility into feedback disparities by demographic group
- Platform culture: "we're neutral, users decide"—actually amplifying bias

**Consequences:**
- Systematically disadvantages certain users (legally: discrimination risk)
- Creates feedback death spiral (low feedback → shown less → get less feedback)
- Erodes trust when users discover bias in system
- Regulatory scrutiny (fairness in algorithmic systems)
- Unfair/hostile environment for marginalized users

**Prevention:**
1. **Structured feedback** (Phase 1):
   - Don't allow free-form text feedback alone
   - Use categories: "communication style", "honesty", "respectfulness", "effort in planning"
   - Remove appearance-based feedback entirely
   - This reduces biased language

2. **Bias detection & monitoring** (Phase 2):
   - Query: "Are women receiving different feedback language than men for same behavior?"
   - Metric: "Average feedback score by age, race, gender" (publicly report)
   - Flag: Users whose feedback is statistically biased against certain demographics
   - Response: Down-weight their feedback contributions

3. **User education** (Phase 1):
   - Show users: "Feedback should be about [communication, effort, honesty]—not appearance"
   - Examples of good/bad feedback before they submit

4. **Feedback review process** (Phase 2):
   - Human review of feedback that's exceptionally negative (< 2 stars)
   - Reject feedback that uses appearance language ("too ugly", "boring look")
   - Reject feedback that profiles suggest is demographic-targeted

5. **Visibility & appeal** (Phase 2):
   - Let users see *why* feedback was given (categories, not comments if possible)
   - Allow appeal/context: "That feedback is unfair, here's why"
   - Users can request anonymization of low scores if pattern seems biased

**Detection:**
- Users from same demographic group have systematically lower feedback scores
- Feedback language differs by demographic (same behavior, different feedback)
- User reports: "I'm getting [racist/sexist/ageist] feedback"
- Statistical analysis: "Female users average 3.2 stars, male users 3.8 stars for same behavior"

**Phase responsibility:** Phase 1 (structured feedback, education) + Phase 2 (bias detection, monitoring)

---

### Pitfall 4: Privacy Violations & Uncontrolled Information Spread

**What goes wrong:**
Feedback system reveals private information users shared during dates (sexual orientation, health status, relationship preferences, location, real name if they used pseudonym). Information spreads beyond original context and causes harm.

**Why it happens:**
- Feedback isn't moderated for disclosure of private info
- Assuming: "feedback is just about the date, not about the person"
- No privacy guidelines for feedback content
- Feedback is publicly visible but users haven't consented to have that info public
- System doesn't distinguish between public-facing info and private date conversation

**Consequences:**
- User is outed (sexual orientation, political beliefs, medical status)
- User's location/routine exposed through feedback details
- Harassment/stalking using information from feedback
- Legal liability if platform enables privacy violations
- Users leave platform because it's unsafe

**Prevention:**
1. **Strict content guidelines** (Phase 1):
   - Feedback is about interaction quality, not person's characteristics
   - Forbidden: Names, addresses, phone numbers, workplace, health info, sexual orientation
   - Forbidden: Direct quotes revealing private conversations
   - Only allowed: "This person was [honest/rude/late/polite]"

2. **Automated filtering** (Phase 2):
   - Scan feedback for PII (names, phone numbers, addresses)
   - Scan for keywords that reveal sensitive info ("HIV", "gay", "trans", workplace names)
   - Reject or redact before publishing

3. **User training** (Phase 1):
   - Show what's allowed/forbidden in feedback
   - "Don't reveal: names, locations, medical info, sexual preferences"
   - Example: "Bad: 'He mentioned he has HIV' → Good: 'He was honest and direct'"

4. **Data minimization** (Phase 2):
   - Don't store location info in feedback (already have it from match)
   - Don't store real names in feedback (use IDs)
   - Expire sensitive feedback after 1-2 years

**Detection:**
- User reports: "My personal info was shared in feedback"
- Manual review finds PII in feedback regularly
- Search for keywords (addresses, phone patterns, health terms)

**Phase responsibility:** Phase 1 (content guidelines, user education) + Phase 2 (automation, filtering)

---

### Pitfall 5: System Gaming Through Feedback Inflation/Deflation

**What goes wrong:**
Users figure out how to game reputation:
- Give all dates 5 stars hoping for 5-star feedback back (mutual rating boost)
- Collude with friends: "I'll give you 5 stars, you give me 5 stars"
- Strategic negative feedback to eliminate competition
- Selective feedback timing (give low stars to people you matched but rejected)

**Why it happens:**
- No mechanism to reward *honest* feedback vs. strategic feedback
- Feedback is fungible (all 5-star feedback looks the same)
- No cost to giving dishonest feedback
- Users who game system aren't detected or penalized
- Feedback algorithm treats all data as equally reliable

**Consequences:**
- System becomes useless (everyone is 4.8 stars, ratings are noise)
- Honest feedback gets ignored in sea of inflated ratings
- Bad behavior rewarded (people learn: "be strategic, not honest")
- Trust collapse: "These ratings are fake"

**Prevention:**
1. **Feedback quality signals** (Phase 2):
   - Track feedback accuracy: Does this person's feedback match others' feedback about the same person?
   - Users who give honest/consistent feedback get higher "rater weight"
   - Users who give suspicious feedback (all 5 stars, or all same rating) get flagged

2. **Diversity of feedback required** (Phase 2):
   - If someone gives 50 feedbacks, they should show diversity (not all 5 stars)
   - Algorithm: Expect 15-20% negative, 20-30% neutral, rest positive for unbiased rater
   - Deviation signals gaming

3. **Reciprocity detection** (Phase 2):
   - Flag: Person A gives 5 stars, person B gives 5 stars, happen same day
   - Especially suspicious if feedback text is generic ("great person!")
   - Hold for review or down-weight

4. **Feedback context** (Phase 1):
   - Require feedback to include *specific* comment (not just star rating)
   - Examples: "Was 20 minutes late" (honest) vs. "Great person" (generic/gaming)

5. **Feedback decay** (Phase 2):
   - Recent feedback weighted more than old feedback
   - Older feedback counts less (reduces incentive for gaming years in advance)

**Detection:**
- User A always rates 5 stars (or always same rating)
- Two users consistently give each other 5 stars
- Feedback text is suspiciously generic/positive
- Statistical: Rater's distribution is abnormal vs. population

**Phase responsibility:** Phase 2 (quality signals, detection, weighting)

---

## MAJOR PITFALLS

These cause delays, technical debt, or revenue impact but aren't existential.

### Pitfall 6: False Negatives in Abuse Detection

**What goes wrong:**
System misses real abuse because it only flags explicit slurs or all-caps aggression. Subtle harassment slips through: "No one will date you" (demoralizing but not slur), "You'll never find someone" (not explicit), pattern of "you're boring" from multiple accounts (coordinated but individually mild).

**Why it happens:**
- Keyword-based filtering (blocks obvious slurs but misses subtlety)
- Don't check patterns across multiple feedbacks
- Humans can't review all feedback (volume problem)
- ML models trained on obvious abuse might miss covert harassment

**Consequences:**
- User experiences harassment campaign they can't prove to system
- User gets isolated (feedback is demoralizing but system says it's OK)
- Platform gets bad reputation ("allows harassment")
- Vulnerable users at risk

**Prevention:**
1. **Pattern-based detection** (Phase 2):
   - Flag: Same user receives 10+ negative feedbacks in 1 week (even if individually mild)
   - Flag: Multiple new accounts all giving negative feedback to same target
   - Escalate to human review

2. **Contextual ML** (Phase 3):
   - Train model on real harassment examples (not just slurs)
   - Include: aggressive language, isolation tactics, demoralizing feedback
   - Model learns to detect tone, not just keywords

3. **User reporting** (Phase 1):
   - Simple flag: "This feedback feels like harassment"
   - Collect reports, identify patterns humans missed
   - Act on patterned reports

4. **Structured feedback** (Phase 1):
   - Removing free text feedback reduces subtle harassment opportunities
   - Make feedback about specific behaviors, not character attacks

**Detection:**
- User reports: "I'm being harassed via feedback"
- Pattern analysis: One user has unusually high negative feedback rate
- Manual review finds 20 mean feedbacks that individually passed filter

**Phase responsibility:** Phase 1 (user reporting) + Phase 2 (pattern detection)

---

### Pitfall 7: False Positives & Innocent Users Locked Out

**What goes wrong:**
System flags innocent feedback as abuse/gaming and removes it. Or blocks user from giving feedback because algorithm thinks they're gaming. Users can't appeal because decision is opaque. Reputation becomes meaningless if legitimate feedback is rejected.

**Why it happens:**
- Overly aggressive abuse/gaming filters
- No human review before removing feedback
- Automated moderation errors
- Users can't explain context (why they gave that rating)

**Consequences:**
- Innocent user banned from feedback system
- Legitimate feedback removed unfairly
- Users lose trust in moderation
- System becomes less useful (good data removed)

**Prevention:**
1. **Appeal process** (Phase 2):
   - If feedback removed: User can request review with explanation
   - Human reviewer sees removed feedback + user's context
   - Transparent decision: why was it removed?

2. **Graduated response** (Phase 2):
   - Don't immediately remove feedback
   - First: Flag for review, give user chance to edit
   - Second: Remove with notification and right to appeal
   - Only ban user after repeated violations

3. **Explainable moderation** (Phase 2):
   - If you remove feedback, tell user why: "This contains PII" vs. "This appears to be gaming"
   - Let user fix it instead of deleting

**Detection:**
- User reports: "My feedback was unfairly removed"
- Metrics: X% removal rate seems high
- Appeals: Users consistently win appeals (= system was wrong)

**Phase responsibility:** Phase 2 (appeal process, graduated response)

---

### Pitfall 8: Power Imbalance & Coercion

**What goes wrong:**
Person with more social power coerces less powerful person into positive feedback. Or person threatens negative feedback as coercion. Examples:
- "Give me 5 stars or I'll give you 1 star"
- Popular person pressures date: "Good feedback will help me"
- Implicit threat: "I know where you work" + negative feedback

**Why it happens:**
- No way to detect/prevent pre-feedback coercion (happens via text/outside platform)
- Feedback system enables coercion (negative feedback has power)
- Power dynamics from the date itself carry into feedback

**Consequences:**
- Victim feels pressured, gives false positive feedback
- System data becomes corrupted (can't tell honest from coerced)
- Psychological harm to victim
- Trust in system decays

**Prevention:**
1. **Feedback independence** (Phase 1):
   - Strong privacy: Never show someone who gave feedback about them
   - One-way feedback: A gives feedback about B, but B doesn't find out until later (if ever)
   - Consider not showing identity of negative reviewers

2. **User education** (Phase 1):
   - "Feedback should be honest, not influenced by pressure"
   - "If someone pressures you about feedback, report it"
   - Make reporting easy

3. **Coercion detection** (Phase 2):
   - Monitor for threats in chat messages
   - Flag: Messages + feedback pattern suggests coercion
   - Example: "Give me good feedback or..." followed by rating spike

4. **Victim support** (Phase 2):
   - Users can report: "I was coerced into this feedback"
   - Allow feedback withdrawal if coercion proven
   - Consider protecting victim by removing feedback

**Detection:**
- User reports: "I was pressured into giving this feedback"
- Chat analysis: Messages contain threats before feedback given
- Reputation pattern: Sudden spike upward after message pattern

**Phase responsibility:** Phase 1 (privacy, education) + Phase 2 (detection, support)

---

### Pitfall 9: Missing Bad Actors (False Negatives in Vetting)

**What goes wrong:**
Person with history of harassment/abuse creates account, passes Face ID check, and continues harassment on your platform. Face ID blocks *obvious* fake accounts but not someone with real identity + bad intentions.

**Why it happens:**
- Face ID authenticates identity, not character
- No connection between your platform and other platforms (doesn't know if person is banned elsewhere)
- No behavioral screening at signup
- Assumes: "If they have real face ID, they'll behave"

**Consequences:**
- Victim is harassed by person who should have been flagged
- Platform liability: "You knew they were dangerous"
- Victim leaves platform, trusts are broken
- Bad reputation: "This platform doesn't protect users"

**Prevention:**
1. **Cross-platform reputation** (Phase 2-3):
   - If available: Check if person is banned on other platforms
   - Integrate with abuse reporting databases (RAINN, etc.) if privacy allows
   - Flag: Person has pattern of reports on other apps

2. **Early behavior screening** (Phase 2):
   - First 20 interactions are monitored
   - Flag aggressive/disrespectful language early
   - Warn person before they get banned

3. **User feedback loop** (Phase 1):
   - Simple report: "This person harassed me"
   - If 3+ reports for same person → investigation/ban
   - Don't wait for pattern, act on first serious report

4. **Chat monitoring** (Phase 2):
   - Scan messages for threats, abuse patterns
   - Flag: "I know where you live" or similar threats
   - Immediate action: warn/ban

**Detection:**
- User reports: "This person is harassing me and they've done it before"
- Multiple reports for same user
- Escalation pattern: Warnings ignored, user continues harmful behavior

**Phase responsibility:** Phase 1 (user reporting, early warnings) + Phase 2 (cross-platform checks, monitoring)

---

## MODERATE PITFALLS

These cause friction but aren't blockers.

### Pitfall 10: Poor Feedback Interpretation

**What goes wrong:**
Feedback is vague and users interpret it differently. "Not my type" could mean appearance or personality or politics. User receives 10 feedbacks saying "not my type" and can't improve because feedback is too abstract.

**Why it happens:**
- Free-form text feedback allows ambiguity
- Feedback giver doesn't structure their thoughts
- System allows 1-star with no comment

**Prevention:**
- Structured feedback (required categories)
- Comments required for low ratings
- Question templates: "What didn't click?" with predefined answers

**Detection:**
- Users report confusion about feedback
- Low engagement with feedback (people don't read it)

**Phase responsibility:** Phase 1 (structured feedback)

---

### Pitfall 11: Reputation Staleness

**What goes wrong:**
Someone who was rude 2 years ago still has low reputation even though they've improved. Old feedback dominates rating and person can't recover.

**Why it happens:**
- Feedback weighted equally regardless of age
- No redemption pathway

**Prevention:**
- Decay old feedback over time
- Allow reputation recovery: Positive feedback in recent months increases weight
- Show trend: "Improving" badge if recent feedback better than old

**Detection:**
- User reports: "That feedback is old, I've changed"
- Reputation trend stagnates despite recent positive feedback

**Phase responsibility:** Phase 2 (weighting, trends)

---

### Pitfall 12: Visibility Asymmetry

**What goes wrong:**
Person A can see feedback they received, but can't see feedback they *gave*. Or sees it only partially. Creates confusion and prevents accountability for honest/dishonest feedback.

**Why it happens:**
- Privacy model unclear (trying to protect giver)
- Technical: Different visibility for givers vs. receivers

**Prevention:**
- Clarity: "You can see feedback you gave and received"
- Consistent visibility rules applied fairly

**Detection:**
- User confusion about what others see
- Support requests about visibility

**Phase responsibility:** Phase 1 (UX/design clarity)

---

## PHASE-SPECIFIC WARNINGS

| Phase | Topic | Likely Pitfall | Mitigation |
|-------|-------|----------------|-----------|
| **Phase 1: Feedback Basics** | Consent architecture | Launching without two-party consent → consent violations | Require explicit consent flow before any feedback goes public |
| | Structured feedback | Free-form text only → enables bias & harassment | Mandatory category-based + comment feedback |
| | Account maturity | Any age account can feedback → enables Sybil | Require 48h account age + message exchange before feedback |
| | Privacy guidelines | No PII filtering → privacy violations | Publish strict content rules, train users |
| | Rate limiting | No limits → spam/gaming | Max 1 feedback per match, cooldown periods |
| | User education | Users don't understand consent → conflicts | Clear docs on what's allowed, examples |
| **Phase 2: Quality & Safety** | Abuse detection | Keyword filtering only → subtle harassment misses | Add pattern detection, user reporting, manual review queue |
| | Sybil detection | No coordination checking → coordinated attacks | Monitor IP/location clusters, similar feedback patterns |
| | Bias monitoring | No visibility → disparate impact invisible | Track feedback by demographic, public reporting |
| | Feedback weighting | All feedback equal → gaming wins | Weight by rater history, diversity, account age |
| | Appeal process | No recourse → users lose trust | Transparent moderation with appeal rights |
| | Chat monitoring | Threats in messages + bad feedback = coercion | Scan messages for abuse patterns, link to feedback |
| **Phase 3+: Advanced** | ML moderation | Basic filters insufficient → misses abuse | Train contextual models on real harassment data |
| | Cross-platform reputation | No integration → known bad actors return | Connect to abuse databases, other platforms (if possible) |
| | Feedback trends | Single snapshot → misses recovery | Show trending, decay, redemption pathways |

---

## SUMMARY: Prevention Strategy by Phase

### Phase 1: Consent, Education, Safety Foundations
**Goal:** Build system that can't violate consent, educates users, has basic rate limiting

- Explicit two-party consent before feedback published
- Structured feedback (categories + comments)
- Strict privacy/PII guidelines with user education
- 48h account maturity requirement
- Rate limiting (1 feedback per match, cooldowns)
- Simple user reporting for abuse

### Phase 2: Detection, Moderation, Fairness
**Goal:** Detect gaming, abuse, bias; create moderation workflows

- Pattern-based Sybil detection (coordinate attacks)
- Bias monitoring by demographic
- Feedback weighting by rater quality
- Chat monitoring for threats
- Appeal process for moderation
- Manual review queue for flagged content

### Phase 3+: Intelligence, Recovery, Optimization
**Goal:** Smart systems for reputation recovery, emerging abuse patterns

- ML-based contextual abuse detection
- Cross-platform reputation checks
- Feedback decay & trend analysis
- Redemption pathways (old feedback gets less weight)
- Advanced ML for false positive/negative reduction

---

## Regulatory & Legal Context (2025)

**TAKE IT DOWN Act (May 2025):**
- Criminalizes non-consensual intimate imagery
- Platforms must remove within 48 hours of notice
- **Your system implication:** Must scan feedback for intimate images, have removal process, log consent

**EFF & Advocacy (2025):**
- Platforms should require explicit consent for all feedback
- Privacy-by-default for user data shared during dates
- Transparent moderation with appeal rights
- **Your system implication:** Consent model is foundational, not optional

**Match Group Investigations (2025):**
- Dating platforms held liable for predictable harm
- Known bad actors not removed
- Safety promises ignored
- **Your system implication:** Take abuse reports seriously, act on patterns, don't ignore warnings

---

## Sources

**Consent & Privacy (TAKE IT DOWN Act, 2025):**
- [The TAKE IT DOWN Act: Federal Law on Nonconsensual Intimate Imagery](https://www.congress.gov/crs-product/LSB11314)
- [StopNCII.org - Technology Partnership](https://stopncii.org/)
- [EFF: Dating Apps Need to Learn How Consent Works](https://www.eff.org/deeplinks/2025/07/dating-apps-need-learn-how-consent-works)
- [Take It Down Act Enforcement Details](https://www.skadden.com/insights/publications/2025/06/take-it-down-act)

**Abuse & Safety (Match Group Investigation, 2025):**
- [Global Investigative Journalism Network: Systemic Failures Enabling Abuse on Dating Apps](https://gijn.org/stories/investigating-systemic-failure-enabling-abuse-dating-apps/)
- [NPR: Match Group Slow to Weed Out Predators](https://www.npr.org/2025/02/21/nx-s1-5301046/match-group-dating-app-tinder-hinge-assault-cases-investigation)
- [The Markup: Dating App Cover-Up Investigation](https://themarkup.org/investigations/2025/02/13/dating-app-tinder-hinge-cover-up)
- [Study: 75% of Dating Apps are Unsafe](https://www.globenewswire.com/news-release/2025/09/03/3143762/0/en/75-of-dating-apps-are-unsafe-new-study-find.html)

**Reputation Gaming & Sybil Attacks:**
- [Identity Management Institute: Sybil Attack Risks](https://identitymanagementinstitute.org/sybil-attack-risks-and-solutions/)
- [Survey of Sybil Attacks in Social Networks (Academic)](https://arxiv.org/pdf/1504.05522)
- [Game Theoretical Defense Against Reputation-Based Sybil Attacks](https://www.sciencedirect.com/science/article/pii/S1877050920307651)

**Review Bombing & Coordinated Attacks:**
- [Minclaw: Stop Review Bombing Attacks - Legal Guide](https://www.minclaw.com/review-bombing/)
- [Erase: Google Review Bombing & Extortion 2026](https://www.erase.com/how-to-stop-google-review-extortion-and-review-bombing-in-2026/)
- [Thrive Agency: Identify, Report and Recover From Review Bombing](https://thriveagency.com/news/how-to-identify-report-and-recover-from-review-bombing/)
- [CX Dive: Politically Motivated Review Bombing Harms Customer Journeys](https://www.customerexperiencedive.com/news/political-review-bombing-customer-journey/723207/)

**Bias & Fairness:**
- [SwipeTogether: Bias and Fairness in Dating Apps 2025](https://swipetogether.com/blog/bias-and-fairness-in-dating-apps)
- [Carnegie Mellon: Popularity Bias in Dating Apps](https://www.cmu.edu/tepper-news/news/stories/2023/november/popularity-bias-dating-apps.html)
- [FAIR-MATCH: Multi-Objective Framework for Bias Mitigation](https://arxiv.org/html/2507.01063v1)
- [ACM: Unmasking Gender Bias in Recommendation Systems 2025](https://dl.acm.org/doi/10.1145/3696410.3714528)

**Online Harassment & Moderation:**
- [PEN America: Treating Online Abuse Like Spam (2025 Report)](https://pen.org/report/treating-online-abuse-like-spam/)
- [Consumer Reports: Digital Harassment - New 2025 Tools Report](https://innovation.consumerreports.org/new-report-digital-harassment-treating-online-abuse-like-spam/)
- [TechPolicy.Press: Tools for Reporting Online Violence Are Broken](https://www.techpolicy.press/tools-for-reporting-online-violence-are-broken-heres-how-to-fix-them/)

**Moderation & False Positives:**
- [Redact.dev: Expect More Negative Feedback on Social Media 2025](https://redact.dev/blog/expect-more-negative-feedback-social-media-2025)
- [San Diego Law: AI Detectors - False Positives and False Negatives](https://lawlibguides.sandiego.edu/c.php?g=1443311&p=10721367)
- [SEON: Strategies to Reduce False Positives in Fraud Prevention](https://trustdecision.com/resources/blog/strategies-reduce-false-positives-fraud-prevention)

**Information Asymmetry & Algorithms:**
- [Photofeeler: How Dating App Algorithms Really Work 2025](https://blog.photofeeler.com/dating-app-algorithms/)
- [Medium: Dating Apps Changing How We Think About User Matching Algorithms](https://medium.com/@sohail_saifi/how-dating-apps-are-changing-how-we-think-about-user-matching-algorithms-eac1101d5d9d)
- [Power Dynamics Research: Isolation, Control, and Dependency](https://publichealth.gmu.edu/news/2025-06/power-dynamics-role-isolation-control-and-dependency-intimate-partner-abuse)

---

**Confidence Assessment:**

| Area | Confidence | Reason |
|------|------------|--------|
| **Consent violations** | HIGH | TAKE IT DOWN Act (federal law 2025), widespread platform liability |
| **Sybil attacks & gaming** | HIGH | Well-documented research, current blockchain/Web3 mitigation efforts |
| **Bias in feedback** | HIGH | Academic research (CMU, ACM 2025), platform fairness audits (Hinge, Bumble) |
| **Privacy violations** | HIGH | Federal legislation, RAINN data, multiple platforms caught violating |
| **Abuse detection gaps** | MEDIUM | PEN America report 2025, but specific moderation tech varies by platform |
| **Coercion & power dynamics** | MEDIUM | Research on intimate partner abuse + feedback systems, but less dating-specific data |
| **Cross-platform integration** | MEDIUM | Sybil resistance frameworks exist but dating platform adoption unclear |

