# ChongPlus Image MCP

ChongPlus Image API を使い、AI アシスタントによる画像生成と参照画像の編集を可能にする MCP サーバーです。

[English](../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [Español](README.es.md) | [Русский](README.ru.md) | [한국어](README.ko.md)

通常の会話で使いやすいよう設計されています。インストール後、AI は API Key が設定済みか確認し、必要な場合にのみユーザーへ尋ねてローカルに保存します。環境変数や Python コマンドの手動実行は不要です。

## 機能

- ChongPlus の準備状況を確認
- ChongPlus API Key の安全な保存・更新
- プロンプトから 1〜4 枚の画像を生成
- ローカルの参照画像を編集
- 利用可能な画像サイズと上限を案内

生成画像はローカルに保存され、ツールは絶対パスを返します。MCP クライアントはそのパスから画像を開いたり表示したりできます。

## インストール

以下を MCP 対応 AI クライアントにそのまま貼り付けてください。

```text
ChongPlus Image MCP をインストールして設定してください:
https://github.com/Rodert/chongplus-image-mcp

次のコマンドを使用して、ローカル stdio MCP Server としてインストールしてください:
uvx --from git+https://github.com/Rodert/chongplus-image-mcp chongplus-image-mcp

設定後、setup_status を呼び出して API Key の状態を確認してください。未設定の場合は ChongPlus API Key を私に尋ね、configure_api_key を呼び出してローカル設定に安全に保存してください。その後は保存済みのキーを再利用し、環境変数の設定を求めないでください。
```

手動設定では `uvx` を使用できます。

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

チェックアウト済みリポジトリでは、次を使用してください。

```json
{
  "command": "uv",
  "args": ["run", "--directory", "/absolute/path/to/chongplus-image-mcp", "chongplus-image-mcp"]
}
```

## 初回利用

AI に画像の生成または編集を依頼してください。AI は `setup_status` を呼び出し、キーがなければ ChongPlus API Key を尋ねてから `configure_api_key` を呼び出します。

[ChongPlus Keys](https://api.chongplus.plus/keys) にログインし、画像生成グループを選んでキーを作成してください。API Key は機密情報です。信頼できる AI クライアントとローカル MCP サーバーにのみ渡してください。

キーの保存先：

| プラットフォーム | 保存先 |
| --- | --- |
| macOS/Linux | `$XDG_CONFIG_HOME/chongplus-image/config.json`、または `~/.config/chongplus-image/config.json` |
| Windows | `%APPDATA%\\chongplus-image\\config.json` |

macOS/Linux では、ディレクトリの権限は `0700`、ファイルの権限は `0600` です。

## ツール

| ツール | 用途 |
| --- | --- |
| `setup_status` | ローカルに API Key が保存されているか確認します。 |
| `configure_api_key` | ユーザーの API Key を安全に保存します。キーは返しません。 |
| `generate_image` | プロンプトから画像を生成します。 |
| `edit_image` | ローカル画像を編集します。 |
| `list_image_options` | 対応サイズとリクエスト上限を返します。 |

`edit_image` は URL ではなくローカル画像パスのみ受け付けます。サービスは任意のローカルファイル内容を返しません。

## 開発

Python 3.10 以降と [uv](https://docs.astral.sh/uv/) が必要です。

```bash
uv sync
uv run python -m unittest discover -s tests
uv run chongplus-image-mcp
```

テストはオフラインで実行でき、API Key は不要です。

## エラー

- `401` または `403`：API Key が無効、画像モデルへの権限不足、またはクォータ不足の可能性があります。
- `403` と Cloudflare `1010`：API 処理前にエッジファイアウォールがリクエストをブロックしました。おおよそのリクエスト時刻を添えて ChongPlus サポートへ連絡してください。
- 接続エラー：ネットワーク接続を確認して再試行してください。

API の正しい仕様は [ChongPlus Image API ドキュメント](https://api.chongplus.plus/tools/image-studio/docs/) を参照してください。
