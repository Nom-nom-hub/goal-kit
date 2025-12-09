"""Unit tests for webhook manager.

Tests cover:
- Webhook registration and management
- Webhook persistence
- Event triggering
- HMAC signing
- Retry logic
- Event logging
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from goalkeeper_cli.webhooks import (
    Webhook,
    WebhookEvent,
    WebhookManager,
)


@pytest.fixture
def webhook_manager(tmp_path):
    """Create webhook manager with temporary directory."""
    goalkit_dir = tmp_path / ".goalkit"
    goalkit_dir.mkdir()
    return WebhookManager(goalkit_dir)


@pytest.fixture
def sample_webhook(webhook_manager):
    """Create a sample webhook."""
    webhook = webhook_manager.register_webhook(
        event_type="task_completed",
        url="https://example.com/webhook",
    )
    return webhook


class TestWebhook:
    """Test Webhook data class."""

    def test_create_webhook(self):
        """Test creating a webhook."""
        webhook = Webhook(
            id="wh_abc123",
            event_type="task_completed",
            url="https://example.com/webhook",
            secret="secret_xyz789",
            created_at="2024-12-08T10:00:00",
        )

        assert webhook.id == "wh_abc123"
        assert webhook.event_type == "task_completed"
        assert webhook.url == "https://example.com/webhook"
        assert webhook.enabled is True

    def test_webhook_to_dict(self):
        """Test webhook serialization."""
        webhook = Webhook(
            id="wh_abc123",
            event_type="task_completed",
            url="https://example.com/webhook",
            secret="secret_xyz789",
            created_at="2024-12-08T10:00:00",
        )

        data = webhook.to_dict()
        assert data["id"] == "wh_abc123"
        assert data["event_type"] == "task_completed"

    def test_webhook_from_dict(self):
        """Test webhook deserialization."""
        data = {
            "id": "wh_abc123",
            "event_type": "task_completed",
            "url": "https://example.com/webhook",
            "secret": "secret_xyz789",
            "created_at": "2024-12-08T10:00:00",
        }

        webhook = Webhook.from_dict(data)
        assert webhook.id == "wh_abc123"
        assert webhook.event_type == "task_completed"


class TestWebhookEvent:
    """Test WebhookEvent data class."""

    def test_create_event(self):
        """Test creating a webhook event."""
        event = WebhookEvent(
            event_type="task_completed",
            goal_id="goal-1",
            task_id="task-1",
            data={"status": "done"},
        )

        assert event.event_type == "task_completed"
        assert event.goal_id == "goal-1"
        assert event.task_id == "task-1"
        assert event.timestamp is not None

    def test_event_default_timestamp(self):
        """Test that timestamp is generated if not provided."""
        event = WebhookEvent(
            event_type="task_completed",
            goal_id="goal-1",
        )

        assert event.timestamp is not None

    def test_event_to_dict(self):
        """Test event serialization."""
        event = WebhookEvent(
            event_type="task_completed",
            goal_id="goal-1",
            data={"status": "done"},
        )

        data = event.to_dict()
        assert data["event_type"] == "task_completed"
        assert data["goal_id"] == "goal-1"
        assert "timestamp" in data


class TestWebhookRegistration:
    """Test webhook registration."""

    def test_register_webhook(self, webhook_manager):
        """Test registering a new webhook."""
        webhook = webhook_manager.register_webhook(
            event_type="task_completed",
            url="https://example.com/webhook",
        )

        assert webhook.id.startswith("wh_")
        assert webhook.event_type == "task_completed"
        assert webhook.url == "https://example.com/webhook"
        assert webhook.secret
        assert webhook.enabled is True

    def test_register_multiple_webhooks(self, webhook_manager):
        """Test registering multiple webhooks."""
        webhook1 = webhook_manager.register_webhook(
            "task_completed", "https://example.com/webhook1"
        )
        webhook2 = webhook_manager.register_webhook(
            "goal_completed", "https://example.com/webhook2"
        )

        webhooks = webhook_manager.list_webhooks()
        assert len(webhooks) == 2

    def test_webhook_secrets_unique(self, webhook_manager):
        """Test that webhook secrets are unique."""
        webhook1 = webhook_manager.register_webhook(
            "task_completed", "https://example.com/webhook1"
        )
        webhook2 = webhook_manager.register_webhook(
            "task_completed", "https://example.com/webhook2"
        )

        assert webhook1.secret != webhook2.secret


class TestWebhookManagement:
    """Test webhook CRUD operations."""

    def test_list_webhooks(self, webhook_manager):
        """Test listing webhooks."""
        webhook_manager.register_webhook(
            "task_completed", "https://example.com/webhook1"
        )
        webhook_manager.register_webhook(
            "goal_completed", "https://example.com/webhook2"
        )

        webhooks = webhook_manager.list_webhooks()
        assert len(webhooks) == 2

    def test_list_webhooks_by_type(self, webhook_manager):
        """Test listing webhooks filtered by event type."""
        webhook_manager.register_webhook(
            "task_completed", "https://example.com/webhook1"
        )
        webhook_manager.register_webhook(
            "goal_completed", "https://example.com/webhook2"
        )

        task_webhooks = webhook_manager.list_webhooks("task_completed")
        assert len(task_webhooks) == 1
        assert task_webhooks[0].event_type == "task_completed"

    def test_get_webhook(self, sample_webhook, webhook_manager):
        """Test getting a specific webhook."""
        webhook = webhook_manager.get_webhook(sample_webhook.id)

        assert webhook is not None
        assert webhook.id == sample_webhook.id
        assert webhook.event_type == sample_webhook.event_type

    def test_get_nonexistent_webhook(self, webhook_manager):
        """Test getting a webhook that doesn't exist."""
        webhook = webhook_manager.get_webhook("nonexistent")
        assert webhook is None

    def test_delete_webhook(self, sample_webhook, webhook_manager):
        """Test deleting a webhook."""
        success = webhook_manager.delete_webhook(sample_webhook.id)

        assert success is True
        assert webhook_manager.get_webhook(sample_webhook.id) is None

    def test_delete_nonexistent_webhook(self, webhook_manager):
        """Test deleting a webhook that doesn't exist."""
        success = webhook_manager.delete_webhook("nonexistent")
        assert success is False

    def test_enable_webhook(self, sample_webhook, webhook_manager):
        """Test enabling a webhook."""
        webhook_manager.disable_webhook(sample_webhook.id)
        success = webhook_manager.enable_webhook(sample_webhook.id)

        assert success is True
        webhook = webhook_manager.get_webhook(sample_webhook.id)
        assert webhook.enabled is True

    def test_disable_webhook(self, sample_webhook, webhook_manager):
        """Test disabling a webhook."""
        success = webhook_manager.disable_webhook(sample_webhook.id)

        assert success is True
        webhook = webhook_manager.get_webhook(sample_webhook.id)
        assert webhook.enabled is False

    def test_enable_nonexistent_webhook(self, webhook_manager):
        """Test enabling a webhook that doesn't exist."""
        success = webhook_manager.enable_webhook("nonexistent")
        assert success is False


