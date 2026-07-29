"""The stdio MCP server exposed to AI clients."""

from __future__ import annotations

from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .client import MAX_IMAGES, MODEL, SIZES, ChongPlusError, edit, generate, is_configured, save_api_key

mcp = FastMCP("ChongPlus Image")


def _default_output_directory() -> Path:
    return Path.cwd() / "outputs"


def _result_payload(images: list) -> dict:
    return {
        "images": [
            {"path": str(image.path), "width": image.width, "height": image.height}
            for image in images
        ],
        "message": "Images were saved locally. Use the absolute paths above to open or attach them.",
    }


@mcp.tool()
def setup_status() -> dict:
    """Check whether this computer has a saved ChongPlus API key. Call this before image generation when setup is uncertain."""
    configured = is_configured()
    return {
        "configured": configured,
        "message": (
            "ChongPlus is ready to use."
            if configured
            else "No ChongPlus API key is saved. Ask the user for their key from https://api.chongplus.plus/keys, then call configure_api_key."
        ),
    }


@mcp.tool()
def configure_api_key(api_key: str) -> dict:
    """Save a user's ChongPlus API key locally. api_key is sensitive: never repeat it in chat, logs, or tool results."""
    try:
        save_api_key(api_key)
    except ChongPlusError as error:
        return {"configured": False, "error": str(error)}
    return {"configured": True, "message": "ChongPlus API key saved securely on this computer."}


@mcp.tool()
def list_image_options() -> dict:
    """List ChongPlus image generation limits. Use this to choose a supported image size or count."""
    return {"model": MODEL, "sizes": list(SIZES), "minimum_count": 1, "maximum_count": MAX_IMAGES}


@mcp.tool()
def generate_image(prompt: str, size: str = "2048x2048", count: int = 1, output_directory: str | None = None) -> dict:
    """Generate one to four images from a prompt and save them locally. Returns absolute image paths."""
    destination = Path(output_directory).expanduser() if output_directory else _default_output_directory()
    try:
        return _result_payload(generate(prompt, size, count, destination))
    except ChongPlusError as error:
        return {"error": str(error)}


@mcp.tool()
def edit_image(image_path: str, prompt: str, size: str = "2048x2048", count: int = 1, output_directory: str | None = None) -> dict:
    """Edit one existing local image with a prompt and save the result locally. image_path must be a local file path, not a URL."""
    destination = Path(output_directory).expanduser() if output_directory else _default_output_directory()
    try:
        return _result_payload(edit(Path(image_path), prompt, size, count, destination))
    except ChongPlusError as error:
        return {"error": str(error)}


def main() -> None:
    mcp.run(transport="stdio")
