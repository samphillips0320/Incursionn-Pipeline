from __future__ import annotations

from collections.abc import Callable

import customtkinter as ctk

from ui import theme
from ui.components import (
    create_body_label,
    create_card_title,
    create_danger_button,
    create_secondary_button,
)


class ConfirmationDialog(ctk.CTkToplevel):
    """Reusable confirmation dialog for destructive actions."""

    def __init__(
        self,
        parent: ctk.CTkBaseClass,
        *,
        title: str,
        message: str,
        confirm_text: str = "Confirm",
        on_confirm: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(parent)

        self.on_confirm = on_confirm

        self.title(title)
        self.geometry("440x245")
        self.resizable(False, False)
        self.configure(
            fg_color=theme.APP_BG,
        )

        self.transient(
            parent.winfo_toplevel()
        )
        self.grab_set()

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self._build_content(
            title,
            message,
        )

        self._build_actions(
            confirm_text,
        )

        self.after(
            50,
            self._center_on_parent,
        )

    def _build_content(
        self,
        title: str,
        message: str,
    ) -> None:
        """Create the confirmation message area."""

        content = ctk.CTkFrame(
            self,
            fg_color=theme.CARD_BG,
            border_color=theme.CARD_BORDER,
            border_width=theme.BORDER_WIDTH,
            corner_radius=theme.CARD_CORNER_RADIUS,
        )
        content.grid(
            row=0,
            column=0,
            padx=22,
            pady=(22, 14),
            sticky="ew",
        )
        content.grid_columnconfigure(
            0,
            weight=1,
        )

        create_card_title(
            content,
            title,
        ).grid(
            row=0,
            column=0,
            padx=18,
            pady=(18, 8),
            sticky="w",
        )

        create_body_label(
            content,
            message,
            muted=True,
            wraplength=365,
        ).grid(
            row=1,
            column=0,
            padx=18,
            pady=(0, 18),
            sticky="w",
        )

    def _build_actions(
        self,
        confirm_text: str,
    ) -> None:
        """Create Cancel and destructive confirmation buttons."""

        actions = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        actions.grid(
            row=1,
            column=0,
            padx=22,
            pady=(0, 22),
            sticky="ew",
        )

        actions.grid_columnconfigure(
            0,
            weight=1,
        )
        actions.grid_columnconfigure(
            1,
            weight=1,
        )

        create_secondary_button(
            actions,
            "Cancel",
            self.destroy,
            width=140,
        ).grid(
            row=0,
            column=0,
            padx=(0, 6),
            sticky="ew",
        )

        create_danger_button(
            actions,
            confirm_text,
            self._handle_confirm,
            width=140,
        ).grid(
            row=0,
            column=1,
            padx=(6, 0),
            sticky="ew",
        )

    def _handle_confirm(self) -> None:
        """Run the confirmation callback and close the dialog."""

        if self.on_confirm is not None:
            self.on_confirm()

        self.destroy()

    def _center_on_parent(self) -> None:
        """Center the dialog over the application window."""

        self.update_idletasks()

        parent = self.master.winfo_toplevel()

        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()

        x = (
            parent_x
            + (parent_width - dialog_width) // 2
        )

        y = (
            parent_y
            + (parent_height - dialog_height) // 2
        )

        self.geometry(
            f"+{x}+{y}"
        )