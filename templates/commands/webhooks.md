---
description: Set up automated event notifications and integrations with external systems (Slack, Discord, GitHub, Jira, email) for task completions, goal achievements, deadline alerts, and risk detection.
handoffs:
  - label: Manage Webhooks
    agent: goalkit.webhooks
    prompt: Manage webhook configuration for the project
    send: true
scripts: {}
---

# Webhooks Command Guide

## Purpose

Use `/goalkit.webhooks` commands to set up automated event notifications and integrations when important project events occur (tasks completed, goals achieved, deadlines approaching, risks detected).

Enable integration with external systems (Slack, Discord, GitHub, Jira, email, custom APIs) for real-time notifications.

## When to Use

| Situation | Action | Frequency |
|-----------|--------|-----------|
| 🔔 Want Slack notifications on task completion | `webhooks add` | Once per project |
| 📱 Notify team of deadline approaching | `webhooks add` | Once per project |
| ⚠️ Alert on high-risk detection | `webhooks add` | Once per project |
| 🧪 Test webhook configuration | `webhooks test` | Before going live |
| 📋 Check registered webhooks | `webhooks list` | Weekly |
| 🗑️ Remove old/broken webhooks | `webhooks remove` | As needed |
| 📊 Review webhook delivery history | `webhooks events` | Troubleshooting |

## Command Reference

### `/goalkit.webhooks list`

**Purpose**: Show all registered webhooks and their status

**When to use**:
- Audit current webhook configuration
- Check if specific integration is active
- Verify webhook health
- Before adding duplicate webhooks

**Outputs**:
```
Registered Webhooks (3 active, 1 disabled)
═══════════════════════════════════════════

1️⃣  Slack Notifications
    URL: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXX
    Events: task_completed, goal_completed, deadline_approaching
    Status: ✅ ACTIVE (Last delivery: 2025-01-15 14:32)
    Failures: 0

2️⃣  GitHub Status Update
    URL: https://api.github.com/repos/myorg/myrepo/issues/webhooks
    Events: goal_completed, high_risk
    Status: ✅ ACTIVE (Last delivery: 2025-01-14 09:15)
    Failures: 0

3️⃣  Email Notifications
    URL: https://email.company.com/api/notify
    Events: deadline_approaching, high_risk
    Status: ❌ DISABLED (Auto-disabled after 10 failures)
    Failures: 10 (last: 2025-01-10 16:22)

4️⃣  Discord Alerts
    URL: https://discordapp.com/api/webhooks/123456789/ABCDEF
    Events: goal_completed
    Status: ⚠️  DEGRADED (Last 3 failures, retrying)
    Failures: 3
```

**Example**:
```bash
/goalkit.webhooks list

# Expected: Table of all webhooks with status
```

**Interpretation**:
- ✅ ACTIVE = Working correctly
- ⚠️  DEGRADED = Failing intermittently (will retry)
- ❌ DISABLED = Auto-disabled after 10 failures (fix and re-enable)

---

### `/goalkit.webhooks add [URL] [--events EVENT1,EVENT2] [--secret SECRET]`

**Purpose**: Register a new webhook URL to receive event notifications

**When to use**:
- Setting up Slack/Discord/email notifications
- Integrating with external project management tools
- Creating custom automation workflows
- First-time webhook setup

**Supported Events**:
- `task_completed` - When a task is marked done
- `goal_completed` - When a goal reaches 100% completion
- `deadline_approaching` - When goal deadline is within 7 days
- `high_risk` - When analytics detect at-risk status

**Outputs**:
```
Webhook Registered Successfully ✅
═════════════════════════════════

Webhook ID: wh_abc123def456
URL: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXX
Events: task_completed, goal_completed
Status: ✅ ACTIVE
Secret: [auto-generated, stored securely]
First Delivery: [pending next event]

Header Verification:
├─ Algorithm: HMAC-SHA256
├─ Header: X-Goalkit-Signature
└─ Format: sha256=<hex_encoded_hash>

Next Steps:
1. Update your webhook consumer to verify signature
2. Test with `/goalkit.webhooks test <webhook_id>`
3. Monitor webhook events: `/goalkit.webhooks events`
```

