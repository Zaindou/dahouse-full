from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import func, distinct, extract, or_, case, and_
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS
from flask_migrate import Migrate
from models import (
    db,
    Modelo,
    Ganancia,
    Pagina,
    GananciaPorPagina,
    Periodo,
    Deducible,
    Rol,
    MetaPeriodo,
    PagoDeduccion,
)
from datetime import datetime, timedelta, date
import pytz

from config import Config
from dotenv import load_dotenv

from flask import render_template
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime
from flask_mail import Mail, Message

from pdf_nomina import generar_pdf_desprendible
from sms_send import send_sms
from tool_db import (
    inicializar_paginas,
    inicializar_roles,
    obtener_periodo_actual,
    calcular_nuevo_periodo,
    get_stats_por_periodo,
    get_deducciones_por_periodo,
    get_tokens_por_modelo_pagina,
    calculate_trends,
    MESES_MAP,
)

from modules import register_blueprints
import requests
import environ
import os

env = environ.Env()
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)
app.jinja_env.globals.update(int=int)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
mail = Mail(app)


@app.template_filter("currency")
def currency_format(value, currency_symbol="$", decimals=0):
    """
    Formato de moneda con manejo de múltiples casos.

    Args:
        value: Valor a formatear (str, int, float o None)
        currency_symbol: Símbolo de moneda (default: "$")
        decimals: Número de decimales a mostrar (default: 0)

    Returns:
        str: Valor formateado como moneda
    """
    try:
        # Manejar casos de valor None o vacío
        if value is None or value == "":
            return "-"

        # Convertir a float y manejar strings que puedan contener comas
        if isinstance(value, str):
            value = float(value.replace(",", ""))
        else:
            value = float(value)

        # Manejar valores negativos
        is_negative = value < 0
        value = abs(value)

        # Formatear el número con los decimales especificados
        if decimals > 0:
            formatted = f"{value:,.{decimals}f}"
        else:
            formatted = f"{value:,.0f}"

        # Reemplazar punto por coma para separador decimal
        # y coma por punto para separador de miles
        formatted = formatted.replace(",", "temp")
        formatted = formatted.replace(".", ",")
        formatted = formatted.replace("temp", ".")

        # Agregar símbolo de moneda y signo negativo si corresponde
        result = f"{currency_symbol}{formatted}"
        if is_negative:
            result = f"-{result}"

        return result

    except (ValueError, TypeError) as e:
        # Log del error para debugging
        print(f"Error formateando valor {value}: {str(e)}")
        return str(value)


app.jinja_env.filters["currency"] = currency_format


def obtener_trm():
    url = os.environ.get("TRM_URL")
    response = requests.get(url)
    data = response.json()
    valor = float(data[0]["valor"])
    valor = valor - float(os.environ.get("TRM_ADICIONAL"))
    return valor


@app.route("/", methods=["GET"])
def index():
    return "API: V1.4.0 - FRONTEND: V1.3.1 -- DAHOUSE"


