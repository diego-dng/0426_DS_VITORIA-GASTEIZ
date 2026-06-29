# MCP — Model Context Protocol


Esta guía explica qué es **MCP**, para qué sirve y cómo encaja con todo lo que ya hemos visto sobre agentes y *function calling*. Al final tienes las instrucciones para probarlo tú mismo/a con el script `mcp_demo.py`.

---

## 1. La idea en una frase

> **MCP es un "enchufe universal" para conectar herramientas y datos a la IA.**

La analogía del **USB-C**: antes cada aparato tenía su propio cargador; con USB-C, un mismo cable vale para todo. **MCP es el USB-C de las herramientas de IA**: una forma estándar de que *cualquier* asistente se conecte a *cualquier* herramienta.

Es un **estándar abierto** que hoy usan multitud de aplicaciones y herramientas.

---

## 2. El problema que resuelve

En los notebooks anteriores dimos herramientas a nuestro agente de dos formas:

- Escribiéndolas **a mano** (una función para el tiempo, otra para divisas…).
- Con una **plataforma** como Composio (muchas integraciones ya hechas).

El problema: si cada modelo y cada plataforma tiene **su propia manera** de conectar herramientas, todo el mundo acaba reinventando lo mismo. Si creas una herramienta para una app, no sirve directamente para otra.

**MCP pone de acuerdo a todos:** defines una herramienta **una vez** como "servidor MCP", y la puede usar **cualquier** cliente compatible (tu agente, Claude Desktop, Cursor, VS Code…).

---

## 3. La arquitectura: cliente y servidor

MCP tiene dos piezas que se hablan entre sí:

| Pieza | Qué es | Ejemplos |
|-------|--------|----------|
| **Servidor MCP** | Un programa que **ofrece** herramientas y datos. | Un servidor de archivos, de GitHub, de una base de datos, o uno que hagas tú. |
| **Cliente MCP** | Quien **usa** esas herramientas (normalmente con un LLM detrás). | Tu agente en Python, Claude Desktop, Cursor… |

A veces se habla también del **host**: la aplicación que contiene al cliente (por ejemplo, el programa de Claude Desktop es el host; dentro tiene un cliente MCP).

```
   [ LLM + Cliente MCP ]  <--- protocolo MCP --->  [ Servidor MCP ]  ---> (archivos, APIs, BBDD…)
        tu agente                                     ofrece herramientas
```

---

## 4. Qué ofrece un servidor MCP

Un servidor puede exponer **tres tipos de cosas**. La forma fácil de recordarlo es compararlo con una API web:

| Primitiva | Para qué sirve | Analogía web |
|-----------|----------------|--------------|
| **Tools** (herramientas) | **Ejecutar acciones**: calcular, enviar un correo, crear un archivo… | Como un `POST` (hace algo) |
| **Resources** (recursos) | **Aportar datos/contexto** al modelo: el contenido de un archivo, una ficha… | Como un `GET` (lee algo) |
| **Prompts** (plantillas) | **Plantillas de instrucciones** reutilizables que el servidor sugiere. | Como recetas guardadas |

---

## 5. ¿Cómo viajan los mensajes?"

MCP puede funcionar de dos maneras según dónde esté el servidor:


- **HTTP**: el servidor corre como un **servicio web** (local o en internet) y el cliente se conecta por una URL. Ideal para servidores **remotos** o compartidos.

> **Aviso importante (Windows + Jupyter):** el transporte *stdio* necesita **lanzar un subproceso**, y **Jupyter en Windows no lo permite** (da errores como `NotImplementedError` o `UnsupportedOperation: fileno`). **Por eso MCP se prueba con un script `.py`, no en el notebook.** Ejecutado como script, Windows usa el bucle de eventos adecuado y funciona sin problemas.

---

## 6. MCP y el *function calling*: cómo encajan

MCP **no sustituye** al function calling que ya conoces; se apoya en él. El flujo es:

1. El cliente pregunta al servidor: *"¿qué herramientas tienes?"* (`list_tools`).
2. El cliente **traduce** esas herramientas al formato de *function calling* del modelo.
3. El modelo decide cuál usar (igual que siempre).
4. El cliente le pide al servidor que la ejecute (`call_tool`) y le devuelve el resultado al modelo.

Es decir: **MCP es la "fontanería" estandarizada** para descubrir y ejecutar herramientas; el *function calling* sigue siendo la forma en que el modelo las pide.

---

## 7. MCP vs. Composio: ¿cuál uso?

No compiten, se complementan:

| | **Composio** | **MCP** |
|---|---|---|
| Qué es | Una **plataforma** con apps y login gestionado | Un **estándar abierto** de conexión |
| Ideal para | Conectar rápido apps reales (Gmail, GitHub…) | Que cualquier IA hable con cualquier herramienta |
| Quién ejecuta | Composio, en su nube | El servidor MCP (tuyo o de terceros) |

De hecho, Composio **ofrece** su propio servidor MCP. En la práctica usarás el que mejor encaje en cada proyecto.

---

## 8. MCP en el mundo real

No hace falta programar todos los servidores: ya existen **muchísimos** listos para usar. Algunos típicos:

- **Filesystem** — leer y escribir archivos de tu ordenador.
- **Fetch / web** — descargar páginas web.
- **GitHub, Slack, Google Drive, Postgres…** — conectar con apps y bases de datos.

Y del lado del **cliente**, aplicaciones como **Claude Desktop**, **Cursor** o **VS Code** te permiten **añadir** estos servidores con un archivo de configuración: al instante, el asistente "gana" esas herramientas. Muchos servidores se lanzan con `uvx` (Python).

---

## 9. Seguridad

Dar herramientas MCP a un agente es **darle poder**, así que con cabeza:

- **Confía solo en servidores que conozcas.** Un servidor MCP puede hacer cosas reales (borrar archivos, enviar mensajes).
- **Empieza con permisos mínimos** y herramientas de **solo lectura**.
- **Cuidado con la inyección de *prompts*:** si una herramienta devuelve texto de una web o un documento, trátalo como **datos**, nunca como **órdenes** que el agente deba obedecer.
- **Pon límites** (un máximo de pasos) para que el agente no se descontrole.

---

## 10. Cómo probarlo (script `mcp_demo.py`)

### Preparación (una sola vez)
```bash
pip install mcp openai
```
Para la demo del agente necesitas una clave gratuita de **Groq** (recomendado) u OpenRouter. Puedes ponerla como variable de entorno para no escribirla cada vez:
```bash
# Windows (CMD)
set GROQ_API_KEY=gsk_tu_clave
# Windows (PowerShell)
$env:GROQ_API_KEY="gsk_tu_clave"
```

### Ejecutar
```bash
python mcp_demo.py
```

Aparecerá un **menú** con tres pruebas:

1. **Listar las herramientas del servidor** — el cliente se conecta y pregunta qué ofrece el servidor (verás `sumar`, `multiplicar`, `hora_actual`, `precio_producto`).
2. **Llamar una herramienta a mano** — invoca `sumar(12, 30)` directamente (sin LLM), para ver el mecanismo.
3. **El agente usa el servidor** — aquí el **modelo decide** qué herramientas usar para responder a tu pregunta (esta opción sí usa tu clave de API).

> El script escribe automáticamente el archivo del servidor (`mi_servidor_mcp.py`) a su lado. Para el **reto**, edita el texto `CODIGO_SERVIDOR` dentro del script (añade una herramienta nueva, p. ej. `restar`) y vuelve a ejecutarlo.

---


