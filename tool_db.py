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
