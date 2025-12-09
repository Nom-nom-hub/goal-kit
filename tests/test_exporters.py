"""Tests for data export functionality."""

import pytest
import json
import csv
from io import StringIO
from uuid import uuid4
from datetime import datetime, timedelta

from src.goalkeeper_cli.exporters import (
    ExportManager,
    CSVExporter,
    JSONExporter,
    MarkdownExporter,
    TextExporter,
)
from src.goalkeeper_cli.tasks import TaskTracker
from src.goalkeeper_cli.reporting import ReportGenerator, Report, ReportType, Insight, InsightType, InsightSeverity
from src.goalkeeper_cli.models import TaskStatus


@pytest.fixture
def tmp_project(tmp_path):
    """Create a temporary project."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    (project_dir / ".goalkit").mkdir()
    return project_dir


@pytest.fixture
def sample_tasks(tmp_project):
    """Create sample tasks."""
    tracker = TaskTracker(tmp_project)
    goal_id = str(uuid4())

    tasks = []
    for i in range(5):
        task_id = tracker.create_task(goal_id, f"Task {i}", f"Description {i}", float(i))
        if i < 2:
            tracker.update_task_status(task_id, TaskStatus.COMPLETED)
        elif i < 4:
            tracker.update_task_status(task_id, TaskStatus.IN_PROGRESS)
        tasks.append(tracker.get_task(task_id))

    return tasks


@pytest.fixture
def sample_report(tmp_project):
    """Create a sample report."""
    generator = ReportGenerator(tmp_project)
    # Populate some data first
    tracker = TaskTracker(tmp_project)
    goal_id = str(uuid4())
    for i in range(10):
        task_id = tracker.create_task(goal_id, f"Task {i}", "Desc")
        if i < 5:
            tracker.update_task_status(task_id, TaskStatus.COMPLETED)

    report = generator.generate_summary_report()
    return report


class TestCSVExporter:
    """Test CSV export functionality."""

    def test_export_tasks_csv(self, sample_tasks):
        """Test exporting tasks to CSV."""
        exporter = CSVExporter()
        csv_data = exporter.export_tasks(sample_tasks)

        assert isinstance(csv_data, str)
        assert "Task 0" in csv_data
        assert "completed" in csv_data
        assert "in_progress" in csv_data

    def test_csv_is_valid(self, sample_tasks):
        """Test that exported CSV is valid."""
        exporter = CSVExporter()
        csv_data = exporter.export_tasks(sample_tasks)

        reader = csv.DictReader(StringIO(csv_data))
        rows = list(reader)

        assert len(rows) == 5
        assert rows[0]["Title"] == "Task 0"

    def test_export_report_csv(self, sample_report):
        """Test exporting report to CSV."""
        exporter = CSVExporter()
        csv_data = exporter.export_report(sample_report)

        assert isinstance(csv_data, str)
        assert "Report:" in csv_data or "Summary" in csv_data

    def test_export_metrics_csv(self):
        """Test exporting metrics to CSV."""
        exporter = CSVExporter()
        metrics = {"metric1": 100, "metric2": 50.5}
        csv_data = exporter.export_metrics(metrics)

        assert "metric1" in csv_data
        assert "100" in csv_data


class TestJSONExporter:
    """Test JSON export functionality."""

    def test_export_tasks_json(self, sample_tasks):
        """Test exporting tasks to JSON."""
        exporter = JSONExporter()
        json_data = exporter.export_tasks(sample_tasks)

        data = json.loads(json_data)
        assert isinstance(data, list)
        assert len(data) == 5
        assert data[0]["title"] == "Task 0"

    def test_json_completeness(self, sample_tasks):
        """Test that JSON export includes all fields."""
        exporter = JSONExporter()
        json_data = exporter.export_tasks(sample_tasks)

        data = json.loads(json_data)
        task = data[0]

        assert "id" in task
        assert "title" in task
        assert "status" in task
        assert "goal_id" in task

    def test_export_report_json(self, sample_report):
        """Test exporting report to JSON."""
        exporter = JSONExporter()
        json_data = exporter.export_report(sample_report)

        data = json.loads(json_data)
        assert "title" in data
        assert "summary" in data
        assert "metrics" in data

    def test_export_metrics_json(self):
        """Test exporting metrics to JSON."""
        exporter = JSONExporter()
        metrics = {"metric1": 100, "metric2": 50.5}
        json_data = exporter.export_metrics(metrics)

        data = json.loads(json_data)
        assert data["metric1"] == 100
        assert data["metric2"] == 50.5


class TestMarkdownExporter:
    """Test Markdown export functionality."""

    def test_export_tasks_markdown(self, sample_tasks):
        """Test exporting tasks to Markdown."""
        exporter = MarkdownExporter()
        md_data = exporter.export_tasks(sample_tasks)

        assert isinstance(md_data, str)
        assert "# Tasks" in md_data
        assert "Task 0" in md_data
        assert "✓" in md_data or "○" in md_data

    def test_markdown_formatting(self, sample_tasks):
        """Test Markdown formatting."""
        exporter = MarkdownExporter()
        md_data = exporter.export_tasks(sample_tasks)

        assert "##" in md_data  # Headers
        assert "-" in md_data  # Lists

    def test_export_report_markdown(self, sample_report):
        """Test exporting report to Markdown."""
        exporter = MarkdownExporter()
        md_data = exporter.export_report(sample_report)

        assert isinstance(md_data, str)
        assert "#" in md_data  # Has headers

    def test_export_metrics_markdown(self):
        """Test exporting metrics to Markdown."""
        exporter = MarkdownExporter()
        metrics = {"metric1": 100, "metric2": 50.5}
        md_data = exporter.export_metrics(metrics)

        assert "# Metrics" in md_data
        assert "metric1" in md_data


class TestTextExporter:
    """Test plain text export functionality."""

    def test_export_tasks_text(self, sample_tasks):
        """Test exporting tasks to plain text."""
        exporter = TextExporter()
        text_data = exporter.export_tasks(sample_tasks)

        assert isinstance(text_data, str)
        assert "TASKS" in text_data
        assert "Task 0" in text_data

    def test_text_formatting(self, sample_tasks):
        """Test plain text formatting."""
        exporter = TextExporter()
        text_data = exporter.export_tasks(sample_tasks)

        assert "[✓]" in text_data or "[ ]" in text_data

    def test_export_report_text(self, sample_report):
        """Test exporting report to plain text."""
        exporter = TextExporter()
        text_data = exporter.export_report(sample_report)

        assert isinstance(text_data, str)
        assert "Type:" in text_data or "SUMMARY" in text_data

    def test_export_metrics_text(self):
        """Test exporting metrics to plain text."""
        exporter = TextExporter()
        metrics = {"metric1": 100, "metric2": 50.5}
        text_data = exporter.export_metrics(metrics)

        assert "METRICS" in text_data
        assert "metric1" in text_data


class TestExportManager:
    """Test ExportManager functionality."""

    def test_export_manager_supports_formats(self):
        """Test that manager supports all formats."""
        manager = ExportManager()
        formats = manager.get_supported_formats()

        assert "csv" in formats
        assert "json" in formats
        assert "markdown" in formats
        assert "text" in formats

    def test_export_tasks_csv(self, sample_tasks):
        """Test export through manager to CSV."""
        manager = ExportManager()
        csv_data = manager.export_tasks(sample_tasks, format="csv")

        assert isinstance(csv_data, str)
        assert "Task 0" in csv_data

    def test_export_tasks_json(self, sample_tasks):
        """Test export through manager to JSON."""
        manager = ExportManager()
        json_data = manager.export_tasks(sample_tasks, format="json")

        data = json.loads(json_data)
        assert len(data) == 5

    def test_export_tasks_markdown(self, sample_tasks):
        """Test export through manager to Markdown."""
        manager = ExportManager()
        md_data = manager.export_tasks(sample_tasks, format="markdown")

        assert "# Tasks" in md_data

    def test_export_tasks_text(self, sample_tasks):
        """Test export through manager to text."""
        manager = ExportManager()
        text_data = manager.export_tasks(sample_tasks, format="text")

        assert "TASKS" in text_data

    def test_export_report_all_formats(self, sample_report):
        """Test exporting report in all formats."""
        manager = ExportManager()

        for format in manager.get_supported_formats():
            data = manager.export_report(sample_report, format=format)
            assert isinstance(data, str)
            assert len(data) > 0

    def test_export_metrics_all_formats(self):
        """Test exporting metrics in all formats."""
        manager = ExportManager()
        metrics = {"metric1": 100, "metric2": 50.5}

        for format in manager.get_supported_formats():
            data = manager.export_metrics(metrics, format=format)
            assert isinstance(data, str)
            assert len(data) > 0

    def test_unsupported_format_raises_error(self, sample_tasks):
        """Test that unsupported format raises error."""
        manager = ExportManager()

        with pytest.raises(ValueError):
            manager.export_tasks(sample_tasks, format="pdf")


class TestExportDataIntegrity:
    """Test data integrity in exports."""

    def test_csv_round_trip(self, sample_tasks):
        """Test that CSV can be re-parsed."""
        manager = ExportManager()
        csv_data = manager.export_tasks(sample_tasks, format="csv")

        reader = csv.DictReader(StringIO(csv_data))
        rows = list(reader)

        assert len(rows) == len(sample_tasks)
        assert rows[0]["Title"] == sample_tasks[0].title

    def test_json_round_trip(self, sample_tasks):
        """Test that JSON can be re-parsed."""
        manager = ExportManager()
        json_data = manager.export_tasks(sample_tasks, format="json")

        data = json.loads(json_data)
        assert len(data) == len(sample_tasks)
        assert data[0]["title"] == sample_tasks[0].title

    def test_special_characters_in_csv(self, tmp_project):
        """Test CSV export with special characters."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create task with special characters
        task_id = tracker.create_task(goal_id, 'Task "with quotes"', "Description, with, commas")
        task = tracker.get_task(task_id)

        exporter = CSVExporter()
        csv_data = exporter.export_tasks([task])

        reader = csv.DictReader(StringIO(csv_data))
        rows = list(reader)
        assert rows[0]["Title"] == 'Task "with quotes"'

    def test_special_characters_in_json(self, tmp_project):
        """Test JSON export with special characters."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        task_id = tracker.create_task(goal_id, "Task with 日本語", "Unicode characters ñ é")
        task = tracker.get_task(task_id)

        exporter = JSONExporter()
        json_data = exporter.export_tasks([task])

        data = json.loads(json_data)
        assert "日本語" in data[0]["title"]


class TestExportEdgeCases:
    """Test edge cases in export."""

    def test_export_empty_task_list(self):
        """Test exporting empty task list."""
        manager = ExportManager()

        for format in manager.get_supported_formats():
            data = manager.export_tasks([], format=format)
            assert isinstance(data, str)

    def test_export_empty_metrics(self):
        """Test exporting empty metrics."""
        manager = ExportManager()

        for format in manager.get_supported_formats():
            data = manager.export_metrics({}, format=format)
            assert isinstance(data, str)
