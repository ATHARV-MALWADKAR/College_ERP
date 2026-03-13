import reflex as rx

from college_erp.components.layouts import dashboard_layout


@rx.page(route="/assignments", title="Assignments")
def assignments() -> rx.Component:
    return dashboard_layout(
        rx.vstack(
            rx.heading("Assignments", size="lg"),
            rx.text("Manage assignments and submissions."),
            # TODO: Add assignment list, create form, etc.
            spacing="1.5rem",
            align_items="stretch",
        )
    )