**Example - Slack Integration**:
```bash
/goalkit.webhooks add https://hooks.slack.com/services/T00000000/B00000000/XXXX \
  --events task_completed,goal_completed,deadline_approaching

# Expected: Webhook registered and ready
```

**Example - Custom API**:
```bash
/goalkit.webhooks add https://api.mycompany.com/goalkit/webhooks \
  --events goal_completed,high_risk \
  --secret my-custom-secret-key-12345

# Expected: Webhook with custom secret registered
```

**Security Notes**:
- Each webhook gets unique HMAC-SHA256 signing
- Include X-Goalkit-Signature header verification
- Secrets auto-generated and stored securely
- Never expose webhook URLs in logs/version control

---

### `/goalkit.webhooks remove [WEBHOOK_ID]`

**Purpose**: Unregister a webhook and stop sending events

**When to use**:
- Removing broken integrations
- Disabling old notifications
- Cleaning up unused webhooks
- Testing before removing (disable first)

**Outputs**:
```
Webhook Removed ✅
═════════════════

Webhook ID: wh_abc123def456
URL: https://hooks.slack.com/services/T00000000/B00000000/XXXX
Status: DELETED

Notes:
- Cannot be undone, must re-add if needed
- Existing events not affected
- Future events will not be sent
```

**Example**:
```bash
/goalkit.webhooks remove wh_abc123def456

# Expected: Webhook deleted confirmation
```

**Caution**: Use `disable` if you want to temporarily stop events (can re-enable later)

---

### `/goalkit.webhooks test [WEBHOOK_ID]`

**Purpose**: Send a test event to validate webhook configuration

**When to use**:
- After adding new webhook
- After fixing webhook consumer
- Before going live with automation
- Troubleshooting delivery issues

**Outputs**:
```
Webhook Test Event Sent ✅
══════════════════════════

Webhook ID: wh_abc123def456
Event Type: task_completed (test)
Timestamp: 2025-01-15 14:32:45 UTC
Signed: Yes (X-Goalkit-Signature header included)

Response:
├─ Status: 200 OK ✅
├─ Body: {"status":"received","message":"Test event accepted"}
└─ Round-trip: 245ms

Headers Received:
├─ User-Agent: GoalKit/2.0.0
├─ X-Goalkit-Signature: sha256=abc123def456...
└─ Content-Type: application/json

✅ Ready for production!
```

**Example**:
```bash
/goalkit.webhooks test wh_abc123def456

# Expected: Test event sent and response validated
```

**Troubleshooting**:
- 404 Not Found → Check webhook URL is correct
- 401 Unauthorized → Check authentication/secret
- Timeout → Webhook consumer is too slow
- Connection refused → Consumer endpoint is down

---

### `/goalkit.webhooks enable [WEBHOOK_ID]`

**Purpose**: Re-enable a previously disabled webhook

**When to use**:
- After fixing a broken webhook consumer
- Resuming notifications after maintenance
- Recovering from auto-disable (fix issue first)

**Outputs**:
```
Webhook Enabled ✅
═════════════════

Webhook ID: wh_abc123def456
URL: https://hooks.slack.com/services/T00000000/B00000000/XXXX
Status: ✅ ACTIVE

Failure Counter: Reset to 0
Next Events: Will be delivered

Note: Missed events while disabled are NOT replayed
(Only future events will be sent)
```

**Example**:
```bash
/goalkit.webhooks enable wh_abc123def456

# Expected: Webhook re-enabled and counting failures reset
```

---

### `/goalkit.webhooks disable [WEBHOOK_ID]`

**Purpose**: Temporarily stop sending events to a webhook

**When to use**:
- Fixing webhook consumer issues
- Scheduled maintenance windows
- Testing without going live
- Preventing duplicate notifications

**Outputs**:
```
Webhook Disabled ⏸️
═══════════════════

Webhook ID: wh_abc123def456
URL: https://hooks.slack.com/services/T00000000/B00000000/XXXX
Status: ⏸️  DISABLED

Events: Will NOT be delivered
Re-enable: Use `webhooks enable <webhook_id>`

Note: You can re-enable this webhook anytime
(Unlike `remove`, which is permanent)
```

