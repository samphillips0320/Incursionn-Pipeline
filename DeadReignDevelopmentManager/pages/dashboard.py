from __future__ import annotations
from typing import Any
import customtkinter as ctk
from pages.dashboard_data import (
    DashboardData,
    load_dashboard_data,
)
from ui import theme
from ui.components import (
    create_body_label,
    create_card,
    create_card_title,
    create_page_title,
    create_primary_button,
    create_progress_bar,
    create_section_title,
    create_small_label,
)
from ui.layout import StandardPage
from ui.components import (
    create_body_label,
    create_card,
    create_card_title,
    create_page_title,
    create_primary_button,
    create_progress_bar,
    create_secondary_button,
    create_section_title,
    create_small_label,
    make_hoverable,
    make_clickable
)
from ui.charts import (
    CircularProgressRing,
    LineChart,
)

from datetime import datetime

BOARD_CONFIGURATION = [
    ("Ideas", theme.WARNING),
    ("Planned", theme.INFO),
    ("In Progress", theme.ACCENT_ORANGE),
    ("Testing", theme.PURPLE),
    ("Complete", theme.SUCCESS),
]


def show_dashboard(
    parent: ctk.CTkBaseClass,
) -> StandardPage:
    """Display the live DR Pipeline Management Dashboard."""

    dashboard_data = load_dashboard_data()

    page = StandardPage(
        parent,
        show_details=False,
        scroll_main=True,
    )
    page.pack(
        fill="both",
        expand=True,
    )

    _build_page_header(
        page,
        dashboard_data,
    )

    _build_dashboard_content(
        page,
        dashboard_data,
    )

    return page


# =========================================================
# HEADER
# =========================================================

def _build_page_header(
    page: StandardPage,
    data: DashboardData,
) -> None:
    """Create the Dashboard heading and current-work summary."""

    page.header.grid_columnconfigure(0, weight=1)

    title = create_page_title(
        page.header,
        "Dashboard",
    )
    title.grid(
        row=0,
        column=0,
        sticky="w",
    )

    if data.current_focus == "No active task":
        subtitle_text = (
            "Welcome back. No active tasks are currently waiting."
        )
    else:
        subtitle_text = (
            f"Welcome back. Current focus: "
            f"{data.current_system} — {data.current_focus}"
        )

    subtitle = create_small_label(
        page.header,
        subtitle_text,
        muted=True,
    )
    subtitle.grid(
        row=1,
        column=0,
        pady=(4, 0),
        sticky="w",
    )

    refreshed_text = datetime.now().strftime(
        "Refreshed %I:%M %p"
    ).lstrip("0")

    refreshed_label = create_small_label(
        page.header,
        refreshed_text,
        muted=True,
    )
    refreshed_label.grid(
        row=0,
        column=1,
        rowspan=2,
        sticky="e",
    )

    page.toolbar.grid_remove()


# =========================================================
# DASHBOARD STRUCTURE
# =========================================================

def _build_dashboard_content(
    page: StandardPage,
    data: DashboardData,
) -> None:
    """Build the live interactive Dashboard content."""

    main = page.main
    main.grid_columnconfigure(0, weight=1)

    _build_top_row(
        main,
        data,
        row=0,
    )

    _build_quick_actions(
        main,
        row=1,
    )

    _build_task_board(
        main,
        data,
        row=2,
    )

    _build_bottom_row(
        main,
        data,
        row=3,
    )


# =========================================================
# TOP CARDS
# =========================================================

def _build_top_row(
    parent: ctk.CTkBaseClass,
    data: DashboardData,
    *,
    row: int,
) -> None:
    """Create the four Dashboard overview cards."""

    container = _create_equal_column_container(
        parent,
        columns=4,
    )
    container.grid(
        row=row,
        column=0,
        pady=(0, theme.SECTION_GAP),
        sticky="ew",
    )

    cards = [
        _create_project_card(container, data),
        _create_current_tasks_card(container, data),
        _create_latest_log_card(container, data),
        _create_progress_card(container, data),
    ]

    _grid_equal_cards(cards)

