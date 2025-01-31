from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import check_password_hash
from datetime import timedelta
from models import db, Modelo, Rol

# Crear Blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/")


@auth_bp.route("/login", methods=["POST"])
def login():
    datos = request.json
    modelo = Modelo.query.filter_by(nombre_usuario=datos["nombre_usuario"]).first()

    if not modelo or not check_password_hash(modelo.password, datos["password"]):
        return jsonify({"mensaje": "Credenciales incorrectas"}), 401

    rol = Rol.query.get(modelo.rol_id)

    # Generar tokens con expiración
    access_token = create_access_token(
        identity={"id": modelo.id, "rol": rol.nombre},
        expires_delta=timedelta(hours=5)
    )
    refresh_token = create_refresh_token(identity={"id": modelo.id})

    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@auth_bp.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    current_user = get_jwt_identity()
    modelo = Modelo.query.get(current_user["id"])

    if modelo:
        return jsonify({
                    "id": modelo.id,
                    "tipo_documento": modelo.tipo_documento,
                    "numero_documento": modelo.numero_documento,
                    "nombres": modelo.nombres,
                    "apellidos": modelo.apellidos,
                    "correo_electronico": modelo.correo_electronico,
                    "nombre_usuario": modelo.nombre_usuario,
                    "rol": modelo.rol.nombre,  
                    "banco": modelo.banco,
                    "numero_cuenta": modelo.numero_cuenta,
                    "habilitado": modelo.habilitado,
                    "exclusividad": modelo.exclusividad,
                    "jornada": modelo.jornada,
                    "fecha_registro": modelo.fecha_registro,
                    "paginas_habilitadas": [pagina.nombre for pagina in modelo.paginas],
        }), 200

    return jsonify({"mensaje": "Usuario no encontrado"}), 404


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user, expires_delta=timedelta(hours=4))
    return jsonify(access_token=access_token), 200


# Manejadores de errores de JWT
from flask_jwt_extended import JWTManager

def configure_jwt_errors(app):
    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({"mensaje": "Token requerido", "error": "token_missing"}), 401

    @app.errorhandler(422)
    def invalid_token_error(error):
        return jsonify({"mensaje": "Token inválido", "error": "token_invalid"}), 401

    @app.errorhandler(498)
    def expired_token_error(error):
        return jsonify({"mensaje": "Token expirado", "error": "token_expired"}), 401
