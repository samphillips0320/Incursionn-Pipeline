from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

import customtkinter as ctk

from ui import theme


# =========================================================
# LABELS AND TEXT
# =========================================================

def create_page_title(
    parent: ctk.CTkBaseClass,
    text: str,
) -> ctk.CTkLabel:
    """Create the main title displayed at the top of a page."""
    return ctk.CTkLabel(
        parent,
        text=text,
        font=theme.FONT_PAGE_TITLE,
        text_color=theme.TEXT_PRIMARY,
        anchor="w",
    )


def create_section_title(
    parent: ctk.CTkBaseClass,
    text: str,
) -> ctk.CTkLabel:
    """Create a title for a page section or card group."""
    return ctk.CTkLabel(
        parent,
        text=text,
        font=theme.FONT_SECTION_TITLE,
        text_color=theme.TEXT_PRIMARY,
        anchor="w",
    )


def create_card_title(
    parent: ctk.CTkBaseClass,
    text: str,
) -> ctk.CTkLabel:
    """Create a standard title used inside a card."""
    return ctk.CTkLabel(
        parent,
        text=text,
        font=theme.FONT_CARD_TITLE,
        text_color=theme.TEXT_PRIMARY,
        anchor="w",
    )


def create_body_label(
    parent: ctk.CTkBaseClass,
    text: str,
    *,
    muted: bool = False,
    bold: bool = False,
    wraplength: int = 0,
    anchor: str = "w",
    justify: str = "left",
) -> ctk.CTkLabel:
    """Create a standard body-text label."""
    text_color = theme.TEXT_MUTED if muted else theme.TEXT_SECONDARY
    font = theme.FONT_BODY_BOLD if bold else theme.FONT_BODY

    return ctk.CTkLabel(
        parent,
        text=text,
        font=font,
        text_color=text_color,
        wraplength=wraplength,
        anchor=anchor,
        justify=justify,
    )


def create_small_label(
    parent: ctk.CTkBaseClass,
    text: str,
    *,
    muted: bool = True,
    bold: bool = False,
    anchor: str = "w",
) -> ctk.CTkLabel:
    """Create smaller supporting text."""
    text_color = theme.TEXT_MUTED if muted else theme.TEXT_SECONDARY
    font = theme.FONT_SMALL_BOLD if bold else theme.FONT_SMALL

    return ctk.CTkLabel(
        parent,
        text=text,
        font=font,
        text_color=text_color,
        anchor=anchor,
    )


# =========================================================
# CONTAINERS
# =========================================================

def create_card(
    parent: ctk.CTkBaseClass,
    *,
    fg_color: str | None = None,
    border_color: str | None = None,
    corner_radius: int | None = None,
) -> ctk.CTkFrame:
    """Create a standard bordered content card."""
    return ctk.CTkFrame(
        parent,
        fg_color=fg_color or theme.CARD_BG,
        border_color=border_color or theme.CARD_BORDER,
        border_width=theme.BORDER_WIDTH,
        corner_radius=(
            corner_radius
            if corner_radius is not None
            else theme.CARD_CORNER_RADIUS
        ),
    )


def create_toolbar(
    parent: ctk.CTkBaseClass,
) -> ctk.CTkFrame:
    """Create a transparent frame for search, filters, and actions."""
    return ctk.CTkFrame(
        parent,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
    )


def create_scroll_frame(
    parent: ctk.CTkBaseClass,
    *,
    fg_color: str | None = None,
    corner_radius: int | None = None,
) -> ctk.CTkScrollableFrame:
    """Create a standard scrollable content area."""
    return ctk.CTkScrollableFrame(
        parent,
        fg_color=fg_color or theme.TRANSPARENT,
        corner_radius=(
            corner_radius
            if corner_radius is not None
            else theme.CARD_CORNER_RADIUS
        ),
        scrollbar_button_color=theme.CARD_BORDER,
        scrollbar_button_hover_color=theme.TEXT_MUTED,
    )


def create_empty_state(
    parent: ctk.CTkBaseClass,
    *,
    title: str,
    message: str,
) -> ctk.CTkFrame:
    """Create a card shown when a page or section has no content."""
    frame = create_card(parent)

    frame.grid_columnconfigure(0, weight=1)

    title_label = create_card_title(frame, title)
    title_label.grid(
        row=0,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=(theme.CARD_PADDING_Y, 4),
        sticky="w",
    )

    message_label = create_body_label(
        frame,
        message,
        muted=True,
        wraplength=500,
    )
    message_label.grid(
        row=1,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=(0, theme.CARD_PADDING_Y),
        sticky="w",
    )

    return frame