def _build_quick_actions(
    parent: ctk.CTkBaseClass,
    *,
    row: int,
) -> None:
    """Create the Dashboard's primary navigation shortcuts."""

    card = create_card(parent)
    card.grid(
        row=row,
        column=0,
        pady=(0, theme.SECTION_GAP),
        sticky="ew",
    )

    card.grid_columnconfigure(0, weight=1)
    card.grid_columnconfigure(1, weight=0)
    card.grid_columnconfigure(2, weight=0)
    card.grid_columnconfigure(3, weight=0)
    card.grid_columnconfigure(4, weight=0)

    title_frame = ctk.CTkFrame(
        card,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
    )
    title_frame.grid(
        row=0,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=theme.CARD_PADDING_Y,
        sticky="w",
    )

    create_card_title(
        title_frame,
        "QUICK ACTIONS",
    ).grid(
        row=0,
        column=0,
        sticky="w",
    )

    create_small_label(
        title_frame,
        "Jump directly into your most common workflows.",
        muted=True,
    ).grid(
        row=1,
        column=0,
        pady=(3, 0),
        sticky="w",
    )

    new_task_button = create_primary_button(
        card,
        "+ New Task",
        command=lambda: _navigate_to(
            card,
            "task_board",
        ),
        width=115,
    )
    new_task_button.grid(
        row=0,
        column=1,
        padx=(8, 4),
        pady=theme.CARD_PADDING_Y,
    )

    new_log_button = create_secondary_button(
        card,
        "+ Dev Log",
        command=lambda: _navigate_to(
            card,
            "development_log",
        ),
        width=115,
    )
    new_log_button.grid(
        row=0,
        column=2,
        padx=4,
        pady=theme.CARD_PADDING_Y,
    )

    systems_button = create_secondary_button(
        card,
        "Systems",
        command=lambda: _navigate_to(
            card,
            "systems",
        ),
        width=105,
    )
    systems_button.grid(
        row=0,
        column=3,
        padx=4,
        pady=theme.CARD_PADDING_Y,
    )

    roadmap_button = create_secondary_button(
        card,
        "Roadmap",
        command=lambda: _navigate_to(
            card,
            "roadmap",
        ),
        width=105,
    )
    roadmap_button.grid(
        row=0,
        column=4,
        padx=(4, theme.CARD_PADDING_X),
        pady=theme.CARD_PADDING_Y,
    )


def _create_project_card(
    parent: ctk.CTkBaseClass,
    data: DashboardData,
) -> ctk.CTkFrame:
    """Create the current project focus card."""

    card = create_card(parent)
    card.grid_columnconfigure(0, weight=1)
    card.grid_columnconfigure(1, weight=0)

    _add_card_header(
        card,
        "PROJECT OVERVIEW",
        columnspan=2,
    )

    details = ctk.CTkFrame(
        card,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
    )
    details.grid(
        row=2,
        column=0,
        padx=(theme.CARD_PADDING_X, 8),
        pady=(8, 4),
        sticky="nsew",
    )
    details.grid_columnconfigure(0, weight=1)

    create_small_label(
        details,
        "Current Milestone",
        muted=True,
    ).grid(
        row=0,
        column=0,
        sticky="w",
    )

    create_body_label(
        details,
        "Vertical Slice",
        bold=True,
    ).grid(
        row=1,
        column=0,
        pady=(2, 12),
        sticky="w",
    )

    create_small_label(
        details,
        "Current Focus",
        muted=True,
    ).grid(
        row=2,
        column=0,
        sticky="w",
    )

    focus_text = data.current_focus

    if data.current_system != "Unassigned":
        focus_text = (
            f"{data.current_system} - "
            f"{data.current_focus}"
        )

    create_body_label(
        details,
        focus_text,
        bold=True,
        wraplength=160,
    ).grid(
        row=3,
        column=0,
        pady=(2, 0),
        sticky="w",
    )

    progress_ring = CircularProgressRing(
        card,
        progress=data.completion_progress,
        size=115,
        thickness=10,
        label="Complete",
    )
    progress_ring.grid(
        row=2,
        column=1,
        padx=(0, theme.CARD_PADDING_X),
        pady=(10, 4),
        sticky="ne",
    )

    stats = ctk.CTkFrame(
        card,
        fg_color=theme.INPUT_BG,
        corner_radius=theme.CARD_CORNER_RADIUS,
    )
    stats.grid(
        row=3,
        column=0,
        columnspan=2,
        padx=theme.CARD_PADDING_X,
        pady=(8, 12),
        sticky="ew",
    )

    stats.grid_columnconfigure(0, weight=1)
    stats.grid_columnconfigure(1, weight=1)

    _add_compact_stat(
        stats,
        column=0,
        title="Open Tasks",
        value=str(data.open_tasks),
    )

    _add_compact_stat(
        stats,
        column=1,
        title="Completed",
        value=str(data.completed_tasks),
    )

    button = create_primary_button(
        card,
        "Continue Where I Left Off",
        command=lambda: _navigate_to(
            card,
            "task_board",
        ),
        width=210,
    )
    button.grid(
        row=4,
        column=0,
        columnspan=2,
        padx=theme.CARD_PADDING_X,
        pady=(0, theme.CARD_PADDING_Y),
        sticky="ew",
    )

    make_hoverable(card)

    return card


