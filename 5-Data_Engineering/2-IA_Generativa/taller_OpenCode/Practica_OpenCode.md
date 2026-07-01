# Taller práctico: crear y probar herramientas en OpenCode


> **Punto de partida:** ya tienes OpenCode **instalado** y con tu **clave de API** conectada (Groq u OpenRouter). Aquí vamos a **crear y probar** las piezas que personalizan OpenCode: **comandos, skills, herramientas propias, permisos y plugins**.

Cada laboratorio sigue el mismo patrón: **crea el archivo → reinicia OpenCode → pruébalo → mira qué debería pasar.**

---

## 0. Preparación

Crea una carpeta de prácticas, entra y arranca OpenCode para inicializarla:

```bash
mkdir practica-opencode && cd practica-opencode
opencode
```
Dentro de OpenCode, ejecuta:
```
/init
```
Sal con `Ctrl+C` (o `/exit`). Vamos a crear archivos y, para que OpenCode los detecte, **tendrás que reiniciarlo** después de cada laboratorio.

### Estructura que vamos a ir creando
Todo lo personalizado vive en una carpeta **`.opencode/`** dentro de tu proyecto:
```
practica-opencode/
├─ opencode.json              ← configuración (permisos, etc.)
├─ AGENTS.md                  ← normas del proyecto (creado por /init)
└─ .opencode/
   ├─ commands/<nombre>.md    ← comandos  (/nombre)
   ├─ skills/<nombre>/SKILL.md← skills
   ├─ tools/<nombre>.ts       ← herramientas propias
   └─ plugins/<nombre>.ts     ← plugins
```

> **Regla de oro:** cada vez que crees o edites un archivo en `.opencode/`, **cierra y vuelve a abrir OpenCode** para que lo cargue.

---

## 1- Un comando (`/comando`)

**Qué es:** un atajo para un prompt que repites a menudo.

### Crear
Crea el archivo **`.opencode/commands/revisar.md`** con este contenido:

```markdown
---
description: Revisa un archivo y sugiere mejoras (sin cambiar nada)
---

Revisa el código del archivo @$ARGUMENTS.
Sugiéreme 3 mejoras concretas y explica por qué. No modifiques nada todavía.
```

- El **nombre del archivo** (`revisar`) será el comando: `/revisar`.
- `$ARGUMENTS` se sustituye por lo que escribas después del comando.
- `@archivo` hace que OpenCode incluya el contenido de ese archivo.

### Probar
1. Crea un archivo cualquiera para revisar, p. ej. `ejemplo.py`:
   ```python
   def f(x):
       return x*2+1
   ```
2. Reinicia OpenCode (`opencode`).
3. Escribe:
   ```
   /revisar ejemplo.py
   ```

### Qué deberías ver
OpenCode lee `ejemplo.py` y te da 3 sugerencias (nombres más claros, type hints, docstring…), **sin tocar el archivo**.

> **Variante pro (salida de un comando):** puedes inyectar la salida de un comando de terminal con `` !`comando` ``. Crea `.opencode/commands/commit-msg.md`:
> ```markdown
> ---
> description: Propón un mensaje de commit a partir de los cambios
> ---
>
> Cambios actuales:
> !`git diff --staged`
>
> Propón un mensaje de commit claro en español (estilo Conventional Commits).
> ```
> Tras hacer `git add`, prueba `/commit-msg`.

---

## 2 - Una skill (`SKILL.md`)

**Qué es:** un "manual" de **cómo** hacer una tarea a tu manera. El agente lo carga **solo cuando encaja**.

### Crear
Crea el archivo **`.opencode/skills/documentar-funcion/SKILL.md`** (¡la carpeta debe llamarse igual que el `name`!):

```markdown
---
name: documentar-funcion
description: Documenta funciones de Python con docstrings estilo Google y type hints, sin cambiar la lógica
---

## Qué hago
- Añado un docstring estilo Google (secciones Args, Returns, Raises).
- Añado type hints a los parámetros y al valor de retorno.
- NO cambio la lógica de la función.

## Cuándo usarme
Úsame cuando se pida documentar o añadir docstrings a código Python.
```

Reglas: `name` y `description` son obligatorios, el `name` va en minúsculas-con-guiones y **coincide con el nombre de la carpeta**. El archivo se llama **`SKILL.md`** (mayúsculas).

### Probar
1. Reinicia OpenCode.
2. Con el `ejemplo.py` de antes, pide:
   ```
   documenta la función de @ejemplo.py
   ```

### Qué deberías ver
El agente **carga tu skill** (verás una llamada a la herramienta `skill`) y documenta la función siguiendo **tu estilo** (docstring Google + type hints), sin cambiar la lógica.

---

## 3 - Una herramienta propia (custom tool)

**Qué es:** una **acción nueva** que el agente puede ejecutar. Se define en un archivo `.ts`.

