# ChongPlus Image MCP

An MCP server that lets AI assistants generate and edit images through the ChongPlus Image API.

Languages: [English](README.md) | [简体中文](docs/README.zh-CN.md) | [繁體中文](docs/README.zh-TW.md) | [日本語](docs/README.ja.md) | [Español](docs/README.es.md) | [Русский](docs/README.ru.md) | [한국어](docs/README.ko.md)

It is designed for normal chat usage: after installation, the assistant checks whether a key is configured, asks for one only when necessary, and saves it in the user's local configuration directory. Users do not need to set environment variables or run Python commands.

## What the assistant can do

- Check whether ChongPlus is ready to use.
- Save or replace a ChongPlus API key securely.
- Generate one to four images from a prompt.
- Edit one local reference image with a prompt.
- Explain available image sizes and limits.

Generated images are saved locally. The tools return their absolute paths, so an MCP client can show or open them.

## Install

The simplest route is to ask an MCP-capable AI client to install this repository. For manual configuration, use `uvx`:

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

For a checked-out repository, replace the command and arguments with:

```json
{
  "command": "uv",
  "args": ["run", "--directory", "/absolute/path/to/chongplus-image-mcp", "chongplus-image-mcp"]
}
```

## First use

Ask the assistant to generate or edit an image. It should call `setup_status` first. If no key exists, it asks you for a ChongPlus API key and calls `configure_api_key`.

Get a key from <https://api.chongplus.plus/keys>; choose the image-generation group. Treat this as sensitive information: only provide it to an AI client and local MCP server you trust.

The key is stored at:

| Platform | Location |
| --- | --- |
| macOS/Linux | `$XDG_CONFIG_HOME/chongplus-image/config.json`, or `~/.config/chongplus-image/config.json` |
| Windows | `%APPDATA%\\chongplus-image\\config.json` |

On macOS and Linux, the directory is set to `0700` and the file to `0600`.

## Tools

| Tool | Purpose |
| --- | --- |
| `setup_status` | Returns whether a local API key has been saved. |
| `configure_api_key` | Securely saves a supplied API key. The server never returns it. |
| `generate_image` | Generates images from a prompt. |
| `edit_image` | Edits a local image using a prompt. |
| `list_image_options` | Lists supported sizes and request limits. |

The server accepts existing local files for editing. It does not accept URLs, and it never returns file contents from arbitrary local paths.

## Development

Requires Python 3.10 or newer and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python -m unittest discover -s tests
uv run chongplus-image-mcp
```

Tests are offline and do not require an API key.

## Errors

- `401` or `403`: the API key may be invalid, lack image-model access, or have no remaining quota.
- `403` with Cloudflare `1010`: ChongPlus's edge firewall blocked the request before the API processed it. Contact ChongPlus support with the approximate request time.
- Connection errors: check your internet connection and retry.

The API source of truth is <https://api.chongplus.plus/tools/image-studio/docs/>.
