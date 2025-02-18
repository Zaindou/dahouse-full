from flask import Blueprint, request, jsonify
from models import db, Earning, Periodo
from datetime import datetime, timedelta
from collections import defaultdict

earnings_bp = Blueprint("earnings", __name__)


# Función para obtener las fechas de inicio y fin de cada semana por página
def calcular_fechas_semanales(periodo):
    ajustes = {
        "Streamate": -2,
        "Stripchat": -1,
        "Camsoda": -1,
        "Bongacams": -1,
        "Chaturbate": 0,
    }
    semanas_por_pagina = defaultdict(dict)

    for page, ajuste in ajustes.items():
        fecha_inicio_ajustada = periodo.fecha_inicio + timedelta(days=ajuste)
        semanas = {
            "week_1": (
                fecha_inicio_ajustada,
                fecha_inicio_ajustada + timedelta(days=6),
            ),
            "week_2": (
                fecha_inicio_ajustada + timedelta(days=7),
                fecha_inicio_ajustada + timedelta(days=13),
            ),
            "week_3": (
                fecha_inicio_ajustada + timedelta(days=14),
                fecha_inicio_ajustada + timedelta(days=20),
            ),
            "week_4": (
                fecha_inicio_ajustada + timedelta(days=21),
                fecha_inicio_ajustada + timedelta(days=27),
            ),
        }
        for week, (start, end) in semanas.items():
            semanas_por_pagina[page][week] = {"start": start, "end": end}

    return semanas_por_pagina


@earnings_bp.route("/initial-data", methods=["GET"])
def obtener_datos_iniciales():
    # Obtener todos los periodos desde enero del año actual
    year_actual = datetime.now().year
    periodos_disponibles = (
        Periodo.query.filter(Periodo.fecha_inicio >= f"{year_actual}-01-01")
        .order_by(Periodo.fecha_inicio)
        .all()
    )

    # Agrupar por mes y año en formato YYYY-MMM (ejemplo: 2025-FEB)
    meses_disponibles = sorted(
        {p.fecha_inicio.strftime("%Y-%b").upper() for p in periodos_disponibles}
    )

    # Obtener todos los modelos con ganancias registradas
    modelos_con_ganancias = (
        db.session.query(Earning.nickname).distinct().order_by(Earning.nickname).all()
    )
    modelos_json = [m.nickname for m in modelos_con_ganancias]

    # Determinar la semana actual dentro del mes actual
    today = datetime.today().date()
    mes_actual = today.strftime("%Y-%b").upper()
    current_week = None

    # Buscar el primer periodo del mes actual
    periodo_actual = next(
        (
            p
            for p in periodos_disponibles
            if p.fecha_inicio.strftime("%Y-%b").upper() == mes_actual
        ),
        None,
    )

    if periodo_actual:
        semanas_por_pagina = calcular_fechas_semanales(periodo_actual)
        for _, weeks in semanas_por_pagina.items():
            for week, date_range in weeks.items():
                start_date = date_range["start"]  # Ya es un objeto datetime.date
                end_date = date_range["end"]  # Ya es un objeto datetime.date

                if start_date <= today <= end_date:
                    current_week = week
                    break
            if current_week:
                break  # Salir del loop si encontramos la semana actual

    return jsonify(
        {
            "meses_disponibles": meses_disponibles,  # Solo YYYY-MMM
            "modelos_con_ganancias": modelos_json,
            "current_week": current_week,  # Semana actual del mes
        }
    )


