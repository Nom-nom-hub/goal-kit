# Goal Kit Quick Reference Card

## 🎯 Core Concept

**Goal-Driven Development** = Focus on **outcomes** (what users achieve) instead of **specifications** (what to build)

---

## 📋 When to Use Each Command

| Situation | Command | Output File |
|-----------|---------|-------------|
| 🆕 Starting new project | `/goalkit.vision` | `.goalkit/vision.md` |
| 🎯 New user outcome to achieve | `/goalkit.goal` | `goals/###-name/goal.md` |
| 🔀 Choosing implementation approach | `/goalkit.strategies` | `goals/###-name/strategies.md` |
| 📊 Planning measurable checkpoints | `/goalkit.milestones` | `goals/###-name/milestones.md` |
| 🛠️ Building the feature | `/goalkit.execute` | `goals/###-name/execution.md` |
| 📈 Tracking progress | `/goalkit.report` | `goals/###-name/report.md` |
| 🔍 Retrospective analysis | `/goalkit.review` | `goals/###-name/review.md` |
| 📚 Capturing insights | `/goalkit.learnings` | `goals/###-name/learnings.md` |
| ✅ Breaking into tasks | `/goalkit.tasks` | `goals/###-name/tasks.md` |

---

## 🔄 Basic Workflow

```
1. Vision → 2. Goal → 3. Strategies → 4. Milestones → 5. Execute → 6. Measure → 7. Review
     ↑                      ↑              ↑              ↑                           |
     └──────────────────────┴──────────────┴──────────────┴───── Feedback Loops ─────┘
```

**Key principle**: Be willing to loop back based on what you learn!

---

## ✅ Success Criteria Checklist

For each success criterion, ensure it's:

- [ ] **Measurable**: Specific number/percentage (not "good" or "fast")
- [ ] **Time-bound**: Clear deadline (by when?)
- [ ] **User-focused**: User outcome, not feature (what users achieve)
- [ ] **Baseline defined**: Current state documented
- [ ] **Achievable**: Realistic given resources

**Example**:
- ❌ Bad: "Users are happy with the feature"
- ✅ Good: "NPS score ≥ 8/10 within 3 months (baseline: 6/10)"

---

## 🎯 Writing Good Goals

### The Formula
```
[User/Business Outcome] + [Measurable Success Criteria] + [Timeframe]
```

### Examples

**❌ Bad (Specification)**:
> Build a REST API with 5 endpoints for user management

**✅ Good (Outcome)**:
> Enable mobile app to sync user data reliably
> - 95% sync success rate
> - <2s sync latency (p95)
> - 90% user satisfaction
> - Within 6 weeks

---

## 🔀 Strategy Exploration Template

Always explore **2-3+ approaches** before choosing:

```
Option 1: [Approach Name]
  Pros: [Benefits]
  Cons: [Tradeoffs]
  Cost: [Time/money]
  Risk: [High/Medium/Low]

Option 2: [Approach Name]
  [Same structure]

Option 3: [Approach Name]
  [Same structure]

Selected: Option [X]
Rationale: [Why chosen, why others rejected]
```

---

## 📊 Milestone Planning Checklist

Each milestone should:

- [ ] **Deliver standalone value**: Can be demonstrated independently
- [ ] **Validate assumptions**: Tests a hypothesis or risk
- [ ] **Be measurable**: Clear success criteria
- [ ] **Build progressively**: Each milestone builds on previous
- [ ] **Front-load risk**: Riskiest assumptions validated first

**Example**:
- M1: Prototype with 5 users (validates UX)
- M2: Backend with real data (validates performance)
- M3: Beta with 50 users (validates adoption)

---

## 🚦 Metric Decision Thresholds

Define what to do based on metric values:

| Zone | Threshold | Action |
|------|-----------|--------|
| 🟢 **Green** | ≥ Target | Continue, scale, celebrate |
| 🟡 **Yellow** | Near target | Investigate, adjust tactics |
| 🔴 **Red** | < Threshold | Pivot strategy or goal |

**Pivot Trigger Example**:
> If metric stays in red zone for 2 weeks → Explore new strategy

---

## 🔄 When to Pivot

```
Check metrics:
├─ All GREEN → Continue current approach
├─ Some YELLOW → Investigate and adjust tactics
└─ RED for [X weeks] → Pivot
   ├─ Tactical pivot: Adjust execution
   ├─ Strategic pivot: Try different strategy
   └─ Goal pivot: Reframe the goal
```

---

## 📚 Common Patterns

