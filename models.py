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


modelos_paginas = db.Table(
    "modelos_paginas",
    db.Column("modelo_id", db.Integer, db.ForeignKey("modelo.id"), primary_key=True),
    db.Column("pagina_id", db.Integer, db.ForeignKey("pagina.id"), primary_key=True),
)


class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    tipo_documento = db.Column(db.String(10), nullable=False)
    numero_documento = db.Column(db.String(20), nullable=False, unique=True)
    nombre_usuario = db.Column(db.String(50), nullable=False, unique=True)
    habilitado = db.Column(db.Boolean, default=True, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey("rol.id"), nullable=False)
    rol = db.relationship("Rol", backref="modelos")
    paginas = db.relationship(
        "Pagina", secondary=modelos_paginas, backref=db.backref("modelos", lazy=True)
    )
    ganancias = db.relationship("Ganancia", backref="modelo", lazy=True)
    banco = db.Column(db.String(50), nullable=False)
    numero_cuenta = db.Column(db.String(50), nullable=False)
    correo_electronico = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False)


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


class Periodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(
        db.String(10), nullable=False
    )  # Asegúrate de que este campo esté definido
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