def _create_current_tasks_card(
    parent: ctk.CTkBaseClass,
    data: DashboardData,
) -> ctk.CTkFrame:
    """Create a preview of current open tasks."""

    card = create_card(parent)
    card.grid_columnconfigure(0, weight=1)

    _add_card_header(
        card,
        "CURRENT TASKS",
    )

    if not data.current_tasks:
        create_body_label(
            card,
            "No open tasks. The board is gloriously quiet.",
            muted=True,
            wraplength=230,
        ).grid(
            row=2,
            column=0,
            padx=theme.CARD_PADDING_X,
            pady=theme.CARD_PADDING_Y,
            sticky="w",
        )
    else:
        for index, task in enumerate(
                data.current_tasks,
                start=2,
        ):
            task_row = _create_current_task_row(
                card,
                task,
            )

            task_row.grid(
                row=index,
                column=0,
                padx=theme.CARD_PADDING_X,
                pady=4,
                sticky="ew",
            )

            make_clickable(
                task_row,
                lambda selected_task=task: _open_task(
                    task_row,
                    selected_task,
                ),
            )

    link = _create_orange_link(
        card,
        "View All Tasks  →",
    )

    make_hoverable(card)

    # make_clickable(
    #     card,
    #     lambda: _navigate_to(
    #         card,
    #         "task_board",
    #     ),
    # )

    return card



