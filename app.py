from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from models import (
    db,
    Modelo,
    Ganancia,
    Pagina,
    GananciaPorPagina,
    PaginaHabilitada,
    Periodo,
    Deducible,
)
from datetime import datetime, timedelta

from config import Config

import requests


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


from datetime import datetime, date


def obtener_periodo_actual():
    hoy = datetime.today().date()
    mes = hoy.strftime(
        "%b"
    ).upper()  # Obtiene el mes en formato abreviado y en mayúsculas
    año = hoy.year
    if hoy.day <= 15:
        nombre_periodo = f"{año}-{mes}-1"
        fecha_inicio = date(hoy.year, hoy.month, 1)
        fecha_fin = date(hoy.year, hoy.month, 15)
    else:
        nombre_periodo = f"{año}-{mes}-2"
        fecha_inicio = date(hoy.year, hoy.month, 16)
        ultimo_dia = (hoy.replace(day=28) + timedelta(days=4)).replace(
            day=1
        ) - timedelta(days=1)
        fecha_fin = date(hoy.year, hoy.month, ultimo_dia.day)
    return nombre_periodo, fecha_inicio, fecha_fin


def obtener_trm():
    url = "https://www.datos.gov.co/resource/32sa-8pi3.json"
    response = requests.get(url)
    data = response.json()
    valor = float(data[0]["valor"])
    print(valor)
    valor = valor - 90
    print(valor, "MENOS 80 PESOS POR DOLAR")
    return valor


@app.route("/modelos", methods=["POST"])
def crear_modelo():
    datos = request.json
    nuevo_modelo = Modelo(
        nombres=datos["nombres"],
        apellidos=datos["apellidos"],
        tipo_documento=datos["tipo_documento"],
        numero_documento=datos["numero_documento"],
        nombre_usuario=datos["nombre_usuario"],
    )
    db.session.add(nuevo_modelo)
    db.session.flush()  # Para obtener el ID del modelo recién creado

    for pagina_nombre in datos["paginas_habilitadas"]:
        pagina = Pagina.query.filter_by(nombre=pagina_nombre).first()
        if pagina:
            nueva_pagina_habilitada = PaginaHabilitada(
                modelo_id=nuevo_modelo.id, pagina_id=pagina.id
            )
            db.session.add(nueva_pagina_habilitada)

    db.session.commit()
    return jsonify({"mensaje": "Modelo creado con éxito"})


@app.route("/modelos", methods=["GET"])
def obtener_modelos():
    try:
        # Consulta todos los modelos
        modelos = Modelo.query.all()
        # Serializa los datos para enviarlos como JSON
        lista_modelos = [
            {
                "id": modelo.id,
                "nombres": modelo.nombres,
                "apellidos": modelo.apellidos,
                "tipo_documento": modelo.tipo_documento,
                "numero_documento": modelo.numero_documento,
                "nombre_usuario": modelo.nombre_usuario,
            }
            for modelo in modelos
        ]
        print(lista_modelos)
        return jsonify(lista_modelos)
    except Exception as e:
        # En caso de error, envía una respuesta de error
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

    db.session.commit()
    return jsonify({"mensaje": "Modelo actualizado con éxito"})


@app.route("/modelos/<int:modelo_id>", methods=["DELETE"])
def eliminar_modelo(modelo_id):
    modelo = Modelo.query.get_or_404(modelo_id)

    # Verifica si el modelo tiene deducibles pendientes
    deducibles_pendientes = Deducible.query.filter(
        Deducible.modelo_id == modelo.id, Deducible.quincenas_restantes > 0
    ).first()
    if deducibles_pendientes:
        return (
            jsonify(
                {
                    "mensaje": "El modelo tiene deducibles pendientes y no puede ser eliminado"
                }
            ),
            400,
        )

    # Elimina las ganancias y páginas habilitadas asociadas con el modelo
    Ganancia.query.filter_by(modelo_id=modelo.id).delete()
    PaginaHabilitada.query.filter_by(modelo_id=modelo.id).delete()

    db.session.delete(modelo)
    db.session.commit()
    return jsonify({"mensaje": "Modelo y registros asociados eliminados con éxito"})