@earnings_bp.route("/", methods=["GET"])
def listar_earnings():
    periodo_nombre = request.args.get("periodo")
    nickname = request.args.get("nickname")

    periodos = (
        Periodo.query.filter(Periodo.nombre.like(f"{periodo_nombre}%"))
        .order_by(Periodo.nombre)
        .all()
    )

    if not periodos:
        return jsonify({"error": "Periodo no encontrado"}), 404

    periodo_base = periodos[0]
    semanas_por_pagina = calcular_fechas_semanales(periodo_base)

    tokens_por_dia_y_semana = defaultdict(
        lambda: defaultdict(lambda: {"tokens_por_dia": {}, "total_tokens": 0})
    )

    tokens_totales_por_dia_y_semana = defaultdict(
        lambda: {"tokens_por_dia": {}, "total_tokens": 0}
    )

    horas_totales = defaultdict(lambda: {"horas_por_dia": {}, "total_horas_semana": 0})

    totals = {
        "total_tokens": 0,
        "total_hours": 0,
        "tokens_totales_por_dia_y_semana": tokens_totales_por_dia_y_semana,
    }

    resultado = []
    dias_asistidos_set = set()  # Días asistidos de una modelo específica
    dias_generales_set = set()  # Días con tokens > 0 (sin importar modelo)

    for page_name, weeks in semanas_por_pagina.items():
        for week, date_range in weeks.items():
            start_date = date_range["start"]
            end_date = date_range["end"]

            # Filtrar solo por página y fechas
            earnings_list = Earning.query.filter(
                Earning.page_name == page_name,
                Earning.date >= start_date,
                Earning.date <= end_date,
            )

            # Si hay un nickname, filtramos por ese modelo
            if nickname:
                earnings_list = earnings_list.filter(Earning.nickname == nickname)

            earnings_list = earnings_list.all()

            for e in earnings_list:
                hours_worked = (
                    (e.hours_worked.total_seconds() / 3600 if e.hours_worked else 0)
                    if e.page_name == "Stripchat"
                    else 0
                )

                resultado.append(
                    {
                        "id": e.id,
                        "nickname": e.nickname,
                        "dollars": e.dollars,
                        "tokens": e.tokens,
                        "timestamp": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "date": e.date.strftime("%Y-%m-%d"),
                        "page_name": e.page_name,
                        "hours_worked": round(hours_worked, 2),
                        "is_locked": e.is_locked,
                    }
                )

                fecha_str = e.date.strftime("%Y-%m-%d")

                # Acumulamos tokens por día y por semana por página
                tokens_por_dia_y_semana[page_name][week]["tokens_por_dia"].setdefault(
                    fecha_str, 0
                )
                tokens_por_dia_y_semana[page_name][week]["tokens_por_dia"][
                    fecha_str
                ] += e.tokens
                tokens_por_dia_y_semana[page_name][week]["total_tokens"] += e.tokens

                # Acumulamos tokens totales por día y semana
                tokens_totales_por_dia_y_semana[week]["tokens_por_dia"].setdefault(
                    fecha_str, 0
                )
                tokens_totales_por_dia_y_semana[week]["tokens_por_dia"][
                    fecha_str
                ] += e.tokens
                tokens_totales_por_dia_y_semana[week]["total_tokens"] += e.tokens

                # Sumamos al total general de tokens
                totals["total_tokens"] += e.tokens

                # Acumulamos horas trabajadas solo si es Stripchat
                if e.page_name == "Stripchat":
                    horas_totales[week]["horas_por_dia"].setdefault(fecha_str, 0)
                    horas_totales[week]["horas_por_dia"][fecha_str] += hours_worked
                    horas_totales[week]["total_horas_semana"] += hours_worked

                    totals["total_hours"] += hours_worked

                # Si hay un nickname, contar sus días asistidos
                if nickname and e.tokens > 0:
                    dias_asistidos_set.add(fecha_str)

                # Contamos días con actividad en general (cuando no hay filtro de modelo)
                if not nickname and e.tokens > 0:
                    dias_generales_set.add(fecha_str)

    # Si se filtra por modelo, solo contar los días asistidos de la modelo
    if nickname:
        totals["total_dias_asistidos"] = len(dias_asistidos_set)
    else:
        # Si no hay filtro, contar los días con actividad en el periodo
        totals["total_dias_asistidos"] = len(dias_generales_set)

    return (
        jsonify(
            {
                "totals": totals,
                "horas_totales": horas_totales,
                "tokens_por_dia_y_semana": tokens_por_dia_y_semana,
                "week_date_ranges": {
                    page: {
                        week: {
                            "start": dates["start"].strftime("%Y-%m-%d"),
                            "end": dates["end"].strftime("%Y-%m-%d"),
                        }
                        for week, dates in weeks.items()
                    }
                    for page, weeks in semanas_por_pagina.items()
                },
                "earnings": resultado,
            }
        ),
        200,
    )


