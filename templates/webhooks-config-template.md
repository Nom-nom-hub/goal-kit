# Webhooks Configuration Template

**Project**: [PROJECT_NAME]
**Created**: [DATE]
**Last Updated**: [DATE]
**Owner**: [TEAM_NAME / PERSON_NAME]

---

## 📋 Webhook Overview

Summary of all webhook integrations for this project.

**Example**:
> This project uses 3 webhooks for team notifications:
> 1. **Slack** - Daily progress and alerts to #goals channel
> 2. **GitHub** - Risk escalation as issues in tracking repository
> 3. **Email** - Deadline reminders to project stakeholders

**Your Overview**:
[Write 2-3 sentences describing your webhook setup and purpose]

---

## ✅ Registered Webhooks

### Summary Table

| # | Name | Platform | Events | Status | Owner |
|---|------|----------|--------|--------|-------|
| 1 | [NAME] | [Slack/Discord/GitHub/Email/Custom] | [task_completed, goal_completed, ...] | ✅ ACTIVE | [OWNER] |
| 2 | [NAME] | [Slack/Discord/GitHub/Email/Custom] | [task_completed, goal_completed, ...] | ✅ ACTIVE | [OWNER] |
| 3 | [NAME] | [Slack/Discord/GitHub/Email/Custom] | [task_completed, goal_completed, ...] | ⏸️  DISABLED | [OWNER] |

**Example**:
| # | Name | Platform | Events | Status | Owner |
|---|------|----------|--------|--------|-------|
| 1 | Slack Progress | Slack | task_completed, goal_completed | ✅ ACTIVE | PM |
| 2 | GitHub Escalation | GitHub | high_risk, deadline_approaching | ✅ ACTIVE | Eng Lead |
| 3 | Email Backup | Email | goal_completed | ⏸️  DISABLED | Ops |

---

## 🔔 Webhook Configurations

### Webhook 1: [NAME]

**Purpose**: [What this webhook does and why]

**Example**: 
> Send Slack notifications to #goals channel when tasks complete, keeping team in sync on progress

**Configuration**:
```
Platform:    [Slack/Discord/GitHub/Email/Custom]
Webhook ID:  [wh_xxxxx]
URL:         [WEBHOOK_URL]
Secret:      [Generated automatically - stored securely]
Status:      ✅ ACTIVE / ⏸️  DISABLED / ❌ FAILED
Created:     [DATE]
Last Tested: [DATE]
```

**Events Subscribed**:
- [ ] `task_completed` - When task marked done
- [ ] `goal_completed` - When goal reaches 100%
- [ ] `deadline_approaching` - When deadline is 7 days away
- [ ] `high_risk` - When at-risk status detected

**Example**:
```
Platform:    Slack
Webhook ID:  wh_abc123def456
URL:         https://hooks.slack.com/services/T00000000/B00000000/XXXX
Secret:      [Auto-generated - 32 chars]
Status:      ✅ ACTIVE
Created:     2025-01-10
Last Tested: 2025-01-15

Events:
- ✅ task_completed
- ✅ goal_completed
- ✅ deadline_approaching
- ❌ high_risk
```

**Notification Format**:

**What gets sent**:
```
[MESSAGE PREVIEW / EXAMPLE OF WHAT TEAM RECEIVES]
```

**Example Slack Message**:
```
✅ Task Completed
Goal: Improve API Performance
Task: Implement caching layer
Completed: 2025-01-15 14:32 UTC
Progress: 8 of 12 tasks (67%)
```

**Integration Details**:

- **Channel/Recipient**: [Where messages go]
- **Frequency**: [How often events fire]
- **Filtering**: [Any event filtering applied]
- **Customization**: [Any custom modifications]

**Example Details**:
- **Channel**: #goals (public team channel)
- **Frequency**: Real-time (on task completion)
- **Filtering**: Only for active goals (not completed)
- **Customization**: Includes emoji reactions for quick status

**Testing**:
- [ ] Webhook created and registered
- [ ] Test event sent successfully
- [ ] Team verified message received
- [ ] Message format validated
- [ ] Secret verification enabled

**Last Test Result**: ✅ PASSED (2025-01-15 14:32)

**Troubleshooting**:
If webhook not delivering:
1. Check status: `/goalkit.webhooks list`
2. View events: `/goalkit.webhooks events --webhook [ID]`
3. Look for failures in log
4. Common causes:
   - URL changed or domain down
   - Authentication token expired
   - Firewall/IP blocking
   - Endpoint too slow (timeout)
5. Fix issue, then re-test: `/goalkit.webhooks test [ID]`

**Next Review**: [DATE]
**Owner**: [PERSON]
**Escalation**: [WHO TO CONTACT IF BROKEN]

---

### Webhook 2: [NAME]

**Purpose**: [What this webhook does and why]

