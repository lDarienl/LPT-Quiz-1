"""
Problema 1: Sistema de navegación de páginas web

Diagrama de flujo (conceptual):
    [Inicio] --> loadPage(url) --> [Añadir a historial back, limpiar forward]
    goBack() --> [¿Hay páginas anteriores?] --> No --> [Retornar None/error]
                --> Sí --> [Mover actual a forward, ir a anterior]
    goForward() --> [¿Hay páginas siguientes?] --> No --> [Retornar None/error]
                   --> Sí --> [Mover actual a back, ir a siguiente]
"""


class WebBrowser:
    """
    Sistema de navegación tipo navegador: back, forward y carga de página.
    Usa dos pilas: una para "atrás" (historial pasado) y otra para "adelante".
    """

    def __init__(self):
        self._current: str | None = None   # Página actual
        self._back: list[str] = []         # Pilas para ir atrás
        self._forward: list[str] = []      # Pila para ir adelante

    def load_page(self, url: str) -> str:
        """
        Carga una nueva página. La página actual (si existe) se guarda en back.
        Se vacía la pila forward (como en un navegador real).
        """
        if self._current is not None:
            self._back.append(self._current)
        self._forward.clear()
        self._current = url
        return self._current

    def go_back(self) -> str | None:
        """
        Vuelve a la página anterior.
        Retorna la URL de la página anterior o None si no hay.
        """
        if not self._back:
            return None
        if self._current is not None:
            self._forward.append(self._current)
        self._current = self._back.pop()
        return self._current

    def go_forward(self) -> str | None:
        """
        Avanza a la página siguiente (después de haber hecho go_back).
        Retorna la URL o None si no hay siguiente.
        """
        if not self._forward:
            return None
        if self._current is not None:
            self._back.append(self._current)
        self._current = self._forward.pop()
        return self._current

    def current_page(self) -> str | None:
        """Devuelve la URL de la página actual, o None si no hay ninguna."""
        return self._current

    # Aliases en camelCase como se pide en el enunciado
    def loadPage(self, url: str) -> str:
        return self.load_page(url)

    def goBack(self) -> str | None:
        return self.go_back()

    def goForward(self) -> str | None:
        return self.go_forward()
