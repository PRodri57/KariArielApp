from datetime import date, datetime
from io import BytesIO
from typing import Iterable

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

from App.Schemas.orden_trabajo import OrdenSenaOut, OrdenTrabajoOut


def _fmt_fecha(value: object) -> str:
    if value is None:
        return "-"
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        return value[:10]
    return str(value)


def _fmt_monto(value: object) -> str:
    if value is None:
        return "-"
    return str(value)


def _wrap_text(
    text: str, font_name: str, font_size: float, max_width: float
) -> list[str]:
    if not text:
        return ["-"]
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        next_piece = f"{current} {word}".strip()
        if (
            pdfmetrics.stringWidth(next_piece, font_name, font_size)
            <= max_width
        ):
            current = next_piece
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _draw_lines(
    pdf: canvas.Canvas,
    lines: Iterable[str],
    x: float,
    y: float,
    line_height: float,
    min_y: float,
) -> float:
    for line in lines:
        if y < min_y:
            pdf.drawString(x, min_y, "...")
            return min_y - line_height
        pdf.drawString(x, y, line)
        y -= line_height
    return y


def _draw_wrapped(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    line_height: float,
    min_y: float,
    font_name: str,
    font_size: float,
    max_width: float,
) -> float:
    lines = _wrap_text(text, font_name, font_size, max_width)
    return _draw_lines(pdf, lines, x, y, line_height, min_y)


def _draw_section(
    pdf: canvas.Canvas,
    orden: OrdenTrabajoOut,
    senas: list[OrdenSenaOut],
    x: float,
    y_start: float,
    y_min: float,
    page_width: float,
) -> None:
    signature_height = 22 * mm
    content_min_y = y_min + signature_height

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(x, y_start, "Comprobante de orden")
    y = y_start - 16
    font_name = "Helvetica"
    font_size = 10
    pdf.setFont(font_name, font_size)

    total_senas = orden.total_senas
    if total_senas is None:
        if orden.sena is not None:
            total_senas = orden.sena
        else:
            total_senas = sum(int(item.monto) for item in senas)
    if orden.costo_estimado is not None:
        resto_pagar = orden.resto_pagar
        if resto_pagar is None:
            resto_pagar = orden.costo_estimado - total_senas
    else:
        resto_pagar = None

    detalles = [
        ("Orden", f"#{orden.numero_orden}"),
        ("Ingreso", _fmt_fecha(orden.fecha_ingreso)),
        ("Retiro", _fmt_fecha(orden.fecha_retiro)),
        ("Cliente", orden.cliente_nombre or "-"),
        (
            "Telefono",
            orden.telefono_label
            or (f"Telefono #{orden.telefono_id}" if orden.telefono_id else "-"),
        ),
        ("Problema", orden.problema or "-"),
        ("Diagnostico", orden.diagnostico or "-"),
        ("Costo estimado", _fmt_monto(orden.costo_estimado)),
        ("Costo revision", _fmt_monto(orden.costo_revision)),
        ("Seña revisión", _fmt_monto(orden.sena_revision)),
        ("Total señas", _fmt_monto(total_senas)),
        ("Resto a pagar", _fmt_monto(resto_pagar)),
    ]

    line_height = 12
    col_gap = 10 * mm
    left_bound = x
    right_bound = page_width - x
    available_width = right_bound - left_bound
    col_width = (available_width - col_gap) / 2
    label_width = min(32 * mm, col_width * 0.45)
    value_width = col_width - label_width
    left_value_x = left_bound + label_width
    right_col_x = left_bound + col_width + col_gap
    right_value_x = right_col_x + label_width

    y_current = y
    filas: list[tuple[tuple[str, str], tuple[str, str] | None]] = []
    for idx in range(0, len(detalles), 2):
        izquierda = detalles[idx]
        derecha = detalles[idx + 1] if idx + 1 < len(detalles) else None
        filas.append((izquierda, derecha))

    truncado = False
    for izquierda, derecha in filas:
        etiqueta_izq, valor_izq = izquierda
        lineas_izq = _wrap_text(
            valor_izq, font_name, font_size, value_width
        )
        if derecha:
            etiqueta_der, valor_der = derecha
            lineas_der = _wrap_text(
                valor_der, font_name, font_size, value_width
            )
        else:
            etiqueta_der = ""
            lineas_der = []
        lineas_fila = max(len(lineas_izq), len(lineas_der), 1)

        for indice in range(lineas_fila):
            if y_current < content_min_y:
                pdf.drawString(left_bound, content_min_y, "...")
                y_current = content_min_y - line_height
                truncado = True
                break
            if indice == 0:
                pdf.drawString(left_bound, y_current, f"{etiqueta_izq}:")
                if lineas_izq:
                    pdf.drawString(left_value_x, y_current, lineas_izq[0])
                if derecha:
                    pdf.drawString(
                        right_col_x, y_current, f"{etiqueta_der}:"
                    )
                    if lineas_der:
                        pdf.drawString(
                            right_value_x, y_current, lineas_der[0]
                        )
            else:
                if indice < len(lineas_izq):
                    pdf.drawString(
                        left_value_x, y_current, lineas_izq[indice]
                    )
                if derecha and indice < len(lineas_der):
                    pdf.drawString(
                        right_value_x, y_current, lineas_der[indice]
                    )
            y_current -= line_height
        if truncado:
            break
    y = y_current

    y -= 6
    pdf.setFont("Helvetica-Bold", 11)
    y = _draw_lines(
        pdf, ["Historial de senas"], x, y, line_height, content_min_y
    )
    pdf.setFont(font_name, font_size)
    full_width = right_bound - left_bound

    if not senas:
        y = _draw_wrapped(
            pdf,
            "Sin señas registradas.",
            x,
            y,
            line_height,
            content_min_y,
            font_name,
            font_size,
            full_width,
        )
    else:
        for sena in senas:
            linea = f"{_fmt_fecha(sena.created_at)} - ${_fmt_monto(sena.monto)}"
            y = _draw_wrapped(
                pdf,
                linea,
                x,
                y,
                line_height,
                content_min_y,
                font_name,
                font_size,
                full_width,
            )

    pdf.setFont("Helvetica", 10)
    firma_y = y_min + 14 * mm
    fecha_y = y_min + 5 * mm
    pdf.drawString(x, firma_y, "Firma del cliente:")
    pdf.line(x + 40 * mm, firma_y - 2, page_width - x, firma_y - 2)
    pdf.drawString(x, fecha_y, "Fecha: __/__/____")


def generar_comprobante_pdf(
    orden: OrdenTrabajoOut, senas: list[OrdenSenaOut]
) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin = 15 * mm
    gap = 8 * mm
    x = 18 * mm

    available = height - 2 * margin - gap
    section_height = available / 2
    top_y = height - margin
    top_min = top_y - section_height
    bottom_y = top_min - gap
    bottom_min = margin

    _draw_section(pdf, orden, senas, x, top_y, top_min, width)
    pdf.setLineWidth(0.5)
    pdf.line(margin, bottom_y + gap / 2, width - margin, bottom_y + gap / 2)
    _draw_section(pdf, orden, senas, x, bottom_y, bottom_min, width)

    pdf.save()
    buffer.seek(0)
    return buffer.read()
