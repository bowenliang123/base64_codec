from collections.abc import Generator
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool

DEFAULT_TEXT_CHUNK_SIZE = 512


def send_text_in_chunks(tool: Tool,
                        text: str,
                        chunk_size: int = DEFAULT_TEXT_CHUNK_SIZE
                        ) -> Generator[ToolInvokeMessage]:
    """
    Sends a text message in chunks using the provided tool.
    :param tool:
    :param text:
    :param chunk_size:
    :return:
    """
    for i in range(0, len(text), chunk_size):
        yield tool.create_text_message(text=text[i:i + chunk_size])
