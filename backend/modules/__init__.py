from modules.inventory import inventory_bp


def register_blueprints(app):
    """
    Registra todos los blueprints en la aplicación Flask.
    """
    # Registrar cada blueprint aquí
    app.register_blueprint(inventory_bp, url_prefix="/")
