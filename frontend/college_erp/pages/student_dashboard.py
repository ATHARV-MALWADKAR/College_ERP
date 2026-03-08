import reflex as rx

from college_erp.components.layouts import dashboard_layout


@rx.page(route="/student/dashboard", title="Student Dashboard")
def student_dashboard() -> rx.Component:
    return dashboard_layout(
        rx.vstack(
            rx.heading("Student Dashboard", size="lg"),
            rx.text("Overview of attendance, assignments, results, and notices."),
            rx.grid(
                rx.box(
                    rx.heading("Attendance", size="md"),
                    rx.text("Attendance summary will appear here."),
                    padding="1rem",
                    border_radius="md",
                    background_color="white",
                    box_shadow="sm",
                ),
                rx.box(
                    rx.heading("Assignments", size="md"),
                    rx.text("Upcoming and pending assignments will appear here."),
                    padding="1rem",
                    border_radius="md",
                    background_color="white",
                    box_shadow="sm",
                ),
                rx.box(
                    rx.heading("Results", size="md"),
                    rx.text("Recent exam results will appear here."),
                    padding="1rem",
                    border_radius="md",
                    background_color="white",
                    box_shadow="sm",
                ),
                rx.box(
                    rx.heading("Notices", size="md"),
                    rx.text("Important college notices will appear here."),
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

