import reflex as rx

from college_erp.components.layouts import dashboard_layout


@rx.page(route="/admin/dashboard", title="Admin Dashboard")
def admin_dashboard() -> rx.Component:
    return dashboard_layout(
        rx.vstack(
            rx.heading("Admin Dashboard", size="lg"),
            rx.text("High-level overview of college operations."),
            rx.grid(
                rx.box(
                    rx.heading("Users", size="md"),
                    rx.text("Summary of students and faculty will appear here."),
                    padding="1rem",
                    border_radius="md",
                    background_color="white",
                    box_shadow="sm",
                ),
                rx.box(
                    rx.heading("Attendance", size="md"),
                    rx.text("Global attendance trends will appear here."),
                    padding="1rem",
                    border_radius="md",
                    background_color="white",
                    box_shadow="sm",
                ),
                rx.box(
                    rx.heading("Results", size="md"),
                    rx.text("Recent result statistics will appear here."),
                    padding="1rem",
                    border_radius="md",
                    background_color="white",
                    box_shadow="sm",
                ),
                rx.box(
                    rx.heading("Notices & Timetable", size="md"),
                    rx.text("Administrative notices and timetable overview."),
                    padding="1rem",
                    border_radius="md",
                    background_color="white",
                    box_shadow="sm",
                ),
                template_columns="repeat(2, minmax(0, 1fr))",
                gap="1.5rem",
            ),
            spacing="1.5rem",
            align_items="stretch",
        )
    )

