import customtkinter as ctk

from pages.common import build_placeholder_page


def show_knowledge_base(
    parent: ctk.CTkBaseClass,
):
    """Display project research and Unreal Engine notes."""
    return build_placeholder_page(
        parent,
        title="Knowledge Base",
        description="Keep Unreal Engine discoveries and project research searchable.",
        empty_title="Knowledge base ready",
        empty_message=(
            "Technical notes, tutorials, research, useful links, solutions, "
            "and lessons learned will be organized here."
        ),
        search_placeholder="Search knowledge articles...",
        primary_button_text="+ New Article",
        show_details=True,
        detail_title="Article",
        detail_empty_message=(
            "Select an article to read its notes, linked resources, tags, "
            "related systems, and associated tasks."
        ),
    )