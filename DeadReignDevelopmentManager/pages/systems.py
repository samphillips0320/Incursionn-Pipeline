import customtkinter as ctk

from pages.common import build_placeholder_page


def show_systems(
    parent: ctk.CTkBaseClass,
):
    """Display gameplay systems and technical architecture."""
    return build_placeholder_page(
        parent,
        title="Systems",
        description="Document gameplay systems and the architecture behind them.",
        empty_title="Systems library ready",
        empty_message=(
            "Inventory, crafting, weapons, AI, building, animation, world "
            "systems, and their technical relationships will appear here."
        ),
        search_placeholder="Search systems...",
        primary_button_text="+ New System",
        show_details=True,
        detail_title="System Details",
        detail_empty_message=(
            "Select a system to view its purpose, implementation status, "
            "dependencies, architecture, related tasks, and development logs."
        ),
    )