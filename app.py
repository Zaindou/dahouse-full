from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import func, distinct, extract, or_, case, and_
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
    SupuestoGanancia,
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
)

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
    return "API: V1.1.1 - FRONTEND: V1.2.2 -- DAHOUSE"


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
                    "vpn_data": {
                        "username": modelo.vpn_username,
                        "password": modelo.vpn_password,
                        "preshared_key": modelo.vpn_preshared_key,
                    },
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


# TODO PENDIENTE REALIZAR LA VISTA DE ESTE ENDPOINT
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


@app.route("/estadisticas-negocio", methods=["GET"])
def obtener_estadisticas_negocio():
    # Base query
    query = db.session.query(Ganancia)

    # Estadísticas por período
    stats_por_periodo = (
        query.join(Periodo)
        .outerjoin(GananciaPorPagina)
        .group_by(Periodo.nombre, Periodo.fecha_inicio)
        .order_by(Periodo.fecha_inicio.desc())
        .with_entities(
            Periodo.nombre,
            func.sum(GananciaPorPagina.total_cop).label("total_ganancia_modelos"),
            func.sum(GananciaPorPagina.ganancia_estudio_cop).label("ganancia_estudio"),
            (
                func.sum(GananciaPorPagina.total_cop)
                + func.sum(GananciaPorPagina.ganancia_estudio_cop)
            ).label("total_ganancias_reales"),
            func.count(distinct(Ganancia.modelo_id)).label("total_modelos"),
            func.sum(GananciaPorPagina.tokens).label("total_tokens"),
        )
        .all()
    )

    # Procesar tokens y modelos únicos por título de período
    tokens_por_titulo = {}
    modelos_por_titulo = {}
    for stat in stats_por_periodo:
        titulo = stat.nombre
        tokens_por_titulo[titulo] = stat.total_tokens or 0
        modelos_por_titulo[titulo] = stat.total_modelos or 0

    # Agrupar por títulos que pertenezcan al mismo mes
    stats_por_mes = {}
    for stat in stats_por_periodo:
        titulo = stat.nombre
        # Extraer año y mes del título
        partes_titulo = titulo.split("-")
        año = int(partes_titulo[0])  # Primer componente es el año
        mes = partes_titulo[1]  # Segundo componente es el mes (en texto)

        mes_año = f"{año}-{mes}"  # Combinar como llave única
        if mes_año not in stats_por_mes:
            stats_por_mes[mes_año] = {
                "total_ganancia_modelos": 0,
                "ganancia_estudio": 0,
                "total_ganancias_reales": 0,
                "total_modelos": 0,
                "total_tokens": 0,
                "numero_periodos": 0,
            }

        # Sumar valores al mes correspondiente
        stats_por_mes[mes_año]["total_ganancia_modelos"] += (
            stat.total_ganancia_modelos or 0
        )
        stats_por_mes[mes_año]["ganancia_estudio"] += stat.ganancia_estudio or 0
        stats_por_mes[mes_año]["total_ganancias_reales"] += (
            stat.total_ganancias_reales or 0
        )
        stats_por_mes[mes_año]["total_tokens"] += tokens_por_titulo[titulo]
        stats_por_mes[mes_año]["total_modelos"] = max(
            stats_por_mes[mes_año]["total_modelos"], modelos_por_titulo[titulo]
        )
        stats_por_mes[mes_año]["numero_periodos"] += 1

    # Diccionario para convertir nombres de meses a índices
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

    # Ordenar meses cronológicamente
    meses_ordenados = sorted(
        stats_por_mes.keys(),
        key=lambda mes_año: (
            int(mes_año.split("-")[0]),  # Año
            MESES_MAP[mes_año.split("-")[1]],  # Mes numérico
        ),
    )

    # Crear lista final de estadísticas por mes con métricas adicionales
    estadisticas_por_mes = []
    for i, mes_año in enumerate(meses_ordenados):
        data = stats_por_mes[mes_año]
        total_ganancias_reales = data["total_ganancias_reales"]
        ganancia_estudio = data["ganancia_estudio"]

        # Porcentaje del estudio
        porcentaje_estudio = (
            (ganancia_estudio / total_ganancias_reales) * 100
            if total_ganancias_reales
            else 0
        )

        # Crecimiento de ganancias mes a mes
        crecimiento_ganancias = None
        if i > 0:  # Solo calcular si hay un mes anterior
            mes_anterior = meses_ordenados[i - 1]
            ganancias_mes_anterior = stats_por_mes[mes_anterior][
                "total_ganancias_reales"
            ]
            if ganancias_mes_anterior:
                crecimiento_ganancias = (
                    (total_ganancias_reales - ganancias_mes_anterior)
                    / ganancias_mes_anterior
                ) * 100

        estadisticas_por_mes.append(
            {
                "año": int(mes_año.split("-")[0]),  # Extraer el año
                "mes": mes_año.split("-")[1],  # Extraer el mes
                "total_ganancia_modelos": float(data["total_ganancia_modelos"]),
                "ganancia_estudio": float(data["ganancia_estudio"]),
                "total_ganancias_reales": float(data["total_ganancias_reales"]),
                "total_modelos": int(data["total_modelos"]),
                "total_tokens": int(data["total_tokens"]),
                "numero_periodos": data["numero_periodos"],
                "porcentaje_estudio": porcentaje_estudio,
                "crecimiento_ganancias": crecimiento_ganancias,
            }
        )

    # Estadísticas de tokens por página
    tokens_por_pagina = (
        db.session.query(
            Pagina.nombre,
            func.sum(GananciaPorPagina.tokens).label("total_tokens"),
            func.sum(GananciaPorPagina.total_cop).label("total_ganado"),
        )
        .join(GananciaPorPagina)
        .group_by(Pagina.nombre)
        .all()
    )

    # Estadísticas de deducciones
    deducciones_stats = (
        db.session.query(
            Deducible.concepto,
            func.sum(PagoDeduccion.monto_pagado).label("total_deducido"),
            func.count(distinct(Deducible.modelo_id)).label("total_modelos"),
        )
        .join(PagoDeduccion)
        .group_by(Deducible.concepto)
        .all()
    )

    # Construir respuesta JSON
    return jsonify(
        {
            "estadisticas_por_periodo": [
                {
                    "periodo": stat.nombre,
                    "total_ganancia_modelos": float(stat.total_ganancia_modelos),
                    "ganancia_estudio": float(stat.ganancia_estudio),
                    "total_ganancias_reales": float(stat.total_ganancias_reales),
                    "total_modelos": stat.total_modelos,
                    "total_tokens": int(stat.total_tokens or 0),
                }
                for stat in stats_por_periodo
            ],
            "estadisticas_por_mes": estadisticas_por_mes,
            "tokens_por_pagina": [
                {
                    "pagina": stat.nombre,
                    "total_tokens": stat.total_tokens,
                    "total_ganado": float(stat.total_ganado),
                }
                for stat in tokens_por_pagina
            ],
            "deducciones": [
                {
                    "concepto": stat.concepto,
                    "total_deducido": float(stat.total_deducido),
                    "total_modelos": stat.total_modelos,
                }
                for stat in deducciones_stats
            ],
        }
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
        f"Resumen de mis ganancias - {nombre_periodo}",
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


@app.route("/supuestos/ganancia/<int:modelo_id>", methods=["GET"])
def obtener_supuestos_ganancia(modelo_id):
    supuestos = SupuestoGanancia.query.filter_by(modelo_id=modelo_id).all()
    supuestos_lista = [
        {
            "id": supuesto.id,
            "pagina": supuesto.pagina.nombre,
            "tokens": supuesto.tokens,
            "total_cop": supuesto.total_cop,
            "fecha": supuesto.fecha.strftime("%Y-%m-%d"),
            "inicio_periodo": supuesto.inicio_periodo.strftime("%Y-%m-%d"),
            "fin_periodo": supuesto.fin_periodo.strftime("%Y-%m-%d"),
        }
        for supuesto in supuestos
    ]
    return jsonify(supuestos_lista)


@app.route(
    "/supuestos/ganancias/periodo/<string:inicio_periodo>/<string:fin_periodo>",
    methods=["GET"],
)
def listar_supuestos_ganancias_por_periodo(inicio_periodo, fin_periodo):
    inicio_periodo_dt = datetime.strptime(inicio_periodo, "%Y-%m-%d").replace(
        tzinfo=pytz.UTC
    )
    fin_periodo_dt = datetime.strptime(fin_periodo, "%Y-%m-%d").replace(tzinfo=pytz.UTC)

    supuestos = SupuestoGanancia.query.filter(
        SupuestoGanancia.inicio_periodo >= inicio_periodo_dt,
        SupuestoGanancia.fin_periodo <= fin_periodo_dt,
    ).all()

    resultado = {}
    total_ganancias = 0
    total_ganancias_turno = {
        "Tarde": 0,
        "Tarde Satélite": 0,
        "Noche": 0,
        "Noche Satélite": 0,
    }

    for supuesto in supuestos:
        modelo_nombre = f"{supuesto.modelo.nombres} {supuesto.modelo.apellidos}"
        pagina_nombre = supuesto.pagina.nombre
        turno = supuesto.modelo.jornada or "Desconocido"

        if modelo_nombre not in resultado:
            resultado[modelo_nombre] = {"total": 0, "por_pagina": {}, "turno": turno}

        if pagina_nombre not in resultado[modelo_nombre]["por_pagina"]:
            resultado[modelo_nombre]["por_pagina"][pagina_nombre] = 0

        resultado[modelo_nombre]["por_pagina"][pagina_nombre] += supuesto.tokens
        resultado[modelo_nombre]["total"] += supuesto.tokens
        if turno in total_ganancias_turno:
            total_ganancias_turno[turno] += supuesto.tokens
        total_ganancias += supuesto.tokens

    print(total_ganancias_turno)
    print(resultado)
    print(total_ganancias)

    return jsonify(
        {
            "total_ganancias": total_ganancias,
            "total_ganancias_turno": total_ganancias_turno,
            "ganancias_por_modelo": resultado,
        }
    )


@app.route("/supuestos/ganancia/<int:id>", methods=["PUT"])
def editar_supuesto_ganancia(id):
    supuesto = SupuestoGanancia.query.get_or_404(id)
    datos = request.json
    tokens = datos.get("tokens")
    if tokens:
        supuesto.tokens = tokens
        supuesto.total_cop = tokens * 0.05 * obtener_trm()
        db.session.commit()
        return jsonify({"mensaje": "Supuesto de ganancia actualizado correctamente"})
    return jsonify({"mensaje": "No se proporcionaron tokens"}), 400


@app.route("/periodos/supuestos", methods=["GET"])
def listar_periodos_supuestos():
    periodos_supuestos = (
        db.session.query(SupuestoGanancia.inicio_periodo, SupuestoGanancia.fin_periodo)
        .distinct()
        .all()
    )
    return jsonify(
        [
            {
                "inicio_periodo": periodo[0].strftime("%Y-%m-%d"),
                "fin_periodo": periodo[1].strftime("%Y-%m-%d"),
            }
            for periodo in periodos_supuestos
        ]
    )


@app.route("/modelos/<int:modelo_id>/ganancias", methods=["POST"])
def registrar_supuesto_ganancia(modelo_id):
    modelo = Modelo.query.get_or_404(modelo_id)
    datos = request.json
    fecha = datetime.strptime(datos["fecha"], "%Y-%m-%d")
    _, fecha_inicio, fecha_fin = obtener_periodo_actual()
    fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
    fecha_limite = fecha_fin_dt - timedelta(days=1)

    if fecha > fecha_limite:
        return (
            jsonify(
                {
                    "mensaje": "No se pueden agregar ganancias después del periodo límite."
                }
            ),
            400,
        )

    supuestos_existentes = SupuestoGanancia.query.filter_by(
        modelo_id=modelo_id, fecha=fecha
    ).all()
    if supuestos_existentes:
        return (
            jsonify(
                {
                    "mensaje": "Ya existe una ganancia registrada para este modelo en esta fecha."
                }
            ),
            400,
        )

    supuestos = []
    for pagina in datos["paginas"]:
        pagina_obj = Pagina.query.get_or_404(pagina["pagina_id"])
        inicio_periodo, fin_periodo, _ = obtener_cierre_por_pagina(
            pagina_obj.nombre, fecha
        )
        print(
            f"Registrando ganancia para {pagina_obj.nombre}: {fecha}, {inicio_periodo}, {fin_periodo}"
        )
        tokens_to_float = float(pagina["tokens"])
        supuesto_ganancia = SupuestoGanancia(
            modelo_id=modelo.id,
            pagina_id=pagina_obj.id,
            tokens=pagina["tokens"],
            total_cop=tokens_to_float * 0.05 * obtener_trm(),
            fecha=fecha,
            inicio_periodo=inicio_periodo,
            fin_periodo=fin_periodo,
            porcentaje=1,
            estado="Supuesto",
        )
        db.session.add(supuesto_ganancia)
        supuestos.append(supuesto_ganancia)
    db.session.commit()
    return jsonify(
        {"mensaje": "Ganancias registradas", "supuestos": [s.id for s in supuestos]}
    )


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


@app.route("/periodos/<int:periodo_id>/dias", methods=["GET"])
def obtener_dias_disponibles(periodo_id):
    periodo = Periodo.query.get_or_404(periodo_id)
    supuestos = SupuestoGanancia.query.filter(
        SupuestoGanancia.fecha >= periodo.fecha_inicio,
        SupuestoGanancia.fecha <= periodo.fecha_fin,
    ).all()
    dias_disponibles = sorted(set(s.fecha.strftime("%Y-%m-%d") for s in supuestos))
    return jsonify(dias_disponibles)


@app.route("/ganancias/consolidadas", methods=["GET"])
def obtener_ganancias_consolidadas():
    periodo_id = request.args.get("periodo_id")
    tipo_periodo = request.args.get("tipo_periodo")
    periodo = Periodo.query.get_or_404(periodo_id)

    if tipo_periodo == "dia":
        fecha = datetime.strptime(request.args.get("fecha"), "%Y-%m-%d")
        supuestos = SupuestoGanancia.query.filter(
            (SupuestoGanancia.fecha == fecha)
            | (
                (SupuestoGanancia.fecha == fecha + timedelta(days=1))
                & (
                    SupuestoGanancia.pagina.has(
                        Pagina.nombre.in_(["Chaturbate", "CherryTV"])
                    )
                )
            )
        ).all()
    elif tipo_periodo == "semana":
        inicio_semana = datetime.strptime(request.args.get("inicio_semana"), "%Y-%m-%d")
        fin_semana = datetime.strptime(request.args.get("fin_semana"), "%Y-%m-%d")
        supuestos = SupuestoGanancia.query.filter(
            (
                (SupuestoGanancia.fecha >= inicio_semana)
                & (SupuestoGanancia.fecha <= fin_semana)
            )
            | (
                (SupuestoGanancia.fecha == fin_semana + timedelta(days=1))
                & (
                    SupuestoGanancia.pagina.has(
                        Pagina.nombre.in_(["Chaturbate", "CherryTV"])
                    )
                )
            )
        ).all()
    else:  # mes
        year = periodo.fecha_inicio.year
        month = periodo.fecha_inicio.month

        periodos_mes = Periodo.query.filter(
            extract("year", Periodo.fecha_inicio) == year,
            extract("month", Periodo.fecha_inicio) == month,
        ).all()

        fechas_inicio = [p.fecha_inicio for p in periodos_mes]
        fechas_fin = [p.fecha_fin for p in periodos_mes]

        filtros = [
            (SupuestoGanancia.fecha >= inicio) & (SupuestoGanancia.fecha <= fin)
            for inicio, fin in zip(fechas_inicio, fechas_fin)
        ]

        supuestos = SupuestoGanancia.query.filter(or_(*filtros)).all()

    total_ganancias = sum([s.tokens for s in supuestos])
    ganancias_por_modelo = {}
    total_ganancias_turno = {
        "Tarde": 0,
        "Tarde Satélite": 0,
        "Noche": 0,
        "Noche Satélite": 0,
    }

    for supuesto in supuestos:
        modelo_nombre = f"{supuesto.modelo.nombre_usuario}"
        pagina_nombre = supuesto.pagina.nombre
        turno = supuesto.modelo.jornada or "Desconocido"

        if modelo_nombre not in ganancias_por_modelo:
            ganancias_por_modelo[modelo_nombre] = {
                "total": 0,
                "por_pagina": {},
                "turno": turno,
            }

        if pagina_nombre not in ganancias_por_modelo[modelo_nombre]["por_pagina"]:
            ganancias_por_modelo[modelo_nombre]["por_pagina"][pagina_nombre] = 0

        ganancias_por_modelo[modelo_nombre]["por_pagina"][
            pagina_nombre
        ] += supuesto.tokens
        ganancias_por_modelo[modelo_nombre]["total"] += supuesto.tokens
        if turno in total_ganancias_turno:
            total_ganancias_turno[turno] += supuesto.tokens

    return jsonify(
        {
            "total_ganancias": total_ganancias,
            "ganancias_por_modelo": ganancias_por_modelo,
            "total_ganancias_turno": total_ganancias_turno,
            "tipo_periodo": tipo_periodo,
        }
    )


def calcular_ganancias_consolidadas(fecha_inicio, fecha_fin):
    supuestos = SupuestoGanancia.query.filter(
        SupuestoGanancia.fecha >= fecha_inicio, SupuestoGanancia.fecha <= fecha_fin
    ).all()

    total_ganancias = sum([s.total_cop for s in supuestos])
    ganancias_por_modelo = {}
    for supuesto in supuestos:
        modelo_nombre = f"{supuesto.modelo.nombres} {supuesto.modelo.apellidos}"
        if modelo_nombre not in ganancias_por_modelo:
            ganancias_por_modelo[modelo_nombre] = 0
        ganancias_por_modelo[modelo_nombre] += supuesto.total_cop

    return {
        "total_ganancias": total_ganancias,
        "ganancias_por_modelo": ganancias_por_modelo,
    }


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


@app.route("/periodos/ultimo", methods=["GET"])
def obtener_ultimo_periodo():
    ultimo_periodo = (
        db.session.query(SupuestoGanancia.inicio_periodo, SupuestoGanancia.fin_periodo)
        .order_by(SupuestoGanancia.fin_periodo.desc())
        .first()
    )
    if ultimo_periodo:
        return jsonify(
            {
                "periodo": f"{ultimo_periodo.inicio_periodo} - {ultimo_periodo.fin_periodo}",
                "fecha_inicio": ultimo_periodo.inicio_periodo.strftime("%Y-%m-%d"),
                "fecha_fin": ultimo_periodo.fin_periodo.strftime("%Y-%m-%d"),
            }
        )
    return jsonify({"mensaje": "No se encontró ningún periodo"}), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        inicializar_paginas()
        inicializar_roles()
    app.run(debug=True)