@app.route("/periodos/crear-nuevo", methods=["POST"])
def crear_nuevo_periodo_endpoint():
    try:
        # Obtener el último período registrado
        ultimo_periodo = Periodo.query.order_by(Periodo.fecha_fin.desc()).first()

        if not ultimo_periodo:
            return (
                jsonify(
                    {
                        "error": "No hay períodos registrados. Inicializa los datos primero."
                    }
                ),
                400,
            )

        # Calcular la fecha actual y el próximo día tras el último período
        fecha_actual = datetime.now().date()
        # fecha_actual = datetime(2024, 12, 13).date()
        fecha_fin_ultimo_periodo = (
            ultimo_periodo.fecha_fin
        )  # Asumimos que fecha_fin ya es datetime.date

        # Verificar si es necesario crear un nuevo período
        if fecha_actual > fecha_fin_ultimo_periodo:
            nuevo_periodo = calcular_nuevo_periodo()

            if nuevo_periodo:
                # Registrar el nuevo período en la base de datos
                nuevo_periodo_db = Periodo(
                    nombre=nuevo_periodo["nombre"],
                    fecha_inicio=nuevo_periodo["fecha_inicio"],
                    fecha_fin=nuevo_periodo["fecha_fin"],
                )
                db.session.add(nuevo_periodo_db)
                db.session.commit()
                return (
                    jsonify(
                        {"message": "Nuevo período creado", "periodo": nuevo_periodo}
                    ),
                    201,
                )
            else:
                return jsonify({"error": "No se pudo calcular el nuevo período"}), 500

        return jsonify({"message": "No es necesario crear un nuevo período aún"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear un nuevo período: {str(e)}"}), 500


@app.route("/login", methods=["POST"])
def login():
    datos = request.json
    modelo = Modelo.query.filter_by(nombre_usuario=datos["nombre_usuario"]).first()
    rol = Rol.query.filter_by(id=modelo.rol_id).first()

    if modelo not in Modelo.query.all():
        return jsonify({"mensaje": "Usario no encontrado."}), 404

    if not modelo or not check_password_hash(modelo.password, datos["password"]):
        return jsonify({"mensaje": "Credenciales incorrectas"}), 401

    # Si la contraseña es correcta, generar y devolver el token
    access_token = create_access_token(identity={"id": modelo.id, "rol": rol.nombre})
    return jsonify(access_token=access_token, port="5900"), 200


@app.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    current_user = get_jwt_identity()  # Obtiene el ID y el rol del usuario del token
    modelo = Modelo.query.get(current_user["id"])

    if modelo:
        return (
            jsonify(
                {
                    "id": modelo.id,
                    "tipo_documento": modelo.tipo_documento,
                    "numero_documento": modelo.numero_documento,
                    "nombres": modelo.nombres,
                    "apellidos": modelo.apellidos,
                    "correo_electronico": modelo.correo_electronico,
                    "nombre_usuario": modelo.nombre_usuario,
                    "rol": modelo.rol.nombre,  # Asume que tienes una relación con la tabla de roles
                    "banco": modelo.banco,
                    "numero_cuenta": modelo.numero_cuenta,
                    "habilitado": modelo.habilitado,
                    "exclusividad": modelo.exclusividad,
                    "jornada": modelo.jornada,
                    "fecha_registro": modelo.fecha_registro,
                    "paginas_habilitadas": [pagina.nombre for pagina in modelo.paginas],
                }
            ),
            200,
        )
    return jsonify({"mensaje": "Usuario no encontrado"}), 404


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token)


@app.route("/historial-pagos/<int:modelo_id>", methods=["GET"])
def obtener_historial_pagos(modelo_id):
    modelo = Modelo.query.get_or_404(modelo_id)
    ganancias = (
        Ganancia.query.filter_by(modelo_id=modelo.id).order_by(Ganancia.id.desc()).all()
    )

    historial = []
    historial.append(
        {
            "id": modelo.id,
            "nombres": modelo.nombres,
            "apellidos": modelo.apellidos,
            "tipo_documento": modelo.tipo_documento,
            "numero_documento": modelo.numero_documento,
            "nombre_usuario": modelo.nombre_usuario,
            "correo_electronico": modelo.correo_electronico,
            "numero_celular": modelo.numero_celular,
            "numero_cuenta": modelo.numero_cuenta,
            "banco": modelo.banco,
            "rol": modelo.rol.nombre,
            "habilitado": modelo.habilitado,
        }
    )
    for ganancia in ganancias:
        # Detalles de las ganancias por página
        detalles_paginas = [
            {
                "nombre_pagina": ganancia_pagina.pagina.nombre,
                "tokens": ganancia_pagina.tokens,
                "total_cop": ganancia_pagina.total_cop,
                "ganancia_estudio_cop": ganancia_pagina.ganancia_estudio_cop,
            }
            for ganancia_pagina in ganancia.ganancias_por_pagina
        ]

        # Deducciones asociadas al pago
        deducciones_asociadas = [
            {
                "deduccion_id": pago_deduccion.deduccion.id,
                "concepto": pago_deduccion.deduccion.concepto,
                "plazo": pago_deduccion.deduccion.plazo,
                "cuotas_restantes": pago_deduccion.cuotas_restantes,
                "valor_total": pago_deduccion.deduccion.valor_total,
                "valor_quincenal": pago_deduccion.deduccion.valor_quincenal,
                "monto_pagado": pago_deduccion.monto_pagado,
                "estado": pago_deduccion.deduccion.estado,
            }
            for pago_deduccion in ganancia.deducciones_asociadas
        ]

        # Construir la entrada del historial
        historial.append(
            {
                "ganancia_id": ganancia.id,
                "periodo": {
                    "nombre": ganancia.periodo.nombre,
                    "fecha_inicio": ganancia.periodo.fecha_inicio.strftime("%Y-%m-%d"),
                    "fecha_fin": ganancia.periodo.fecha_fin.strftime("%Y-%m-%d"),
                },
                "trm": ganancia.trm,
                "total_cop": ganancia.total_cop,
                "porcentaje": ganancia.porcentaje,
                "ganancia_estudio_general_cop": ganancia.ganancia_general_cop,
                "detalles_paginas": detalles_paginas,
                "deducciones_asociadas": deducciones_asociadas,
            }
        )

    return jsonify(historial)


# TODO Terminar este fuking endpoint que ya me esta sacando canas.
@app.route("/estadisticas-negocio", methods=["GET"])
def obtener_estadisticas_negocio():
    try:
        # Obtener datos básicos
        stats_por_periodo = get_stats_por_periodo()
        deducciones_por_periodo = get_deducciones_por_periodo()
        tokens_por_modelo_pagina = get_tokens_por_modelo_pagina()

        # Procesar deducciones por período
        deducciones_dict = {}
        for item in deducciones_por_periodo:
            deducciones_dict.setdefault(item.periodo, []).append(
                {
                    "concepto": item.concepto,
                    "total_deducciones": float(item.total_deducciones or 0),
                }
            )

        # Procesar tokens por modelo y página agrupados por período
        tokens_por_modelo_pagina_dict = {}
        tokens_totales_por_pagina_periodo = {}
        tokens_totales_por_modelo = {}
        for item in tokens_por_modelo_pagina:
            periodo = item.periodo
            modelo = item.modelo_usuario
            pagina = item.pagina
            tokens = int(item.total_tokens or 0)

            if periodo not in tokens_por_modelo_pagina_dict:
                tokens_por_modelo_pagina_dict[periodo] = {}

            if modelo not in tokens_por_modelo_pagina_dict[periodo]:
                tokens_por_modelo_pagina_dict[periodo][modelo] = {"total_tokens": 0}

            tokens_por_modelo_pagina_dict[periodo][modelo][pagina] = tokens
            tokens_por_modelo_pagina_dict[periodo][modelo]["total_tokens"] += tokens

            # Consolidar tokens por página en cada período
            if periodo not in tokens_totales_por_pagina_periodo:
                tokens_totales_por_pagina_periodo[periodo] = {}

            if pagina not in tokens_totales_por_pagina_periodo[periodo]:
                tokens_totales_por_pagina_periodo[periodo][pagina] = 0

            tokens_totales_por_pagina_periodo[periodo][pagina] += tokens

            # Consolidar tokens totales por modelo a nivel general
            if modelo not in tokens_totales_por_modelo:
                tokens_totales_por_modelo[modelo] = 0

            tokens_totales_por_modelo[modelo] += tokens

        # Agrupar estadísticas por mes y calcular tendencias
        estadisticas_por_mes = {}
        tokens_totales_por_modelo_mes = {}
        for stat in stats_por_periodo:
            periodo = stat.periodo
            año, mes = periodo.split("-")[:2]
            mes_año = f"{año}-{mes}"

            if mes_año not in estadisticas_por_mes:
                estadisticas_por_mes[mes_año] = {
                    "ganancia_modelos": 0,
                    "ganancia_estudio": 0,
                    "ganancia_bruta": 0,
                    "total_tokens": 0,
                    "tokens_totales_por_pagina": {},  # Consolidar tokens por página
                    "periodos": [],
                }

            data = estadisticas_por_mes[mes_año]
            data["ganancia_modelos"] += float(stat.ganancia_modelos or 0)
            data["ganancia_estudio"] += float(stat.ganancia_estudio or 0)
            data["ganancia_bruta"] += float(stat.ganancia_modelos or 0) + float(
                stat.ganancia_estudio or 0
            )
            data["total_tokens"] += int(stat.total_tokens or 0)
            data["periodos"].append(periodo)

            # Consolidar tokens por página a nivel de mes
            tokens_por_pagina = tokens_por_modelo_pagina_dict.get(periodo, {})
            for modelo, paginas in tokens_por_pagina.items():
                for pagina, tokens in paginas.items():
                    if pagina == "total_tokens":
                        continue
                    if pagina not in data["tokens_totales_por_pagina"]:
                        data["tokens_totales_por_pagina"][pagina] = 0
                    data["tokens_totales_por_pagina"][pagina] += tokens

                # Consolidar tokens totales por modelo a nivel de mes
                if modelo not in tokens_totales_por_modelo_mes:
                    tokens_totales_por_modelo_mes[modelo] = {}
                if mes_año not in tokens_totales_por_modelo_mes[modelo]:
                    tokens_totales_por_modelo_mes[modelo][mes_año] = 0
                tokens_totales_por_modelo_mes[modelo][mes_año] += paginas.get(
                    "total_tokens", 0
                )

        estadisticas_con_tendencia = calculate_trends(
            [{"mes_año": mes, **data} for mes, data in estadisticas_por_mes.items()]
        )

        # Generar mejores modelos
        mejores_modelos = {
            "mejor_modelo_año": sorted(
                [
                    {"modelo": modelo, "tokens": tokens}
                    for modelo, tokens in tokens_totales_por_modelo.items()
                ],
                key=lambda x: x["tokens"],
                reverse=True,
            ),
            "mejor_modelo_por_mes": {
                mes: sorted(
                    [
                        {"modelo": modelo, "tokens": tokens[mes]}
                        for modelo, tokens in tokens_totales_por_modelo_mes.items()
                        if mes in tokens
                    ],
                    key=lambda x: x["tokens"],
                    reverse=True,
                )
                for mes in sorted(estadisticas_por_mes.keys())
            },
            "mejor_modelo_por_periodo": {
                periodo: sorted(
                    [
                        {"modelo": modelo, "tokens": datos["total_tokens"]}
                        for modelo, datos in modelos.items()
                    ],
                    key=lambda x: x["tokens"],
                    reverse=True,
                )
                for periodo, modelos in sorted(tokens_por_modelo_pagina_dict.items())
            },
        }

        # Ordenar las estadísticas por mes
        estadisticas_con_tendencia = sorted(
            estadisticas_con_tendencia,
            key=lambda x: (
                int(x["mes_año"].split("-")[0]),  # Año
                MESES_MAP[x["mes_año"].split("-")[1]],  # Mes
            ),
        )

        # Ordenar estadísticas por período
        estadisticas_por_periodo = sorted(
            [
                {
                    "periodo": stat.periodo,
                    "ganancia_modelos": float(stat.ganancia_modelos or 0),
                    "ganancia_estudio": float(stat.ganancia_estudio or 0),
                    "ganancia_bruta": float(stat.ganancia_modelos or 0)
                    + float(stat.ganancia_estudio or 0),
                    "total_tokens": int(stat.total_tokens or 0),
                    "deducciones": deducciones_dict.get(stat.periodo, []),
                    "tokens_por_modelo_pagina": tokens_por_modelo_pagina_dict.get(
                        stat.periodo, {}
                    ),
                    "tokens_totales_por_pagina": tokens_totales_por_pagina_periodo.get(
                        stat.periodo, {}
                    ),
                }
                for stat in stats_por_periodo
            ],
            key=lambda x: (
                int(x["periodo"].split("-")[0]),  # Año
                MESES_MAP[x["periodo"].split("-")[1]],  # Mes
                int(x["periodo"].split("-")[2]),  # Parte del período
            ),
        )

        # Formatear respuesta final
        response = {
            "estadisticas_por_periodo": estadisticas_por_periodo,
            "estadisticas_por_mes": estadisticas_con_tendencia,
            "mejores_modelos": mejores_modelos,
        }
        return jsonify(response), 200

    except SQLAlchemyError as e:
        return (
            jsonify({"error": "Error al obtener estadísticas", "details": str(e)}),
            500,
        )


@app.route("/financiero", methods=["GET"])
def financiero():
    trm_actual = obtener_trm() + float(os.environ.get("TRM_ADICIONAL"))
    periodo_actual = obtener_periodo_actual()

    datos_financieros = {
        "trm_liquidacion": obtener_trm(),
        "trm_actual": trm_actual,
        "periodo_actual": periodo_actual,
    }
    return jsonify(datos_financieros)


@app.route("/modelos", methods=["POST"])
def crear_modelo():
    datos = request.json
    hashed_password = generate_password_hash(datos["password"], method="pbkdf2:sha256")

    nuevo_modelo = Modelo(
        tipo_documento=datos["tipo_documento"],
        numero_documento=datos["numero_documento"],
        nombres=datos["nombres"],
        apellidos=datos["apellidos"],
        fecha_nacimiento=datetime.strptime(datos["fecha_nacimiento"], "%Y-%m-%d"),
        correo_electronico=datos["correo_electronico"],
        numero_celular=datos["numero_celular"],
        nombre_usuario=datos["nombre_usuario"],
        rol_id=datos["rol_id"],
        banco=datos["banco"],
        numero_cuenta=datos["numero_cuenta"],
        password=hashed_password,
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
                    "numero_celular": modelo.numero_celular,
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
                            "fecha_inicio": deducible.fecha_inicio.strftime("%Y-%m-%d"),
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
    hashed_password = generate_password_hash(
        datos.get("password", modelo.password), method="pbkdf2:sha256"
    )

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
    modelo.numero_celular = datos.get("numero_celular", modelo.numero_celular)
    modelo.fecha_nacimiento = datetime.strptime(
        datos.get("fecha_nacimiento", modelo.fecha_nacimiento), "%Y-%m-%d"
    )
    modelo.password = hashed_password
    modelo.exclusividad = datos.get("exclusividad", modelo.exclusividad)

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
    deducciones_activas = (
        0  # Inicializa una variable para sumar solo las deducciones activas
    )
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
        porcentaje=0,
        ganancia_general_cop=0,
    )
    db.session.add(nueva_ganancia)  # Agrega la nueva ganancia a la sesión
    db.session.flush()

    # Procesar deducciones
    for deducible in modelo.deducibles:
        if deducible.quincenas_restantes > 0:
            deducible.quincenas_restantes -= 1  # Disminuye las quincenas restantes
            deducible.valor_pagado = (
                deducible.plazo - deducible.quincenas_restantes
            ) * deducible.valor_quincenal
            deducible.valor_restante = deducible.valor_total - deducible.valor_pagado
            # deducible.estado = (
            #     "Activo" if deducible.quincenas_restantes > 0 else "Pagado"
            # )

            # Añadir al total de deducciones activas
            deducciones_activas += deducible.valor_quincenal

            detalles_deducibles.append(
                {
                    "concepto": deducible.concepto,
                    "valor_quincenal": deducible.valor_quincenal,
                    "quincenas_restantes": deducible.quincenas_restantes,
                    # "estado": deducible.estado,
                }
            )

            # Registrar en la tabla intermedia PagoDeduccion
            pago_deduccion = PagoDeduccion(
                pago_id=nueva_ganancia.id,
                deduccion_id=deducible.id,
                monto_pagado=deducible.valor_quincenal,
                cuotas_restantes=deducible.quincenas_restantes,
            )
            db.session.add(pago_deduccion)

    # Procesar ganancias por página
    total_tokens = 0
    ganancias_por_pagina = []
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
            total_cop=0,
            ganancia_estudio_cop=0,
            ganancia_id=nueva_ganancia.id,
            pagina_id=pagina_obj.id,
        )
        db.session.add(nueva_ganancia_por_pagina)
        ganancias_por_pagina.append(nueva_ganancia_por_pagina)

    # Determina el porcentaje según la cantidad total de tokens y la exclusividad
    if modelo.exclusividad:
        if modelo.porcentaje_base == 0.7:
            porcentaje = 0.70
        elif modelo.porcentaje_base == 0.65:
            porcentaje = 0.65
        elif modelo.porcentaje_base == 0.55:
            if total_tokens <= 44200:
                porcentaje = 0.55
            elif total_tokens <= 72000:
                porcentaje = max(0.60, modelo.porcentaje_base)
            else:
                porcentaje = min(0.70 + (total_tokens - 72000) // 5000 * 0.01, 0.75)
        else:  # Para los que parten de 60%
            if total_tokens <= 72000:
                porcentaje = 0.60
            else:
                porcentaje = min(0.70 + (total_tokens - 72000) // 5000 * 0.01, 0.75)
    else:
        if total_tokens >= 61200:
            porcentaje = min(0.70 + (total_tokens - 61200) // 6000 * 0.01, 0.75)
        elif total_tokens >= 57000:
            porcentaje = 0.70
        elif total_tokens >= 51000:
            porcentaje = 0.60
        elif total_tokens >= 26000:
            porcentaje = 0.55
        else:
            porcentaje = 0.50

    porcentaje_estudio = 1 - porcentaje
    nueva_ganancia.porcentaje = porcentaje

    # Procesar detalles de las ganancias por página
    for ganancia_pagina in ganancias_por_pagina:
        tokens = ganancia_pagina.tokens
        total_usd = tokens * 0.05
        total_cop_modelo = round(total_usd * porcentaje * trm)
        total_cop_estudio = round(total_usd * porcentaje_estudio * trm)

        gran_total_cop += total_cop_modelo
        ganancia_pagina.total_cop = total_cop_modelo
        ganancia_pagina.ganancia_estudio_cop = total_cop_estudio

        detalles_paginas.append(
            {
                "nombre_pagina": ganancia_pagina.pagina.nombre,
                "tokens": tokens,
                "total_cop_modelo": total_cop_modelo,
                "ganancia_estudio_cop": total_cop_estudio,
            }
        )

    # Resta deducciones e impuestos
    gran_total_cop -= deducciones_activas
    impuesto = round(gran_total_cop * 4 / 1000)
    gran_total_cop -= impuesto

    nueva_ganancia.total_cop = round(gran_total_cop)
    nueva_ganancia.ganancia_general_cop = sum(
        gp.ganancia_estudio_cop for gp in ganancias_por_pagina
    )
    nueva_ganancia.estado = "Liquidado"
    db.session.commit()

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
            "ganancia_estudio_general_cop": nueva_ganancia.ganancia_general_cop,
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
            "total_cop": sum(d["total_cop"] for d in detalles_paginas),
        }
    )


@app.route("/modelos/<nombre_usuario>/creardeducible", methods=["POST"])
def agregar_deducible(nombre_usuario):
    modelo = Modelo.query.filter_by(nombre_usuario=nombre_usuario).first()
    if not modelo:
        return jsonify({"mensaje": "Modelo no encontrado"}), 404

    datos = request.json

    # Validación de datos de entrada
    campos_requeridos = ["concepto", "valor_total", "plazo", "tasa"]
    for campo in campos_requeridos:
        if campo not in datos:
            return jsonify({"mensaje": f"Falta el campo requerido: {campo}"}), 400

    if datos["valor_total"] <= 0 or datos["plazo"] <= 0 or datos["tasa"] < 0:
        return jsonify({"mensaje": "Los valores deben ser mayores que cero"}), 400

    # Conversión de la tasa a decimal si está en porcentaje
    tasa = datos["tasa"]
    if tasa > 1:  # Si está en porcentaje, convertir a decimal
        tasa = tasa / 100

    plazo = datos["plazo"]
    valor_total = datos["valor_total"]

    if tasa == 0:
        # Sin intereses, cuota simple
        cuota_quincenal = valor_total / plazo
        valor_total_con_interes = valor_total  # Sin incremento
    else:
        # Con intereses, usar la fórmula del sistema francés
        tasa_quincenal = tasa / 2
        cuota_quincenal = (
            valor_total
            * tasa_quincenal
            * (1 + tasa_quincenal) ** plazo
            / ((1 + tasa_quincenal) ** plazo - 1)
        )
        valor_total_con_interes = cuota_quincenal * plazo

    # Verificar si ya existe un deducible con el mismo concepto y estado activo
    # deducible_existente = Deducible.query.filter_by(
    #     modelo_id=modelo.id, concepto=datos["concepto"], estado="Pagado"
    # ).first()
    # if deducible_existente:
    #     return (
    #         jsonify({"mensaje": "Ya existe un deducible activo con este concepto"}),
    #         400,
    #     )

    # Crear el nuevo deducible
    nuevo_deducible = Deducible(
        concepto=datos["concepto"],
        valor_sin_interes=valor_total,
        valor_total=valor_total_con_interes,
        plazo=plazo,
        tasa=tasa / 2 if tasa > 0 else 0,  # Tasa quincenal o 0 si no hay intereses
        valor_quincenal=cuota_quincenal,
        quincenas_restantes=plazo,
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(days=plazo * 15),
        valor_pagado=0,
        valor_restante=valor_total_con_interes,
        modelo_id=modelo.id,
        estado="Activo",
    )

    try:
        db.session.add(nuevo_deducible)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": "Error al agregar deducible", "error": str(e)}), 500

    return jsonify(
        {"mensaje": "Deducible agregado con éxito", "deducible_id": nuevo_deducible.id}
    )


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


@app.route("/ganancias/<int:ganancia_id>/pagar", methods=["GET"])
def pagar_ganancia(ganancia_id):
    ganancia = Ganancia.query.get_or_404(ganancia_id, "Ganancia no encontrada.")
    prestamos_activos = ganancia.modelo.deducibles
    modelo = ganancia.modelo
    email_modelo = modelo.correo_electronico
    fecha_pago = datetime.now().strftime("%d/%m/%Y")

    # Realiza una solicitud interna a la ruta `obtener_ganancias_por_usuario_y_periodo`
    nombre_usuario = modelo.nombre_usuario
    nombre_periodo = ganancia.periodo.nombre
    url = f"{Config.NOMINA_API_URL}/ganancias/usuario/{nombre_usuario}/periodo/{nombre_periodo}"
    print(url)

    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"mensaje": "Error al obtener información de ganancias"}), 500

    datos = response.json()

    # Genera el contenido para el correo y el PDF usando los datos obtenidos
    trm_liquidacion = datos.get("trm")
    porcentaje_ganancia = datos.get("porcentaje") * 100
    detalles_ganancias = [
        {
            "nombre": detalle["nombre_pagina"],
            "tokens": f"{detalle['tokens']}",
            # "valor_usd": f"${float(detalle['tokens']) * 0.05:.2f}",
            "valor_cop": f"${round(float(detalle['total_cop']))}",
        }
        for detalle in datos.get("detalles_paginas", [])
    ]

    # Calcula los totales
    total_tokens = sum(
        float(detalle["tokens"]) for detalle in datos["detalles_paginas"]
    )
    total_usd = total_tokens * 0.05
    total_cop = datos.get("total_cop")
    gran_total_cop = datos.get("gran_total_cop")
    deducibles_activos = [
        d for d in datos.get("detalles_deducibles", []) if d["estado"] == "Activo"
    ]

    total_deducibles = datos.get("total_deducibles")

    # Renderiza el HTML del correo
    correo_html = render_template(
        "desprendible_email.html",
        modelo=modelo,
        trm_liquidacion=trm_liquidacion,
        porcentaje_ganancia=porcentaje_ganancia,
        detalles_ganancias=detalles_ganancias,
        total_tokens=total_tokens,
        total_usd=total_usd,
        total_cop=total_cop,
        gran_total_cop=gran_total_cop,
        total_deducibles=total_deducibles,
        detalles_deducibles=deducibles_activos,
        id_pago=ganancia.id,
    )

    # Genera el PDF usando la función auxiliar `generar_pdf_desprendible`
    pdf_attachment = generar_pdf_desprendible(
        modelo, ganancia, gran_total_cop, fecha_pago
    )

    # Enviar el correo con el PDF adjunto
    msg = Message(
        f"¡Buenas noticias! Te pagaron tu nómina 🎉💸 - {nombre_periodo}",
        sender="Nomina Dahouse<notificaciones@dahouse.co>",
        recipients=[email_modelo, "comprobantesnomina@dahouse.co"],
        html=correo_html,
    )

    msg.attach(f"desprendible_{nombre_periodo}.pdf", "application/pdf", pdf_attachment)

    send_sms(
        modelo.numero_celular,
        f"¡Tu pago llegará pronto, {modelo.nombres}!\n\nRevisa tu desprendible de pago para el periodo {nombre_periodo} en tu correo: {email_modelo}.\n\nSi tienes dudas, contáctanos al +573182879509.\n\nDahouse Studio.",
    )

    for deducible in prestamos_activos:
        if deducible.valor_restante == 0:
            deducible.estado = "Pagado"
            db.session.commit()

    mail.send(msg)

    # Actualiza el estado de ganancia
    ganancia.estado = "Pagado"
    db.session.commit()

    return jsonify({"mensaje": "Ganancia pagada y correo enviado con éxito"})


