from __future__ import annotations

from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from ui import theme
from ui.components import (
    create_body_label,
    create_card,
    create_card_title,
    create_primary_button,
    create_secondary_button,
    create_separator,
    create_small_label,
)


class Inspector(ctk.CTkFrame):
    """
    Shared right-side Inspector used throughout the application.

    Pages can populate the Inspector with information about the
    currently selected task, system, asset, article, milestone,
    development log, or other project object.
    """

    def __init__(
        self,
        parent: ctk.CTkBaseClass,
        *,
        title: str = "Inspector",
        empty_title: str = "Nothing selected",
        empty_message: str = (
            "Select an item to inspect its details."
        ),
    ) -> None:
        super().__init__(
            parent,
            fg_color=theme.CARD_BG,
            border_color=theme.CARD_BORDER,
            border_width=theme.BORDER_WIDTH,
            corner_radius=theme.CARD_CORNER_RADIUS,
        )

        self.default_title = title
        self.empty_title = empty_title
        self.empty_message = empty_message

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_content()
        self._build_actions()

        self.show_empty_state()

    # =====================================================
    # BUILD METHODS
    # =====================================================

    def _build_header(self) -> None:
        """Create the Inspector header."""

        self.header = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        self.header.grid(
            row=0,
            column=0,
            padx=theme.CARD_PADDING_X,
            pady=(theme.CARD_PADDING_Y, 10),
            sticky="ew",
        )
        self.header.grid_columnconfigure(0, weight=1)

        self.title_label = create_card_title(
            self.header,
            self.default_title,
        )
        self.title_label.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.subtitle_label = create_small_label(
            self.header,
            "",
            muted=True,
        )
        self.subtitle_label.grid(
            row=1,
            column=0,
            pady=(3, 0),
            sticky="w",
        )
        self.subtitle_label.grid_remove()

        separator = create_separator(self)
        separator.grid(
            row=1,
            column=0,
            padx=theme.CARD_PADDING_X,
            sticky="ew",
        )

    def _build_content(self) -> None:
        """Create the scrollable Inspector content area."""

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
            scrollbar_button_color=theme.CARD_BORDER,
            scrollbar_button_hover_color=theme.TEXT_MUTED,
        )
        self.content.grid(
            row=2,
            column=0,
            padx=theme.CARD_PADDING_X,
            pady=theme.CARD_PADDING_Y,
            sticky="nsew",
        )
        self.content.grid_columnconfigure(0, weight=1)

    def _build_actions(self) -> None:
        """Create the bottom Inspector action area."""

        self.actions = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        self.actions.grid(
            row=3,
            column=0,
            padx=theme.CARD_PADDING_X,
            pady=(0, theme.CARD_PADDING_Y),
            sticky="ew",
        )
        self.actions.grid_columnconfigure(0, weight=1)
        self.actions.grid_columnconfigure(1, weight=1)

        self.actions.grid_remove()

    # =====================================================
    # GENERAL METHODS
    # =====================================================

    def clear(self) -> None:
        """Clear all Inspector content and actions."""

        for child in self.content.winfo_children():
            child.destroy()

        for child in self.actions.winfo_children():
            child.destroy()

        self.actions.grid_remove()

    def set_header(
        self,
        title: str,
        subtitle: str = "",
    ) -> None:
        """Update the Inspector title and subtitle."""

        self.title_label.configure(
            text=title,
        )

        self.subtitle_label.configure(
            text=subtitle,
        )

        if subtitle:
            self.subtitle_label.grid()
        else:
            self.subtitle_label.grid_remove()

    def show_empty_state(
        self,
        *,
        title: str | None = None,
        message: str | None = None,
    ) -> None:
        """Display the empty Inspector state."""

        self.clear()

        self.set_header(
            self.default_title,
        )

        empty_card = create_card(
            self.content,
            fg_color=theme.INPUT_BG,
        )
        empty_card.grid(
            row=0,
            column=0,
            sticky="ew",
        )
        empty_card.grid_columnconfigure(0, weight=1)

        create_card_title(
            empty_card,
            title or self.empty_title,
        ).grid(
            row=0,
            column=0,
            padx=theme.CARD_PADDING_X,
            pady=(theme.CARD_PADDING_Y, 5),
            sticky="w",
        )

        create_body_label(
            empty_card,
            message or self.empty_message,
            muted=True,
            wraplength=275,
        ).grid(
            row=1,
            column=0,
            padx=theme.CARD_PADDING_X,
            pady=(0, theme.CARD_PADDING_Y),
            sticky="w",
        )

    # =====================================================
    # SECTION METHODS
    # =====================================================

    def add_section(
        self,
        title: str,
        *,
        row: int,
    ) -> ctk.CTkFrame:
        """
        Add a titled Inspector section.

        Returns the section body for page-specific content.
        """

        section = ctk.CTkFrame(
            self.content,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        section.grid(
            row=row,
            column=0,
            pady=(0, theme.SECTION_GAP),
            sticky="ew",
        )
        section.grid_columnconfigure(0, weight=1)

        create_small_label(
            section,
            title.upper(),
            muted=True,
            bold=True,
        ).grid(
            row=0,
            column=0,
            pady=(0, 6),
            sticky="w",
        )

        body = create_card(
            section,
            fg_color=theme.INPUT_BG,
        )
        body.grid(
            row=1,
            column=0,
            sticky="ew",
        )
        body.grid_columnconfigure(0, weight=1)

        return body

    def add_text_section(
        self,
        title: str,
        text: str,
        *,
        row: int,
    ) -> ctk.CTkFrame:
        """Add a section containing wrapped text."""

        body = self.add_section(
            title,
            row=row,
        )

        create_body_label(
            body,
            text,
            muted=False,
            wraplength=275,
        ).grid(
            row=0,
            column=0,
            padx=theme.CARD_PADDING_X,
            pady=theme.CARD_PADDING_Y,
            sticky="w",
        )

        return body

    def add_info_section(
        self,
        title: str,
        values: list[tuple[str, str]],
        *,
        row: int,
    ) -> ctk.CTkFrame:
        """Add a section containing label/value information."""

        body = self.add_section(
            title,
            row=row,
        )
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)

        for item_row, (label_text, value_text) in enumerate(
            values
        ):
            create_small_label(
                body,
                label_text,
                muted=True,
                bold=True,
            ).grid(
                row=item_row,
                column=0,
                padx=(theme.CARD_PADDING_X, 8),
                pady=(
                    theme.CARD_PADDING_Y
                    if item_row == 0
                    else 5,
                    theme.CARD_PADDING_Y
                    if item_row == len(values) - 1
                    else 5,
                ),
                sticky="w",
            )

            create_body_label(
                body,
                value_text,
                muted=False,
            ).grid(
                row=item_row,
                column=1,
                padx=(8, theme.CARD_PADDING_X),
                pady=(
                    theme.CARD_PADDING_Y
                    if item_row == 0
                    else 5,
                    theme.CARD_PADDING_Y
                    if item_row == len(values) - 1
                    else 5,
                ),
                sticky="e",
            )

        return body

    # =====================================================
    # ACTION METHODS
    # =====================================================

    def set_actions(
        self,
        *,
        primary_text: str | None = None,
        primary_command: Callable[[], Any] | None = None,
        secondary_text: str | None = None,
        secondary_command: Callable[[], Any] | None = None,
    ) -> None:
        """Configure up to two Inspector action buttons."""

        for child in self.actions.winfo_children():
            child.destroy()

        has_actions = False

        if secondary_text:
            secondary_button = create_secondary_button(
                self.actions,
                secondary_text,
                secondary_command,
                width=110,
            )
            secondary_button.grid(
                row=0,
                column=0,
                padx=(0, 5),
                sticky="ew",
            )
            has_actions = True

        if primary_text:
            primary_button = create_primary_button(
                self.actions,
                primary_text,
                primary_command,
                width=110,
            )
            primary_button.grid(
                row=0,
                column=1,
                padx=(5, 0),
                sticky="ew",
            )
            has_actions = True

        if has_actions:
            self.actions.grid()
        else:
            self.actions.grid_remove()