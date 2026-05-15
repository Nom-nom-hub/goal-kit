"""Export Goal Kit data in multiple formats.

This module provides exporters for converting Goal Kit data (tasks, reports,
metrics) into various formats (CSV, JSON, Markdown, plaintext).
"""

import json
import csv
from io import StringIO
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from datetime import datetime

from .models import Task, TaskStatus
from .reporting import Report, Insight


class BaseExporter(ABC):
    """Abstract base class for exporters."""

    @abstractmethod
    def export_tasks(self, tasks: List[Task]) -> str:
        """Export tasks to the target format.

        Args:
            tasks: List of tasks to export.

        Returns:
            String representation in target format.
        """
        pass

    @abstractmethod
    def export_report(self, report: Report) -> str:
        """Export a report to the target format.

        Args:
            report: Report to export.

        Returns:
            String representation in target format.
        """
        pass

    @abstractmethod
    def export_metrics(self, metrics: Dict[str, Any]) -> str:
        """Export metrics to the target format.

        Args:
            metrics: Dictionary of metrics to export.

        Returns:
            String representation in target format.
        """
        pass


class CSVExporter(BaseExporter):
    """Export data to CSV format."""

    def export_tasks(self, tasks: List[Task]) -> str:
        """Export tasks to CSV.

        Args:
            tasks: List of tasks to export.

        Returns:
            CSV-formatted string.
        """
        output = StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow([
            "ID",
            "Title",
            "Description",
            "Status",
            "Estimated Hours",
            "Created",
            "Updated",
            "Completed",
            "Goal ID",
            "Depends On",
        ])

        # Rows
        for task in tasks:
            writer.writerow([
                task.id[:8],
                task.title,
                task.description,
                task.status.value,
                task.estimated_hours,
                task.created_at.isoformat() if task.created_at else "",
                task.updated_at.isoformat() if task.updated_at else "",
                task.completed_at.isoformat() if task.completed_at else "",
                task.goal_id[:8],
                task.depends_on[:8] if task.depends_on else "",
            ])

        return output.getvalue()

    def export_report(self, report: Report) -> str:
        """Export report to CSV.

        Args:
            report: Report to export.

        Returns:
            CSV-formatted string.
        """
        output = StringIO()
        writer = csv.writer(output)

        # Header section
        writer.writerow(["Report:", report.title])
        writer.writerow(["Type:", report.report_type.value])
        writer.writerow(["Generated:", report.generated_at.isoformat()])
        writer.writerow(["Period Start:", report.period_start.isoformat()])
        writer.writerow(["Period End:", report.period_end.isoformat()])
        writer.writerow([])

        # Summary section
        writer.writerow(["Summary"])
        for key, value in report.summary.items():
            writer.writerow([key, value])
        writer.writerow([])

        # Metrics section
        writer.writerow(["Metrics"])
        for key, value in report.metrics.items():
            writer.writerow([key, value])
        writer.writerow([])

        # Insights section
        if report.insights:
            writer.writerow(["Insights"])
            writer.writerow(["Type", "Title", "Severity", "Description", "Value"])
            for insight in report.insights:
                writer.writerow([
                    insight.type.value,
                    insight.title,
                    insight.severity.value,
                    insight.description,
                    insight.value,
                ])

        return output.getvalue()

    def export_metrics(self, metrics: Dict[str, Any]) -> str:
        """Export metrics to CSV.

        Args:
            metrics: Dictionary of metrics to export.

        Returns:
            CSV-formatted string.
        """
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(["Metric", "Value"])
        for key, value in metrics.items():
            writer.writerow([key, value])

        return output.getvalue()


class JSONExporter(BaseExporter):
    """Export data to JSON format."""

    def export_tasks(self, tasks: List[Task]) -> str:
        """Export tasks to JSON.

        Args:
            tasks: List of tasks to export.

        Returns:
            JSON-formatted string.
        """
        data = []
        for task in tasks:
            data.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "estimated_hours": task.estimated_hours,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "goal_id": task.goal_id,
                "depends_on": task.depends_on,
            })

        return json.dumps(data, indent=2)

    def export_report(self, report: Report) -> str:
        """Export report to JSON.

        Args:
            report: Report to export.

        Returns:
            JSON-formatted string.
        """
        data = {
            "title": report.title,
            "type": report.report_type.value,
            "generated_at": report.generated_at.isoformat(),
            "period_start": report.period_start.isoformat(),
            "period_end": report.period_end.isoformat(),
            "summary": report.summary,
            "metrics": report.metrics,
            "insights": [
                {
                    "type": i.type.value,
                    "title": i.title,
                    "description": i.description,
                    "severity": i.severity.value,
                    "value": str(i.value),
                    "recommendation": i.recommendation,
                }
                for i in report.insights
            ],
        }

        return json.dumps(data, indent=2)

    def export_metrics(self, metrics: Dict[str, Any]) -> str:
        """Export metrics to JSON.

        Args:
            metrics: Dictionary of metrics to export.

        Returns:
            JSON-formatted string.
        """
        return json.dumps(metrics, indent=2)


