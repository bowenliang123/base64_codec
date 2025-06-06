from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils.base64_utils import encode_to_base64, encode_bytes_to_base64


class HexToBase64Tool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        hex_text: str = tool_parameters.get("hex_text")
        try:
            hex_bytes=bytes.fromhex(hex_text)
        except Exception:
            raise ValueError("Failed to decode hex text")

        urlsafe_enabled = bool("true" == tool_parameters.get("urlsafe_enabled", "").lower())
        try:
            result_base_str = encode_bytes_to_base64(hex_bytes, urlsafe_enabled)
        except Exception as e:
            raise ValueError("Failed to encode text input, Exception: " + str(e))

        yield self.create_text_message(result_base_str)
