from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from uuid import uuid4
from supabase import Client
from app.core.supabase import get_supabase
from app.schemas.poi import POICreate, POIUpdate, POIResponse, POINearbyQuery

router = APIRouter(prefix="/pois", tags=["Points of Interest (POIs)"])

# ==========================================
# SEED DATA: Puntos de Interés Macrozona de Chile
# ==========================================
CHILE_MACROZONE_POIS = [
    # --- NORTE GRANDE (Arica, Iquique, Antofagasta, San Pedro de Atacama) ---
    {
        "id": "poi-ng-01",
        "name": "Copec 93 Octanos - Acceso Arica",
        "description": "Estación de servicio principal con combustible de 93 y 97 octanos, aire para neumáticos y tienda de conveniencia Pronto Copec. Punto clave antes de iniciar la Ruta Costera o subida a Putre.",
        "category": "gasolinera",
        "lat": -18.4783,
        "lng": -70.3126,
        "address": "Av. Comandante San Martín 1500, Arica",
        "rating": 4.8,
        "metadata": {
            "macrozone": "Norte Grande",
            "octanes": [93, 97, "Diesel"],
            "services": ["Aire comprimido", "Tienda Pronto", "Estacionamiento vigilado"],
            "biker_friendly": True,
            "mechanic_onsite": False
        }
    },
    {
        "id": "poi-ng-02",
        "name": "Enduro & Moto Workshop Putre",
        "description": "Taller mecánico de alta montaña especializado en inyección electrónica, ajuste de suspensión para altura extrema y reparación de pinchazos en ruta.",
        "category": "taller",
        "lat": -18.2015,
        "lng": -69.5578,
        "address": "Bolognesi 120, Putre",
        "rating": 4.9,
        "metadata": {
            "macrozone": "Norte Grande",
            "specialties": ["Inyección en altura", "Pinchazos tubeless", "Repuestos BMW / KTM / Honda"],
            "emergency_phone": "+56 9 8765 4321",
            "biker_friendly": True
        }
    },
    {
        "id": "poi-ng-03",
        "name": "Hostal Biker Rutas del Desierto Iquique",
        "description": "Alojamiento con estacionamiento cerrado bajo techo, kit de herramientas básico disponible, lavandería y zona de lavado de motos.",
        "category": "hostal_motero",
        "lat": -20.2133,
        "lng": -70.1503,
        "address": "Av. Arturo Prat 850, Iquique",
        "rating": 4.7,
        "metadata": {
            "macrozone": "Norte Grande",
            "secure_parking": True,
            "tool_kit": True,
            "biker_friendly": True
        }
    },
    {
        "id": "poi-ng-04",
        "name": "Petrobras Premium 97 Octanos Antofagasta Centro",
        "description": "Estación con alta disponibilidad de combustible de 97 octanos, zona de sombra y compresor digital de aire calibrado.",
        "category": "gasolinera",
        "lat": -23.6509,
        "lng": -70.3975,
        "address": "Av. Balmaceda 2500, Antofagasta",
        "rating": 4.6,
        "metadata": {
            "macrozone": "Norte Grande",
            "octanes": [93, 95, 97],
            "services": ["Compresor digital", "Cafetería"],
            "biker_friendly": True
        }
    },
    {
        "id": "poi-ng-05",
        "name": "Atacama Biker Lodge San Pedro",
        "description": "Refugio estratégico para motoristas exploradores del Salar de Atacama y Cordillera de la Sal. Zona de fogata y mecánico recomendado en la zona.",
        "category": "hostal_motero",
        "lat": -22.9087,
        "lng": -68.2030,
        "address": "Caracoles 310, San Pedro de Atacama",
        "rating": 4.9,
        "metadata": {
            "macrozone": "Norte Grande",
            "secure_parking": True,
            "biker_friendly": True,
            "altitude_m": 2400
        }
    },

    # --- NORTE CHICO (La Serena, Copiapó, Valle del Elqui) ---
    {
        "id": "poi-nc-01",
        "name": "Copec Full Ruta 5 Norte - La Serena",
        "description": "Estación de servicio ideal para repostar 97 octanos antes de adentrarse en la Ruta 5 Panamericana o tomar hacia el Valle del Elqui.",
        "category": "gasolinera",
        "lat": -29.9045,
        "lng": -71.2489,
        "address": "Ruta 5 Norte Km 472, La Serena",
        "rating": 4.7,
        "metadata": {
            "macrozone": "Norte Chico",
            "octanes": [93, 95, 97, "Diesel"],
            "services": ["Pronto Copec", "Baños limpios", "Aire"],
            "biker_friendly": True
        }
    },
    {
        "id": "poi-nc-02",
        "name": "Elqui Moto Service & Tyres",
        "description": "Taller especializado en cambio de neumáticos mixtos y de ruta (Metzeler, Michelin, Pirelli), balanceo computarizado y mantención general.",
        "category": "taller",
        "lat": -29.9150,
        "lng": -71.2520,
        "address": "Av. Balmaceda 1820, La Serena",
        "rating": 4.8,
        "metadata": {
            "macrozone": "Norte Chico",
            "services": ["Cambio de neumáticos", "Balanceo", "Escáner multimarca"],
            "biker_friendly": True
        }
    },
    {
        "id": "poi-nc-03",
        "name": "Hostal Riders del Valle - Vicuña",
        "description": "Hospedaje temático motero en el corazón del Valle del Elqui. Guardamoto bajo techo y recomendaciones de rutas off-road locales.",
        "category": "hostal_motero",
        "lat": -30.0275,
        "lng": -70.7082,
        "address": "Gabriela Mistral 450, Vicuña",
        "rating": 4.9,
        "metadata": {
            "macrozone": "Norte Chico",
            "secure_parking": True,
            "biker_friendly": True
        }
    },

    # --- ZONA CENTRAL (Valparaíso, Santiago, Ruta Los Libertadores) ---
    {
        "id": "poi-zc-01",
        "name": "Copec Baquedano 98 Octanos - Santiago Centro",
        "description": "Emblemática estación de servicio en Santiago con alta disponibilidad de combustible de alto octanaje y punto de encuentro de moteros los fines de semana.",
        "category": "gasolinera",
        "lat": -33.4430,
        "lng": -70.6350,
        "address": "Av. Vicuña Mackenna 20, Santiago",
        "rating": 4.9,
        "metadata": {
            "macrozone": "Zona Central",
            "octanes": [93, 95, 97],
            "services": ["Punto de encuentro motero", "Pronto Copec 24/7"],
            "biker_friendly": True
        }
    },
    {
        "id": "poi-zc-02",
        "name": "MotoPro Chile - Taller Multimarca",
        "description": "Taller mecánico líder en Santiago para mantención de alta cilindrada (BMW GS, Ducati, KTM, Triumph, Honda Africa Twin).",
        "category": "taller",
        "lat": -33.4190,
        "lng": -70.6010,
        "address": "Av. Vitacura 3500, Vitacura, Santiago",
        "rating": 4.9,
        "metadata": {
            "macrozone": "Zona Central",
            "specialties": ["Suspensiones Öhlins/WP", "Revisión 10.000km", "Scanner oficial"],
            "biker_friendly": True
        }
    },
    {
        "id": "poi-zc-03",
        "name": "Shell Costanera - Valparaíso",
        "description": "Estación de servicio frente al puerto de Valparaíso, ideal para iniciar la Ruta 68 o el camino costero hacia Concón y Ventanas.",
        "category": "gasolinera",
        "lat": -33.0472,
        "lng": -71.6127,
        "address": "Av. Errázuriz 800, Valparaíso",
        "rating": 4.7,
        "metadata": {
            "macrozone": "Zona Central",
            "octanes": [93, 95, 97],
            "biker_friendly": True
        }
    },
    {
        "id": "poi-zc-04",
        "name": "Hotel & Cabañas Los Caracoles - Los Andes (Ruta 60 CH)",
        "description": "Punto de descanso estratégico antes de enfrentar las 29 curvas del Paso Los Libertadores hacia Argentina. Estacionamiento cerrado y desayuno temprano para viajeros.",
        "category": "hostal_motero",
        "lat": -32.8328,
        "lng": -70.5976,
        "address": "Ruta 60 Ch Km 78, Los Andes",
        "rating": 4.8,
        "metadata": {
            "macrozone": "Zona Central",
            "secure_parking": True,
            "biker_friendly": True,
            "near_border_pass": True
        }
    },

    # --- ZONA SUR (Concepción, Temuco, Valdivia, Osorno) ---
    {
        "id": "poi-zs-01",
        "name": "Copec Pedro de Valdivia - Concepción",
        "description": "Estación con combustible 97 octanos y zona cubierta para revisar equipamiento ante la lluvia frecuente del sur.",
        "category": "gasolinera",
        "lat": -36.8270,
        "lng": -73.0500,
        "address": "Av. Pedro de Valdivia 900, Concepción",
        "rating": 4.7,
        "metadata": {
            "macrozone": "Zona Sur",
            "octanes": [93, 95, 97],
            "biker_friendly": True
        }
    },
    {
        "id": "poi-zs-02",
        "name": "SurMoto Taller & Accesorios - Temuco",
        "description": "Taller mecánico y tienda de indumentaria impermeable Gore-Tex y botas de aventura. Reparación de sistemas eléctricos y transmisiones.",
        "category": "taller",
        "lat": -38.7390,
        "lng": -72.5900,
        "address": "Av. Alemania 0450, Temuco",
        "rating": 4.8,
        "metadata": {
            "macrozone": "Zona Sur",
            "services": ["Equipamiento impermeable", "Taller mecánico", "Auxilio en ruta"],
            "biker_friendly": True
        }
    },
    {
        "id": "poi-zs-03",
        "name": "Valdivia Biker House & Hostal",
        "description": "Alojamiento atendido por motociclistas locales. Cuenta con taller básico de emergencia, secador de botas y ropa, y parrillada de bienvenida.",
        "category": "hostal_motero",
        "lat": -39.8196,
        "lng": -73.2452,
        "address": "Picarte 1200, Valdivia",
        "rating": 4.9,
        "metadata": {
            "macrozone": "Zona Sur",
            "secure_parking": True,
            "drying_room": True,
            "biker_friendly": True
        }
    },
    {
        "id": "poi-zs-04",
        "name": "Petrobras Osorno Centro",
        "description": "Estación clave antes de tomar la ruta internacional hacia Puyehue y el paso Cardenal Samoré.",
        "category": "gasolinera",
        "lat": -40.5725,
        "lng": -73.1353,
        "address": "Mackenna 850, Osorno",
        "rating": 4.6,
        "metadata": {
            "macrozone": "Zona Sur",
            "octanes": [93, 95, 97],
            "biker_friendly": True
        }
    },

    # --- PATAGONIA / CARRETERA AUSTRAL / CHILOÉ ---
    {
        "id": "poi-pat-01",
        "name": "Copec Puerto Montt - Km 0 Carretera Austral",
        "description": "El punto de repostaje más importante antes de embarcar hacia Chiloé o iniciar la legendaria Carretera Austral (Ruta 7). Venta de mapas offline y aditivos.",
        "category": "gasolinera",
        "lat": -41.4693,
        "lng": -72.9424,
        "address": "Av. Diego Portales 500, Puerto Montt",
        "rating": 4.9,
        "metadata": {
            "macrozone": "Patagonia",
            "octanes": [93, 95, 97, "Diesel"],
            "services": ["Pronto Copec", "Punto de partida Carretera Austral"],
            "biker_friendly": True
        }
    },
    {
        "id": "poi-pat-02",
        "name": "Hostal y Cabañas Chiloé Biker - Ancud",
        "description": "Refugio en la Isla Grande de Chiloé. Estacionamiento techado, herramientas para reapriete de maletas y tornillería tras caminos de ripio.",
        "category": "hostal_motero",
        "lat": -41.8690,
        "lng": -73.8210,
        "address": "Prat 210, Ancud",
        "rating": 4.8,
        "metadata": {
            "macrozone": "Patagonia",
            "secure_parking": True,
            "tool_kit": True,
            "biker_friendly": True
        }
    },
    {
        "id": "poi-pat-03",
        "name": "Copec Castro Chiloé",
        "description": "Gasolinera principal en Castro. Recomendado llenar estanque completo antes de avanzar hacia Chonchi y los transbordadores hacia Hornopirén o Quellón.",
        "category": "gasolinera",
        "lat": -42.4826,
        "lng": -73.7654,
        "address": "Panamericana Sur Km 1150, Castro",
        "rating": 4.7,
        "metadata": {
            "macrozone": "Patagonia",
            "octanes": [93, 95, 97],
            "biker_friendly": True
        }
    },
    {
        "id": "poi-pat-04",
        "name": "Patagonia Austral Taller & Rescue - Coyhaique",
        "description": "El taller mecánico más austral y especializado de la Carretera Austral. Soldadura de chasis, reparación de llantas con rayos y stock de cámaras de repuesto.",
        "category": "taller",
        "lat": -45.5752,
        "lng": -72.0662,
        "address": "Eusebio Lillo 420, Coyhaique",
        "rating": 5.0,
        "metadata": {
            "macrozone": "Patagonia",
            "specialties": ["Soldadura aluminio/hierro", "Reparación llantas con rayos", "Auxilio en ruta Carretera Austral"],
            "emergency_phone": "+56 9 1234 5678",
            "biker_friendly": True
        }
    },
    {
        "id": "poi-pat-05",
        "name": "Coyhaique Biker Lodge & Refugio",
        "description": "Alojamiento icónico para moteros que completan la Ruta 7 Norte o Sur. Chimenea a leña, secado de ropa técnica, espacio de taller y cervecería artesanal.",
        "category": "hostal_motero",
        "lat": -45.5810,
        "lng": -72.0715,
        "address": "Baquedano 710, Coyhaique",
        "rating": 4.9,
        "metadata": {
            "macrozone": "Patagonia",
            "secure_parking": True,
            "drying_room": True,
            "biker_friendly": True
        }
    },
    {
        "id": "poi-pat-06",
        "name": "Copec Punta Arenas - Zona Austral",
        "description": "La estación de servicio Copec más austral del continente americano. Combustible 97 octanos y punto de partida hacia el Estrecho de Magallanes y Tierra del Fuego.",
        "category": "gasolinera",
        "lat": -53.1638,
        "lng": -70.9171,
        "address": "Av. Bulnes 0650, Punta Arenas",
        "rating": 4.9,
        "metadata": {
            "macrozone": "Patagonia",
            "octanes": [93, 95, 97, "Diesel"],
            "services": ["Pronto Copec", "Punto extremo austral"],
            "biker_friendly": True
        }
    },
    {
        "id": "poi-pat-07",
        "name": "Estrecho Biker Hostel - Punta Arenas",
        "description": "Hospedaje especializado en viajeros de ruta transcontinental que cruzan hacia Ushuaia o Tierra del Fuego. Asesoramiento sobre clima patagónico y vientos extremos.",
        "category": "hostal_motero",
        "lat": -53.1543,
        "lng": -70.9112,
        "address": "O'Higgins 1150, Punta Arenas",
        "rating": 4.8,
        "metadata": {
            "macrozone": "Patagonia",
            "secure_parking": True,
            "wind_advisory_hub": True,
            "biker_friendly": True
        }
    }
]

