from datetime import date, datetime
from io import BytesIO
from typing import Iterable

import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
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


def _draw_boxed_text(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y_top: float,
    width: float,
    min_y: float,
    font_name: str,
    font_size: float,
    line_height: float,
    padding: float,
) -> float:
    blocks = text.split("\n")
    lines: list[str] = []
    for block in blocks:
        block = block.strip()
        if not block:
            lines.append("")
            continue
        lines.extend(
            _wrap_text(block, font_name, font_size, width - 2 * padding)
        )
    available_height = y_top - min_y
    max_lines = int((available_height - 2 * padding) // line_height)
    if max_lines < 1:
        max_lines = 1
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = f"{lines[-1].rstrip()}..."
    height = 2 * padding + line_height * len(lines)
    y_bottom = y_top - height
    if y_bottom < min_y:
        y_bottom = min_y
        height = y_top - y_bottom

    pdf.setLineWidth(0.6)
    pdf.rect(x, y_bottom, width, height)
    pdf.setFont(font_name, font_size)
    y_text = y_top - padding - font_size
    for line in lines:
        pdf.drawString(x + padding, y_text, line)
        y_text -= line_height
    return y_bottom


def _draw_section(
    pdf: canvas.Canvas,
    orden: OrdenTrabajoOut,
    senas: list[OrdenSenaOut],
    x: float,
    y_start: float,
    y_min: float,
    page_width: float,
    include_cliente: bool,
    include_firma: bool,
) -> None:
    signature_height = 14 * mm if include_firma else 0
    content_min_y = y_min + signature_height

    logo_path = os.path.join(os.path.dirname(__file__), "LOGO KariAriel IG.jpg")
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        logo_width = 24 * mm
        logo_height = 24 * mm
        logo_x = page_width - x - logo_width
        logo_y = y_start - logo_height + 10
        pdf.drawImage(
            logo,
            logo_x,
            logo_y,
            width=logo_width,
            height=logo_height,
            preserveAspectRatio=True,
            mask="auto",
        )

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(x, y_start, "KARI ARIEL")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(x, y_start - 14, "Servicio técnico de celulares")
    pdf.drawString(x, y_start - 26, "Dominicis 815, Campana")
    pdf.drawString(x, y_start - 38, "Whatsapp 3489 515072")
    y = y_start - 52 - 24
    font_name = "Helvetica"
    font_size = 9
    pdf.setFont(font_name, font_size)
    left_bound = x
    right_bound = page_width - x
    full_width = right_bound - left_bound

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
        ("Retiro", "__/__/____"),
    ]
    if include_cliente:
        detalles.extend(
            [
                ("Cliente", orden.cliente_nombre or "-"),
                ("DNI", orden.cliente_dni or "-"),
                ("Contacto", orden.cliente_telefono_contacto or "-"),
                ("Email", orden.cliente_email or "-"),
            ]
        )
    detalles.extend(
        [
        (
            "Telefono",
            orden.telefono_label
            or (f"Telefono #{orden.telefono_id}" if orden.telefono_id else "-"),
        ),
        ("Problema", orden.problema or "-"),
        ("Diagnostico", orden.diagnostico or "-"),
        ("Presupuesto", _fmt_monto(orden.costo_estimado)),
        ("Costo revision", _fmt_monto(orden.costo_revision)),
        ("Garantía (días)", _fmt_monto(orden.garantia)),
        ("Total señas", _fmt_monto(total_senas)),
        ("Resto a pagar", _fmt_monto(resto_pagar)),
        ]
    )

    line_height = 12
    col_gap = 6 * mm
    available_width = right_bound - left_bound
    col_width = (available_width - 2 * col_gap) / 3
    label_width = min(26 * mm, col_width * 0.5)
    value_width = col_width - label_width
    col_x = [
        left_bound,
        left_bound + col_width + col_gap,
        left_bound + 2 * (col_width + col_gap),
    ]
    value_x = [col + label_width for col in col_x]

    y_current = y
    filas: list[list[tuple[str, str]]] = []
    for idx in range(0, len(detalles), 3):
        filas.append(detalles[idx : idx + 3])

    truncado = False
    for fila in filas:
        lineas_por_columna: list[list[str]] = []
        for item in fila:
            _, valor = item
            lineas_por_columna.append(
                _wrap_text(valor, font_name, font_size, value_width)
            )
        lineas_fila = max(
            [len(lineas) for lineas in lineas_por_columna] + [1]
        )

        for indice in range(lineas_fila):
            if y_current < content_min_y:
                pdf.drawString(left_bound, content_min_y, "...")
                y_current = content_min_y - line_height
                truncado = True
                break
            for col_idx, item in enumerate(fila):
                etiqueta, _ = item
                lineas_valor = lineas_por_columna[col_idx]
                if indice == 0:
                    pdf.drawString(col_x[col_idx], y_current, f"{etiqueta}:")
                    if lineas_valor:
                        pdf.drawString(
                            value_x[col_idx], y_current, lineas_valor[0]
                        )
                else:
                    if indice < len(lineas_valor):
                        pdf.drawString(
                            value_x[col_idx],
                            y_current,
                            lineas_valor[indice],
                        )
            y_current -= line_height
        if truncado:
            break
    y = y_current

    y -= 6
    pdf.setFont("Helvetica-Bold", 10)
    y = _draw_lines(
        pdf, ["Historial de señas"], x, y, line_height, content_min_y
    )
    pdf.setFont(font_name, font_size)
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

    aviso_principal = (
        "Queda notificado que el presupuesto se congelará con una seña "
        "mayor o igual al 50%, durante 30 días corridos, luego de "
        "recibida la seña. En caso de haber concluido el plazo, el "
        "presupuesto se actualizará al precio del momento. "
        "Una vez reparado el equipo, y notificado, cuenta con 45 días "
        "para retirar del equipo en Barnetche 2283 o en Dominicis 815, "
        "Campana. Caso contrario, será aplicable la normativa vigente "
        "del CCyCN y ccdts. (Cosa mueble abandonada por su Propietario)."
        "\n"
        "Por cuestiones de seguridad, el equipo sólo podrá retirarse con este comprobante."
    )
    aviso_importante = (
        "Importante: No dejar en el teléfono Chip ni tarjeta de memoria."
    )

    y -= 12
    y = _draw_boxed_text(
        pdf,
        aviso_principal,
        left_bound,
        y,
        full_width,
        content_min_y,
        font_name,
        7.5,
        9,
        4,
    )
    y -= 10
    y = _draw_boxed_text(
        pdf,
        aviso_importante,
        left_bound,
        y,
        full_width,
        content_min_y,
        font_name,
        8,
        9,
        4,
    )
    y -= 10

    if include_firma:
        pdf.setFont("Helvetica", 10)
        firma_y = y_min + 8 * mm
        pdf.drawString(x, firma_y, "Firma del cliente:")
        pdf.line(x + 40 * mm, firma_y - 2, page_width - x, firma_y - 2)


def generar_comprobante_pdf(
    orden: OrdenTrabajoOut, senas: list[OrdenSenaOut]
) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin = 15 * mm
    gap = 15 * mm
    x = 18 * mm

    available = height - 2 * margin - gap
    section_height = available / 2
    top_y = height - margin
    top_min = top_y - section_height
    bottom_y = top_min - gap
    bottom_min = margin

    _draw_section(
        pdf, orden, senas, x, top_y, top_min, width, False, False
    )
    pdf.setLineWidth(0.5)
    pdf.line(margin, bottom_y + gap / 2, width - margin, bottom_y + gap / 2)
    _draw_section(
        pdf, orden, senas, x, bottom_y, bottom_min, width, True, True
    )

    pdf.save()
    buffer.seek(0)
    return buffer.read()
