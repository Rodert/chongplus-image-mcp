# ChongPlus Image MCP

Un servidor MCP que permite a los asistentes de IA generar y editar imagenes mediante la API de ChongPlus Image.

[English](../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [한국어](README.ko.md)

Esta pensado para conversaciones normales: despues de instalarlo, la IA comprueba si existe una API Key y solo la solicita cuando hace falta; despues la guarda localmente. No se necesitan variables de entorno ni comandos manuales de Python.

## Funciones

- Comprueba si ChongPlus esta listo para usarse.
- Guarda o reemplaza una ChongPlus API Key de forma segura.
- Genera de una a cuatro imagenes a partir de un prompt.
- Edita una imagen local de referencia.
- Indica los tamanos y limites disponibles.

Las imagenes generadas se guardan localmente. Las herramientas devuelven rutas absolutas para que el cliente MCP pueda abrirlas o mostrarlas.

## Instalacion

La forma mas sencilla es pedir a un cliente de IA compatible con MCP que instale este repositorio. Para configurarlo manualmente, use `uvx`:

```json
{
  "mcpServers": {
    "chongplus-image": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/Rodert/chongplus-image-mcp", "chongplus-image-mcp"]
    }
  }
}
```

Para un repositorio ya clonado, use:

```json
{
  "command": "uv",
  "args": ["run", "--directory", "/absolute/path/to/chongplus-image-mcp", "chongplus-image-mcp"]
}
```

## Primer uso

Pida a la IA que genere o edite una imagen. Primero llamara a `setup_status`; si no hay una clave guardada, le pedira su ChongPlus API Key y llamara a `configure_api_key`.

Obtenga una clave en [ChongPlus Keys](https://api.chongplus.plus/keys), iniciando sesion, creando una clave y seleccionando el grupo de generacion de imagenes. La API Key es informacion sensible: compartala solo con un cliente de IA y un servidor MCP local en los que confie.

Ubicacion de la clave:

| Plataforma | Ubicacion |
| --- | --- |
| macOS/Linux | `$XDG_CONFIG_HOME/chongplus-image/config.json` o `~/.config/chongplus-image/config.json` |
| Windows | `%APPDATA%\\chongplus-image\\config.json` |

En macOS/Linux, el directorio usa permiso `0700` y el archivo `0600`.

## Herramientas

| Herramienta | Uso |
| --- | --- |
| `setup_status` | Comprueba si hay una API Key local guardada. |
| `configure_api_key` | Guarda de forma segura la API Key del usuario; el servidor nunca la devuelve. |
| `generate_image` | Genera imagenes desde un prompt. |
| `edit_image` | Edita una imagen local. |
| `list_image_options` | Lista los tamanos y limites admitidos. |

`edit_image` solo acepta una ruta de imagen local, no una URL. El servidor tampoco devuelve el contenido de archivos locales arbitrarios.

## Desarrollo

Requiere Python 3.10 o posterior y [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python -m unittest discover -s tests
uv run chongplus-image-mcp
```

Las pruebas se ejecutan sin conexion y no requieren una API Key.

## Errores

- `401` o `403`: la API Key puede ser invalida, no tener acceso al modelo de imagenes o no tener cuota.
- `403` con Cloudflare `1010`: el firewall perimetral bloqueo la solicitud antes de que la API la procesara. Contacte con el soporte de ChongPlus e indique la hora aproximada de la solicitud.
- Errores de conexion: compruebe su red y vuelva a intentarlo.

La fuente de verdad de la API es la [documentacion de ChongPlus Image API](https://api.chongplus.plus/tools/image-studio/docs/).