class TestPayloadSigning:
    """Test HMAC-SHA256 payload signing."""

    def test_sign_payload(self, webhook_manager):
        """Test payload signing."""
        payload = '{"key": "value"}'
        secret = "test_secret"

        signature = webhook_manager._sign_payload(payload, secret)

        assert signature
        assert len(signature) == 64  # SHA256 hex length

    def test_signature_consistency(self, webhook_manager):
        """Test that same payload and secret produce same signature."""
        payload = '{"key": "value"}'
        secret = "test_secret"

        sig1 = webhook_manager._sign_payload(payload, secret)
        sig2 = webhook_manager._sign_payload(payload, secret)

        assert sig1 == sig2

    def test_signature_differs_for_different_payload(self, webhook_manager):
        """Test that different payloads produce different signatures."""
        secret = "test_secret"

        sig1 = webhook_manager._sign_payload('{"key": "value1"}', secret)
        sig2 = webhook_manager._sign_payload('{"key": "value2"}', secret)

        assert sig1 != sig2

    def test_signature_differs_for_different_secret(self, webhook_manager):
        """Test that different secrets produce different signatures."""
        payload = '{"key": "value"}'

        sig1 = webhook_manager._sign_payload(payload, "secret1")
        sig2 = webhook_manager._sign_payload(payload, "secret2")

        assert sig1 != sig2

    def test_create_headers(self, webhook_manager):
        """Test header creation with signature."""
        payload = '{"key": "value"}'
        secret = "test_secret"

        headers = webhook_manager._create_headers(payload, secret)

        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json"
        assert "X-Goalkit-Signature" in headers
        assert headers["X-Goalkit-Signature"].startswith("sha256=")
        assert "X-Goalkit-Timestamp" in headers


