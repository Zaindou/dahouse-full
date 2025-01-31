from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Inventario, Modelo, Categoria

inventory_bp = Blueprint("inventory", __name__)

# Ruta para listar categorías
@inventory_bp.route("/categorias", methods=["GET"])
def listar_categorias():
    categorias = Categoria.query.all()
    resultado = [
        {
            "id": categoria.id,
            "nombre": categoria.nombre,
            "descripcion": categoria.descripcion,
        }
        for categoria in categorias
    ]
    return jsonify(resultado), 200


# Ruta para crear una nueva categoría
@inventory_bp.route("/categorias", methods=["POST"])
@jwt_required()
def crear_categoria():
    datos = request.json

    if not datos.get("nombre"):
        return jsonify({"mensaje": "El nombre de la categoría es requerido"}), 400

    if not datos.get("descripcion"):
        return jsonify({"mensaje": "La descripción de la categoría es requerida"}), 400

    if Categoria.query.filter_by(nombre=datos.get("nombre")).first():
        return jsonify({"mensaje": "La categoría ya existe"}), 400

    nueva_categoria = Categoria(
        nombre=datos.get("nombre"), descripcion=datos.get("descripcion")
    )
    db.session.add(nueva_categoria)
    db.session.commit()
    return (
        jsonify({"mensaje": "Categoría creada con éxito", "id": nueva_categoria.id}),
        201,
    )


# Ruta para crear un nuevo ítem
@inventory_bp.route("/inventario", methods=["POST"])
@jwt_required()
def crear_item():
    datos = request.json
    usuario_id = get_jwt_identity()

    if datos.get("cantidad", 0) < 0:
        return jsonify({"mensaje": "La cantidad no puede ser negativa"}), 400

    if datos.get("precio", 0.0) < 0:
        return jsonify({"mensaje": "El precio no puede ser negativo"}), 400

    usuario = db.session.get(Modelo, usuario_id.get("id"))
    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    # Validar que la categoría existe
    categoria_id = datos.get("categoria_id")
    categoria = Categoria.query.get(categoria_id)
    if not categoria:
        return jsonify({"mensaje": "Categoría no encontrada"}), 404

    nuevo_item = Inventario(
        nombre_item=datos.get("nombre_item"),
        descripcion=datos.get("descripcion"),
        cantidad=datos.get("cantidad", 0),
        estado=datos.get("estado", "Disponible"),
        estado_articulo=datos.get("estado_articulo", "Excelente"),  # Nuevo campo
        precio=datos.get("precio", 0.0),
        categoria_id=categoria.id,
        usuario_modificacion_id=usuario.id,
    )
    db.session.add(nuevo_item)
    db.session.commit()
    return (
        jsonify(
            {
                "mensaje": "Ítem creado con éxito",
                "item": {
                    "id": nuevo_item.id,
                    "nombre_item": nuevo_item.nombre_item,
                    "descripcion": nuevo_item.descripcion,
                    "cantidad": nuevo_item.cantidad,
                    "estado": nuevo_item.estado,
                    "estado_articulo": nuevo_item.estado_articulo,  # Incluido en la respuesta
                    "precio": nuevo_item.precio,
                    "categoria": {"id": categoria.id, "nombre": categoria.nombre},
                },
            }
        ),
        201,
    )


# Ruta para listar ítems
@inventory_bp.route("/inventario", methods=["GET"])
def listar_items():
    items = Inventario.query.all()
    resultado = [
        {
            "id": item.id,
            "nombre_item": item.nombre_item,
            "descripcion": item.descripcion,
            "cantidad": item.cantidad,
            "estado": item.estado,
            "estado_articulo": item.estado_articulo,  # Estado del artículo
            "precio": item.precio,
            "fecha_actualizacion": item.fecha_actualizacion.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "categoria": {"id": item.categoria.id, "nombre": item.categoria.nombre},
            "usuario_modificacion": (
                {
                    "id": item.usuario_modificacion.id,
                    "nombre": f"{item.usuario_modificacion.nombres} {item.usuario_modificacion.apellidos}",
                    "nombre_usuario": item.usuario_modificacion.nombre_usuario,
                }
                if item.usuario_modificacion
                else None
            ),
        }
        for item in items
    ]
    return jsonify(resultado), 200


# Ruta para obtener un ítem por ID
@inventory_bp.route("/inventario/<int:item_id>", methods=["GET"])
def obtener_item(item_id):
    item = Inventario.query.get(item_id)
    if not item:
        return jsonify({"mensaje": "Ítem no encontrado"}), 404

    return (
        jsonify(
            {
                "id": item.id,
                "nombre_item": item.nombre_item,
                "descripcion": item.descripcion,
                "cantidad": item.cantidad,
                "estado": item.estado,
                "estado_articulo": item.estado_articulo,  # Incluido en la respuesta
                "precio": item.precio,
                "fecha_actualizacion": item.fecha_actualizacion.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "categoria": {"id": item.categoria.id, "nombre": item.categoria.nombre},
                "usuario_modificacion": (
                    {
                        "id": item.usuario_modificacion.id,
                        "nombre": f"{item.usuario_modificacion.nombres} {item.usuario_modificacion.apellidos}",
                        "nombre_usuario": item.usuario_modificacion.nombre_usuario,
                    }
                    if item.usuario_modificacion
                    else None
                ),
            }
        ),
        200,
    )


# Ruta para actualizar un ítem existente
@inventory_bp.route("/inventario/<int:item_id>", methods=["PUT"])
@jwt_required()
def actualizar_item(item_id):
    item = Inventario.query.get(item_id)

    datos = request.json

    if not item:
        return jsonify({"mensaje": "Ítem no encontrado"}), 404

    if datos.get("precio", 0.0) < 0:
        return jsonify({"mensaje": "El precio no puede ser negativo"}), 400

    usuario_id = get_jwt_identity()
    usuario = db.session.get(Modelo, usuario_id.get("id"))
    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    # Validar categoría si se intenta actualizar
    categoria_id = datos.get("categoria_id")
    if categoria_id:
        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            return jsonify({"mensaje": "Categoría no encontrada"}), 404
        item.categoria_id = categoria.id

    item.nombre_item = datos.get("nombre_item", item.nombre_item)
    item.descripcion = datos.get("descripcion", item.descripcion)
    item.cantidad = datos.get("cantidad", item.cantidad)
    item.estado = datos.get("estado", item.estado)
    item.estado_articulo = datos.get("estado_articulo", item.estado_articulo)  # Nuevo campo
    item.precio = datos.get("precio", item.precio)
    item.usuario_modificacion_id = usuario.id

    db.session.commit()
    return jsonify({"mensaje": "Ítem actualizado con éxito"}), 200


# Ruta para eliminar un ítem
@inventory_bp.route("/inventario/<int:item_id>", methods=["DELETE"])
@jwt_required()
def eliminar_item(item_id):
    item = Inventario.query.get(item_id)
    if not item:
        return jsonify({"mensaje": "Ítem no encontrado"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"mensaje": "Ítem eliminado con éxito"}), 200


# Manejador de errores generales
@inventory_bp.errorhandler(Exception)
def manejar_errores_generales(error):
    return jsonify({"mensaje": "Ocurrió un error inesperado", "error": str(error)}), 500
