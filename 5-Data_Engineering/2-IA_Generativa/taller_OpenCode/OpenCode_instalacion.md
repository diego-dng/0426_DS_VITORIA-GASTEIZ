# Taller: instalar y usar OpenCode en local

**OpenCode** es un **agente de IA para programar** que vive en la terminal: lee tu proyecto, edita archivos, ejecuta comandos y te ayuda a desarrollar, usando el modelo de IA que tú elijas. Es de código abierto y una alternativa a herramientas como Claude Code o Cursor.

Esta guía te lleva **paso a paso** desde cero hasta tenerlo funcionando en tu ordenador.

---

## Recursos.

> **¿Necesito WSL?**
> - **Windows:** **Sí, es lo recomendado** (lo dice la propia documentación oficial). Funciona mejor y con todas las características. Más abajo te explico cómo instalarlo. *(También se puede instalar en Windows "nativo" con Scoop/Chocolatey, pero la experiencia es peor.)*
> - **macOS / Linux:** **No.** Se instala directamente.
>
> **¿Qué sistema uso en WSL?**
> - **WSL 2 con Ubuntu** (es la distribución por defecto, perfecta para esto).
>
> **¿Qué necesito sí o sí?**
> - Una **terminal** y una **clave de API** de algún proveedor de modelos 


> **Nota importante:** desde 2026, **OpenCode no puede usar los modelos de Claude/Anthropic**. Usa **Groq**, **OpenRouter**, **Google Gemini** o modelos **locales (Ollama)**. En este taller: **Groq**.

---

## 1. Instalación según tu sistema operativo

Ve directamente a tu caso: **A** (Windows con WSL, recomendado), **B** (Windows nativo), **C** (macOS) o **D** (Linux).

---

### A) Windows con WSL — **recomendado**

#### Paso 1 — Instalar WSL 2 + Ubuntu
1. Abre **PowerShell como Administrador** (botón derecho → *Ejecutar como administrador*).
2. Ejecuta:
   ```powershell
   wsl --install
   ```
   Esto instala **WSL 2** y **Ubuntu** automáticamente.
3. **Reinicia** el ordenador si te lo pide.
4. Al volver, se abrirá Ubuntu y te pedirá **crear un usuario y una contraseña** de Linux (apúntala; no se ve al escribirla, es normal).

#### Paso 2 — Actualizar Ubuntu
Dentro de la terminal de **Ubuntu**, ejecuta:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl unzip
```

#### Paso 3 — Instalar OpenCode
Sigue **dentro de Ubuntu** (no en PowerShell):
```bash
curl -fsSL https://opencode.ai/install | bash
```
Cierra y vuelve a abrir la terminal de Ubuntu para que detecte el comando.

---

### B) macOS

La forma más sencilla:
```bash
curl -fsSL https://opencode.ai/install | bash
```
O con **Homebrew** (recomendado para mantenerlo actualizado):
```bash
brew install anomalyco/tap/opencode
```

---

### D) Linux

```bash
curl -fsSL https://opencode.ai/install | bash
```
O con **Homebrew**:
```bash
brew install anomalyco/tap/opencode
```
En **Arch Linux**: `sudo pacman -S opencode`.

---

## 2. Verificar que se ha instalado

En la terminal, ejecuta:
```bash
opencode --version
```

> **¿"comando no encontrado"?** Cierra y vuelve a abrir la terminal. Si sigue sin aparecer, el instalador lo dejó en `~/.local/bin` o `~/bin`; añade esa carpeta al PATH:
> ```bash
> echo 'export PATH="$HOME/.local/bin:$HOME/bin:$PATH"' >> ~/.bashrc
> source ~/.bashrc
> ```

---

## 3. Conectar tu modelo (Groq)

OpenCode no trae modelo propio: hay que **conectarle un proveedor**. Lo haremos **desde dentro de OpenCode**.

1. Arranca OpenCode (en cualquier carpeta, de momento):
   ```bash
   opencode
   ```
2. Dentro de la interfaz, escribe el comando:
   ```
   /connect
   ```
3. Busca y selecciona **Groq** en la lista.
4. **Pega tu clave de API** de Groq (la de `console.groq.com`) y pulsa Enter.
5. Ahora elige el modelo con:
   ```
   /models
   ```
   Para programar, una buena opción gratuita es **`llama-3.3-70b-versatile`**.

> Tus claves se guardan en `~/.local/share/opencode/auth.json`. Para comprobar qué proveedores tienes conectados, en la terminal: `opencode auth list`.

> **¿Prefieres OpenRouter?** Igual, pero en el paso 3 elige **OpenRouter** y pega la clave de `openrouter.ai/settings/keys`. Trae muchos modelos ya cargados.

---
