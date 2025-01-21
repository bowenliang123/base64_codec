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

        mime_types_to_prefix = {
            "image/png": "data:image/png;base64,",
            "image/jpeg": "data:image/jpeg;base64,",
            "image/webp": "data:image/webp;base64,",
            "image/svg+xml": "data:image/svg+xml;base64,"
        }
        target_mime_type = "image/png"
        for mime_type, prefix in mime_types_to_prefix.items():
            if encoded_text.startswith(prefix):
                target_mime_type = mime_type
                encoded_text = encoded_text.replace(prefix, "")
                break

        try:
            result_file_bytes = base64.decodebytes(encoded_text.encode())
        except Exception as e:
            raise RuntimeError(f"Failed to decode base64 image to {target_mime_type}, error: {str(e)}")

        yield self.create_blob_message(
            blob=result_file_bytes,
            meta={"mime_type": target_mime_type})
