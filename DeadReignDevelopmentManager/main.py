import customtkinter as ctk
from pages.dashboard import show_dashboard
from pages.dev_log import show_development_log
from pages.tasks import show_tasks
from pages.bugs import show_bugs
from pages.ideas import show_ideas
from pages.milestones import show_milestones
from pages.polish_backlog import show_polish_backlog


#------------ Application Settings ---------------#

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


#--- Page Switching Function ---#

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

def show_page(page_name):
    clear_content()

    page_functions = {
        "Dashboard": lambda: show_dashboard(content_frame),
        "Development Log": lambda: show_development_log(content_frame, show_page),
        "Tasks": lambda: show_tasks(content_frame, show_page),
        "Bugs": lambda: show_bugs(content_frame),
        "Ideas": lambda: show_ideas(content_frame),
        "Milestones": lambda: show_milestones(content_frame),
        "Polish Backlog": lambda: show_polish_backlog(content_frame)
    }

    selected_page = page_functions.get(page_name)

    if selected_page:
        selected_page()


# def show_placeholder_page(page_name):
#     page_title = ctk.CTkLabel(
#         content_frame,
#         text=page_name,
#         font=("Arial", 26, "bold")
#     )
#
#     page_title.grid(
#         row=0,
#         column=0,
#         padx=30,
#         pady=(30, 10),
#         sticky="w"
#     )
#     page_description = ctk.CTkLabel(
#         content_frame,
#         text=f"This is the {page_name} page.",
#         font=("Arial", 15)
#     )
#     page_description.grid(
#         row=1,
#         column=0,
#         padx=30,
#         pady=10,
#         sticky="nw"
#     )

