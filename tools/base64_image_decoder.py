import base64
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class Base64ImageDecodeTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        encoded_text: str = tool_parameters.get("encoded_text")
        if not encoded_text:
            raise ValueError("Invalid input encoded_text")

        target_mime_type = "image/png"
        if encoded_text.startswith("data:image/jpeg;base64,"):
            target_mime_type = "image/jpeg"
            encoded_text = encoded_text.replace("data:image/jpeg;base64,", "")
        elif encoded_text.startswith("data:image/png;base64,"):
            target_mime_type = "image/png"
            encoded_text = encoded_text.replace("data:image/png;base64,", "")
        elif encoded_text.startswith("data:image/webp;base64,"):
            target_mime_type = "image/webp"
            encoded_text = encoded_text.replace("data:image/webp;base64,", "")
        elif encoded_text.startswith("data:image/svg+xml;base64,"):
            target_mime_type = "image/svg+xml"
            encoded_text = encoded_text.replace("data:image/svg+xml;base64,", "")

        try:
            result_file_bytes = base64.decodebytes(encoded_text.encode())
        except Exception as e:
            raise RuntimeError(f"Failed to decode base64 image to {target_mime_type}, error: {str(e)}")

        yield self.create_blob_message(
            blob=result_file_bytes,
            meta={"mime_type": target_mime_type})
