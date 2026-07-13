# ui/header.py

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from UI import theme
from UI.components import (
    create_icon_button,
    create_search_box,
)


class AppHeader(ctk.CTkFrame):
    """
    Persistent top application header.

    The page itself still owns its page title. This header is reserved
    for application-wide controls such as project selection, global
    search, notifications, and account controls.
    """

    def __init__(
        self,
        parent: ctk.CTkBaseClass,
        *,
        on_global_search: Callable[[str], Any] | None = None,
        on_notifications: Callable[[], Any] | None = None,
        on_profile: Callable[[], Any] | None = None,
    ) -> None:
        super().__init__(
            parent,
            height=theme.HEADER_HEIGHT,
            fg_color=theme.HEADER_BG,
            border_color=theme.CARD_BORDER,
            border_width=0,
            corner_radius=0,
        )

        self.on_global_search = on_global_search
        self.on_notifications = on_notifications
        self.on_profile = on_profile

        self.search_variable = ctk.StringVar()

        self.grid_propagate(False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_project_area()
        self._build_center_area()
        self._build_actions()

    # =====================================================
    # BUILD METHODS
    # =====================================================

    def _build_project_area(self) -> None:
        """Create the current-project display on the left."""
        self.project_frame = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        self.project_frame.grid(
            row=0,
            column=0,
            padx=(theme.PAGE_PADDING_X, 12),
            sticky="w",
        )

        project_caption = ctk.CTkLabel(
            self.project_frame,
            text="PROJECT",
            font=theme.FONT_SMALL_BOLD,
            text_color=theme.TEXT_MUTED,
            anchor="w",
        )
        project_caption.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.project_name_label = ctk.CTkLabel(
            self.project_frame,
            text="Dead Reign: Outbreak",
            font=theme.FONT_BODY_BOLD,
            text_color=theme.TEXT_PRIMARY,
            anchor="w",
        )
        self.project_name_label.grid(
            row=1,
            column=0,
            pady=(2, 0),
            sticky="w",
        )

    def _build_center_area(self) -> None:
        """Create the global search area."""
        self.center_frame = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        self.center_frame.grid(
            row=0,
            column=1,
            padx=12,
            sticky="ew",
        )
        self.center_frame.grid_columnconfigure(0, weight=1)

        self.search_box = create_search_box(
            self.center_frame,
            placeholder="Search the project...",
            width=360,
            textvariable=self.search_variable,
        )
        self.search_box.grid(
            row=0,
            column=0,
            sticky="e",
        )

        self.search_box.bind(
            "<Return>",
            self._handle_search,
        )

    def _build_actions(self) -> None:
        """Create the notification and profile controls."""
        self.action_frame = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        self.action_frame.grid(
            row=0,
            column=2,
            padx=(12, theme.PAGE_PADDING_X),
            sticky="e",
        )

        self.notification_button = create_icon_button(
            self.action_frame,
            "!",
            self._handle_notifications,
            width=38,
        )
        self.notification_button.grid(
            row=0,
            column=0,
            padx=(0, 8),
        )

        self.profile_button = ctk.CTkButton(
            self.action_frame,
            text="SP",
            command=self._handle_profile,
            width=40,
            height=40,
            fg_color=theme.ACCENT_ORANGE,
            hover_color=theme.ACCENT_ORANGE_HOVER,
            text_color=theme.TEXT_PRIMARY,
            corner_radius=20,
            font=theme.FONT_BODY_BOLD,
            border_width=0,
        )
        self.profile_button.grid(
            row=0,
            column=1,
        )

    # =====================================================
    # EVENT METHODS
    # =====================================================

    def _handle_search(self, _event=None) -> None:
        """Send the current global search query to the application."""
        query = self.search_variable.get().strip()

        if self.on_global_search is not None:
            self.on_global_search(query)

    def _handle_notifications(self) -> None:
        """Notify the application that notifications were opened."""
        if self.on_notifications is not None:
            self.on_notifications()

    def _handle_profile(self) -> None:
        """Notify the application that the profile control was opened."""
        if self.on_profile is not None:
            self.on_profile()

    # =====================================================
    # PUBLIC METHODS
    # =====================================================

    def set_project_name(self, project_name: str) -> None:
        """Update the project name shown in the header."""
        self.project_name_label.configure(text=project_name)

    def clear_search(self) -> None:
        """Clear the global search field."""
        self.search_variable.set("")