@earnings_bp.route("/summary", methods=["GET"])
def resumen_rendimiento_modelo():
    periodo_nombre = request.args.get("periodo")
    nickname = request.args.get("nickname")

    if not periodo_nombre or not nickname:
        return jsonify({"error": "Se requiere un periodo y un nickname"}), 400

    # Obtener todos los periodos del mes
    periodos = (
        Periodo.query.filter(Periodo.nombre.like(f"{periodo_nombre}%"))
        .order_by(Periodo.nombre)
        .all()
    )

    if not periodos:
        return jsonify({"error": "Periodo no encontrado"}), 404

    # Usar el primer periodo del mes como referencia para las fechas
    periodo_base = periodos[0]
    semanas_por_pagina = calcular_fechas_semanales(periodo_base)

    tokens_por_dia_y_semana = defaultdict(
        lambda: defaultdict(lambda: {"tokens_por_dia": {}, "total_tokens": 0})
    )

    totals = {
        "total_tokens": 0,
        "total_dollars": 0,
        "days_worked": 0,
        "earnings_per_page": defaultdict(int),
    }

    resultado = []
    dias_asistidos_set = set()

    for page_name, weeks in semanas_por_pagina.items():
        for week, date_range in weeks.items():
            start_date = date_range["start"]
            end_date = date_range["end"]

            # Obtener ganancias del modelo en este rango de fechas
            earnings_list = Earning.query.filter(
                Earning.nickname == nickname,
                Earning.page_name == page_name,
                Earning.date >= start_date,
                Earning.date <= end_date,
            ).all()

            for e in earnings_list:
                fecha_str = e.date.strftime("%Y-%m-%d")

                # Acumular tokens por día y por semana
                tokens_por_dia_y_semana[page_name][week]["tokens_por_dia"].setdefault(
                    fecha_str, 0
                )
                tokens_por_dia_y_semana[page_name][week]["tokens_por_dia"][
                    fecha_str
                ] += e.tokens
                tokens_por_dia_y_semana[page_name][week]["total_tokens"] += e.tokens

                # Acumular totales generales
                totals["total_tokens"] += e.tokens
                totals["total_dollars"] += e.dollars
                totals["earnings_per_page"][page_name] += e.tokens

                # Contar los días trabajados
                dias_asistidos_set.add(fecha_str)

                resultado.append(
                    {
                        "id": e.id,
                        "nickname": e.nickname,
                        "dollars": e.dollars,
                        "tokens": e.tokens,
                        "timestamp": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "date": fecha_str,
                        "page_name": e.page_name,
                    }
                )

    # Calcular días trabajados únicos
    totals["days_worked"] = len(dias_asistidos_set)

    # Calcular promedios
    totals["average_tokens_per_day"] = (
        totals["total_tokens"] / totals["days_worked"]
        if totals["days_worked"] > 0
        else 0
    )
    weeks_count = len(
        semanas_por_pagina["Chaturbate"]
    )  # Cualquier página tiene 4 semanas
    totals["average_tokens_per_week"] = (
        totals["total_tokens"] / weeks_count if weeks_count > 0 else 0
    )

    return jsonify(
        {
            "nickname": nickname,
            "totals": totals,
            "tokens_por_dia_y_semana": tokens_por_dia_y_semana,
        }
    )


