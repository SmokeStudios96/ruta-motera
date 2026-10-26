'use client';

import { useState, useEffect, useRef } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { 
  Fuel, 
  Utensils, 
  Bed, 
  ShieldAlert, 
  Compass, 
  Send, 
  Bot, 
  User, 
  MapPin, 
  Navigation, 
  AlertTriangle, 
  Sparkles,
  Menu,
  X,
  Layers,
  CloudSun
} from 'lucide-react';

interface POI {
  id: string;
  name: string;
  category: 'fuel' | 'restaurant' | 'hotel' | 'workshop';
  lat: number;
  lng: number;
  rating?: number;
  description?: string;
  address?: string;
}

interface WeatherAlert {
  id: string;
  title: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  lat: number;
  lng: number;
  description: string;
}

interface ChatMessage {
  id: string;
  sender: 'user' | 'agent';
  text: string;
  timestamp: string;
}

const MOCK_POIS: POI[] = [
  { id: '1', name: 'Bencinera Copec Asfalto Total', category: 'fuel', lat: -33.4489, lng: -70.6693, rating: 4.8, description: 'Alta octanaje 97, compresor de aire y café 24/7.', address: 'Av. Libertador Bernardo O\'Higgins 1200' },
  { id: '2', name: 'Parador El Motorista Errante', category: 'restaurant', lat: -33.4569, lng: -70.6483, rating: 4.9, description: 'Comida casera contundente, estacionamiento vigilado para motos.', address: 'Ruta 68 Km 18' },
  { id: '3', name: 'Hotel Biker Lodge Cordillera', category: 'hotel', lat: -33.4189, lng: -70.6093, rating: 4.7, description: 'Garaje cerrado bajo techo, herramientas básicas y lavado de cascos.', address: 'Camino a Farellones 4500' },
  { id: '4', name: 'Taller & Auxilio Ruta Sur', category: 'workshop', lat: -33.4889, lng: -70.6893, rating: 4.9, description: 'Vulcanización especializada en neumáticos tubeless y cadenas.', address: 'Panamericana Sur Km 12' },
  { id: '5', name: 'Shell Estación Cordillera', category: 'fuel', lat: -33.4289, lng: -70.6393, rating: 4.5, description: 'Cafetería y punto de encuentro rutero.', address: 'Av. Vitacura 3400' }
];

const MOCK_ALERTS: WeatherAlert[] = [
  { id: 'a1', title: 'Alerta Viento Blanco / Ráfagas Fuertes', severity: 'high', lat: -33.4100, lng: -70.5900, description: 'Precaución en curvas de alta montaña por vientos cruzados superiores a 65 km/h.' },
  { id: 'a2', title: 'Peligro Placa de Hielo Matutina', severity: 'critical', lat: -33.3900, lng: -70.5500, description: 'Suelo resbaladizo en sectores sombríos antes de las 10:00 AM.' }
];