def _create_latest_log_card(
    parent: ctk.CTkBaseClass,
    data: DashboardData,
) -> ctk.CTkFrame:
    """Create the newest saved development-log preview."""

    card = create_card(parent)
    card.grid_columnconfigure(0, weight=1)

    _add_card_header(
        card,
        "LATEST DEVELOPMENT LOG",
    )

    log = data.latest_log

    if log is None:
        create_body_label(
            card,
            "No development entries have been recorded yet.",
            muted=True,
            wraplength=240,
        ).grid(
            row=2,
            column=0,
            padx=theme.CARD_PADDING_X,
            pady=theme.CARD_PADDING_Y,
            sticky="w",
        )
        return card

    create_small_label(
        card,
        log["date"] or "Date not recorded",
        muted=True,
    ).grid(
        row=2,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=(10, 2),
        sticky="w",
    )

    title = (
        log["work_completed"]
        or f"{log['system']} Development Entry"
    )

    title_label = create_card_title(
        card,
        title,
    )
    title_label.configure(
        text_color=theme.ACCENT_ORANGE,
        wraplength=245,
        justify="left",
    )
    title_label.grid(
        row=3,
        column=0,
        padx=theme.CARD_PADDING_X,
        sticky="w",
    )

    create_small_label(
        card,
        f"System: {log['system']}",
        muted=True,
    ).grid(
        row=4,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=(8, 0),
        sticky="w",
    )

    detail_title, detail_value = _get_log_detail(log)

    create_small_label(
        card,
        detail_title,
        muted=True,
        bold=True,
    ).grid(
        row=5,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=(12, 4),
        sticky="w",
    )

    create_body_label(
        card,
        detail_value,
        muted=True,
        wraplength=245,
    ).grid(
        row=6,
        column=0,
        padx=theme.CARD_PADDING_X,
        sticky="w",
    )

    media_parts = []

    if log["screenshot_captured"]:
        media_parts.append("Screenshot")

    if log["video_recorded"]:
        media_parts.append("Video")

    if log["git_commit_created"]:
        media_parts.append("Git commit")

    media_text = (
        " • ".join(media_parts)
        if media_parts
        else "No media recorded"
    )

    create_small_label(
        card,
        media_text,
        muted=True,
    ).grid(
        row=7,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=(12, 0),
        sticky="w",
    )

    log_link = _create_orange_link(
        card,
        "Read Full Log  →",
    )

    log_link.grid(
        row=8,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=(14, theme.CARD_PADDING_Y),
        sticky="w",
    )

    make_hoverable(card)

    make_clickable(
        log_link,
        lambda: _navigate_to(
            card,
            "development_log",
        ),
    )

    return card


def _create_progress_card(
    parent: ctk.CTkBaseClass,
    data: DashboardData,
) -> ctk.CTkFrame:
    """Create the live task activity and completion panel."""

    card = create_card(parent)
    card.grid_columnconfigure(0, weight=1)

    _add_card_header(
        card,
        "PROGRESS OVERVIEW",
    )

    heading = ctk.CTkFrame(
        card,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
    )
    heading.grid(
        row=2,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=(10, 5),
        sticky="ew",
    )
    heading.grid_columnconfigure(0, weight=1)

    create_body_label(
        heading,
        "Tasks Added",
        bold=True,
    ).grid(
        row=0,
        column=0,
        sticky="w",
    )

    create_small_label(
        heading,
        "Last 14 days",
        muted=True,
    ).grid(
        row=0,
        column=1,
        sticky="e",
    )

    chart = LineChart(
        card,
        values=data.task_creation_values,
        labels=data.task_creation_labels,
        line_color=theme.ACCENT_ORANGE,
        fill_color=theme.ACCENT_ORANGE_DARK,
        height=125,
    )
    chart.grid(
        row=3,
        column=0,
        padx=theme.CARD_PADDING_X,
        sticky="ew",
    )

    status_frame = ctk.CTkFrame(
        card,
        fg_color=theme.INPUT_BG,
        corner_radius=theme.CARD_CORNER_RADIUS,
    )
    status_frame.grid(
        row=4,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=(12, theme.CARD_PADDING_Y),
        sticky="ew",
    )

    for column in range(3):
        status_frame.grid_columnconfigure(
            column,
            weight=1,
        )

    _add_compact_stat(
        status_frame,
        column=0,
        title="Completion",
        value=_format_percentage(
            data.completion_progress
        ),
    )

    _add_compact_stat(
        status_frame,
        column=1,
        title="In Progress",
        value=str(data.in_progress_tasks),
    )

    _add_compact_stat(
        status_frame,
        column=2,
        title="Systems",
        value=str(len(data.systems)),
    )

    make_hoverable(card)

    return card


# =========================================================
# TASK BOARD
# =========================================================

