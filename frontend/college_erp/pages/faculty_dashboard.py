import reflex as rx

from college_erp.components.layouts import dashboard_layout


@rx.page(route="/faculty/dashboard", title="Faculty Dashboard")
def faculty_dashboard() -> rx.Component:
    return dashboard_layout(
        rx.vstack(
            rx.heading("Faculty Dashboard", size="lg"),
            rx.text("Manage attendance, assignments, results, and timetable."),
            rx.grid(
                rx.box(
                    rx.heading("Today’s Classes", size="md"),
                    rx.text("Your schedule for today will appear here."),
                    padding="1rem",
                    border_radius="md",
                    background_color="white",
                    box_shadow="sm",
                ),
                rx.box(
                    rx.heading("Assignments", size="md"),
                    rx.text("Assignments to review or publish will appear here."),
                    padding="1rem",
                    border_radius="md",
                    background_color="white",
                    box_shadow="sm",
                ),
                rx.box(
                    rx.heading("Attendance", size="md"),
                    rx.text("Attendance management tools will appear here."),
                    padding="1rem",
                    border_radius="md",
                    background_color="white",
                    box_shadow="sm",
                ),
                rx.box(
                    rx.heading("Notices", size="md"),
                    rx.text("Notices relevant to faculty will appear here."),
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

