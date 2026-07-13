from __future__ import annotations

from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from ui import theme
from ui.resources import ImageManager


class Sidebar(ctk.CTkFrame):
    """
    Persistent application sidebar.

    Responsibilities:
        - Display Incursionn Studios branding
        - Display navigation buttons
        - Highlight the active page
        - Notify the application when navigation changes
    """

    NAV_ITEMS = [
        ("Dashboard", "dashboard"),
        ("Task Board", "task_board"),
        ("Roadmap", "roadmap"),
        ("Development Log", "development_log"),
        ("Systems", "systems"),
        ("Knowledge Base", "knowledge_base"),
        ("Assets", "assets"),
        ("Progress Analytics", "analytics"),
        ("Release Checklist", "release_checklist"),
        ("Settings", "settings"),
    ]

    def __init__(
        self,
        parent: ctk.CTkBaseClass,
        *,
        on_navigate: Callable[[str], Any],
        initial_page: str = "dashboard",
    ) -> None:
        super().__init__(
            parent,
            width=theme.SIDEBAR_WIDTH,
            fg_color=theme.SIDEBAR_BG,
            corner_radius=0,
        )

        self.on_navigate = on_navigate
        self.active_page = initial_page
        self.nav_buttons: dict[str, ctk.CTkButton] = {}

        self.logo_image: ctk.CTkImage | None = None

        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_branding()
        self._build_separator()
        self._build_navigation()
        self._build_version_label()

        self.set_active(initial_page)

    # =====================================================
    # BUILD METHODS
    # =====================================================

    def _build_branding(self) -> None:
        """Create the Incursionn Studios logo area."""
        self.brand_frame = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        self.brand_frame.grid(
            row=0,
            column=0,
            padx=8,
            pady=(16, 14),
            sticky="ew",
        )
        self.brand_frame.grid_columnconfigure(0, weight=1)

        self.logo_image = ImageManager.load_logo(
            "incursionn_logo.png",
            width=215,
            height=112,
        )

        if self.logo_image is not None:
            self.logo_label = ctk.CTkLabel(
                self.brand_frame,
                text="",
                image=self.logo_image,
                fg_color=theme.TRANSPARENT,
            )
        else:
            self.logo_label = ctk.CTkLabel(
                self.brand_frame,
                text="INCURSIONN\nSTUDIOS",
                font=(theme.FONT_FAMILY, 15, "bold"),
                text_color=theme.TEXT_PRIMARY,
                justify="left",
                anchor="w",
            )

        self.logo_label.grid(
            row=0,
            column=0,
            sticky="ew",
        )

    def _build_separator(self) -> None:
        """Create the divider beneath the branding."""
        separator = ctk.CTkFrame(
            self,
            height=1,
            fg_color=theme.CARD_BORDER,
            corner_radius=0,
        )
        separator.grid(
            row=1,
            column=0,
            padx=12,
            sticky="ew",
        )

    def _build_navigation(self) -> None:
        """Create the navigation button list."""
        self.nav_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
            scrollbar_button_color=theme.CARD_BORDER,
            scrollbar_button_hover_color=theme.TEXT_MUTED,
        )
        self.nav_frame.grid(
            row=2,
            column=0,
            padx=(8, 4),
            pady=(12, 6),
            sticky="nsew",
        )
        self.nav_frame.grid_columnconfigure(0, weight=1)

        for row_index, (label, page_key) in enumerate(
            self.NAV_ITEMS
        ):
            button = ctk.CTkButton(
                self.nav_frame,
                text=label,
                command=lambda key=page_key: (
                    self._handle_navigation(key)
                ),
                height=theme.NAV_BUTTON_HEIGHT,
                fg_color=theme.TRANSPARENT,
                hover_color=theme.CARD_BG_HOVER,
                text_color=theme.TEXT_SECONDARY,
                corner_radius=theme.BUTTON_CORNER_RADIUS,
                font=theme.FONT_NAV,
                anchor="w",
                border_width=0,
            )
            button.grid(
                row=row_index,
                column=0,
                pady=2,
                sticky="ew",
            )

            self.nav_buttons[page_key] = button

    def _build_version_label(self) -> None:
        """Display the application version at the bottom."""
        self.version_label = ctk.CTkLabel(
            self,
            text="DR PIPELINE MANAGEMENT v0.1.0",
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_MUTED,
            anchor="w",
        )
        self.version_label.grid(
            row=3,
            column=0,
            padx=12,
            pady=(4, 12),
            sticky="ew",
        )

    # =====================================================
    # NAVIGATION METHODS
    # =====================================================

    def _handle_navigation(self, page_key: str) -> None:
        """Set the selected state and notify the application."""
        self.set_active(page_key)
        self.on_navigate(page_key)

    def set_active(self, page_key: str) -> None:
        """Highlight the currently selected navigation item."""
        if page_key not in self.nav_buttons:
            return

        self.active_page = page_key

        for key, button in self.nav_buttons.items():
            if key == page_key:
                button.configure(
                    fg_color=theme.ACCENT_ORANGE_DARK,
                    hover_color=theme.ACCENT_ORANGE_DARK,
                    text_color=theme.TEXT_PRIMARY,
                    font=theme.FONT_NAV_ACTIVE,
                    border_width=1,
                    border_color=theme.ACCENT_ORANGE,
                )
            else:
                button.configure(
                    fg_color=theme.TRANSPARENT,
                    hover_color=theme.CARD_BG_HOVER,
                    text_color=theme.TEXT_SECONDARY,
                    font=theme.FONT_NAV,
                    border_width=0,
                )