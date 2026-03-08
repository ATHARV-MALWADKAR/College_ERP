import reflex as rx


class AuthState(rx.State):
    is_authenticated: bool = False
    role: str | None = None
    access_token: str | None = None

    def login(self, role: str, token: str) -> None:
        self.is_authenticated = True
        self.role = role
        self.access_token = token

    def logout(self) -> None:
        self.is_authenticated = False
        self.role = None
        self.access_token = None

