import base64
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils.image_prefix_utils import PREFIX_TO_MIME_TYPE


class Base64ImageDecodeTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        encoded_text: str = tool_parameters.get("encoded_text")
        if not encoded_text:
            raise ValueError("Invalid input encoded_text")

        image_mime_type = "image/png"
        if "," in encoded_text:
            prefix = encoded_text[:encoded_text.index(",")]
            image_mime_type = PREFIX_TO_MIME_TYPE.get(prefix)
            if not image_mime_type:
                raise ValueError(f"Invalid image prefix in encoded_text: {prefix}")
            encoded_text = encoded_text[encoded_text.index(","):]

        try:
            result_file_bytes = base64.decodebytes(encoded_text.encode())
        except Exception as e:
            raise RuntimeError(f"Failed to decode base64 image to {image_mime_type}, error: {str(e)}")

        yield self.create_blob_message(
            blob=result_file_bytes,
            meta={"mime_type": image_mime_type})
