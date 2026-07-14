from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from storage import (
    load_development_entries,
    load_systems,
    load_tasks,
)


@dataclass
class DashboardData:
    """Normalized data used by the dashboard."""

    tasks: list[dict[str, Any]] = field(default_factory=list)
    development_entries: list[dict[str, Any]] = field(default_factory=list)
    systems: list[str] = field(default_factory=list)

    total_tasks: int = 0
    completed_tasks: int = 0
    open_tasks: int = 0
    in_progress_tasks: int = 0
    testing_tasks: int = 0
    completion_progress: float = 0.0

    current_focus: str = "No active task"
    current_system: str = "Unassigned"

    current_tasks: list[dict[str, Any]] = field(default_factory=list)
    latest_log: dict[str, Any] | None = None

    board_columns: dict[str, list[dict[str, Any]]] = field(
        default_factory=dict
    )

    task_creation_values: list[int] = field(
        default_factory=list
    )

    task_creation_labels: list[str] = field(
        default_factory=list
    )


STATUS_COLUMN_MAP = {
    "idea": "Ideas",
    "ideas": "Ideas",
    "backlog": "Ideas",
    "ideas / backlog": "Ideas",

    "planned": "Planned",
    "to do": "Planned",
    "todo": "Planned",
    "not started": "Planned",

    "in progress": "In Progress",
    "in-progress": "In Progress",
    "active": "In Progress",

    "testing": "Testing",
    "test": "Testing",
    "qa": "Testing",

    "complete": "Complete",
    "completed": "Complete",
    "done": "Complete",
}


def load_dashboard_data() -> DashboardData:
    """Load and normalize all data required by the Dashboard."""

    raw_tasks = load_tasks()
    raw_entries = load_development_entries()
    raw_systems = load_systems()

    tasks = [
        normalize_task(task)
        for task in raw_tasks
        if isinstance(task, dict)
    ]

    entries = [
        normalize_development_entry(entry)
        for entry in raw_entries
        if isinstance(entry, dict)
    ]

    total_tasks = len(tasks)

    completed_tasks = sum(
        1
        for task in tasks
        if task["normalized_status"] == "Complete"
    )

    in_progress_tasks = sum(
        1
        for task in tasks
        if task["normalized_status"] == "In Progress"
    )

    testing_tasks = sum(
        1
        for task in tasks
        if task["normalized_status"] == "Testing"
    )

    open_tasks = total_tasks - completed_tasks

    completion_progress = (
        completed_tasks / total_tasks
        if total_tasks
        else 0.0
    )

    open_task_list = [
        task
        for task in tasks
        if task["normalized_status"] != "Complete"
    ]

    open_task_list.sort(
        key=lambda task: task["created_sort_value"],
        reverse=True,
    )

    current_tasks = open_task_list[:5]

    if current_tasks:
        current_focus = current_tasks[0]["title"]
        current_system = current_tasks[0]["system"]
    else:
        current_focus = "No active task"
        current_system = "Unassigned"

    board_columns = {
        "Ideas": [],
        "Planned": [],
        "In Progress": [],
        "Testing": [],
        "Complete": [],
    }

    sorted_tasks = sorted(
        tasks,
        key=lambda task: task["created_sort_value"],
        reverse=True,
    )

    for task in sorted_tasks:
        column = task["normalized_status"]

        if column not in board_columns:
            column = "Planned"

        board_columns[column].append(task)

    # Show only the newest few tasks in each dashboard preview column.
    for column_name in board_columns:
        board_columns[column_name] = board_columns[column_name][:3]

    # Entries are appended by storage.py, so the final entry is the newest.
    latest_log = entries[-1] if entries else None

    task_creation_values, task_creation_labels = (
        build_task_creation_history(
            tasks,
            days=14,
        )
    )

    return DashboardData(
        tasks=tasks,
        development_entries=entries,
        systems=raw_systems,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        open_tasks=open_tasks,
        in_progress_tasks=in_progress_tasks,
        testing_tasks=testing_tasks,
        completion_progress=completion_progress,
        current_focus=current_focus,
        current_system=current_system,
        current_tasks=current_tasks,
        latest_log=latest_log,
        board_columns=board_columns,
        task_creation_values=task_creation_values,
        task_creation_labels=task_creation_labels,
    )

def build_task_creation_history(
    tasks: list[dict[str, Any]],
    *,
    days: int = 14,
) -> tuple[list[int], list[str]]:
    """Count tasks created during the most recent days."""
    from datetime import timedelta

    today = datetime.now().date()

    date_range = [
        today - timedelta(days=offset)
        for offset in reversed(range(days))
    ]

    counts = {
        date_value: 0
        for date_value in date_range
    }

    for task in tasks:
        created_value = task.get(
            "created_sort_value",
            datetime.min,
        )

        if created_value == datetime.min:
            continue

        created_date = created_value.date()

        if created_date in counts:
            counts[created_date] += 1

    values = [
        counts[date_value]
        for date_value in date_range
    ]

    labels = [
        date_value.strftime("%b %d")
        for date_value in date_range
    ]

    return values, labels


def normalize_task(task: dict[str, Any]) -> dict[str, Any]:
    """Return a safe, normalized task dictionary."""

    status = str(task.get("status", "Planned")).strip()
    normalized_status = STATUS_COLUMN_MAP.get(
        status.lower(),
        "Planned",
    )

    return {
        **task,
        "id": str(task.get("id", "")),
        "title": str(
            task.get("title", "Untitled Task")
        ).strip() or "Untitled Task",
        "system": str(
            task.get("system", "Unassigned")
        ).strip() or "Unassigned",
        "priority": str(
            task.get("priority", "Low")
        ).strip() or "Low",
        "status": status,
        "normalized_status": normalized_status,
        "notes": str(task.get("notes", "")).strip(),
        "created_at": str(task.get("created_at", "")).strip(),
        "completed_at": task.get("completed_at"),
        "created_sort_value": parse_task_datetime(
            task.get("created_at")
        ),
    }


def normalize_development_entry(
    entry: dict[str, Any],
) -> dict[str, Any]:
    """Return a safe, normalized development-log entry."""

    return {
        **entry,
        "date": str(entry.get("date", "")).strip(),
        "system": str(
            entry.get("system", "Unassigned")
        ).strip() or "Unassigned",
        "work_completed": str(
            entry.get("work_completed", "")
        ).strip(),
        "problems": str(
            entry.get("problems", "")
        ).strip(),
        "solution": str(
            entry.get("solution", "")
        ).strip(),
        "next_steps": str(
            entry.get("next_steps", "")
        ).strip(),
        "comments": str(
            entry.get("comments", "")
        ).strip(),
        "screenshot_captured": bool(
            entry.get("screenshot_captured", False)
        ),
        "video_recorded": bool(
            entry.get("video_recorded", False)
        ),
        "git_commit_created": bool(
            entry.get("git_commit_created", False)
        ),
        "portfolio_worthy": bool(
            entry.get("portfolio_worthy", False)
        ),
    }


def parse_task_datetime(value: Any) -> datetime:
    """Parse the current task timestamp format safely."""

    if not value:
        return datetime.min

    value_string = str(value).strip()

    supported_formats = (
        "%m-%d-%y %H:%M:%S",
        "%m-%d-%Y %H:%M:%S",
        "%m/%d/%Y",
        "%Y-%m-%d",
    )

    for date_format in supported_formats:
        try:
            return datetime.strptime(
                value_string,
                date_format,
            )
        except ValueError:
            continue



    return datetime.min