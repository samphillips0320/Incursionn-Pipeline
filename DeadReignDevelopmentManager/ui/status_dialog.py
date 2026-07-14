# ui/status_dialog.py

from __future__ import annotations

from collections.abc import Callable

import customtkinter as ctk

from ui import theme
from ui.components import (
    create_card_title,
    create_dropdown,
    create_primary_button,
    create_secondary_button,
    create_small_label,
)


class StatusDialog(ctk.CTkToplevel):
    """Small reusable dialog for changing a task status."""

    STATUS_VALUES = [
        "Ideas / Backlog",
        "Planned",
        "In Progress",
        "Testing",
        "Complete",
    ]

    def __init__(
        self,
        parent: ctk.CTkBaseClass,
        *,
        current_status: str,
        task_title: str,
        on_save: Callable[[str], None] | None = None,
    ) -> None:
        super().__init__(parent)

        self.on_save = on_save

        self.title("Change Task Status")
        self.geometry("420x290")
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

        self.status_variable = ctk.StringVar(
            value=self._normalize_status(
                current_status
            )
        )

        self._build_content(
            task_title
        )
        self._build_actions()

        self.after(
            50,
            self._center_on_parent,
        )

    def _build_content(
        self,
        task_title: str,
    ) -> None:
        """Create the dialog content."""

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
            "Change Status",
        ).grid(
            row=0,
            column=0,
            padx=18,
            pady=(18, 4),
            sticky="w",
        )

        create_small_label(
            content,
            task_title,
            muted=True,
        ).grid(
            row=1,
            column=0,
            padx=18,
            pady=(0, 14),
            sticky="w",
        )

        create_small_label(
            content,
            "STATUS",
            muted=True,
            bold=True,
        ).grid(
            row=2,
            column=0,
            padx=18,
            pady=(0, 6),
            sticky="w",
        )

        self.status_menu = create_dropdown(
            content,
            self.STATUS_VALUES,
            variable=self.status_variable,
            width=260,
        )
        self.status_menu.grid(
            row=3,
            column=0,
            padx=18,
            pady=(0, 18),
            sticky="ew",
        )

    def _build_actions(self) -> None:
        """Create Cancel and Save buttons."""

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

        create_primary_button(
            actions,
            "Update Status",
            self._handle_save,
            width=140,
        ).grid(
            row=0,
            column=1,
            padx=(6, 0),
            sticky="ew",
        )

    def _handle_save(self) -> None:
        """Return the selected status."""

        new_status = self.status_variable.get().strip()

        if self.on_save is not None:
            self.on_save(
                new_status
            )

        self.destroy()

    def _center_on_parent(self) -> None:
        """Center the dialog over the application."""

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

    @staticmethod
    def _normalize_status(
        status: str,
    ) -> str:
        """Convert older status labels into current values."""

        status_map = {
            "idea": "Ideas / Backlog",
            "ideas": "Ideas / Backlog",
            "backlog": "Ideas / Backlog",
            "ideas / backlog": "Ideas / Backlog",
            "planned": "Planned",
            "to do": "Planned",
            "todo": "Planned",
            "not started": "Planned",
            "in progress": "In Progress",
            "in-progress": "In Progress",
            "active": "In Progress",
            "testing": "Testing",
            "test": "Testing",
            "qa": "Testing",
            "complete": "Complete",
            "completed": "Complete",
            "done": "Complete",
        }

        return status_map.get(
            status.strip().lower(),
            "Planned",
        )