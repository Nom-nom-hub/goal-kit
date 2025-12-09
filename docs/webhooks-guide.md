# Webhooks Guide - Event Automation for Goal Kit

## Overview

Webhooks enable Goal Kit to automatically notify external systems when important events occur. Integrate with Slack, Discord, GitHub, Jira, email, or custom APIs.

## When to Use Webhooks

| Use Case | Event | Action |
|----------|-------|--------|
| 📱 Notify team on progress | `task_completed` | Send Slack message |
| 🎉 Celebrate goal completion | `goal_completed` | Post to team chat |
| ⚠️  Alert on deadline risk | `deadline_approaching` | Escalate to manager |
| 🚨 Trigger intervention | `high_risk` | Create urgent ticket |

## Setup Walkthrough

### Step 1: Choose Your Platform

**Slack** (recommended for teams):
```bash
# Go to: https://api.slack.com/messaging/webhooks
# Create Incoming Webhook
# Copy webhook URL
```

**Discord**:
```bash
# Server Settings → Integrations → Webhooks
# Create Webhook
# Copy Webhook URL
```

**Custom API** (for internal systems):
```bash
# Deploy webhook consumer at your API
# Can be anything: Node.js, Python, Go, etc.
# Must accept POST requests with JSON payload
```

### Step 2: Register with Goal Kit

**Slack**:
```bash
/goalkit.webhooks add https://hooks.slack.com/services/T000/B000/XXXX \
  --events task_completed,goal_completed,deadline_approaching
```

**Discord**:
```bash
/goalkit.webhooks add https://discordapp.com/api/webhooks/123/ABC \
  --events goal_completed,high_risk
```

**Custom API**:
```bash
/goalkit.webhooks add https://api.company.com/goalkit \
  --events goal_completed,high_risk,deadline_approaching \
  --secret my-secret-key-12345
```

### Step 3: Test It Works

```bash
# Send test event to your webhook
/goalkit.webhooks test wh_abc123def456

# Check: Did you receive the test event?
# - Slack: Message in channel
# - Discord: Embed in channel
# - Custom API: Check your logs
```

### Step 4: Verify in Production

```bash
# Monitor webhook deliveries
/goalkit.webhooks events --webhook wh_abc123def456

# Expected: Events showing as ✅ DELIVERED
```

## Event Types

### task_completed

**When**: Every time a task is marked complete

**Payload**:
```json
{
  "event": "task_completed",
  "goal_id": "001",
  "goal_name": "Improve API Performance",
  "task_id": "task-abc123",
  "task_name": "Implement caching layer",
  "timestamp": "2025-01-15T14:32:45Z"
}
```

**Use Cases**:
- Real-time progress notifications
- Daily stand-up summaries (aggregate events)
- Task completion milestones

**Slack Message Example**:
```
✅ Task Completed
Goal: Improve API Performance
Task: Implement caching layer
Time: 2025-01-15 14:32 UTC
```

---

### goal_completed

**When**: Goal reaches 100% completion (all milestones done)

**Payload**:
```json
{
  "event": "goal_completed",
  "goal_id": "001",
  "goal_name": "Improve API Performance",
  "completion_time_days": 32,
  "velocity_avg": 3.2,
  "timestamp": "2025-01-15T16:45:00Z"
}
```

**Use Cases**:
- Celebration announcements
- Trigger next-phase automation
- Launch new goal
- Formal reporting

**Slack Message Example**:
```
🎉 Goal Completed!
Goal: Improve API Performance
Duration: 32 days
Average Velocity: 3.2 tasks/week

Team: Great work! Ready for the next goal?
```

---

### deadline_approaching

**When**: Goal deadline is within 7 days

**Payload**:
```json
{
  "event": "deadline_approaching",
  "goal_id": "001",
  "goal_name": "Improve API Performance",
  "deadline": "2025-01-20",
  "days_remaining": 5,
  "tasks_remaining": 4,
  "velocity_required": 0.8,
  "velocity_current": 0.6,
  "timestamp": "2025-01-15T09:00:00Z"
}
```

**Use Cases**:
- Escalate urgency to stakeholders
- Check if deadline still feasible
- Trigger scope reduction if needed
- Organize crunch-mode effort

**Slack Message Example**:
```
⏰ Deadline Approaching
Goal: Improve API Performance
Days Left: 5
Tasks Remaining: 4
Status: ⚠️  Behind pace (need 0.8 tasks/day, have 0.6)

Action: Escalate if can't accelerate
```

---

### high_risk

**When**: Analytics detect at-risk status (unlikely to hit deadline at current pace)

