import reflex as rx

from college_erp.components.layouts import dashboard_layout


@rx.page(route="/notices", title="Notices")
def notices() -> rx.Component:
    return dashboard_layout(
        rx.vstack(
            rx.heading("Notices", size="lg"),
            rx.text("View announcements and updates."),
            # TODO: Add notices list, create form for faculty/admin
            spacing="1.5rem",
            align_items="stretch",
        )
    )