### Crear
Crea el archivo **`.opencode/tools/dado.ts`** (el nombre del archivo será el nombre de la herramienta):

```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Tira un dado con el número de caras indicado y devuelve el resultado.",
  args: {
    caras: tool.schema.number().describe("Número de caras del dado, por ejemplo 6 o 20"),
  },
  async execute(args) {
    const resultado = Math.floor(Math.random() * args.caras) + 1
    return `Has sacado un ${resultado} (dado de ${args.caras} caras).`
  },
})
```

> No necesitas instalar nada: `@opencode-ai/plugin` viene incluido en OpenCode.

### Probar
1. Reinicia OpenCode.
2. Pide:
   ```
   Tira un dado de 20 caras
   ```

### Qué deberías ver
El agente llama a tu herramienta **`dado`** con `caras: 20` y te da un número del 1 al 20. (Si no la usa, sé explícito: *"usa la herramienta dado con 20 caras"*.)

> **Variante (varias herramientas en un archivo):** si exportas varias, el nombre será `<archivo>_<export>`. Por ejemplo, en `.opencode/tools/mates.ts` con `export const sumar = tool({...})` se crea la herramienta `mates_sumar`.

> **Variante avanzada (tu herramienta llama a Python):** el `.ts` solo es la "ficha"; dentro puede ejecutar un script en cualquier lenguaje con `Bun.$`. Útil si quieres reutilizar código Python tuyo.

---

## 4 - Permisos de herramientas

**Qué es:** controlar qué herramientas se ejecutan solas, cuáles **piden permiso** y cuáles están prohibidas.

### Crear
Crea el archivo **`opencode.json`** en la raíz del proyecto:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "bash": "ask",
    "edit": "ask"
  }
}
```

- `ask` → te pide confirmación antes de actuar.
- `allow` → sin preguntar · `deny` → prohibido.

### Probar
1. Reinicia OpenCode.
2. Pide algo que requiera la terminal, por ejemplo:
   ```
   Lista los archivos del proyecto y dime cuántos hay
   ```

### Qué deberías ver
Antes de ejecutar `bash`, OpenCode **te pide permiso** (Aceptar / Rechazar). Lo mismo si intenta editar un archivo. Es tu **red de seguridad** para trabajar tranquilo.

---

## 5 - Un plugin

**Qué es:** **código** que se "engancha" a los eventos de OpenCode para cambiar su comportamiento. Aquí haremos uno que **impide leer archivos `.env`** (protección de secretos).

### Crear
Crea el archivo **`.opencode/plugins/proteger-env.ts`**:

```typescript
export const ProtegerEnv = async ({ project, client, $, directory, worktree }) => {
  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool === "read" && output.args.filePath.includes(".env")) {
        throw new Error("Bloqueado: no se permite leer archivos .env")
      }
    },
  }
}
```

Este plugin se ejecuta **antes de cada herramienta** (`tool.execute.before`); si detecta que se va a leer un `.env`, lo corta.

### Probar
1. Crea un archivo `.env` con un secreto de mentira:
   ```bash
   echo "API_KEY=secreto-de-prueba-123" > .env
   ```
2. Reinicia OpenCode.
3. Pide:
   ```
   Lee el archivo .env y dime qué contiene
   ```

### Qué deberías ver
El intento de leer `.env` **falla** con tu mensaje ("Bloqueado…"), y el agente **no llega a ver el secreto**. Acabas de modificar el comportamiento de OpenCode con unas líneas.

> Los plugins también pueden **añadir herramientas**, **avisarte al terminar una tarea** o **inyectar variables de entorno**. Y se pueden instalar desde npm añadiéndolos en `opencode.json` con `"plugin": ["nombre-del-paquete"]`.

---

## Chuleta: dónde va cada cosa

| Pieza | Archivo | Se usa con |
|-------|---------|------------|
| **Comando** | `.opencode/commands/<n>.md` | `/n` |
| **Skill** | `.opencode/skills/<n>/SKILL.md` | el agente la carga sola |
| **Herramienta** | `.opencode/tools/<n>.ts` | el agente la llama (o se la pides) |
| **Permisos** | `opencode.json` → `permission` | automático |
| **Plugin** | `.opencode/plugins/<n>.ts` | automático (eventos) |

**Recuerda:**
- Tras crear/editar archivos en `.opencode/`, **reinicia OpenCode**.
- Para usarlo en **equipo**, sube `.opencode/`, `opencode.json` y `AGENTS.md` a **Git**: todos compartirán los mismos comandos, skills, tools y plugins.



Referencias: https://opencode.ai/docs/custom-tools · https://opencode.ai/docs/skills · https://opencode.ai/docs/commands · https://opencode.ai/docs/plugins · https://opencode.ai/docs/permissions


