from __future__ import annotations

from typing import Any

import customtkinter as ctk

from pages.task_board_data import (
    TaskBoardData,
    load_task_board_data,
)
from ui import theme
from ui.components import (
    create_body_label,
    create_card,
    create_card_title,
    create_danger_button,
    create_dropdown,
    create_page_title,
    create_primary_button,
    create_search_box,
    create_secondary_button,
    create_section_title,
    create_small_label,
    make_clickable,
    make_hoverable,
)
from ui.inspector import Inspector
from ui.layout import StandardPage
from datetime import datetime
from uuid import uuid4
from storage import (
    delete_task,
    save_new_task,
    update_task
)
from ui.task_dialog import TaskDialog
from ui.status_dialog import StatusDialog
from ui.confirmation_dialog import ConfirmationDialog

ACTIVE_COLUMN_CONFIGURATION = [
    (
        "Ideas / Backlog",
        theme.WARNING,
    ),
    (
        "Planned",
        theme.INFO,
    ),
    (
        "In Progress",
        theme.ACCENT_ORANGE,
    ),
    (
        "Testing",
        theme.PURPLE,
    ),
]

BOARD_COLUMN_HEIGHT = 520
COMPLETED_PREVIEW_LIMIT = 12

def show_task_board(
    parent: ctk.CTkBaseClass,
) -> StandardPage:
    """Display the live, selectable Task Board."""

    board_data = load_task_board_data()

    page = StandardPage(
        parent,
        show_details=True,
        details_width=350,
        scroll_main=False,
    )
    page.pack(
        fill="both",
        expand=True,
    )

    page.board_data = board_data
    page.available_systems = board_data.systems

    page.all_tasks = list(board_data.tasks)
    page.board_content = None
    page.selected_task_id = None

    # Page-level selection state.
    page.selected_task = None
    page.selected_task_card = None

    # Lets us locate a specific task when arriving from the Dashboard.
    page.task_cards = {}
    page.task_lookup = {
        task["id"]: task
        for task in board_data.tasks
        if task.get("id")
    }

    page.completed_expanded = False
    page.filtered_task_count = len(board_data.tasks)

    _build_page_header(page)

    _build_toolbar(
        page,
        board_data,
    )

    _build_board(
        page,
        board_data,
    )

    _build_inspector(page)

    _select_pending_task(page)

    _bind_task_board_shortcuts(page)

    return page


# =========================================================
# HEADER
# =========================================================

def _build_page_header(
    page: StandardPage,
) -> None:
    """Create the Task Board page heading."""

    page.header.grid_columnconfigure(
        0,
        weight=1,
    )

    create_page_title(
        page.header,
        "Task Board",
    ).grid(
        row=0,
        column=0,
        sticky="w",
    )

    create_small_label(
        page.header,
        (
            "Plan, organize, and complete the work "
            "that moves Dead Reign forward."
        ),
        muted=True,
    ).grid(
        row=1,
        column=0,
        pady=(4, 0),
        sticky="w",
    )

    create_primary_button(
        page.header,
        "+ New Task",
        command=lambda: _open_new_task_dialog(
            page
        ),
        width=125,
    ).grid(
        row=0,
        column=1,
        rowspan=2,
        sticky="e",
    )


# =========================================================
# TOOLBAR
# =========================================================

def _build_toolbar(
    page: StandardPage,
    data: TaskBoardData,
) -> None:
    """Create live search, filtering, and sorting controls."""

    toolbar = page.toolbar
    toolbar.grid_columnconfigure(
        0,
        weight=1,
    )

    page.search_variable = ctk.StringVar()

    search = create_search_box(
        toolbar,
        placeholder="Search tasks...",
        width=310,
        textvariable=page.search_variable,
    )

    page.search_entry = search

    search.grid(
        row=0,
        column=0,
        padx=(0, theme.SECTION_GAP),
        sticky="w",
    )

    page.system_filter_variable = ctk.StringVar(
        value="All Systems"
    )

    system_filter = create_dropdown(
        toolbar,
        [
            "All Systems",
            *data.systems,
        ],
        variable=page.system_filter_variable,
        command=lambda _value: _refresh_task_board(
            page
        ),
        width=145,
    )
    system_filter.grid(
        row=0,
        column=1,
        padx=4,
    )

    page.priority_filter_variable = ctk.StringVar(
        value="All Priorities"
    )

    priority_filter = create_dropdown(
        toolbar,
        [
            "All Priorities",
            "Critical",
            "High",
            "Medium",
            "Low",
        ],
        variable=page.priority_filter_variable,
        command=lambda _value: _refresh_task_board(
            page
        ),
        width=145,
    )
    priority_filter.grid(
        row=0,
        column=2,
        padx=4,
    )

    page.status_filter_variable = ctk.StringVar(
        value="All Statuses"
    )

    status_filter = create_dropdown(
        toolbar,
        [
            "All Statuses",
            "Ideas / Backlog",
            "Planned",
            "In Progress",
            "Testing",
            "Complete",
        ],
        variable=page.status_filter_variable,
        command=lambda _value: _refresh_task_board(
            page
        ),
        width=145,
    )
    status_filter.grid(
        row=0,
        column=3,
        padx=4,
    )

    page.sort_variable = ctk.StringVar(
        value="Newest First"
    )

    sort_menu = create_dropdown(
        toolbar,
        [
            "Newest First",
            "Oldest First",
            "Priority",
            "System",
            "Title",
        ],
        variable=page.sort_variable,
        command=lambda _value: _refresh_task_board(
            page
        ),
        width=135,
    )
    sort_menu.grid(
        row=0,
        column=4,
        padx=(4, 0),
    )

    page.search_variable.trace_add(
        "write",
        lambda *_args: _refresh_task_board(
            page
        ),
    )

    clear_button = create_secondary_button(
        toolbar,
        "Clear",
        command=lambda: _clear_task_filters(
            page
        ),
        width=75,
    )
    clear_button.grid(
        row=0,
        column=5,
        padx=(8, 0),
    )

    page.result_count_label = create_small_label(
        toolbar,
        "",
        muted=True,
    )

    page.result_count_label.grid(
        row=1,
        column=0,
        columnspan=6,
        pady=(7, 0),
        sticky="w",
    )

