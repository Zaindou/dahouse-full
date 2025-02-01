from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
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


# Crear el blueprint de loans
loans_bp = Blueprint("loans", __name__)


@loans_bp.route("/<nombre_usuario>/creardeducible", methods=["POST"])
@jwt_required()
def agregar_deducible(nombre_usuario):
    # Buscar el modelo por nombre de usuario
    modelo = Modelo.query.filter_by(nombre_usuario=nombre_usuario).first()
    if not modelo:
        return jsonify({"mensaje": "Modelo no encontrado"}), 404

    # Obtener los datos del cuerpo de la solicitud
    datos = request.json

    # Validar campos requeridos
    campos_requeridos = ["concepto", "valor_total", "plazo", "tasa"]
    for campo in campos_requeridos:
        if campo not in datos:
            return jsonify({"mensaje": f"Falta el campo requerido: {campo}"}), 400

    if datos["valor_total"] <= 0 or datos["plazo"] <= 0 or datos["tasa"] < 0:
        return jsonify({"mensaje": "Los valores deben ser mayores que cero"}), 400

    # Convertir tasa a decimal si está en porcentaje
    tasa = datos["tasa"]
    if tasa > 1:  # Si está en porcentaje, convertir a decimal
        tasa = tasa / 100

    plazo = datos["plazo"]
    valor_total = datos["valor_total"]

    if tasa == 0:
        # Sin intereses
        cuota_quincenal = valor_total / plazo
        valor_total_con_interes = valor_total
    else:
        # Con intereses (sistema francés)
        tasa_quincenal = tasa / 2
        cuota_quincenal = (
            valor_total
            * tasa_quincenal
            * (1 + tasa_quincenal) ** plazo
            / ((1 + tasa_quincenal) ** plazo - 1)
        )
        valor_total_con_interes = cuota_quincenal * plazo

    # Obtener información del usuario que realiza la operación
    usuario_id = get_jwt_identity()
    usuario = db.session.get(Modelo, usuario_id.get("id"))
    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    # Crear el nuevo deducible
    nuevo_deducible = Deducible(
        concepto=datos["concepto"],
        valor_sin_interes=valor_total,
        valor_total=valor_total_con_interes,
        plazo=plazo,
        tasa=tasa / 2 if tasa > 0 else 0,
        valor_quincenal=cuota_quincenal,
        quincenas_restantes=plazo,
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(days=plazo * 15),
        valor_pagado=0,
        valor_restante=valor_total_con_interes,
        modelo_id=modelo.id,
        creado_por=usuario.id,  # Registrar el ID del usuario que crea el deducible
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


@loans_bp.route("/<int:deducible_id>/refinanciar", methods=["PUT"])
@jwt_required()
def refinanciar_deducible(deducible_id):
    # Obtener información del usuario que realiza la operación
    usuario_id = get_jwt_identity()
    usuario = db.session.get(Modelo, usuario_id.get("id"))

    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    # Verificar que el usuario tenga rol de Administrador
    if usuario.rol.nombre != "Administrador":
        return (
            jsonify(
                {
                    "mensaje": "Acceso denegado: solo los administradores pueden refinanciar deducibles"
                }
            ),
            403,
        )

    # Buscar el deducible por ID
    deducible = Deducible.query.get(deducible_id)
    if not deducible:
        return jsonify({"mensaje": "Deducible no encontrado"}), 404

    # Verificar el estado actual del deducible
    if deducible.estado == "Refinanciado":
        return jsonify({"mensaje": "El deducible ya está refinanciado"}), 400

    # Actualizar el estado del deducible a Refinanciado
    deducible.estado = "Refinanciado"
    deducible.modificado_por = usuario.id  # Registrar el ID del usuario que modifica
    deducible.fecha_modificacion = datetime.now()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"mensaje": "Error al refinanciar el deducible", "error": str(e)}),
            500,
        )

    return jsonify(
        {"mensaje": "Deducible refinanciado con éxito", "deducible_id": deducible.id}
    )


@loans_bp.route("/historial-pagos/<int:modelo_id>", methods=["GET"])
def obtener_historial_pagos(modelo_id):
    modelo = Modelo.query.get_or_404(modelo_id)
    ganancias = (
        Ganancia.query.filter_by(modelo_id=modelo.id).order_by(Ganancia.id.desc()).all()
    )

    historial = [
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
    ]

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
