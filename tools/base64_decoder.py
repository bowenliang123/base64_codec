import base64
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class Base64TextDecodeTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        encoded_text: str = tool_parameters.get("encoded_text")
        if not encoded_text:
            yield self.create_text_message("")
            return

        urlsafe_enabled: bool = ("true" == tool_parameters.get("urlsafe_enabled", "").lower())
        decoded_str: str = ""
        try:
            if urlsafe_enabled:
                decoded_str: str = base64.urlsafe_b64decode(encoded_text.encode("utf-8")).decode("utf-8")
            else:
                decoded_str: str = base64.b64decode(encoded_text.encode("utf-8")).decode("utf-8")
        except Exception as e:
            raise ValueError("Failed to decode Base64 text input, Exception: " + str(e))

        yield self.create_text_message(decoded_str)