@app.route("/modelos/<int:modelo_id>", methods=["GET"])
def obtener_modelo(modelo_id):
    modelo = Modelo.query.get_or_404(modelo_id)
    detalles_modelo = {
        "id": modelo.id,
        "nombres": modelo.nombres,
        "apellidos": modelo.apellidos,
        "tipo_documento": modelo.tipo_documento,
        "numero_documento": modelo.numero_documento,
        "nombre_usuario": modelo.nombre_usuario,
    }
    return jsonify(detalles_modelo)


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
        trm=trm, total_cop=0, modelo_id=modelo.id, periodo_id=periodo.id
    )
    db.session.add(nueva_ganancia)
    db.session.flush()

    for deducible in modelo.deducibles:
        if deducible.quincenas_restantes > 0:
            deducciones += deducible.valor_quincenal
            deducible.quincenas_restantes -= 1  # Disminuye las quincenas restantes
            detalles_deducibles.append(
                {
                    "concepto": deducible.concepto,
                    "valor_quincenal": deducible.valor_quincenal,
                    "quincenas_restantes": deducible.quincenas_restantes,
                }
            )
        db.session.commit()

    for pagina in datos["paginas"]:
        pagina_nombre = pagina["nombre"]
        valor = pagina["valor"]

        if pagina_nombre == "Streamate":
            tokens = valor / 0.05
        else:
            tokens = valor

        total_usd = tokens * 0.05 * 0.6
        total_cop = round(total_usd * trm)  # Redondea el total en COP
        gran_total_cop += total_cop

        pagina_obj = Pagina.query.filter_by(nombre=pagina_nombre).first()
        if not pagina_obj:
            pagina_obj = Pagina(nombre=pagina_nombre)
            db.session.add(pagina_obj)
            db.session.flush()

        nueva_ganancia_por_pagina = GananciaPorPagina(
            tokens=tokens,
            total_cop=total_cop,
            ganancia_id=nueva_ganancia.id,
            pagina_id=pagina_obj.id,
        )
        db.session.add(nueva_ganancia_por_pagina)

        # Añade los detalles de la página a la lista
        detalles_paginas.append(
            {"nombre_pagina": pagina_nombre, "tokens": tokens, "total_cop": total_cop}
        )
    print(gran_total_cop, "GRAN TOTAL COP")
    gran_total_cop -= deducciones

    impuesto = round(gran_total_cop * 4 / 1000)  # Calcula el 4% del total
    gran_total_cop -= impuesto  # Resta el descuento del total

    nueva_ganancia.total_cop = round(gran_total_cop)  # Redondea el gran total
    db.session.commit()

    # Incluye los detalles de las páginas en la respuesta
    return jsonify(
        {
            "mensaje": "Ganancias liquidadas",
            "periodo": {
                "nombre": periodo.nombre,
                "fecha_inicio": periodo.fecha_inicio.strftime("%Y-%m-%d"),
                "fecha_fin": periodo.fecha_fin.strftime("%Y-%m-%d"),
            },
            "gran_total_cop": gran_total_cop,
            "deducciones": deducciones,
            "detalles_deducibles": detalles_deducibles,
            "detalles_paginas": detalles_paginas,
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

    ganancias = Ganancia.query.filter_by(
        modelo_id=modelo.id, periodo_id=periodo.id
    ).all()
    if not ganancias:
        return (
            jsonify(
                {"mensaje": "No se encontraron ganancias para el período especificado"}
            ),
            404,
        )

    # ULTIMA GANANCIA
    ganancia = ganancias[-1]

    total_cop = ganancia.total_cop
    return jsonify(
        {
            "nombre_usuario": nombre_usuario,
            "nombre_periodo": nombre_periodo,
            "total_cop": total_cop,
        }
    )


@app.route("/modelos/<nombre_usuario>/deducibles", methods=["POST"])
def agregar_deducible(nombre_usuario):
    modelo = Modelo.query.filter_by(nombre_usuario=nombre_usuario).first()
    if not modelo:
        return jsonify({"mensaje": "Modelo no encontrado"}), 404

    datos = request.json
    nuevo_deducible = Deducible(
        concepto=datos["concepto"],
        valor_total=datos["valor_total"],
        valor_quincenal=datos["valor_quincenal"],
        plazo=datos["plazo"],
        quincenas_restantes=datos["plazo"],
        modelo_id=modelo.id,
    )
    db.session.add(nuevo_deducible)
    db.session.commit()

    return jsonify({"mensaje": "Deducible agregado con éxito"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea las tablas de la base de datos si no existen
        inicializar_paginas()  # Inicializa las páginas preestablecidas
    app.run(debug=True)
