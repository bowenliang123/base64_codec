from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.base64_decoder.base64_decoder import Base64TextDecoderTool
from tools.base64_encoder.base64_encoder import Base64TextEncoderTool
from tools.base64_file_decoder.base64_file_decoder import Base64FileDecoderTool
from tools.base64_file_encoder.base64_file_encoder import Base64FileEncoderTool
from tools.base64_image_decoder.base64_image_decoder import Base64ImageDecoderTool
from tools.base64_image_encoder.base64_image_encoder import Base64ImageEncoderTool
from tools.base64_to_hex.base64_to_hex import Base64ToHexTool
from tools.hex_to_base64.hex_to_base64 import HexToBase64Tool


class Base64CodecProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            """
            IMPLEMENT YOUR VALIDATION HERE
            """
            for tool_cls in [
                Base64TextEncoderTool,
                Base64TextDecoderTool,
                Base64ImageEncoderTool,
                Base64ImageDecoderTool,
                Base64FileEncoderTool,
                Base64FileDecoderTool,
                Base64ToHexTool,
                HexToBase64Tool,
            ]:
                tool_cls.from_credentials({})
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