def _build_task_board(
    parent: ctk.CTkBaseClass,
    data: DashboardData,
    *,
    row: int,
) -> None:
    """Create the live compact Task Board preview."""

    board = create_card(parent)
    board.grid(
        row=row,
        column=0,
        pady=(0, theme.SECTION_GAP),
        sticky="ew",
    )
    board.grid_columnconfigure(0, weight=1)

    heading = ctk.CTkFrame(
        board,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
    )
    heading.grid(
        row=0,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=(theme.CARD_PADDING_Y, 10),
        sticky="ew",
    )
    heading.grid_columnconfigure(0, weight=1)

    create_section_title(
        heading,
        "Task Board",
    ).grid(
        row=0,
        column=0,
        sticky="w",
    )

    create_primary_button(
        heading,
        "+ Add Task",
        command=lambda: _navigate_to(
            board,
            "task_board",
        ),
        width=105,
    ).grid(
        row=0,
        column=1,
        sticky="e",
    )

    columns = _create_equal_column_container(
        board,
        columns=5,
    )
    columns.grid(
        row=1,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=(0, theme.CARD_PADDING_Y),
        sticky="ew",
    )

    task_columns = []

    for title, color in BOARD_CONFIGURATION:
        task_columns.append(
            _create_board_column(
                columns,
                title=title,
                accent_color=color,
                tasks=data.board_columns.get(
                    title,
                    [],
                ),
            )
        )

    _grid_equal_cards(
        task_columns,
        gap=5,
    )


def _create_board_column(
    parent: ctk.CTkBaseClass,
    *,
    title: str,
    accent_color: str,
    tasks: list[dict[str, Any]],
) -> ctk.CTkFrame:
    """Create one live Dashboard Kanban column."""

    column = ctk.CTkFrame(
        parent,
        fg_color=theme.INPUT_BG,
        border_color=theme.CARD_BORDER,
        border_width=theme.BORDER_WIDTH,
        corner_radius=theme.CARD_CORNER_RADIUS,
    )
    column.grid_columnconfigure(0, weight=1)

    heading = ctk.CTkFrame(
        column,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
    )
    heading.grid(
        row=0,
        column=0,
        padx=10,
        pady=(11, 7),
        sticky="ew",
    )
    heading.grid_columnconfigure(0, weight=1)

    title_label = create_card_title(
        heading,
        title.upper(),
    )
    title_label.configure(
        text_color=accent_color,
    )
    title_label.grid(
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
        padx=10,
        sticky="ew",
    )

    if not tasks:
        create_small_label(
            column,
            "No tasks",
            muted=True,
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=14,
            sticky="w",
        )
    else:
        for index, task in enumerate(
            tasks,
            start=2,
        ):
            _create_task_card(
                column,
                task,
                accent_color,
            ).grid(
                row=index,
                column=0,
                padx=7,
                pady=(7, 0),
                sticky="ew",
            )

    create_small_label(
        column,
        "+ Add Task",
        muted=True,
    ).grid(
        row=6,
        column=0,
        padx=10,
        pady=11,
        sticky="w",
    )

    return column


def _create_task_card(
    parent: ctk.CTkBaseClass,
    task: dict[str, Any],
    accent_color: str,
) -> ctk.CTkFrame:
    """Create a compact card from a real saved task."""

    card = create_card(parent)
    card.grid_columnconfigure(0, weight=1)

    create_body_label(
        card,
        task["title"],
        bold=True,
        wraplength=180,
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        padx=9,
        pady=(9, 6),
        sticky="w",
    )

    system_label = ctk.CTkLabel(
        card,
        text=f"  {task['system'].upper()}  ",
        height=20,
        fg_color=theme.ACCENT_ORANGE_DARK,
        text_color=accent_color,
        corner_radius=3,
        font=theme.FONT_SMALL_BOLD,
    )
    system_label.grid(
        row=1,
        column=0,
        padx=(9, 4),
        pady=(0, 9),
        sticky="w",
    )

    priority_label = create_small_label(
        card,
        task["priority"],
        muted=False,
        bold=True,
    )
    priority_label.configure(
        text_color=_priority_color(
            task["priority"]
        )
    )
    priority_label.grid(
        row=1,
        column=1,
        padx=(4, 9),
        pady=(0, 9),
        sticky="e",
    )

    make_hoverable(card)

    make_clickable(
        card,
        lambda: _open_task(
            card,
            task,
        ),
    )

    return card


