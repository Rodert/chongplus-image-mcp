# ChongPlus Image MCP

通过 ChongPlus Image API 让 AI 助手生成图片和编辑参考图的 MCP 服务。

[English](../README.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [Español](README.es.md) | [Русский](README.ru.md) | [한국어](README.ko.md)

它面向日常对话使用：安装后，AI 会检查 API Key 是否已配置；只有需要时才询问用户，并将密钥保存到本机。无需环境变量，也无需手动运行 Python 命令。

## 功能

- 检查 ChongPlus 是否已准备就绪。
- 安全保存或替换 ChongPlus API Key。
- 根据提示词生成一到四张图片。
- 根据本地参考图编辑图片。
- 告知 AI 可用尺寸和数量限制。

生成的图片会保存到本机。工具会返回绝对路径，MCP 客户端可以据此打开或展示图片。

## 安装

最简单的方式是让支持 MCP 的 AI 客户端安装此仓库。手动配置时可使用 `uvx`：

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

对于已检出的仓库，请改用：

```json
{
  "command": "uv",
  "args": ["run", "--directory", "/absolute/path/to/chongplus-image-mcp", "chongplus-image-mcp"]
}
```

## 首次使用

请 AI 生成或编辑图片。它会先调用 `setup_status`；若尚未保存密钥，会询问你的 ChongPlus API Key，再调用 `configure_api_key`。

请前往 [ChongPlus Keys](https://api.chongplus.plus/keys) 登录、创建密钥，并选择生图分组。API Key 属于敏感信息，只应提供给你信任的 AI 客户端和本地 MCP 服务。

密钥保存位置：

| 平台 | 路径 |
| --- | --- |
| macOS/Linux | `$XDG_CONFIG_HOME/chongplus-image/config.json`，或 `~/.config/chongplus-image/config.json` |
| Windows | `%APPDATA%\\chongplus-image\\config.json` |

在 macOS/Linux 上，目录权限为 `0700`，文件权限为 `0600`。

## 工具

| 工具 | 用途 |
| --- | --- |
| `setup_status` | 检查本机是否已保存 API Key。 |
| `configure_api_key` | 安全保存用户提供的 API Key；服务不会返回密钥。 |
| `generate_image` | 根据提示词生成图片。 |
| `edit_image` | 使用一张本地图片进行编辑。 |
| `list_image_options` | 列出支持的尺寸和调用限制。 |

`edit_image` 仅接受本地图片路径，不接受 URL；服务也不会返回任意本地文件的内容。

## 开发

需要 Python 3.10 或更高版本及 [uv](https://docs.astral.sh/uv/)。

```bash
uv sync
uv run python -m unittest discover -s tests
uv run chongplus-image-mcp
```

测试离线运行，不需要 API Key。

## 错误说明

- `401` 或 `403`：API Key 可能无效、没有生图模型权限或额度不足。
- `403` 且包含 Cloudflare `1010`：边缘防火墙在 API 处理前拦截了请求，请联系 ChongPlus 支持并提供大致请求时间。
- 网络错误：检查网络连接后重试。

接口的权威说明请以 [ChongPlus Image API 文档](https://api.chongplus.plus/tools/image-studio/docs/) 为准。