# def show_development_log():
#
#     def save_entry():
#         selected_date = date_entry.get().strip()
#         selected_system = system_combo.get().strip()
#         completed_text = work_completed_textbox.get("1.0", "end").strip()
#         problem_text = problems_textbox.get("1.0", "end").strip()
#         solution_text = solution_textbox.get("1.0", "end").strip()
#         next_steps_text = next_steps_textbox.get("1.0", "end").strip()
#         comments_text = comments_textbox.get("1.0", "end").strip()
#
#         if not selected_date:
#             messagebox.showerror(
#                 title="Missing Date",
#                 message="Please enter a date."
#             )
#             return
#
#         if not selected_system:
#             messagebox.showerror(
#                 title="Missing System",
#                 message="Please enter a system or feature."
#             )
#             return
#
#         if not completed_text:
#             messagebox.showerror(
#                 title="Missing Work Description",
#                 message="Describe the work completed."
#             )
#             return
#
#         entry = {
#             "date": selected_date,
#             "system": selected_system,
#             "work_completed": completed_text,
#             "problems": problem_text,
#             "solution": solution_text,
#             "next_steps": next_steps_text,
#             "comments": comments_text,
#             "screenshot_captured": screenshot_var.get(),
#             "video_recorded": video_var.get(),
#             "git_commit_created": git_var.get(),
#             "portfolio_worthy": portfolio_var.get()
#         }
#
#         save_development_entry(entry)
#         save_new_system(selected_system)
#
#         messagebox.showinfo(
#             title="Entry Saved",
#             message="Your dev log entry was saved successfully."
#         )
#
#
#     page_title = ctk.CTkLabel(
#     content_frame,
#     text="Development Log",
#     font=("Arial", 26, "bold")
#     )
#
#     page_title.grid(
#         row=0,
#         column=0,
#         columnspan=2,
#         padx=30,
#         pady=(30, 15),
#         sticky="w"
#     )
#
#     form_frame = ctk.CTkScrollableFrame(
#         content_frame,
#         corner_radius=10
#     )
#
#     form_frame.grid(
#         row=1,
#         column=0,
#         padx=30,
#         pady=(0, 30),
#         sticky="nsew"
#     )
#
#
#
#     date_label = ctk.CTkLabel(
#         form_frame,
#         text="Date"
#     )
#
#     date_label.grid(
#         row=0,
#         column=0,
#         padx=(20, 10),
#         pady=10,
#         sticky="w"
#     )
#
#     date_entry = ctk.CTkEntry(
#         form_frame,
#         width=180
#     )
#
#     date_entry.grid(
#         row=0,
#         column=1,
#         padx=(0, 20,),
#         pady=10,
#         sticky="w"
#     )
#
#     date_entry.insert(0, date.today().strftime("%m/%d/%Y"))
#
#     system_label = ctk.CTkLabel(
#         form_frame,
#         text="System or Feature"
#     )
#
#     system_label.grid(
#         row=1,
#         column=0,
#         padx=(20, 10),
#         pady=10,
#         sticky="w"
#     )
#
#     saved_systems = load_systems()
#
#     system_combo = ctk.CTkComboBox(
#         form_frame,
#         values=saved_systems,
#         width=260
#     )
#
#     system_combo.grid(
#         row=1,
#         column=1,
#         padx=(0, 20),
#         pady=10,
#         sticky="w"
#     )
#
#     system_combo.set("")
#
#     work_completed_label = ctk.CTkLabel(
#         form_frame,
#         text="Work Completed"
#     )
#
#     work_completed_label.grid(
#         row=2,
#         column=0,
#         padx=(20, 10),
#         pady=10,
#         sticky="nw"
#     )
#
#     work_completed_textbox = ctk.CTkTextbox(
#         form_frame,
#         height=100
#     )
#
#     work_completed_textbox.grid(
#         row=2,
#         column=1,
#         padx=(0, 20),
#         pady=10,
#         sticky="ew"
#     )
#
#     problems_label = ctk.CTkLabel(
#         form_frame,
#         text="Problems Encountered"
#     )
#
#     problems_label.grid(
#         row=3,
#         column=0,
#         padx=(20, 10),
#         pady=10,
#         sticky="nw"
#     )
#
#     problems_textbox = ctk.CTkTextbox(
#         form_frame,
#         height=90
#     )
#
#     problems_textbox.grid(
#         row=3,
#         column=1,
#         padx=(0, 20),
#         pady=10,
#         sticky="ew"
#     )
#
#
#
#     solutions_label = ctk.CTkLabel(
#         form_frame,
#         text="Solutions Used"
#     )
#
#     solutions_label.grid(
#         row=4,
#         column=0,
#         padx=(20, 10),
#         pady=10,
#         sticky="nw"
#     )
#
#     solution_textbox = ctk.CTkTextbox(
#         form_frame,
#         height=90
#     )
#
#     solution_textbox.grid(
#         row=4,
#         column=1,
#         padx=(0, 20),
#         pady=10,
#         sticky="ew"
#     )
#
#     next_steps_label = ctk.CTkLabel(
#         form_frame,
#         text="Next Steps"
#     )
#
#     next_steps_label.grid(
#         row=5,
#         column=0,
#         padx=(20, 10),
#         pady=10,
#         sticky="nw"
#     )
#
#     next_steps_textbox = ctk.CTkTextbox(
#         form_frame,
#         height=90
#     )
#
#     next_steps_textbox.grid(
#         row=5,
#         column=1,
#         padx=(0, 20),
#         pady=10,
#         sticky="ew"
#     )
#
#     comments_label = ctk.CTkLabel(
#         form_frame,
#         text="Comments and Notes"
#     )
#
#     comments_label.grid(
#         row=6,
#         column=0,
#         padx=(20, 10),
#         pady=10,
#         sticky="nw"
#     )
#
#     comments_textbox = ctk.CTkTextbox(
#         form_frame,
#         height=100
#     )
#
#     comments_textbox.grid(
#         row=6,
#         column=1,
#         padx=(0, 20),
#         pady=10,
#         sticky="ew"
#     )
#
#     documentation_label = ctk.CTkLabel(
#         form_frame,
#         text="Documentation"
#     )
#
#     documentation_label.grid(
#         row=7,
#         column=0,
#         padx=(20, 10),
#         pady=10,
#         sticky="nw"
#     )
#
#     documentation_frame = ctk.CTkFrame(
#         form_frame,
#         fg_color="transparent"
#     )
#
#     documentation_frame.grid(
#         row=7,
#         column=1,
#         padx=(0, 20),
#         pady=10,
#         sticky="ew"
#     )
#
#     screenshot_var = ctk.BooleanVar()
#     video_var = ctk.BooleanVar()
#     git_var = ctk.BooleanVar()
#     portfolio_var = ctk.BooleanVar()
#
#     screenshot_checkbox = ctk.CTkCheckBox(
#         documentation_frame,
#         text="Screenshot Captured",
#         variable=screenshot_var
#     )
#
#     screenshot_checkbox.grid(
#         row=0,
#         column=0,
#         padx=(0, 20),
#         pady=5,
#         sticky="w"
#     )
#
#     video_checkbox = ctk.CTkCheckBox(
#         documentation_frame,
#         text="Video Recorded",
#         variable=video_var
#     )
#
#     video_checkbox.grid(
#         row=0,
#         column=1,
#         padx=(0, 20),
#         pady=5,
#         sticky="w"
#     )
#
#     git_checkbox = ctk.CTkCheckBox(
#         documentation_frame,
#         text="Git Commit Created",
#         variable=git_var
#     )
#
#     git_checkbox.grid(
#         row=1,
#         column=0,
#         padx=(0, 20),
#         pady=5,
#         sticky="w"
#     )
#
#     portfolio_checkbox = ctk.CTkCheckBox(
#         documentation_frame,
#         text="Portfolio Worthy Milestone",
#         variable=portfolio_var
#     )
#
#     portfolio_checkbox.grid(
#         row=1,
#         column=1,
#         padx=(0, 20),
#         pady=5,
#         sticky="w"
#     )
#
#     save_button = ctk.CTkButton(
#         form_frame,
#         text="Save Development Entry",
#         width=220,
#         height=40,
#         command=save_entry
#     )
#
#     save_button.grid(
#         row=8,
#         column=1,
#         padx=(0, 20),
#         pady=(20, 30),
#         sticky="e"
#     )








    # system_combo = ctk.CTkComboBox(
    #     content_frame,
    #     values=[
    #         "",
    #         "Animations",
    #         "Crafting",
    #         "Inventory",
    #         "UI",
    #         "Weapons",
    #         "Zombie AI"
    #     ],
    #     width=250
    # )
    #
    # system_combo.grid(
    #     row=2,
    #     column=1,
    #     padx=(0, 30),
    #     pady=10,
    #     sticky="w"
    # )
    #
    # system_combo.set("")


    # page_description.configure(
    #     text=f"This is the {page_name} page."
    # )