def _clear_task_filters(
    page: StandardPage,
) -> None:
    """Reset all Task Board search and filter controls."""

    page.search_variable.set("")
    page.system_filter_variable.set(
        "All Systems"
    )
    page.priority_filter_variable.set(
        "All Priorities"
    )
    page.status_filter_variable.set(
        "All Statuses"
    )
    page.sort_variable.set(
        "Newest First"
    )

    _refresh_task_board(
        page
    )


# =========================================================
# BOARD
# =========================================================

def _build_board(
    page: StandardPage,
    data: TaskBoardData,
) -> None:
    """Create the Task Board container and render its task content."""

    main = page.main

    main.grid_columnconfigure(
        0,
        weight=1,
    )
    main.grid_rowconfigure(
        0,
        weight=1,
    )

    board_container = ctk.CTkFrame(
        main,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
    )
    board_container.grid(
        row=0,
        column=0,
        sticky="nsew",
    )

    board_container.grid_columnconfigure(
        0,
        weight=1,
    )
    board_container.grid_rowconfigure(
        0,
        weight=1,
    )

    page.board_container = board_container

    _refresh_task_board(
        page
    )

def _refresh_task_board(
    page: StandardPage,
) -> None:
    """
    Filter, sort, and redraw the Task Board.

    Only the board content is rebuilt. The toolbar, Inspector,
    and overall page remain in place.
    """

    if not hasattr(
        page,
        "board_container",
    ):
        return

    selected_task_id = None

    if page.selected_task is not None:
        selected_task_id = page.selected_task.get(
            "id"
        )

    for child in page.board_container.winfo_children():
        child.destroy()

    page.task_cards = {}
    page.selected_task_card = None

    filtered_tasks = _get_filtered_tasks(
        page
    )

    page.filtered_task_count = len(filtered_tasks)

    result_label = getattr(
        page,
        "result_count_label",
        None,
    )

    if result_label is not None:
        total_count = len(page.all_tasks)

        result_label.configure(
            text=(
                f"Showing {len(filtered_tasks)} "
                f"of {total_count} tasks"
            )
        )

    columns = _group_tasks_by_status(
        filtered_tasks
    )

    scroll_area = ctk.CTkScrollableFrame(
        page.board_container,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
        scrollbar_button_color=theme.CARD_BORDER,
        scrollbar_button_hover_color=theme.TEXT_MUTED,
    )
    scroll_area.grid(
        row=0,
        column=0,
        sticky="nsew",
    )
    scroll_area.grid_columnconfigure(
        0,
        weight=1,
    )

    page.board_scroll_area = scroll_area

    filtered_data = TaskBoardData(
        tasks=filtered_tasks,
        systems=page.available_systems,
        columns=columns,
    )

    _build_active_columns(
        page,
        scroll_area,
        filtered_data,
        row=0,
    )

    _build_completed_section(
        page,
        scroll_area,
        columns.get(
            "Complete",
            [],
        ),
        row=1,
    )

    if selected_task_id:
        selected_task = next(
            (
                task
                for task in filtered_tasks
                if task.get("id") == selected_task_id
            ),
            None,
        )

        selected_card = page.task_cards.get(
            selected_task_id
        )

        if (
            selected_task is not None
            and selected_card is not None
        ):
            _select_task(
                page,
                selected_task,
                selected_card,
            )
        else:
            page.selected_task = None
            page.selected_task_card = None

            if hasattr(
                page,
                "inspector",
            ):
                page.inspector.show_empty_state(
                    title="Task hidden by filters",
                    message=(
                        "The selected task does not match the "
                        "current search or filters."
                    ),
                )

