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
)

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
