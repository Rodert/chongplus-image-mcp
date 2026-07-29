# ChongPlus Image MCP

透過 ChongPlus Image API 讓 AI 助手產生圖片與編輯參考圖的 MCP 服務。

[English](../README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md) | [Русский](README.ru.md) | [한국어](README.ko.md)

此服務專為一般對話使用：安裝後，AI 會檢查 API Key 是否已設定，只在需要時詢問使用者，並將金鑰儲存在本機。不需要環境變數，也不需要手動執行 Python 指令。

## 功能

- 檢查 ChongPlus 是否可使用。
- 安全儲存或取代 ChongPlus API Key。
- 依提示詞產生一到四張圖片。
- 使用本機參考圖編輯圖片。
- 提供支援的尺寸與數量限制。

產生的圖片會儲存在本機。工具會回傳絕對路徑，MCP 客戶端可用來開啟或顯示圖片。

## 安裝

最簡單的方式是請支援 MCP 的 AI 客戶端安裝此倉庫。手動設定時可使用 `uvx`：

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

對已檢出的倉庫，請改用：

```json
{
  "command": "uv",
  "args": ["run", "--directory", "/absolute/path/to/chongplus-image-mcp", "chongplus-image-mcp"]
}
```

## 第一次使用

請 AI 產生或編輯圖片。它會先呼叫 `setup_status`；若尚未儲存金鑰，會詢問你的 ChongPlus API Key，接著呼叫 `configure_api_key`。

請到 [ChongPlus Keys](https://api.chongplus.plus/keys) 登入、建立金鑰並選擇生圖群組。API Key 是敏感資訊，僅應提供給信任的 AI 客戶端與本機 MCP 服務。

金鑰儲存位置：

| 平台 | 位置 |
| --- | --- |
| macOS/Linux | `$XDG_CONFIG_HOME/chongplus-image/config.json`，或 `~/.config/chongplus-image/config.json` |
| Windows | `%APPDATA%\\chongplus-image\\config.json` |

在 macOS/Linux，目錄權限為 `0700`，檔案權限為 `0600`。

## 工具

| 工具 | 用途 |
| --- | --- |
| `setup_status` | 檢查本機是否已有 API Key。 |
| `configure_api_key` | 安全儲存使用者提供的 API Key；服務不會回傳金鑰。 |
| `generate_image` | 依提示詞產生圖片。 |
| `edit_image` | 以一張本機圖片進行編輯。 |
| `list_image_options` | 列出支援的尺寸與呼叫限制。 |

`edit_image` 僅接受本機圖片路徑，不接受 URL；服務不會回傳任意本機檔案的內容。

## 開發

需要 Python 3.10 以上與 [uv](https://docs.astral.sh/uv/)。

```bash
uv sync
uv run python -m unittest discover -s tests
uv run chongplus-image-mcp
```

測試離線執行，不需要 API Key。

## 錯誤說明

- `401` 或 `403`：API Key 可能無效、缺少生圖模型權限，或額度不足。
- `403` 且包含 Cloudflare `1010`：邊緣防火牆在 API 處理前攔截請求。請聯絡 ChongPlus 支援並提供大約的請求時間。
- 網路錯誤：請檢查網路連線後重試。

端點的權威說明請以 [ChongPlus Image API 文件](https://api.chongplus.plus/tools/image-studio/docs/) 為準。
