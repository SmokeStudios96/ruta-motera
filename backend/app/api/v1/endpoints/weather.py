from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.weather import WeatherScanRequest, WeatherScanResponse
from app.services.weather_service import weather_service

router = APIRouter(prefix="/weather", tags=["Weather & Biker Risk Analysis"])

# ==========================================
# MODELO DE ALERTA CLIMÁTICA GEOLOCALIZADA
# ==========================================
class WeatherAlertResponse(BaseModel):
    id: str = Field(..., description="ID único de la alerta")
    title: str = Field(..., description="Título de la alerta climática")
    macrozone: str = Field(..., description="Macrozona de Chile afectada")
    location_name: str = Field(..., description="Nombre del sector, ruta o paso fronterizo")
    lat: float = Field(..., description="Latitud de la alerta")
    lng: float = Field(..., description="Longitud de la alerta")
    risk_level: str = Field(..., description="Nivel de riesgo: BAJO, MODERADO, ALTO, CRITICO")
    condition: str = Field(..., description="Condición meteorológica principal")
    description: str = Field(..., description="Descripción detallada del peligro para motociclistas")
    recommendations: List[str] = Field(..., description="Recomendaciones de seguridad vial")
    active: bool = Field(True, description="Estado de vigencia de la alerta")
    valid_until: str = Field(..., description="Fecha y hora de vigencia estimada")

# ==========================================
# SEED DATA: Alertas Climáticas Geolocalizadas de Chile
# ==========================================
CHILE_WEATHER_ALERTS = [
    {
        "id": "alert-ng-01",
        "title": "Alerta por Viento Blanco y Altura Extrema",
        "macrozone": "Norte Grande",
        "location_name": "Ruta 11-CH Putre - Tambo Quemado (Paso Fronterizo)",
        "lat": -18.1750,
        "lng": -69.3450,
        "risk_level": "ALTO",
        "condition": "Snow / Wind",
        "description": "Rachas de viento blanco por encima de los 4.200 msnm con formación esporádica de placas de hielo en curvas cerradas.",
        "recommendations": [
            "Transitar únicamente en horario diurno (10:00 a 16:00 hrs).",
            "Uso obligatorio de ropa térmica y revisión de carburación/inyección en altura."
        ],
        "active": True,
        "valid_until": "2026-10-15T23:59:00Z"
    },
    {
        "id": "alert-ng-02",
        "title": "Neblina Costera Densa (Camanchaca)",
        "macrozone": "Norte Grande",
        "location_name": "Ruta 1 Costera Antofagasta - Iquique (Sector Tocopilla)",
        "lat": -22.0833,
        "lng": -70.2000,
        "risk_level": "MODERADO",
        "condition": "Fog",
        "description": "Camanchaca muy densa durante las primeras horas de la mañana con humedad sobre la calzada asfáltica.",
        "recommendations": [
            "Encender luces rompeniebla y mantener velocidad moderada.",
            "Evitar adelantamientos en curvas con acantilado."
        ],
        "active": True,
        "valid_until": "2026-10-13T12:00:00Z"
    },
    {
        "id": "alert-nc-01",
        "title": "Viento Moderado a Fuerte en Cuesta",
        "macrozone": "Norte Chico",
        "location_name": "Cuesta Las Cardas - Ruta 5 Norte",
        "lat": -30.2500,
        "lng": -71.3800,
        "risk_level": "MODERADO",
        "condition": "Wind",
        "description": "Rachas cruzadas de viento sur-poniente que afectan la estabilidad de motocicletas con maletas laterales cargadas.",
        "recommendations": [
            "Sujetar firmemente el manillar y mantener velocidad constante.",
            "Atención al cruzar por sectores de quebradas abiertas."
        ],
        "active": True,
        "valid_until": "2026-10-14T18:00:00Z"
    },
    {
        "id": "alert-zc-01",
        "title": "Alerta por Sistema Frontal y Lluvia en Santiago",
        "macrozone": "Zona Central",
        "location_name": "Autopista Vespucio Sur y Ruta 68 Santiago - Valparaíso",
        "lat": -33.4500,
        "lng": -70.6667,
        "risk_level": "ALTO",
        "condition": "Rain",
        "description": "Primeras horas de lluvia intensa con acumulación de aceite y combustible en las vías urbanas eINTERurbanas.",
        "recommendations": [
            "Extremar precaución en pasos bajo nivel y enlaces viales.",
            "Evitar frenadas bruscas sobre pintura vial mojada."
        ],
        "active": True,
        "valid_until": "2026-10-14T10:00:00Z"
    },
    {
        "id": "alert-zc-02",
        "title": "Peligro de Hielo en Alta Montaña",
        "macrozone": "Zona Central",
        "location_name": "Ruta 60-CH Los Libertadores (Caracoles)",
        "lat": -32.8300,
        "lng": -70.0800,
        "risk_level": "CRITICO",
        "condition": "Ice / Freezing",
        "description": "Temperaturas bajo 0°C en curvas de alta montaña con presencia de hielo negro invisible en sectores de umbría.",
        "recommendations": [
            "No transitar sin neumáticos con especificación M+S o cadenas si lo exige Carabineros.",
            "Suspender viaje en moto si la temperatura desciende de 0°C."
        ],
        "active": True,
        "valid_until": "2026-10-15T12:00:00Z"
    },
    {
        "id": "alert-zs-01",
        "title": "Alerta por Lluvia Persistente y Viento Sur",
        "macrozone": "Zona Sur",
        "location_name": "Ruta 5 Sur tramo Temuco - Valdivia",
        "lat": -39.2000,
        "lng": -72.5000,
        "risk_level": "ALTO",
        "condition": "Heavy Rain",
        "description": "Precipitaciones continuas con formación de pozas de agua en la calzada y riesgo de aquaplaning en tramos rectos.",
        "recommendations": [
            "Usar traje impermeable de alta visibilidad reflectante.",
            "Aumentar al doble la distancia de seguridad con respecto al vehículo precedente."
        ],
        "active": True,
        "valid_until": "2026-10-15T20:00:00Z"
    },
    {
        "id": "alert-pat-01",
        "title": "Alerta Roja por Vientos Patagónicos Extremos",
        "macrozone": "Patagonia",
        "location_name": "Ruta 7 Carretera Austral Norte (Sector Chaitén - Puyuhuapi)",
        "lat": -44.5000,
        "lng": -72.7000,
        "risk_level": "CRITICO",
        "condition": "Severe Gale",
        "description": "Rachas de viento huracanado superiores a 85 km/h bajando por fiordos y cordillera. Imposible mantener la moto en línea recta.",
        "recommendations": [
            "DETENER LA MARCHA INMEDIATAMENTE en refugios o localidades cercanas.",
            "No exponerse en puentes colgantes ni zonas de bosques con riesgo de caída de ramas."
        ],
        "active": True,
        "valid_until": "2026-10-14T22:00:00Z"
    },
    {
        "id": "alert-pat-02",
        "title": "Precaución por Ripio Suelto y Barro Post-Lluvia",
        "macrozone": "Patagonia",
        "location_name": "Ruta 9 Punta Arenas - Puerto Natales / Parque Torres del Paine",
        "lat": -51.7333,
        "lng": -72.5000,
        "risk_level": "ALTO",
        "condition": "Gravel / Mud",
        "description": "Sectores en obras y tramos de ripio suelto con barro profundo debido a recientes deshielos y precipitaciones.",
        "recommendations": [
            "Conducir de pie sobre las estriberas con peso retrasado.",
            "Desconectar ABS trasero (si la moto lo permite) para mejor frenado en tierra."
        ],
        "active": True,
        "valid_until": "2026-10-16T18:00:00Z"
    }
]

