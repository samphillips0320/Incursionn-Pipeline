# ui/task_dialog.py

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from ui import theme
from ui.components import (
    create_body_label,
    create_card_title,
    create_dropdown,
    create_primary_button,
    create_secondary_button,
    create_small_label,
    create_text_entry,
    create_textbox,
)


class TaskDialog(ctk.CTkToplevel):
    """
    Reusable dialog for creating and editing tasks.

    When task is None, the dialog operates in create mode.
    When task is provided, the dialog operates in edit mode.
    """

    def __init__(
        self,
        parent: ctk.CTkBaseClass,
        *,
        systems: list[str],
        task: dict[str, Any] | None = None,
        on_save: Callable[[dict[str, Any]], None] | None = None,
    ) -> None:
        super().__init__(parent)

        self.task = task
        self.on_save = on_save
        self.is_edit_mode = task is not None

        self.title(
            "Edit Task"
            if self.is_edit_mode
            else "New Task"
        )

        self.geometry("560x670")
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
        self.grid_rowconfigure(
            1,
            weight=1,
        )

        self._create_variables(
            systems
        )
        self._build_header()
        self._build_form()
        self._build_actions()

        self.after(
            50,
            self._center_on_parent,
        )

        self.after(
            100,
            self.title_entry.focus_set,
        )

    # =====================================================
    # SETUP
    # =====================================================

    def _create_variables(
        self,
        systems: list[str],
    ) -> None:
        """Create form variables and normalize dropdown values."""

        clean_systems = sorted(
            {
                str(system).strip()
                for system in systems
                if str(system).strip()
            }
        )

        if not clean_systems:
            clean_systems = [
                "Unassigned"
            ]

        self.system_values = clean_systems

        task = self.task or {}

        default_system = str(
            task.get(
                "system",
                clean_systems[0],
            )
        ).strip()

        if default_system not in self.system_values:
            self.system_values.append(
                default_system
            )
            self.system_values.sort()

        self.title_variable = ctk.StringVar(
            value=str(
                task.get(
                    "title",
                    "",
                )
            )
        )

        self.system_variable = ctk.StringVar(
            value=default_system
        )

        self.priority_variable = ctk.StringVar(
            value=str(
                task.get(
                    "priority",
                    "Medium",
                )
            )
        )

        self.status_variable = ctk.StringVar(
            value=self._normalize_status(
                str(
                    task.get(
                        "status",
                        "Planned",
                    )
                )
            )
        )

        self.validation_variable = ctk.StringVar(
            value=""
        )

    # =====================================================
    # BUILD
    # =====================================================

    def _build_header(self) -> None:
        """Create the dialog heading."""

        header = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        header.grid(
            row=0,
            column=0,
            padx=24,
            pady=(22, 14),
            sticky="ew",
        )
        header.grid_columnconfigure(
            0,
            weight=1,
        )

        create_card_title(
            header,
            (
                "Edit Task"
                if self.is_edit_mode
                else "Create New Task"
            ),
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        create_small_label(
            header,
            (
                "Update the selected task."
                if self.is_edit_mode
                else (
                    "Add a new piece of work "
                    "to the development pipeline."
                )
            ),
            muted=True,
        ).grid(
            row=1,
            column=0,
            pady=(4, 0),
            sticky="w",
        )

    def _build_form(self) -> None:
        """Create the task form."""

        form = ctk.CTkScrollableFrame(
            self,
            fg_color=theme.CARD_BG,
            border_color=theme.CARD_BORDER,
            border_width=theme.BORDER_WIDTH,
            corner_radius=theme.CARD_CORNER_RADIUS,
            scrollbar_button_color=theme.CARD_BORDER,
            scrollbar_button_hover_color=theme.TEXT_MUTED,
        )
        form.grid(
            row=1,
            column=0,
            padx=24,
            pady=(0, 14),
            sticky="nsew",
        )

        form.grid_columnconfigure(
            0,
            weight=1,
        )
        form.grid_columnconfigure(
            1,
            weight=1,
        )

        create_small_label(
            form,
            "TITLE",
            muted=True,
            bold=True,
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=18,
            pady=(18, 6),
            sticky="w",
        )

        self.title_entry = create_text_entry(
            form,
            placeholder="Describe the work to be completed...",
            textvariable=self.title_variable,
        )
        self.title_entry.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=18,
            sticky="ew",
        )

        create_small_label(
            form,
            "SYSTEM",
            muted=True,
            bold=True,
        ).grid(
            row=2,
            column=0,
            padx=(18, 8),
            pady=(18, 6),
            sticky="w",
        )

        create_small_label(
            form,
            "PRIORITY",
            muted=True,
            bold=True,
        ).grid(
            row=2,
            column=1,
            padx=(8, 18),
            pady=(18, 6),
            sticky="w",
        )

        self.system_menu = create_dropdown(
            form,
            self.system_values,
            variable=self.system_variable,
            width=200,
        )
        self.system_menu.grid(
            row=3,
            column=0,
            padx=(18, 8),
            sticky="ew",
        )

        self.priority_menu = create_dropdown(
            form,
            [
                "Critical",
                "High",
                "Medium",
                "Low",
            ],
            variable=self.priority_variable,
            width=200,
        )
        self.priority_menu.grid(
            row=3,
            column=1,
            padx=(8, 18),
            sticky="ew",
        )

        create_small_label(
            form,
            "STATUS",
            muted=True,
            bold=True,
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            padx=18,
            pady=(18, 6),
            sticky="w",
        )

        self.status_menu = create_dropdown(
            form,
            [
                "Ideas / Backlog",
                "Planned",
                "In Progress",
                "Testing",
                "Complete",
            ],
            variable=self.status_variable,
            width=200,
        )
        self.status_menu.grid(
            row=5,
            column=0,
            columnspan=2,
            padx=18,
            sticky="ew",
        )

        create_small_label(
            form,
            "NOTES",
            muted=True,
            bold=True,
        ).grid(
            row=6,
            column=0,
            columnspan=2,
            padx=18,
            pady=(18, 6),
            sticky="w",
        )

        self.notes_textbox = create_textbox(
            form,
            height=170,
        )
        self.notes_textbox.grid(
            row=7,
            column=0,
            columnspan=2,
            padx=18,
            sticky="ew",
        )

        if self.task is not None:
            self.notes_textbox.insert(
                "1.0",
                str(
                    self.task.get(
                        "notes",
                        "",
                    )
                ),
            )

        validation_label = create_body_label(
            form,
            "",
            muted=False,
        )
        validation_label.configure(
            textvariable=self.validation_variable,
            text_color=theme.ERROR,
        )
        validation_label.grid(
            row=8,
            column=0,
            columnspan=2,
            padx=18,
            pady=(10, 18),
            sticky="w",
        )

    def _build_actions(self) -> None:
        """Create the dialog action buttons."""

        actions = ctk.CTkFrame(
            self,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        actions.grid(
            row=2,
            column=0,
            padx=24,
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
            width=150,
        ).grid(
            row=0,
            column=0,
            padx=(0, 6),
            sticky="ew",
        )

        create_primary_button(
            actions,
            (
                "Save Changes"
                if self.is_edit_mode
                else "Create Task"
            ),
            self._handle_save,
            width=150,
        ).grid(
            row=0,
            column=1,
            padx=(6, 0),
            sticky="ew",
        )

    # =====================================================
    # SAVE
    # =====================================================

    def _handle_save(self) -> None:
        """Validate the form and return the task payload."""

        title = self.title_variable.get().strip()
        system = self.system_variable.get().strip()
        priority = self.priority_variable.get().strip()
        status = self.status_variable.get().strip()
        notes = self.notes_textbox.get(
            "1.0",
            "end",
        ).strip()

        if not title:
            self.validation_variable.set(
                "Task title is required."
            )
            self.title_entry.focus_set()
            return

        self.validation_variable.set("")

        result = {
            "title": title,
            "system": system or "Unassigned",
            "priority": priority or "Medium",
            "status": status or "Planned",
            "notes": notes,
        }

        if self.task is not None:
            result["id"] = self.task.get(
                "id"
            )
            result["created_at"] = self.task.get(
                "created_at"
            )
            result["completed_at"] = self.task.get(
                "completed_at"
            )

        if self.on_save is not None:
            self.on_save(
                result
            )

        self.destroy()

    # =====================================================
    # POSITIONING
    # =====================================================

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

    @staticmethod
    def _normalize_status(
        status: str,
    ) -> str:
        """Convert older saved status names into current labels."""

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