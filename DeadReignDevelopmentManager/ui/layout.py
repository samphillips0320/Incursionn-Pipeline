from __future__ import annotations

import customtkinter as ctk

from ui import theme


class StandardPage(ctk.CTkFrame):
    """
    Shared page layout used throughout DR Pipeline Management.

    Structure:
        page
        ├── header
        ├── toolbar
        └── body
            ├── main
            └── details

    The details panel can be shown or hidden depending on the page.
    """

    def __init__(
        self,
        parent: ctk.CTkBaseClass,
        *,
        show_details: bool = False,
        details_width: int | None = None,
        scroll_main: bool = False,
    ) -> None:
        super().__init__(
            parent,
            fg_color=theme.APP_BG,
            corner_radius=0,
        )

        self.show_details = show_details
        self.details_width = details_width or theme.DETAIL_PANEL_WIDTH
        self.scroll_main = scroll_main

        self._build_grid()
        self._build_sections()

    def _build_grid(self) -> None:
        """Configure the page's primary rows and columns."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def _build_sections(self) -> None:
        """Create the page header, toolbar, body, and optional detail area."""

        # -------------------------------------------------
        # PAGE HEADER AREA
        # -------------------------------------------------

        self.header = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        self.header.grid(
            row=0,
            column=0,
            padx=theme.PAGE_PADDING_X,
            pady=(theme.PAGE_PADDING_Y, 0),
            sticky="ew",
        )
        self.header.grid_columnconfigure(0, weight=1)

        # -------------------------------------------------
        # PAGE TOOLBAR AREA
        # -------------------------------------------------

        self.toolbar = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        self.toolbar.grid(
            row=1,
            column=0,
            padx=theme.PAGE_PADDING_X,
            pady=(theme.SECTION_GAP, 0),
            sticky="ew",
        )
        self.toolbar.grid_columnconfigure(0, weight=1)

        # -------------------------------------------------
        # PAGE BODY
        # -------------------------------------------------

        self.body = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        self.body.grid(
            row=2,
            column=0,
            padx=theme.PAGE_PADDING_X,
            pady=(theme.SECTION_GAP, theme.PAGE_PADDING_Y),
            sticky="nsew",
        )

        self.body.grid_rowconfigure(0, weight=1)
        self.body.grid_columnconfigure(0, weight=1)

        if self.show_details:
            self.body.grid_columnconfigure(
                1,
                weight=0,
                minsize=self.details_width,
            )

        # -------------------------------------------------
        # MAIN CONTENT AREA
        # -------------------------------------------------

        if self.scroll_main:
            self.main = ctk.CTkScrollableFrame(
                self.body,
                fg_color=theme.TRANSPARENT,
                corner_radius=0,
                scrollbar_button_color=theme.CARD_BORDER,
                scrollbar_button_hover_color=theme.TEXT_MUTED,
            )
        else:
            self.main = ctk.CTkFrame(
                self.body,
                fg_color=theme.TRANSPARENT,
                corner_radius=0,
            )

        self.main.grid(
            row=0,
            column=0,
            sticky="nsew",
        )
        self.main.grid_columnconfigure(0, weight=1)

        # -------------------------------------------------
        # OPTIONAL RIGHT-SIDE DETAIL AREA
        # -------------------------------------------------

        if self.show_details:
            self.details = ctk.CTkFrame(
                self.body,
                width=self.details_width,
                fg_color=theme.TRANSPARENT,
                corner_radius=0,
            )
            self.details.grid(
                row=0,
                column=1,
                padx=(theme.SECTION_GAP, 0),
                sticky="nsew",
            )
            self.details.grid_propagate(False)
            self.details.grid_columnconfigure(0, weight=1)
            self.details.grid_rowconfigure(0, weight=1)
        else:
            self.details = None

    def clear_header(self) -> None:
        """Remove all widgets from the page header."""
        self._clear_children(self.header)

    def clear_toolbar(self) -> None:
        """Remove all widgets from the page toolbar."""
        self._clear_children(self.toolbar)

    def clear_main(self) -> None:
        """Remove all widgets from the main content area."""
        self._clear_children(self.main)

    def clear_details(self) -> None:
        """Remove all widgets from the detail area, if it exists."""
        if self.details is not None:
            self._clear_children(self.details)

    @staticmethod
    def _clear_children(container: ctk.CTkBaseClass) -> None:
        """Destroy every child widget inside a container."""
        for child in container.winfo_children():
            child.destroy()


class TwoColumnLayout(ctk.CTkFrame):
    """
    Reusable two-column layout.

    Useful for:
        - dashboard card groups
        - settings forms
        - systems overview
        - analytics sections
    """

    def __init__(
        self,
        parent: ctk.CTkBaseClass,
        *,
        left_weight: int = 1,
        right_weight: int = 1,
        gap: int | None = None,
    ) -> None:
        super().__init__(
            parent,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )

        self.gap = gap if gap is not None else theme.SECTION_GAP

        self.grid_columnconfigure(0, weight=left_weight)
        self.grid_columnconfigure(1, weight=right_weight)
        self.grid_rowconfigure(0, weight=1)

        self.left = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        self.left.grid(
            row=0,
            column=0,
            padx=(0, self.gap // 2),
            sticky="nsew",
        )
        self.left.grid_columnconfigure(0, weight=1)

        self.right = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        self.right.grid(
            row=0,
            column=1,
            padx=(self.gap // 2, 0),
            sticky="nsew",
        )
        self.right.grid_columnconfigure(0, weight=1)


class ThreeColumnLayout(ctk.CTkFrame):
    """
    Reusable three-column layout.

    Useful for:
        - Kanban boards
        - grouped cards
        - analytics summaries
        - release checklist categories
    """

    def __init__(
        self,
        parent: ctk.CTkBaseClass,
        *,
        weights: tuple[int, int, int] = (1, 1, 1),
        gap: int | None = None,
    ) -> None:
        super().__init__(
            parent,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )

        self.gap = gap if gap is not None else theme.SECTION_GAP

        for index, weight in enumerate(weights):
            self.grid_columnconfigure(index, weight=weight)

        self.grid_rowconfigure(0, weight=1)

        self.left = self._create_column(
            column=0,
            padx=(0, self.gap // 2),
        )

        self.center = self._create_column(
            column=1,
            padx=(self.gap // 2, self.gap // 2),
        )

        self.right = self._create_column(
            column=2,
            padx=(self.gap // 2, 0),
        )

    def _create_column(
        self,
        *,
        column: int,
        padx: tuple[int, int],
    ) -> ctk.CTkFrame:
        """Create one transparent layout column."""
        frame = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        frame.grid(
            row=0,
            column=column,
            padx=padx,
            sticky="nsew",
        )
        frame.grid_columnconfigure(0, weight=1)

        return frame


class VerticalStack(ctk.CTkFrame):
    """
    Simple vertical content stack with consistent spacing.

    Add widgets with:
        stack.add(widget)
    """

    def __init__(
        self,
        parent: ctk.CTkBaseClass,
        *,
        gap: int | None = None,
    ) -> None:
        super().__init__(
            parent,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )

        self.gap = gap if gap is not None else theme.CARD_GAP
        self._next_row = 0

        self.grid_columnconfigure(0, weight=1)

    def add(
        self,
        widget: ctk.CTkBaseClass,
        *,
        sticky: str = "ew",
        padx: int | tuple[int, int] = 0,
        pady: int | tuple[int, int] | None = None,
    ) -> None:
        """Add a widget beneath the previous widget."""
        resolved_pady = (
            pady
            if pady is not None
            else (0, self.gap)
        )

        widget.grid(
            row=self._next_row,
            column=0,
            padx=padx,
            pady=resolved_pady,
            sticky=sticky,
        )

        self._next_row += 1

    def clear(self) -> None:
        """Destroy all widgets and reset the stack."""
        for child in self.winfo_children():
            child.destroy()

        self._next_row = 0