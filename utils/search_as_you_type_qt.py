from __future__ import annotations

import threading
from typing import Callable, Optional, Any

from PySide6.QtCore import QTimer, QMetaObject, Qt
from PySide6.QtWidgets import QLineEdit


class SearchAsYouTypeQt:
    """
    Utilidad genérica de "search as you type" para PySide6.

    Uso:
        helper = SearchAsYouTypeQt(
            line_edit=myLineEdit,
            search_callable=lambda term: do_query(term),
            on_results=lambda results, term: render(results),
            on_started=lambda term: set_status("Buscando..."),
            on_error=lambda err, term: show_error(err),
            delay_ms=500,
            min_chars=2,
        )

    - Ejecuta search_callable(term) en un hilo de fondo
    - Entrega resultados en el hilo principal vía on_results(results, term)
    - Ignora resultados obsoletos cuando el término cambió mientras la búsqueda corría
    """

    def __init__(
        self,
        line_edit: QLineEdit,
        search_callable: Callable[[str], Any],
        on_results: Callable[[Any, str], None],
        *,
        on_started: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[Exception, str], None]] = None,
        delay_ms: int = 500,
        min_chars: int = 1,
    ) -> None:
        self._line_edit = line_edit
        self._search_callable = search_callable
        self._on_results = on_results
        self._on_started = on_started
        self._on_error = on_error
        self._delay_ms = delay_ms
        self._min_chars = max(0, min_chars)

        self._timer = QTimer(line_edit)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._on_timeout)

        self._last_term: str = ""
        self._active_query_id: int = 0

        line_edit.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self, text: str) -> None:
        self._last_term = text.strip()
        self._timer.start(self._delay_ms)
        if self._on_started is not None:
            self._on_started(self._last_term)

    def _on_timeout(self) -> None:
        term = self._last_term
        print(f"DEBUG: SearchAsYouTypeQt._on_timeout llamado con término: '{term}', min_chars: {self._min_chars}")
        if len(term) < self._min_chars:
            print(f"DEBUG: Término '{term}' es muy corto (longitud: {len(term)})")
            # Consideramos "sin término suficiente" como resultado vacío inmediato
            self._deliver_results(term, [])
            return

        print(f"DEBUG: Ejecutando búsqueda para término: '{term}'")
        self._active_query_id += 1
        query_id = self._active_query_id

        # Ejecutar búsqueda directamente en el hilo principal
        try:
            results = self._search_callable(term)
            print(f"DEBUG: SearchAsYouTypeQt obtuvo {len(results) if results else 0} resultados")
        except Exception as exc:  # noqa: BLE001
            print(f"DEBUG: SearchAsYouTypeQt error: {exc}")
            self._deliver_error(term, exc, query_id)
            return
        print(f"DEBUG: SearchAsYouTypeQt entregando resultados")
        self._deliver_results(term, results, query_id)

    def _deliver_results(self, term: str, results: Any, query_id: Optional[int] = None) -> None:
        print(f"DEBUG: SearchAsYouTypeQt._deliver_results llamado con {len(results) if results else 0} resultados, término: '{term}'")
        # Ignorar si llegó tarde
        if query_id is not None and query_id != self._active_query_id:
            print(f"DEBUG: Resultados ignorados porque query_id {query_id} != active_query_id {self._active_query_id}")
            return
        print(f"DEBUG: Entregando resultados al callback on_results")
        
        # Ejecutar directamente en el hilo principal
        print(f"DEBUG: Ejecutando callback on_results con {len(results) if results else 0} resultados")
        self._on_results(results, term)

    def _deliver_error(self, term: str, error: Exception, query_id: Optional[int] = None) -> None:
        if query_id is not None and query_id != self._active_query_id:
            return
        if self._on_error is not None:
            QTimer.singleShot(0, lambda: self._on_error(error, term))

    def dispose(self) -> None:
        try:
            self._timer.stop()
        except Exception:
            pass
        try:
            self._line_edit.textChanged.disconnect(self._on_text_changed)
        except Exception:
            pass


__all__ = ["SearchAsYouTypeQt"]


