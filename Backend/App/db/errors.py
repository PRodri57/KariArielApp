class DatabaseUnavailableError(RuntimeError):
    def __init__(
        self,
        detail: str = "Base de datos no disponible. Intenta mas tarde.",
    ) -> None:
        super().__init__(detail)
        self.detail = detail