@router.get("/alerts", response_model=List[WeatherAlertResponse], summary="Obtener alertas climáticas geolocalizadas de Chile")
def get_weather_alerts(
    macrozone: Optional[str] = Query(None, description="Filtrar por macrozona (Norte Grande, Norte Chico, Zona Central, Zona Sur, Patagonia)"),
    risk_level: Optional[str] = Query(None, description="Filtrar por nivel de riesgo (MODERADO, ALTO, CRITICO)")
):
    """
    Devuelve la lista masiva y robusta de alertas climáticas geolocalizadas específicas para motociclistas distribuidas en todas las macrozonas de Chile.
    """
    try:
        filtered = CHILE_WEATHER_ALERTS
        if macrozone:
            filtered = [a for a in filtered if a["macrozone"].lower() == macrozone.lower()]
        if risk_level:
            filtered = [a for a in filtered if a["risk_level"].upper() == risk_level.upper()]
        return filtered
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener alertas climáticas: {str(e)}"
        )

@router.post("/scan-route", response_model=WeatherScanResponse, summary="Escanear ruta meteorológicamente para motociclistas")
def scan_route_weather(payload: WeatherScanRequest):
    """
    Analiza el clima actual y evalúa los riesgos específicos para motociclistas (lluvia, viento lateral,
    temperaturas críticas de asfalto/hipotermia y visibilidad) a lo largo de una lista de waypoints de una ruta.
    """
    try:
        if not payload.waypoints or len(payload.waypoints) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe proporcionar al menos un waypoint (lat, lng) para analizar la ruta."
            )
            
        result = weather_service.scan_route(
            waypoints=payload.waypoints,
            route_name=payload.route_name
        )
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al realizar el escaneo meteorológico de la ruta: {str(e)}"
        )

@router.get("/scan-route", response_model=WeatherScanResponse, summary="Escanear ruta meteorológicamente mediante query params")
def scan_route_weather_get(
    lat: float,
    lng: float,
    name: Optional[str] = "Punto de Ruta Único"
):
    """
    Endpoint GET /weather/scan-route para pruebas rápidas o evaluación de un punto clave de la ruta.
    """
    try:
        from app.schemas.weather import RouteWaypoint
        waypoints = [RouteWaypoint(lat=lat, lng=lng, name=name)]
        result = weather_service.scan_route(waypoints=waypoints, route_name=name)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en escaneo GET: {str(e)}"
        )
