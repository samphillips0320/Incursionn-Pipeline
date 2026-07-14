from __future__ import annotations

from collections.abc import Callable

import customtkinter as ctk

from pages.analytics import show_analytics
from pages.assets import show_assets
from pages.dashboard import show_dashboard
from pages.dev_log import show_development_log
from pages.knowledge_base import show_knowledge_base
from pages.release_checklist import show_release_checklist
from pages.roadmap import show_roadmap
from pages.settings import show_settings
from pages.systems import show_systems
from pages.task_board import show_task_board
from ui import theme
from ui.header import AppHeader
from ui.sidebar import Sidebar


class DRPipelineApp(ctk.CTk):
    """
    Main application window for DR Pipeline Management.

    Responsibilities:
        - Create the persistent application shell
        - Own the header and sidebar
        - Route navigation to the correct page
        - Replace the active page safely
        - Handle temporary application-wide controls
    """

    def __init__(self) -> None:
        super().__init__()

        self.title("DR Pipeline Management")
        self.geometry("1500x900")
        self.minsize(1280, 760)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configure(
            fg_color=theme.APP_BG,
        )

        self.current_page_key = "dashboard"
        self.current_page = None

        self.page_routes: dict[str, Callable] = {
            "dashboard": show_dashboard,
            "task_board": show_task_board,
            "roadmap": show_roadmap,
            "development_log": show_development_log,
            "systems": show_systems,
            "knowledge_base": show_knowledge_base,
            "assets": show_assets,
            "analytics": show_analytics,
            "release_checklist": show_release_checklist,
            "settings": show_settings,
        }

        self._configure_root_grid()
        self._build_sidebar()
        self._build_main_area()
        self._build_header()
        self._build_page_container()

        self.show_page(self.current_page_key)

    # =====================================================
    # ROOT LAYOUT
    # =====================================================

    def _configure_root_grid(self) -> None:
        """Configure the main application rows and columns."""
        self.grid_columnconfigure(
            0,
            weight=0,
            minsize=theme.SIDEBAR_WIDTH,
        )
        self.grid_columnconfigure(
            1,
            weight=1,
        )
        self.grid_rowconfigure(
            0,
            weight=1,
        )

    def _build_sidebar(self) -> None:
        """Create the persistent left navigation sidebar."""
        self.sidebar = Sidebar(
            self,
            on_navigate=self.show_page,
            initial_page=self.current_page_key,
        )
        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

    def _build_main_area(self) -> None:
        """Create the area containing the header and active page."""
        self.main_area = ctk.CTkFrame(
            self,
            fg_color=theme.APP_BG,
            corner_radius=0,
        )
        self.main_area.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        self.main_area.grid_columnconfigure(
            0,
            weight=1,
        )
        self.main_area.grid_rowconfigure(
            1,
            weight=1,
        )

    def _build_header(self) -> None:
        """Create the persistent application header."""
        self.header = AppHeader(
            self.main_area,
            on_global_search=self.handle_global_search,
            on_notifications=self.handle_notifications,
            on_profile=self.handle_profile,
        )
        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        separator = ctk.CTkFrame(
            self.main_area,
            height=1,
            fg_color=theme.CARD_BORDER,
            corner_radius=0,
        )
        separator.grid(
            row=0,
            column=0,
            pady=(theme.HEADER_HEIGHT - 1, 0),
            sticky="sew",
        )

    def _build_page_container(self) -> None:
        """Create the container where routed pages are displayed."""
        self.page_container = ctk.CTkFrame(
            self.main_area,
            fg_color=theme.APP_BG,
            corner_radius=0,
        )
        self.page_container.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        self.page_container.grid_columnconfigure(
            0,
            weight=1,
        )
        self.page_container.grid_rowconfigure(
            0,
            weight=1,
        )

    # =====================================================
    # PAGE ROUTING
    # =====================================================

    def show_page(self, page_key: str) -> None:
        """
        Display the requested page.

        The previous page is destroyed before the new page is created.
        This keeps the widget tree clean and avoids overlapping pages.
        """
        page_builder = self.page_routes.get(page_key)

        if page_builder is None:
            print(f"Unknown page route: {page_key}")
            return

        if self.current_page is not None:
            self.current_page.destroy()
            self.current_page = None

        self.current_page_key = page_key
        self.sidebar.set_active(page_key)
        self.header.clear_search()

        self.current_page = page_builder(
            self.page_container,
        )

    # =====================================================
    # HEADER ACTIONS
    # =====================================================

    def handle_global_search(self, query: str) -> None:
        """
        Handle global search submissions.

        This is temporary shell behavior. A full cross-project search
        system will replace it later.
        """
        if not query:
            return

        print(
            f"Global search requested for: {query}"
        )

    def handle_notifications(self) -> None:
        """Temporary notification-button behavior."""
        print(
            "Notifications opened."
        )

    def handle_profile(self) -> None:
        """Temporary profile-button behavior."""
        print(
            "Profile opened."
        )


if __name__ == "__main__":
    app = DRPipelineApp()
    app.mainloop()
