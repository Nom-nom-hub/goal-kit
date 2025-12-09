"""Webhook management for event notifications.

This module provides webhook functionality for integrating Goal Kit with
external services. Features include:

- Webhook registration and management
- Event triggering with payload delivery
- HMAC-SHA256 signed payloads for security
- Retry logic with exponential backoff
- Event type filtering and selective delivery
"""

import hashlib
import hmac
import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import httpx
except ImportError:
    httpx = None


@dataclass
class Webhook:
    """Webhook registration.

    Attributes:
        id: Unique webhook ID
        event_type: Type of event to trigger on
        url: Webhook endpoint URL
        secret: Secret for HMAC payload signing
        created_at: Creation timestamp (ISO 8601)
        last_triggered: Last trigger timestamp
        failure_count: Number of consecutive failures
        enabled: Whether webhook is active
    """

    id: str
    event_type: str
    url: str
    secret: str
    created_at: str
    last_triggered: Optional[str] = None
    failure_count: int = 0
    enabled: bool = True

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Webhook":
        """Create from dictionary (JSON deserialization)."""
        return cls(**data)


@dataclass
class WebhookEvent:
    """Webhook event payload.

    Attributes:
        event_type: Type of event
        goal_id: ID of affected goal
        task_id: ID of affected task (if applicable)
        timestamp: When event occurred (ISO 8601)
        data: Additional event data
    """

    event_type: str
    goal_id: str
    task_id: Optional[str] = None
    timestamp: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Set default timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class WebhookDelivery:
    """Record of webhook delivery attempt.

    Attributes:
        webhook_id: ID of the webhook
        event_type: Type of event
        timestamp: When delivery was attempted
        status: HTTP status code (0 if failed to connect)
        success: Whether delivery succeeded
        retries: Number of retry attempts
    """

    webhook_id: str
    event_type: str
    timestamp: str
    status: int
    success: bool
    retries: int = 0