def _get_filtered_tasks(
    page: StandardPage,
) -> list[dict[str, Any]]:
    """Return tasks matching the current search and filters."""

    search_text = (
        page.search_variable.get()
        .strip()
        .lower()
    )

    selected_system = (
        page.system_filter_variable.get()
    )

    selected_priority = (
        page.priority_filter_variable.get()
    )

    selected_status = (
        page.status_filter_variable.get()
    )

    filtered_tasks = []

    for task in page.all_tasks:
        if search_text:
            searchable_text = " ".join(
                [
                    str(
                        task.get(
                            "title",
                            "",
                        )
                    ),
                    str(
                        task.get(
                            "notes",
                            "",
                        )
                    ),
                    str(
                        task.get(
                            "system",
                            "",
                        )
                    ),
                    str(
                        task.get(
                            "priority",
                            "",
                        )
                    ),
                    str(
                        task.get(
                            "normalized_status",
                            "",
                        )
                    ),
                ]
            ).lower()

            if search_text not in searchable_text:
                continue

        if (
            selected_system != "All Systems"
            and task.get("system") != selected_system
        ):
            continue

        if (
            selected_priority != "All Priorities"
            and task.get("priority") != selected_priority
        ):
            continue

        if (
            selected_status != "All Statuses"
            and task.get(
                "normalized_status"
            ) != selected_status
        ):
            continue

        filtered_tasks.append(
            task
        )

    return _sort_tasks(
        filtered_tasks,
        page.sort_variable.get(),
    )

def _sort_tasks(
    tasks: list[dict[str, Any]],
    sort_mode: str,
) -> list[dict[str, Any]]:
    """Sort tasks using the selected Task Board mode."""

    sorted_tasks = list(tasks)

    if sort_mode == "Oldest First":
        sorted_tasks.sort(
            key=lambda task: task.get(
                "created_sort_value",
                datetime.min,
            )
        )

    elif sort_mode == "Priority":
        priority_order = {
            "Critical": 0,
            "High": 1,
            "Medium": 2,
            "Low": 3,
        }

        sorted_tasks.sort(
            key=lambda task: (
                priority_order.get(
                    task.get(
                        "priority",
                        "Low",
                    ),
                    99,
                ),
                task.get(
                    "title",
                    "",
                ).lower(),
            )
        )

    elif sort_mode == "System":
        sorted_tasks.sort(
            key=lambda task: (
                task.get(
                    "system",
                    "",
                ).lower(),
                task.get(
                    "title",
                    "",
                ).lower(),
            )
        )

    elif sort_mode == "Title":
        sorted_tasks.sort(
            key=lambda task: task.get(
                "title",
                "",
            ).lower()
        )

    else:
        sorted_tasks.sort(
            key=lambda task: task.get(
                "created_sort_value",
                datetime.min,
            ),
            reverse=True,
        )

    return sorted_tasks