# =========================================================
# BOTTOM CARDS
# =========================================================

def _build_bottom_row(
    parent: ctk.CTkBaseClass,
    data: DashboardData,
    *,
    row: int,
) -> None:
    """Create the Dashboard summary cards."""

    container = _create_equal_column_container(
        parent,
        columns=5,
    )
    container.grid(
        row=row,
        column=0,
        pady=(0, theme.PAGE_PADDING_Y),
        sticky="ew",
    )

    cards = [
        _create_media_card(container, data),
        _create_status_card(container, data),
        _create_systems_card(container, data),
        _create_activity_card(container, data),
        _create_release_card(container),
    ]

    _grid_equal_cards(
        cards,
        gap=5,
    )


def _create_media_card(
    parent: ctk.CTkBaseClass,
    data: DashboardData,
) -> ctk.CTkFrame:
    """Summarize media captured in development logs."""

    screenshots = sum(
        1
        for entry in data.development_entries
        if entry["screenshot_captured"]
    )

    videos = sum(
        1
        for entry in data.development_entries
        if entry["video_recorded"]
    )

    portfolio_entries = sum(
        1
        for entry in data.development_entries
        if entry["portfolio_worthy"]
    )

    return _create_simple_summary_card(
        parent,
        "CAPTURED MEDIA",
        [
            ("Screenshots", str(screenshots)),
            ("Videos", str(videos)),
            ("Portfolio Entries", str(portfolio_entries)),
        ],
    )


def _create_status_card(
    parent: ctk.CTkBaseClass,
    data: DashboardData,
) -> ctk.CTkFrame:
    """Summarize live task statuses."""

    return _create_simple_summary_card(
        parent,
        "TASK STATUS",
        [
            ("Open", str(data.open_tasks)),
            ("In Progress", str(data.in_progress_tasks)),
            ("Testing", str(data.testing_tasks)),
            ("Complete", str(data.completed_tasks)),
        ],
    )


def _create_systems_card(
    parent: ctk.CTkBaseClass,
    data: DashboardData,
) -> ctk.CTkFrame:
    """Show the most common active systems."""

    system_counts: dict[str, int] = {}

    for task in data.tasks:
        system = task["system"]
        system_counts[system] = (
            system_counts.get(system, 0) + 1
        )

    sorted_systems = sorted(
        system_counts.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:5]

    if not sorted_systems:
        sorted_systems = [
            ("No systems assigned", 0)
        ]

    return _create_simple_summary_card(
        parent,
        "ACTIVE SYSTEMS",
        [
            (name, str(count))
            for name, count in sorted_systems
        ],
    )


def _create_activity_card(
    parent: ctk.CTkBaseClass,
    data: DashboardData,
) -> ctk.CTkFrame:
    """Show recent saved development activity."""

    recent_entries = list(
        reversed(data.development_entries[-4:])
    )

    card = create_card(parent)
    card.grid_columnconfigure(0, weight=1)

    _add_card_header(
        card,
        "RECENT ACTIVITY",
    )

    if not recent_entries:
        create_small_label(
            card,
            "No development activity yet.",
            muted=True,
        ).grid(
            row=2,
            column=0,
            padx=theme.CARD_PADDING_X,
            pady=theme.CARD_PADDING_Y,
            sticky="w",
        )
    else:
        for index, entry in enumerate(
            recent_entries,
            start=2,
        ):
            text = (
                entry["work_completed"]
                or entry["system"]
            )

            activity_label = create_small_label(
                card,
                text,
                muted=False,
            )

            activity_label.grid(
                row=index,
                column=0,
                padx=theme.CARD_PADDING_X,
                pady=5,
                sticky="w",
            )

            make_clickable(
                activity_label,
                lambda: _navigate_to(
                    card,
                    "development_log",
                ),
            )

    return card


