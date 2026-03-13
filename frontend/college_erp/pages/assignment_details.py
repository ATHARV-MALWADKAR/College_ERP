import reflex as rx

from college_erp.components.layouts import dashboard_layout


@rx.page(route="/assignments/[id]", title="Assignment Details")
def assignment_details() -> rx.Component:
    return dashboard_layout(
        rx.vstack(
            rx.heading("Assignment Details", size="lg"),
            rx.text("View assignment details and submissions."),
            # TODO: Add assignment details, submission form for students, grading for faculty
            spacing="1.5rem",
            align_items="stretch",
        )
    )