from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Pagina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)


class GananciaPorPagina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tokens = db.Column(db.Integer, nullable=False)
    total_cop = db.Column(db.Float, nullable=False)  # Nuevo campo
    ganancia_id = db.Column(db.Integer, db.ForeignKey("ganancia.id"), nullable=False)
    pagina_id = db.Column(db.Integer, db.ForeignKey("pagina.id"), nullable=False)


class Ganancia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trm = db.Column(db.Float, nullable=False)
    total_cop = db.Column(db.Float, nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey("modelo.id"), nullable=False)
    ganancias_por_pagina = db.relationship(
        "GananciaPorPagina", backref="ganancia", lazy=True
    )
    periodo_id = db.Column(db.Integer, db.ForeignKey("periodo.id"), nullable=False)
    periodo = db.relationship("Periodo", backref="ganancias")


class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    tipo_documento = db.Column(db.String(10), nullable=False)
    numero_documento = db.Column(db.String(20), nullable=False, unique=True)
    nombre_usuario = db.Column(db.String(50), nullable=False, unique=True)
    paginas_habilitadas = db.relationship(
        "PaginaHabilitada", backref="modelo", lazy=True
    )
    habilitado = db.Column(db.Boolean, default=True, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey("rol.id"), nullable=False)
    rol = db.relationship("Rol", backref="modelos")


class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)


class Deducible(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concepto = db.Column(db.String(100), nullable=False)  # Concepto del deducible
    valor_total = db.Column(db.Float, nullable=False)
    valor_quincenal = db.Column(db.Float, nullable=False)
    plazo = db.Column(db.Integer, nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey("modelo.id"), nullable=False)
    modelo = db.relationship("Modelo", backref="deducibles")
    quincenas_restantes = db.Column(db.Integer, nullable=False)


class PaginaHabilitada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo_id = db.Column(db.Integer, db.ForeignKey("modelo.id"), nullable=False)
    pagina_id = db.Column(db.Integer, db.ForeignKey("pagina.id"), nullable=False)


class Periodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(
        db.String(10), nullable=False
    )  # Asegúrate de que este campo esté definido
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
