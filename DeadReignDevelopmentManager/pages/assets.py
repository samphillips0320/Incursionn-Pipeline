import customtkinter as ctk

from pages.common import build_placeholder_page


def show_assets(
    parent: ctk.CTkBaseClass,
):
    """Display the project asset library."""
    return build_placeholder_page(
        parent,
        title="Assets",
        description="Track models, animations, audio, materials, and licenses.",
        empty_title="Asset library ready",
        empty_message=(
            "Project assets will appear here with categories, source details, "
            "license information, usage status, and related systems."
        ),
        search_placeholder="Search assets...",
        primary_button_text="+ Add Asset",
        show_details=True,
        detail_title="Asset Details",
        detail_empty_message=(
            "Select an asset to view its source, type, file location, license, "
            "implementation status, and where it is used."
        ),
    )