class TestEventTriggering:
    """Test event triggering."""

    def test_trigger_event_no_webhooks(self, webhook_manager):
        """Test triggering event with no matching webhooks."""
        event = WebhookEvent(
            event_type="task_completed",
            goal_id="goal-1",
        )

        results = webhook_manager.trigger_event(event)
        assert results == {}

    def test_trigger_event_matching_webhook(self, sample_webhook, webhook_manager):
        """Test triggering event with matching webhook."""
        event = WebhookEvent(
            event_type="task_completed",
            goal_id="goal-1",
        )

        # Mock the delivery method to avoid actual HTTP call
        with patch.object(
            webhook_manager, "_deliver_webhook", return_value=True
        ) as mock_deliver:
            results = webhook_manager.trigger_event(event)

            assert sample_webhook.id in results
            assert mock_deliver.called

    def test_trigger_event_filters_by_type(self, webhook_manager):
        """Test that trigger filters by event type."""
        webhook_manager.register_webhook(
            "task_completed", "https://example.com/webhook1"
        )
        webhook_manager.register_webhook(
            "goal_completed", "https://example.com/webhook2"
        )

        event = WebhookEvent(
            event_type="task_completed",
            goal_id="goal-1",
        )

        with patch.object(
            webhook_manager, "_deliver_webhook", return_value=True
        ) as mock_deliver:
            webhook_manager.trigger_event(event)

            # Only one webhook should be triggered
            assert mock_deliver.call_count == 1

    def test_trigger_event_skips_disabled(self, webhook_manager):
        """Test that trigger skips disabled webhooks."""
        webhook1 = webhook_manager.register_webhook(
            "task_completed", "https://example.com/webhook1"
        )
        webhook_manager.disable_webhook(webhook1.id)

        event = WebhookEvent(
            event_type="task_completed",
            goal_id="goal-1",
        )

        with patch.object(
            webhook_manager, "_deliver_webhook", return_value=True
        ) as mock_deliver:
            webhook_manager.trigger_event(event)

            # No webhooks should be triggered
            assert mock_deliver.call_count == 0


class TestWebhookPersistence:
    """Test webhook file persistence."""

    def test_webhooks_saved_to_file(self, webhook_manager):
        """Test that webhooks are saved to file."""
        webhook_manager.register_webhook(
            "task_completed", "https://example.com/webhook"
        )

        assert webhook_manager.webhooks_file.exists()

    def test_webhooks_file_format(self, webhook_manager):
        """Test webhook file is valid JSON."""
        webhook_manager.register_webhook(
            "task_completed", "https://example.com/webhook"
        )

        with open(webhook_manager.webhooks_file) as f:
            data = json.load(f)

        assert isinstance(data, dict)

    def test_webhooks_load_from_file(self, webhook_manager):
        """Test loading webhooks from file."""
        webhook_manager.register_webhook(
            "task_completed", "https://example.com/webhook"
        )

        webhooks = webhook_manager.list_webhooks()
        assert len(webhooks) == 1

    def test_load_empty_webhooks(self, webhook_manager):
        """Test loading when no webhooks exist."""
        webhooks = webhook_manager.list_webhooks()
        assert webhooks == []

    def test_load_corrupted_webhooks(self, webhook_manager):
        """Test loading corrupted webhooks file."""
        # Write invalid JSON
        with open(webhook_manager.webhooks_file, "w") as f:
            f.write("invalid json {")

        webhooks = webhook_manager.list_webhooks()
        assert webhooks == []


class TestEventLogging:
    """Test event delivery logging."""

    def test_log_delivery(self, webhook_manager):
        """Test logging webhook delivery."""
        webhook_manager._log_delivery(
            webhook_id="wh_abc123",
            event_type="task_completed",
            status=200,
            success=True,
            retries=0,
        )

        assert webhook_manager.events_log_file.exists()

    def test_event_log_format(self, webhook_manager):
        """Test event log entry format."""
        webhook_manager._log_delivery(
            webhook_id="wh_abc123",
            event_type="task_completed",
            status=200,
            success=True,
            retries=0,
        )

        with open(webhook_manager.events_log_file) as f:
            line = f.readline()
            entry = json.loads(line)

        assert entry["webhook_id"] == "wh_abc123"
        assert entry["event_type"] == "task_completed"
        assert entry["status"] == 200
        assert entry["success"] is True

    def test_get_event_log(self, webhook_manager):
        """Test retrieving event log."""
        webhook_manager._log_delivery(
            webhook_id="wh_abc123",
            event_type="task_completed",
            status=200,
            success=True,
            retries=0,
        )

        log = webhook_manager.get_event_log()
        assert len(log) > 0
        assert log[0]["webhook_id"] == "wh_abc123"

    def test_event_log_filtering(self, webhook_manager):
        """Test filtering event log by webhook ID."""
        webhook_manager._log_delivery(
            webhook_id="wh_abc123",
            event_type="task_completed",
            status=200,
            success=True,
        )
        webhook_manager._log_delivery(
            webhook_id="wh_xyz789",
            event_type="goal_completed",
            status=200,
            success=True,
        )

        log = webhook_manager.get_event_log("wh_abc123")
        assert len(log) == 1
        assert log[0]["webhook_id"] == "wh_abc123"

    def test_event_log_limit(self, webhook_manager):
        """Test event log result limiting."""
        for i in range(30):
            webhook_manager._log_delivery(
                webhook_id="wh_abc123",
                event_type="task_completed",
                status=200,
                success=True,
            )

        log = webhook_manager.get_event_log(limit=10)
        assert len(log) == 10