**Payload**:
```json
{
  "event": "high_risk",
  "goal_id": "001",
  "goal_name": "Improve API Performance",
  "risk_level": "critical",
  "days_to_deadline": 10,
  "tasks_remaining": 8,
  "days_remaining_available": 10,
  "velocity_required": 0.8,
  "velocity_current": 0.4,
  "blockers": [
    {
      "task": "Backend optimization",
      "blocked_by": "Infrastructure team",
      "days_blocked": 3
    }
  ],
  "recommendation": "Reduce scope or extend deadline",
  "timestamp": "2025-01-15T14:00:00Z"
}
```

**Use Cases**:
- Immediate escalation to management
- Trigger emergency project reviews
- Create urgent action items
- Prevent deadline misses

**Slack Message Example**:
```
🚨 Goal at Risk
Goal: Improve API Performance
Risk Level: CRITICAL
Days Left: 10
Tasks Left: 8

Problem: Need 0.8 tasks/day, averaging 0.4
Blocker: Infrastructure team (3 days delay)

Action Required: Scope reduction OR deadline extension
```

---

## Integration Examples

### Slack - Daily Progress Summary

**Goal**: Notify team daily at 9am with progress update

**Setup**:
```bash
# 1. Create Slack Incoming Webhook for #goals channel
# 2. Register with Goal Kit
/goalkit.webhooks add [SLACK_WEBHOOK_URL] \
  --events task_completed,deadline_approaching,high_risk

# 3. Custom integration (create daily aggregator)
#    Your webhook consumer:
#    - Receives events as they occur
#    - Aggregates task_completed events
#    - At 9am, sends summary to Slack
```

**Example Daily Summary**:
```
📊 Daily Progress Update - Jan 15
═════════════════════════════════
✅ 4 tasks completed today
📈 Velocity: 3.2 tasks/week
🎯 Goal: Improve API Performance (67% done)
⏰ On track for Jan 22 completion
```

---

### Discord - Celebration on Completion

**Goal**: Post celebration when goal completes

**Setup**:
```bash
# 1. Create Discord webhook in #wins channel
# 2. Register with Goal Kit
/goalkit.webhooks add [DISCORD_WEBHOOK_URL] \
  --events goal_completed
```

**Example Message**:
```
🎉🎉🎉 GOAL COMPLETED! 🎉🎉🎉

📌 Goal: Improve API Performance
⏱️  Duration: 32 days
📈 Velocity: 3.2 tasks/week
✅ All success criteria met

Team: Fantastic work! Celebrate!
Next: Starting new goal on Jan 16
```

---

### GitHub - Create Issue on High Risk

**Goal**: Automatically create urgent issue when risk detected

**Setup**:
```bash
# 1. Create GitHub webhook consumer (can use Actions)
# 2. Register with Goal Kit
/goalkit.webhooks add https://api.github.com/repos/myorg/myrepo/webhooks \
  --events high_risk

# 3. Webhook consumer code (Python example):
from flask import Flask, request
import hmac
import hashlib
import requests

def verify_signature(body, signature, secret):
    expected = 'sha256=' + hmac.new(
        secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    return signature == expected

@app.route('/goalkit-webhook', methods=['POST'])
def handle_webhook():
    signature = request.headers.get('X-Goalkit-Signature')
    body = request.get_data()
    
    if not verify_signature(body, signature, SECRET):
        return 'Unauthorized', 401
    
    event = request.json
    if event['event'] == 'high_risk':
        # Create GitHub issue
        issue = {
            'title': f"🚨 {event['goal_name']} at Risk",
            'body': f"""
Goal: {event['goal_name']}
Risk: {event['risk_level']}
Days left: {event['days_to_deadline']}
Velocity needed: {event['velocity_required']}
Velocity current: {event['velocity_current']}

Recommendation: {event['recommendation']}
            """
        }
        requests.post(
            f"https://api.github.com/repos/myorg/myrepo/issues",
            json=issue,
            headers={'Authorization': f'token {GITHUB_TOKEN}'}
        )
    
    return 'OK', 200
```

---

### Email - Deadline Reminder

**Goal**: Email manager when deadline is 7 days away

**Setup**:
```bash
# 1. Create email service webhook (SendGrid, Mailgun, etc.)
# 2. Register with Goal Kit
/goalkit.webhooks add https://api.sendgrid.com/v3/mail/send \
  --events deadline_approaching

# 3. Consumer handles deadline_approaching events
#    Sends: "Goal XYZ deadline in 7 days, verify feasibility"
```

---

### Custom API - Multi-Action Workflow

