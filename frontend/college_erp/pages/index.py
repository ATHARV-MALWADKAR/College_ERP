import reflex as rx

from college_erp.components.layouts import dashboard_layout


@rx.page(route="/", title="College ERP - Login")
def index() -> rx.Component:
    return dashboard_layout(
        rx.vstack(
            rx.heading("Welcome to College ERP", size="lg"),
            rx.text(
                "Log in as a student, faculty member, or administrator "
                "to access your dashboard."
            ),
            rx.hstack(
                rx.button("Student", on_click=lambda: rx.redirect("/student/dashboard")),
                rx.button("Faculty", on_click=lambda: rx.redirect("/faculty/dashboard")),
                rx.button("Admin", on_click=lambda: rx.redirect("/admin/dashboard")),
                spacing="4",
            ),
            spacing="4",
            align_items="flex-start",
        )
    )

