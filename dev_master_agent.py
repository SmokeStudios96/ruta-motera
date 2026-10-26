#!/usr/bin/env python3
"""
RutaMotera - Lead Software Engineer Autonomous Agent
Powered by Agno & Local Ollama (Qwen2.5-Coder)
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Carga de variables de entorno desde .env
load_dotenv()

# Importaciones de Agno
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.file import FileTools
from agno.tools.shell import ShellTools

# 1. Configuración del espacio de trabajo
WORKSPACE_DIR = Path.cwd()

# 2. Inicialización de Herramientas del sistema de archivos y consola
file_tools = FileTools(base_dir=WORKSPACE_DIR)
shell_tools = ShellTools(base_dir=WORKSPACE_DIR)

# 3. Selección y configuración del Modelo Ollama Local
# Lee desde tu .env (por defecto: qwen2.5-coder:latest)
OLLAMA_MODEL_ID = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:latest")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

model = Ollama(
    id=OLLAMA_MODEL_ID,
    host=OLLAMA_HOST,
)

# 4. Instrucciones del Sistema para el Lead Software Engineer
SYSTEM_INSTRUCTIONS = f"""
Eres el "Lead Software Engineer & Software Architect" autónomo a cargo del desarrollo de la plataforma 'RutaMotera'.
Tu objetivo es implementar código de calidad de producción directamente en el sistema de archivos del proyecto.

### DIRECTORIO DE TRABAJO:
Estás operando en la raíz del proyecto: {WORKSPACE_DIR}

### REGLA CRÍTICA DE EJECUCIÓN DE HERRAMIENTAS (ANTI-JSON TEXT):
1. INVOCACIÓN NATIVA: NUNCA respondas en el chat con bloques de texto plano o cadenas JSON del tipo '{{"name": "...", "arguments": ...}}'. 
2. ACCIÓN REAL: Si necesitas leer o escribir un archivo, DEBES invocar la herramienta interna provista ('save_file', 'read_file'). No muestres el JSON de la llamada, ejecútala directamente.
3. COMPATIBILIDAD CON WINDOWS: Usa siempre rutas relativas estándar con barras diagonales normales '/' (por ejemplo: 'backend/app/core/config.py').
4. CÓDIGO COMPLETO: No dejes placeholders ni comentarios como '// aquí va el resto'. Escribe el código 100% completo con imports, tipado y manejo de errores.

### ARQUITECTURA TÉCNICA OBLIGATORIA:
1. FRONTEND:
   - Framework: Next.js 15 (App Router con React 19).
   - Estilos: Tailwind CSS con estética "Dark Biker / Heritage / Neo-Retro" (zinc oscuro #09090b, negro asfalto #18181b, acentos ámbar cálido #f59e0b).
   - Mapas: Mapbox GL JS (`mapbox-gl`) con capas GeoJSON.
   - Ubicación: Subdirectorio `./frontend/`

2. BACKEND & SERVICIOS:
   - Framework: Python 3.11+, FastAPI, Pydantic v2, Uvicorn.
   - Agente de IA para clima y rutas moteras con Agno.
   - Despliegue objetivo: Render Web Service (incluir Dockerfile y render.yaml).
   - Ubicación: Subdirectorio `./backend/`

3. BASE DE DATOS (YA DESPLEGADA EN SUPABASE):
   - PostgreSQL con PostGIS, tabla `pois` con columna `location` tipo GEOMETRY(Point, 4326).
   - Enum poi_category: 'scenic_curve', 'biker_restaurant', 'mechanic', 'gas_station', 'biker_hotel', 'camping'.
   - Función RPC: `get_nearby_pois(user_lng, user_lat, radius_meters, filter_category)` que retorna lat, lng, distance_meters.
"""

# 5. Creación de la instancia del Agente
lead_agent = Agent(
    name="RutaMotera Lead Engineer",
    model=model,
    tools=[file_tools, shell_tools],
    instructions=[SYSTEM_INSTRUCTIONS],
    markdown=True,
)


def run_interactive_mode():
    """Modo consola interactiva para desarrollo con Ollama local."""
    print("=" * 70)
    print("🏍️  RUTAMOTERA - DEV MASTER AGENT (Agno + Qwen2.5-Coder Local) EN LÍNEA")
    print(f"📁 Workspace: {WORKSPACE_DIR}")
    print(f"🧠 Modelo: {OLLAMA_MODEL_ID} en {OLLAMA_HOST}")
    print("Escribe tu instrucción o requerimiento. Escribe 'salir' o 'exit' para terminar.")
    print("=" * 70 + "\n")

    while True:
        try:
            user_input = input("\n[Lead Dev Prompt] ❯ ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "salir", "quit"]:
                print("\n👋 Cerrando sesión de desarrollo local. ¡Buenas rutas!")
                break

            print("\n⚙️  Qwen2.5-Coder local está analizando y ejecutando cambios...\n")
            lead_agent.print_response(user_input, stream=True)

        except KeyboardInterrupt:
            print("\n\nOperación interrumpida por el usuario.")
            break
        except Exception as e:
            print(f"\n❌ Error durante la ejecución del agente: {e}")


def run_single_task(task_prompt: str):
    """Ejecución de tarea única por línea de comando."""
    print(f"\n🚀 Ejecutando tarea local: '{task_prompt}'\n")
    lead_agent.print_response(task_prompt, stream=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        run_single_task(task)
    else:
        run_interactive_mode()