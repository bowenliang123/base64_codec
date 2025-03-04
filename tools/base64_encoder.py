import base64
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class Base64TextEncodeTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        plain_text: str = tool_parameters.get("plain_text")
        if not plain_text:
            yield self.create_text_message("")
            return

        urlsafe_enabled: bool = ("true" == tool_parameters.get("urlsafe_enabled", "").lower())
        encoded_str: str = ""
        try:
            if urlsafe_enabled:
                encoded_str = base64.urlsafe_b64encode(plain_text.encode("utf-8")).decode("utf-8")
            else:
                encoded_str = base64.b64encode(plain_text.encode("utf-8")).decode("utf-8")
        except Exception as e:
            raise ValueError("Failed to encode text input, Exception: " + str(e))

        yield self.create_text_message(encoded_str)
