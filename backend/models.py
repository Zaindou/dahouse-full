from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()


class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    modelos = db.relationship("Modelo", back_populates="rol", lazy=True)


class Pagina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    ganancias_por_pagina = db.relationship(
        "GananciaPorPagina", back_populates="pagina", lazy=True
    )
    supuestos_ganancias = db.relationship(
        "SupuestoGanancia", back_populates="pagina", lazy=True
    )
    modelos = db.relationship(
        "Modelo", secondary="modelos_paginas", back_populates="paginas"
    )


class GananciaPorPagina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tokens = db.Column(db.Float, nullable=False)
    total_cop = db.Column(db.Float, nullable=False)
    ganancia_estudio_cop = db.Column(db.Float, nullable=False, default=0)
    ganancia_id = db.Column(db.Integer, db.ForeignKey("ganancia.id"), nullable=False)
    pagina_id = db.Column(db.Integer, db.ForeignKey("pagina.id"), nullable=False)
    pagina = db.relationship("Pagina", back_populates="ganancias_por_pagina")
    ganancia = db.relationship("Ganancia", back_populates="ganancias_por_pagina")


class Ganancia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trm = db.Column(db.Float, nullable=False)
    total_cop = db.Column(db.Float, nullable=False)
    ganancia_general_cop = db.Column(
        db.Float, nullable=False, default=0
    )  # Ganancia general del estudio
    modelo_id = db.Column(db.Integer, db.ForeignKey("modelo.id"), nullable=False)
    periodo_id = db.Column(db.Integer, db.ForeignKey("periodo.id"), nullable=False)
    estado = db.Column(db.String(60), nullable=False, default="Pendiente")
    porcentaje = db.Column(db.Float, nullable=False)
    modelo = db.relationship("Modelo", back_populates="ganancias")
    periodo = db.relationship("Periodo", back_populates="ganancias")
    ganancias_por_pagina = db.relationship(
        "GananciaPorPagina", back_populates="ganancia", lazy="dynamic"
    )
    deducciones_asociadas = db.relationship(
        "PagoDeduccion", back_populates="pago", lazy="dynamic"
    )


modelos_paginas = db.Table(
    "modelos_paginas",
    db.Column("modelo_id", db.Integer, db.ForeignKey("modelo.id"), primary_key=True),
    db.Column("pagina_id", db.Integer, db.ForeignKey("pagina.id"), primary_key=True),
)


class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_documento = db.Column(db.String(50), nullable=False)
    numero_documento = db.Column(db.String(50), unique=True, nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    correo_electronico = db.Column(db.String(100), unique=True, nullable=False)
    numero_celular = db.Column(db.String(50), nullable=True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey("rol.id"), nullable=False)
    banco = db.Column(db.String(50))
    numero_cuenta = db.Column(db.String(50))
    habilitado = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.now)
    exclusividad = db.Column(db.Boolean, default=False)
    jornada = db.Column(db.String(50), nullable=True)  # Asegurando que es nulleable
    rol = db.relationship("Rol", back_populates="modelos")
    ganancias = db.relationship("Ganancia", back_populates="modelo", lazy="dynamic")
    deducibles = db.relationship("Deducible", back_populates="modelo", lazy=True)
    paginas = db.relationship(
        "Pagina", secondary="modelos_paginas", back_populates="modelos"
    )
    supuestos_ganancias = db.relationship(
        "SupuestoGanancia", back_populates="modelo", lazy=True
    )
    password = db.Column(db.String(255), nullable=True)
    porcentaje_base = db.Column(db.Float, nullable=True)
    es_satelite = db.Column(db.Boolean, default=False)

    acciones_inventario = db.relationship(
        "Inventario", back_populates="usuario_modificacion", lazy="dynamic"
    )


class SupuestoGanancia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo_id = db.Column(db.Integer, db.ForeignKey("modelo.id"), nullable=False)
    pagina_id = db.Column(db.Integer, db.ForeignKey("pagina.id"), nullable=False)
    tokens = db.Column(db.Float, nullable=False)
    total_cop = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    inicio_periodo = db.Column(db.Date, nullable=False)
    fin_periodo = db.Column(db.Date, nullable=False)
    porcentaje = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    modelo = db.relationship("Modelo", back_populates="supuestos_ganancias")
    pagina = db.relationship("Pagina", back_populates="supuestos_ganancias")


