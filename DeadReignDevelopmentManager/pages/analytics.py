import customtkinter as ctk

from pages.common import build_placeholder_page


def show_analytics(
    parent: ctk.CTkBaseClass,
):
    """Display detailed project progress analytics."""
    return build_placeholder_page(
        parent,
        title="Progress Analytics",
        description="Turn project history into meaningful development insight.",
        empty_title="Analytics workspace ready",
        empty_message=(
            "Task velocity, time spent, system progress, milestone completion, "
            "development trends, and project health will appear here."
        ),
        search_placeholder="Filter analytics...",
        show_details=True,
        detail_title="Project Summary",
        detail_empty_message=(
            "Detailed summaries and selected chart information will appear "
            "here as project data accumulates."
        ),
    )