class MarkdownExporter(BaseExporter):
    """Export data to Markdown format."""

    def export_tasks(self, tasks: List[Task]) -> str:
        """Export tasks to Markdown.

        Args:
            tasks: List of tasks to export.

        Returns:
            Markdown-formatted string.
        """
        lines = ["# Tasks\n"]

        for task in tasks:
            status_icon = "✓" if task.status == TaskStatus.COMPLETED else "○"
            lines.append(f"## {status_icon} {task.title}\n")
            lines.append(f"- **Description**: {task.description}\n")
            lines.append(f"- **Status**: {task.status.value}\n")
            lines.append(f"- **Hours**: {task.estimated_hours}\n")
            if task.depends_on:
                lines.append(f"- **Depends on**: {task.depends_on[:8]}\n")
            lines.append("")

        return "\n".join(lines)

    def export_report(self, report: Report) -> str:
        """Export report to Markdown.

        Args:
            report: Report to export.

        Returns:
            Markdown-formatted string.
        """
        lines = [
            f"# {report.title}\n",
            f"**Type**: {report.report_type.value}\n",
            f"**Generated**: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"**Period**: {report.period_start.date()} to {report.period_end.date()}\n",
            "\n",
        ]

        # Summary section
        lines.append("## Summary\n")
        for key, value in report.summary.items():
            lines.append(f"- **{key}**: {value}\n")
        lines.append("")

        # Metrics section
        lines.append("## Metrics\n")
        for key, value in report.metrics.items():
            lines.append(f"- **{key}**: {value}\n")
        lines.append("")

        # Insights section
        if report.insights:
            lines.append("## Insights\n")
            for insight in report.insights:
                severity_emoji = {"info": "ℹ️", "warning": "⚠️", "alert": "🚨"}.get(
                    insight.severity.value, "•"
                )
                lines.append(f"### {severity_emoji} {insight.title}\n")
                lines.append(f"{insight.description}\n")
                if insight.recommendation:
                    lines.append(f"> **Recommendation**: {insight.recommendation}\n")
                lines.append("")

        return "\n".join(lines)

    def export_metrics(self, metrics: Dict[str, Any]) -> str:
        """Export metrics to Markdown.

        Args:
            metrics: Dictionary of metrics to export.

        Returns:
            Markdown-formatted string.
        """
        lines = ["# Metrics\n"]

        for key, value in metrics.items():
            lines.append(f"- **{key}**: {value}\n")

        return "\n".join(lines)


class TextExporter(BaseExporter):
    """Export data to plain text format."""

    def export_tasks(self, tasks: List[Task]) -> str:
        """Export tasks to plain text.

        Args:
            tasks: List of tasks to export.

        Returns:
            Plain text string.
        """
        lines = ["TASKS\n"]

        for task in tasks:
            status_icon = "[✓]" if task.status == TaskStatus.COMPLETED else "[ ]"
            lines.append(f"{status_icon} {task.title}")
            lines.append(f"    {task.description}")
            lines.append(f"    Status: {task.status.value} | Hours: {task.estimated_hours}")
            if task.depends_on:
                lines.append(f"    Depends on: {task.depends_on[:8]}")
            lines.append("")

        return "\n".join(lines)

    def export_report(self, report: Report) -> str:
        """Export report to plain text.

        Args:
            report: Report to export.

        Returns:
            Plain text string.
        """
        lines = [
            report.title,
            "=" * len(report.title),
            "",
            f"Type: {report.report_type.value}",
            f"Generated: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Period: {report.period_start.date()} to {report.period_end.date()}",
            "",
            "SUMMARY",
            "-" * 7,
        ]

        for key, value in report.summary.items():
            lines.append(f"{key}: {value}")

        lines.extend(["", "METRICS", "-" * 7])
        for key, value in report.metrics.items():
            lines.append(f"{key}: {value}")

        if report.insights:
            lines.extend(["", "INSIGHTS", "-" * 8])
            for insight in report.insights:
                lines.append(f"[{insight.severity.value.upper()}] {insight.title}")
                lines.append(f"  {insight.description}")
                if insight.recommendation:
                    lines.append(f"  Recommendation: {insight.recommendation}")

        return "\n".join(lines)

    def export_metrics(self, metrics: Dict[str, Any]) -> str:
        """Export metrics to plain text.

        Args:
            metrics: Dictionary of metrics to export.

        Returns:
            Plain text string.
        """
        lines = ["METRICS", "=======", ""]

        for key, value in metrics.items():
            lines.append(f"{key}: {value}")

        return "\n".join(lines)


class ExportManager:
    """Manage exports in multiple formats."""

    def __init__(self):
        """Initialize ExportManager with all available exporters."""
        self.exporters = {
            "csv": CSVExporter(),
            "json": JSONExporter(),
            "markdown": MarkdownExporter(),
            "text": TextExporter(),
        }

    def export_tasks(self, tasks: List[Task], format: str = "csv") -> str:
        """Export tasks to specified format.

        Args:
            tasks: List of tasks to export.
            format: Export format (csv, json, markdown, text).

        Returns:
            Exported data as string.

        Raises:
            ValueError: If format not supported.
        """
        if format not in self.exporters:
            raise ValueError(f"Unsupported format: {format}")

        return self.exporters[format].export_tasks(tasks)

    def export_report(self, report: Report, format: str = "markdown") -> str:
        """Export report to specified format.

        Args:
            report: Report to export.
            format: Export format (csv, json, markdown, text).

        Returns:
            Exported data as string.

        Raises:
            ValueError: If format not supported.
        """
        if format not in self.exporters:
            raise ValueError(f"Unsupported format: {format}")

        return self.exporters[format].export_report(report)

    def export_metrics(self, metrics: Dict[str, Any], format: str = "csv") -> str:
        """Export metrics to specified format.

        Args:
            metrics: Dictionary of metrics to export.
            format: Export format (csv, json, markdown, text).

        Returns:
            Exported data as string.

        Raises:
            ValueError: If format not supported.
        """
        if format not in self.exporters:
            raise ValueError(f"Unsupported format: {format}")

        return self.exporters[format].export_metrics(metrics)

    def get_supported_formats(self) -> List[str]:
        """Get list of supported export formats.

        Returns:
            List of format names.
        """
        return list(self.exporters.keys())
