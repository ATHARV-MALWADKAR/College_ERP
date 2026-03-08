import reflex as rx


def navbar() -> rx.Component:
    return rx.hstack(
        rx.text("College ERP", font_size="1.5rem", font_weight="bold"),
        rx.spacer(),
        rx.link("Student", href="/student/dashboard"),
        rx.link("Faculty", href="/faculty/dashboard"),
        rx.link("Admin", href="/admin/dashboard"),
        padding="1rem",
        border_bottom="1px solid #e2e8f0",
        background_color="white",
        align_items="center",
    )

