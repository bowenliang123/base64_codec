from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils.base64_utils import encode_to_base64
from tools.utils.tool_utils import send_text_in_chunks


class Base64TextEncoderTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        plain_text: str = tool_parameters.get("plain_text")
        if not plain_text:
            return send_text_in_chunks(self, text="")

        urlsafe_enabled = bool("true" == tool_parameters.get("urlsafe_enabled", "").lower())
        try:
            result_str = encode_to_base64(plain_text, urlsafe_enabled)

        except Exception as e:
            raise ValueError("Failed to encode text input, Exception: " + str(e))

        return send_text_in_chunks(self, text=result_str)
