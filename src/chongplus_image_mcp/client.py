"""Small, dependency-free client for the ChongPlus Image API."""

from __future__ import annotations

import base64
import json
import mimetypes
import os
import secrets
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

BASE_URL = "https://api.chongplus.plus"
MODEL = "gpt-image-2"
SIZES = ("1024x1024", "2048x2048", "1536x1024", "1024x1536", "3840x2160", "2160x3840")
MAX_IMAGES = 4


class ChongPlusError(RuntimeError):
    """An error safe to show to an MCP client."""


@dataclass(frozen=True)
class GeneratedImage:
    path: Path
    width: int | None = None
    height: int | None = None


def config_path() -> Path:
    if os.name == "nt":
        root = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return root / "chongplus-image" / "config.json"


def _private_mode(path: Path, mode: int) -> None:
    if os.name != "nt":
        os.chmod(path, mode)


def save_api_key(api_key: str) -> None:
    key = api_key.strip()
    if not key:
        raise ChongPlusError("The API key cannot be empty.")
    path = config_path()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    _private_mode(path.parent, 0o700)
    temporary = path.parent / f".{path.name}.{secrets.token_hex(8)}.tmp"
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            _private_mode(temporary, 0o600)
            json.dump({"api_key": key}, handle)
            handle.write("\n")
        os.replace(temporary, path)
        _private_mode(path, 0o600)
    finally:
        if temporary.exists():
            temporary.unlink()


def is_configured() -> bool:
    try:
        with config_path().open(encoding="utf-8") as handle:
            return bool(json.load(handle).get("api_key", "").strip())
    except (OSError, json.JSONDecodeError):
        return False


def _load_api_key() -> str:
    try:
        with config_path().open(encoding="utf-8") as handle:
            key = json.load(handle).get("api_key", "").strip()
    except (OSError, json.JSONDecodeError):
        key = ""
    if not key:
        raise ChongPlusError(
            "ChongPlus is not configured. Ask the user for their ChongPlus API key, "
            "then call configure_api_key. They can create a key at https://api.chongplus.plus/keys."
        )
    return key


def _request(endpoint: str, body: bytes, content_type: str) -> dict:
    headers = {
        "Authorization": f"Bearer {_load_api_key()}",
        "Content-Type": content_type,
        "Accept": "application/json",
        "User-Agent": "ChongPlusImageMCP/0.1 (local MCP server)",
    }
    request = urllib.request.Request(BASE_URL + endpoint, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            raw = response.read()
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")[:1000]
        if error.code == 403 and "1010" in details:
            raise ChongPlusError(
                "ChongPlus's Cloudflare edge firewall blocked this request (error 1010) before the API handled it. "
                "Ask the ChongPlus operator to inspect its Cloudflare events for the request time."
            ) from error
        if error.code in (401, 403):
            raise ChongPlusError(
                f"ChongPlus rejected the request (HTTP {error.code}). The API key may be invalid, lack image access, or have no quota."
            ) from error
        raise ChongPlusError(f"ChongPlus API request failed with HTTP {error.code}: {details}") from error
    except urllib.error.URLError as error:
        raise ChongPlusError(f"Could not reach ChongPlus: {error.reason}") from error
    if not raw:
        raise ChongPlusError("ChongPlus returned an empty response.")
    try:
        result = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as error:
        raise ChongPlusError("ChongPlus returned an unexpected non-JSON response.") from error
    if not isinstance(result, dict):
        raise ChongPlusError("ChongPlus returned an unexpected response.")
    return result


def _multipart(fields: dict[str, str | int], image_path: Path) -> tuple[bytes, str]:
    boundary = "----ChongPlus" + secrets.token_hex(16)
    parts: list[bytes] = []
    for name, value in fields.items():
        parts.extend((
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
            str(value).encode(),
            b"\r\n",
        ))
    mime_type = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
    parts.extend((
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="image"; filename="{image_path.name}"\r\n'.encode(),
        f"Content-Type: {mime_type}\r\n\r\n".encode(),
        image_path.read_bytes(),
        b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ))
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def _image_extension(content_type: str) -> str:
    return {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp"}.get(
        content_type.split(";", 1)[0].lower(), "png"
    )


def _png_dimensions(raw: bytes) -> tuple[int, int] | None:
    if raw[:8] == b"\x89PNG\r\n\x1a\n" and raw[12:16] == b"IHDR":
        return int.from_bytes(raw[16:20], "big"), int.from_bytes(raw[20:24], "big")
    return None


def _validate_request(size: str, count: int) -> None:
    if size not in SIZES:
        raise ChongPlusError(f"Unsupported size: {size}. Choose one of: {', '.join(SIZES)}.")
    if not 1 <= count <= MAX_IMAGES:
        raise ChongPlusError(f"count must be between 1 and {MAX_IMAGES}.")


def _save_results(response: dict, output_directory: Path) -> list[GeneratedImage]:
    entries = response.get("data")
    if not isinstance(entries, list) or not entries:
        raise ChongPlusError("ChongPlus returned no image data.")
    output_directory.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    request_id = secrets.token_hex(4)
    results: list[GeneratedImage] = []
    for index, item in enumerate(entries, 1):
        if not isinstance(item, dict):
            raise ChongPlusError("ChongPlus returned invalid image metadata.")
        if "b64_json" in item:
            try:
                raw = base64.b64decode(item["b64_json"], validate=True)
            except (ValueError, TypeError) as error:
                raise ChongPlusError("ChongPlus returned invalid Base64 image data.") from error
            extension = "png"
        elif "url" in item:
            try:
                with urllib.request.urlopen(item["url"], timeout=300) as download:
                    raw = download.read()
                    extension = _image_extension(download.headers.get_content_type())
            except urllib.error.URLError as error:
                raise ChongPlusError(f"Could not download the generated image: {error.reason}") from error
        else:
            raise ChongPlusError("A ChongPlus image result has neither image data nor a download URL.")
        path = output_directory / f"chongplus-{timestamp}-{request_id}-{index}.{extension}"
        path.write_bytes(raw)
        dimensions = _png_dimensions(raw)
        results.append(GeneratedImage(path.resolve(), *(dimensions or (None, None))))
    return results


def generate(prompt: str, size: str, count: int, output_directory: Path) -> list[GeneratedImage]:
    _validate_request(size, count)
    if not prompt.strip():
        raise ChongPlusError("The prompt cannot be empty.")
    body = json.dumps({"model": MODEL, "prompt": prompt, "size": size, "n": count, "response_format": "b64_json"}).encode()
    return _save_results(_request("/v1/images/generations", body, "application/json"), output_directory)


def edit(image_path: Path, prompt: str, size: str, count: int, output_directory: Path) -> list[GeneratedImage]:
    _validate_request(size, count)
    if not prompt.strip():
        raise ChongPlusError("The prompt cannot be empty.")
    image_path = image_path.expanduser().resolve()
    if not image_path.is_file():
        raise ChongPlusError(f"The image file does not exist: {image_path}")
    body, content_type = _multipart({"model": MODEL, "prompt": prompt, "size": size, "n": count}, image_path)
    return _save_results(_request("/v1/images/edits", body, content_type), output_directory)
