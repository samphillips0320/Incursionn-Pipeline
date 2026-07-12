import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from uuid import uuid4
from storage import (
load_systems,
load_tasks,
save_new_system,
save_new_task,
update_task,
update_task_status
)

def show_tasks(content_frame, refresh_page, search_text=""):
    editing_task_id = None

    def add_task():
        nonlocal editing_task_id
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


        if editing_task_id is None:
            task_data = {
                "id": str(uuid4()),
                "title": task_title,
                "system": selected_system,
                "priority": selected_priority,
                "status": selected_status,
                "notes": task_notes,
                "created_at": datetime.now().strftime("%m-%d-%y %H:%M:%S"),
                "completed_at": None
            }

            save_new_task(task_data)

            messagebox.showinfo(
                title="Task Added",
                message="Your task was added successfully."
            )

        else:
            tasks = load_tasks()

            original_task = next(
                task for task in tasks
                if task["id"] == editing_task_id
            )

            task_data = {
                "id": original_task["id"],
                "title": task_title,
                "system": selected_system,
                "priority": selected_priority,
                "status": selected_status,
                "notes": task_notes,
                "created_at": original_task["created_at"],
                "completed_at": original_task["completed_at"]
            }

            update_task(task_data)

            messagebox.showinfo(
                title="Task Updated",
                message="Your task was updated successfully."
            )

        save_new_system(selected_system)

        refresh_page("Tasks")

    def change_task_status(task_id, current_status):
        if current_status == "Complete":
            new_status = "Not started"
        else:
            new_status = "Complete"

        update_task_status(task_id, new_status)
        refresh_page("Tasks")

    def toggle_task_details(details_frame):
        if details_frame.winfo_viewable():
            details_frame.grid_remove()
        else:
            details_frame.grid()

    def edit_task(task):
        nonlocal editing_task_id
        editing_task_id = task["id"]
        title_entry.delete(0, "end")
        title_entry.insert(0, task["title"])

        system_combo.set(task["system"])
        priority_combo.set(task["priority"])
        status_combo.set(task["status"])

        notes_textbox.delete("1.0", "end")
        notes_textbox.insert("1.0", task["notes"])

        add_button.configure(text="Save Changes")

    def apply_task_filters():
        update_clear_button()

        render_task_list(
            search_entry.get().strip()
        )

    def get_priority_rank(priority):
        priority_ranks = {
            "Critical": 4,
            "High": 3,
            "Medium": 2,
            "Low": 1
        }

        return priority_ranks.get(priority, 0)

    def get_priority_colors(priority):
        priority_colors = {
            "Critical": ("#8B1E1E", "#FFB3B3"),
            "High": ("#8A4B08", "#FFD29B"),
            "Medium": ("#1F4E79", "#B9DAF5"),
            "Low": ("#3F4A52", "#D0D7DC")
        }

        return priority_colors.get(
            priority,
            ("#3F4A52", "#D0D7DC")
        )

    def get_status_colors(status):
        status_colors = {
            "Blocked": ("#7A1F1F", "#FFBABA"),
            "In progress": ("#7A5A00", "#FFE08A"),
            "Complete": ("#1F6B3A", "#B8F0C8"),
            "Not started": ("#41474D", "#D4D8DC")
        }

        return status_colors.get(
            status,
            ("#41474D", "#D4D8DC")
        )

    def clear_filters():
        search_entry.delete(0, "end")

        system_filter_combo.set("All Systems")
        priority_filter_combo.set("All Priorities")
        status_filter_combo.set("All Statuses")
        sort_combo.set("Newest first")

        update_clear_button()
        render_task_list()

    def update_clear_button():
        search_is_active = bool(
            search_entry.get().strip()
        )

        filters_are_active = (
                system_filter_combo.get() != "All Systems"
                or priority_filter_combo.get() != "All Priorities"
                or status_filter_combo.get() != "All Statuses"
                or sort_combo.get() != "Newest first"
        )

        if search_is_active or filters_are_active:
            clear_search_button.place(
                relx=1.0,
                rely=0.5,
                x=-8,
                anchor="e"
            )
        else:
            clear_search_button.place_forget()


    def create_task_card(parent, task, row):
        task_frame = ctk.CTkFrame(
            parent,
            corner_radius=10
        )

        task_frame.grid(
            row=row,
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
                           status=task["status"]: change_task_status(
                task_id,
                status
            )
        )

        complete_checkbox.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(15, 5),
            pady=15,
            sticky="nw"
        )

        title_font = (
            "Arial",
            16,
            "overstrike" if task["status"] == "Complete" else "bold"
        )

        title_row_frame = ctk.CTkFrame(
            task_frame,
            fg_color="transparent"
        )

        title_row_frame.grid(
            row=0,
            column=1,
            padx=(10, 20),
            pady=(15, 10),
            sticky="ew"
        )

        title_row_frame.grid_columnconfigure(0, weight=1)

        task_title_label = ctk.CTkLabel(
            title_row_frame,
            text=task["title"],
            font=title_font,
            wraplength=550,
            justify="left",
            anchor="w",
            cursor="hand2"
        )

        task_title_label.grid(
            row=0,
            column=0,
            padx=(0, 10),
            sticky="ew"
        )

        priority_background, priority_text = get_priority_colors(
            task.get("priority", "")
        )

        priority_chip = ctk.CTkLabel(
            title_row_frame,
            text=task.get("priority", ""),
            width=75,
            height=26,
            corner_radius=8,
            fg_color=priority_background,
            text_color=priority_text,
            font=("Arial", 11, "bold")
        )

        priority_chip.grid(
            row=0,
            column=1,
            padx=(0, 6)
        )

        status_background, status_text = get_status_colors(
            task.get("status", "")
        )

        status_chip = ctk.CTkLabel(
            title_row_frame,
            text=task.get("status", ""),
            width=90,
            height=26,
            corner_radius=8,
            fg_color=status_background,
            text_color=status_text,
            font=("Arial", 11, "bold")
        )

        status_chip.grid(
            row=0,
            column=2
        )

        details_frame = ctk.CTkFrame(
            task_frame,
            fg_color="transparent"
        )

        details_frame.grid(
            row=1,
            column=1,
            padx=(10, 20),
            pady=(0, 15),
            sticky="ew"
        )

        details_text = (
            f'System: {task["system"]}\n'
            f'Created: {task["created_at"]}'
        )

        details_label = ctk.CTkLabel(
            details_frame,
            text=details_text,
            font=("Arial", 12),
            justify="left"
        )

        details_label.grid(
            row=0,
            column=0,
            sticky="w"
        )

        if task["notes"]:
            task_notes_label = ctk.CTkLabel(
                details_frame,
                text=task["notes"],
                font=("Arial", 12),
                wraplength=700,
                justify="left"
            )

            task_notes_label.grid(
                row=1,
                column=0,
                pady=(10, 0),
                sticky="w"
            )

        edit_button = ctk.CTkButton(
            details_frame,
            text="Edit Task",
            width=110,
            command=lambda selected_task=task: edit_task(
                selected_task
            )
        )

        edit_button.grid(
            row=2,
            column=0,
            pady=(15, 0),
            sticky="w"
        )

        task_title_label.bind(
            "<Button-1>",
            lambda event,
                   frame=details_frame: toggle_task_details(frame)
        )

        details_frame.grid_remove()

    def render_task_list(search_text=""):
        for widget in task_list_frame.winfo_children():
            widget.destroy()

        tasks = load_tasks()

        normalized_search = search_text.lower()

        selected_system = system_filter_combo.get()
        selected_priority = priority_filter_combo.get()
        selected_status = status_filter_combo.get()

        filtered_tasks = []

        for task in tasks:
            task_title = task.get("title", "")
            task_notes = task.get("notes", "")
            task_system = task.get("system", "")
            task_priority = task.get("priority", "")
            task_status = task.get("status", "")

            matches_search = (
                    not normalized_search
                    or normalized_search in task_title.lower()
                    or normalized_search in task_notes.lower()
            )

            matches_system = (
                    selected_system == "All Systems"
                    or task_system == selected_system
            )

            matches_priority = (
                    selected_priority == "All Priorities"
                    or task_priority == selected_priority
            )

            matches_status = (
                    selected_status == "All Statuses"
                    or task_status == selected_status
            )

            if (
                    matches_search
                    and matches_system
                    and matches_priority
                    and matches_status
            ):
                filtered_tasks.append(task)

        tasks = filtered_tasks

        selected_sort = sort_combo.get()

        def is_complete(task):
            return task.get("status", "") == "Complete"

        if selected_sort == "Newest first":
            tasks.sort(
                key=lambda task: (
                    is_complete(task),
                    -datetime.strptime(
                        task["created_at"],
                        "%m-%d-%y %H:%M:%S"
                    ).timestamp()
                )
            )

        elif selected_sort == "Oldest first":
            tasks.sort(
                key=lambda task: (
                    is_complete(task),
                    datetime.strptime(
                        task["created_at"],
                        "%m-%d-%y %H:%M:%S"
                    ).timestamp()
                )
            )

        elif selected_sort == "Priority: highest first":
            tasks.sort(
                key=lambda task: (
                    is_complete(task),
                    -get_priority_rank(
                        task.get("priority", "")
                    )
                )
            )

        elif selected_sort == "Priority: lowest first":
            tasks.sort(
                key=lambda task: (
                    is_complete(task),
                    get_priority_rank(
                        task.get("priority", "")
                    )
                )
            )

        elif selected_sort == "Status":
            status_order = {
                "Blocked": 0,
                "In progress": 1,
                "Not started": 2,
                "Complete": 3
            }

            tasks.sort(
                key=lambda task: (
                    is_complete(task),
                    status_order.get(
                        task.get("status", ""),
                        99
                    )
                )
            )

        elif selected_sort == "System":
            tasks.sort(
                key=lambda task: (
                    is_complete(task),
                    task.get("system", "").lower()
                )
            )

        elif selected_sort == "Title: A-Z":
            tasks.sort(
                key=lambda task: (
                    is_complete(task),
                    task.get("title", "").lower()
                )
            )

        if not tasks:
            active_filters = []

            if search_text:
                active_filters.append(f'Search: "{search_text}"')

            if selected_system != "All Systems":
                active_filters.append(f"System: {selected_system}")

            if selected_priority != "All Priorities":
                active_filters.append(f"Priority: {selected_priority}")

            if selected_status != "All Statuses":
                active_filters.append(f"Status: {selected_status}")

            if active_filters:
                empty_message = (
                        "No tasks match the selected filters:\n"
                        + " | ".join(active_filters)
                )
            else:
                empty_message = (
                    "No tasks yet. The void is peaceful, but suspicious."
                )

            empty_label = ctk.CTkLabel(
                task_list_frame,
                text=empty_message,
                font=("Arial", 14),
                justify="left"
            )

            empty_label.grid(
                row=0,
                column=0,
                padx=15,
                pady=20,
                sticky="w"
            )

            return

        for index, task in enumerate(tasks):
            create_task_card(
                task_list_frame,
                task,
                index
            )


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
        values=["Not started", "In progress", "Blocked", "Complete"],
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

    search_frame = ctk.CTkFrame(
        page_frame,
        fg_color="transparent"
    )

    search_frame.grid(
        row=2,
        column=0,
        padx=10,
        pady=(0, 10),
        sticky="ew"
    )

    search_frame.grid_columnconfigure(0, weight=1)

    search_box_frame = ctk.CTkFrame(
        search_frame,
        fg_color="transparent"
    )

    search_box_frame.grid(
        row=0,
        column=0,
        padx=(5, 10),
        sticky="ew"
    )

    search_box_frame.grid_columnconfigure(0, weight=1)

    search_entry = ctk.CTkEntry(
        search_box_frame,
        placeholder_text="Search task titles and notes..."
    )

    search_entry.grid(
        row=0,
        column=0,
        sticky="ew"
    )

    clear_search_button = ctk.CTkButton(
        search_box_frame,
        text="×",
        width=28,
        height=24,
        corner_radius=6,
        fg_color="transparent",
        hover_color=("gray80", "gray30"),
        command=clear_filters
    )

    search_entry.insert(0, search_text)

    search_entry.bind(
        "<Return>",
        lambda event: apply_task_filters()
    )

    search_entry.bind(
        "<KeyRelease>",
        lambda event: apply_task_filters()
    )

    search_button = ctk.CTkButton(
        search_frame,
        text="Search",
        width=100,
        command=apply_task_filters
    )

    search_button.grid(
        row=0,
        column=1,
        padx=(0, 5)
    )


    filter_frame = ctk.CTkFrame(
        page_frame,
        fg_color="transparent"
    )

    filter_frame.grid(
        row=3,
        column=0,
        padx=15,
        pady=(0, 10),
        sticky="ew"
    )

    filter_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    system_filter_values = [
        "All Systems",
        *load_systems()
    ]

    system_filter_combo = ctk.CTkComboBox(
        filter_frame,
        values=system_filter_values,
        state="readonly",
        command=lambda selected_value: apply_task_filters()
    )

    system_filter_combo.grid(
        row=0,
        column=0,
        padx=(0, 5),
        sticky="ew"
    )

    system_filter_combo.set("All Systems")

    priority_filter_combo = ctk.CTkComboBox(
        filter_frame,
        values=[
            "All Priorities",
            "Low",
            "Medium",
            "High",
            "Critical"
        ],
        state="readonly",
        command=lambda selected_value: apply_task_filters()
    )

    priority_filter_combo.grid(
        row=0,
        column=1,
        padx=5,
        sticky="ew"
    )

    priority_filter_combo.set("All Priorities")

    status_filter_combo = ctk.CTkComboBox(
        filter_frame,
        values=[
            "All Statuses",
            "Not started",
            "In progress",
            "Blocked",
            "Complete"
        ],
        state="readonly",
        command=lambda selected_value: apply_task_filters()
    )

    status_filter_combo.grid(
        row=0,
        column=2,
        padx=5,
        sticky="ew"
    )

    status_filter_combo.set("All Statuses")

    sort_combo = ctk.CTkComboBox(
        filter_frame,
        values=[
            "Newest first",
            "Oldest first",
            "Priority: highest first",
            "Priority: lowest first",
            "Status",
            "System",
            "Title: A-Z"
        ],
        state="readonly",
        command=lambda selected_value: apply_task_filters()
    )

    sort_combo.grid(
        row=0,
        column=3,
        padx=(5, 0),
        sticky="ew"
    )

    sort_combo.set("Newest first")

    task_list_frame = ctk.CTkFrame(
        page_frame,
        fg_color="transparent"
    )

    task_list_frame.grid(
        row=4,
        column=0,
        padx=0,
        pady=(0, 10),
        sticky="ew"
    )

    task_list_frame.grid_columnconfigure(0, weight=1)

    update_clear_button()

    render_task_list(search_text)