# =========================================================
# BUTTONS
# =========================================================

def create_primary_button(
    parent: ctk.CTkBaseClass,
    text: str,
    command: Callable[[], Any] | None = None,
    *,
    width: int = 120,
) -> ctk.CTkButton:
    """Create the main orange action button."""
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=theme.BUTTON_HEIGHT,
        fg_color=theme.ACCENT_ORANGE,
        hover_color=theme.ACCENT_ORANGE_HOVER,
        text_color=theme.TEXT_PRIMARY,
        corner_radius=theme.BUTTON_CORNER_RADIUS,
        font=theme.FONT_BODY_BOLD,
        border_width=0,
    )


def create_secondary_button(
    parent: ctk.CTkBaseClass,
    text: str,
    command: Callable[[], Any] | None = None,
    *,
    width: int = 120,
) -> ctk.CTkButton:
    """Create a dark outlined secondary action button."""
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=theme.BUTTON_HEIGHT,
        fg_color=theme.CARD_BG,
        hover_color=theme.CARD_BG_HOVER,
        text_color=theme.TEXT_PRIMARY,
        border_width=theme.BORDER_WIDTH,
        border_color=theme.CARD_BORDER,
        corner_radius=theme.BUTTON_CORNER_RADIUS,
        font=theme.FONT_BODY,
    )


def create_danger_button(
    parent: ctk.CTkBaseClass,
    text: str,
    command: Callable[[], Any] | None = None,
    *,
    width: int = 120,
) -> ctk.CTkButton:
    """Create a destructive action button."""
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=theme.BUTTON_HEIGHT,
        fg_color=theme.ERROR,
        hover_color="#C93636",
        text_color=theme.TEXT_PRIMARY,
        corner_radius=theme.BUTTON_CORNER_RADIUS,
        font=theme.FONT_BODY_BOLD,
        border_width=0,
    )


def create_icon_button(
    parent: ctk.CTkBaseClass,
    text: str,
    command: Callable[[], Any] | None = None,
    *,
    width: int = 38,
) -> ctk.CTkButton:
    """Create a compact button for icons or short symbols."""
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=theme.BUTTON_HEIGHT,
        fg_color=theme.CARD_BG,
        hover_color=theme.CARD_BG_HOVER,
        text_color=theme.TEXT_PRIMARY,
        border_width=theme.BORDER_WIDTH,
        border_color=theme.CARD_BORDER,
        corner_radius=theme.BUTTON_CORNER_RADIUS,
        font=theme.FONT_BODY_BOLD,
    )


# =========================================================
# INPUTS
# =========================================================

def create_search_box(
    parent: ctk.CTkBaseClass,
    *,
    placeholder: str = "Search...",
    width: int = 260,
    textvariable: ctk.StringVar | None = None,
) -> ctk.CTkEntry:
    """Create the shared search field used across pages."""
    return ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        width=width,
        height=theme.INPUT_HEIGHT,
        fg_color=theme.INPUT_BG,
        border_color=theme.INPUT_BORDER,
        border_width=theme.BORDER_WIDTH,
        text_color=theme.TEXT_PRIMARY,
        placeholder_text_color=theme.TEXT_MUTED,
        corner_radius=theme.INPUT_CORNER_RADIUS,
        font=theme.FONT_BODY,
        textvariable=textvariable,
    )


def create_text_entry(
    parent: ctk.CTkBaseClass,
    *,
    placeholder: str = "",
    width: int = 220,
    textvariable: ctk.StringVar | None = None,
) -> ctk.CTkEntry:
    """Create a standard single-line text entry."""
    return ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        width=width,
        height=theme.INPUT_HEIGHT,
        fg_color=theme.INPUT_BG,
        border_color=theme.INPUT_BORDER,
        border_width=theme.BORDER_WIDTH,
        text_color=theme.TEXT_PRIMARY,
        placeholder_text_color=theme.TEXT_MUTED,
        corner_radius=theme.INPUT_CORNER_RADIUS,
        font=theme.FONT_BODY,
        textvariable=textvariable,
    )


def create_textbox(
    parent: ctk.CTkBaseClass,
    *,
    height: int = 130,
    wrap: str = "word",
) -> ctk.CTkTextbox:
    """Create a multiline text area."""
    return ctk.CTkTextbox(
        parent,
        height=height,
        fg_color=theme.INPUT_BG,
        border_color=theme.INPUT_BORDER,
        border_width=theme.BORDER_WIDTH,
        text_color=theme.TEXT_PRIMARY,
        corner_radius=theme.INPUT_CORNER_RADIUS,
        font=theme.FONT_BODY,
        wrap=wrap,
        scrollbar_button_color=theme.CARD_BORDER,
        scrollbar_button_hover_color=theme.TEXT_MUTED,
    )


