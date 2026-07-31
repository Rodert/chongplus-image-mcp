# ChongPlus Image MCP

ChongPlus Image API를 통해 AI 어시스턴트가 이미지를 생성하고 참조 이미지를 편집할 수 있게 해 주는 MCP 서버입니다.

[English](../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [Español](README.es.md) | [Русский](README.ru.md)

일반 대화에서 쉽게 사용하도록 설계되었습니다. 설치 후 AI가 API Key 설정 여부를 확인하고, 필요한 경우에만 사용자에게 요청하여 로컬에 저장합니다. 환경 변수나 Python 명령을 직접 실행할 필요가 없습니다.

## 기능

- ChongPlus 사용 준비 상태 확인
- ChongPlus API Key의 안전한 저장 또는 교체
- 프롬프트로 1~4장의 이미지 생성
- 로컬 참조 이미지 편집
- 지원되는 이미지 크기와 제한 안내

생성된 이미지는 로컬에 저장됩니다. 도구는 MCP 클라이언트가 이미지를 열거나 표시할 수 있는 절대 경로를 반환합니다.

## 설치

다음을 MCP 지원 AI 클라이언트에 그대로 붙여 넣으세요.

```text
ChongPlus Image MCP를 설치하고 설정해 주세요:
https://github.com/Rodert/chongplus-image-mcp

다음 명령으로 로컬 stdio MCP Server로 설치해 주세요:
uvx --from git+https://github.com/Rodert/chongplus-image-mcp chongplus-image-mcp

설정이 끝나면 setup_status를 호출하여 API Key 상태를 확인해 주세요. 설정되어 있지 않다면 ChongPlus API Key를 요청하고 configure_api_key를 호출하여 로컬 설정에 안전하게 저장해 주세요. 이후에는 저장된 키를 재사용하고 환경 변수 설정을 요구하지 마세요.
```

수동 설정에는 `uvx`를 사용하세요.

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

이미 체크아웃한 저장소에는 다음을 사용하세요.

```json
{
  "command": "uv",
  "args": ["run", "--directory", "/absolute/path/to/chongplus-image-mcp", "chongplus-image-mcp"]
}
```

## 처음 사용

AI에게 이미지 생성 또는 편집을 요청하세요. AI는 먼저 `setup_status`를 호출하며, 저장된 키가 없으면 ChongPlus API Key를 요청한 후 `configure_api_key`를 호출합니다.

[ChongPlus Keys](https://api.chongplus.plus/keys)에 로그인하여 키를 만들고 이미지 생성 그룹을 선택하세요. API Key는 민감한 정보이므로 신뢰할 수 있는 AI 클라이언트와 로컬 MCP 서버에만 제공하세요.

키 저장 위치:

| 플랫폼 | 위치 |
| --- | --- |
| macOS/Linux | `$XDG_CONFIG_HOME/chongplus-image/config.json` 또는 `~/.config/chongplus-image/config.json` |
| Windows | `%APPDATA%\\chongplus-image\\config.json` |

macOS/Linux에서는 디렉터리에 `0700`, 파일에 `0600` 권한이 적용됩니다.

## 도구

| 도구 | 용도 |
| --- | --- |
| `setup_status` | 로컬 API Key가 저장되었는지 확인합니다. |
| `configure_api_key` | 사용자의 API Key를 안전하게 저장하며 서버는 키를 반환하지 않습니다. |
| `generate_image` | 프롬프트에서 이미지를 생성합니다. |
| `edit_image` | 로컬 이미지를 편집합니다. |
| `list_image_options` | 지원되는 크기와 요청 제한을 보여 줍니다. |

`edit_image`는 URL이 아닌 로컬 이미지 경로만 받습니다. 서버는 임의의 로컬 파일 내용도 반환하지 않습니다.

## 개발

Python 3.10 이상과 [uv](https://docs.astral.sh/uv/)가 필요합니다.

```bash
uv sync
uv run python -m unittest discover -s tests
uv run chongplus-image-mcp
```

테스트는 오프라인으로 실행되며 API Key가 필요하지 않습니다.

## 오류

- `401` 또는 `403`: API Key가 유효하지 않거나, 이미지 모델 접근 권한 또는 할당량이 없을 수 있습니다.
- Cloudflare `1010`이 포함된 `403`: API가 처리하기 전에 에지 방화벽이 요청을 차단했습니다. 대략적인 요청 시간과 함께 ChongPlus 지원팀에 문의하세요.
- 연결 오류: 네트워크를 확인한 후 다시 시도하세요.

API의 기준 문서는 [ChongPlus Image API 문서](https://api.chongplus.plus/tools/image-studio/docs/)입니다.
