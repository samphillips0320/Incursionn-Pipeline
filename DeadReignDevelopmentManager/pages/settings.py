import customtkinter as ctk

from pages.common import build_placeholder_page


def show_settings(
    parent: ctk.CTkBaseClass,
):
    """Display application and project settings."""
    return build_placeholder_page(
        parent,
        title="Settings",
        description="Configure DR Pipeline Management and project preferences.",
        empty_title="Settings foundation ready",
        empty_message=(
            "Appearance, project defaults, task behavior, data management, "
            "integrations, notifications, and application preferences "
            "will be configured here."
        ),
        show_toolbar=False,
        show_details=False,
        scroll_main=True,
    )