def create_dropdown(
    parent: ctk.CTkBaseClass,
    values: Iterable[str],
    *,
    command: Callable[[str], Any] | None = None,
    variable: ctk.StringVar | None = None,
    width: int = 160,
) -> ctk.CTkOptionMenu:
    """Create a standard dropdown menu."""
    values_list = list(values)

    if not values_list:
        values_list = ["No options"]

    return ctk.CTkOptionMenu(
        parent,
        values=values_list,
        command=command,
        variable=variable,
        width=width,
        height=theme.INPUT_HEIGHT,
        fg_color=theme.INPUT_BG,
        button_color=theme.CARD_BORDER,
        button_hover_color=theme.CARD_BG_HOVER,
        dropdown_fg_color=theme.CARD_BG,
        dropdown_hover_color=theme.CARD_BG_HOVER,
        dropdown_text_color=theme.TEXT_PRIMARY,
        text_color=theme.TEXT_PRIMARY,
        corner_radius=theme.INPUT_CORNER_RADIUS,
        font=theme.FONT_BODY,
        dropdown_font=theme.FONT_BODY,
    )


def create_switch(
    parent: ctk.CTkBaseClass,
    text: str,
    *,
    command: Callable[[], Any] | None = None,
    variable: ctk.BooleanVar | None = None,
) -> ctk.CTkSwitch:
    """Create a standard toggle switch."""
    return ctk.CTkSwitch(
        parent,
        text=text,
        command=command,
        variable=variable,
        font=theme.FONT_BODY,
        text_color=theme.TEXT_PRIMARY,
        progress_color=theme.ACCENT_ORANGE,
        button_color=theme.TEXT_SECONDARY,
        button_hover_color=theme.TEXT_PRIMARY,
    )


# =========================================================
# VISUAL STATUS COMPONENTS
# =========================================================

def create_badge(
    parent: ctk.CTkBaseClass,
    text: str,
    *,
    color: str,
    text_color: str = theme.TEXT_PRIMARY,
) -> ctk.CTkLabel:
    """Create a small colored badge."""
    return ctk.CTkLabel(
        parent,
        text=f"  {text}  ",
        height=24,
        fg_color=color,
        text_color=text_color,
        corner_radius=4,
        font=theme.FONT_SMALL_BOLD,
    )


def create_status_badge(
    parent: ctk.CTkBaseClass,
    status: str,
) -> ctk.CTkLabel:
    """Create a badge using the configured status color."""
    color = theme.STATUS_COLORS.get(status, theme.TEXT_MUTED)

    return create_badge(
        parent,
        status,
        color=color,
    )


def create_priority_badge(
    parent: ctk.CTkBaseClass,
    priority: str,
) -> ctk.CTkLabel:
    """Create a badge using the configured priority color."""
    color = theme.PRIORITY_COLORS.get(priority, theme.TEXT_MUTED)

    return create_badge(
        parent,
        priority,
        color=color,
    )


def create_system_badge(
    parent: ctk.CTkBaseClass,
    system_name: str,
) -> ctk.CTkLabel:
    """Create a badge using the configured system color."""
    color = theme.SYSTEM_COLORS.get(system_name, theme.TEXT_MUTED)

    return create_badge(
        parent,
        system_name,
        color=color,
    )


def create_progress_bar(
    parent: ctk.CTkBaseClass,
    *,
    progress: float = 0.0,
    width: int = 200,
    height: int = 8,
    color: str | None = None,
) -> ctk.CTkProgressBar:
    """
    Create a progress bar.

    Progress should be between 0.0 and 1.0.
    """
    normalized_progress = max(0.0, min(progress, 1.0))

    progress_bar = ctk.CTkProgressBar(
        parent,
        width=width,
        height=height,
        fg_color=theme.INPUT_BG,
        progress_color=color or theme.ACCENT_ORANGE,
        corner_radius=height // 2,
    )

    progress_bar.set(normalized_progress)

    return progress_bar


# =========================================================
# INFORMATION DISPLAY
# =========================================================

def create_separator(
    parent: ctk.CTkBaseClass,
    *,
    orientation: str = "horizontal",
) -> ctk.CTkFrame:
    """Create a horizontal or vertical divider."""
    if orientation == "vertical":
        return ctk.CTkFrame(
            parent,
            width=1,
            fg_color=theme.CARD_BORDER,
            corner_radius=0,
        )

    return ctk.CTkFrame(
        parent,
        height=1,
        fg_color=theme.CARD_BORDER,
        corner_radius=0,
    )


