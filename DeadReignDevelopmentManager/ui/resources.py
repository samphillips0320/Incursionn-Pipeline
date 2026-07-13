# UI/resources.py

from __future__ import annotations

from pathlib import Path

import customtkinter as ctk
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESOURCE_ROOT = PROJECT_ROOT / "resources"

LOGO_DIRECTORY = RESOURCE_ROOT / "logos"
ICON_DIRECTORY = RESOURCE_ROOT / "icons"
IMAGE_DIRECTORY = RESOURCE_ROOT / "images"


class ImageManager:
    """
    Central image loader for DR Pipeline Management.

    Loaded CTkImage objects are cached so the same image does not need
    to be opened repeatedly across different pages and components.
    """

    _image_cache: dict[tuple[str, int, int], ctk.CTkImage] = {}

    @classmethod
    def load_image(
        cls,
        file_path: Path,
        *,
        width: int,
        height: int,
    ) -> ctk.CTkImage | None:
        """
        Load and cache an image.

        Returns None when the requested file cannot be found or opened.
        """
        resolved_path = file_path.resolve()
        cache_key = (
            str(resolved_path),
            width,
            height,
        )

        if cache_key in cls._image_cache:
            return cls._image_cache[cache_key]

        if not resolved_path.exists():
            print(f"Image file not found: {resolved_path}")
            return None

        try:
            source_image = Image.open(resolved_path)

            ctk_image = ctk.CTkImage(
                light_image=source_image,
                dark_image=source_image,
                size=(width, height),
            )

            cls._image_cache[cache_key] = ctk_image

            return ctk_image

        except (OSError, ValueError) as error:
            print(
                f"Unable to load image '{resolved_path}': {error}"
            )
            return None

    @classmethod
    def load_logo(
        cls,
        filename: str,
        *,
        width: int,
        height: int,
    ) -> ctk.CTkImage | None:
        """Load an image from the resources/logos directory."""
        return cls.load_image(
            LOGO_DIRECTORY / filename,
            width=width,
            height=height,
        )

    @classmethod
    def load_icon(
        cls,
        filename: str,
        *,
        width: int,
        height: int,
    ) -> ctk.CTkImage | None:
        """Load an image from the resources/icons directory."""
        return cls.load_image(
            ICON_DIRECTORY / filename,
            width=width,
            height=height,
        )

    @classmethod
    def load_content_image(
        cls,
        filename: str,
        *,
        width: int,
        height: int,
    ) -> ctk.CTkImage | None:
        """Load an image from the resources/images directory."""
        return cls.load_image(
            IMAGE_DIRECTORY / filename,
            width=width,
            height=height,
        )