**Configuration**:
```
Platform:    [Platform]
Webhook ID:  [ID]
URL:         [URL]
Secret:      [Auto-generated]
Status:      [Status]
Created:     [DATE]
Last Tested: [DATE]
```

**Events Subscribed**:
- [ ] `task_completed`
- [ ] `goal_completed`
- [ ] `deadline_approaching`
- [ ] `high_risk`

**Example**:
```
Platform:    GitHub
Webhook ID:  wh_xyz789abc123
URL:         https://api.github.com/repos/myorg/myrepo/webhooks
Secret:      [Auto-generated - 32 chars]
Status:      ✅ ACTIVE
Created:     2025-01-12
Last Tested: 2025-01-15

Events:
- ❌ task_completed
- ❌ goal_completed
- ✅ deadline_approaching
- ✅ high_risk
```

**Notification Format**:

```
[MESSAGE PREVIEW / EXAMPLE OF WHAT GETS SENT]
```

**Example GitHub Issue Creation**:
```
Title: 🚨 Goal "Improve API Performance" at Risk

Body:
Goal: Improve API Performance (ID: 001)
Risk Level: CRITICAL
Days Left: 10
Tasks Left: 8
Status: Need 0.8 tasks/day, averaging 0.4
Blocker: Infrastructure team (3 days delay)

Action Required: Scope reduction OR deadline extension
```

**Integration Details**:
- **Destination**: [Where issues/data goes]
- **Frequency**: [How often events fire]
- **Impact**: [What happens when triggered]

**Testing**:
- [ ] Webhook created and registered
- [ ] Test event sent successfully
- [ ] Integration verified (issue created, data updated, etc.)
- [ ] Signature verification enabled

**Last Test Result**: ✅ PASSED (2025-01-15 09:45)

**Next Review**: [DATE]
**Owner**: [PERSON]

---

### Webhook 3: [NAME]

[Repeat same structure for each webhook]

---

## 🚀 Setup Instructions

For agents/team members setting up new webhooks:

### Step 1: Choose Platform
- **Slack**: For team notifications (easiest)
- **Discord**: For gaming/creative teams
- **GitHub**: For development workflow integration
- **Email**: For formal notifications
- **Custom API**: For internal systems

### Step 2: Create Webhook on Platform
- Slack: https://api.slack.com/messaging/webhooks
- Discord: Server Settings → Integrations → Webhooks
- GitHub: Repository → Settings → Webhooks
- Email: Use SendGrid/Mailgun/similar service
- Custom: Deploy webhook consumer endpoint

### Step 3: Register with Goal Kit
```bash
/goalkit.webhooks add [PLATFORM_WEBHOOK_URL] \
  --events task_completed,goal_completed,deadline_approaching \
  [--secret my-custom-secret]
```

### Step 4: Test
```bash
/goalkit.webhooks test [WEBHOOK_ID]
```

### Step 5: Verify
Check `/goalkit.webhooks events --webhook [ID]` to confirm delivery

---

## 📊 Event Types Reference

### Available Events

| Event | Fired When | Payload Size | Frequency |
|-------|-----------|--------------|-----------|
| `task_completed` | Task marked done | ~200 bytes | Per task (~10-20x per goal) |
| `goal_completed` | Goal reaches 100% | ~300 bytes | Once per goal |
| `deadline_approaching` | 7 days until deadline | ~400 bytes | Once per goal |
| `high_risk` | At-risk status detected | ~500 bytes | 2-5x per goal |

### Event Payload Example

**task_completed**:
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

**goal_completed**:
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

---

## 🔒 Security Configuration

### HMAC Signature Verification

Every webhook includes `X-Goalkit-Signature` header for verification.

**Implementation** (Python example):
```python
import hmac
import hashlib

def verify_signature(body, signature_header, secret):
    expected = 'sha256=' + hmac.new(
        secret.encode('utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()
    return signature_header == expected
```

**Verification Status**:
- [ ] Webhook 1: ✅ Signature verification enabled
- [ ] Webhook 2: ✅ Signature verification enabled
- [ ] Webhook 3: ✅ Signature verification enabled

**Secrets Storage**:
- Stored securely in `.goalkit/webhooks.json` (never commit to git)
- Auto-generated for each webhook
- Rotatable if compromised
- View command: `/goalkit.webhooks list` (shows status, not actual secrets)

---

## 📈 Monitoring & Health

### Webhook Health Dashboard

