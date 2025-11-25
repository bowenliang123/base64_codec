import base64
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File

from tools.utils.tool_utils import send_text_in_chunks


class Base64FileEncoderTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        input_file: File = tool_parameters.get("input_file")
        if not input_file or not isinstance(input_file, File):
            raise ValueError("Not a valid file for input input_file")
        input_file_bytes = input_file.blob

        try:
            result_str = base64.b64encode(input_file_bytes).decode("utf-8")
        except Exception as e:
            raise RuntimeError(f"Failed to encode file to Base64 encoded text, error: {str(e)}")

        return send_text_in_chunks(self, text=result_str)
