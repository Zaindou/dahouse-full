from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from io import BytesIO


def generar_pdf_desprendible(modelo, ganancia, total_cop, fecha_pago):
    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=1 * cm,
        leftMargin=1 * cm,
        topMargin=1 * cm,
        bottomMargin=1 * cm,
    )

    elements = []
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="MainHeader",
            parent=styles["Heading1"],
            fontSize=18,
            textColor=colors.HexColor("#003366"),
            spaceAfter=10,
            alignment=TA_CENTER,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeader",
            parent=styles["Heading2"],
            fontSize=12,
            textColor=colors.HexColor("#003366"),
            spaceAfter=6,
            alignment=TA_LEFT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="NormalText",
            parent=styles["Normal"],
            fontSize=10,
            leading=12,
            textColor=colors.black,
        )
    )

    styles.add(
        ParagraphStyle(
            name="WhiteText",
            parent=styles["NormalText"],
            fontSize=10,
            leading=12,
            textColor=colors.white,
        )
    )

    # Header with Logo
    header_table = Table(
        [
            [
                Image("frontend/assets/logo.png", width=180, height=34),
                "Desprendible de Pago",
            ]
        ],
        colWidths=[2 * inch, 4 * inch],
    )

    header_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("TEXTCOLOR", (1, 0), (1, 0), colors.HexColor("#003366")),
                ("FONTNAME", (1, 0), (1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (1, 0), (1, 0), 18),
            ]
        )
    )

    elements.append(header_table)
    elements.append(
        HRFlowable(
            width="100%",
            thickness=1,
            lineCap="round",
            color=colors.HexColor("#003366"),
            spaceBefore=5,
            spaceAfter=10,
        )
    )

    # NIT
    elements.append(
        Paragraph(
            "NIT: 1010014363-7", ParagraphStyle("NIT", fontSize=10, alignment=TA_RIGHT)
        )
    )
    elements.append(Spacer(1, 20))

    # Period
    elements.append(
        Paragraph(
            f"<b>Período de Pago:</b> {ganancia.periodo.nombre}",
            styles["SectionHeader"],
        )
    )
    elements.append(Spacer(1, 20))

    # Employee Information
    elements.append(Paragraph("Información del Empleado", styles["SectionHeader"]))

    employee_data = [
        [
            Paragraph(
                f"<b>Nombre:</b> {modelo.nombres} {modelo.apellidos}",
                styles["NormalText"],
            )
        ],
        [
            Paragraph(
                f"<b>Número de Cédula:</b> {modelo.numero_documento}",
                styles["NormalText"],
            )
        ],
        [Paragraph(f"<b>Fecha de Pago:</b> {fecha_pago}", styles["NormalText"])],
    ]

    employee_table = Table(employee_data, colWidths=[6 * inch])
    employee_table.setStyle(
        TableStyle(
            [
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LINEBELOW", (0, 0), (-1, -1), 1, colors.HexColor("#E6E6E6")),
            ]
        )
    )

    elements.append(employee_table)
    elements.append(Spacer(1, 20))

    # Bank Details
    elements.append(Paragraph("Detalles Bancarios", styles["SectionHeader"]))

    bank_data = [
        [Paragraph(f"<b>Entidad de Pago:</b> {modelo.banco}", styles["NormalText"])],
        [Paragraph("<b>Tipo de Cuenta:</b> Ahorros", styles["NormalText"])],
        [
            Paragraph(
                f"<b>Número de Cuenta:</b> {modelo.numero_cuenta}", styles["NormalText"]
            )
        ],
    ]

    bank_table = Table(bank_data, colWidths=[6 * inch])
    bank_table.setStyle(
        TableStyle(
            [
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LINEBELOW", (0, 0), (-1, -1), 1, colors.HexColor("#E6E6E6")),
            ]
        )
    )

    elements.append(bank_table)
    elements.append(Spacer(1, 20))

    # Payment Details
    elements.append(Paragraph("Detalle de Pagos", styles["SectionHeader"]))

    valor_cop_str = f"${total_cop:,.0f}"

    payment_data = [
        [
            Paragraph("<b>Descripción</b>", styles["WhiteText"]),
            Paragraph("<b>Valor Devengado</b>", styles["WhiteText"]),
            Paragraph("<b>Valor Descontado</b>", styles["WhiteText"]),
        ],
        ["Salario Base", valor_cop_str, "$0"],
        ["Total Neto a Pagar", valor_cop_str, ""],
    ]

    payment_table = Table(payment_data, colWidths=[2.5 * inch, 2 * inch, 2 * inch])
    payment_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("ALIGN", (0, 1), (0, -1), "LEFT"),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LINEBELOW", (0, 0), (-1, 0), 1, colors.white),
                ("LINEABOVE", (0, -1), (-1, -1), 1, colors.HexColor("#003366")),
                ("LINEBELOW", (0, -2), (-1, -2), 1, colors.HexColor("#E6E6E6")),
            ]
        )
    )
    elements.append(payment_table)

    # Footer
    elements.append(Spacer(1, 50))
    elements.append(
        HRFlowable(
            width="100%",
            thickness=1,
            lineCap="round",
            color=colors.HexColor("#003366"),
            spaceBefore=5,
            spaceAfter=5,
        )
    )
    elements.append(
        Paragraph(
            "Generado por el Sistema de Nómina de DaHouse Studio",
            ParagraphStyle("Footer", fontSize=8, alignment=TA_CENTER),
        )
    )

    pdf.build(elements)
    return buffer.getvalue()
