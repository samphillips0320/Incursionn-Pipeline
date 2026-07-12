import customtkinter as ctk


def show_bugs(content_frame):
    page_title = ctk.CTkLabel(
        content_frame,
        text="Bugs",
        font=("Arial", 26, "bold")
    )

    page_title.grid(
        row=0,
        column=0,
        padx=30,
        pady=(30, 10),
        sticky="w"
    )

    page_description = ctk.CTkLabel(
        content_frame,
        text="Bug reports and resolutions will appear here.",
        font=("Arial", 15)
    )

    page_description.grid(
        row=1,
        column=0,
        padx=30,
        pady=10,
        sticky="nw"
    )