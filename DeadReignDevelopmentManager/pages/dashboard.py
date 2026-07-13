# pages/dashboard.py

import customtkinter as ctk

from pages.common import build_placeholder_page


def show_dashboard(
    parent: ctk.CTkBaseClass,
):
    """Display the application dashboard."""
    return build_placeholder_page(
        parent,
        title="Dashboard",
        description="Your command center for Dead Reign: Outbreak.",
        empty_title="Dashboard foundation ready",
        empty_message=(
            "Project progress, current priorities, recent development "
            "activity, and basic analytics will appear here."
        ),
        show_toolbar=False,
        show_details=False,
    )



