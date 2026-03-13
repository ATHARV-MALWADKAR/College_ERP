import reflex as rx

from college_erp.components.layouts import dashboard_layout


@rx.page(route="/submissions/[id]", title="Submission Details")
def submission() -> rx.Component:
    return dashboard_layout(
        rx.vstack(
            rx.heading("Submission Details", size="lg"),
            rx.text("View and grade submission."),
            # TODO: Add submission details, grading form
            spacing="1.5rem",
            align_items="stretch",
        )
    )