**Example**:
```bash
/goalkit.webhooks disable wh_abc123def456

# Expected: Webhook disabled, can be re-enabled later
```

---

### `/goalkit.webhooks events [--webhook WEBHOOK_ID] [--limit 50]`

**Purpose**: View webhook delivery history and event log

**When to use**:
- Troubleshooting failed deliveries
- Verifying events were sent
- Monitoring webhook health
- Auditing integration activity

**Outputs**:
```
Webhook Event History (wh_abc123def456)
═════════════════════════════════════════

Last 10 Events:

1. 2025-01-15 14:32:45 ✅ task_completed
   Task: "Implement API endpoint"
   Delivery: 234ms
   Response: 200 OK

2. 2025-01-15 10:15:20 ✅ task_completed
   Task: "Write unit tests"
   Delivery: 189ms
   Response: 200 OK

3. 2025-01-14 16:45:33 ⚠️  task_completed (Retry 2/5)
   Task: "Update documentation"
   Delivery: 5843ms (timeout)
   Response: 504 Gateway Timeout
   Retry scheduled: 2025-01-14 17:00

4. 2025-01-14 09:20:10 ✅ goal_completed
   Goal: "Improve API Performance"
   Delivery: 312ms
   Response: 200 OK

...

Summary:
├─ Total events: 47
├─ Successful: 45 (96%)
├─ Retrying: 1
├─ Failed: 1
├─ Average delivery time: 267ms
└─ Last failure: 2025-01-10 (recovered)
```

**Example**:
```bash
/goalkit.webhooks events --webhook wh_abc123def456 --limit 50

# Expected: Event delivery history with status
```

**Interpretation**:
- ✅ Green = Delivered successfully
- ⚠️  Yellow = Retry in progress (will succeed)
- 🔴 Red = Failed (needs attention)

---

### `/goalkit.webhooks types`

**Purpose**: Show available webhook event types

**When to use**:
- Planning webhook setup
- Understanding what events are available
- Determining which events to subscribe to

**Outputs**:
```
Available Webhook Event Types
═════════════════════════════

📋 Event Types:

1. task_completed
   ├─ Triggered: When a task is marked complete
   ├─ Payload: task_id, goal_id, task_name, timestamp
   ├─ Frequency: Per task (multiple times per goal)
   └─ Use case: Real-time progress updates, notifications

2. goal_completed
   ├─ Triggered: When a goal reaches 100% completion
   ├─ Payload: goal_id, goal_name, velocity, timeline, timestamp
   ├─ Frequency: Once per goal (per goal completion)
   └─ Use case: Celebrations, next-phase automation, reports

3. deadline_approaching
   ├─ Triggered: When goal deadline is within 7 days
   ├─ Payload: goal_id, goal_name, deadline, days_remaining, timestamp
   ├─ Frequency: Once per goal (on 7-day threshold)
   └─ Use case: Urgency alerts, priority escalation

4. high_risk
   ├─ Triggered: When analytics detect at-risk status
   ├─ Payload: goal_id, risk_level, blockers, required_velocity, timestamp
   ├─ Frequency: When status changes (3/5 times per goal)
   └─ Use case: Escalation alerts, intervention triggers

🔒 Security:
├─ Every event is signed with HMAC-SHA256
├─ Signature in X-Goalkit-Signature header
└─ Verify before processing
```

**Example**:
```bash
/goalkit.webhooks types

# Expected: Full list of event types and payloads
```

---

## Integration Examples

### Slack Integration

```bash
# 1. Create Slack incoming webhook at:
#    https://api.slack.com/messaging/webhooks

# 2. Register with Goal Kit
/goalkit.webhooks add https://hooks.slack.com/services/T00000000/B00000000/XXXX \
  --events task_completed,goal_completed,deadline_approaching

# 3. Test
/goalkit.webhooks test wh_abc123def456

# Result: Slack messages on events
# Channel sees: "[Goal Kit] Task completed: Implement API endpoint"
```

### Discord Integration

