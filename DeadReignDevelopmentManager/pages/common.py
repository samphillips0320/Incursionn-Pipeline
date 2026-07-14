from __future__ import annotations

from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from ui import theme
from ui.components import (
    create_empty_state,
    create_page_title,
    create_primary_button,
    create_search_box,
    create_small_label,
)
from ui.detail_panel import DetailPanel
from ui.layout import StandardPage


def build_placeholder_page(
    parent: ctk.CTkBaseClass,
    *,
    title: str,
    description: str,
    empty_title: str,
    empty_message: str,
    search_placeholder: str = "Search...",
    primary_button_text: str | None = None,
    primary_button_command: Callable[[], Any] | None = None,
    show_details: bool = False,
    detail_title: str = "Details",
    detail_empty_message: str = "Select an item to view its details.",
    show_toolbar: bool = True,
    scroll_main: bool = False,
) -> StandardPage:
    """
    Build a consistent temporary page for the application shell.

    These pages verify navigation, resizing, spacing, and shared styling
    before the full page features are implemented.
    """

    page = StandardPage(
        parent,
        show_details=show_details,
        scroll_main=scroll_main,
    )
    page.pack(
        fill="both",
        expand=True,
    )

    # -----------------------------------------------------
    # PAGE HEADER
    # -----------------------------------------------------

    title_label = create_page_title(
        page.header,
        title,
    )
    title_label.grid(
        row=0,
        column=0,
        sticky="w",
    )

    description_label = create_small_label(
        page.header,
        description,
        muted=True,
    )
    description_label.grid(
        row=1,
        column=0,
        pady=(4, 0),
        sticky="w",
    )

    # -----------------------------------------------------
    # TOOLBAR
    # -----------------------------------------------------

    if show_toolbar:
        page.toolbar.grid_columnconfigure(0, weight=1)

        search_box = create_search_box(
            page.toolbar,
            placeholder=search_placeholder,
            width=300,
        )
        search_box.grid(
            row=0,
            column=0,
            sticky="w",
        )

        if primary_button_text:
            action_button = create_primary_button(
                page.toolbar,
                primary_button_text,
                primary_button_command,
                width=135,
            )
            action_button.grid(
                row=0,
                column=1,
                padx=(theme.SECTION_GAP, 0),
                sticky="e",
            )
    else:
        page.toolbar.grid_remove()

    # -----------------------------------------------------
    # MAIN CONTENT
    # -----------------------------------------------------

    page.main.grid_rowconfigure(0, weight=1)

    empty_state = create_empty_state(
        page.main,
        title=empty_title,
        message=empty_message,
    )
    empty_state.grid(
        row=0,
        column=0,
        sticky="nsew",
    )

    # -----------------------------------------------------
    # DETAIL PANEL
    # -----------------------------------------------------

    if show_details and page.details is not None:
        detail_panel = DetailPanel(
            page.details,
            title=detail_title,
            empty_message=detail_empty_message,
        )
        detail_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        page.detail_panel = detail_panel
    else:
        page.detail_panel = None

    return page