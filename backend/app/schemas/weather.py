from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RouteWaypoint(BaseModel):
    lat: float = Field(..., description="Latitud")
    lng: float = Field(..., description="Longitud")
    name: Optional[str] = Field(None, description="Nombre o descripción del punto")

class WeatherScanRequest(BaseModel):
    waypoints: List[RouteWaypoint] = Field(..., description="Lista de puntos de paso de la ruta (lat, lng)")
    route_name: Optional[str] = Field(None, description="Nombre opcional de la ruta")

class WeatherCondition(BaseModel):
    temp_celsius: float = Field(..., description="Temperatura actual en °C")
    feels_like_celsius: float = Field(..., description="Sensación térmica en °C")
    condition: str = Field(..., description="Descripción del clima (ej: Clear, Rain, Snow, Thunderstorm, Fog)")
    condition_code: int = Field(..., description="Código de condición meteorológica")
    precipitation_mm: float = Field(..., description="Precipitación en mm/h")
    wind_speed_kmh: float = Field(..., description="Velocidad del viento en km/h")
    wind_gust_kmh: Optional[float] = Field(None, description="Ráfagas de viento en km/h")
    humidity_percent: int = Field(..., description="Humedad relativa %")
    visibility_km: float = Field(..., description="Visibilidad en km")

class BikerRiskEvaluation(BaseModel):
    risk_level: str = Field(..., description="Nivel de riesgo general: 'BAJO', 'MODERADO', 'ALTO', 'CRITICO'")
    risk_score: int = Field(..., description="Puntuación numérica de riesgo de 0 a 100")
    warnings: List[str] = Field(..., description="Lista de advertencias y peligros específicos para motociclistas")
    recommendations: List[str] = Field(..., description="Consejos de conducción segura específicos para estas condiciones")
    can_ride: bool = Field(..., description="Indica si es seguro o viable rodar bajo estas condiciones")

class RoutePointAnalysis(BaseModel):
    lat: float
    lng: float
    name: Optional[str] = None
    weather: WeatherCondition
    biker_evaluation: BikerRiskEvaluation

class WeatherScanResponse(BaseModel):
    route_name: Optional[str] = None
    total_points_analyzed: int
    overall_risk_level: str = Field(..., description="Riesgo máximo encontrado en toda la ruta")
    overall_can_ride: bool = Field(..., description="True si toda la ruta es viable (sin riesgo crítico)")
    summary_message: str = Field(..., description="Resumen general del análisis meteorológico de la ruta")
    points: List[RoutePointAnalysis]
    ai_biker_advice: Optional[str] = Field(None, description="Consejo experto de Agno/Gemini para la ruta completa")