@app.route("/ganancias/eliminar", methods=["DELETE"])
def eliminar_ganancia():
    datos = request.json
    ganancia_id = datos.get("ganancia_id")
    if not ganancia_id:
        return jsonify({"mensaje": "ID de ganancia no proporcionado"}), 400

    # Obtener la ganancia
    ganancia = Ganancia.query.get(ganancia_id)
    if not ganancia:
        return jsonify({"mensaje": "Ganancia no encontrada"}), 404

    # Eliminar deducciones asociadas
    for deduccion in ganancia.deducciones_asociadas:
        db.session.delete(deduccion)

    # Eliminar ganancias por página asociadas
    for gpp in ganancia.ganancias_por_pagina:
        db.session.delete(gpp)

    # Eliminar la ganancia principal
    db.session.delete(ganancia)

    try:
        db.session.commit()
        return jsonify({"mensaje": "Ganancia eliminada con éxito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": f"Error al eliminar ganancia: {str(e)}"}), 500


##NUEVO MODULO GANANCIAS
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


# Definimos las zonas horarias y horarios específicos de cierre
HORARIOS_PAGINAS = {
    "Streamate": pytz.timezone("GMT"),  # Sábado a sábado a las 00:00 GMT
    "Camsoda": pytz.timezone("UTC"),  # Lunes a domingo a las 00:00 UTC
    "Stripchat": pytz.timezone("UTC"),  # Lunes a domingo a las 00:00 UTC
    "Chaturbate": pytz.timezone("America/Bogota"),  # Lunes a lunes a las 00:00 UTC-5
    "CherryTV": pytz.timezone("America/Bogota"),  # Lunes a lunes a las 00:00 UTC-5
    "default": pytz.timezone("UTC"),  # Usaremos UTC como zona horaria predeterminada
}