**Goal**: Complex orchestration on goal completion

**Setup**:
```bash
# 1. Deploy webhook consumer
/goalkit.webhooks add https://company-automation.internal/goalkit \
  --events goal_completed \
  --secret automation-secret-12345

# 2. Consumer implements multi-step workflow
def handle_goal_completed(event):
    goal = event['goal_name']
    
    # 1. Post to team Slack
    slack.post(f"Goal completed: {goal}")
    
    # 2. Update project dashboard
    dashboard.update_goal_status(event['goal_id'], 'completed')
    
    # 3. Archive goal folder
    drive.archive(f"goals/{event['goal_id']}")
    
    # 4. Create retrospective template
    confluence.create_page('Learnings', goal)
    
    # 5. Trigger next phase
    start_next_phase(event['goal_id'])
    
    return {'status': 'success'}
```

---

## Webhook Payload Verification

### Why Verify?

Ensures events came from Goal Kit, not attacker impersonating Goal Kit.

### How to Verify

Every webhook includes `X-Goalkit-Signature` header:

```
X-Goalkit-Signature: sha256=abc123def456...
```

**Verification code** (Python):

```python
import hmac
import hashlib

def verify_webhook(body_bytes, signature_header, secret):
    """Verify X-Goalkit-Signature header"""
    
    # Calculate expected signature
    expected = 'sha256=' + hmac.new(
        secret.encode('utf-8'),
        body_bytes,
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures
    return signature_header == expected
```

**Usage in Flask**:

```python
from flask import Flask, request
import json

@app.route('/goalkit', methods=['POST'])
def webhook():
    # 1. Get signature from header
    signature = request.headers.get('X-Goalkit-Signature')
    if not signature:
        return 'Missing signature', 401
    
    # 2. Get raw body
    body = request.get_data()
    
    # 3. Verify
    if not verify_webhook(body, signature, WEBHOOK_SECRET):
        return 'Invalid signature', 401
    
    # 4. Parse and process
    event = json.loads(body)
    handle_event(event)
    
    return 'OK', 200
```

---

## Troubleshooting

### Webhook Not Receiving Events

**Checklist**:
```bash
# 1. Verify webhook is registered and active
/goalkit.webhooks list
# Status should be: ✅ ACTIVE

# 2. Verify correct event types are subscribed
/goalkit.webhooks types
# Ensure the event type that should fire is registered

# 3. Send test event
/goalkit.webhooks test wh_abc123
# Did you receive it? If yes, issue is specific events not firing

# 4. Check event history
/goalkit.webhooks events --webhook wh_abc123
# Are there any events? If not, no goals/tasks matching trigger
```

### Webhook Disabled After Failures

**Issue**: Status shows ❌ DISABLED

**Cause**: 10 consecutive delivery failures

**Solution**:
```bash
# 1. Check what failed
/goalkit.webhooks events --webhook wh_abc123 --limit 10
# Look at last entries for errors

# 2. Fix the problem
# Common issues:
#   - URL changed or domain down
#   - Authentication token expired
#   - IP whitelist blocking us
#   - Request timeout (endpoint too slow)

# 3. Test again
/goalkit.webhooks test wh_abc123

# 4. Re-enable if test passes
/goalkit.webhooks enable wh_abc123
```

### Signature Verification Failing

**Problem**: X-Goalkit-Signature doesn't match

**Cause**: Incorrect secret or body encoding

**Fix**:
```python
# ❌ WRONG: Using request.json (parses then serializes differently)
body = json.dumps(request.json)  # Different order/format!

# ✅ RIGHT: Using raw request body
body = request.get_data()  # Exact bytes received

# Verify with exact secret from registration
expected = 'sha256=' + hmac.new(
    WEBHOOK_SECRET.encode('utf-8'),  # Exact secret
    body,                              # Exact bytes
    hashlib.sha256
).hexdigest()
```

---

## Pro Tips

1. **Start with Slack** - Easiest to set up and test
2. **Test immediately** - Use `webhooks test` after adding
3. **Monitor regularly** - Check `webhooks events` weekly
4. **Verify signatures** - Always verify X-Goalkit-Signature in production
5. **Plan for failures** - Implement retry logic in your consumer
6. **Log everything** - Store webhook requests/responses for audit trail
7. **Start with one event** - Add more events after proving one works

## See Also

- [Webhooks Command Reference](../templates/commands/webhooks.md) - All webhook commands
- [Analytics Guide](./analytics-guide.md) - Understanding what triggers high_risk events
- [Forecast Command](../templates/commands/analytics.md#goalkitforecast) - deadline_approaching trigger
