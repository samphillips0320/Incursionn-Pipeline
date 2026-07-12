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

def show_page(page_name, search_text=""):
    clear_content()

    page_functions = {
        "Dashboard": lambda: show_dashboard(content_frame),
        "Development Log": lambda: show_development_log(content_frame, show_page),
        "Tasks": lambda: show_tasks(content_frame, show_page, search_text),
        "Bugs": lambda: show_bugs(content_frame),
        "Ideas": lambda: show_ideas(content_frame),
        "Milestones": lambda: show_milestones(content_frame),
        "Polish Backlog": lambda: show_polish_backlog(content_frame)
    }

    selected_page = page_functions.get(page_name)

    if selected_page:
        selected_page()



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


#--- Start The Application ---#

show_page("Dashboard")


app.mainloop()