def create_info_row(
    parent: ctk.CTkBaseClass,
    label_text: str,
    value_text: str,
    *,
    row: int,
) -> tuple[ctk.CTkLabel, ctk.CTkLabel]:
    """Create a two-column label/value row inside a grid container."""
    label = create_small_label(
        parent,
        label_text,
        muted=True,
        bold=True,
    )
    label.grid(
        row=row,
        column=0,
        padx=(0, 12),
        pady=4,
        sticky="w",
    )

    value = create_body_label(
        parent,
        value_text,
        muted=False,
    )
    value.grid(
        row=row,
        column=1,
        pady=4,
        sticky="w",
    )

    return label, value


def create_labeled_field(
    parent: ctk.CTkBaseClass,
    label_text: str,
    widget: ctk.CTkBaseClass,
    *,
    row: int,
    column: int = 0,
    columnspan: int = 1,
) -> None:
    """Place a label above an input widget using a shared layout."""
    label = create_small_label(
        parent,
        label_text,
        muted=False,
        bold=True,
    )
    label.grid(
        row=row,
        column=column,
        columnspan=columnspan,
        sticky="w",
        pady=(0, 5),
    )

    widget.grid(
        row=row + 1,
        column=column,
        columnspan=columnspan,
        sticky="ew",
        pady=(0, 12),
    )


# =========================================================
# COMPOSITE CARDS
# =========================================================

def create_stat_card(
    parent: ctk.CTkBaseClass,
    *,
    title: str,
    value: str,
    subtitle: str = "",
    accent_color: str | None = None,
) -> ctk.CTkFrame:
    """Create a compact metric card for dashboards and analytics."""
    card = create_card(parent)

    card.grid_columnconfigure(0, weight=1)

    accent = ctk.CTkFrame(
        card,
        width=4,
        fg_color=accent_color or theme.ACCENT_ORANGE,
        corner_radius=2,
    )
    accent.grid(
        row=0,
        column=0,
        rowspan=3,
        padx=(0, 12),
        pady=12,
        sticky="nsw",
    )

    title_label = create_small_label(
        card,
        title,
        muted=True,
        bold=True,
    )
    title_label.grid(
        row=0,
        column=1,
        padx=(0, theme.CARD_PADDING_X),
        pady=(theme.CARD_PADDING_Y, 2),
        sticky="w",
    )

    value_label = ctk.CTkLabel(
        card,
        text=value,
        font=(theme.FONT_FAMILY, 24, "bold"),
        text_color=theme.TEXT_PRIMARY,
        anchor="w",
    )
    value_label.grid(
        row=1,
        column=1,
        padx=(0, theme.CARD_PADDING_X),
        sticky="w",
    )

    if subtitle:
        subtitle_label = create_small_label(
            card,
            subtitle,
            muted=True,
        )
        subtitle_label.grid(
            row=2,
            column=1,
            padx=(0, theme.CARD_PADDING_X),
            pady=(2, theme.CARD_PADDING_Y),
            sticky="w",
        )

    return card


def create_progress_card(
    parent: ctk.CTkBaseClass,
    *,
    title: str,
    progress: float,
    detail_text: str = "",
    color: str | None = None,
) -> ctk.CTkFrame:
    """Create a card containing a title, percentage, and progress bar."""
    card = create_card(parent)

    card.grid_columnconfigure(0, weight=1)

    title_label = create_card_title(card, title)
    title_label.grid(
        row=0,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=(theme.CARD_PADDING_Y, 4),
        sticky="w",
    )

    percentage = f"{round(max(0.0, min(progress, 1.0)) * 100)}%"

    percentage_label = create_body_label(
        card,
        percentage,
        bold=True,
    )
    percentage_label.grid(
        row=0,
        column=1,
        padx=theme.CARD_PADDING_X,
        pady=(theme.CARD_PADDING_Y, 4),
        sticky="e",
    )

    progress_bar = create_progress_bar(
        card,
        progress=progress,
        color=color,
    )
    progress_bar.grid(
        row=1,
        column=0,
        columnspan=2,
        padx=theme.CARD_PADDING_X,
        pady=6,
        sticky="ew",
    )

    if detail_text:
        detail_label = create_small_label(
            card,
            detail_text,
            muted=True,
        )
        detail_label.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=theme.CARD_PADDING_X,
            pady=(2, theme.CARD_PADDING_Y),
            sticky="w",
        )

    return card