"""POIs semilla de Chile (datos de demostración / bootstrap).

Solo se usan de forma explícita (ENABLE_POI_SEED_FALLBACK=true). No se mezclan con datos reales.
"""
from typing import Any, Dict, List

SEED_POIS: List[Dict[str, Any]] = [
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
