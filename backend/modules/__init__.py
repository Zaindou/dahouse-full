from modules.inventory import inventory_bp
from modules.auth import auth_bp


def register_blueprints(app):
    """
    Registra todos los blueprints en la aplicación Flask.
    """
    # Registrar cada blueprint aquí
    app.register_blueprint(inventory_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")



