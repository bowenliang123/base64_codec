import base64
import multiprocessing
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils.image_prefix_utils import extract_mime_type
from tools.utils.string_utils import normalize_splitter, DEFAULT_SPLITTER


class Base64ImageDecoderTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        encoded_text: str = tool_parameters.get("encoded_text")
        output_filename_str: str = tool_parameters.get("output_filename","")
        splitter_str: str = normalize_splitter(tool_parameters.get("splitter_str", DEFAULT_SPLITTER).strip() or DEFAULT_SPLITTER)
        if not encoded_text:
            raise ValueError("Invalid input encoded_text")

        pool_executor: ThreadPoolExecutor = None
        try:
            splitted = [s for s in encoded_text.split(splitter_str) if s]
            output_filenames = [s for s in output_filename_str.split("\n") if s]
            pool_executor = ThreadPoolExecutor(max_workers=min(len(splitted), multiprocessing.cpu_count()))
            with pool_executor as executor:
                futures = {
                    i: executor.submit(
                        self.decode,
                        splitted[i],
                        output_filenames[i] if i < len(output_filenames) else f"output_{i + 1}.bin",
                    )
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
            try:
                comma_index = encoded_text.index(",")
                prefix = encoded_text[:comma_index]
                encoded_text = encoded_text[comma_index:]
                image_mime_type = extract_mime_type(prefix)
            except ValueError:  # ValueError when comma is not found
                image_mime_type = "image/png"

            result_file_bytes = base64.decodebytes(encoded_text.encode())
            meta_data = {
                "mime_type": image_mime_type,
                "filename": output_filename,
            }
            return meta_data, result_file_bytes
        except Exception as e:
            raise RuntimeError(f"Failed to decode base64 text, error: {str(e)}")