class TestTestWebhook:
    """Test webhook testing functionality."""

    def test_test_webhook_nonexistent(self, webhook_manager):
        """Test testing a webhook that doesn't exist."""
        result = webhook_manager.test_webhook("nonexistent")
        assert result is False

    def test_test_webhook_with_mock(self, sample_webhook, webhook_manager):
        """Test webhook testing with mocked delivery."""
        with patch.object(
            webhook_manager, "_deliver_webhook", return_value=True
        ):
            result = webhook_manager.test_webhook(sample_webhook.id)
            assert result is True


class TestRetryLogic:
    """Test retry logic for webhook delivery."""

    @patch("goalkeeper_cli.webhooks.httpx.post")
    def test_delivery_success_first_try(self, mock_post, sample_webhook, webhook_manager):
        """Test successful delivery on first attempt."""
        mock_post.return_value.status_code = 200

        webhook = webhook_manager.get_webhook(sample_webhook.id)
        event = WebhookEvent(
            event_type="task_completed",
            goal_id="goal-1",
        )

        result = webhook_manager._deliver_webhook(webhook, event)

        assert result is True
        assert mock_post.call_count == 1

    @patch("goalkeeper_cli.webhooks.time.sleep")
    @patch("goalkeeper_cli.webhooks.httpx.post")
    def test_delivery_retry_on_failure(self, mock_post, mock_sleep, sample_webhook, webhook_manager):
        """Test retry on delivery failure."""
        # Fail first 2 times, succeed on 3rd
        mock_post.side_effect = [
            MagicMock(status_code=500),
            MagicMock(status_code=500),
            MagicMock(status_code=200),
        ]

        webhook = webhook_manager.get_webhook(sample_webhook.id)
        event = WebhookEvent(
            event_type="task_completed",
            goal_id="goal-1",
        )

        result = webhook_manager._deliver_webhook(webhook, event)

        assert result is True
        assert mock_post.call_count == 3

    @patch("goalkeeper_cli.webhooks.httpx.post")
    def test_delivery_max_retries(self, mock_post, sample_webhook, webhook_manager):
        """Test max retry limit."""
        mock_post.side_effect = Exception("Connection error")

        webhook = webhook_manager.get_webhook(sample_webhook.id)
        event = WebhookEvent(
            event_type="task_completed",
            goal_id="goal-1",
        )

        result = webhook_manager._deliver_webhook(webhook, event)

        assert result is False
        # Should attempt initial + max retries
        assert mock_post.call_count == 6  # 1 + 5 retries

    @patch("goalkeeper_cli.webhooks.httpx.post")
    def test_failure_count_incremented(self, mock_post, sample_webhook, webhook_manager):
        """Test that failure count is incremented."""
        mock_post.side_effect = Exception("Connection error")

        webhook = webhook_manager.get_webhook(sample_webhook.id)
        event = WebhookEvent(
            event_type="task_completed",
            goal_id="goal-1",
        )

        webhook_manager._deliver_webhook(webhook, event)

        updated = webhook_manager.get_webhook(sample_webhook.id)
        assert updated.failure_count > 0

    @patch("goalkeeper_cli.webhooks.httpx.post")
    def test_webhook_disabled_on_too_many_failures(
        self, mock_post, sample_webhook, webhook_manager
    ):
        """Test webhook is disabled after too many failures."""
        mock_post.side_effect = Exception("Connection error")

        webhook = webhook_manager.get_webhook(sample_webhook.id)
        event = WebhookEvent(
            event_type="task_completed",
            goal_id="goal-1",
        )

        # Simulate 11 failed delivery attempts
        for _ in range(11):
            webhook_manager._deliver_webhook(webhook, event)
            webhook = webhook_manager.get_webhook(sample_webhook.id)

        # Should be disabled
        assert webhook.enabled is False


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_webhook_list(self, webhook_manager):
        """Test empty webhook list."""
        webhooks = webhook_manager.list_webhooks()
        assert webhooks == []

    def test_webhook_with_empty_url(self, webhook_manager):
        """Test webhook with empty URL."""
        # Should still create webhook
        webhook = webhook_manager.register_webhook(
            "task_completed", ""
        )
        assert webhook.url == ""

    def test_event_with_empty_data(self, webhook_manager):
        """Test event with empty data dict."""
        event = WebhookEvent(
            event_type="task_completed",
            goal_id="goal-1",
            data={},
        )

        data = event.to_dict()
        assert data["data"] == {}

    def test_large_event_payload(self, webhook_manager):
        """Test with large event payload."""
        large_data = {"key": "x" * 10000}
        event = WebhookEvent(
            event_type="task_completed",
            goal_id="goal-1",
            data=large_data,
        )

        payload = json.dumps(event.to_dict())
        assert len(payload) > 10000
