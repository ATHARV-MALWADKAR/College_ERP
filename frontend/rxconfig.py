import reflex as rx


class CollegeErpConfig(rx.Config):
    app_name: str = "college_erp"
    db_url: str | None = None
    api_url: str = "http://localhost:8000"


config = CollegeErpConfig()

