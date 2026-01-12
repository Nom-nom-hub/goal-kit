# Goal Alignment Guide

*How to ensure all goals connect to organizational vision and strategy.*

---

## Overview

Goal alignment ensures every goal your organization pursues serves strategic objectives. Without alignment, teams work on disconnected initiatives—killing velocity and focus.

This guide shows how to create and maintain alignment from vision → goals → execution.

---

## The Alignment Stack

```
Organization Vision
  ↓ defines
Strategic Pillars (3-5 major areas)
  ↓ enable
3-Year Objectives (where we want to be)
  ↓ achieved by
Quarterly OKRs (focused bets for the quarter)
  ↓ driven by
Individual Goals (1-4 month initiatives)
  ↓ measured by
Success Criteria (metrics that prove achievement)
```

**Each level connects to the one above it.**

---

## Step 1: Create Organization Vision

**See**: `templates/org-vision-template.md`

### What Belongs in Vision
- **Mission**: Why does the organization exist?
- **Values**: What principles guide how we work?
- **Strategic Pillars**: 3-5 major areas where you invest long-term
- **3-Year Objectives**: Where do you want to be in 3 years?
- **Success Metrics**: How do you know you're progressing?
- **Guiding Principles**: How do you approach work?

### Common Mistakes
- ❌ Vision is too generic ("be the best") - Make it specific and measurable
- ❌ Vision changes every month - Revisit annually, not constantly
- ❌ Vision isn't visible - Share it with every new goal owner
- ❌ Vision has 10+ strategic pillars - Keep to 3-5, or goals get diffuse