def _create_release_card(
    parent: ctk.CTkBaseClass,
) -> ctk.CTkFrame:
    """Keep the symbolic release preview for now."""

    card = create_card(parent)
    card.grid_columnconfigure(0, weight=1)

    _add_card_header(
        card,
        "RELEASE CHECKLIST",
    )

    items = [
        ("Steam Page", False),
        ("Trailer", False),
        ("Achievements", False),
        ("Localization", False),
        ("Optimization", False),
    ]

    for index, (name, completed) in enumerate(
        items,
        start=2,
    ):
        checkbox = ctk.CTkCheckBox(
            card,
            text=name,
            checkbox_width=17,
            checkbox_height=17,
            text_color=theme.TEXT_SECONDARY,
            font=theme.FONT_SMALL,
            state="disabled",
        )
        checkbox.grid(
            row=index,
            column=0,
            padx=theme.CARD_PADDING_X,
            pady=4,
            sticky="w",
        )

        if completed:
            checkbox.select()

    return card


# =========================================================
# HELPERS
# =========================================================

def _create_equal_column_container(
    parent: ctk.CTkBaseClass,
    *,
    columns: int,
) -> ctk.CTkFrame:
    """Create a transparent equal-width column container."""

    frame = ctk.CTkFrame(
        parent,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
    )

    for column in range(columns):
        frame.grid_columnconfigure(
            column,
            weight=1,
            uniform=f"equal_{columns}",
        )

    return frame


def _grid_equal_cards(
    cards: list[ctk.CTkBaseClass],
    *,
    gap: int = 6,
) -> None:
    """Place cards evenly across one row."""

    final_index = len(cards) - 1

    for index, card in enumerate(cards):
        card.grid(
            row=0,
            column=index,
            padx=(
                0 if index == 0 else gap,
                0 if index == final_index else gap,
            ),
            sticky="nsew",
        )


def _add_card_header(
    parent: ctk.CTkBaseClass,
    title: str,
    *,
    columnspan: int = 1,
) -> None:
    """Create a consistent card title and divider."""

    create_card_title(
        parent,
        title,
    ).grid(
        row=0,
        column=0,
        columnspan=columnspan,
        padx=theme.CARD_PADDING_X,
        pady=(theme.CARD_PADDING_Y, 8),
        sticky="w",
    )

    ctk.CTkFrame(
        parent,
        height=1,
        fg_color=theme.CARD_BORDER,
        corner_radius=0,
    ).grid(
        row=1,
        column=0,
        columnspan=columnspan,
        padx=theme.CARD_PADDING_X,
        sticky="ew",
    )


def _add_caption_value(
    parent: ctk.CTkBaseClass,
    *,
    row: int,
    caption: str,
    value: str,
    wraplength: int = 0,
) -> None:
    """Add a caption followed by a value."""

    create_small_label(
        parent,
        caption,
        muted=True,
    ).grid(
        row=row,
        column=0,
        padx=theme.CARD_PADDING_X,
        pady=(10, 2),
        sticky="w",
    )

    create_body_label(
        parent,
        value,
        bold=True,
        wraplength=wraplength,
    ).grid(
        row=row + 1,
        column=0,
        padx=theme.CARD_PADDING_X,
        sticky="w",
    )


def _add_compact_stat(
    parent: ctk.CTkBaseClass,
    *,
    column: int,
    title: str,
    value: str,
) -> None:
    """Add a small title/value metric."""

    frame = ctk.CTkFrame(
        parent,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
    )
    frame.grid(
        row=0,
        column=column,
        padx=8,
        pady=9,
        sticky="ew",
    )

    create_small_label(
        frame,
        title,
        muted=True,
    ).grid(
        row=0,
        column=0,
        sticky="w",
    )

    create_body_label(
        frame,
        value,
        bold=True,
    ).grid(
        row=1,
        column=0,
        pady=(2, 0),
        sticky="w",
    )


