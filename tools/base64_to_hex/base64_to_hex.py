from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils.base64_utils import decode_base64_to_bytes
from tools.utils.tool_utils import send_text_in_chunks


class Base64ToHexTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        encoded_text: str = tool_parameters.get("encoded_text")
        if not encoded_text:
            return send_text_in_chunks(self, text="")

        urlsafe_enabled = bool("true" == tool_parameters.get("urlsafe_enabled", "").lower())
        try:
            decoded_bytes = decode_base64_to_bytes(encoded_text, urlsafe_enabled)
            result_str = decoded_bytes.hex()
        except Exception as e:
            raise ValueError("Failed to covert Base64 text to Hex text, Exception: " + str(e))

        return send_text_in_chunks(self, text=result_str)