### Pattern 1: New Feature
```
Goal (user outcome) → Strategies (3+ options) → 
Milestones (3-5 checkpoints) → Execute → Measure → Review
```

### Pattern 2: Performance Optimization
```
Goal (performance target) → Strategies (profiling) → 
Milestones (incremental improvements) → Execute ↔ Measure (tight loop)
```

### Pattern 3: Exploratory Innovation
```
Goal (learning objective) → Strategies (experiments) → 
Milestones (hypothesis tests) → Execute → Measure → Pivot (rapid)
```

---

## ❌ Common Mistakes to Avoid

1. **Goals that are specs**: Focus on outcomes, not implementation
2. **Unmeasurable criteria**: Use specific numbers, not "good" or "fast"
3. **Skipping strategy exploration**: Always explore 2-3+ options
4. **No baseline metrics**: Measure current state before starting
5. **Milestones without value**: Each should be demonstrable
6. **Not measuring until end**: Measure after each milestone
7. **Refusing to pivot**: Respond to data, don't ignore red metrics
8. **No learnings capture**: Document insights for future goals

---

## 🎓 Decision Trees

### Should I create a new goal?

```
New user outcome? 
  YES → Different metrics than existing goals?
    YES → Create new goal
    NO → Update existing goal
  NO → Implementation detail?
    YES → This is a strategy
    NO → This is a task
```

### Should I explore new strategies?

```
Metrics meeting targets?
  YES → Continue execution
  NO → Why failing?
    Tactical issues → Adjust execution
    Strategy flawed → Explore new strategies
    Goal unrealistic → Reframe goal
```

---

## 📖 Key Principles

1. **Goals Over Specs**: Focus on outcomes, not implementation
2. **Multiple Strategies**: Always explore alternatives
3. **Measurable Success**: Define clear metrics upfront
4. **Adaptive Execution**: Be willing to pivot based on data
5. **Learning Integration**: Treat execution as hypothesis testing

---

## 🚀 Getting Started (5 Minutes)

```bash
# 1. Install
uv tool install --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkeeper-cli

# 2. Initialize
goalkeeper init my-project
cd my-project

# 3. Start with vision
/goalkit.vision

# 4. Define first goal
/goalkit.goal

# 5. Explore strategies
/goalkit.strategies
```

---

## 📊 Metric Types

Ensure balanced measurement across:

- **User Behavior**: How users actually use the feature
- **Business Impact**: Revenue, cost, efficiency gains
- **Technical Quality**: Performance, reliability, scalability
- **Learning**: What we discovered, capabilities built

---

## 🔍 Quality Checks

### Before starting execution:
- [ ] Vision documented and team-aligned
- [ ] Goal defines user outcome (not feature)
- [ ] Success criteria are measurable
- [ ] Baseline metrics captured
- [ ] 2-3+ strategies explored
- [ ] Strategy selected with rationale
- [ ] Milestones deliver standalone value
- [ ] Instrumentation plan ready

### During execution:
- [ ] Measuring metrics continuously
- [ ] Documenting learnings as you go
- [ ] Willing to pivot if needed
- [ ] Regular team reviews

### After completion:
- [ ] All success criteria evaluated
- [ ] Learnings documented
- [ ] Insights applied to next goal

---

## 💡 Pro Tips

1. **Start small**: Begin with one simple goal to learn the methodology
2. **Measure early**: Don't wait until the end to collect metrics
3. **Document learnings**: Use `/goalkit.learnings` after every goal
4. **Front-load risk**: Validate scariest assumptions in M1
5. **Plan onboarding**: Great features need great user education
6. **Set pivot triggers**: Decide upfront when to change course
7. **Review this card**: Check before each phase to avoid mistakes

---

## 📚 Learn More

- **Full Guide**: [Goal-Driven Development](./goal-driven.md)
- **Workflow**: [Workflow Guide](./workflow-guide.md)
- **Mistakes**: [Common Mistakes](./common-mistakes.md)
- **Examples**: [Practical Examples](./examples.md)
- **Quickstart**: [5-Minute Quickstart](./quickstart.md)

---

## 🆘 Need Help?

- **Issues**: [GitHub Issues](https://github.com/Nom-nom-hub/goal-kit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Nom-nom-hub/goal-kit/discussions)
- **Troubleshooting**: [Troubleshooting Guide](./troubleshooting.md)

---

**Print this card and keep it handy while using Goal Kit!**

*Version: Phase 1 (2024) | Part of Goal Kit Methodology*