# Zona horaria del servidor
SERVIDOR_TZ = pytz.timezone("America/Bogota")  # UTC-5


def obtener_cierre_por_pagina(pagina_nombre, fecha):
    # Convertimos la fecha a la zona horaria de la página y ajustamos a las 00:00
    tz_pagina = HORARIOS_PAGINAS.get(pagina_nombre, HORARIOS_PAGINAS["default"])
    fecha_pagina = fecha.astimezone(tz_pagina).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    if pagina_nombre == "Streamate":
        # Streamate cierra de sábado a sábado a las 00:00 GMT
        inicio_periodo = fecha_pagina - timedelta(days=(fecha_pagina.weekday() + 1) % 7)
        fin_periodo = inicio_periodo + timedelta(
            days=6, hours=23, minutes=59, seconds=59
        )
        proximo_cierre = fin_periodo + timedelta(
            seconds=1
        )  # Ajuste para el próximo cierre a 00:00 GMT
        fin_periodo = fin_periodo.replace(
            hour=23, minute=59, second=59
        )  # Fin del periodo es el sábado

    elif pagina_nombre == "Camsoda":
        # Camsoda va de lunes a domingo (domingo a las 23:59 UTC)
        inicio_periodo = fecha_pagina - timedelta(days=fecha_pagina.weekday())
        fin_periodo = inicio_periodo + timedelta(days=6, hours=23, minutes=59)
        proximo_cierre = fin_periodo  # El próximo cierre es el mismo que el fin del periodo para Camsoda y Stripchat

    elif pagina_nombre == "Stripchat":
        # Stripchat va de lunes a domingo (domingo a las 23:59 UTC)
        inicio_periodo = fecha_pagina - timedelta(days=fecha_pagina.weekday())
        fin_periodo = inicio_periodo + timedelta(days=6, hours=23, minutes=59)
        proximo_cierre = fin_periodo  # El próximo cierre es el mismo que el fin del periodo para Camsoda y Stripchat

    elif pagina_nombre in ["Chaturbate", "CherryTV"]:
        # Chaturbate y CherryTV cierran de lunes a lunes a las 00:00 UTC-5 (de martes a lunes)
        inicio_periodo = fecha_pagina - timedelta(
            days=(fecha_pagina.weekday() + 6) % 7
        )  # Inicia el martes
        fin_periodo = inicio_periodo + timedelta(days=6, hours=23, minutes=59)
        proximo_cierre = fin_periodo  # El próximo cierre es el mismo que el fin del periodo para Chaturbate y CherryTV

    else:
        # Para otros casos, se usa un periodo semanal estándar de lunes a domingo
        inicio_periodo = fecha_pagina - timedelta(days=fecha_pagina.weekday())
        fin_periodo = inicio_periodo + timedelta(days=6, hours=23, minutes=59)
        proximo_cierre = fin_periodo + timedelta(
            days=1
        )  # Ajuste para el próximo cierre

    # Convertimos a la zona horaria del servidor
    inicio_periodo = inicio_periodo.astimezone(SERVIDOR_TZ)
    fin_periodo = fin_periodo.astimezone(SERVIDOR_TZ)
    proximo_cierre = proximo_cierre.astimezone(SERVIDOR_TZ)

    print(
        f"Página: {pagina_nombre}, Fecha: {fecha}, Inicio Periodo: {inicio_periodo}, Fin Periodo: {fin_periodo}, Próximo Cierre: {proximo_cierre}"
    )

    return inicio_periodo, fin_periodo, proximo_cierre