```bash
# 1. Create Discord webhook in server settings

# 2. Register
/goalkit.webhooks add https://discordapp.com/api/webhooks/123456789/ABCDEF \
  --events goal_completed,high_risk

# 3. Test
/goalkit.webhooks test wh_def789ghi012

# Result: Discord embeds on goal completion and risks
```

### Custom API Integration

```bash
# 1. Deploy custom webhook consumer at your API

# 2. Register with secret
/goalkit.webhooks add https://api.company.com/goalkit/webhooks \
  --events goal_completed,high_risk \
  --secret company-secret-key-12345

# 3. Implement signature verification in your consumer:
#    def verify_webhook(body, signature, secret):
#        expected = hmac.new(secret, body, sha256).hexdigest()
#        return signature == f"sha256={expected}"

# 4. Test
/goalkit.webhooks test wh_xyz123abc456

# Result: Custom automation triggered on events
```

---

## Common Workflows

### Setup Complete Notifications

```bash
# Register for goal completion
/goalkit.webhooks add https://hooks.slack.com/services/... \
  --events goal_completed

# Test
/goalkit.webhooks test wh_abc123

# Wait for goal completion, Slack message appears automatically
```

### Risk Alert Automation

```bash
# Register for high-risk detection
/goalkit.webhooks add https://api.company.com/escalate \
  --events high_risk

# When analytics detect risk, webhook fires immediately
# Your system can escalate, notify manager, trigger intervention
```

### Deadline Reminder System

```bash
# Register for deadline approaching
/goalkit.webhooks add https://calendar.company.com/api/reminders \
  --events deadline_approaching

# 7 days before deadline, webhook fires
# Your system can send team notifications
```

---

## Troubleshooting

### Webhook Disabled After 10 Failures

**Problem**: Webhook auto-disabled due to repeated failures

**Solution**:
```bash
# 1. Check what's failing
/goalkit.webhooks events --webhook wh_abc123

# 2. Fix the issue (URL, authentication, endpoint down, etc.)

# 3. Re-enable
/goalkit.webhooks enable wh_abc123

# 4. Test
/goalkit.webhooks test wh_abc123
```

### Events Not Being Delivered

**Problem**: Registered webhook but not receiving events

**Solution**:
```bash
# 1. Verify webhook is active
/goalkit.webhooks list

# 2. Check event history
/goalkit.webhooks events --webhook wh_abc123

# 3. Send test event
/goalkit.webhooks test wh_abc123

# 4. If test works but real events don't:
#    - Verify event type is registered (webhooks types)
#    - Check if event has occurred yet
#    - Monitor with: /goalkit.webhooks events --limit 100
```

### Signature Verification Failing

**Problem**: X-Goalkit-Signature doesn't match

**Solution**:
```python
# Correct verification:
import hmac
import hashlib

def verify_signature(request_body, signature_header):
    # 1. Get raw request body as bytes
    body_bytes = request_body.encode('utf-8') if isinstance(request_body, str) else request_body
    
    # 2. Calculate expected signature
    expected = 'sha256=' + hmac.new(
        secret.encode('utf-8'),
        body_bytes,
        hashlib.sha256
    ).hexdigest()
    
    # 3. Compare
    return signature_header == expected
```

---

## Data Files

Webhook configuration persists in `.goalkit/webhooks.json`:
- Registered webhooks with URLs and events
- Auto-generated secrets for signing
- Failure counts and status

Event history in `.goalkit/webhook_events.log`:
- Delivery attempts and responses
- Signatures and payloads
- Timestamps and durations
- Used for auditing and troubleshooting

---

## Pro Tips

1. **Start with one webhook** - Test thoroughly before adding multiple
2. **Use test command frequently** - Validate configuration before issues arise
3. **Monitor event history** - Check `/goalkit.webhooks events` weekly
4. **Implement signature verification** - Always verify X-Goalkit-Signature header
5. **Set up deadline notifications** - Early warning for approaching deadlines
6. **Track high-risk events** - Automate escalation for at-risk goals

## See Also

- [Analytics Guide](../analytics-guide.md) - Understanding what triggers events
- [Analytics Commands](./analytics.md) - Creating events with burndown/forecast
- [Forecast Command](./analytics.md#goalkitforecast) - Deadline detection triggers webhooks
