from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from storage import load_systems, load_tasks


STATUS_MAP = {
    "idea": "Ideas / Backlog",
    "ideas": "Ideas / Backlog",
    "backlog": "Ideas / Backlog",
    "ideas / backlog": "Ideas / Backlog",

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


@dataclass
class TaskBoardData:
    """Normalized data used by the Task Board."""

    tasks: list[dict[str, Any]] = field(
        default_factory=list
    )

    systems: list[str] = field(
        default_factory=list
    )

    columns: dict[str, list[dict[str, Any]]] = field(
        default_factory=dict
    )


def load_task_board_data() -> TaskBoardData:
    """Load and normalize saved Task Board data."""

    raw_tasks = load_tasks()
    raw_systems = load_systems()

    tasks = [
        normalize_task(task)
        for task in raw_tasks
        if isinstance(task, dict)
    ]

    tasks.sort(
        key=lambda task: task["created_sort_value"],
        reverse=True,
    )

    columns = {
        "Ideas / Backlog": [],
        "Planned": [],
        "In Progress": [],
        "Testing": [],
        "Complete": [],
    }

    for task in tasks:
        status = task["normalized_status"]

        if status not in columns:
            status = "Planned"

        columns[status].append(task)

    systems = sorted(
        {
            str(system).strip()
            for system in raw_systems
            if str(system).strip()
        }
    )

    return TaskBoardData(
        tasks=tasks,
        systems=systems,
        columns=columns,
    )


def normalize_task(
    task: dict[str, Any],
) -> dict[str, Any]:
    """Return a safe Task Board task dictionary."""

    raw_status = str(
        task.get("status", "Planned")
    ).strip()

    normalized_status = STATUS_MAP.get(
        raw_status.lower(),
        "Planned",
    )

    return {
        **task,
        "id": str(
            task.get("id", "")
        ),
        "title": (
            str(
                task.get(
                    "title",
                    "Untitled Task",
                )
            ).strip()
            or "Untitled Task"
        ),
        "system": (
            str(
                task.get(
                    "system",
                    "Unassigned",
                )
            ).strip()
            or "Unassigned"
        ),
        "priority": (
            str(
                task.get(
                    "priority",
                    "Low",
                )
            ).strip()
            or "Low"
        ),
        "status": raw_status,
        "normalized_status": normalized_status,
        "notes": str(
            task.get("notes", "")
        ).strip(),
        "created_at": str(
            task.get("created_at", "")
        ).strip(),
        "completed_at": task.get(
            "completed_at"
        ),
        "created_sort_value": parse_task_datetime(
            task.get("created_at")
        ),
    }


def parse_task_datetime(
    value: Any,
) -> datetime:
    """Parse saved task dates safely."""

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