@earnings_bp.route("/distribution", methods=["GET"])
def distribucion_ganancias():
    periodo_nombre = request.args.get("periodo")
    nickname = request.args.get("nickname")  # Opcional
    date_filter = request.args.get("date")  # Opcional (YYYY-MM-DD)

    if not periodo_nombre:
        return jsonify({"error": "Se requiere un periodo"}), 400

    # Obtener todos los periodos del mes
    periodos = (
        Periodo.query.filter(Periodo.nombre.like(f"{periodo_nombre}%"))
        .order_by(Periodo.nombre)
        .all()
    )

    if not periodos:
        return jsonify({"error": "Periodo no encontrado"}), 404

    # Usar el primer periodo como referencia de fechas
    periodo_base = periodos[0]
    semanas_por_pagina = calcular_fechas_semanales(periodo_base)

    tokens_totales = 0
    earnings_per_page = defaultdict(lambda: {"tokens": 0, "percentage": 0})

    # Validar si `date_filter` es una fecha válida
    date_filter_obj = None
    if date_filter:
        try:
            date_filter_obj = datetime.strptime(date_filter, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400

    # Recorrer páginas y calcular distribución de ganancias
    for page_name, weeks in semanas_por_pagina.items():
        for week, date_range in weeks.items():
            start_date = date_range["start"]
            end_date = date_range["end"]

            # Construir la consulta base
            earnings_query = Earning.query.filter(
                Earning.page_name == page_name,
                Earning.date >= start_date,
                Earning.date <= end_date,
            )

            # Filtrar por modelo si se especifica `nickname`
            if nickname:
                earnings_query = earnings_query.filter(Earning.nickname == nickname)

            # Filtrar por día específico si se especifica `date_filter`
            if date_filter_obj:
                earnings_query = earnings_query.filter(Earning.date == date_filter_obj)

            # Obtener los datos
            earnings_list = earnings_query.all()

            for e in earnings_list:
                # Acumulamos tokens por página
                earnings_per_page[page_name]["tokens"] += e.tokens
                tokens_totales += e.tokens

    # Calcular el porcentaje de cada página
    if tokens_totales > 0:
        for page in earnings_per_page:
            earnings_per_page[page]["percentage"] = round(
                (earnings_per_page[page]["tokens"] / tokens_totales) * 100, 2
            )

    return jsonify(
        {
            "total_tokens": tokens_totales,
            "earnings_distribution": earnings_per_page,
            "filtered_nickname": nickname if nickname else "All Models",
            "filtered_date": date_filter if date_filter else "Full Period",
        }
    )


@earnings_bp.route("/goal_progress", methods=["GET"])
def progreso_meta():
    periodo_nombre = request.args.get("periodo")

    if not periodo_nombre:
        return jsonify({"error": "Se requiere un periodo"}), 400

    # Obtener todos los periodos del mes
    periodos = (
        Periodo.query.filter(Periodo.nombre.like(f"{periodo_nombre}%"))
        .order_by(Periodo.nombre)
        .all()
    )

    if not periodos:
        return jsonify({"error": "Periodo no encontrado"}), 404

    # Usar el primer periodo como referencia para las fechas
    periodo_base = periodos[0]
    semanas_por_pagina = calcular_fechas_semanales(periodo_base)
    meta_mensual = periodo_base.meta_periodo  # Meta del mes desde la DB

    # Definir metas parciales
    meta_por_semana = meta_mensual / 4  # 4 semanas
    meta_por_periodo = meta_mensual / 2  # 2 periodos de dos semanas

    # Inicializar contadores de tokens generados
    tokens_totales = 0
    tokens_por_semana = defaultdict(int)
    tokens_por_periodo = [0, 0]  # Para los dos periodos de 2 semanas

    # Recorrer cada página y calcular tokens por semana
    for page_name, weeks in semanas_por_pagina.items():
        for i, (week, date_range) in enumerate(weeks.items()):
            start_date = date_range["start"]
            end_date = date_range["end"]

            # Obtener ganancias en este rango
            earnings_list = Earning.query.filter(
                Earning.page_name == page_name,
                Earning.date >= start_date,
                Earning.date <= end_date,
            ).all()

            # Sumar tokens de esta semana
            tokens_semana = sum(e.tokens for e in earnings_list)
            tokens_por_semana[week] += tokens_semana
            tokens_totales += tokens_semana

            # Sumar al periodo correcto (dos periodos de 2 semanas)
            if i < 2:
                tokens_por_periodo[0] += tokens_semana  # Primer periodo (2 semanas)
            else:
                tokens_por_periodo[1] += tokens_semana  # Segundo periodo (2 semanas)

    # Calcular porcentajes de cumplimiento
    porcentaje_mensual = (
        (tokens_totales / meta_mensual) * 100 if meta_mensual > 0 else 0
    )
    porcentaje_por_semana = {
        week: (tokens / meta_por_semana) * 100 if meta_por_semana > 0 else 0
        for week, tokens in tokens_por_semana.items()
    }
    porcentaje_por_periodo = [
        (tokens / meta_por_periodo) * 100 if meta_por_periodo > 0 else 0
        for tokens in tokens_por_periodo
    ]

    return jsonify(
        {
            "meta_mensual": meta_mensual,
            "tokens_totales_generados": tokens_totales,
            "porcentaje_cumplimiento_mensual": round(porcentaje_mensual, 2),
            "meta_por_semana": meta_por_semana,
            "tokens_por_semana": tokens_por_semana,
            "porcentaje_por_semana": porcentaje_por_semana,
            "meta_por_periodo": meta_por_periodo,
            "tokens_por_periodo": {
                "primer_periodo": tokens_por_periodo[0],
                "segundo_periodo": tokens_por_periodo[1],
            },
            "porcentaje_por_periodo": {
                "primer_periodo": round(porcentaje_por_periodo[0], 2),
                "segundo_periodo": round(porcentaje_por_periodo[1], 2),
            },
        }
    )
