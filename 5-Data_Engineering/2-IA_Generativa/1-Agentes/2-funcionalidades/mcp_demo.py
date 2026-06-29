"""
============================================================================
 MCP (Model Context Protocol) 
============================================================================

¿POR QUÉ UN SCRIPT Y NO EL NOTEBOOK?
 Para usar un servidor MCP por "stdio" hay que LANZARLO como un subproceso.
 Jupyter en Windows usa un bucle de eventos (SelectorEventLoop) que NO permite
 crear subprocesos, por eso el notebook daba:
     NotImplementedError ... / UnsupportedOperation: fileno
 Ejecutado como script, Windows usa el ProactorEventLoop (que SÍ soporta
 subprocesos) y todo funciona. Este script ya lo fuerza por si acaso.

----------------------------------------------------------------------------
 PREPARACIÓN (una vez)
----------------------------------------------------------------------------
   pip install mcp openai

 (Opcional) Para la demo del AGENTE necesitas una clave de Groq u OpenRouter.
 Puedes ponerla como variable de entorno para no escribirla cada vez:
   Windows (CMD):        set GROQ_API_KEY=gsk_tu_clave
   Windows (PowerShell): $env:GROQ_API_KEY="gsk_tu_clave"
 Si no la pones, el programa te la pedirá solo cuando haga falta.

----------------------------------------------------------------------------
 EJECUTAR
----------------------------------------------------------------------------
   python mcp_demo.py
============================================================================
"""

import os
import sys
import json
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_OK = True
except ImportError:
    MCP_OK = False

CODIGO_SERVIDOR = r'''
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("HerramientasDelCurso")

@mcp.tool()
def sumar(a: float, b: float) -> float:
    "Suma dos números y devuelve el resultado."
    return a + b

@mcp.tool()
def multiplicar(a: float, b: float) -> float:
    "Multiplica dos números y devuelve el resultado."
    return a * b

@mcp.tool()
def hora_actual() -> str:
    "Devuelve la fecha y la hora actuales."
    from datetime import datetime
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

@mcp.tool()
def precio_producto(nombre: str) -> str:
    "Consulta el precio en euros de un producto de la tienda."
    catalogo = {"portátil": 799, "ratón": 19, "monitor": 229}
    for clave, precio in catalogo.items():
        if clave in nombre.lower():
            return f"{clave}: {precio} euros"
    return "Producto no encontrado."

if __name__ == "__main__":
    mcp.run(transport="stdio")
'''

SERVIDOR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "servidor_mcp.py")


def guardar_servidor():
    with open(SERVIDOR_PATH, "w", encoding="utf-8") as f:
        f.write(CODIGO_SERVIDOR)

def server_params():
    return StdioServerParameters(command=sys.executable, args=[SERVIDOR_PATH])


PROVEEDOR = "groq"
if PROVEEDOR == "groq":
    BASE_URL, MODELO, ENV_KEY = "https://api.groq.com/openai/v1", "llama-3.3-70b-versatile", "GROQ_API_KEY"
else:
    BASE_URL, MODELO, ENV_KEY = "https://openrouter.ai/api/v1", "meta-llama/llama-3.3-70b-instruct:free", "OPENROUTER_API_KEY"

_cliente = None


def get_cliente():
    """Crea el cliente del modelo la primera vez que se usa."""
    global _cliente
    if _cliente is None:
        from openai import OpenAI
        from getpass import getpass
        api_key = os.environ.get(ENV_KEY) or getpass(f"Pega tu clave ({PROVEEDOR}): ")
        _cliente = OpenAI(api_key=api_key, base_url=BASE_URL)
    return _cliente


def mcp_a_openai(tool):
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": tool.inputSchema or {"type": "object", "properties": {}},
        },
    }


async def demo_listar():
    print("\n=== 1. HERRAMIENTAS DEL SERVIDOR ===")
    async with stdio_client(server_params()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            lista = (await session.list_tools()).tools
            for t in lista:
                print(f"  - {t.name}: {t.description}")


async def demo_llamar():
    print("\n=== 2. LLAMAR UNA HERRAMIENTA A MANO ===")
    async with stdio_client(server_params()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            res = await session.call_tool("sumar", arguments={"a": 12, "b": 30})
            print("Resultado de sumar(12, 30):", res.content[0].text)


async def demo_agente(pregunta, max_pasos=5):
    cliente = get_cliente()
    async with stdio_client(server_params()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = [mcp_a_openai(t) for t in (await session.list_tools()).tools]

            mensajes = [
                {"role": "system", "content": "Eres un asistente que usa herramientas cuando hace falta."},
                {"role": "user", "content": pregunta},
            ]
            for paso in range(1, max_pasos + 1):
                resp = cliente.chat.completions.create(
                    model=MODELO, messages=mensajes, tools=tools, tool_choice="auto", temperature=0)
                msg = resp.choices[0].message

                if not msg.tool_calls:
                    return msg.content

                mensajes.append({
                    "role": "assistant", "content": msg.content,
                    "tool_calls": [{"id": tc.id, "type": "function",
                                    "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                                   for tc in msg.tool_calls],
                })
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments or "{}")
                    res = await session.call_tool(tc.function.name, arguments=args)
                    texto = res.content[0].text if res.content else ""
                    print(f"   [Paso {paso}] 🛠️  {tc.function.name}({args}) → {texto}")
                    mensajes.append({"role": "tool", "tool_call_id": tc.id, "content": texto})
            return "He alcanzado el límite de pasos."


def correr_agente():
    print("\n=== 3. EL AGENTE USA EL SERVIDOR MCP ===")
    print("(Esta demo usa el modelo, así que necesita tu clave de API.)")
    pregunta = input("\nEscribe tu pregunta (Enter para una de ejemplo): ").strip() \
        or "¿Cuánto es 1234 por 5678? Y dime también la hora actual."
    print("\nPensando...\n")
    respuesta = asyncio.run(demo_agente(pregunta))
    print("\nRESPUESTA FINAL:\n")
    print(respuesta)


def main():
    print("=" * 64)
    print(" MCP (Model Context Protocol) — script de prácticas")
    print("=" * 64)

    if not MCP_OK:
        print("\nNo encuentro el SDK de MCP. Instálalo primero con:")
        print("     pip install mcp openai")
        return

    guardar_servidor()
    print(f"\nServidor MCP escrito en: {SERVIDOR_PATH}")

    opciones = {
        "1": ("Listar las herramientas del servidor", lambda: asyncio.run(demo_listar())),
        "2": ("Llamar una herramienta a mano (sumar)", lambda: asyncio.run(demo_llamar())),
        "3": ("El agente usa el servidor (necesita clave)", correr_agente),
    }

    while True:
        print("\n" + "-" * 64)
        print("¿Qué quieres probar?")
        for k, (nombre, _) in opciones.items():
            print(f"  {k}) {nombre}")
        print("  0) Salir")
        eleccion = input("\nElige una opción: ").strip()

        if eleccion == "0":
            print("¡Hasta luego!")
            break
        accion = opciones.get(eleccion)
        if accion is None:
            print("Opción no válida, prueba otra vez.")
            continue
        try:
            accion[1]()
        except Exception as e:
            print(f"\nAlgo ha fallado: {type(e).__name__}: {e}")
            print("   Comprueba que instalaste 'mcp' y 'openai', y tu clave de API.")


if __name__ == "__main__":
    main()