| Webhook | Status | Last Delivery | Success Rate | Failures | Action |
|---------|--------|---------------|--------------|----------|--------|
| [Name] | ✅ ACTIVE | [DATE TIME] | [%] | [#] | Monitor |
| [Name] | ✅ ACTIVE | [DATE TIME] | [%] | [#] | Monitor |
| [Name] | ⏸️  DISABLED | [DATE TIME] | [%] | [#] | Re-enable |

**Example**:
| Webhook | Status | Last Delivery | Success Rate | Failures | Action |
|---------|--------|---------------|--------------|----------|--------|
| Slack Progress | ✅ ACTIVE | 2025-01-15 16:32 | 98.5% | 1 | Monitor |
| GitHub Risk | ✅ ACTIVE | 2025-01-14 14:22 | 100% | 0 | Monitor |
| Email Alerts | ❌ DISABLED | 2025-01-10 09:15 | 70% | 10 | Fix & re-enable |

### Monitoring Schedule

- **Daily**: Check status during execution
- **Weekly**: Review delivery history in team meeting
- **Monthly**: Audit all webhooks for continued relevance

**Monitoring Commands**:
```bash
# Quick status check
/goalkit.webhooks list

# Detailed event history
/goalkit.webhooks events --webhook [ID] --limit 50

# Test after fixing
/goalkit.webhooks test [ID]
```

---

## 🔄 Webhook Lifecycle

### Adding New Webhook

1. **Create** webhook on external platform
2. **Register** with Goal Kit: `/goalkit.webhooks add [URL] --events [EVENTS]`
3. **Test** with `/goalkit.webhooks test [ID]`
4. **Document** in this file with full details
5. **Train** team on what to expect
6. **Monitor** first week for issues

**Estimated Setup Time**: 10 minutes

### Disabling Webhook

```bash
# Temporary pause (can re-enable)
/goalkit.webhooks disable [ID]
```

**When to disable**:
- Fixing consumer endpoint issues
- Scheduled maintenance
- Reducing noise during testing
- Preventing duplicate notifications

### Removing Webhook

```bash
# Permanent deletion
/goalkit.webhooks remove [ID]
```

**When to remove**:
- Integration no longer needed
- Platform being deprecated
- Repeated failures after attempts to fix

⚠️ **Cannot be undone** - must re-add if needed later

### Auto-Disable Rule

Webhook **auto-disabled after 10 consecutive failures**.

**To recover**:
1. Investigate failure cause (check `/goalkit.webhooks events`)
2. Fix the issue (URL, authentication, endpoint, etc.)
3. Re-test: `/goalkit.webhooks test [ID]`
4. Re-enable: `/goalkit.webhooks enable [ID]`

---

## 📋 Maintenance Log

Track webhook changes and maintenance history.

| Date | Webhook | Action | Reason | Owner |
|------|---------|--------|--------|-------|
| [DATE] | [NAME] | [Added/Fixed/Disabled/Removed] | [REASON] | [OWNER] |
| [DATE] | [NAME] | [Added/Fixed/Disabled/Removed] | [REASON] | [OWNER] |

**Example**:
| Date | Webhook | Action | Reason | Owner |
|------|---------|--------|--------|-------|
| 2025-01-10 | Slack Progress | Added | Initial setup | PM |
| 2025-01-12 | GitHub Risk | Added | Risk escalation automation | Eng Lead |
| 2025-01-14 | Email Alerts | Fixed | Token expired, renewed | Ops |
| 2025-01-15 | Email Alerts | Disabled | Too verbose, deferring | PM |

---

## 🔗 Related Documents

- **Analytics Guide**: `docs/analytics-guide.md` - Understanding data that triggers webhooks
- **Webhook Command Guide**: `templates/commands/webhooks.md` - How to use webhook commands
- **Webhooks Setup Guide**: `docs/webhooks-guide.md` - Detailed integration examples
- **Webhook Config File**: `.goalkit/webhooks.json` - Raw webhook data (don't edit manually)

---

## ✅ Compliance Checklist

- [ ] All webhooks documented in this file
- [ ] All webhooks tested in last 30 days
- [ ] All webhooks have signature verification
- [ ] Security audit completed
- [ ] Team trained on webhook behavior
- [ ] Escalation contacts identified
- [ ] Monitoring process established
- [ ] Backup notification method identified

---

## 👥 Team Contacts

| Role | Name | Contact | Responsibility |
|------|------|---------|-----------------|
| Webhook Owner | [NAME] | [EMAIL/SLACK] | Webhook maintenance |
| Escalation Contact | [NAME] | [EMAIL/SLACK] | When webhooks fail |
| Security Owner | [NAME] | [EMAIL/SLACK] | Signature/secret management |

---

## 📝 Notes

[Any additional context, decisions, or observations about webhooks]

**Example Notes**:
> - Slack notifications very popular with team, high engagement
> - GitHub issues sometimes create duplicate notifications - consider filtering
> - Email service has been unreliable, considering alternative
> - Consider adding webhook for Jira integration in future

---

**Last Review**: [DATE]
**Next Review**: [DATE]
**Approval**: [WHO APPROVED THIS CONFIG]

---

*Template Version*: 1.0
*Reference Guide*: [See `docs/webhooks-guide.md` for detailed setup help]