def asignar_ganancias_a_periodos(supuesto, pagina_nombre, fecha):
    inicio_periodo, fin_periodo, proximo_cierre = obtener_cierre_por_pagina(
        pagina_nombre, fecha
    )

    if pagina_nombre in ["Chaturbate", "CherryTV"]:
        # Ajustar lógica para que las ganancias del lunes hasta las 23:59 se asignen al periodo anterior
        if fecha.weekday() == 0:  # Si es lunes
            inicio_periodo -= timedelta(days=7)
            fin_periodo -= timedelta(days=7)

    supuesto.inicio_periodo = inicio_periodo
    supuesto.fin_periodo = fin_periodo
    supuesto.proximo_cierre = proximo_cierre

    return supuesto


@app.route("/periodos/<int:periodo_id>/semanas", methods=["GET"])
def obtener_semanas_disponibles(periodo_id):
    periodo = Periodo.query.get_or_404(periodo_id)
    semanas_disponibles = []

    fecha_actual = periodo.fecha_inicio
    while fecha_actual <= periodo.fecha_fin:
        inicio_semana = fecha_actual
        fin_semana = inicio_semana + timedelta(days=6)
        if fin_semana > periodo.fecha_fin:
            fin_semana = periodo.fecha_fin
        semanas_disponibles.append(
            {
                "inicio_semana": inicio_semana.strftime("%Y-%m-%d"),
                "fin_semana": fin_semana.strftime("%Y-%m-%d"),
                "descripcion": f"Semana del {inicio_semana.strftime('%d de %B del %Y')} al {fin_semana.strftime('%d de %B del %Y')}",
            }
        )
        fecha_actual = fin_semana + timedelta(days=1)

    return jsonify(semanas_disponibles)