### How to Create It
1. Gather leadership team for half-day workshop
2. Draft mission statement (2-3 sentences)
3. Define 4-5 core values with behavioral examples
4. Identify 3-5 strategic pillars (things you'll invest in for 3+ years)
5. For each pillar, write 3-year vision (what does success look like?)
6. Define 3-year organizational objectives (measurable outcomes)
7. Set success metrics (track progress toward 3-year vision)
8. Finalize guiding principles (how you operate)
9. Share widely and update quarterly

---

## Step 2: Connect Goals to Strategic Pillars

**See**: `templates/goal-alignment-template.md`

### The Question
*Which of our strategic pillars does this goal advance?*

### Why It Matters
- Prevents scattered execution on non-strategic work
- Ensures resource allocation matches strategy
- Makes portfolio management easier
- Helps rejected goal owners understand "why not"

### How to Do It

**For each new goal**, ask:

1. **Which pillar?** - Does this goal clearly support one of our 3-5 strategic pillars?
   - ✅ "Mobile App Development" → Strategic Pillar "Product Innovation"
   - ✅ "CI/CD Improvement" → Strategic Pillar "Operational Efficiency"
   - ❌ "Clean up code comments" → No clear pillar (wrong level)

2. **Why that pillar?** - Articulate the connection in 1-2 sentences
   - Example: "This goal advances Product Innovation by enabling faster feature development through improved deployment velocity"

3. **Which 3-year objectives?** - What 3-year outcomes does this help achieve?
   - Multiple connections are fine (goal can support multiple objectives)

4. **Missing alignment?** - If the goal doesn't clearly fit:
   - **Option A**: Clarify the goal to connect it to a pillar
   - **Option B**: Reject the goal as off-strategy
   - **Option C**: Expand strategic pillars (rare—do quarterly at most)

### Template in Action

```markdown
# Goal: Real-Time Collaboration Features

## Strategic Alignment
**Selected Pillar**: Product Excellence

**Pillar Vision**: Build software customers love and competitors envy

**How This Goal Advances It**: 
Real-time collaboration is #1 customer request. Shipping this enables faster feature adoption 
and improves competitive differentiation in the market.

## 3-Year Objectives Supported
1. Deploy 20+ major features with >90% adoption → (This is feature 3 of 20)
2. Achieve 4.5+ app store rating → (Collaboration directly improves rating)
```

---

## Step 3: Create Quarterly OKRs

**See**: `templates/okr-template.md`

### What OKRs Represent
- **Objectives**: Qualitative outcomes we want to achieve this quarter
- **Key Results**: 3-4 measurable proof points for each objective

### Example OKR Structure

```
Objective: Become the fastest shipping product in our category
  KR 1.1: Ship 5 major features
  KR 1.2: Achieve >90% adoption of new features
  KR 1.3: Reduce feature cycle time from 8 weeks to 4 weeks

Objective: Build industry-leading team
  KR 2.1: Hire 3 senior engineers
  KR 2.2: Achieve 85+ eNPS (employee satisfaction)
  KR 2.3: Complete skill development for 20+ engineers
```

### How to Create OKRs
1. Start with 3-year objectives from vision
2. Pick 3-5 for **this quarter** (focused!)
3. For each quarterly objective, define 3-4 measurable key results
4. Ensure each KR is aspirational (70-80% confidence, not 100%)
5. Assign owner to each KR (who reports progress?)

### OKR Mistakes to Avoid
- ❌ Too many OKRs (5+ = can't focus) - Keep to 3-5 per quarter
- ❌ KRs that are tasks, not outcomes ("Write documentation") - Outcomes only
- ❌ 100% confidence on all KRs - Should be 70-80% confident (stretch goals)
- ❌ OKRs with no goals mapping - OKRs without execution die on the vine

---

## Step 4: Map Individual Goals to OKRs

**See**: `templates/okr-mapping-template.md`

### The Question
*Which KRs does this goal help achieve?*

### Why It Matters
- Every goal knows its strategic value
- Portfolio leaders understand cross-dependencies
- At quarter end, you can measure real business impact

### How to Do It

**For each goal in a quarter:**

1. **Identify supporting KRs** - Which OKR KRs does this goal contribute to?
   - Goal supports 1-3 KRs (not more)
   - Multiple goals can support same KR (good - more assurance)

2. **Define contribution %** - What % of the KR does this goal represent?
   - "This goal is 1 of 5 features (KR 1.1 = Ship 5 features) = 20%"
   - "This goal's success directly impacts KR 1.2 = 40% of adoption gains"

3. **Timeline alignment** - Is the goal completion by the OKR measurement date?
   - ✅ Completed well before EOQ measurement
   - ⚠️ Partial—goal contributes 60% by EOQ, rest next quarter
   - ❌ Goal slips past EOQ—won't measure impact this quarter

4. **Risk to KR** - If this goal fails, what happens to the KR?
   - Critical (KR impossible without goal) = escalate
   - Important (KR harder without goal) = monitor
   - Nice-to-have (KR achievable without goal) = continue as planned

### Template in Action

```markdown
# Goal: Real-Time Collaboration

## OKR Mapping

| OKR | KR | This Goal's Role | Impact % |
|-----|----|----|---|
| Obj 1: Ship 5 features | KR 1.1 | This is feature #2 of 5 | 20% |
| Obj 1: Reduce cycle time | KR 1.3 | Proves 4-week cycle is possible | 100% |

## Confidence
- If this goal succeeds: KR 1.1 and 1.3 are both achievable
- If this goal fails: KR 1.1 drops to 4 features, KR 1.3 becomes harder
- Mitigation: Backup feature (Goal 007) can substitute if needed
```

---

## Step 5: Track Alignment Through Execution

### Weekly Goal Updates
Include alignment section in goal status updates:
- Are we tracking toward OKR? (Yes / Partial / No)
- Any changes to strategic value?
- Risks to achieving the KRs we support?

### Mid-Quarter Check-In
- Which goals are on track for their OKRs?
- Which goals slipping and what's the KR impact?
- Do we need to adjust strategy/goals?

### End-of-Quarter Review
- Did goals achieve their success criteria?
- Did they drive the OKRs we expected?
- What should inform next quarter's OKRs?

### OKR Review Process
1. **Week 1**: Goals check in with final metrics
2. **Week 2**: Tally up KR achievement across supporting goals
3. **Week 3**: Leadership reviews OKR results and discusses Q2
4. **Week 4**: Retrospective - what did we learn? How do we improve?

---

## Special Cases

### Alignment Exceptions
Sometimes goals don't cleanly fit a pillar or OKR. Document the exception:

```markdown
# Goal: Code Cleanup (no clear strategic pillar)

## Misalignment Notes

### Why No Clear Alignment
- This goal is technical debt reduction, not strategic initiative
- Doesn't directly advance a strategic pillar

### Exception Justification
- Infrastructure team can't move fast while saddled with tech debt
- Spending 2 weeks here prevents 10-week delays on Goals 005 and 007
- Critical path blocker removal

### Duration
- One-time exception (not recurring pattern)
- Next time, bundle tech debt into product goals upfront

### Trade-Off
- Pushes lower-priority work (Goal 004) to next quarter
- Trade-off approved by VP Eng
```

### Scaling Across Multiple Teams
When teams operate independently, alignment gets harder. Solution:

1. **Unified Vision** - All teams work to same org vision
2. **Shared OKRs** - Teams choose which OKRs to pursue
3. **Cross-Team Mapping** - Goals can support OKRs across teams
4. **Dependency Management** - Document which teams block others
5. **Portfolio View** - See all goals/OKRs across org

---

## Alignment Checklist

Before launching a goal, verify:

- [ ] **Goal supports a strategic pillar** - Clear which one
- [ ] **Goal advances 3-year objectives** - At least one identified
- [ ] **Goal mapped to OKR(s)** - If in OKR quarter
- [ ] **Timeline makes sense** - Goal completes before measurement date
- [ ] **Values/principles reflected** - Goal approach aligns with how we work
- [ ] **Business case documented** - ROI, customer impact, strategic value clear
- [ ] **Stakeholders aligned** - No surprises; exec sponsor aware
- [ ] **Success criteria connected** - Goal metrics feed org-level metrics where relevant
- [ ] **Misalignments documented** - If any, exception is approved

---

## Common Questions

**Q: Should every goal support an OKR?**  
A: Goals in an OKR quarter should map to OKRs. Some goals are ongoing maintenance (tech debt, security) and don't map to quarterly OKRs. Document why, don't hide it.

**Q: Can one goal support multiple OKRs?**  
A: Yes, if genuinely true. Example: "API redesign" might support both "Ship features faster" (KR 1.1) and "Improve code quality" (KR 3.2). But be honest—not every goal should support 3+ KRs.

**Q: What if a goal doesn't fit any strategic pillar?**  
A: Either:
1. Clarify the goal to fit a pillar
2. Reject it as off-strategy (hard but necessary)
3. Document as one-time exception (tech debt, urgent fixes)

**Q: How often does vision change?**  
A: Rarely. Vision should be stable for 12+ months. Review annually, not monthly. Strategic pillars might shift quarterly; 3-year objectives might evolve based on market, but core vision stays consistent.

**Q: Who decides if a goal is strategic?**  
A: Vision owner (usually CEO/exec) + affected teams. Not every engineer. Not every idea is strategic—and that's okay.

---

## Related Templates

- `templates/org-vision-template.md` - Define vision
- `templates/goal-alignment-template.md` - Align individual goals
- `templates/okr-template.md` - Create quarterly OKRs
- `templates/okr-mapping-template.md` - Map goals to OKRs
- `templates/portfolio-template.md` - See all goals aligned
