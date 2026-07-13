# UI/charts.py

from __future__ import annotations

from collections.abc import Sequence

import customtkinter as ctk

from ui import theme


class CircularProgressRing(ctk.CTkCanvas):
    """Responsive circular progress indicator."""

    def __init__(
        self,
        parent,
        *,
        progress: float = 0.0,
        size: int = 130,
        thickness: int = 12,
        progress_color: str | None = None,
        track_color: str | None = None,
        label: str = "Complete",
    ) -> None:
        super().__init__(
            parent,
            width=size,
            height=size,
            bg=theme.CARD_BG,
            highlightthickness=0,
        )

        self.progress = self._clamp(progress)
        self.size = size
        self.thickness = thickness
        self.progress_color = (
            progress_color or theme.ACCENT_ORANGE
        )
        self.track_color = (
            track_color or theme.INPUT_BG
        )
        self.label = label

        self.bind(
            "<Configure>",
            self._handle_resize,
        )

        self.after_idle(self._draw)

    def set_progress(
        self,
        progress: float,
    ) -> None:
        """Update the displayed progress."""
        self.progress = self._clamp(progress)
        self._draw()

    def _handle_resize(self, _event=None) -> None:
        """Redraw the ring when its canvas changes size."""
        self._draw()

    def _draw(self) -> None:
        """Draw the circular track, progress arc, and labels."""
        self.delete("all")

        width = max(self.winfo_width(), 2)
        height = max(self.winfo_height(), 2)

        diameter = min(width, height)
        padding = self.thickness + 4

        left = (width - diameter) / 2 + padding
        top = (height - diameter) / 2 + padding
        right = (width + diameter) / 2 - padding
        bottom = (height + diameter) / 2 - padding

        self.create_oval(
            left,
            top,
            right,
            bottom,
            outline=self.track_color,
            width=self.thickness,
        )

        extent = -(self.progress * 360)

        self.create_arc(
            left,
            top,
            right,
            bottom,
            start=90,
            extent=extent,
            style="arc",
            outline=self.progress_color,
            width=self.thickness,
        )

        percentage = f"{round(self.progress * 100)}%"

        self.create_text(
            width / 2,
            height / 2 - 8,
            text=percentage,
            fill=theme.TEXT_PRIMARY,
            font=(theme.FONT_FAMILY, 23, "bold"),
        )

        self.create_text(
            width / 2,
            height / 2 + 17,
            text=self.label,
            fill=theme.TEXT_MUTED,
            font=theme.FONT_SMALL,
        )

    @staticmethod
    def _clamp(value: float) -> float:
        """Keep progress between zero and one."""
        return max(0.0, min(float(value), 1.0))


class LineChart(ctk.CTkCanvas):
    """Small responsive line chart for Dashboard metrics."""

    def __init__(
        self,
        parent,
        *,
        values: Sequence[float],
        labels: Sequence[str] | None = None,
        line_color: str | None = None,
        fill_color: str | None = None,
        height: int = 125,
    ) -> None:
        super().__init__(
            parent,
            height=height,
            bg=theme.INPUT_BG,
            highlightthickness=0,
        )

        self.values = list(values)
        self.labels = list(labels or [])
        self.line_color = (
            line_color or theme.ACCENT_ORANGE
        )
        self.fill_color = (
            fill_color or theme.ACCENT_ORANGE_DARK
        )

        self.bind(
            "<Configure>",
            self._handle_resize,
        )

        self.after_idle(self._draw)

    def set_data(
        self,
        values: Sequence[float],
        labels: Sequence[str] | None = None,
    ) -> None:
        """Replace the chart data and redraw it."""
        self.values = list(values)
        self.labels = list(labels or [])
        self._draw()

    def _handle_resize(self, _event=None) -> None:
        """Redraw when the chart changes size."""
        self._draw()

    def _draw(self) -> None:
        """Render grid lines, area fill, line, and data points."""
        self.delete("all")

        width = max(self.winfo_width(), 10)
        height = max(self.winfo_height(), 10)

        left_padding = 12
        right_padding = 12
        top_padding = 12
        bottom_padding = 23

        chart_width = width - left_padding - right_padding
        chart_height = height - top_padding - bottom_padding

        if chart_width <= 0 or chart_height <= 0:
            return

        for grid_index in range(4):
            y = (
                top_padding
                + chart_height * grid_index / 3
            )

            self.create_line(
                left_padding,
                y,
                width - right_padding,
                y,
                fill=theme.CARD_BORDER,
                dash=(2, 4),
            )

        if not self.values:
            self.create_text(
                width / 2,
                height / 2,
                text="No trend data yet",
                fill=theme.TEXT_MUTED,
                font=theme.FONT_SMALL,
            )
            return

        maximum = max(self.values)

        if maximum <= 0:
            maximum = 1

        point_count = len(self.values)

        if point_count == 1:
            x_positions = [width / 2]
        else:
            x_positions = [
                left_padding
                + chart_width * index / (point_count - 1)
                for index in range(point_count)
            ]

        points: list[tuple[float, float]] = []

        for x, value in zip(
            x_positions,
            self.values,
        ):
            normalized_value = value / maximum

            y = (
                top_padding
                + chart_height
                - normalized_value * chart_height
            )

            points.append((x, y))

        if len(points) > 1:
            fill_coordinates = [
                points[0][0],
                top_padding + chart_height,
            ]

            for point in points:
                fill_coordinates.extend(point)

            fill_coordinates.extend(
                [
                    points[-1][0],
                    top_padding + chart_height,
                ]
            )

            self.create_polygon(
                fill_coordinates,
                fill=self.fill_color,
                outline="",
                stipple="gray25",
            )

            flattened_points = [
                coordinate
                for point in points
                for coordinate in point
            ]

            self.create_line(
                flattened_points,
                fill=self.line_color,
                width=2,
                smooth=True,
            )

        for x, y in points:
            radius = 3

            self.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=self.line_color,
                outline="",
            )

        self._draw_axis_labels(
            width=width,
            height=height,
            left_padding=left_padding,
            right_padding=right_padding,
        )

    def _draw_axis_labels(
        self,
        *,
        width: int,
        height: int,
        left_padding: int,
        right_padding: int,
    ) -> None:
        """Draw a small selection of date labels."""
        if not self.labels:
            return

        available_indices = [
            0,
            len(self.labels) // 2,
            len(self.labels) - 1,
        ]

        unique_indices = list(
            dict.fromkeys(available_indices)
        )

        chart_width = width - left_padding - right_padding

        for index in unique_indices:
            if len(self.labels) == 1:
                x = width / 2
            else:
                x = (
                    left_padding
                    + chart_width * index
                    / (len(self.labels) - 1)
                )

            self.create_text(
                x,
                height - 9,
                text=self.labels[index],
                fill=theme.TEXT_MUTED,
                font=(theme.FONT_FAMILY, 9),
            )