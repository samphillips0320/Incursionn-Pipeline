import customtkinter as ctk
from storage import (
load_development_entries,
load_tasks
)


def show_dashboard(content_frame):
    tasks = load_tasks()
    development_entries = load_development_entries()

    open_tasks = 0
    completed_tasks = 0

    for task in tasks:
        if task["status"] == "Complete":
            completed_tasks += 1
        else:
            open_tasks += 1


    page_title = ctk.CTkLabel(
        content_frame,
        text="Dashboard",
        font=("Arial", 26, "bold")
    )

    page_title.grid(
        row=0,
        column=0,
        padx=30,
        pady=(30, 20),
        sticky="w"
    )

    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)
    content_frame.grid_columnconfigure(2, weight=1)

    create_summary_card(
        content_frame,
        row=1,
        column=0,
        title="Open Tasks",
        value=open_tasks
    )

    create_summary_card(
        content_frame,
        row=1,
        column=1,
        title="Completed Tasks",
        value=completed_tasks
    )

    create_summary_card(
        content_frame,
        row=1,
        column=2,
        title="Development Entries",
        value=len(development_entries)
    )

    recent_activity_title = ctk.CTkLabel(
        content_frame,
        text="Latest Development Entry",
        font=("Arial", 20, "bold")
    )

    recent_activity_title.grid(
        row=2,
        column=0,
        columnspan=3,
        padx=30,
        pady=(35, 10),
        sticky="w"
    )

    if development_entries:
        latest_entry = development_entries[-1]

        latest_entry_frame = ctk.CTkFrame(
            content_frame,
            corner_radius=10
        )

        latest_entry_frame.grid(
            row=3,
            column=0,
            columnspan=3,
            padx=30,
            pady=(0, 30),
            sticky="ew"
        )

        entry_system = ctk.CTkLabel(
            latest_entry_frame,
            text=latest_entry["date"],
            font=("Arial", 12)
        )

        entry_system.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 10),
            sticky="w"
        )

        entry_description = ctk.CTkLabel(
            latest_entry_frame,
            text=latest_entry["work_completed"],
            font=("Arial", 13),
            wraplength=750,
            justify="left"
        )

        entry_description.grid(
            row=2,
            column=0,
            padx=20,
            pady=(0, 18),
            sticky="w"
        )

    else:
        empty_label = ctk.CTkLabel(
            content_frame,
            text="No development entries have been recorded yet.",
            font=("Arial", 14)
        )

        empty_label.grid(
            row=3,
            column=0,
            columnspan=3,
            padx=30,
            pady=20,
            sticky="w"
        )


def create_summary_card(parent, row, column, title, value):
    card = ctk.CTkFrame(
        parent,
        corner_radius=10
    )

    card.grid(
        row=row,
        column=column,
        padx=10,
        pady=10,
        sticky="nsew"
    )

    card_title = ctk.CTkLabel(
        card,
        text=title,
        font=("Arial", 14)
    )

    card_title.pack(
        padx=25,
        pady=(20, 5)
    )

    card_value = ctk.CTkLabel(
        card,
        text=str(value),
        font=("Arial", 30, "bold")
    )

    card_value.pack(
        padx=25,
        pady=(0, 20)
    )















    # page_description = ctk.CTkLabel(
    #     content_frame,
    #     text="Project activity and progress will appear here.",
    #     font=("Arial", 15)
    # )
    #
    # page_description.grid(
    #     row=1,
    #     column=0,
    #     padx=30,
    #     pady=10,
    #     sticky="nw"
    # )

