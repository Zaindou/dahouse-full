from models import (
    db,
    Modelo,
    Ganancia,
    Pagina,
    GananciaPorPagina,
    Periodo,
    Deducible,
    Rol,
    SupuestoGanancia,
    MetaPeriodo,
    PagoDeduccion,
)


from sqlalchemy import func
from datetime import datetime, timedelta, date


def inicializar_paginas():
    paginas = ["Chaturbate", "Stripchat", "Streamate", "Camsoda"]
    for nombre in paginas:
        if not Pagina.query.filter_by(nombre=nombre).first():
            db.session.add(Pagina(nombre=nombre))
    db.session.commit()


def inicializar_roles():
    roles = ["Administrador", "Modelo", "Usuario"]
    for nombre_rol in roles:
        if not Rol.query.filter_by(nombre=nombre_rol).first():
            nuevo_rol = Rol(nombre=nombre_rol)
            db.session.add(nuevo_rol)
    db.session.commit()


def obtener_periodo_actual():
    ultimo_periodo = Periodo.query.order_by(Periodo.fecha_fin.desc()).first()

    fecha_inicio = ultimo_periodo.fecha_inicio.strftime("%Y-%m-%d")
    fecha_fin = ultimo_periodo.fecha_fin.strftime("%Y-%m-%d")

    return (
        ultimo_periodo.nombre,
        fecha_inicio,
        fecha_fin,
    )


def calcular_nuevo_periodo():
    """
    Calcula el próximo período basado en la última fecha de la tabla Periodo.

    Returns:
        dict: Información del nuevo período con las claves 'nombre', 'fecha_inicio', y 'fecha_fin'.
    """
    try:
        # Obtener el último período registrado
        ultimo_periodo = Periodo.query.order_by(Periodo.fecha_fin.desc()).first()

        if not ultimo_periodo:
            raise ValueError("No hay períodos registrados en la base de datos.")

        # Usar la fecha fin del último período como el inicio del nuevo
        fecha_inicio = ultimo_periodo.fecha_fin

        # Calcular la nueva fecha de fin (14 días desde la fecha de inicio)
        fecha_fin = fecha_inicio + timedelta(days=14)

        # Generar el nombre del período usando el mes de la fecha de fin
        año = fecha_fin.year
        mes = fecha_fin.strftime("%b").upper()
        semana = 1 if fecha_fin.day <= 14 else 2  # Asignar 1 o 2 según el rango de días
        nombre_periodo = f"{año}-{mes}-{semana}"

        return {
            "nombre": nombre_periodo,
            "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
            "fecha_fin": fecha_fin.strftime("%Y-%m-%d"),
        }

    except Exception as e:
        print(f"Error al calcular el nuevo período: {e}")
        return None


# TOOLS FOR BUSSINES ENDPOINTS

MESES_MAP = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}


def get_stats_por_periodo():
    return (
        db.session.query(
            Periodo.nombre.label("periodo"),
            func.sum(GananciaPorPagina.total_cop).label("ganancia_modelos"),
            func.sum(GananciaPorPagina.ganancia_estudio_cop).label("ganancia_estudio"),
            func.sum(GananciaPorPagina.tokens).label("total_tokens"),
        )
        .join(Ganancia, Ganancia.periodo_id == Periodo.id)
        .join(GananciaPorPagina, Ganancia.id == GananciaPorPagina.ganancia_id)
        .group_by(Periodo.nombre)
        .order_by(Periodo.nombre)
        .all()
    )


def get_deducciones_por_periodo():
    return (
        db.session.query(
            Periodo.nombre.label("periodo"),
            Deducible.concepto.label("concepto"),
            func.sum(PagoDeduccion.monto_pagado).label("total_deducciones"),
        )
        .join(Ganancia, Ganancia.periodo_id == Periodo.id)
        .join(PagoDeduccion, PagoDeduccion.pago_id == Ganancia.id)
        .join(Deducible, Deducible.id == PagoDeduccion.deduccion_id)
        .group_by(Periodo.nombre, Deducible.concepto)
        .order_by(Periodo.nombre, Deducible.concepto)
        .all()
    )


def get_tokens_por_modelo_pagina():
    return (
        db.session.query(
            Periodo.nombre.label("periodo"),
            Modelo.nombre_usuario.label("modelo_usuario"),
            Pagina.nombre.label("pagina"),
            func.sum(GananciaPorPagina.tokens).label("total_tokens"),
        )
        .join(Ganancia, Ganancia.periodo_id == Periodo.id)
        .join(GananciaPorPagina, Ganancia.id == GananciaPorPagina.ganancia_id)
        .join(Modelo, Ganancia.modelo_id == Modelo.id)
        .join(Pagina, GananciaPorPagina.pagina_id == Pagina.id)
        .group_by(Periodo.nombre, Modelo.nombre_usuario, Pagina.nombre)
        .order_by(Periodo.nombre, Modelo.nombre_usuario, Pagina.nombre)
        .all()
    )


def calculate_trends(stats):
    """
    The function `calculate_trends` sorts statistics by year and month, calculates the percentage trend
    in total tokens, and adds this trend to each statistic entry.

    :param stats: It seems like the code snippet you provided is a Python function `calculate_trends`
    that calculates the trend percentage based on the total tokens in the input statistics data.
    However, the `MESES_MAP` variable is not defined in the snippet
    :return: The function `calculate_trends` is returning a list of dictionaries where each dictionary
    represents a statistical data point with an added key "tendencia" that represents the percentage
    change in "total_tokens" compared to the previous data point. The list contains these updated
    statistical data points with the calculated trends.
    """
    # Ordenar los datos por año y mes
    stats_ordenados = sorted(
        stats,
        key=lambda x: (
            int(x["mes_año"].split("-")[0]),  # Año
            MESES_MAP[x["mes_año"].split("-")[1]],  # Mes
        ),
    )

    tendencia_anterior_tokens = None
    estadisticas_con_tendencia = []

    for stat in stats_ordenados:
        total_tokens = stat["total_tokens"]
        if tendencia_anterior_tokens is not None:
            if tendencia_anterior_tokens > 0:
                tendencia = (
                    (total_tokens - tendencia_anterior_tokens)
                    / tendencia_anterior_tokens
                ) * 100
            else:
                tendencia = 0
        else:
            tendencia = None

        stat["tendencia"] = round(tendencia, 2) if tendencia is not None else None
        tendencia_anterior_tokens = total_tokens
        estadisticas_con_tendencia.append(stat)

    return estadisticas_con_tendencia


def obtener_nombre_creador(creado_por_id):
    if creado_por_id is None:
        return "Administrador"  # Valor por defecto si no hay creador

    creador = Modelo.query.get(creado_por_id)
    return creador.nombre_usuario if creador else "Administrador"
