import customtkinter as ctk

from pages.common import build_placeholder_page


def show_task_board(
    parent: ctk.CTkBaseClass,
):
    """Display the task-management board."""
    return build_placeholder_page(
        parent,
        title="Task Board",
        description="Plan, organize, and complete development work.",
        empty_title="Task board coming next",
        empty_message=(
            "Tasks will be organized into active workflow columns, "
            "with completed work archived toward the bottom."
        ),
        search_placeholder="Search tasks...",
        primary_button_text="+ New Task",
        show_details=True,
        detail_title="Task Details",
        detail_empty_message=(
            "Select a task to view its description, system, priority, "
            "roadmap milestone, and related development logs."
        ),
    )











