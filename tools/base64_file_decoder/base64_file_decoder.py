import base64
import mimetypes
from collections.abc import Generator
from tempfile import NamedTemporaryFile
from typing import Any, Optional

import filetype
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class Base64FileDecoderTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        encoded_text: str = tool_parameters.get("encoded_text")
        output_filename: str = tool_parameters.get("output_filename")
        if not encoded_text:
            raise ValueError("Empty input encoded_text")
        if not output_filename:
            raise ValueError("Empty input output_filename")

        try:
            result_file_bytes = base64.decodebytes(encoded_text.encode())
            with NamedTemporaryFile(delete=True) as temp_file:
                temp_file.write(result_file_bytes)
                temp_file.flush()
                mime_type = filetype.guess_mime(temp_file.name)
            if not mime_type:
                mime_type = self.get_mime_type(output_filename)
        except Exception as e:
            raise RuntimeError(f"Failed to decode base64 text, error: {str(e)}")

        yield self.create_blob_message(
            blob=result_file_bytes,
            meta={
                "mime_type": mime_type,
                "filename": output_filename,
            },
        )

    def get_mime_type(self, declared_filename: Optional[str]) -> str:
        if not declared_filename:
            return "application/octet-stream"
        mime_type, _ = mimetypes.guess_type(declared_filename)
        return mime_type or "application/octet-stream"