@router.get("/", response_model=List[POIResponse])
def get_pois(
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    macrozone: Optional[str] = Query(None, description="Filtrar por macrozona de Chile"),
    limit: int = Query(100, ge=1, le=500, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Desplazamiento para paginación"),
    supabase: Client = Depends(get_supabase)
):
    """
    Obtener lista de puntos de interés (POIs) con opción de filtrado por categoría, macrozona de Chile y paginación.
    Combina datos en vivo de Supabase con nuestro set robusto de respaldo para garantizar cobertura total en Chile.
    """
    try:
        # Intentar obtener de Supabase
        query = supabase.table("pois").select("*")
        
        if category:
            query = query.eq("category", category)
            
        response = query.range(offset, offset + limit - 1).execute()
        db_pois = response.data if response.data else []

        # Si Supabase devuelve pocos o 0 POIs, o si queremos asegurar el set robusto nacional, fusionamos o devolvemos nuestro catálogo robusto filtrado
        combined_list = list(db_pois)
        db_ids = {p.get("id") for p in combined_list}

        for seed_poi in CHILE_MACROZONE_POIS:
            if seed_poi["id"] not in db_ids:
                # Aplicar filtros al seed si se especifican
                match_cat = not category or seed_poi["category"] == category
                match_mz = not macrozone or seed_poi["metadata"].get("macrozone") == macrozone
                if match_cat and match_mz:
                    combined_list.append(seed_poi)

        # Aplicar paginación final
        paginated = combined_list[offset: offset + limit]
        return paginated

    except Exception as e:
        # Fallback robusto en caso de error de conexión a Supabase
        filtered = CHILE_MACROZONE_POIS
        if category:
            filtered = [p for p in filtered if p["category"] == category]
        if macrozone:
            filtered = [p for p in filtered if p["metadata"].get("macrozone") == macrozone]
        return filtered[offset: offset + limit]

@router.post("/nearby", response_model=List[POIResponse])
def get_nearby_pois(
    body: POINearbyQuery,
    supabase: Client = Depends(get_supabase)
):
    """
    Buscar POIs cercanos utilizando la función RPC de PostGIS en Supabase o cálculo haversine local de respaldo.
    """
    try:
        rpc_params = {
            "user_lng": body.lng,
            "user_lat": body.lat,
            "radius_meters": body.radius_meters,
            "filter_category": body.category
        }
        
        response = supabase.rpc("get_nearby_pois", rpc_params).execute()
        if response.data and len(response.data) > 0:
            return response.data
    except Exception:
        pass

    # Fallback de cálculo geoespacial Haversine en memoria con el catálogo robusto de Chile
    import math
    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371000  # Radio de la tierra en metros
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lambda = math.radians(lon2 - lon1)
        a = math.sin(d_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    nearby = []
    for poi in CHILE_MACROZONE_POIS:
        if body.category and poi["category"] != body.category:
            continue
        dist = calculate_distance(body.lat, body.lng, poi["lat"], poi["lng"])
        if dist <= body.radius_meters:
            poi_copy = dict(poi)
            poi_copy["distance_meters"] = round(dist, 1)
            nearby.append(poi_copy)

    # Ordenar por cercanía
    nearby.sort(key=lambda x: x.get("distance_meters", 0))
    return nearby

@router.get("/{poi_id}", response_model=POIResponse)
def get_poi_by_id(
    poi_id: str,
    supabase: Client = Depends(get_supabase)
):
    """
    Obtener un punto de interés específico por su ID.
    """
    try:
        response = supabase.table("pois").select("*").eq("id", poi_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
    except Exception:
        pass

    # Buscar en seed data
    for poi in CHILE_MACROZONE_POIS:
        if poi["id"] == poi_id:
            return poi

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"POI con ID {poi_id} no encontrado"
    )

@router.post("/", response_model=POIResponse, status_code=status.HTTP_201_CREATED)
def create_poi(
    poi: POICreate,
    supabase: Client = Depends(get_supabase)
):
    """
    Crear un nuevo punto de interés motero.
    """
    try:
        poi_data = poi.model_dump()
        response = supabase.table("pois").insert(poi_data).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
    except Exception:
        pass

    # Fallback si Supabase no está conectado
    new_id = f"poi-custom-{uuid4().hex[:8]}"
    new_poi = poi.model_dump()
    new_poi["id"] = new_id
    new_poi["created_at"] = "2026-10-12T20:00:00Z"
    CHILE_MACROZONE_POIS.append(new_poi)
    return new_poi

@router.put("/{poi_id}", response_model=POIResponse)
def update_poi(
    poi_id: str,
    poi_update: POIUpdate,
    supabase: Client = Depends(get_supabase)
):
    """
    Actualizar un punto de interés existente.
    """
    try:
        update_data = {k: v for k, v in poi_update.model_dump().items() if v is not None}
        response = supabase.table("pois").update(update_data).eq("id", poi_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
    except Exception:
        pass

    for poi in CHILE_MACROZONE_POIS:
        if poi["id"] == poi_id:
            for k, v in poi_update.model_dump().items():
                if v is not None:
                    poi[k] = v
            return poi

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"POI con ID {poi_id} no encontrado"
    )

@router.delete("/{poi_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_poi(
    poi_id: str,
    supabase: Client = Depends(get_supabase)
):
    """
    Eliminar un punto de interés por su ID.
    """
    try:
        supabase.table("pois").delete().eq("id", poi_id).execute()
    except Exception:
        pass

    global CHILE_MACROZONE_POIS
    CHILE_MACROZONE_POIS = [p for p in CHILE_MACROZONE_POIS if p["id"] != poi_id]
    return None
