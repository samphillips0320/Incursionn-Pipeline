from __future__ import annotations

import customtkinter as ctk

from ui import theme
from ui.components import (
    create_body_label,
    create_card,
    create_card_title,
    create_info_row,
    create_primary_button,
    create_secondary_button,
    create_separator,
    create_small_label,
)


class DetailPanel(ctk.CTkFrame):
    """
    Reusable right-side information panel.

    The panel is intentionally generic so it can support:
        - task details
        - development log details
        - system documentation
        - asset information
        - knowledge base articles
        - roadmap milestones
    """

    def __init__(
        self,
        parent: ctk.CTkBaseClass,
        *,
        title: str = "Details",
        subtitle: str = "",
        empty_message: str = "Select an item to view its details.",
    ) -> None:
        super().__init__(
            parent,
            fg_color=theme.CARD_BG,
            border_color=theme.CARD_BORDER,
            border_width=theme.BORDER_WIDTH,
            corner_radius=theme.CARD_CORNER_RADIUS,
        )

        self.title_text = title
        self.subtitle_text = subtitle
        self.empty_message = empty_message

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_separator()
        self._build_content()
        self._build_actions()

        self.show_empty_state()

    def _build_header(self) -> None:
        """Create the fixed panel header."""
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
            self.title_text,
        )
        self.title_label.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.subtitle_label = create_small_label(
            self.header,
            self.subtitle_text,
            muted=True,
        )
        self.subtitle_label.grid(
            row=1,
            column=0,
            pady=(3, 0),
            sticky="w",
        )

        if not self.subtitle_text:
            self.subtitle_label.grid_remove()

    def _build_separator(self) -> None:
        """Create the divider below the panel header."""
        separator = create_separator(self)
        separator.grid(
            row=1,
            column=0,
            padx=theme.CARD_PADDING_X,
            sticky="ew",
        )

    def _build_content(self) -> None:
        """Create the scrollable detail content area."""
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
        """Create the optional bottom action bar."""
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
    # HEADER METHODS
    # =====================================================

    def set_title(
        self,
        title: str,
        subtitle: str = "",
    ) -> None:
        """Update the panel's title and optional subtitle."""
        self.title_text = title
        self.subtitle_text = subtitle

        self.title_label.configure(text=title)
        self.subtitle_label.configure(text=subtitle)

        if subtitle:
            self.subtitle_label.grid()
        else:
            self.subtitle_label.grid_remove()

    # =====================================================
    # CONTENT METHODS
    # =====================================================

    def clear(self) -> None:
        """Remove all current detail content and action buttons."""
        for child in self.content.winfo_children():
            child.destroy()

        for child in self.actions.winfo_children():
            child.destroy()

        self.actions.grid_remove()

    def show_empty_state(
        self,
        message: str | None = None,
    ) -> None:
        """Show the default panel state when nothing is selected."""
        self.clear()

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

        empty_title = create_card_title(
            empty_card,
            "Nothing selected",
        )
        empty_title.grid(
            row=0,
            column=0,
            padx=theme.CARD_PADDING_X,
            pady=(theme.CARD_PADDING_Y, 5),
            sticky="w",
        )

        empty_label = create_body_label(
            empty_card,
            message or self.empty_message,
            muted=True,
            wraplength=260,
        )
        empty_label.grid(
            row=1,
            column=0,
            padx=theme.CARD_PADDING_X,
            pady=(0, theme.CARD_PADDING_Y),
            sticky="w",
        )

    def add_section(
        self,
        title: str,
        *,
        row: int,
    ) -> ctk.CTkFrame:
        """
        Add a titled section to the panel.

        Returns the section body so page-specific widgets can be
        placed inside it.
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

        section_title = create_small_label(
            section,
            title.upper(),
            muted=True,
            bold=True,
        )
        section_title.grid(
            row=0,
            column=0,
            pady=(0, 7),
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
        body.grid_columnconfigure(1, weight=1)

        return body

    def add_text_section(
        self,
        title: str,
        text: str,
        *,
        row: int,
    ) -> ctk.CTkFrame:
        """Add a titled card containing body text."""
        body = self.add_section(
            title,
            row=row,
        )

        text_label = create_body_label(
            body,
            text,
            muted=False,
            wraplength=270,
        )
        text_label.grid(
            row=0,
            column=0,
            columnspan=2,
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
        """Add a titled section containing label/value information."""
        body = self.add_section(
            title,
            row=row,
        )

        for info_row, (label, value) in enumerate(values):
            create_info_row(
                body,
                label,
                value,
                row=info_row,
            )

        for child in body.winfo_children():
            child.grid_configure(
                padx=theme.CARD_PADDING_X,
            )

        if values:
            first_children = body.grid_slaves(row=0)
            last_children = body.grid_slaves(row=len(values) - 1)

            for child in first_children:
                child.grid_configure(
                    pady=(theme.CARD_PADDING_Y, 4),
                )

            for child in last_children:
                child.grid_configure(
                    pady=(4, theme.CARD_PADDING_Y),
                )

        return body

    # =====================================================
    # ACTION METHODS
    # =====================================================

    def set_actions(
        self,
        *,
        primary_text: str | None = None,
        primary_command=None,
        secondary_text: str | None = None,
        secondary_command=None,
    ) -> None:
        """Configure up to two bottom action buttons."""
        for child in self.actions.winfo_children():
            child.destroy()

        has_action = False

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
            has_action = True

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
            has_action = True

        if has_action:
            self.actions.grid()
        else:
            self.actions.grid_remove()