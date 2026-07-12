import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from uuid import uuid4
from storage import (
load_systems,
load_tasks,
save_new_system,
save_new_task,
update_task_status
)

def show_tasks(content_frame, refresh_page):

    def add_task():
        task_title = title_entry.get().strip()
        selected_system = system_combo.get().strip()
        selected_priority = priority_combo.get().strip()
        selected_status = status_combo.get().strip()
        task_notes = notes_textbox.get("1.0", "end").strip()

        if not task_title:
            messagebox.showerror(
                title="Missing Title",
                message="Please enter a task title."
            )
            return

        new_task = {
            "id": str(uuid4()),
            "title": task_title,
            "system": selected_system,
            "priority": selected_priority,
            "status": selected_status,
            "notes": task_notes,
            "created_at": datetime.now().strftime("%m-%d-%y %H:%M:%S"),
            "completed_at": None
        }

        save_new_task(new_task)
        save_new_system(selected_system)

        messagebox.showinfo(
            title="Task Added",
            message="Your task was added successfully."
        )

        refresh_page("Tasks")

    def change_task_status(task_id, current_status):
        if current_status == "Complete":
            new_status = "Not started"
        else:
            new_status = "Complete"

        update_task_status(task_id, new_status)
        refresh_page("Tasks")

    page_title = ctk.CTkLabel(
        content_frame,
        text="Tasks",
        font=("Arial", 26, "bold")
    )

    page_title.grid(
        row=0,
        column=0,
        padx=30,
        pady=(30, 15),
        sticky="w"
    )

    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_rowconfigure(1, weight=1)

    page_frame = ctk.CTkScrollableFrame(
        content_frame,
        corner_radius=10
    )

    page_frame.grid(
        row=1,
        column=0,
        padx=30,
        pady=(0, 30),
        sticky="nsew"
    )

    page_frame.grid_columnconfigure(0, weight=1)

    add_task_frame = ctk.CTkFrame(
        page_frame,
        corner_radius=10
    )

    add_task_frame.grid(
        row=0,
        column=0,
        padx=10,
        pady=10,
        sticky="ew"
    )

    add_task_frame.grid_columnconfigure(1, weight=1)

    form_title = ctk.CTkLabel(
        add_task_frame,
        text="Add New Task",
        font=("Arial", 20, "bold")
    )

    form_title.grid(
        row=0,
        column=0,
        columnspan=2,
        padx=20,
        pady=(20, 15),
        sticky="w"
    )

    title_label = ctk.CTkLabel(
        add_task_frame,
        text="Task Title:"
    )

    title_label.grid(
        row=1,
        column=0,
        padx=(20, 10),
        pady=10,
        sticky="w"
    )

    title_entry = ctk.CTkEntry(
        add_task_frame,
        placeholder_text="Example: Add weapon recoil"
    )

    title_entry.grid(
        row=1,
        column=1,
        padx=(0, 20),
        pady=10,
        sticky="ew"
    )

    system_label = ctk.CTkLabel(
        add_task_frame,
        text="System:"
    )

    system_label.grid(
        row=2,
        column=0,
        padx=(20, 10),
        pady=10,
        sticky="w"
    )

    system_combo = ctk.CTkComboBox(
        add_task_frame,
        values=load_systems(),
        width=250
    )

    system_combo.grid(
        row=2,
        column=1,
        padx=(0, 20),
        pady=10,
        sticky="w"
    )

    system_combo.set("")

    priority_label = ctk.CTkLabel(
        add_task_frame,
        text="Priority:"
    )

    priority_label.grid(
        row=3,
        column=0,
        padx=(20, 10),
        pady=10,
        sticky="w"
    )

    priority_combo = ctk.CTkComboBox(
        add_task_frame,
        values=["Low", "Medium", "High", "Critical"],
        width=280,
        state="readonly"
    )

    priority_combo.grid(
        row=3,
        column=1,
        padx=(0, 20),
        pady=10,
        sticky="w"
    )

    priority_combo.set("Medium")

    status_label = ctk.CTkLabel(
        add_task_frame,
        text="Status:"
    )

    status_label.grid(
        row=4,
        column=0,
        padx=(20, 10),
        pady=10,
        sticky="w"
    )

    status_combo = ctk.CTkComboBox(
        add_task_frame,
        values=["Not started", "In progress", "Clocked", "Complete"],
        width=180,
        state="readonly"
    )

    status_combo.grid(
        row=4,
        column=1,
        padx=(0, 20),
        pady=10,
        sticky="w"
    )

    status_combo.set("Not started")

    notes_label = ctk.CTkLabel(
        add_task_frame,
        text="Notes:"
    )

    notes_label.grid(
        row=5,
        column=0,
        padx=(20, 10),
        pady=10,
        sticky="nw"
    )

    notes_textbox = ctk.CTkTextbox(
        add_task_frame,
        height=90
    )

    notes_textbox.grid(
        row=5,
        column=1,
        padx=(0, 20),
        pady=10,
        sticky="ew"
    )

    add_button = ctk.CTkButton(
        add_task_frame,
        text="Add Task",
        width=160,
        height=38,
        command=add_task
    )

    add_button.grid(
        row=6,
        column=1,
        padx=(0, 20),
        pady=(10, 20),
        sticky="e"
    )

    task_list_title = ctk.CTkLabel(
        page_frame,
        text="Task List",
        font=("Arial", 20, "bold")
    )

    task_list_title.grid(
        row=1,
        column=0,
        padx=15,
        pady=(25, 10),
        sticky="w"
    )

    tasks = load_tasks()

    if not tasks:
        empty_label = ctk.CTkLabel(
            page_frame,
            text="No tasks yet. The void is peaceful, but suspicious,",
            font=("Arial", 14)
        )

        empty_label.grid(
            row=2,
            column=0,
            padx=15,
            pady=20,
            sticky="w"
        )

        return

    for index, task in enumerate(tasks, start=2):
        task_frame = ctk.CTkFrame(
            page_frame,
            corner_radius=10
        )

        task_frame.grid(
            row=index,
            column=0,
            padx=10,
            pady=7,
            sticky="ew"
        )

        task_frame.grid_columnconfigure(1, weight=1)

        complete_var = ctk.BooleanVar(
            value=task["status"] == "Complete"
            )

        complete_checkbox = ctk.CTkCheckBox(
            task_frame,
            text="",
            width=30,
            variable=complete_var,
            command=lambda task_id=task["id"],
            status=task["status"]: change_task_status(task_id, status)

        )

        complete_checkbox.grid(
            row=0,
            column=0,
            rowspan=3,
            padx=(15, 5),
            pady=15,
            sticky="n"
        )

        title_font = (
            "Arial", 16, "overstrike" if task["status"] == "Complete" else "bold"
        )

        task_title_label = ctk.CTkLabel(
            task_frame,
            text=task["title"],
            font=title_font
        )

        task_title_label.grid(
            row=0,
            column=1,
            padx=10,
            pady=(12, 2),
            sticky="w"
        )

        details_text = (
            f'System: {task["system"]} '
            f'Priority: {task["priority"]} '
            f'Status: {task["status"]}'
        )

        details_label = ctk.CTkLabel(
            task_frame,
            text=details_text,
            font=("Arial", 12)
        )

        details_label.grid(
            row=1,
            column=1,
            padx=10,
            pady=2,
            sticky="w"
        )

        if task["notes"]:
            notes_label = ctk.CTkLabel(
                task_frame,
                text=task["notes"],
                font=("Arial", 12),
                wraplength=650,
                justify="left"
            )

            notes_label.grid(
                row=2,
                column=1,
                padx=10,
                pady=(2, 12),
                sticky="w"
            )