class WebhookManager:
    """Manager for webhook registration and delivery.

    Handles storage, triggering, and delivery of webhooks with:
    - Persistence in .goalkit/webhooks.json
    - HMAC-SHA256 signed payloads
    - Retry logic with exponential backoff
    - Event-based filtering
    """

    def __init__(self, goalkit_dir: Path) -> None:
        """Initialize webhook manager.

        Args:
            goalkit_dir: Path to .goalkit directory
        """
        self.goalkit_dir = Path(goalkit_dir)
        self.webhooks_file = self.goalkit_dir / "webhooks.json"
        self.events_log_file = self.goalkit_dir / "webhook_events.log"

    def _load_webhooks(self) -> Dict[str, Webhook]:
        """Load webhooks from file.

        Returns:
            Dictionary mapping webhook ID to Webhook object
        """
        if not self.webhooks_file.exists():
            return {}

        try:
            with open(self.webhooks_file) as f:
                data = json.load(f)
                return {
                    webhook_id: Webhook.from_dict(webhook_data)
                    for webhook_id, webhook_data in data.items()
                }
        except (json.JSONDecodeError, ValueError, TypeError):
            return {}

    def _save_webhooks(self, webhooks: Dict[str, Webhook]) -> None:
        """Save webhooks to file.

        Args:
            webhooks: Dictionary of webhooks to save
        """
        self.goalkit_dir.mkdir(parents=True, exist_ok=True)

        data = {
            webhook_id: webhook.to_dict()
            for webhook_id, webhook in webhooks.items()
        }

        with open(self.webhooks_file, "w") as f:
            json.dump(data, f, indent=2)

    def register_webhook(
        self, event_type: str, url: str
    ) -> Webhook:
        """Register a new webhook.

        Args:
            event_type: Type of event ('task_completed', 'goal_completed', etc.)
            url: Webhook endpoint URL

        Returns:
            Registered Webhook object
        """
        webhooks = self._load_webhooks()

        # Generate ID and secret
        webhook_id = f"wh_{uuid.uuid4().hex[:12]}"
        secret = uuid.uuid4().hex

        webhook = Webhook(
            id=webhook_id,
            event_type=event_type,
            url=url,
            secret=secret,
            created_at=datetime.utcnow().isoformat(),
        )

        webhooks[webhook_id] = webhook
        self._save_webhooks(webhooks)

        return webhook

    def list_webhooks(
        self, event_type: Optional[str] = None
    ) -> List[Webhook]:
        """List registered webhooks.

        Args:
            event_type: Optional filter by event type

        Returns:
            List of Webhook objects
        """
        webhooks = self._load_webhooks()
        webhooks_list = list(webhooks.values())

        if event_type:
            webhooks_list = [
                w for w in webhooks_list
                if w.event_type == event_type
            ]

        return sorted(webhooks_list, key=lambda w: w.created_at)

    def get_webhook(self, webhook_id: str) -> Optional[Webhook]:
        """Get a specific webhook.

        Args:
            webhook_id: ID of the webhook

        Returns:
            Webhook object or None if not found
        """
        webhooks = self._load_webhooks()
        return webhooks.get(webhook_id)

    def delete_webhook(self, webhook_id: str) -> bool:
        """Delete a webhook.

        Args:
            webhook_id: ID of the webhook to delete

        Returns:
            True if deleted, False if not found
        """
        webhooks = self._load_webhooks()

        if webhook_id not in webhooks:
            return False

        del webhooks[webhook_id]
        self._save_webhooks(webhooks)
        return True

    def enable_webhook(self, webhook_id: str) -> bool:
        """Enable a webhook.

        Args:
            webhook_id: ID of the webhook

        Returns:
            True if enabled, False if not found
        """
        webhooks = self._load_webhooks()

        if webhook_id not in webhooks:
            return False

        webhooks[webhook_id].enabled = True
        self._save_webhooks(webhooks)
        return True

    def disable_webhook(self, webhook_id: str) -> bool:
        """Disable a webhook.

        Args:
            webhook_id: ID of the webhook

        Returns:
            True if disabled, False if not found
        """
        webhooks = self._load_webhooks()

        if webhook_id not in webhooks:
            return False

        webhooks[webhook_id].enabled = False
        self._save_webhooks(webhooks)
        return True

    def _sign_payload(self, payload: str, secret: str) -> str:
        """Create HMAC-SHA256 signature for payload.

        Args:
            payload: JSON payload string
            secret: Webhook secret

        Returns:
            Hex-encoded signature
        """
        signature = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _create_headers(
        self, payload: str, secret: str
    ) -> Dict[str, str]:
        """Create HTTP headers for webhook delivery.

        Args:
            payload: JSON payload string
            secret: Webhook secret

        Returns:
            Dictionary of HTTP headers
        """
        signature = self._sign_payload(payload, secret)

        return {
            "Content-Type": "application/json",
            "X-Goalkit-Signature": f"sha256={signature}",
            "X-Goalkit-Timestamp": datetime.utcnow().isoformat(),
        }

    def trigger_event(
        self,
        event: WebhookEvent,
        async_mode: bool = False,
    ) -> Dict[str, bool]:
        """Trigger an event and deliver to matching webhooks.

        Args:
            event: WebhookEvent to trigger
            async_mode: If True, return immediately (fire-and-forget)

        Returns:
            Dictionary mapping webhook_id to success status
        """
        webhooks = self._load_webhooks()

        # Filter to matching event types
        matching_webhooks = [
            w for w in webhooks.values()
            if w.event_type == event.event_type and w.enabled
        ]

        results = {}

        for webhook in matching_webhooks:
            if async_mode:
                # Fire-and-forget
                self._deliver_webhook(webhook, event)
                results[webhook.id] = True
            else:
                # Wait for delivery
                success = self._deliver_webhook(webhook, event)
                results[webhook.id] = success

        return results

    def _deliver_webhook(
        self,
        webhook: Webhook,
        event: WebhookEvent,
        attempt: int = 0,
        max_attempts: int = 5,
    ) -> bool:
        """Deliver webhook with retry logic.

        Args:
            webhook: Webhook to deliver
            event: Event to deliver
            attempt: Current attempt number
            max_attempts: Maximum number of retries

        Returns:
            True if successful, False if failed after all attempts
        """
        if httpx is None:
            # httpx not available, log but don't fail
            return False

        payload = json.dumps(event.to_dict())
        headers = self._create_headers(payload, webhook.secret)

        try:
            response = httpx.post(
                webhook.url,
                content=payload,
                headers=headers,
                timeout=10.0,
            )

            if response.status_code in (200, 201, 202, 204):
                # Success
                webhook.last_triggered = datetime.utcnow().isoformat()
                webhook.failure_count = 0

                # Update webhook
                webhooks = self._load_webhooks()
                webhooks[webhook.id] = webhook
                self._save_webhooks(webhooks)

                self._log_delivery(webhook.id, event.event_type, response.status_code, True)
                return True
            else:
                # Server error, retry
                if attempt < max_attempts:
                    backoff = 2 ** attempt  # Exponential backoff
                    time.sleep(backoff)
                    return self._deliver_webhook(
                        webhook, event, attempt + 1, max_attempts
                    )
                else:
                    # Failed after all retries
                    webhook.failure_count += 1

                    # Disable if too many failures
                    if webhook.failure_count > 10:
                        webhook.enabled = False

                    # Update webhook
                    webhooks = self._load_webhooks()
                    webhooks[webhook.id] = webhook
                    self._save_webhooks(webhooks)

                    self._log_delivery(webhook.id, event.event_type, response.status_code, False, attempt + 1)
                    return False

        except Exception as e:
            # Connection error, retry with backoff
            if attempt < max_attempts:
                backoff = 2 ** attempt
                time.sleep(backoff)
                return self._deliver_webhook(
                    webhook, event, attempt + 1, max_attempts
                )
            else:
                # Failed after all retries
                webhook.failure_count += 1

                # Disable if too many failures
                if webhook.failure_count > 10:
                    webhook.enabled = False

                # Update webhook
                webhooks = self._load_webhooks()
                webhooks[webhook.id] = webhook
                self._save_webhooks(webhooks)

                self._log_delivery(webhook.id, event.event_type, 0, False, attempt + 1, str(e))
                return False

    def _log_delivery(
        self,
        webhook_id: str,
        event_type: str,
        status: int,
        success: bool,
        retries: int = 0,
        error: Optional[str] = None,
    ) -> None:
        """Log webhook delivery attempt.

        Args:
            webhook_id: ID of the webhook
            event_type: Type of event
            status: HTTP status code
            success: Whether delivery succeeded
            retries: Number of retries attempted
            error: Error message if applicable
        """
        self.goalkit_dir.mkdir(parents=True, exist_ok=True)

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "webhook_id": webhook_id,
            "event_type": event_type,
            "status": status,
            "success": success,
            "retries": retries,
        }

        if error:
            log_entry["error"] = error

        with open(self.events_log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def test_webhook(self, webhook_id: str) -> bool:
        """Test webhook delivery.

        Args:
            webhook_id: ID of the webhook

        Returns:
            True if test successful
        """
        webhook = self.get_webhook(webhook_id)
        if not webhook:
            return False

        test_event = WebhookEvent(
            event_type="test",
            goal_id="test",
            data={"message": "Test webhook delivery"},
        )

        return self._deliver_webhook(webhook, test_event)

    def get_event_log(
        self, webhook_id: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get event delivery log.

        Args:
            webhook_id: Optional filter by webhook ID
            limit: Maximum number of entries to return

        Returns:
            List of log entries (most recent first)
        """
        if not self.events_log_file.exists():
            return []

        entries = []

        try:
            with open(self.events_log_file) as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if webhook_id is None or entry.get("webhook_id") == webhook_id:
                            entries.append(entry)
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            pass

        # Return most recent first
        return sorted(
            entries,
            key=lambda e: e.get("timestamp", ""),
            reverse=True
        )[:limit]
