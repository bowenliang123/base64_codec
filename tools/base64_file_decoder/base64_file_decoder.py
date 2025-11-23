import base64
import mimetypes
import multiprocessing
import uuid
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor
from tempfile import NamedTemporaryFile
from typing import Any, Optional

import filetype
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class Base64FileDecoderTool(Tool):

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        encoded_text: str = tool_parameters.get("encoded_text", "")
        output_filename_str: str = tool_parameters.get("output_filename", str(uuid.uuid4()) + ".bin")
        splitter: str = tool_parameters.get("splitter_str") or '\n\n'
        if not encoded_text:
            raise ValueError("Empty input encoded_text")

        pool_executor: ThreadPoolExecutor = None
        try:
            # normalize splitter
            splitter = splitter.replace('\\n', '\n')
            splitted = [s for s in encoded_text.split(splitter) if s]
            print(f"splitted: {splitted}")
            output_filenames = [s for s in output_filename_str.split("\n") if s]
            pool_executor = ThreadPoolExecutor(max_workers=min(len(splitted), multiprocessing.cpu_count()))
            with pool_executor as executor:
                futures = {
                    i: executor.submit(self.decode,
                                       encoded_text,
                                       output_filenames[i] if i < len(output_filenames) else f"output_{i + 1}.bin")
                    for i, encoded_text in enumerate(splitted)
                }
                for i in sorted(futures.keys()):
                    meta_data, result_file_bytes = futures[i].result()
                    if result_file_bytes:
                        yield self.create_blob_message(blob=result_file_bytes, meta=meta_data)
        finally:
            if pool_executor:
                pool_executor.shutdown(wait=False, cancel_futures=True)

    def decode(self, encoded_text: str, output_filename: str) -> tuple[dict[str, Any], bytes]:
        try:
            result_file_bytes = base64.decodebytes(encoded_text.encode())
            filetype_type: Optional[filetype.Type] = None
            with NamedTemporaryFile(delete=True) as temp_file:
                temp_file.write(result_file_bytes)
                temp_file.flush()
                filetype_type = filetype.guess(temp_file.name)

            if filetype_type:
                mime_type = filetype_type.mime

                # ensure the output filename has the correct extension
                extension = filetype_type.extension
                if not output_filename.endswith(f".{extension}"):
                    output_filename = f"{output_filename}.{extension}"
            else:
                mime_type = self.get_mime_type(output_filename)
            meta_data = {
                "mime_type": mime_type,
                "filename": output_filename,
            }
            return meta_data, result_file_bytes

        except Exception as e:
            raise RuntimeError(f"Failed to decode base64 text, error: {str(e)}")

    def get_mime_type(self, declared_filename: Optional[str]) -> str:
        if not declared_filename:
            return "application/octet-stream"
        mime_type, _ = mimetypes.guess_type(declared_filename)
        return mime_type or "application/octet-stream"