def _group_tasks_by_status(
    tasks: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Group filtered tasks into Task Board workflow columns."""

    columns = {
        "Ideas / Backlog": [],
        "Planned": [],
        "In Progress": [],
        "Testing": [],
        "Complete": [],
    }

    for task in tasks:
        status = task.get(
            "normalized_status",
            "Planned",
        )

        if status not in columns:
            status = "Planned"

        columns[status].append(
            task
        )

    return columns



def _build_active_columns(
    page: StandardPage,
    parent: ctk.CTkBaseClass,
    data: TaskBoardData,
    *,
    row: int,
) -> None:
    """Create live active workflow columns."""

    active_board = ctk.CTkFrame(
        parent,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
    )
    active_board.grid(
        row=row,
        column=0,
        pady=(0, theme.SECTION_GAP),
        sticky="ew",
    )

    for column_index in range(4):
        active_board.grid_columnconfigure(
            column_index,
            weight=1,
            uniform="active_task_columns",
        )

    for column_index, (
        title,
        accent_color,
    ) in enumerate(
        ACTIVE_COLUMN_CONFIGURATION
    ):
        tasks = data.columns.get(
            title,
            [],
        )

        board_column = _create_board_column(
            page,
            active_board,
            title=title,
            accent_color=accent_color,
            tasks=tasks,
        )
        board_column.grid(
            row=0,
            column=column_index,
            padx=(
                0 if column_index == 0 else 5,
                0 if column_index == 3 else 5,
            ),
            sticky="nsew",
        )


def _create_board_column(
    page: StandardPage,
    parent: ctk.CTkBaseClass,
    *,
    title: str,
    accent_color: str,
    tasks: list[dict[str, Any]],
) -> ctk.CTkFrame:
    """Create one independently scrollable Task Board column."""

    column = ctk.CTkFrame(
        parent,
        height=BOARD_COLUMN_HEIGHT,
        fg_color=theme.INPUT_BG,
        border_color=theme.CARD_BORDER,
        border_width=theme.BORDER_WIDTH,
        corner_radius=theme.CARD_CORNER_RADIUS,
    )

    column.grid_propagate(False)
    column.grid_columnconfigure(0, weight=1)
    column.grid_rowconfigure(2, weight=1)

    heading = ctk.CTkFrame(
        column,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
    )
    heading.grid(
        row=0,
        column=0,
        padx=12,
        pady=(12, 8),
        sticky="ew",
    )
    heading.grid_columnconfigure(0, weight=1)

    heading_label = create_card_title(
        heading,
        title.upper(),
    )
    heading_label.configure(
        text_color=accent_color,
    )
    heading_label.grid(
        row=0,
        column=0,
        sticky="w",
    )

    create_small_label(
        heading,
        str(len(tasks)),
        muted=True,
    ).grid(
        row=0,
        column=1,
        sticky="e",
    )

    ctk.CTkFrame(
        column,
        height=2,
        fg_color=accent_color,
        corner_radius=1,
    ).grid(
        row=1,
        column=0,
        padx=12,
        sticky="ew",
    )

    task_list = ctk.CTkScrollableFrame(
        column,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
        scrollbar_button_color=theme.CARD_BORDER,
        scrollbar_button_hover_color=theme.TEXT_MUTED,
    )
    task_list.grid(
        row=2,
        column=0,
        padx=(5, 2),
        pady=(6, 2),
        sticky="nsew",
    )
    task_list.grid_columnconfigure(0, weight=1)

    if tasks:
        for task_row, task in enumerate(tasks):
            task_card = _create_live_task_card(
                page,
                task_list,
                task=task,
                accent_color=accent_color,
            )
            task_card.grid(
                row=task_row,
                column=0,
                padx=3,
                pady=(0, 8),
                sticky="ew",
            )
    else:
        empty_message = create_small_label(
            task_list,
            "No matching tasks",
            muted=True,
        )
        empty_message.grid(
            row=0,
            column=0,
            padx=7,
            pady=14,
            sticky="w",
        )

    add_task_label = create_small_label(
        column,
        "+ Add Task",
        muted=False,
        bold=True,
    )
    add_task_label.configure(
        text_color=accent_color,
    )
    add_task_label.grid(
        row=3,
        column=0,
        padx=12,
        pady=(7, 12),
        sticky="w",
    )

    make_clickable(
        add_task_label,
        lambda selected_status=title: _open_new_task_dialog(
            page,
            default_status=selected_status,
        ),
    )

    return column


def _create_live_task_card(
    page: StandardPage,
    parent: ctk.CTkBaseClass,
    *,
    task: dict[str, Any],
    accent_color: str,
) -> ctk.CTkFrame:
    """Create a selectable card from one real saved task."""

    card = create_card(parent)
    card.grid_columnconfigure(
        0,
        weight=1,
    )

    create_body_label(
        card,
        task["title"],
        bold=True,
        wraplength=205,
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        padx=11,
        pady=(11, 5),
        sticky="w",
    )

    notes = task["notes"]

    if notes:
        description_label = create_small_label(
            card,
            notes,
            muted=True,
        )
        description_label.configure(
            wraplength=205,
            justify="left",
        )
        description_label.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=11,
            pady=(0, 9),
            sticky="w",
        )

    system_label = ctk.CTkLabel(
        card,
        text=f"  {task['system'].upper()}  ",
        height=21,
        fg_color=theme.ACCENT_ORANGE_DARK,
        text_color=accent_color,
        corner_radius=3,
        font=theme.FONT_SMALL_BOLD,
    )
    system_label.grid(
        row=2,
        column=0,
        padx=(11, 5),
        pady=(0, 11),
        sticky="w",
    )

    priority_label = create_small_label(
        card,
        task["priority"].upper(),
        muted=False,
        bold=True,
    )
    priority_label.configure(
        text_color=_priority_color(
            task["priority"]
        )
    )
    priority_label.grid(
        row=2,
        column=1,
        padx=(5, 11),
        pady=(0, 11),
        sticky="e",
    )

    card.task_data = task

    task_id = task.get("id")

    if task_id:
        page.task_cards[task_id] = card

    make_hoverable(card)

    make_clickable(
        card,
        lambda selected_task=task, selected_card=card: _select_task(
            page,
            selected_task,
            selected_card,
        ),
    )

    # card.after_idle(
    #     lambda: _bind_double_click_recursive(
    #         card,
    #         lambda: _open_edit_task_dialog(
    #             page,
    #             task,
    #         ),
    #     )
    # )

    return card

# def _bind_double_click_recursive(
#     widget: ctk.CTkBaseClass,
#     command,
#     *,
#     interval: float = 0.35,
# ) -> None:
#     """
#     Detect a double-click manually across a CustomTkinter widget.
#
#     CustomTkinter can intercept native double-click events through its
#     internal canvas and label widgets, so this compares two normal
#     left-click timestamps instead.
#     """
#
#     last_click_time = 0.0
#     bound_widgets = set()

    # def handle_click(_event=None):
    #     nonlocal last_click_time
    #
    #     current_time = time.monotonic()
    #
    #     if current_time - last_click_time <= interval:
    #         last_click_time = 0.0
    #         command()
    #         return "break"
    #
    #     last_click_time = current_time
    #
    # def bind_target(target) -> None:
    #     if target is None:
    #         return
    #
    #     target_id = str(target)
    #
    #     if target_id in bound_widgets:
    #         return
    #
    #     bound_widgets.add(target_id)
    #
    #     try:
    #         target.bind(
    #             "<Button-1>",
    #             handle_click,
    #             add="+",
    #         )
    #     except (AttributeError, TypeError):
    #         pass
    #
    #     try:
    #         for child in target.winfo_children():
    #             bind_target(child)
    #     except AttributeError:
    #         pass
    #
    #     for attribute_name in (
    #         "_canvas",
    #         "_text_label",
    #         "_label",
    #     ):
    #         bind_target(
    #             getattr(
    #                 target,
    #                 attribute_name,
    #                 None,
    #             )
    #         )
    #
    # bind_target(widget)

def _bind_task_board_shortcuts(
    page: StandardPage,
) -> None:
    """Bind shortcuts and remove them when the Task Board closes."""

    application = page.winfo_toplevel()

    # Remove any Task Board shortcuts left by an older page instance.
    _unbind_task_board_shortcuts(application)

    application.task_board_binding_ids = {
        "<Control-n>": application.bind(
            "<Control-n>",
            lambda _event: _open_new_task_dialog(page),
            add="+",
        ),
        "<Control-f>": application.bind(
            "<Control-f>",
            lambda _event: _focus_task_search(page),
            add="+",
        ),
        "<Escape>": application.bind(
            "<Escape>",
            lambda _event: _clear_task_selection(page),
            add="+",
        ),
    }

    page.bind(
        "<Destroy>",
        lambda event: _handle_task_board_destroy(
            event,
            page,
            application,
        ),
        add="+",
    )

def _handle_task_board_destroy(
    event,
    page: StandardPage,
    application,
) -> None:
    """Clean up shortcuts when this Task Board page is destroyed."""

    # Destroy events also fire for child widgets. Only react when the
    # StandardPage itself is being destroyed.
    if event.widget is page:
        _unbind_task_board_shortcuts(application)

def _unbind_task_board_shortcuts(
    application,
) -> None:
    """Remove keyboard bindings created by the Task Board."""

    binding_ids = getattr(
        application,
        "task_board_binding_ids",
        {},
    )

    for sequence, binding_id in binding_ids.items():
        if binding_id:
            try:
                application.unbind(
                    sequence,
                    binding_id,
                )
            except Exception:
                pass

    application.task_board_binding_ids = {}

def _focus_task_search(
    page: StandardPage,
) -> None:
    """Focus and select the Task Board search field."""

    if not page.winfo_exists():
        return

    search_entry = getattr(
        page,
        "search_entry",
        None,
    )

    if (
        search_entry is None
        or not search_entry.winfo_exists()
    ):
        return

    search_entry.focus_set()
    search_entry.select_range(
        0,
        "end",
    )

def _clear_task_selection(
    page: StandardPage,
) -> None:
    """Clear the selected task and reset the Inspector."""

    selected_card = page.selected_task_card

    if (
        selected_card is not None
        and selected_card.winfo_exists()
    ):
        selected_card.configure(
            border_color=theme.CARD_BORDER,
            border_width=theme.BORDER_WIDTH,
        )

    page.selected_task = None
    page.selected_task_card = None

    inspector = getattr(
        page,
        "inspector",
        None,
    )

    if inspector is not None:
        inspector.show_empty_state()

def _open_new_task_dialog(
    page: StandardPage,
    *,
    default_status: str = "Planned",
) -> None:
    """Open the reusable dialog for a new task."""

    dialog = TaskDialog(
        page,
        systems=page.available_systems,
        on_save=lambda task_payload: _save_new_task_from_dialog(
            page,
            task_payload,
            default_status=default_status,
        ),
    )

    dialog.status_variable.set(
        default_status
    )

def _open_edit_task_dialog(
    page: StandardPage,
    task: dict[str, Any],
) -> None:
    """Open the reusable Task Dialog in edit mode."""

    TaskDialog(
        page,
        systems=page.available_systems,
        task=task,
        on_save=lambda task_payload: _save_edited_task_from_dialog(
            page,
            task,
            task_payload,
        ),
    )

def _save_edited_task_from_dialog(
    page: StandardPage,
    original_task: dict[str, Any],
    task_payload: dict[str, Any],
) -> None:
    """Save edits, refresh the board, and preserve selection."""

    previous_status = original_task.get(
        "normalized_status",
        original_task.get("status", "Planned"),
    )

    new_status = task_payload.get(
        "status",
        "Planned",
    )

    completed_at = original_task.get(
        "completed_at"
    )

    if (
        new_status == "Complete"
        and previous_status != "Complete"
    ):
        completed_at = datetime.now().strftime(
            "%m-%d-%y %H:%M:%S"
        )

    elif new_status != "Complete":
        completed_at = None

    updated_task = {
        "id": original_task.get("id"),
        "title": task_payload.get(
            "title",
            original_task.get(
                "title",
                "Untitled Task",
            ),
        ),
        "system": task_payload.get(
            "system",
            original_task.get(
                "system",
                "Unassigned",
            ),
        ),
        "priority": task_payload.get(
            "priority",
            original_task.get(
                "priority",
                "Medium",
            ),
        ),
        "status": new_status,
        "notes": task_payload.get(
            "notes",
            original_task.get(
                "notes",
                "",
            ),
        ),
        "created_at": original_task.get(
            "created_at"
        ),
        "completed_at": completed_at,
    }

    update_task(
        updated_task
    )

    application = page.winfo_toplevel()

    application.pending_task_id = updated_task["id"]

    application.show_page(
        "task_board"
    )



def _save_new_task_from_dialog(
    page: StandardPage,
    task_payload: dict[str, Any],
    *,
    default_status: str = "Planned",
) -> None:
    """Create, save, and display a new task."""

    status = (
        task_payload.get("status")
        or default_status
    )

    now = datetime.now()

    new_task = {
        "id": str(uuid4()),
        "title": task_payload.get(
            "title",
            "Untitled Task",
        ),
        "system": task_payload.get(
            "system",
            "Unassigned",
        ),
        "priority": task_payload.get(
            "priority",
            "Medium",
        ),
        "status": status,
        "notes": task_payload.get(
            "notes",
            "",
        ),
        "created_at": now.strftime(
            "%m-%d-%y %H:%M:%S"
        ),
        "completed_at": (
            now.strftime("%m-%d-%y %H:%M:%S")
            if status == "Complete"
            else None
        ),
    }

    save_new_task(
        new_task
    )

    application = page.winfo_toplevel()

    application.pending_task_id = new_task["id"]

    application.show_page(
        "task_board"
    )


# =========================================================
# COMPLETED SECTION
# =========================================================

def _build_completed_section(
    page: StandardPage,
    parent: ctk.CTkBaseClass,
    tasks: list[dict[str, Any]],
    *,
    row: int,
) -> None:
    """Create the collapsible completed-task archive."""

    completed_card = create_card(parent)
    completed_card.grid(
        row=row,
        column=0,
        pady=(0, theme.PAGE_PADDING_Y),
        sticky="ew",
    )
    completed_card.grid_columnconfigure(0, weight=1)

    header = ctk.CTkFrame(
        completed_card,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
    )
    header.grid(
        row=0,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=theme.CARD_PADDING_Y,
        sticky="ew",
    )
    header.grid_columnconfigure(0, weight=1)

    arrow = "▼" if page.completed_expanded else "▶"

    title_label = create_section_title(
        header,
        f"{arrow} Completed",
    )
    title_label.grid(
        row=0,
        column=0,
        sticky="w",
    )

    create_small_label(
        header,
        (
            "Finished work remains available for reference "
            "without occupying the active board."
        ),
        muted=True,
    ).grid(
        row=1,
        column=0,
        pady=(3, 0),
        sticky="w",
    )

    create_small_label(
        header,
        f"{len(tasks)} tasks",
        muted=True,
        bold=True,
    ).grid(
        row=0,
        column=1,
        rowspan=2,
        sticky="e",
    )

    make_clickable(
        header,
        lambda: _toggle_completed_section(page),
    )

    if not page.completed_expanded:
        return

    completed_grid = ctk.CTkFrame(
        completed_card,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
    )
    completed_grid.grid(
        row=1,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=(0, theme.CARD_PADDING_Y),
        sticky="ew",
    )

    for column_index in range(4):
        completed_grid.grid_columnconfigure(
            column_index,
            weight=1,
            uniform="completed_tasks",
        )

    if not tasks:
        create_small_label(
            completed_grid,
            "No completed tasks match the current filters.",
            muted=True,
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            pady=12,
            sticky="w",
        )
        return

    visible_tasks = tasks[:COMPLETED_PREVIEW_LIMIT]

    for task_index, task in enumerate(visible_tasks):
        grid_row = task_index // 4
        grid_column = task_index % 4

        task_card = _create_completed_task_card(
            page,
            completed_grid,
            task=task,
        )
        task_card.grid(
            row=grid_row,
            column=grid_column,
            padx=(
                0 if grid_column == 0 else 5,
                0 if grid_column == 3 else 5,
            ),
            pady=(0, 10),
            sticky="nsew",
        )

    hidden_count = len(tasks) - len(visible_tasks)

    if hidden_count > 0:
        create_small_label(
            completed_grid,
            (
                f"{hidden_count} additional completed tasks are hidden. "
                "Use search and filters to narrow the archive."
            ),
            muted=True,
        ).grid(
            row=(len(visible_tasks) + 3) // 4,
            column=0,
            columnspan=4,
            pady=(4, 8),
            sticky="w",
        )

def _toggle_completed_section(
    page: StandardPage,
) -> None:
    """Expand or collapse the completed-task archive."""

    page.completed_expanded = not page.completed_expanded

    _refresh_task_board(page)


def _create_completed_task_card(
    page: StandardPage,
    parent: ctk.CTkBaseClass,
    *,
    task: dict[str, Any],
) -> ctk.CTkFrame:
    """Create one selectable completed-task card."""

    card = create_card(parent)
    card.grid_columnconfigure(
        0,
        weight=1,
    )

    create_body_label(
        card,
        task["title"],
        bold=True,
        wraplength=190,
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        padx=11,
        pady=(11, 8),
        sticky="w",
    )

    create_small_label(
        card,
        task["system"],
        muted=True,
    ).grid(
        row=1,
        column=0,
        padx=(11, 5),
        pady=(0, 11),
        sticky="w",
    )

    status_label = create_small_label(
        card,
        "COMPLETE",
        muted=False,
        bold=True,
    )
    status_label.configure(
        text_color=theme.SUCCESS,
    )
    status_label.grid(
        row=1,
        column=1,
        padx=(5, 11),
        pady=(0, 11),
        sticky="e",
    )

    card.task_data = task

    task_id = task.get("id")

    if task_id:
        page.task_cards[task_id] = card

    make_hoverable(card)

    make_clickable(
        card,
        lambda selected_task=task, selected_card=card: _select_task(
            page,
            selected_task,
            selected_card,
        ),
    )

    # card.after_idle(
    #     lambda: _bind_double_click_recursive(
    #         card,
    #         lambda: _open_edit_task_dialog(
    #             page,
    #             task,
    #         ),
    #     )
    # )

    return card


# =========================================================
# INSPECTOR
# =========================================================

def _build_inspector(
    page: StandardPage,
) -> None:
    """Create the persistent Task Inspector."""

    if page.details is None:
        return

    inspector = Inspector(
        page.details,
        title="Task Inspector",
        empty_title="No task selected",
        empty_message=(
            "Select a task card to inspect its description, "
            "system, priority, status, notes, and related work."
        ),
    )
    inspector.grid(
        row=0,
        column=0,
        sticky="nsew",
    )

    page.inspector = inspector

def _select_task(
    page: StandardPage,
    task: dict[str, Any],
    task_card: ctk.CTkFrame,
) -> None:
    """Select a task, style its card, and populate the Inspector."""

    previous_card = page.selected_task_card

    if (
        previous_card is not None
        and previous_card.winfo_exists()
    ):
        previous_card.configure(
            border_color=theme.CARD_BORDER,
            border_width=theme.BORDER_WIDTH,
        )

    page.selected_task = task
    page.selected_task_card = task_card

    task_card.configure(
        border_color=theme.ACCENT_ORANGE,
        border_width=2,
    )

    _populate_task_inspector(
        page,
        task,
    )

def _populate_task_inspector(
    page: StandardPage,
    task: dict[str, Any],
) -> None:
    """Display the selected task inside the reusable Inspector."""

    inspector = getattr(
        page,
        "inspector",
        None,
    )

    if inspector is None:
        return

    inspector.clear()

    inspector.set_header(
        task["title"],
        task["system"],
    )

    inspector.add_info_section(
        "Overview",
        [
            (
                "System",
                task["system"],
            ),
            (
                "Priority",
                task["priority"],
            ),
            (
                "Status",
                task["normalized_status"],
            ),
            (
                "Created",
                _format_task_date(
                    task.get("created_at")
                ),
            ),
            (
                "Completed",
                _format_completed_date(
                    task.get("completed_at")
                ),
            ),
        ],
        row=0,
    )

    notes = (
        task.get("notes")
        or "No description or notes have been recorded."
    )

    inspector.add_text_section(
        "Description",
        notes,
        row=1,
    )

    inspector.add_text_section(
        "Related Work",
        (
            "Related development logs, roadmap milestones, "
            "assets, and system documentation will appear here "
            "as those relationships are added."
        ),
        row=2,
    )

    inspector.set_actions(
        secondary_text="Change Status",
        secondary_command=lambda: _open_status_dialog(
            page,
            task,
        ),
        primary_text="Edit Task",
        primary_command=lambda: _open_edit_task_dialog(
            page,
            task,
        ),
    )

    _delete_button = create_danger_button(
        inspector.content,
        "Delete Task",
        command=lambda: _open_delete_confirmation(
            page,
            task,
        ),
        width=220,
    )

    _delete_button.grid(
        row=3,
        column=0,
        pady=(0, theme.SECTION_GAP),
        sticky="ew",
    )

def _open_status_dialog(
    page: StandardPage,
    task: dict[str, Any],
) -> None:
    """Open the focused status-change dialog."""

    StatusDialog(
        page,
        current_status=task.get(
            "normalized_status",
            task.get(
                "status",
                "Planned",
            ),
        ),
        task_title=task.get(
            "title",
            "Untitled Task",
        ),
        on_save=lambda new_status: _save_task_status(
            page,
            task,
            new_status,
        ),
    )

def _save_task_status(
    page: StandardPage,
    task: dict[str, Any],
    new_status: str,
) -> None:
    """Update one task status and preserve its selection."""

    previous_status = task.get(
        "normalized_status",
        task.get(
            "status",
            "Planned",
        ),
    )

    completed_at = task.get(
        "completed_at"
    )

    if (
        new_status == "Complete"
        and previous_status != "Complete"
    ):
        completed_at = datetime.now().strftime(
            "%m-%d-%y %H:%M:%S"
        )

    elif new_status != "Complete":
        completed_at = None

    updated_task = {
        "id": task.get("id"),
        "title": task.get(
            "title",
            "Untitled Task",
        ),
        "system": task.get(
            "system",
            "Unassigned",
        ),
        "priority": task.get(
            "priority",
            "Medium",
        ),
        "status": new_status,
        "notes": task.get(
            "notes",
            "",
        ),
        "created_at": task.get(
            "created_at"
        ),
        "completed_at": completed_at,
    }

    update_task(
        updated_task
    )

    application = page.winfo_toplevel()

    application.pending_task_id = updated_task["id"]

    application.show_page(
        "task_board"
    )

def _select_pending_task(
    page: StandardPage,
) -> None:
    """
    Select a task requested by another page, such as the Dashboard.

    The Dashboard stores the clicked task ID on the main application
    before navigating to the Task Board.
    """

    application = page.winfo_toplevel()

    pending_task_id = getattr(
        application,
        "pending_task_id",
        None,
    )

    if not pending_task_id:
        return

    task = page.task_lookup.get(
        pending_task_id
    )

    task_card = page.task_cards.get(
        pending_task_id
    )

    if (
        task is not None
        and task_card is not None
    ):
        _select_task(
            page,
            task,
            task_card,
        )

    # Prevent an old selection from reopening every time.
    application.pending_task_id = None

def _open_delete_confirmation(
    page: StandardPage,
    task: dict[str, Any],
) -> None:
    """Ask the user to confirm task deletion."""

    task_title = task.get(
        "title",
        "Untitled Task",
    )

    ConfirmationDialog(
        page,
        title="Delete Task",
        message=(
            f'Permanently delete "{task_title}"?\n\n'
            "This action cannot be undone."
        ),
        confirm_text="Delete Task",
        on_confirm=lambda: _delete_selected_task(
            page,
            task,
        ),
    )

def _delete_selected_task(
    page: StandardPage,
    task: dict[str, Any],
) -> None:
    """Delete a task and refresh the Task Board."""

    task_id = task.get("id")

    if not task_id:
        print(
            "Unable to delete task: missing task ID."
        )
        return

    delete_task(
        task_id
    )

    application = page.winfo_toplevel()

    application.pending_task_id = None

    application.show_page(
        "task_board"
    )

def _format_task_date(
    value: Any,
) -> str:
    """Format a saved task timestamp for display."""

    if not value:
        return "Not recorded"

    value_string = str(value).strip()

    supported_formats = (
        "%m-%d-%y %H:%M:%S",
        "%m-%d-%Y %H:%M:%S",
        "%m/%d/%Y",
        "%Y-%m-%d",
    )

    for date_format in supported_formats:
        try:
            parsed_date = datetime.strptime(
                value_string,
                date_format,
            )

            return parsed_date.strftime(
                "%b %d, %Y"
            ).replace(
                " 0",
                " ",
            )

        except ValueError:
            continue

    return value_string

def _format_completed_date(
    value: Any,
) -> str:
    """Format a completion date or show an active-task message."""

    if not value:
        return "Not completed"

    return _format_task_date(value)


# =========================================================
# HELPERS
# =========================================================

def _priority_color(
    priority: str,
) -> str:
    """Return the configured priority color."""

    return theme.PRIORITY_COLORS.get(
        priority.title(),
        theme.TEXT_MUTED,
    )










