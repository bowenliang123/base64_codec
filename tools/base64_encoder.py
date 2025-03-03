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

        encoded_str: str = base64.b64encode(plain_text.encode("utf-8")).decode("utf-8")
        yield self.create_text_message(encoded_str)
