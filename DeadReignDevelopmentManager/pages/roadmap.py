import customtkinter as ctk

from pages.common import build_placeholder_page


def show_roadmap(
    parent: ctk.CTkBaseClass,
):
    """Display the project roadmap."""
    return build_placeholder_page(
        parent,
        title="Roadmap",
        description="Track phases, milestones, targets, and long-term progress.",
        empty_title="Roadmap structure ready",
        empty_message=(
            "Development phases and milestones will appear here as a "
            "visual timeline connected to systems and tasks."
        ),
        search_placeholder="Search milestones...",
        primary_button_text="+ New Milestone",
        show_details=True,
        detail_title="Milestone Details",
        detail_empty_message=(
            "Select a milestone to view its goals, target dates, "
            "completion status, and associated tasks."
        ),
    )