class Deducible(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concepto = db.Column(db.String(100), nullable=False)  # Concepto del deducible
    valor_total = db.Column(db.Float, nullable=False)
    valor_quincenal = db.Column(db.Float, nullable=False)
    plazo = db.Column(db.Integer, nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey("modelo.id"), nullable=False)
    quincenas_restantes = db.Column(db.Integer, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    tasa = db.Column(db.Float, nullable=False)
    valor_pagado = db.Column(db.Float, nullable=True)
    valor_restante = db.Column(db.Float, nullable=True)
    estado = db.Column(db.String(60), nullable=True, default="Pendiente")
    valor_sin_interes = db.Column(db.Float, nullable=True)
    modelo = db.relationship("Modelo", back_populates="deducibles")
    concepto = db.Column(db.String(100), nullable=False)
    pagos_asociados = db.relationship(
        "PagoDeduccion", back_populates="deduccion", lazy="dynamic"
    )
    creado_por = db.Column(db.String(50), nullable=True)


class Periodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(10), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    meta_periodo = db.Column(db.Float, nullable=True)
    ganancias = db.relationship("Ganancia", back_populates="periodo", lazy=True)


class MetaPeriodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    periodo = db.Column(db.String(50), unique=True, nullable=False)
    meta = db.Column(db.Integer, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)


class PagoDeduccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pago_id = db.Column(db.Integer, db.ForeignKey("ganancia.id"), nullable=False)
    deduccion_id = db.Column(db.Integer, db.ForeignKey("deducible.id"), nullable=False)
    monto_pagado = db.Column(
        db.Float, nullable=False
    )  # Cantidad descontada de la deducción
    cuotas_restantes = db.Column(
        db.Integer, nullable=False
    )  # Cuotas restantes después del pago
    fecha_pago = db.Column(db.DateTime, default=datetime.now)  # Fecha del pago

    # Relaciones
    pago = db.relationship("Ganancia", back_populates="deducciones_asociadas")
    deduccion = db.relationship("Deducible", back_populates="pagos_asociados")


class Earning(db.Model):
    __tablename__ = "earnings"

    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    nickname = db.Column(db.String(50), nullable=False)  # Nickname de la modelo
    dollars = db.Column(db.Float, nullable=False, default=0.0)  # Ganancia en dólares
    tokens = db.Column(db.Float, nullable=False, default=0.0)  # Ganancia en tokens
    timestamp = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )  # Fecha y hora de registro
    date = db.Column(db.Date, nullable=False)  # Fecha a la que pertenece la ganancia
    page_name = db.Column(db.String(50), nullable=False)  # Nombre de la página
    hours_worked = db.Column(db.Interval, nullable=True)  # Horas trabajadas
    is_locked = db.Column(db.Boolean, nullable=False, default=False)


class EarningsUsers(db.Model):
    __tablename__ = "earnings_users"

    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    nickname = db.Column(db.String(50), nullable=False)  # Nickname de la modelo
    username = db.Column(db.String(50), nullable=False)  # Nickname de la modelo
    password = db.Column(db.String(50), nullable=False)  # Ganancia en dólares
    page_name = db.Column(db.String(50), nullable=False)  # Ganancia en tokens
    is_active = db.Column(db.Boolean, nullable=False, default=True)


# Modelo de Categoría
class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255), nullable=True)

    # Relación con Inventario
    inventarios = db.relationship(
        "Inventario", back_populates="categoria", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Categoria {self.nombre}>"


# Modelo de Inventario
class Inventario(db.Model):
    __tablename__ = "inventario"
    id = db.Column(db.Integer, primary_key=True)
    nombre_item = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    estado = db.Column(db.String(50), nullable=False, default="Disponible")
    estado_articulo = db.Column(db.String(50), nullable=True, default="Excelente")
    precio = db.Column(db.Float, nullable=True, default=0.0)
    fecha_actualizacion = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Clave foránea con nombre explícito
    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey("categoria.id", name="fk_inventario_categoria"),
        nullable=False,
    )
    categoria = db.relationship("Categoria", back_populates="inventarios")

    # Clave foránea con nombre explícito
    usuario_modificacion_id = db.Column(
        db.Integer,
        db.ForeignKey("modelo.id", name="fk_inventario_modelo"),
        nullable=True,
    )
    usuario_modificacion = db.relationship(
        "Modelo", back_populates="acciones_inventario"
    )


# Agregar una relación inversa en el modelo `Modelo`
Modelo.acciones_inventario = db.relationship(
    "Inventario", back_populates="usuario_modificacion", lazy="dynamic"
)

# Establecer las relaciones back_populates en la otra dirección

Pagina.ganancias_por_pagina = db.relationship(
    "GananciaPorPagina", back_populates="pagina", lazy=True
)
Pagina.supuestos_ganancias = db.relationship(
    "SupuestoGanancia", back_populates="pagina", lazy=True
)
Pagina.modelos = db.relationship(
    "Modelo", secondary="modelos_paginas", back_populates="paginas"
)
