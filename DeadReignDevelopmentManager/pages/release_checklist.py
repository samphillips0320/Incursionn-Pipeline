import customtkinter as ctk

from pages.common import build_placeholder_page


def show_release_checklist(
    parent: ctk.CTkBaseClass,
):
    """Display the final release-readiness checklist."""
    return build_placeholder_page(
        parent,
        title="Release Checklist",
        description="Track every requirement standing between development and launch.",
        empty_title="Launch control room ready",
        empty_message=(
            "Build verification, QA, storefront preparation, marketing, "
            "accessibility, legal requirements, and final release gates "
            "will be tracked here."
        ),
        search_placeholder="Search release requirements...",
        primary_button_text="+ Add Requirement",
        show_details=True,
        detail_title="Release Requirement",
        detail_empty_message=(
            "Select a requirement to view its completion criteria, status, "
            "owner, evidence, blockers, and related tasks."
        ),
    )