export default function RutaMoteraHome() {
  const mapContainerRef = useRef<HTMLDivElement | null>(null);
  const mapInstanceRef = useRef<mapboxgl.Map | null>(null);
  const markersRef = useRef<mapboxgl.Marker[]>([]);

  const [mapboxToken, setMapboxToken] = useState<string>(
    process.env.NEXT_PUBLIC_MAPBOX_TOKEN || 'pk.eyJ1IjoicnV0YW1vdGVyYSIsImEiOiJjbHN2Z3R4OGkwMnBlMmptZmVxNWc2aW8wIn0.placeholder'
  );
  const [tokenInput, setTokenInput] = useState<string>('');
  const [showTokenModal, setShowTokenModal] = useState<boolean>(false);
  const [activeCategory, setActiveCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedPoi, setSelectedPoi] = useState<POI | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(true);
  const [isChatOpen, setIsChatOpen] = useState<boolean>(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [isAgentThinking, setIsAgentThinking] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<'map' | 'routes' | 'community'>('map');

  // Inicializar chat inicial en useEffect para evitar render estático con new Date()
  useEffect(() => {
    setChatMessages([
      {
        id: '1',
        sender: 'agent',
        text: '¡Saludos, motorista! Soy tu Agente del Reporte Rutero. ¿En qué ruta te encuentras o qué necesitas verificar hoy?',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
    ]);
  }, []);

  // Inicializar Mapa Mapbox GL JS
  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (!mapboxToken || mapboxToken.includes('placeholder')) {
      setShowTokenModal(true);
      return;
    }

    mapboxgl.accessToken = mapboxToken;

    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: 'mapbox://styles/mapbox/dark-v11',
      center: [-70.6693, -33.4489],
      zoom: 11,
    });

    mapInstanceRef.current = map;

    map.addControl(new mapboxgl.NavigationControl(), 'top-right');
    map.addControl(new mapboxgl.GeolocateControl({
      positionOptions: { enableHighAccuracy: true },
      trackUserLocation: true,
      showUserHeading: true
    }), 'top-right');

    return () => {
      map.remove();
    };
  }, [mapboxToken]);

  // Actualizar Marcadores en el Mapa según filtros y búsqueda
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map) return;

    markersRef.current.forEach(marker => marker.remove());
    markersRef.current = [];

    const filteredPois = MOCK_POIS.filter(poi => {
      const matchesCategory = activeCategory === 'all' || poi.category === activeCategory;
      const matchesSearch = poi.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                            (poi.description && poi.description.toLowerCase().includes(searchQuery.toLowerCase()));
      return matchesCategory && matchesSearch;
    });

    filteredPois.forEach(poi => {
      const el = document.createElement('div');
      el.className = 'custom-marker';
      
      let bgIconColor = 'bg-amber-500';
      let iconSymbol = '⛽';
      if (poi.category === 'fuel') { bgIconColor = 'bg-amber-500'; iconSymbol = '⛽'; }
      if (poi.category === 'restaurant') { bgIconColor = 'bg-orange-600'; iconSymbol = '🍴'; }
      if (poi.category === 'hotel') { bgIconColor = 'bg-yellow-600'; iconSymbol = '🏨'; }
      if (poi.category === 'workshop') { bgIconColor = 'bg-zinc-700'; iconSymbol = '🔧'; }

      el.innerHTML = `
        <div class="w-10 h-10 rounded-full ${bgIconColor} border-2 border-zinc-900 shadow-lg flex items-center justify-center text-lg cursor-pointer transform hover:scale-110 transition-transform">
          ${iconSymbol}
        </div>
      `;

      el.addEventListener('click', () => {
        setSelectedPoi(poi);
        map.flyTo({ center: [poi.lng, poi.lat], zoom: 14, essential: true });
      });

      const marker = new mapboxgl.Marker(el)
        .setLngLat([poi.lng, poi.lat])
        .setPopup(new mapboxgl.Popup({ offset: 25 }).setHTML(`
          <div class="p-2 bg-zinc-900 text-zinc-100 rounded border border-amber-500/30 max-w-xs font-sans">
            <h3 class="font-bold text-amber-400 text-sm">${poi.name}</h3>
            <p class="text-xs text-zinc-300 mt-1">${poi.description || ''}</p>
            <div class="mt-2 text-xs text-amber-300 font-semibold">★ ${poi.rating || 4.8} / 5.0</div>
          </div>
        `))
        .addTo(map);

      markersRef.current.push(marker);
    });

    MOCK_ALERTS.forEach(alert => {
      const el = document.createElement('div');
      el.className = 'alert-marker';
      el.innerHTML = `
        <div class="w-10 h-10 rounded-full bg-red-600 animate-pulse border-2 border-amber-400 shadow-xl flex items-center justify-center text-lg cursor-pointer transform hover:scale-110 transition-transform">
          ⚠️
        </div>
      `;

      el.addEventListener('click', () => {
        map.flyTo({ center: [alert.lng, alert.lat], zoom: 13, essential: true });
      });

      const marker = new mapboxgl.Marker(el)
        .setLngLat([alert.lng, alert.lat])
        .setPopup(new mapboxgl.Popup({ offset: 25 }).setHTML(`
          <div class="p-2 bg-zinc-900 text-zinc-100 rounded border border-red-500 max-w-xs font-sans">
            <h3 class="font-bold text-red-400 text-sm flex items-center gap-1">⚠️ ${alert.title}</h3>
            <p class="text-xs text-zinc-300 mt-1">${alert.description}</p>
          </div>
        `))
        .addTo(map);

      markersRef.current.push(marker);
    });

  }, [activeCategory, searchQuery]);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMsgText = inputMessage;
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: userMsgText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setChatMessages(prev => [...prev, userMsg]);
    setInputMessage('');
    setIsAgentThinking(true);

    setTimeout(() => {
      let agentReplyText = "He analizado las condiciones actuales para tu ruta. Las rutas cordilleranas presentan buen agarre pero atención al viento lateral en las cumbres.";
      
      const lower = userMsgText.toLowerCase();
      if (lower.includes('bencina') || lower.includes('gasolina') || lower.includes('combustible')) {
        agentReplyText = "⛽ Para combustible de alto octanaje (97), te recomiendo la Bencinera Copec Asfalto Total en Av. O'Higgins o la estación Shell Cordillera. Ambas con excelente servicio y aire para neumáticos.";
      } else if (lower.includes('hotel') || lower.includes('dormir') || lower.includes('alojar') || lower.includes('descansar')) {
        agentReplyText = "🏨 El Hotel Biker Lodge Cordillera cuenta con estacionamiento vigilado bajo techo y herramientas básicas para ajuste de cadena. Ideal para pernoctar con total tranquilidad.";
      } else if (lower.includes('clima') || lower.includes('tiempo') || lower.includes('lluvia') || lower.includes('viento')) {
        agentReplyText = "⚠️ Alerta climática activa: Se reportan ráfagas fuertes de viento blanco en la ruta hacia Farellones y posible placa de humedad en zonas sombrías. Conduce con precaución y revisa la presión.";
      } else if (lower.includes('taller') || lower.includes('mecanico') || lower.includes('pinchazo')) {
        agentReplyText = "🔧 Taller & Auxilio Ruta Sur en Panamericana Km 12 está abierto 24 horas para asistencia de emergencia y reparación de neumáticos tubeless.";
      }

      const agentMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'agent',
        text: agentReplyText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setChatMessages(prev => [...prev, agentMsg]);
      setIsAgentThinking(false);
    }, 1200);
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#09090b] text-zinc-100 font-sans">
      
      {showTokenModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-[#18181b] border border-amber-500/40 rounded-xl p-6 max-w-md w-full shadow-2xl">
            <div className="flex items-center gap-3 mb-4">
              <Compass className="w-8 h-8 text-amber-500 animate-spin" />
              <h2 className="text-xl font-bold text-amber-400">Configurar Mapbox Token</h2>
            </div>
            <p className="text-sm text-zinc-300 mb-4">
              Para visualizar el mapa interactivo Dark Biker de RutaMotera, ingresa tu Public Access Token de Mapbox (o usa el predeterminado de demostración).
            </p>
            <input 
              type="text" 
              placeholder="pk.eyJ1I..." 
              value={tokenInput} 
              onChange={(e) => setTokenInput(e.target.value)}
              className="w-full bg-[#09090b] border border-zinc-700 rounded-lg px-4 py-2 text-sm text-zinc-100 focus:outline-none focus:border-amber-500 mb-4"
            />
            <div className="flex justify-end gap-3">
              <button 
                onClick={() => {
                  if (tokenInput.trim()) setMapboxToken(tokenInput.trim());
                  setShowTokenModal(false);
                }}
                className="bg-amber-600 hover:bg-amber-500 text-zinc-950 font-bold px-5 py-2 rounded-lg text-sm transition-colors shadow-lg"
              >
                Cargar Mapa
              </button>
            </div>
          </div>
        </div>
      )}

      {/* BARRA LATERAL (SIDEBAR) ESTÉTICA DARK BIKER */}
      <aside className={`fixed inset-y-0 left-0 z-40 w-80 bg-[#18181b] border-r border-zinc-800 flex flex-col transition-transform duration-300 ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0`}>
        <div className="p-4 border-b border-zinc-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center shadow-lg shadow-amber-500/20">
              <Compass className="w-6 h-6 text-zinc-950" />
            </div>
            <div>
              <h1 className="font-black tracking-wider text-lg bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">RUTA MOTERA</h1>
              <p className="text-[10px] text-zinc-400 tracking-widest uppercase">Dark Biker Navigator</p>
            </div>
          </div>
          <button 
            onClick={() => setIsSidebarOpen(false)} 
            className="md:hidden text-zinc-400 hover:text-zinc-100"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="flex border-b border-zinc-800 bg-[#09090b]">
          <button 
            onClick={() => setActiveTab('map')} 
            className={`flex-1 py-3 text-xs font-bold tracking-wider uppercase flex items-center justify-center gap-2 border-b-2 transition-colors ${activeTab === 'map' ? 'border-amber-500 text-amber-400 bg-[#18181b]' : 'border-transparent text-zinc-400 hover:text-zinc-200'}`}
          >
            <Layers className="w-4 h-4" /> Mapa
          </button>
          <button 
            onClick={() => setActiveTab('routes')} 
            className={`flex-1 py-3 text-xs font-bold tracking-wider uppercase flex items-center justify-center gap-2 border-b-2 transition-colors ${activeTab === 'routes' ? 'border-amber-500 text-amber-400 bg-[#18181b]' : 'border-transparent text-zinc-400 hover:text-zinc-200'}`}
          >
            <Navigation className="w-4 h-4" /> Rutas
          </button>
          <button 
            onClick={() => setActiveTab('community')} 
            className={`flex-1 py-3 text-xs font-bold tracking-wider uppercase flex items-center justify-center gap-2 border-b-2 transition-colors ${activeTab === 'community' ? 'border-amber-500 text-amber-400 bg-[#18181b]' : 'border-transparent text-zinc-400 hover:text-zinc-200'}`}
          >
            <Sparkles className="w-4 h-4" /> Radar
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {activeTab === 'map' && (
            <>
              <div className="relative">
                <input 
                  type="text" 
                  placeholder="Buscar bencineras, paradores..." 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-[#09090b] border border-zinc-700 rounded-lg pl-9 pr-4 py-2.5 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-amber-500"
                />
                <MapPin className="w-4 h-4 text-zinc-500 absolute left-3 top-3" />
              </div>

              <div>
                <h3 className="text-xs font-bold tracking-wider text-zinc-400 uppercase mb-3">Filtros Esenciales</h3>
                <div className="grid grid-cols-2 gap-2">
                  <button 
                    onClick={() => setActiveCategory('all')}
                    className={`p-2.5 rounded-lg border text-xs font-semibold flex items-center gap-2 transition-all ${activeCategory === 'all' ? 'bg-amber-500/10 border-amber-500 text-amber-400' : 'bg-[#09090b] border-zinc-800 text-zinc-400 hover:border-zinc-700'}`}
                  >
                    <Compass className="w-4 h-4 text-amber-500" /> Todos
                  </button>
                  <button 
                    onClick={() => setActiveCategory('fuel')}
                    className={`p-2.5 rounded-lg border text-xs font-semibold flex items-center gap-2 transition-all ${activeCategory === 'fuel' ? 'bg-amber-500/10 border-amber-500 text-amber-400' : 'bg-[#09090b] border-zinc-800 text-zinc-400 hover:border-zinc-700'}`}
                  >
                    <Fuel className="w-4 h-4 text-amber-500" /> Bencineras
                  </button>
                  <button 
                    onClick={() => setActiveCategory('restaurant')}
                    className={`p-2.5 rounded-lg border text-xs font-semibold flex items-center gap-2 transition-all ${activeCategory === 'restaurant' ? 'bg-orange-600/10 border-orange-600 text-orange-400' : 'bg-[#09090b] border-zinc-800 text-zinc-400 hover:border-zinc-700'}`}
                  >
                    <Utensils className="w-4 h-4 text-orange-500" /> Restaurantes
                  </button>
                  <button 
                    onClick={() => setActiveCategory('hotel')}
                    className={`p-2.5 rounded-lg border text-xs font-semibold flex items-center gap-2 transition-all ${activeCategory === 'hotel' ? 'bg-yellow-600/10 border-yellow-600 text-yellow-400' : 'bg-[#09090b] border-zinc-800 text-zinc-400 hover:border-zinc-700'}`}
                  >
                    <Bed className="w-4 h-4 text-yellow-500" /> Hoteles Biker
                  </button>
                  <button 
                    onClick={() => setActiveCategory('workshop')}
                    className={`p-2.5 rounded-lg border text-xs font-semibold flex items-center gap-2 col-span-2 transition-all ${activeCategory === 'workshop' ? 'bg-zinc-700/20 border-zinc-500 text-zinc-200' : 'bg-[#09090b] border-zinc-800 text-zinc-400 hover:border-zinc-700'}`}
                  >
                    <ShieldAlert className="w-4 h-4 text-zinc-400" /> Talleres & Auxilio
                  </button>
                </div>
              </div>

              <div className="pt-2">
                <h3 className="text-xs font-bold tracking-wider text-zinc-400 uppercase mb-3 flex items-center gap-2">
                  <CloudSun className="w-4 h-4 text-amber-500" /> Alertas en Ruta
                </h3>
                <div className="space-y-2">
                  {MOCK_ALERTS.map(alert => (
                    <div key={alert.id} className="bg-[#09090b] border border-red-500/30 rounded-lg p-3 hover:border-red-500 transition-colors">
                      <div className="flex items-center gap-2 text-red-400 font-bold text-xs">
                        <AlertTriangle className="w-4 h-4" /> {alert.title}
                      </div>
                      <p className="text-[11px] text-zinc-300 mt-1 leading-relaxed">{alert.description}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-2">
                <h3 className="text-xs font-bold tracking-wider text-zinc-400 uppercase mb-3">Puntos de Interés Cercanos</h3>
                <div className="space-y-2">
                  {MOCK_POIS.map(poi => (
                    <div 
                      key={poi.id} 
                      onClick={() => {
                        setSelectedPoi(poi);
                        const map = mapInstanceRef.current;
                        if (map) map.flyTo({ center: [poi.lng, poi.lat], zoom: 14, essential: true });
                      }}
                      className="bg-[#09090b] border border-zinc-800 hover:border-amber-500/50 rounded-lg p-3 cursor-pointer transition-all group"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-xs text-zinc-200 group-hover:text-amber-400 transition-colors">{poi.name}</span>
                        <span className="text-[10px] bg-amber-500/10 text-amber-400 px-2 py-0.5 rounded border border-amber-500/30">★ {poi.rating}</span>
                      </div>
                      <p className="text-[11px] text-zinc-400 mt-1 line-clamp-1">{poi.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

          {activeTab === 'routes' && (
            <div className="space-y-3">
              <h3 className="text-xs font-bold tracking-wider text-zinc-400 uppercase">Rutas Recomendadas Motoristas</h3>
              <div className="bg-[#09090b] border border-amber-500/30 rounded-lg p-3 hover:border-amber-500 transition-colors cursor-pointer">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs text-amber-400">Ruta Los Libertadores (Caracoles)</span>
                  <span className="text-[10px] text-zinc-400">142 km</span>
                </div>
                <p className="text-[11px] text-zinc-300 mt-1">29 curvas míticas en alta cordillera con vistas panorámicas excepcionales.</p>
              </div>
              <div className="bg-[#09090b] border border-zinc-800 rounded-lg p-3 hover:border-amber-500/50 transition-colors cursor-pointer">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs text-zinc-200">Circuito Costero Ruta 5 / Zapallar</span>
                  <span className="text-[10px] text-zinc-400">98 km</span>
                </div>
                <p className="text-[11px] text-zinc-300 mt-1">Curvas junto al Océano Pacífico, brisa marina y asfalto en óptimas condiciones.</p>
              </div>
            </div>
          )}

          {activeTab === 'community' && (
            <div className="space-y-3">
              <h3 className="text-xs font-bold tracking-wider text-zinc-400 uppercase">Radar Motero en Vivo</h3>
              <div className="bg-[#09090b] border border-zinc-800 rounded-lg p-3">
                <div className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping" />
                  <span className="text-xs font-bold text-zinc-200">Comando Cordillera (8 motoristas)</span>
                </div>
                <p className="text-[11px] text-zinc-400 mt-1">Rodando rumbo a Portillo. Sin novedades mecánicas.</p>
              </div>
              <div className="bg-[#09090b] border border-zinc-800 rounded-lg p-3">
                <div className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-amber-500" />
                  <span className="text-xs font-bold text-zinc-200">Escuadrón Sur (4 motoristas)</span>
                </div>
                <p className="text-[11px] text-zinc-400 mt-1">Parada técnica en Bencinera Copec.</p>
              </div>
            </div>
          )}
        </div>

        <div className="p-4 border-t border-zinc-800 bg-[#09090b] flex items-center justify-between text-xs text-zinc-400">
          <span>RutaMotera v2.5</span>
          <span className="text-amber-500 font-semibold">Online</span>
        </div>
      </aside>

      {/* CONTENEDOR PRINCIPAL Y MAPA */}
      <main className="flex-1 flex flex-col h-screen md:ml-80 relative">
        <header className="absolute top-4 left-4 z-30 flex items-center gap-3">
          <button 
            onClick={() => setIsSidebarOpen(true)} 
            className="md:hidden bg-[#18181b] border border-zinc-800 p-2.5 rounded-xl text-amber-500 shadow-xl hover:bg-zinc-800 transition-colors"
          >
            <Menu className="w-5 h-5" />
          </button>
        </header>

        <div ref={mapContainerRef} className="flex-1 w-full h-full" />

        {/* PANEL FLOTANTE AGENTE DEL REPORTE RUTERO (IA) */}
        <div className="absolute bottom-6 right-6 z-30 flex flex-col items-end">
          {!isChatOpen && (
            <button 
              onClick={() => setIsChatOpen(true)}
              className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-400 hover:to-orange-500 text-zinc-950 font-black px-5 py-3.5 rounded-2xl shadow-2xl flex items-center gap-3 transform hover:scale-105 transition-all border border-amber-300/30"
            >
              <Bot className="w-6 h-6 animate-pulse" />
              <div className="text-left">
                <div className="text-xs uppercase tracking-wider font-extrabold">Reporte Rutero</div>
                <div className="text-[10px] opacity-80">Consultar Agente AI</div>
              </div>
            </button>
          )}

          {isChatOpen && (
            <div className="w-[90vw] sm:w-[380px] h-[500px] bg-[#18181b] border border-amber-500/40 rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-5 duration-300">
              <div className="bg-[#09090b] p-4 border-b border-zinc-800 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-amber-500/20 border border-amber-500 flex items-center justify-center text-amber-400">
                    <Bot className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-bold text-sm text-amber-400">Agente Reporte Rutero</h3>
                    <p className="text-[10px] text-zinc-400">Asistente IA Dark Biker</p>
                  </div>
                </div>
                <button 
                  onClick={() => setIsChatOpen(false)}
                  className="text-zinc-400 hover:text-zinc-100 p-1"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="flex-1 p-4 overflow-y-auto space-y-3 bg-[#09090b]/50">
                {chatMessages.map(msg => (
                  <div 
                    key={msg.id} 
                    className={`flex items-start gap-2.5 ${msg.sender === 'user' ? 'flex-row-reverse' : ''}`}
                  >
                    <div className={`w-7 h-7 rounded-full flex items-center justify-center shrink-0 ${msg.sender === 'user' ? 'bg-amber-600 text-zinc-950 font-bold text-xs' : 'bg-zinc-800 text-amber-400 border border-amber-500/30'}`}>
                      {msg.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                    </div>
                    <div className={`max-w-[75%] rounded-xl p-3 text-xs leading-relaxed ${msg.sender === 'user' ? 'bg-amber-600 text-zinc-950 font-medium rounded-tr-none' : 'bg-[#18181b] border border-zinc-800 text-zinc-200 rounded-tl-none'}`}>
                      <p>{msg.text}</p>
                      <span className={`block text-[9px] mt-1 text-right ${msg.sender === 'user' ? 'text-zinc-900/70' : 'text-zinc-500'}`}>{msg.timestamp}</span>
                    </div>
                  </div>
                ))}
                {isAgentThinking && (
                  <div className="flex items-center gap-2 text-zinc-400 text-xs italic p-2">
                    <Bot className="w-4 h-4 animate-spin text-amber-500" />
                    <span>Analizando ruta y condiciones meteorológicas...</span>
                  </div>
                )}
              </div>

              <form onSubmit={handleSendMessage} className="p-3 bg-[#09090b] border-t border-zinc-800 flex items-center gap-2">
                <input 
                  type="text" 
                  placeholder="Pregunta sobre bencina, clima, rutas..." 
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  className="flex-1 bg-[#18181b] border border-zinc-700 rounded-xl px-4 py-2.5 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-amber-500"
                />
                <button 
                  type="submit"
                  className="bg-amber-500 hover:bg-amber-400 text-zinc-950 p-2.5 rounded-xl font-bold transition-colors shadow-lg"
                >
                  <Send className="w-4 h-4" />
                </button>
              </form>
            </div>
          )}
        </div>

      </main>

    </div>
  );
}