@app.route("/paginas/cierres", methods=["GET"])
def listar_cierres_paginas():
    try:
        paginas = ["Chaturbate", "Stripchat", "Camsoda", "Streamate", "CherryTV"]
        fecha_actual = datetime.now(SERVIDOR_TZ)  # Usamos la zona horaria del servidor
        cierres = []

        for pagina in paginas:
            inicio_periodo, fin_periodo, proximo_cierre = obtener_cierre_por_pagina(
                pagina, fecha_actual
            )
            dias_restantes = (proximo_cierre - fecha_actual).days
            cierres.append(
                {
                    "pagina": pagina,
                    "proximo_cierre": proximo_cierre.strftime("%Y-%m-%d %H:%M:%S"),
                    "dias_restantes": dias_restantes,
                    "inicio_periodo": inicio_periodo.strftime("%Y-%m-%d %H:%M:%S"),
                    "fin_periodo": fin_periodo.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        return jsonify(cierres)
    except Exception as e:
        return jsonify({"mensaje": str(e)}), 500


@app.route("/jornadas", methods=["GET"])
def listar_jornadas():
    jornadas = ["Tarde", "Tarde Satélite", "Noche", "Noche Satélite"]
    return jsonify(jornadas)


@app.route("/modelos/jornada/<jornada>", methods=["GET"])
def listar_modelos_por_jornada(jornada):
    modelos = Modelo.query.filter_by(jornada=jornada).all()
    return jsonify(
        [
            {
                "id": modelo.id,
                "nombre": f"{modelo.nombres} {modelo.apellidos}",
                "nombre_usuario": modelo.nombre_usuario,
            }
            for modelo in modelos
        ]
    )


@app.route("/modelos/<int:modelo_id>/paginas", methods=["GET"])
def listar_paginas_por_modelo(modelo_id):
    modelo = Modelo.query.get_or_404(modelo_id)
    paginas = modelo.paginas
    return jsonify([{"id": pagina.id, "nombre": pagina.nombre} for pagina in paginas])


@app.route("/periodos", methods=["GET"])
def obtener_periodos_disponibles():
    periodos = Periodo.query.order_by(Periodo.fecha_fin.desc()).all()
    return jsonify(
        [
            {
                "id": periodo.id,
                "nombre": periodo.nombre,
                "fecha_inicio": periodo.fecha_inicio.strftime("%Y-%m-%d"),
                "fecha_fin": periodo.fecha_fin.strftime("%Y-%m-%d"),
            }
            for periodo in periodos
        ]
    )


@app.route("/metas", methods=["POST"])
def establecer_meta():
    datos = request.json
    periodo = datos.get("periodo")
    meta = datos.get("meta")
    nueva_meta = MetaPeriodo(
        periodo=periodo,
        meta=meta,
        fecha_inicio=datos.get("fecha_inicio"),
        fecha_fin=datos.get("fecha_fin"),
    )
    db.session.add(nueva_meta)
    db.session.commit()
    return jsonify({"mensaje": "Meta establecida correctamente"})


@app.route("/metas/<string:periodo>", methods=["GET"])
def obtener_meta(periodo):
    meta = MetaPeriodo.query.filter_by(periodo=periodo).first()
    if meta:
        return jsonify(
            {
                "meta": meta.meta,
                "fecha_inicio": meta.fecha_inicio.strftime("%Y-%m-%d"),
                "fecha_fin": meta.fecha_fin.strftime("%Y-%m-%d"),
            }
        )
    return (
        jsonify({"mensaje": "No se encontró la meta para el periodo especificado"}),
        404,
    )


register_blueprints(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        inicializar_paginas()
        inicializar_roles()
    app.run(debug=True)
