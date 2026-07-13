import customtkinter as ctk

from pages.common import build_placeholder_page


def show_development_log(
    parent: ctk.CTkBaseClass,
):
    """Display the chronological development history."""
    return build_placeholder_page(
        parent,
        title="Development Log",
        description="Preserve the living history of the project.",
        empty_title="Development timeline ready",
        empty_message=(
            "Development entries, accomplishments, challenges, time spent, "
            "screenshots, videos, commits, and related tasks will appear here."
        ),
        search_placeholder="Search development logs...",
        primary_button_text="+ New Entry",
        show_details=True,
        detail_title="Log Entry",
        detail_empty_message=(
            "Select an entry to view its full notes, attachments, related "
            "tasks, milestone, system, and development time."
        ),
    )