def _create_current_task_row(
    parent: ctk.CTkBaseClass,
    task: dict[str, Any],
) -> ctk.CTkFrame:
    """Create one current-task preview row."""

    frame = ctk.CTkFrame(
        parent,
        fg_color=theme.TRANSPARENT,
        corner_radius=0,
    )
    frame.grid_columnconfigure(1, weight=1)

    checkbox = ctk.CTkCheckBox(
        frame,
        text="",
        width=18,
        checkbox_width=17,
        checkbox_height=17,
        border_color=theme.CARD_BORDER,
    )
    checkbox.grid(
        row=0,
        column=0,
        padx=(0, 8),
        sticky="w",
    )

    create_small_label(
        frame,
        task["title"],
        muted=False,
    ).grid(
        row=0,
        column=1,
        sticky="w",
    )

    priority = create_small_label(
        frame,
        task["priority"].upper(),
        muted=False,
        bold=True,
    )
    priority.configure(
        text_color=_priority_color(
            task["priority"]
        )
    )
    priority.grid(
        row=0,
        column=2,
        padx=(8, 0),
        sticky="e",
    )

    return frame


def _create_orange_link(
    parent: ctk.CTkBaseClass,
    text: str,
) -> ctk.CTkLabel:
    """Create orange link-style text."""

    label = create_body_label(
        parent,
        text,
        bold=True,
    )
    label.configure(
        text_color=theme.ACCENT_ORANGE,
    )

    return label


def _create_simple_summary_card(
    parent: ctk.CTkBaseClass,
    title: str,
    rows: list[tuple[str, str]],
) -> ctk.CTkFrame:
    """Create a simple label/value summary card."""

    card = create_card(parent)
    card.grid_columnconfigure(0, weight=1)

    _add_card_header(
        card,
        title,
    )

    for index, (label, value) in enumerate(
        rows,
        start=2,
    ):
        row = ctk.CTkFrame(
            card,
            fg_color=theme.TRANSPARENT,
            corner_radius=0,
        )
        row.grid(
            row=index,
            column=0,
            padx=theme.CARD_PADDING_X,
            pady=5,
            sticky="ew",
        )
        row.grid_columnconfigure(0, weight=1)

        create_small_label(
            row,
            label,
            muted=False,
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        create_small_label(
            row,
            value,
            muted=False,
            bold=True,
        ).grid(
            row=0,
            column=1,
            sticky="e",
        )

        make_hoverable(card)

    return card


def _priority_color(
    priority: str,
) -> str:
    """Return the configured task-priority color."""

    return theme.PRIORITY_COLORS.get(
        priority.title(),
        theme.TEXT_MUTED,
    )


def _format_percentage(
    progress: float,
) -> str:
    """Convert a 0–1 progress value into display text."""

    return f"{round(progress * 100)}%"


def _get_log_detail(
    log: dict[str, Any],
) -> tuple[str, str]:
    """Choose the most useful detail from a log entry."""

    if log["solution"]:
        return "Solution", log["solution"]

    if log["problems"]:
        return "Problem", log["problems"]

    if log["next_steps"]:
        return "Next Step", log["next_steps"]

    if log["comments"]:
        return "Comments", log["comments"]

    return (
        "Entry",
        "No additional notes were recorded.",
    )

def _navigate_to(
    widget: ctk.CTkBaseClass,
    page_key: str,
) -> None:
    """
    Ask the main application window to display another page.

    The root application owns page routing, so the Dashboard does not
    need to import main.py or know how pages are constructed.
    """

    application = widget.winfo_toplevel()

    show_page = getattr(
        application,
        "show_page",
        None,
    )

    if callable(show_page):
        show_page(page_key)
    else:
        print(
            f"Unable to navigate to page: {page_key}"
        )

def _open_task(
    widget: ctk.CTkBaseClass,
    task: dict[str, Any],
) -> None:
    """
    Open the Task Board for a selected task.

    The task ID is stored on the root application so the Task Board can
    automatically select it once that page supports task details.
    """

    application = widget.winfo_toplevel()

    application.pending_task_id = task.get(
        "id"
    )

    _navigate_to(
        widget,
        "task_board",
    )