from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from models import (
    db,
    Modelo,
    Ganancia,
    Pagina,
    GananciaPorPagina,
    Periodo,
    Deducible,
    Rol,
)
from datetime import datetime, timedelta

from config import Config

import requests
import environ
import os

env = environ.Env()


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)


def inicializar_paginas():
    paginas = ["Chaturbate", "Stripchat", "Streamate", "CherryTV", "Camsoda"]
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


def calcular_porcentaje(tokens, exclusividad):
    if exclusividad:
        if tokens <= 29999:
            return 0.6
        elif tokens <= 40000:
            return 0.65
        else:
            return min(0.7, 0.65 + (tokens - 40000) // 4000 * 0.01)
    else:
        if tokens <= 20000:
            return 0.5
        elif tokens <= 25999:
            return 0.55
        elif tokens <= 30999:
            return 0.6
        elif tokens <= 36000:
            return 0.65
        else:
            return min(0.7, 0.65 + (tokens - 36000) // 4000 * 0.01)


def obtener_martes_del_mes(año, mes, n):
    """Devuelve el n-ésimo martes del mes especificado."""
    primer_dia_del_mes = datetime(año, mes, 1)
    dias_hasta_martes = (1 - primer_dia_del_mes.weekday() + 7) % 7
    primer_martes = primer_dia_del_mes + timedelta(days=dias_hasta_martes)
    return primer_martes + timedelta(weeks=n - 1)


def obtener_periodo_actual():
    # hoy = datetime(2031, 10, 12)
    hoy = datetime.today()
    año = hoy.year
    mes = hoy.strftime("%b").upper()

    segundo_martes = obtener_martes_del_mes(año, hoy.month, 2)
    cuarto_martes = obtener_martes_del_mes(año, hoy.month, 4)

    if hoy.date() <= segundo_martes.date():
        nombre_periodo = f"{año}-{mes}-1"
        fecha_inicio = segundo_martes - timedelta(days=14)
        fecha_fin = segundo_martes
    elif hoy.date() <= cuarto_martes.date():
        nombre_periodo = f"{año}-{mes}-2"
        fecha_inicio = segundo_martes
        fecha_fin = cuarto_martes
    else:
        nombre_periodo = f"{año}-{mes}-3"
        fecha_inicio = cuarto_martes
        fecha_fin = cuarto_martes + timedelta(days=14)
    fecha_inicio = fecha_inicio.strftime("%Y-%m-%d")
    fecha_fin = fecha_fin.strftime("%Y-%m-%d")

    return nombre_periodo, fecha_inicio, fecha_fin


def obtener_trm():
    url = os.environ.get("TRM_URL")
    response = requests.get(url)
    data = response.json()
    valor = float(data[0]["valor"])
    valor = valor - float(os.environ.get("TRM_ADICIONAL"))
    return valor


def ganancias_totales_periodo(nombre_periodo):
    periodo = Periodo.query.filter_by(nombre=nombre_periodo).first()
    if not periodo:
        return {"mensaje": "Período no encontrado", "codigo": 404}

    ganancias = Ganancia.query.filter_by(periodo_id=periodo.id).all()
    if not ganancias:
        return {
            "mensaje": "No se encontraron ganancias para el período especificado",
            "codigo": 404,
        }

    total_cop = sum(ganancia.total_cop for ganancia in ganancias)
    return {"total_cop": total_cop, "codigo": 200}


@app.route("/financiero", methods=["GET"])
def financiero():
    trm_actual = obtener_trm() + float(os.environ.get("TRM_ADICIONAL"))
    periodo_actual = obtener_periodo_actual()
    # periodo_ganancias = ganancias_totales_periodo(periodo_actual[0])

    # if periodo_ganancias["codigo"] != 200:
    #     return (
    #         jsonify({"mensaje": periodo_ganancias["mensaje"]}),
    #         periodo_ganancias["codigo"],
    #     )

    datos_financieros = {
        "trm_liquidacion": obtener_trm(),
        "trm_actual": trm_actual,
        "periodo_actual": periodo_actual,
        # "ganancias_totales_periodo": periodo_ganancias["total_cop"],
    }
    return jsonify(datos_financieros)


@app.route("/modelos", methods=["POST"])
def crear_modelo():
    datos = request.json
    nuevo_modelo = Modelo(
        tipo_documento=datos["tipo_documento"],
        numero_documento=datos["numero_documento"],
        nombres=datos["nombres"],
        apellidos=datos["apellidos"],
        fecha_nacimiento=datetime.strptime(datos["fecha_nacimiento"], "%Y-%m-%d"),
        correo_electronico=datos["correo_electronico"],
        nombre_usuario=datos["nombre_usuario"],
        rol_id=datos["rol_id"],
        banco=datos["banco"],
        numero_cuenta=datos["numero_cuenta"],
        habilitado=True,
        fecha_registro=datetime.now(),
        exclusividad=False,
    )

    if numero_documento := datos.get("numero_documento"):
        if Modelo.query.filter_by(numero_documento=numero_documento).first():
            return (
                jsonify(
                    {"mensaje": "Ya existe un usuario con este número de documento"}
                ),
                400,
            )
    if correo_electronico := datos.get("correo_electronico"):
        if Modelo.query.filter_by(correo_electronico=correo_electronico).first():
            return (
                jsonify(
                    {"mensaje": "Ya existe un usuario con este correo electrónico"}
                ),
                400,
            )

    # Agrega las páginas habilitadas al modelo
    for pagina_nombre in datos["paginas_habilitadas"]:
        pagina = Pagina.query.filter_by(nombre=pagina_nombre).first()
        if pagina:
            nuevo_modelo.paginas.append(pagina)

    db.session.add(nuevo_modelo)
    db.session.commit()
    return jsonify({"mensaje": "Usuario creado correctamente!"})


@app.route("/modelos", methods=["GET"])
def obtener_modelos():
    try:
        modelos = Modelo.query.all()
        lista_modelos = []
        for modelo in modelos:
            ultimo_estado_ganancia = "Sin ganancias"
            if modelo.ganancias:
                ultima_ganancia = modelo.ganancias.order_by(Ganancia.id.desc()).first()
                ultimo_estado_ganancia = (
                    ultima_ganancia.estado if ultima_ganancia else "Sin ganancias"
                )
                # con el periodo_id traer el nombre del periodo en la tabla ganancia
                periodo_id = ultima_ganancia.periodo_id if ultima_ganancia else "Sin ID"

                nombre_perido = None
                if periodo_id == "Sin ID":
                    nombre_perido = "Sin periodo asociado"
                else:
                    ganancia = Periodo.query.filter_by(id=periodo_id).first()
                    nombre_periodo = ganancia.nombre

                ganancia_info = (
                    {
                        "id": ultima_ganancia.id,
                        "total_cop": ultima_ganancia.total_cop,
                        "trm": ultima_ganancia.trm,
                        "estado": ultimo_estado_ganancia,
                        "ultimo_periodo": nombre_periodo,
                        "porcentaje": ultima_ganancia.porcentaje,
                    }
                    if ultima_ganancia
                    else "Sin infomación"
                )

            lista_modelos.append(
                {
                    "id": modelo.id,
                    "nombres": modelo.nombres,
                    "apellidos": modelo.apellidos,
                    "tipo_documento": modelo.tipo_documento,
                    "numero_documento": modelo.numero_documento,
                    "nombre_usuario": modelo.nombre_usuario,
                    "habilitado": modelo.habilitado,
                    "rol": modelo.rol.nombre,
                    "paginas_habilitadas": [pagina.nombre for pagina in modelo.paginas],
                    "correo_electronico": modelo.correo_electronico,
                    "fecha_nacimiento": modelo.fecha_nacimiento.strftime("%Y-%m-%d"),
                    "fecha_registro": modelo.fecha_registro.strftime("%Y-%m-%d"),
                    "numero_cuenta": modelo.numero_cuenta,
                    "banco": modelo.banco,
                    "ganancia_info": ganancia_info,
                    "estado_ganancia": ultimo_estado_ganancia,
                    "periodo_actual": obtener_periodo_actual()[0],
                    "deducibles": [
                        {
                            "concepto": deducible.concepto,
                            "valor_total": deducible.valor_total,
                            "valor_quincenal": deducible.valor_quincenal,
                            "plazo": deducible.plazo,
                            "quincenas_restantes": deducible.quincenas_restantes,
                            "estado": deducible.estado,
                            "valor_pagado": deducible.valor_pagado,
                            "valor_restante": deducible.valor_restante,
                        }
                        for deducible in modelo.deducibles
                    ],
                }
            )
        return jsonify(lista_modelos)
    except Exception as e:
        return jsonify({"mensaje": str(e)}), 500


@app.route("/modelos/<int:modelo_id>", methods=["PUT"])
def actualizar_modelo(modelo_id):
    datos = request.json
    modelo = Modelo.query.get_or_404(modelo_id)

    modelo.nombres = datos.get("nombres", modelo.nombres)
    modelo.apellidos = datos.get("apellidos", modelo.apellidos)
    modelo.tipo_documento = datos.get("tipo_documento", modelo.tipo_documento)
    modelo.numero_documento = datos.get("numero_documento", modelo.numero_documento)
    modelo.nombre_usuario = datos.get("nombre_usuario", modelo.nombre_usuario)
    modelo.habilitado = datos.get("habilitado", modelo.habilitado)
    modelo.banco = datos.get("banco", modelo.banco)
    modelo.numero_cuenta = datos.get("numero_cuenta", modelo.numero_cuenta)
    modelo.correo_electronico = datos.get(
        "correo_electronico", modelo.correo_electronico
    )
    modelo.fecha_nacimiento = datetime.strptime(
        datos.get("fecha_nacimiento", modelo.fecha_nacimiento), "%Y-%m-%d"
    )

    rol_id = datos.get("rol_id")
    if rol_id:
        rol = Rol.query.get(rol_id)
        if rol:
            modelo.rol = rol
        else:
            return jsonify({"mensaje": "Rol no encontrado"}), 404

    # Actualizar páginas
    if "paginas_habilitadas" in datos:
        # Eliminar relaciones existentes
        modelo.paginas.clear()
        # Agregar nuevas relaciones
        for nombre_pagina in datos["paginas_habilitadas"]:
            pagina = Pagina.query.filter_by(nombre=nombre_pagina).first()
            if pagina:
                modelo.paginas.append(pagina)

    db.session.commit()
    return jsonify({"mensaje": "Usuario actualizado con éxito."})


@app.route("/ganancias", methods=["POST"])
def liquidar_ganancias():
    datos = request.json
    nombre_usuario = datos["nombre_usuario"]
    modelo = Modelo.query.filter_by(nombre_usuario=nombre_usuario).first()
    if not modelo:
        return jsonify({"mensaje": "Modelo no encontrado"}), 404

    trm = obtener_trm()
    gran_total_cop = 0  # Gran total en COP
    detalles_paginas = []  # Lista para almacenar los detalles de cada página
    deducciones = 0
    detalles_deducibles = []

    # Determina el período actual y busca o crea el período correspondiente
    nombre_periodo, fecha_inicio, fecha_fin = obtener_periodo_actual()
    periodo = Periodo.query.filter_by(nombre=nombre_periodo).first()
    if not periodo:
        periodo = Periodo(
            nombre=nombre_periodo, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
        )
        db.session.add(periodo)
        db.session.flush()

    # Verifica si ya existe una ganancia para este modelo y período
    ganancia_existente = Ganancia.query.filter_by(
        modelo_id=modelo.id, periodo_id=periodo.id
    ).first()
    if ganancia_existente:
        return (
            jsonify(
                {
                    "mensaje": "Ya existe una ganancia registrada para este modelo y período"
                }
            ),
            400,
        )

    # Crea la nueva ganancia y asocia el período
    nueva_ganancia = Ganancia(
        trm=trm,
        total_cop=0,
        modelo_id=modelo.id,
        periodo_id=periodo.id,
        estado="Liquidado",
        porcentaje=0,  # Inicializa el porcentaje con 0, se actualizará más adelante
        ganancia_general_cop=0,  # Inicializa la ganancia del estudio con 0
    )
    db.session.add(nueva_ganancia)  # Agrega la nueva ganancia a la sesión
    db.session.flush()  # Asegúrate de que la nueva ganancia tenga un ID

    deducciones_activas = (
        0  # Inicializa una variable para sumar solo las deducciones activas
    )

    for deducible in modelo.deducibles:
        if deducible.quincenas_restantes > 0:
            deducible.quincenas_restantes -= 1  # Disminuye las quincenas restantes
            deducible.estado = (
                "Activo"  # El deducible está activo y aún se están realizando pagos
            )
            deducible.valor_pagado = (
                deducible.plazo - deducible.quincenas_restantes
            ) * deducible.valor_quincenal
            deducible.valor_restante = deducible.valor_total - deducible.valor_pagado

            deducciones_activas += (
                deducible.valor_quincenal
            )  # Suma solo las deducciones activas

            detalles_deducibles.append(
                {
                    "concepto": deducible.concepto,
                    "valor_quincenal": deducible.valor_quincenal,
                    "quincenas_restantes": deducible.quincenas_restantes,
                    "estado": deducible.estado,  # Incluye el estado del deducible en los detalles
                }
            )

        else:
            deducible.estado = "Pagado"

    db.session.commit()

    # Utiliza la variable deducciones_activas en lugar de deducciones para los cálculos y la respuesta JSON

    total_tokens = 0  # Total de tokens generados por la modelo
    ganancias_por_pagina = []  # Lista para almacenar las ganancias por página
    for pagina in datos["paginas"]:
        pagina_nombre = pagina["nombre"]
        valor = pagina["valor"]

        if pagina_nombre == "Streamate":
            tokens = valor / 0.05
        else:
            tokens = valor

        total_tokens += tokens  # Acumula los tokens generados

        pagina_obj = Pagina.query.filter_by(nombre=pagina_nombre).first()
        if not pagina_obj:
            pagina_obj = Pagina(nombre=pagina_nombre)
            db.session.add(pagina_obj)
            db.session.flush()

        nueva_ganancia_por_pagina = GananciaPorPagina(
            tokens=tokens,
            total_cop=0,  # Se actualizará después de calcular el porcentaje
            ganancia_estudio_cop=0,  # Inicializa la ganancia del estudio por página con 0
            ganancia_id=nueva_ganancia.id,
            pagina_id=pagina_obj.id,
        )
        db.session.add(nueva_ganancia_por_pagina)
        ganancias_por_pagina.append(nueva_ganancia_por_pagina)

    # Determina el porcentaje según la cantidad total de tokens y la exclusividad
    if modelo.exclusividad:
        if total_tokens <= 29999:
            porcentaje = 0.60
        elif total_tokens <= 40000:
            porcentaje = 0.65
        else:
            porcentaje = min(0.65 + (total_tokens - 40000) // 4000 * 0.01, 0.70)
    else:
        if total_tokens < 20000:
            porcentaje = 0.50
        elif total_tokens < 26000:
            porcentaje = 0.55
        elif total_tokens < 31000:
            porcentaje = 0.60
        elif total_tokens < 36000:
            porcentaje = 0.65
        else:
            porcentaje = min(0.65 + (total_tokens - 36000) // 4000 * 0.01, 0.70)

    porcentaje_estudio = 1 - porcentaje  # Porcentaje de ganancia del estudio

    # Actualiza el porcentaje en la nueva ganancia
    nueva_ganancia.porcentaje = porcentaje

    # Actualiza el total en COP, la ganancia del estudio por página y los detalles de cada página con el porcentaje correcto
    for ganancia_pagina in ganancias_por_pagina:
        tokens = ganancia_pagina.tokens
        total_usd = tokens * 0.05  # Total en USD de los tokens generados
        total_cop_modelo = round(
            total_usd * porcentaje * trm
        )  # Total en COP pagado a la modelo
        total_cop_estudio = round(
            total_usd * porcentaje_estudio * trm
        )  # Total en COP de la ganancia del estudio
        gran_total_cop += total_cop_modelo
        ganancia_pagina.total_cop = total_cop_modelo
        ganancia_pagina.ganancia_estudio_cop = (
            total_cop_estudio  # Actualiza la ganancia del estudio por página
        )

        # Añade los detalles de la página a la lista
    detalles_paginas.append(
        {
            "nombre_pagina": ganancia_pagina.pagina.nombre,
            "tokens": tokens,
            "total_cop_modelo": total_cop_modelo,
            "ganancia_estudio_cop": total_cop_estudio,  # Incluye la ganancia del estudio por página en los detalles
        }
    )

    # Calcula la ganancia general del estudio
    # Calcula la ganancia general del estudio
    ganancia_general_cop = sum([gp.ganancia_estudio_cop for gp in ganancias_por_pagina])
    nueva_ganancia.ganancia_general_cop = (
        ganancia_general_cop  # Actualiza la ganancia general del estudio
    )

    gran_total_cop -= deducciones_activas

    impuesto = round(gran_total_cop * 4 / 1000)  # Calcula el 4% del total
    gran_total_cop -= impuesto  # Resta el descuento del total

    nueva_ganancia.total_cop = round(gran_total_cop)  # Redondea el gran total
    nueva_ganancia.estado = "Liquidado"
    db.session.commit()

    # Incluye los detalles de las páginas y la ganancia del estudio en la respuesta
    return jsonify(
        {
            "mensaje": "Ganancias liquidadas",
            "periodo": {
                "nombre": periodo.nombre,
                "fecha_inicio": periodo.fecha_inicio.strftime("%Y-%m-%d"),
                "fecha_fin": periodo.fecha_fin.strftime("%Y-%m-%d"),
            },
            "gran_total_cop": gran_total_cop,
            "detalles_deducibles": detalles_deducibles,
            "detalles_paginas": detalles_paginas,
            "porcentaje": porcentaje,
            "ganancia_estudio_general_cop": ganancia_general_cop,  # Incluye la ganancia general del estudio en la respuesta
        }
    )


@app.route(
    "/ganancias/usuario/<nombre_usuario>/periodo/<nombre_periodo>", methods=["GET"]
)
def obtener_ganancias_por_usuario_y_periodo(nombre_usuario, nombre_periodo):
    modelo = Modelo.query.filter_by(nombre_usuario=nombre_usuario).first()
    if modelo is None:
        return jsonify({"mensaje": "Modelo no encontrado"}), 404

    periodo = Periodo.query.filter_by(nombre=nombre_periodo).first()
    if periodo is None:
        return jsonify({"mensaje": "Período no encontrado"}), 404

    ganancia = (
        Ganancia.query.filter_by(modelo_id=modelo.id, periodo_id=periodo.id)
        .order_by(Ganancia.id.desc())
        .first()
    )
    if not ganancia:
        return (
            jsonify(
                {"mensaje": "No se encontraron ganancias para el período especificado"}
            ),
            404,
        )

    detalles_paginas = [
        {
            "nombre_pagina": ganancia_por_pagina.pagina.nombre,
            "tokens": ganancia_por_pagina.tokens,
            "total_cop": ganancia_por_pagina.total_cop,
        }
        for ganancia_por_pagina in ganancia.ganancias_por_pagina
    ]

    restante_deducibles = sum(
        deducible.valor_restante for deducible in modelo.deducibles
    )

    detalles_deducibles = [
        {
            "concepto": deducible.concepto,
            "valor_total": deducible.valor_total,
            "valor_quincenal": deducible.valor_quincenal,
            "quincenas_restantes": deducible.quincenas_restantes,
            "plazo": deducible.plazo,
            "tasa": deducible.tasa,
            "fecha_inicio": deducible.fecha_inicio.strftime("%Y-%m-%d"),
            "fecha_fin": deducible.fecha_fin.strftime("%Y-%m-%d"),
            "estado": deducible.estado,
            "valor_pagado": deducible.valor_pagado,
            "valor_restante": deducible.valor_restante,
        }
        for deducible in modelo.deducibles
    ]

    total_deducible = 0
    for deducible in modelo.deducibles:
        if deducible.estado != "Pagado":
            total_deducible += deducible.valor_quincenal

    return jsonify(
        {
            "id": ganancia.id,
            "nombre_usuario": nombre_usuario,
            "nombre_periodo": nombre_periodo,
            "trm": ganancia.trm,
            "gran_total_cop": ganancia.total_cop,
            "deducciones": sum(d["valor_quincenal"] for d in detalles_deducibles),
            "detalles_deducibles": detalles_deducibles,
            "detalles_paginas": detalles_paginas,
            "estado": ganancia.estado,
            "porcentaje": ganancia.porcentaje,
            "restante_deducibles": restante_deducibles,
            "total_deducibles": total_deducible,
        }
    )


@app.route("/modelos/<nombre_usuario>/creardeducible", methods=["POST"])
def agregar_deducible(nombre_usuario):
    modelo = Modelo.query.filter_by(nombre_usuario=nombre_usuario).first()
    if not modelo:
        return jsonify({"mensaje": "Modelo no encontrado"}), 404

    datos = request.json

    tasa_quincenal = datos["tasa"] / 2
    valor_quincenal = datos["valor_total"] / datos["plazo"] * (1 + tasa_quincenal)

    nuevo_deducible = Deducible(
        concepto=datos["concepto"],
        valor_sin_interes=datos["valor_total"],
        valor_total=datos["valor_total"] * (1 + tasa_quincenal),
        plazo=datos["plazo"],
        tasa=tasa_quincenal,
        valor_quincenal=valor_quincenal,
        quincenas_restantes=datos["plazo"],
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(days=datos["plazo"] * 15),
        valor_pagado=0,
        valor_restante=datos["valor_total"] * (1 + tasa_quincenal),
        modelo_id=modelo.id,
        estado="Activo",
    )
    db.session.add(nuevo_deducible)
    db.session.commit()

    return jsonify({"mensaje": "Deducible agregado con éxito"})


@app.route("/roles", methods=["GET"])
def obtener_roles():
    roles = Rol.query.all()
    lista_roles = [{"id": rol.id, "nombre": rol.nombre} for rol in roles]
    return jsonify(lista_roles)


@app.route("/paginas", methods=["GET"])
def obtener_paginas():
    paginas = Pagina.query.all()
    lista_paginas = [{"id": pagina.id, "nombre": pagina.nombre} for pagina in paginas]
    return jsonify(lista_paginas)


@app.route("/ganancias/<int:ganancia_id>/pagar", methods=["POST"])
def pagar_ganancia(ganancia_id):
    ganancia = Ganancia.query.get_or_404(ganancia_id)
    ganancia.estado = "Pagado"
    db.session.commit()
    return jsonify({"mensaje": "Ganancia pagada con éxito"})


@app.route("/periodoactual", methods=["GET"])
def obtener_periodo_actual_endpoint():
    nombre_periodo, fecha_inicio, fecha_fin = obtener_periodo_actual()
    return jsonify(
        {
            "nombre": nombre_periodo,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea las tablas de la base de datos si no existen
        inicializar_paginas()  # Inicializa las páginas preestablecidas
        inicializar_roles()
    app.run(debug=False)
