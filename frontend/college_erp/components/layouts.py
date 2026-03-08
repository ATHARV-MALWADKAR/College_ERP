import reflex as rx

from college_erp.components.navbar import navbar


def dashboard_layout(*children: rx.Component) -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            *children,
            max_width="1200px",
            margin_x="auto",
            padding="1.5rem",
        ),
        background_color="#f7fafc",
        min_height="100vh",
    )