#--- Main Window -----#

app = ctk.CTk()

app.title("Dead Reign Development Manager")
app.geometry("1200x750")
app.minsize(900, 600)

app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(1, weight=1)


#--- Header Frame ---#

header_frame = ctk.CTkFrame(
    app,
    height=90,
    corner_radius=0
)

header_frame.grid(
    row=0,
    column=0,
    columnspan=2,
    sticky="nsew"
)

title_label = ctk.CTkLabel(
    header_frame,
    text="Dead Reign Development Manager",
    font=("Arial", 28, "bold")
)

title_label.pack(pady=(18,2))

subtitle_label = ctk.CTkLabel(
    header_frame,
    text="Development Logs • Tasks • Bugs • Ideas • Milestones",
    font=("Arial", 14)
)

#--- Navigation Frame ---#

navigation_frame = ctk.CTkFrame(
    app,
    width=220,
    corner_radius=0
)

navigation_frame.grid(
    row=1,
    column=0,
    sticky="nsew"
)

navigation_frame.grid_propagate(False)

navigation_title = ctk.CTkLabel(
    navigation_frame,
    text="Navigation",
    font=("Arial", 13, "bold")
)

navigation_title.pack(
    pady=(25, 15),
    padx=20
)

dashboard_button = ctk.CTkButton(
    navigation_frame,
    text="Dashboard",
    width=180,
    command=lambda: show_page("Dashboard")
)

dashboard_button.pack(pady=6)

dev_log_button = ctk.CTkButton(
    navigation_frame,
    text="Development Log",
    width=180,
    command=lambda: show_page("Development Log")
)

dev_log_button.pack(pady=6)

tasks_button = ctk.CTkButton(
    navigation_frame,
    text="Tasks",
    width=180,
    command=lambda: show_page("Tasks")
)

tasks_button.pack(pady=6)

bugs_button = ctk.CTkButton(
    navigation_frame,
    text="Bugs",
    width=180,
    command=lambda: show_page("Bugs")
)

bugs_button.pack(pady=6)

ideas_button = ctk.CTkButton(
    navigation_frame,
    text="Ideas",
    width=180,
    command=lambda: show_page("Ideas")
)

ideas_button.pack(pady=6)

milestones_button = ctk.CTkButton(
    navigation_frame,
    text="Milestones",
    width=180,
    command=lambda: show_page("Milestones")
)

milestones_button.pack(pady=6)

polish_button = ctk.CTkButton(
    navigation_frame,
    text="Polish",
    width=180,
    command=lambda: show_page("Polish Backlog")
)

polish_button.pack(pady=6)

#--- Main Content Frame ---#

content_frame = ctk.CTkFrame(
    app,
    corner_radius=12
)

content_frame.grid(
    row=1,
    column=1,
    pady=(20),
    padx=(20),
    sticky="nsew"
)

content_frame.grid_rowconfigure(1, weight=1)
content_frame.grid_columnconfigure(0, weight=1)

# page_title = ctk.CTkLabel(
#     content_frame,
#     text="Dashboard",
#     font=("Arial", 26, "bold")
# )
#
# page_title.grid(
#     row=0,
#     column=0,
#     padx=30,
#     pady=(30, 10),
#     sticky="w"
# )
#
# page_description = ctk.CTkLabel(
#     content_frame,
#     text="This is the dashboard page.",
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


#---Title ---#

# title_label = ctk.CTkLabel(
#     app,
#     text="Dead Reign Development Manager",
#     font=("Arial", 28, "bold")
# )
#
# title_label.pack(pady=(25, 5))
#
# subtitle_label = ctk.CTkLabel(
#     app,
#     text="Development logs • Tasks • Bugs • Ideas • Milestones",
#     font=("Arial", 15)
# )
#
# subtitle_label.pack()
#

#--- Start The Application ---#

show_page("Dashboard")


app.mainloop()
